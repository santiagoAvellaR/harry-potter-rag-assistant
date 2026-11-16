#!/usr/bin/env python3
"""Reproducible retrieval-only benchmark; never imports the generation chain or judge."""
import argparse
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import random
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from eval.metrics import score_question, summarize, page_pair


def file_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_inputs(config):
    side = json.loads((ROOT/'eval/evidence_annotations.json').read_text())
    freeze = json.loads((ROOT/'eval/dataset_freeze.json').read_text())
    raw = (ROOT/'eval/questions.jsonl').read_bytes()
    if hashlib.sha256(raw).hexdigest() != side['questions_sha256'] or freeze['questions_sha256'] != side['questions_sha256']:
        raise ValueError('Dataset freeze hash mismatch')
    if freeze['annotations_sha256'] != file_hash(ROOT/'eval/evidence_annotations.json'):
        raise ValueError('Annotations differ from freeze')
    rows = [json.loads(l) for l in raw.decode().splitlines()]
    validated = [q for q in rows if q['status']=='validated']
    if [q['id'] for q in validated] != freeze['approved_ids'] or freeze['approved_ids'] != side['proposed_ids']:
        raise ValueError('Validated cohort differs from owner approval')
    corpus = json.loads((ROOT/'eval/corpus_manifest.json').read_text())
    for b in corpus['books']:
        if file_hash(ROOT/'data/input'/b['source']) != b['sha256']:
            raise ValueError('Missing or wrong corpus PDF: '+b['source'])
    if config['ks'] != [1,3,5,12] or config['retrieval_depth'] != 12 or config['chroma']['mmr'] != {'k':12,'fetch_k':50,'lambda_mult':0.5}:
        raise ValueError('This baseline requires unchanged production retrieval settings')
    if config['chunking'] != {'size':2500,'overlap':500,'separators':['\n\n','\n','.',' ','']}:
        raise ValueError('Production chunk settings changed')
    if config['embedding']['model'] != 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2' or config['chroma']['distance'] != 'cosine':
        raise ValueError('Production model/distance changed')
    return validated, side, corpus, freeze


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config', type=Path, default=ROOT/'eval/config.yaml')
    parser.add_argument('--build-index', action='store_true', help='Explicitly build absent local indexes with production code')
    args = parser.parse_args()
    import yaml
    cfg = yaml.safe_load(args.config.read_text())
    # Avoid network/telemetry; do not load .env or instantiate Gemini.
    os.environ['HF_HUB_OFFLINE']='1'
    os.environ['TRANSFORMERS_OFFLINE']='1'
    os.environ['ANONYMIZED_TELEMETRY']='False'
    os.environ['TOKENIZERS_PARALLELISM']='false'
    os.environ['CUDA_VISIBLE_DEVICES']=''
    if os.environ.get('PYTHONHASHSEED') != str(cfg['seed']):
        raise ValueError('Launch with PYTHONHASHSEED='+str(cfg['seed']))
    random.seed(cfg['seed'])
    import numpy as np
    import torch
    np.random.seed(cfg['seed'])
    torch.manual_seed(cfg['seed'])
    torch.set_num_threads(cfg['runtime']['threads'])
    questions, side, corpus, freeze = validate_inputs(cfg)
    started = datetime.now(timezone.utc)
    commit = subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    relevant_paths=['app.py','src','eval/run_benchmark.py','eval/retrieval_backends.py','eval/metrics.py','eval/config.yaml']
    code_hashes={}
    for item in relevant_paths:
        path=ROOT/item
        for f in ([path] if path.is_file() else sorted(path.rglob('*.py'))):
            code_hashes[str(f.relative_to(ROOT))]=file_hash(f)
    result={'schema_version':1,'started_utc':started.isoformat(),'commit':commit,
            'git_dirty':bool(subprocess.check_output(['git','status','--porcelain'],cwd=ROOT,text=True).strip()),
            'dataset_sha256':side['questions_sha256'], 'annotations_sha256':file_hash(ROOT/'eval/evidence_annotations.json'),
            'dataset_freeze':freeze,'corpus':corpus['books'],'config':cfg,'config_sha256':file_hash(args.config),
            'source_sha256':code_hashes, 'python':sys.version,'platform':platform.platform(),
            'packages':{d.metadata['Name']:d.version for d in importlib.metadata.distributions()},
            'systems':{}, 'excluded_unanswerable':[q['id'] for q in questions if not q['gold_pages']],
            'retrieval_questions':[q['id'] for q in questions if q['gold_pages']],
            'mrr_definition':'Reciprocal rank of first historical flat relevant page, truncated at 12; misses=0',
            'bootstrap':'Macro means; 10000 iid question samples with replacement, same n; percentile 2.5/97.5, linear quantiles; seed 42 reset per system/category. No interval for unanswerable retrieval.'}
    answerable=[q for q in questions if q['gold_pages']]
    local=ROOT/'data/output/eval/retrieval_runs'/started.strftime('%Y%m%dT%H%M%S')
    local.mkdir(parents=True,exist_ok=True)
    from eval.retrieval_backends import prepare_vector, prepare_classic
    backends={}
    try:
        vector, provenance=prepare_vector(ROOT,cfg,corpus,args.build_index)
        for name, fn in vector.items():
            backends[name]=fn
            result['systems'][name]={'status':'prepared','index_verification':provenance}
    except Exception as exc:
        for name in ['mmr','cosine']:
            result['systems'][name]={'status':'unavailable','reason':f'{type(exc).__name__}: {exc}'}
        print('Vector preparation failed:',type(exc).__name__,str(exc),flush=True)
    if cfg['classic']['enabled']:
        try:
            fn,provenance=prepare_classic(ROOT,corpus,args.build_index)
            backends['bm25_inspired']=fn
            result['systems']['bm25_inspired']={'status':'prepared','index_verification':provenance}
        except Exception as exc:
            result['systems']['bm25_inspired']={'status':'unavailable','reason':f'{type(exc).__name__}: {exc}'}
            print('Classic preparation failed:',type(exc).__name__,str(exc),flush=True)
    for system, retrieve in backends.items():
        output=result['systems'][system]
        per_question=[]
        try:
            with (local/f'{system}_context.jsonl').open('w') as cache:
                for q in answerable:
                    t=time.perf_counter()
                    docs=retrieve(q['question'])
                    if len(docs)>12:
                        raise ValueError('Backend exceeded fixed top-12 depth')
                    refs=[{'source':Path(d.metadata['source']).name,'page':d.metadata['page']} for d in docs]
                    if any(page_pair(r) is None for r in refs):
                        raise ValueError('Retrieved document missing page metadata')
                    values=score_question(refs,q['gold_pages'],side['annotations'][q['id']],cfg['ks'])
                    per_question.append({'id':q['id'],'category':q['category'],'metrics':values,
                        'ranked_pages':refs,'chunk_sha256':[hashlib.sha256(d.page_content.encode()).hexdigest() for d in docs],
                        'retrieval_seconds':time.perf_counter()-t})
                    cache.write(json.dumps({'id':q['id'],'question':q['question'],'documents':[
                        {'metadata':d.metadata,'text':d.page_content} for d in docs]},ensure_ascii=False)+'\n')
                    cache.flush()
                    print(system,q['id'],'retrieved',len(docs),flush=True)
            output['status']='completed'
        except Exception as exc:
            output['status']='failed'
            output['reason']=f'{type(exc).__name__}: {exc}'
        output['per_question']=per_question
        output['completed_questions']=len(per_question)
        # Partial runs are retained for diagnosis, never silently reported as full-cohort means.
        if output['status']=='completed':
            output['global']=summarize([p['metrics'] for p in per_question],
                samples=cfg['bootstrap']['samples'],seed=cfg['seed'],confidence=cfg['bootstrap']['confidence'])
            output['categories']={c:summarize([p['metrics'] for p in per_question if p['category']==c],
                samples=cfg['bootstrap']['samples'],seed=cfg['seed'],confidence=cfg['bootstrap']['confidence'])
                for c in sorted({p['category'] for p in per_question})}
    result['finished_utc']=datetime.now(timezone.utc).isoformat()
    result['execution_status']='completed' if all(s['status']=='completed' for s in result['systems'].values()) else 'incomplete'
    result['local_context_path']=str(local.relative_to(ROOT))
    target=ROOT/'eval/results'/f"{started.strftime('%Y-%m-%dT%H%M%SZ')}_{commit[:8]}.json"
    target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print('RESULT',target,flush=True)
    return 0 if result['execution_status']=='completed' else 2


if __name__=='__main__':
    raise SystemExit(main())
