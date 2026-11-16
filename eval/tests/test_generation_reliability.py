"""Transport and semantic-migration regression tests; no live provider calls."""
import hashlib
import inspect
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from eval.generation_runtime import (CallCache, Caller, CallError, CacheConflict,
                                      InvalidJSON, InvalidJudge, diagnose_error, fingerprint)
from eval.generation_cache import (common_identity, context_binding, generation_binding,
    judge_binding, judge_inputs, migrate_legacy, API_PACKAGES)
from eval.generation_core import validate_faith, validate_accuracy
from eval.run_generation import evaluate_judges

CFG = dict(max_attempts=3, rate_limit_seconds=0, backoff_seconds=2,
           max_backoff_seconds=3, max_retry_wait_seconds=20, jitter_fraction=.25)


class ProviderError(Exception):
    def __init__(self, code, details=None, headers=None):
        super().__init__('private url?key=DO_NOT_LOG and private novel context')
        self.code = code; self.details = details or {}
        self.response = type('Response', (), {'headers': headers or {}, 'status_code': code})()


def supported():
    return {'claims': [{'claim': 'Synthetic claim', 'verdict': 'supported', 'evidence_chunks': [1]}],
            'abstains': False, 'appropriate_abstention': False}


class Clock:
    def __init__(self):
        self.now = 0; self.waits = []
    def clock(self):
        return self.now
    def sleep(self, seconds):
        self.waits.append(seconds); self.now += seconds


class DiagnosticsTest(unittest.TestCase):
    def test_exact_http_statuses_and_wrapped_429(self):
        for status in (500, 502, 503, 504):
            result = diagnose_error(ProviderError(status))
            self.assertEqual(result['category'], f'http_{status}')
            self.assertEqual(result['http_status'], status)
        wrapped = RuntimeError('LangChain wrapper')
        wrapped.__cause__ = ProviderError(429)
        self.assertEqual(diagnose_error(wrapped)['category'], 'rate_limit')
        self.assertEqual(diagnose_error(wrapped)['http_status'], 429)

    def test_timeout_invalid_json_and_schema_are_distinct(self):
        for exc, expected in [(TimeoutError(), 'timeout'), (InvalidJSON(), 'invalid_json'),
                              (InvalidJudge(), 'invalid_judge_output')]:
            self.assertEqual(diagnose_error(exc)['category'], expected)
        self.assertFalse(diagnose_error(ProviderError(400))['retryable'])

    def test_daily_and_tpm_quota_details(self):
        for quota_id, category, scope in [('GenerateRequestsPerDayPerProjectPerModel', 'daily_quota_exhausted', 'daily'),
                                         ('GenerateContentInputTokensPerMinute', 'rate_limit', 'tokens_per_minute')]:
            result = diagnose_error(ProviderError(429, {'error': {'details': [
                {'@type': 'type.googleapis.com/google.rpc.QuotaFailure',
                 'violations': [{'quotaId': quota_id}]},
                {'@type': 'type.googleapis.com/google.rpc.RetryInfo', 'retryDelay': '12s'}]}}))
            self.assertEqual(result['category'], category); self.assertEqual(result['quota_scope'], scope)
            self.assertEqual(result['retry_after_seconds'], 12)
            self.assertEqual(result['retryable'], scope != 'daily')
            self.assertNotIn('DO_NOT_LOG', json.dumps(result))
            self.assertNotIn('novel', json.dumps(result))

    def test_retry_after_http_date_and_seconds(self):
        for header in ['15', 'Thu, 01 Jan 1970 00:00:15 GMT']:
            d = diagnose_error(ProviderError(503, headers={'Retry-After': header}), now=0)
            self.assertEqual(d['retry_after_seconds'], 15)


class PolicyTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.cache = CallCache(Path(self.tmp.name)/'cache')
        self.clock = Clock(); self.events = []
    def tearDown(self):
        self.cache.db.close(); self.tmp.cleanup()
    def caller(self, **kwargs):
        return Caller(self.cache, CFG, sleep=self.clock.sleep, clock=self.clock.clock,
                      jitter=lambda a, b: b, progress=self.events.append, **kwargs)

    def test_retry_after_is_not_clipped_to_backoff_cap(self):
        calls = []
        def invoke():
            calls.append(1)
            if len(calls) == 1:
                raise ProviderError(429, headers={'Retry-After': '11'})
            return {'ok': True}
        self.caller().call({'stage': 'faith'}, invoke, question_id='F01')
        self.assertEqual(self.clock.waits, [11]); self.assertEqual(len(calls), 2)
        self.assertNotIn('DO_NOT_LOG', json.dumps(self.events))
        self.assertEqual(self.events[-1]['status'], 'success')
        self.assertEqual(self.events[-1]['attempt'], 2)

    def test_excessive_retry_after_defers_instead_of_early_retry(self):
        with self.assertRaises(CallError) as exc:
            self.caller().call({'stage': 'accuracy'}, lambda: (_ for _ in ()).throw(
                ProviderError(429, headers={'Retry-After': '21'})))
        self.assertEqual(exc.exception.attempts, 1)
        self.assertEqual(exc.exception.diagnostic['retry_reason'], 'retry_after_exceeds_wait_budget')
        self.assertEqual(self.clock.waits, [])

    def test_retry_after_applies_to_next_stage_and_survives_restart(self):
        caller = self.caller(max_live_calls=2)
        with self.assertRaises(CallError):
            caller.call({'stage': 'faith'}, lambda: (_ for _ in ()).throw(
                ProviderError(429, headers={'Retry-After': '21'})), model='J')
        with self.assertRaises(CallError) as caught:
            caller.call({'stage': 'accuracy'}, lambda: self.fail('Retry-After violated'), model='J')
        self.assertEqual(caught.exception.category, 'rate_limit_deferred')
        restarted = self.caller(max_live_calls=1)
        self.assertGreater(restarted.not_before['J'], 20)
        with self.assertRaises(CallError):
            restarted.call({'stage': 'accuracy'}, lambda: self.fail('Cooldown lost'), model='J')
        self.assertEqual(restarted.live_calls, 0)

    def test_daily_quota_never_retried(self):
        error = ProviderError(429, {'details': [{'violations': [{'quotaId': 'requests_per_day'}]}]})
        with self.assertRaises(CallError) as caught:
            self.caller().call({}, lambda: (_ for _ in ()).throw(error))
        self.assertEqual(caught.exception.attempts, 1)
        self.assertEqual(self.clock.waits, [])

    def test_bounded_jitter_and_hard_live_budget(self):
        caller = self.caller(max_live_calls=2)
        with self.assertRaises(CallError):
            caller.call({}, lambda: (_ for _ in ()).throw(ProviderError(503)))
        self.assertEqual(caller.live_calls, 2)
        self.assertEqual(self.clock.waits, [2.5])
        with self.assertRaises(CallError) as caught:
            caller.call({'new': True}, lambda: self.fail('Budget exceeded'))
        self.assertEqual(caught.exception.category, 'live_call_budget_exhausted')

    def test_model_specific_pacing_and_rolling_token_reservations(self):
        cfg = {**CFG, 'per_model_min_interval_seconds': {'G': 5}, 'tokens_per_minute': {'G': 10}}
        caller = Caller(self.cache, cfg, sleep=self.clock.sleep, clock=self.clock.clock)
        caller.call({'q': 1}, lambda: 1, model='G', estimated_tokens=6)
        caller.call({'q': 2}, lambda: 2, model='G', estimated_tokens=6)
        self.assertEqual(sum(self.clock.waits), 60)
        caller.call({'q': 3}, lambda: 3, model='H', estimated_tokens=6)
        self.assertEqual(sum(self.clock.waits), 60)
        with self.assertRaises(CallError) as caught:
            caller.call({'q': 4}, lambda: self.fail('Over token budget'), model='G', estimated_tokens=11)
        self.assertEqual(caught.exception.category, 'request_exceeds_token_budget')

    def test_no_overwrite_of_success_or_alias(self):
        self.cache.put('old', {'answer': 'Original'})
        self.cache.alias({'semantic': True}, 'old', {'verified': True})
        with self.assertRaises(CacheConflict):
            self.cache.put('old', {'answer': 'Replacement'})
        with self.assertRaises(CacheConflict):
            self.cache.put(fingerprint({'semantic': True}), {'answer': 'Replacement'})
        self.assertEqual(self.cache.get('old'), {'answer': 'Original'})


