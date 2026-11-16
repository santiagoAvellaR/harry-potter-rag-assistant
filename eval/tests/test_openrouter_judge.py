"""Offline OpenRouter routing, budget, isolation and schema contracts."""
from pathlib import Path
import tempfile
import unittest
from eval.judge_providers import (openrouter_payload,endpoint_gate,FreeDailyBudget,
    OpenRouterError,OPENROUTER_MODEL)
from eval.generation_runtime import CallCache,diagnose_error,fingerprint
from eval.generation_cache import judge_binding

class OpenRouterTests(unittest.TestCase):
    def test_fixed_route_strict_and_temperature(self):
        p=openrouter_payload('faith','Exact unchanged request',{'provider_name':'Pinned','supported_parameters':['temperature','structured_outputs']})
        self.assertEqual(p['model'],OPENROUTER_MODEL)
        self.assertFalse(p['provider']['allow_fallbacks'])
        self.assertEqual(p['temperature'],0)
        self.assertTrue(p['response_format']['json_schema']['strict'])
        self.assertEqual(p['messages'][0]['content'],'Exact unchanged request')
    def test_unsupported_parameters_not_assumed(self):
        p=openrouter_payload('accuracy','Q',{'provider_name':'Pinned'})
        self.assertNotIn('temperature',p);self.assertNotIn('response_format',p)
        p=openrouter_payload('accuracy','Q',{'provider_name':'Pinned','supported_parameters':['response_format']})
        self.assertEqual(p['response_format'],{'type':'json_object'})
    def test_empty_endpoint_and_unknown_tpm_block(self):
        self.assertEqual(endpoint_gate([],12037),'blocked_no_endpoints')
        self.assertEqual(endpoint_gate([{'context_length':262144}],12037),'blocked_unknown_or_insufficient_endpoint_tpm')
    def test_daily_reserve_and_original_cache_preserved(self):
        with tempfile.TemporaryDirectory() as d:
            c=CallCache(Path(d)/'cache');c.put('original',{'answer':'synthetic'})
            budget=FreeDailyBudget(c,day='2026-11-16')
            for i in range(40):budget.reserve(50)
            with self.assertRaises(ValueError):budget.reserve(50)
            fresh=FreeDailyBudget(c,day='2026-11-17')
            with self.assertRaises(ValueError):fresh.reserve(10)
            self.assertEqual(c.get('original'),{'answer':'synthetic'});c.db.close()
    def test_provider_cache_isolation(self):
        def key(provider):return fingerprint(judge_binding('faith','P',{'context':'C'},
            {'provider':provider,'model':OPENROUTER_MODEL,'schema_sha256':'S'}, {}, {}))
        self.assertNotEqual(key('openrouter'),key('groq'))
        self.assertNotEqual(key('openrouter'),key('gemini'))
    def test_daily_429_and_retry_after(self):
        response=type('Response',(),{'status_code':429,'headers':{'retry-after':'60'},'text':'Daily free quota reached'})()
        d=diagnose_error(OpenRouterError(response))
        self.assertEqual(d['category'],'daily_quota_exhausted')
        self.assertEqual(d['retry_after_seconds'],60)

if __name__=='__main__':unittest.main()

class FixedLiveModelTests(unittest.TestCase):
    def test_ernie_is_pinned_and_training_is_denied(self):
        p=openrouter_payload('faith','Unchanged',{'provider_name':'Baidu','model_id':'baidu/ernie-5.5-flash-preview:free','supported_parameters':['structured_outputs','temperature']})
        self.assertEqual(p['model'],'baidu/ernie-5.5-flash-preview:free')
        self.assertEqual(p['provider']['order'],['Baidu'])
        self.assertFalse(p['provider']['allow_fallbacks'])
        self.assertEqual(p['provider']['data_collection'],'deny')
    def test_automatic_routing_rejected(self):
        with self.assertRaises(ValueError):openrouter_payload('faith','Q',{'provider_name':'Any','model_id':'openrouter/free'})
