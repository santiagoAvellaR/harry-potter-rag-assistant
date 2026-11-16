"""Strict judge schemas and generation metrics; provider diagnostics are separate."""
import random
from collections import Counter
from eval.generation_runtime import (CallCache, Caller, CallError, InvalidJudge,
                                     fingerprint, error_category)


def validate_faith(value, count):
    if not isinstance(value, dict) or set(value) != {'claims', 'abstains', 'appropriate_abstention'}:
        raise InvalidJudge('Faithfulness schema')
    if type(value['abstains']) is not bool or type(value['appropriate_abstention']) is not bool:
        raise InvalidJudge('Abstention booleans')
    if value['appropriate_abstention'] and not value['abstains']:
        raise InvalidJudge('Inconsistent abstention')
    if not isinstance(value['claims'], list):
        raise InvalidJudge('Claims must be a list')
    seen = set()
    for claim in value['claims']:
        if not isinstance(claim, dict) or set(claim) != {'claim', 'verdict', 'evidence_chunks'}:
            raise InvalidJudge('Claim schema')
        if not isinstance(claim['claim'], str) or not claim['claim'].strip() or claim['claim'] in seen:
            raise InvalidJudge('Empty/duplicate claim')
        seen.add(claim['claim'])
        if claim['verdict'] not in ('supported', 'unsupported', 'uncertain'):
            raise InvalidJudge('Unknown verdict')
        refs = claim['evidence_chunks']
        if not isinstance(refs, list) or len(refs) != len(set(map(str, refs))) or any(type(i) is not int or i < 1 or i > count for i in refs):
            raise InvalidJudge('Invalid evidence reference')
        if claim['verdict'] == 'supported' and not refs:
            raise InvalidJudge('Supported claim needs evidence')
    return value


def validate_accuracy(value):
    if not isinstance(value, dict) or set(value) != {'abstains', 'accuracy'} or type(value['abstains']) is not bool:
        raise InvalidJudge('Accuracy schema')
    if value['accuracy'] not in ('correct', 'partial', 'incorrect', None):
        raise InvalidJudge('Accuracy enum')
    if (value['accuracy'] is None) != value['abstains']:
        raise InvalidJudge('Abstentions require null accuracy, not incorrect')
    return value


def faith_score(verdict):
    claims = verdict['claims']
    return sum(c['verdict'] == 'supported' for c in claims) / len(claims) if claims else None


def aggregate(records, samples=10000, seed=42):
    from eval.metrics import summarize
    # Missing/error results never become zeros. Always report denominators and counts.
    def group(rows):
        faith = [r['faith'] for r in rows if r.get('faith') is not None]
        accuracy = [r['accuracy'] for r in rows if r.get('accuracy') is not None]
        scored = [faith_score(v) for v in faith if v['claims']]
        a = Counter(v['accuracy'] if not v['abstains'] else 'abstained' for v in accuracy)
        negatives = [r for r in rows if r['category'] == 'unanswerable']
        judged_neg = [r for r in negatives if r.get('faith') is not None]
        n_abstain = sum(r['faith']['abstains'] and r['faith']['appropriate_abstention'] for r in judged_neg)
        return {'planned': len(rows), 'generated': sum(r.get('generation_status') == 'completed' for r in rows),
                'generation_completion_percent':100*sum(r.get('generation_status') == 'completed' for r in rows)/len(rows) if rows else None,
                'faith_judged': len(faith), 'faith_missing': len(rows)-len(faith),
                'no_factual_claims': sum(not v['claims'] for v in faith),
                'faithfulness': summarize([{'faithfulness': s} for s in scored], samples=samples, seed=seed),
                'claim_verdict_counts': dict(Counter(c['verdict'] for v in faith for c in v['claims'])),
                'accuracy_judged': len(accuracy), 'accuracy_missing': len(rows)-len(accuracy),
                'accuracy_counts': {k:a[k] for k in ['correct','partial','incorrect','abstained']},
                'accuracy_percent_of_judged': {k:100*a[k]/len(accuracy) if accuracy else None for k in ['correct','partial','incorrect','abstained']},
                'judge_abstention_disagreements':sum(r['faith']['abstains'] != r['accuracy']['abstains'] for r in rows if r.get('faith') is not None and r.get('accuracy') is not None),
                'negative_missing':len(negatives)-len(judged_neg),
                'negative_planned':len(negatives),'negative_judged':len(judged_neg),
                'appropriate_abstentions':n_abstain,
                'abstention_percent_of_judged':100*n_abstain/len(judged_neg) if judged_neg else None}
    return {'global': group(records), 'categories': {c:group([r for r in records if r['category']==c]) for c in sorted({r['category'] for r in records})}}


def audit_ids(records, seed=42):
    available = [r['id'] for r in records if r.get('generation_status') == 'completed']
    # If none completed, create explicitly pending slots; not 15 fictional responses.
    population = sorted(available or [r['id'] for r in records])
    return random.Random(seed).sample(population, min(15, len(population)))
