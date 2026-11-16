"""Evaluation-only judge adapters. No SDK retries or production modifications."""
import json
import os
from pathlib import Path
from eval.generation_runtime import InvalidJSON


def credential(provider, root):
    from dotenv import dotenv_values
    name = 'GROQ_API_KEY' if provider == 'groq' else 'GOOGLE_API_KEY'
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


def make_judge(provider, key, timeout=180, transport=None):
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
