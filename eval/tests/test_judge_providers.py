"""No live HTTP calls; provider cache isolation and quota contracts."""
import json
import unittest
from eval.judge_providers import make_judge, groq_payload, schema, GroqError, throughput_ok
from eval.generation_cache import judge_binding
from eval.generation_runtime import diagnose_error, fingerprint

class Response:
    status_code=200
    headers={}
    text=''
    def json(self):return {'choices':[{'message':{'content':'{"abstains":true,"accuracy":null}'}}], 'model':'openai/gpt-oss-120b','usage':{'prompt_tokens':10}}

class ProviderTests(unittest.TestCase):
    def test_strict_schema_and_unmodified_request(self):
        request='Full context\nNo truncation'
        p=groq_payload('faith',request)
        self.assertEqual(p['messages'][0]['content'],request)
        self.assertTrue(p['response_format']['json_schema']['strict'])
        self.assertFalse(schema('faith')['properties']['claims']['items']['additionalProperties'])
        self.assertEqual(p['temperature'],0)
    def test_http_adapter(self):
        class Transport:
            def post(self,url,**kw):
                self.payload=kw['json'];return Response()
        t=Transport();r=make_judge('groq','synthetic-key',transport=t)('accuracy','Question')
        self.assertIsNone(r['verdict']['accuracy'])
        self.assertEqual(r['usage_metadata']['prompt_tokens'],10)
    def test_provider_model_schema_input_isolation(self):
        base=dict(stage='accuracy',prompt='P',data={'answer':'A'},judge={'provider':'groq','model':'M','schema_sha256':'S'},common={},metadata={})
        original=fingerprint(judge_binding(**base))
        for field,value in [('provider','gemini'),('model','OTHER'),('schema_sha256','OTHER')]:
            changed={**base,'judge':{**base['judge'],field:value}}
            self.assertNotEqual(original,fingerprint(judge_binding(**changed)))
        self.assertNotEqual(original,fingerprint(judge_binding(**{**base,'data':{'answer':'OTHER'}})))
    def test_groq_daily_quota_and_retry_after(self):
        r=Response();r.status_code=429;r.text='Rate limit reached: tokens per day';r.headers={'retry-after':'60'}
        d=diagnose_error(GroqError(r))
        self.assertEqual(d['category'],'daily_quota_exhausted')
        self.assertEqual(d['retry_after_seconds'],60)
        r.text='tokens per minute';self.assertEqual(diagnose_error(GroqError(r))['category'],'rate_limit')
    def test_throughput_guard(self):
        self.assertFalse(throughput_ok({'estimated_input_tokens':8001}))
        self.assertTrue(throughput_ok({'estimated_input_tokens':7999}))

if __name__=='__main__':unittest.main()
