"""Semantic cache identities and verified, additive migration of legacy keys.

No executable historical code is loaded: Git blobs are hashed/AST-inspected.
Legacy contexts/answers/verdicts never leave the local SQLite database.
"""
import ast
import hashlib
import inspect
import json
from pathlib import Path
import subprocess

from eval.generation_runtime import fingerprint
from eval.generation_core import validate_faith, validate_accuracy

# This is the inspected runner at f209eb3 (also ca7bbd8), before the transport fix.
# Unknown legacy behavior is not automatically promoted into semantic aliases.
LEGACY_RUNNER_SHA = '2d89c79c89b887d579716eac907f4fd20b3698d0b948d1054dc89a75b5764b1d'
API_PACKAGES = ('langchain-google-genai', 'langchain-core', 'google-genai')


def sha_bytes(value):
    return hashlib.sha256(value).hexdigest()


def literals(source):
    result = {}
    for node in ast.parse(source).body:
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Constant):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    result[target.id] = node.value.value
    return result


def function_ast(source, name):
    node = next(n for n in ast.parse(source).body if isinstance(n, ast.FunctionDef) and n.name == name)
    return ast.dump(node, include_attributes=False)


def model_identity(metadata):
    """Descriptions/defaults are not generation behavior; provider versions are."""
    return {name: metadata.get('metadata', metadata).get(name) for name in ('name', 'version')}


def common_identity(root, freeze, packages):
    return {'dataset': freeze['questions_sha256'], 'annotations': freeze['annotations_sha256'],
            'production_chain_sha256': sha_bytes((root/'src/RAG/chain.py').read_bytes()),
            'api_packages': {name: packages.get(name) for name in API_PACKAGES}}


def context_binding(question, common, baseline_sha, retrieval_config, corpus_sha):
    return {'semantic_cache_schema': 2, 'stage': 'context', 'question': question,
            'dataset': common['dataset'], 'production_chain_sha256': common['production_chain_sha256'],
            'retrieval_baseline': baseline_sha, 'retrieval_config': retrieval_config,
            'corpus_manifest_sha256': corpus_sha}


def generation_binding(question, context, formatted, prompt, generator, common, metadata):
    return {'semantic_cache_schema': 2, 'stage': 'generation', 'question': question,
            'generator': generator, 'prompt': prompt, 'context_hash': fingerprint(context),
            'formatted_context_hash': fingerprint(formatted), 'common': common,
            'provider_model': model_identity(metadata), 'contract': 'production_prompt_StrOutputParser_v1'}


def judge_request(prompt, data):
    # Preserve the original exact serialization, including insertion order/spaces.
    return prompt+'\nINPUT JSON:\n'+json.dumps(data, ensure_ascii=False)


def judge_binding(stage, prompt, data, judge, common, metadata):
    validator = validate_faith if stage == 'faith' else validate_accuracy
    contract = function_ast(inspect.getsource(validator), validator.__name__)
    return {'semantic_cache_schema': 2, 'stage': stage, 'request': judge_request(prompt, data),
            'judge': judge, 'common': common, 'provider_model': model_identity(metadata),
            'response_mime_type': 'application/json', 'validator_ast_sha256': fingerprint(contract)}


def judge_inputs(question, context, answer, notes):
    return {
        'faith': {'question': question['question'], 'answer': answer, 'context': context},
        'accuracy': {'question': question['question'], 'answer': answer,
                     'gold_answer': question['gold_answer'], 'notes': question['notes'],
                     'annotation_notes': notes, 'category': question['category']}}


def verify_context(context, question_id, baseline):
    """Order/content/page references must match Phase 2A for answerable questions."""
    ranking = {r['id']: r for r in baseline['systems']['mmr']['per_question']}
    if question_id in ranking:
        docs = context['documents']; row = ranking[question_id]
        if [sha_bytes(d['page_content'].encode()) for d in docs] != row['chunk_sha256']:
            raise ValueError('Legacy context content/order differs from Phase 2A')
        refs = [{'source': Path(d['metadata']['source']).name, 'page': d['metadata']['page']} for d in docs]
        if refs != row['ranked_pages']:
            raise ValueError('Legacy context references differ from Phase 2A')


