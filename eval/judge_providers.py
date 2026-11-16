"""Evaluation-only judge adapters. No SDK retries or production modifications."""
import json
import os
from pathlib import Path
from eval.generation_runtime import InvalidJSON


def credential(provider, root):
    from dotenv import dotenv_values
    name = {'groq':'GROQ_API_KEY','openrouter':'OPENROUTER_API_KEY','gemini':'GOOGLE_API_KEY'}[provider]
    local = dotenv_values(root/'.env') if (root/'.env').exists() else {}
    return os.environ.get(name) or local.get(name)


def obj(properties):
    return dict(type='object', properties=properties, required=list(properties), additionalProperties=False)


def schema(stage):
    boolean = {'type': 'boolean'}
    if stage == 'accuracy':
        return obj({'abstains': boolean, 'accuracy': {'type': ['string', 'null'], 'enum': ['correct','partial','incorrect',None]}})
    claim = obj({'claim': {'type':'string'}, 'verdict': {'type':'string','enum':['supported','unsupported','uncertain']},
                 'evidence_chunks': {'type':'array','items':{'type':'integer'}}})
    return obj({'claims':{'type':'array','items':claim}, 'abstains':boolean, 'appropriate_abstention':boolean})


def groq_payload(stage, request):
    return {'model':'openai/gpt-oss-120b','temperature':0,
            'messages':[{'role':'user','content':request}],
            'response_format':{'type':'json_schema','json_schema':{'name':stage,'strict':True,'schema':schema(stage)}}}


class GroqError(Exception):
    def __init__(self, response):
        super().__init__('Groq request failed')
        self.response = response; self.status_code = response.status_code
        # Only known quota dimension markers reach the common error classifier.
        self.details = {}
        if self.status_code == 429:
            text = response.text.lower()
            if 'tokens per day' in text or 'requests per day' in text or 'tpd' in text or 'rpd' in text or response.headers.get('x-ratelimit-remaining-requests') == '0':
                self.details = {'details':[{'quotaId':'per_day'}]}


def make_judge(provider, key, timeout=180, transport=None, endpoint=None, cache=None):
    if provider == 'openrouter':
        return openrouter_judge(key, endpoint, cache, timeout, transport)
    if provider == 'gemini':
        from langchain_google_genai import ChatGoogleGenerativeAI
        from eval.run_generation import judge_api
        return judge_api(ChatGoogleGenerativeAI(model='gemini-3.8-flash',temperature=0,
                                                google_api_key=key,timeout=timeout,max_retries=0))
    if provider != 'groq':
        raise ValueError('Unknown judge provider')
    if transport is None:
        import httpx
        transport = httpx.Client(timeout=timeout)
    def invoke(stage, request):
        response = transport.post('https://api.groq.com/openai/v1/chat/completions',
            headers={'Authorization':'Bearer '+key}, json=groq_payload(stage,request))
        if response.status_code >= 400:
            raise GroqError(response)
        body = response.json()
        try:
            verdict = json.loads(body['choices'][0]['message']['content'])
        except (ValueError,KeyError,TypeError,IndexError) as exc:
            raise InvalidJSON('Invalid Groq judge JSON') from exc
        return {'verdict':verdict,'response_metadata':{'model_name':body.get('model'),
                'system_fingerprint':body.get('system_fingerprint')},'usage_metadata':body.get('usage',{})}
    return invoke


def token_estimate(stage, request, encoding):
    # Exact BPE counts for content/schema; chat/template/server schema overhead is estimated.
    content = len(encoding.encode(request, disallowed_special=()))
    structure = len(encoding.encode(json.dumps(schema(stage)), disallowed_special=()))
    return {'content_bpe_tokens':content,'schema_bpe_tokens':structure,
            'estimated_input_tokens':content+structure+128,'overhead_allowance_tokens':128}


def throughput_ok(estimate, tpm=8000):
    return estimate['estimated_input_tokens'] <= tpm


