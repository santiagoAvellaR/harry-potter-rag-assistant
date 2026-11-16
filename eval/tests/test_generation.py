"""Offline deterministic contract tests: no provider clients or model downloads."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from eval.generation_core import (CallCache,Caller,CallError,InvalidJudge,fingerprint,
 validate_faith,validate_accuracy,faith_score,aggregate,audit_ids)
from eval.run_generation import safe_answer, write_outputs, package_versions

CFG={'max_attempts':3,'rate_limit_seconds':0,'backoff_seconds':2,'max_backoff_seconds':3}


def faith(claims=(),abstains=False,appropriate=False):
    return {'claims':[{'claim':str(i),'verdict':v,'evidence_chunks':[1] if v=='supported' else []} for i,v in enumerate(claims)],'abstains':abstains,'appropriate_abstention':appropriate}


class GenerationTest(unittest.TestCase):
    def test_missing_optional_package_is_recorded(self):
        import importlib.metadata
        def version(name):
            if name == 'optional':
                raise importlib.metadata.PackageNotFoundError(name)
            return '1.0'
        with patch('eval.run_generation.importlib.metadata.version',side_effect=version):
            self.assertEqual(package_versions(['installed','optional']),
                             {'installed':'1.0','optional':None})

    def test_claim_ratio_uncertain_in_denominator(self):
        v=validate_faith(faith(['supported','uncertain','unsupported']),1)
        self.assertEqual(faith_score(v),1/3)
        self.assertEqual(faith_score(faith(['uncertain'])),0)

    def test_no_claims_are_null(self):
        self.assertIsNone(faith_score(validate_faith(faith(abstains=True,appropriate=True),12)))

    def test_invalid_claim_output(self):
        cases=[{},faith(['supported']),faith(['unknown']),faith(appropriate=True)]
        cases[1]['claims'][0]['evidence_chunks']=[13]
        for v in cases:
            with self.assertRaises(InvalidJudge):validate_faith(v,12)
        v=faith(['supported']);v['claims'][0]['evidence_chunks']=[]
        with self.assertRaises(InvalidJudge):validate_faith(v,12)

    def test_accuracy_schema(self):
        validate_accuracy({'abstains':True,'accuracy':None})
        validate_accuracy({'abstains':False,'accuracy':'partial'})
        for v in [{'abstains':True,'accuracy':'incorrect'},{'abstains':False,'accuracy':None}, {'abstains':0,'accuracy':'correct'}]:
            with self.assertRaises(InvalidJudge):validate_accuracy(v)

    def test_cache_survives_interruption_and_context_change(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'cache.sqlite3';c=CallCache(p);calls=[]
            call=Caller(c,CFG,sleep=lambda _:None)
            binding={'question':'Q','context_hash':'a','prompt':'P','model':'G','version':'1'}
            self.assertEqual(call.call(binding,lambda:calls.append(1) or {'answer':'A'}),{'answer':'A'})
            c.db.close()  # process interruption after successful generation, before judge
            c=CallCache(p);call=Caller(c,CFG,sleep=lambda _:None)
            call.call(binding,lambda:self.fail('successful API call repeated'))
            call.call(dict(binding,context_hash='b'),lambda:calls.append(2) or {'answer':'B'})
            self.assertEqual(calls,[1,2]);c.db.close()

    def test_error_not_cached_and_retry_bound(self):
        with tempfile.TemporaryDirectory() as d:
            c=CallCache(Path(d)/'c');wait=[];attempt=[]
            caller=Caller(c,CFG,sleep=wait.append)
            def fail():attempt.append(1);raise TimeoutError('test')
            with self.assertRaises(CallError) as caught:caller.call({'q':1},fail)
            self.assertEqual(caught.exception.attempts,3);self.assertEqual(len(attempt),3)
            self.assertIsNone(c.get(fingerprint({'q':1})))
            self.assertIn(2,wait);self.assertIn(3,wait)
            self.assertEqual(caller.call({'q':1},lambda:{'ok':True}),{'ok':True});c.db.close()

    def test_fatal_auth_not_retried(self):
        class Auth(Exception):code=403
        with tempfile.TemporaryDirectory() as d:
            c=CallCache(Path(d)/'c');caller=Caller(c,CFG,sleep=lambda _:None)
            with self.assertRaises(CallError) as caught:caller.call({},lambda:(_ for _ in ()).throw(Auth()))
            self.assertEqual(caught.exception.attempts,1);c.db.close()

    def test_malformed_judge_retried(self):
        with tempfile.TemporaryDirectory() as d:
            c=CallCache(Path(d)/'c');caller=Caller(c,CFG,sleep=lambda _:None)
            count=[]
            def response():count.append(1);return {} if len(count)<3 else faith(['supported'])
            v=caller.call({},response,lambda v:validate_faith(v,1))
            self.assertEqual(len(count),3);self.assertEqual(faith_score(v),1);c.db.close()

    def test_rate_limit_with_fake_clock(self):
        with tempfile.TemporaryDirectory() as d:
            c=CallCache(Path(d)/'c');wait=[]
            caller=Caller(c,dict(CFG,rate_limit_seconds=5),sleep=wait.append,clock=lambda:10)
            caller.call({'x':1},lambda:1);caller.call({'x':2},lambda:2)
            self.assertEqual(wait,[5]);c.db.close()

    def test_accuracy_and_abstention_aggregation(self):
        rows=[{'id':'A','category':'factual_simple','generation_status':'completed','faith':faith(['supported','uncertain']),'accuracy':{'accuracy':'partial','abstains':False}},
              {'id':'B','category':'factual_simple','generation_status':'completed','faith':faith(abstains=True),'accuracy':{'accuracy':None,'abstains':True}},
              {'id':'U01','category':'unanswerable','generation_status':'completed','faith':faith(abstains=True,appropriate=True),'accuracy':{'accuracy':None,'abstains':True}},
              {'id':'U03','category':'unanswerable','generation_status':'error','faith':None,'accuracy':None},
              {'id':'U05','category':'unanswerable','generation_status':'completed','faith':faith(['unsupported']),'accuracy':{'accuracy':'incorrect','abstains':False}}]
        g=aggregate(rows)['global']
        self.assertEqual(g['faithfulness']['n'],2)
        self.assertEqual(g['faithfulness']['metrics']['faithfulness']['mean'],.25)
        self.assertEqual(g['no_factual_claims'],2)
        self.assertEqual(g['accuracy_counts'],dict(correct=0,partial=1,incorrect=1,abstained=2))
        self.assertEqual(g['negative_planned'],3);self.assertEqual(g['negative_judged'],2)
        self.assertEqual(g['appropriate_abstentions'],1);self.assertEqual(g['abstention_percent_of_judged'],50)

    def test_missing_metrics_are_unavailable(self):
        g=aggregate([{'id':'U01','category':'unanswerable','generation_status':'not_attempted','faith':None,'accuracy':None}])['global']
        self.assertIsNone(g['abstention_percent_of_judged']);self.assertEqual(g['faithfulness']['metrics'],{})
        self.assertEqual(g['accuracy_missing'],1)

    def test_quota_is_bounded_and_sanitized(self):
        class Quota(Exception):
            code=429
        with tempfile.TemporaryDirectory() as d:
            c=CallCache(Path(d)/'c');caller=Caller(c,CFG,sleep=lambda _:None)
            def fail():
                raise Quota('secret-provider-url-and-key')
            with self.assertRaises(CallError) as caught:
                caller.call({'stage':'generation'},fail)
            self.assertEqual(caught.exception.category,'rate_limit')
            self.assertEqual(caught.exception.attempts,3)
            journal=c.db.execute('SELECT category, attempt FROM attempts').fetchall()
            self.assertEqual(journal,[('rate_limit',i) for i in (1,2,3)])
            self.assertNotIn('secret',str(journal));c.db.close()

    def test_missing_run_exports_pending_audit_without_scores(self):
        import csv
        records=[{'id':f'F{i:02}','category':'factual_simple',
                  'generation_status':'not_run_missing_credentials',
                  'faith':None,'accuracy':None,'errors':[]} for i in range(45)]
        result={'questions':records,'execution_status':'blocked','stop_reason':'missing_credentials',
                'config':{'generator':{'model':'G'},'judge':{'model':'J'}}}
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'eval').mkdir()
            output=root/'eval/result.json'
            with patch('eval.run_generation.ROOT',root):
                write_outputs(result,{},output,100)
            public=json.loads(output.read_text())
            self.assertEqual(public['summary']['global']['faith_missing'],45)
            self.assertEqual(public['summary']['global']['faithfulness']['metrics'],{})
            with (root/'eval/judge_audit.csv').open() as stream:
                rows=list(csv.DictReader(stream))
            self.assertEqual(len(rows),15)
            for row in rows:
                for field in ['answer','faithfulness','accuracy','manual_faithfulness','manual_accuracy']:
                    self.assertEqual(row[field],'')

    def test_seeded_audit_and_redaction(self):
        r=[{'id':str(i),'generation_status':'completed'} for i in range(45)]
        self.assertEqual(audit_ids(r),audit_ids(r));self.assertEqual(len(audit_ids(r)),15)
        answer='one two three four five six seven eight nine'
        self.assertTrue(safe_answer(answer,[{'page_content':answer}])[1])
        self.assertEqual(safe_answer('Je ne sais pas.',[]),('Je ne sais pas.',False))


if __name__=='__main__':unittest.main()