def migrate_legacy(root, cache, cfg, freeze, questions, packages, format_docs,
                   production_prompt, faith_prompt, accuracy_prompt):
    """Reconstruct exact old keys, verify provenance, then alias unchanged payloads.

    A hash miss is never filled by nearest-question/model matching. Operational
    hashes are removed only after proving the original complete binding.
    """
    common = common_identity(root, freeze, packages)
    annotations = json.loads((root/'eval/evidence_annotations.json').read_text())['annotations']
    baseline_path = root/cfg['retrieval_result']
    baseline = json.loads(baseline_path.read_text())
    baseline_sha = sha_bytes(baseline_path.read_bytes())
    corpus_sha = sha_bytes((root/'eval/corpus_manifest.json').read_bytes())
    retrieval_cfg = __import__('yaml').safe_load((root/'eval/config.yaml').read_text())
    report = {'matched': {'context': 0, 'generation': 0, 'faith': 0, 'accuracy': 0},
              'sources': [], 'skipped': []}
    anchor = None
    for path in sorted((root/'eval/generation_results').glob('*.json')):
        old = json.loads(path.read_text())
        if not old.get('model_access', {}).get('generator', {}).get('metadata'):
            continue
        try:
            if (old['dataset_sha256'] != common['dataset'] or old['annotations_sha256'] != common['annotations'] or
                    old['phase2a_result_sha256'] != baseline_sha):
                raise ValueError('dataset_or_baseline_mismatch')
            blobs = {}
            for name, digest in old['code_sha256'].items():
                blob = subprocess.check_output(['git', 'show', old['commit']+':'+name], cwd=root, stderr=subprocess.DEVNULL)
                if sha_bytes(blob) != digest:
                    raise ValueError('historical_code_binding_not_verified')
                blobs[name] = blob.decode()
            if old['code_sha256'].get('eval/run_generation.py') != LEGACY_RUNNER_SHA:
                raise ValueError('unrecognized_legacy_runner')
            if old['code_sha256']['src/RAG/chain.py'] != common['production_chain_sha256']:
                raise ValueError('production_behavior_changed')
            for validator in (validate_faith, validate_accuracy):
                if function_ast(blobs['eval/generation_core.py'], validator.__name__) != function_ast(inspect.getsource(validator), validator.__name__):
                    raise ValueError('judge_schema_changed')
            old_prompts = literals(blobs['eval/run_generation.py'])
            if old_prompts['FAITH_PROMPT'] != faith_prompt or old_prompts['ACCURACY_PROMPT'] != accuracy_prompt:
                raise ValueError('judge_prompt_changed')
            if literals(blobs['src/RAG/chain.py'])['DEFAULT_PROMPT_TEMPLATE'] != production_prompt:
                raise ValueError('generator_prompt_changed')
            if any(old['packages'].get(n) != packages.get(n) for n in API_PACKAGES):
                raise ValueError('api_package_versions_changed')
            if old['config']['generator'] != cfg['generator']:
                raise ValueError('generator_configuration_changed')
        except (ValueError, KeyError, StopIteration, subprocess.CalledProcessError) as exc:
            report['skipped'].append({'file': path.name, 'reason': str(exc) if isinstance(exc, ValueError) else type(exc).__name__})
            continue
        report['sources'].append({'file': path.name, 'sha256': sha_bytes(path.read_bytes()), 'commit': old['commit']})
        versions = {'code': old['code_sha256'], 'packages': old['packages'],
                    'generator_metadata': old['model_access']['generator'], 'dataset': old['dataset_sha256'],
                    'annotations': old['annotations_sha256']}
        metadata = old['model_access']
        anchor = old  # last verified run; no network or metadata substitution
        provenance = {'legacy_result_sha256': sha_bytes(path.read_bytes()), 'commit': old['commit']}
        for q in questions:
            cb = {'stage': 'context', 'question': q['question'], 'retrieval_baseline': baseline_sha, 'versions': versions}
            old_key = fingerprint(cb); context = cache.get(old_key)
            if context is None:
                continue
            verify_context(context, q['id'], baseline)
            cache.alias(context_binding(q['question'], common, baseline_sha, retrieval_cfg, corpus_sha), old_key, provenance)
            report['matched']['context'] += 1
            formatted = format_docs(context)
            gb = {'stage': 'generation', 'question': q['question'], 'generator': cfg['generator'],
                  'prompt': production_prompt, 'context_hash': fingerprint(context), 'versions': versions}
            old_key = fingerprint(gb); answer = cache.get(old_key)
            if answer is None:
                continue
            cache.alias(generation_binding(q['question'], context, formatted, production_prompt, cfg['generator'], common, metadata['generator']), old_key, provenance)
            report['matched']['generation'] += 1
            if old['config']['judge'] != cfg['judge'] or 'judge' not in metadata:
                continue
            inputs = judge_inputs(q, formatted, answer['answer'], annotations[q['id']]['notes'])
            for stage, prompt in [('faith', faith_prompt), ('accuracy', accuracy_prompt)]:
                jb = {'stage': stage, 'prompt': prompt, 'data': inputs[stage], 'judge': cfg['judge'],
                      'judge_metadata': metadata['judge'], 'versions': versions}
                old_key = fingerprint(jb); verdict = cache.get(old_key)
                if verdict is None:
                    continue
                if stage == 'faith':
                    validate_faith(verdict['verdict'], len(context['documents']))
                else:
                    validate_accuracy(verdict['verdict'])
                cache.alias(judge_binding(stage, prompt, inputs[stage], cfg['judge'], common, metadata['judge']), old_key, provenance)
                report['matched'][stage] += 1
    return report, anchor