class MigrationTest(unittest.TestCase):
    """Construct a complete opaque-key legacy cache and Git provenance fixture."""
    def test_verified_legacy_recovery_and_semantic_misses(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); (root/'eval/generation_results').mkdir(parents=True); (root/'src/RAG').mkdir(parents=True)
            chain = "DEFAULT_PROMPT_TEMPLATE = 'P'\n"
            runner = "FAITH_PROMPT = 'F'\nACCURACY_PROMPT = 'A'\n"
            core = inspect.getsource(validate_faith)+'\n'+inspect.getsource(validate_accuracy)
            blobs = {'src/RAG/chain.py': chain, 'eval/run_generation.py': runner,
                     'eval/generation_core.py': core, 'eval/generation_config.yaml': 'old operational config'}
            digests = {n: hashlib.sha256(v.encode()).hexdigest() for n, v in blobs.items()}
            (root/'src/RAG/chain.py').write_text(chain)
            (root/'eval/corpus_manifest.json').write_text('{}')
            (root/'eval/config.yaml').write_text('k: 12\n')
            (root/'eval/evidence_annotations.json').write_text(json.dumps({'annotations': {'F01': {'notes': []}}}))
            q = dict(id='F01', question='Question?', gold_answer='Gold', notes='Scope', category='factual_simple')
            context = {'documents': [{'page_content': 'Synthetic context', 'metadata': {'source': 'test.pdf', 'page': 0}}]}
            baseline = {'systems': {'mmr': {'per_question': [{'id': 'F01',
                'chunk_sha256': [hashlib.sha256(b'Synthetic context').hexdigest()],
                'ranked_pages': [{'source': 'test.pdf', 'page': 0}]}]}}}
            (root/'eval/baseline.json').write_text(json.dumps(baseline))
            bsha = hashlib.sha256((root/'eval/baseline.json').read_bytes()).hexdigest()
            packages = {name: '1' for name in API_PACKAGES}
            cfg = {'generator': {'model': 'G'}, 'judge': {'model': 'J'}, 'retrieval_result': 'eval/baseline.json', 'timeout_seconds': 999}
            metadata = {r: {'status': 'metadata_accessible', 'metadata': {'name': 'models/'+m, 'version': '1'}} for r, m in [('generator', 'G'), ('judge', 'J')]}
            freeze = dict(questions_sha256='DATASET', annotations_sha256='ANNOTATIONS')
            old = dict(commit='known', config={**cfg, 'timeout_seconds': 1}, code_sha256=digests,
                       dataset_sha256='DATASET', annotations_sha256='ANNOTATIONS',
                       phase2a_result_sha256=bsha, packages=packages, model_access=metadata)
            (root/'eval/generation_results/legacy.json').write_text(json.dumps(old))
            versions = dict(code=digests, packages=packages, generator_metadata=metadata['generator'], dataset='DATASET', annotations='ANNOTATIONS')
            cache = CallCache(root/'cache')
            cb = dict(stage='context', question=q['question'], retrieval_baseline=bsha, versions=versions)
            cache.put(fingerprint(cb), context)
            gb = dict(stage='generation', question=q['question'], generator=cfg['generator'], prompt='P', context_hash=fingerprint(context), versions=versions)
            answer = {'answer': 'Answer', 'response_metadata': {}}
            cache.put(fingerprint(gb), answer)
            inputs = judge_inputs(q, 'FORMATTED', 'Answer', [])
            for stage, prompt, verdict in [('faith', 'F', supported()), ('accuracy', 'A', {'abstains': False, 'accuracy': 'correct'})]:
                jb = dict(stage=stage, prompt=prompt, data=inputs[stage], judge=cfg['judge'], judge_metadata=metadata['judge'], versions=versions)
                cache.put(fingerprint(jb), {'verdict': verdict, 'response_metadata': {}})
            before = dict(cache.db.execute('SELECT key,payload FROM success'))
            with patch('eval.generation_cache.LEGACY_RUNNER_SHA', digests['eval/run_generation.py']), patch(
                    'eval.generation_cache.subprocess.check_output', side_effect=lambda command, **kw: blobs[command[-1].split(':', 1)[1]].encode()):
                report, anchor = migrate_legacy(root, cache, cfg, freeze, [q], packages, lambda ctx: 'FORMATTED', 'P', 'F', 'A')
                self.assertEqual(report['matched'], dict(context=1, generation=1, faith=1, accuracy=1))
                common = common_identity(root, freeze, packages)
                binding = generation_binding(q['question'], context, 'FORMATTED', 'P', cfg['generator'], common, metadata['generator'])
                self.assertEqual(cache.get(fingerprint(binding)), answer)
                # Timeout changed from 1 to 999: identical semantic key still hits.
                self.assertNotIn('timeout_seconds', json.dumps(binding))
                for changed in [dict(binding, prompt='Other'), dict(binding, question='Other'),
                                dict(binding, context_hash='Other'), dict(binding, generator={'model': 'Other'}),
                                dict(binding, provider_model={'name': 'models/G', 'version': '2'}),
                                dict(binding, common={**common, 'dataset': 'OTHER'})]:
                    self.assertIsNone(cache.get(fingerprint(changed)))
                jb = judge_binding('accuracy', 'A', inputs['accuracy'], cfg['judge'], common, metadata['judge'])
                self.assertIsNotNone(cache.get(fingerprint(jb)))
                for field in ['answer', 'gold_answer', 'annotation_notes']:
                    changed = {**inputs['accuracy'], field: 'Different'}
                    other = judge_binding('accuracy', 'A', changed, cfg['judge'], common, metadata['judge'])
                    self.assertIsNone(cache.get(fingerprint(other)))
            self.assertEqual(before, dict(cache.db.execute('SELECT key,payload FROM success')))
            # Unrecognized behavior never gets promoted, even with a known question/model.
            with patch('eval.generation_cache.subprocess.check_output', side_effect=lambda command, **kw: blobs[command[-1].split(':', 1)[1]].encode()):
                report, _ = migrate_legacy(root, cache, cfg, freeze, [q], packages, lambda ctx: 'FORMATTED', 'P', 'F', 'A')
                self.assertEqual(report['matched']['generation'], 0)
                self.assertEqual(report['skipped'][0]['reason'], 'unrecognized_legacy_runner')
            cache.db.close()


