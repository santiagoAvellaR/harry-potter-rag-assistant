"""Persistent calls, strict judge schemas and generation metrics; no API imports."""
import hashlib
import json
from pathlib import Path
import random
import sqlite3
import time
from collections import Counter


class InvalidJudge(ValueError):
    """Judge returned an invalid verdict; never score as zero."""


class CallError(RuntimeError):
    def __init__(self, category, attempts):
        super().__init__(category)
        self.category, self.attempts = category, attempts


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                     separators=(',', ':')).encode()).hexdigest()


def error_category(exc):
    if isinstance(exc, InvalidJudge):
        return 'invalid_judge_output'
    code = str(getattr(exc, 'code', getattr(exc, 'status_code', '')))
    # Read provider text for classification only, never persist potentially secret URLs.
    text = str(exc).lower()
    if code in ('401', '403') or 'api key not valid' in text:
        return 'authentication_or_permission'
    if code == '404' or 'not found' in text:
        return 'model_unavailable'
    if code == '429' or 'resource_exhausted' in text or 'quota' in text:
        return 'quota_or_rate_limit'
    if isinstance(exc, TimeoutError) or code in ('500', '502', '503', '504'):
        return 'transient_api_error'
    if isinstance(exc, (ConnectionError, OSError)):
        return 'transport_error'
    return 'api_error'


class CallCache:
    """SQLite success checkpoint and attempt journal, committed after every call."""
    def __init__(self, path):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(path)
        self.db.execute('CREATE TABLE IF NOT EXISTS success (key TEXT PRIMARY KEY, payload TEXT NOT NULL)')
        self.db.execute('CREATE TABLE IF NOT EXISTS attempts (key TEXT, category TEXT, attempt INTEGER, at REAL)')
        self.db.commit()

    def get(self, key):
        row = self.db.execute('SELECT payload FROM success WHERE key=?', (key,)).fetchone()
        return json.loads(row[0]) if row else None

    def put(self, key, payload):
        with self.db:
            self.db.execute('INSERT OR REPLACE INTO success VALUES (?,?)',
                            (key, json.dumps(payload, ensure_ascii=False)))

    def event(self, key, category, attempt):
        with self.db:
            self.db.execute('INSERT INTO attempts VALUES (?,?,?,?)', (key, category, attempt, time.time()))


class Caller:
    """Rate-limit all attempts, bound exponential retries; never cache failure as success."""
    def __init__(self, cache, config, sleep=time.sleep, clock=time.monotonic):
        self.cache, self.config, self.sleep, self.clock = cache, config, sleep, clock
        self.last = None

    def call(self, binding, fn, validate=lambda value: value):
        key = fingerprint(binding)
        cached = self.cache.get(key)
        if cached is not None:
            validate(cached)
            return cached
        for attempt in range(1, self.config['max_attempts'] + 1):
            if self.last is not None:
                self.sleep(max(0, self.config['rate_limit_seconds'] - (self.clock() - self.last)))
            self.last = self.clock()
            try:
                payload = fn()
                validate(payload)
                self.cache.put(key, payload)
                self.cache.event(key, 'success', attempt)
                return payload
            except Exception as exc:
                category = error_category(exc)
                self.cache.event(key, category, attempt)
                if category in ('authentication_or_permission', 'model_unavailable') or attempt == self.config['max_attempts']:
                    raise CallError(category, attempt) from exc
                self.sleep(min(self.config['max_backoff_seconds'], self.config['backoff_seconds'] * 2**(attempt-1)))
        raise AssertionError('unreachable')


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
