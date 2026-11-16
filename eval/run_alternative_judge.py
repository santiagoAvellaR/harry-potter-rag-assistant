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
    parser.add_argument('--provider',choices=['groq','gemini','openrouter'],default='groq')
    parser.add_argument('--openrouter-model',choices=['baidu/ernie-5.5-flash-preview:free','nvidia/nemotron-3.5-super-vl:free'],default='baidu/ernie-5.5-flash-preview:free')
    parser.add_argument('--question',default='F01')
    parser.add_argument('--endpoint-snapshot',type=Path,help='Previously inspected public OpenRouter endpoint metadata')
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
    qwen_manifest=None
    if provider=='openrouter' and args.openrouter_model=='qwen/qwen3.8-27b:free':
        from tokenizers import Tokenizer
        directory=ROOT/'data/output/eval/tokenizers/qwen3.8-27b'
        qwen_manifest=json.loads((directory/'manifest.json').read_text())
        for name,digest in qwen_manifest['files'].items():
            if sha(directory/name)!=digest:raise ValueError('Tokenizer fingerprint mismatch')
        tokenizer=Tokenizer.from_file(str(directory/'tokenizer.json'))
        estimates={}
        for stage,prompt in [('faith',FAITH_PROMPT),('accuracy',ACCURACY_PROMPT)]:
            request=judge_request(prompt,inputs[stage])
            content=len(tokenizer.encode(request,add_special_tokens=False).ids)
            schema_count=len(tokenizer.encode(json.dumps(schema(stage)),add_special_tokens=False).ids)
            estimates[stage]={'content_qwen_tokens':content,'schema_qwen_tokens':schema_count,
                'estimated_input_tokens':content+schema_count+128,'overhead_allowance_tokens':128,
                'request_characters':len(request),'request_sha256':fingerprint(request)}
    judge={'provider':provider,'model':{'groq':'openai/gpt-oss-120b','gemini':'gemini-3.8-flash','openrouter':args.openrouter_model}[provider],
           'temperature':0,'schema_sha256':fingerprint({s:schema(s) for s in estimates}) if provider in ('groq','openrouter') else None}
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
    endpoint=None
    gate=None
    if provider=='openrouter':
        from eval.judge_providers import endpoint_gate, OPENROUTER_MODEL
        selected_model=args.openrouter_model
        snapshot=json.loads(args.endpoint_snapshot.read_text()) if args.endpoint_snapshot else {'data':{'id':selected_model,'endpoints':[]}}
        if snapshot['data']['id']!=selected_model:raise ValueError('Fixed model metadata required')
        if args.smoke:
            import httpx
            response=httpx.get('https://openrouter.ai/api/v1/models/'+selected_model+'/endpoints',timeout=30)
            response.raise_for_status()
            # Refresh before a live smoke; never trust a stale endpoint snapshot for routing.
            body=response.json()['data']
            snapshot={'source':'live OpenRouter endpoint metadata','data':{'id':body['id'],'endpoints':[
                {k:e[k] for k in ('provider_name','model_id','supported_parameters','context_length','max_prompt_tokens','rate_limits') if k in e}
                for e in body.get('endpoints',[])]}}
        endpoints=snapshot['data'].get('endpoints',[])
        gate=endpoint_gate(endpoints,max(e['estimated_input_tokens'] for e in estimates.values()))
        record['endpoint_metadata']=snapshot
        record['tokenizer']={**(qwen_manifest or record['tokenizer']),'limitation':'Cross-model proxy only for ERNIE/Nemotron; actual deployed tokenization and usage unknown'}
        record['free_tier_limits']={'rpd':50,'rpm':20,'retry_reserve':10,'endpoint_tpm':None}
        record['limit_source']='https://openrouter.ai/docs/api/reference/limits'
        if gate=='eligible':
            endpoint=next(e for e in endpoints if (e.get('rate_limits') or {}).get('tokens_per_minute',0)>=max(v['estimated_input_tokens'] for v in estimates.values()))
            judge['endpoint']={k:endpoint[k] for k in ('provider_name','model_id','supported_parameters') if k in endpoint}
            judge['response_format_policy']='advertised_parameters_only'
        else:
            record['execution_status']=gate
    compatible=None if provider=='openrouter' else all(throughput_ok(v) for v in estimates.values())
    record['input_throughput_compatible']=compatible
    if provider=='openrouter':
        record['credential_present']=bool(credential(provider,ROOT))
        record['account_quotas_verified']=False
        record['response_token_usage']=None
        record['inference_latency_seconds']=None
        record['data_practices_cleared']=bool(snapshot.get('policy_review',{}).get('cleared') and snapshot.get('policy_review',{}).get('source'))
        if gate=='eligible' and not record['data_practices_cleared']:
            gate='blocked_provider_policy_not_cleared'
        record['inference_blockers']=['Unverified provider TPM','Missing API credentials/account quota verification']
        if selected_model.startswith('baidu'):
            record['inference_blockers'].append('Baidu terms sections 3A.3.1-3A.3.2 permit content storage and ML improvement; no specific exception verified')
    record['execution_status']=gate if gate and gate!='eligible' else 'preflight_only'
    if provider=='groq' and not compatible:
        record['execution_status']='blocked_input_exceeds_published_free_tier_tpm'
    elif provider=='openrouter' and gate!='eligible':
        pass
    elif args.smoke:
        key=credential(provider,ROOT)
        if not key:record['execution_status']='blocked_missing_credentials'
        else:
            # Provider-qualified scope isolates operational cooldowns as well as scores.
            scoped=provider+':'+judge['model'] if provider in ('groq','openrouter') else judge['model']
            op={**cfg,'judge':judge,'max_attempts':1,'rate_limit_seconds':65,
                'per_model_min_interval_seconds':{judge['model']:65},'tokens_per_minute':{}}
            caller=Caller(cache,op,max_live_calls=2,progress=progress_logger({}))
            invoke=make_judge(provider,key,cfg['timeout_seconds'],endpoint=endpoint,cache=cache)
            # evaluate_judges passes the model as scope. Prefix only the operational scope.
            original_call=caller.call
            def qualified_call(*a,**kw):
                kw['model']=scoped
                return original_call(*a,**kw)
            caller.call=qualified_call
            stages=evaluate_judges(q,context,answer,common,op,metadata,
                json.loads((ROOT/'eval/evidence_annotations.json').read_text())['annotations'][q['id']]['notes'],caller,invoke,stop_on_error=(provider=='openrouter'))
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