class SmokeTest(unittest.TestCase):
    def test_one_cached_answer_two_judge_attempts_and_resume(self):
        q = dict(id='F01', question='Question?', gold_answer='Gold', notes='', category='factual_simple')
        ctx = {'documents': [{'page_content': 'Synthetic context', 'metadata': {}}]}
        answer = {'answer': 'Existing French answer'}
        cfg = {**CFG, 'max_attempts': 1, 'judge': {'model': 'J', 'temperature': 0}}
        metadata = {'judge': {'metadata': {'name': 'models/J', 'version': '1'}}}
        with tempfile.TemporaryDirectory() as d, patch('eval.run_generation.format_context', return_value='FORMATTED'):
            cache = CallCache(Path(d)/'cache'); cache.put('existing_generation', answer); calls = []
            def invoke(stage, request):
                calls.append(stage)
                self.assertIn(answer['answer'], request)
                if stage == 'faith':
                    raise ProviderError(503)
                return {'verdict': {'abstains': False, 'accuracy': 'correct'}, 'response_metadata': {}}
            caller = Caller(cache, cfg, max_live_calls=2, sleep=lambda _: None)
            results = evaluate_judges(q, ctx, answer, {}, cfg, metadata, [], caller, invoke)
            self.assertEqual(calls, ['faith', 'accuracy']); self.assertEqual(caller.live_calls, 2)
            self.assertEqual(results['faith']['status'], 'error')
            self.assertNotIn('verdict', results['faith'])
            caller = Caller(cache, cfg, max_live_calls=1, sleep=lambda _: None)
            results = evaluate_judges(q, ctx, answer, {}, cfg, metadata, [], caller,
                lambda stage, request: {'verdict': supported(), 'response_metadata': {}})
            self.assertEqual(caller.live_calls, 1); self.assertEqual(results['accuracy']['status'], 'cache_hit')
            self.assertEqual(cache.get('existing_generation'), answer)
            cache.db.close()


if __name__ == '__main__':
    unittest.main()
