#!/usr/bin/env python3
"""Preflight or bounded judge-only smoke, isolated from Gemini judge aggregates."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from eval.run_generation import (sha, package_versions, format_context, original_prompt,
    FAITH_PROMPT, ACCURACY_PROMPT, context_key, generation_key, success_inventory, public_stages,
    evaluate_judges, progress_logger)
from eval.generation_cache import (migrate_legacy, common_identity, judge_inputs, judge_request,
                                   API_PACKAGES)
from eval.generation_runtime import CallCache, Caller, fingerprint
from eval.judge_providers import credential, make_judge, schema, token_estimate, throughput_ok


def main():
    import yaml
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--provider',choices=['groq','gemini'],default='groq')
    parser.add_argument('--question',default='F01')
    parser.add_argument('--smoke',action='store_true',help='At most two judge attempts; otherwise offline preflight only')
    args=parser.parse_args()
    cfg=yaml.safe_load((ROOT/'eval/generation_config.yaml').read_text())
    freeze=json.loads((ROOT/'eval/dataset_freeze.json').read_text())
    assert sha(ROOT/'eval/questions.jsonl')==freeze['questions_sha256']
    assert sha(ROOT/'eval/evidence_annotations.json')==freeze['annotations_sha256']
    questions=[q for q in map(json.loads,(ROOT/'eval/questions.jsonl').read_text().splitlines()) if q['status']=='validated']
    assert [q['id'] for q in questions]==freeze['approved_ids']
    packages=package_versions(API_PACKAGES)
    common=common_identity(ROOT,freeze,packages)
    baseline=ROOT/cfg['retrieval_result']
    state={'baseline_sha':sha(baseline),'corpus_sha':sha(ROOT/'eval/corpus_manifest.json'),
           'retrieval_config':yaml.safe_load((ROOT/'eval/config.yaml').read_text())}
    cache=CallCache(ROOT/cfg['cache']);before=success_inventory(cache)
    migration,anchor=migrate_legacy(ROOT,cache,cfg,freeze,questions,packages,format_context,
                                    original_prompt(),FAITH_PROMPT,ACCURACY_PROMPT)
    if anchor is None: raise ValueError('Verified historical generation provenance required')
    q=next(q for q in questions if q['id']==args.question)
    context=cache.get(fingerprint(context_key(q,common,state)))
    if context is None:raise ValueError('No cached context; no retrieval will be performed')
    answer=cache.get(fingerprint(generation_key(q,context,common,cfg,anchor['model_access'])))
    if answer is None:raise ValueError('No compatible cached answer; generation is prohibited')
    inputs=judge_inputs(q,format_context(context),answer['answer'],
        json.loads((ROOT/'eval/evidence_annotations.json').read_text())['annotations'][q['id']]['notes'])
    import tiktoken
    encoding=tiktoken.get_encoding('o200k_harmony')
    estimates={stage:token_estimate(stage,judge_request(prompt,inputs[stage]),encoding)
               for stage,prompt in [('faith',FAITH_PROMPT),('accuracy',ACCURACY_PROMPT)]}
    provider=args.provider
    judge={'provider':provider,'model':'openai/gpt-oss-120b' if provider=='groq' else 'gemini-3.8-flash',
           'temperature':0,'schema_sha256':fingerprint({s:schema(s) for s in estimates}) if provider=='groq' else None}
    metadata={**anchor['model_access'],'judge':{'metadata':{'name':judge['model'],'version':None}}}
    stamp=datetime.now(timezone.utc).strftime('%Y-%m-%dT%H%M%SZ')
    record={'question_id':q['id'],'provider':provider,'judge':judge,'generator':cfg['generator'],
        'model_version':'unavailable until returned by API; alias not pinned',
        'tokenizer':{'name':'o200k_harmony','tiktoken_version':tiktoken.__version__},
        'token_estimates':estimates,'free_tier_limits':{'tpm':8000,'tpd':200000,'rpm':30,'rpd':1000},
        'limit_source':'https://console.groq.com/docs/rate-limits','limits_checked_utc':stamp,
        'context_sha256':fingerprint(context),'generation_payload_sha256':fingerprint(answer),
        'dataset_sha256':freeze['questions_sha256'],'commit':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
        'code_sha256':{p:sha(ROOT/p) for p in ['eval/judge_providers.py','eval/run_alternative_judge.py']},
        'live_calls':0,'stages':{},'new_generation_calls':0,'new_retrieval_calls':0}
    compatible=all(throughput_ok(v) for v in estimates.values())
    record['input_throughput_compatible']=compatible
    record['execution_status']='preflight_only'
    if provider=='groq' and not compatible:
        record['execution_status']='blocked_input_exceeds_published_free_tier_tpm'
    elif args.smoke:
        key=credential(provider,ROOT)
        if not key:record['execution_status']='blocked_missing_credentials'
        else:
            # Provider-qualified scope isolates operational cooldowns as well as scores.
            scoped=provider+':'+judge['model'] if provider=='groq' else judge['model']
            op={**cfg,'judge':judge,'max_attempts':1,'rate_limit_seconds':65,
                'per_model_min_interval_seconds':{judge['model']:65},'tokens_per_minute':{}}
            caller=Caller(cache,op,max_live_calls=2,progress=progress_logger({}))
            invoke=make_judge(provider,key,cfg['timeout_seconds'])
            # evaluate_judges passes the model as scope. Prefix only the operational scope.
            original_call=caller.call
            def qualified_call(*a,**kw):
                kw['model']=scoped
                return original_call(*a,**kw)
            caller.call=qualified_call
            stages=evaluate_judges(q,context,answer,common,op,metadata,
                json.loads((ROOT/'eval/evidence_annotations.json').read_text())['annotations'][q['id']]['notes'],caller,invoke)
            record.update(stages=public_stages(stages),live_calls=caller.live_calls,
                execution_status='completed' if all('verdict' in v for v in stages.values()) else 'incomplete')
    after=success_inventory(cache)
    assert all(after.get(k)==v for k,v in before.items())
    record['original_success_entries_preserved']=len(before)
    out=ROOT/'eval/alternative_judge_results';out.mkdir(exist_ok=True)
    path=out/f'{stamp}_{provider}_preflight.json';path.write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps(record,indent=2))
    return 0 if record['execution_status'] in ['preflight_only','completed'] else 2

if __name__=='__main__':raise SystemExit(main())