OPENROUTER_MODEL = 'qwen/qwen3.8-27b:free'


def openrouter_payload(stage, request, endpoint):
    """Use only advertised parameters; pin one endpoint and disable fallback."""
    params = endpoint.get('supported_parameters', [])
    payload = {'model': OPENROUTER_MODEL, 'messages':[{'role':'user','content':request}],
               'provider':{'order':[endpoint['provider_name']], 'allow_fallbacks':False,
                           'require_parameters':True}}
    if 'temperature' in params:
        payload['temperature'] = 0
    if 'structured_outputs' in params:
        payload['response_format'] = groq_payload(stage,request)['response_format']
    elif 'response_format' in params:
        payload['response_format'] = {'type':'json_object'}
    return payload


def endpoint_gate(endpoints, required_input):
    if not endpoints:
        return 'blocked_no_endpoints'
    for endpoint in endpoints:
        # Context capacity is not a throughput limit. Unknown TPM never passes.
        limits = endpoint.get('rate_limits') or {}
        tpm = limits.get('tokens_per_minute')
        if isinstance(tpm,(int,float)) and tpm >= required_input:
            return 'eligible'
    return 'blocked_unknown_or_insufficient_endpoint_tpm'


class OpenRouterError(Exception):
    def __init__(self, response):
        super().__init__('OpenRouter request failed')
        self.response=response;self.status_code=response.status_code;self.details={}
        if self.status_code==429 and any(s in response.text.lower() for s in ['per day','daily','free-models-per-day']):
            self.details={'details':[{'quotaId':'per_day'}]}


class FreeDailyBudget:
    """Persist every attempt before submission; reserve 10 of 50 daily calls."""
    def __init__(self, cache, day=None):
        from datetime import datetime,timezone
        self.db=cache.db
        self.day=day or datetime.now(timezone.utc).strftime('%Y-%m-%d')
        self.db.execute('CREATE TABLE IF NOT EXISTS openrouter_daily (day TEXT PRIMARY KEY, attempts INTEGER NOT NULL)')
        self.db.commit()
    def reserve(self, account_remaining):
        with self.db:
            self.db.execute('INSERT OR IGNORE INTO openrouter_daily VALUES (?,0)',(self.day,))
            used=self.db.execute('SELECT attempts FROM openrouter_daily WHERE day=?',(self.day,)).fetchone()[0]
            if used>=40 or account_remaining<=10:
                raise ValueError('OpenRouter daily reserve would be consumed')
            self.db.execute('UPDATE openrouter_daily SET attempts=attempts+1 WHERE day=?',(self.day,))


def openrouter_judge(key, endpoint, cache, timeout=180, transport=None):
    if transport is None:
        import httpx
        transport=httpx.Client(timeout=timeout)
    headers={'Authorization':'Bearer '+key}
    budget=FreeDailyBudget(cache)
    def invoke(stage,request):
        account=transport.get('https://openrouter.ai/api/v1/key',headers=headers)
        if account.status_code>=400:raise OpenRouterError(account)
        remaining=account.json().get('data',{}).get('free_model_daily_requests',{}).get('remaining')
        if not isinstance(remaining,int):raise ValueError('Unverified OpenRouter remaining daily quota')
        budget.reserve(remaining)
        response=transport.post('https://openrouter.ai/api/v1/chat/completions',headers=headers,
                                json=openrouter_payload(stage,request,endpoint))
        if response.status_code>=400:raise OpenRouterError(response)
        body=response.json()
        if 'error' in body:raise InvalidJSON('OpenRouter returned in-band error')
        try:verdict=json.loads(body['choices'][0]['message']['content'])
        except (KeyError,ValueError,TypeError,IndexError) as exc:raise InvalidJSON('Invalid OpenRouter JSON') from exc
        return {'verdict':verdict,'response_metadata':{'model_name':body.get('model'),
            'provider':body.get('provider'),'system_fingerprint':body.get('system_fingerprint')},
            'usage_metadata':body.get('usage',{})}
    return invoke
