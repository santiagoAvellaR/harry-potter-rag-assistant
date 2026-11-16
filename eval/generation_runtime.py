"""Safe provider diagnostics, append-only success cache, and bounded call policy."""
from collections import defaultdict, deque
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
import hashlib
import json
import math
from pathlib import Path
import random
import re
import sqlite3
import time


class InvalidJudge(ValueError):
    """Well-formed JSON with an invalid verdict schema."""


class InvalidJSON(InvalidJudge):
    """Provider output could not be parsed as JSON."""


class CacheConflict(RuntimeError):
    """Successful cached data must never be overwritten."""


class CallError(RuntimeError):
    def __init__(self, category, attempts, diagnostic=None):
        super().__init__(category)
        self.category, self.attempts = category, attempts
        self.diagnostic = diagnostic or {'category': category}


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                     separators=(',', ':')).encode()).hexdigest()


def _duration(value, now):
    try:
        if isinstance(value, dict):
            return max(0, float(value.get('seconds', 0)) + float(value.get('nanos', 0))/1e9)
        return max(0, float(str(value).removesuffix('s')))
    except (ValueError, TypeError):
        try:
            return max(0, parsedate_to_datetime(str(value)).timestamp() - now)
        except (ValueError, TypeError, OverflowError):
            return None


def diagnose_error(exc, now=None):
    """Allowlisted facts only: never persist exception text, URLs, headers or bodies.

    LangChain wraps 4xx ClientError; inspect its explicit cause for code/details.
    Old journals did not retain these facts and cannot be retroactively expanded.
    """
    now = time.time() if now is None else now
    chain, seen = [], set()
    current = exc
    while current is not None and id(current) not in seen and len(chain) < 8:
        seen.add(id(current)); chain.append(current)
        current = current.__cause__ or current.__context__
    code, waits, details = None, [], []
    for error in chain:
        response = getattr(error, 'response', None)
        candidate = getattr(error, 'code', None) or getattr(error, 'status_code', None) or getattr(response, 'status_code', None)
        try:
            numeric = int(candidate)
            if 100 <= numeric <= 599:
                code = numeric
        except (ValueError, TypeError):
            pass
        headers = getattr(response, 'headers', {}) or {}
        delay = _duration(headers.get('retry-after', headers.get('Retry-After')), now)
        if delay is not None and math.isfinite(delay):
            waits.append(delay)
        body = getattr(error, 'details', None)
        if isinstance(body, dict):
            body = body.get('error', body)
            entries = body.get('details', []) if isinstance(body, dict) else []
            details.extend(x for x in entries if isinstance(x, dict))
    # Used for matching known signals only. None of this text is returned/logged.
    text = ' '.join(str(e).lower() for e in chain)
    quota_text = json.dumps(details).lower()
    for detail in details:
        if str(detail.get('@type', '')).endswith('RetryInfo'):
            delay = _duration(detail.get('retryDelay'), now)
            if delay is not None and math.isfinite(delay):
                waits.append(delay)
    quota_signal = quota_text + ' ' + text
    compact = re.sub(r'[^a-z]', '', quota_signal)
    scope = ('daily' if any(s in compact for s in ['perday', 'dailyquota']) else
             'tokens_per_minute' if 'perminute' in compact and 'token' in compact else
             'requests_per_minute' if 'perminute' in compact and 'request' in compact else 'unknown')
    if isinstance(exc, InvalidJSON) or isinstance(exc, json.JSONDecodeError):
        category, retryable = 'invalid_json', True
    elif isinstance(exc, InvalidJudge):
        category, retryable = 'invalid_judge_output', True
    elif code == 429 or 'resource_exhausted' in text:
        category, retryable = ('daily_quota_exhausted', False) if scope == 'daily' else ('rate_limit', True)
    elif code in (500, 502, 503, 504):
        category, retryable = f'http_{code}', True
    elif code == 408 or any(isinstance(e, TimeoutError) or 'timeout' in type(e).__name__.lower() for e in chain) or 'deadline_exceeded' in text:
        category, retryable = 'timeout', True
    elif code in (401, 403) or 'api key not valid' in text:
        category, retryable = 'authentication_or_permission', False
    elif code == 404:
        category, retryable = 'model_unavailable', False
    elif code is not None:
        category, retryable = f'http_{code}', False
    elif any(isinstance(e, (ConnectionError, OSError)) or 'connecterror' in type(e).__name__.lower() or 'transporterror' in type(e).__name__.lower() for e in chain):
        category, retryable = 'transport_error', True
    else:
        category, retryable = 'unclassified_error', False
    return {'category': category, 'http_status': code, 'retryable': retryable,
            'quota_scope': scope if category in ('rate_limit', 'daily_quota_exhausted') else None,
            'retry_after_seconds': max(waits) if waits else None,
            'dns_failure': any(s in text for s in ['name resolution', 'name or service not known', 'nodename nor servname', 'getaddrinfo'])}


def error_category(exc):
    return diagnose_error(exc)['category']


class CallCache:
    """Original tables are preserved; aliases and diagnostics are additive."""
    def __init__(self, path):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(path)
        self.db.execute('CREATE TABLE IF NOT EXISTS success (key TEXT PRIMARY KEY, payload TEXT NOT NULL)')
        self.db.execute('CREATE TABLE IF NOT EXISTS attempts (key TEXT, category TEXT, attempt INTEGER, at REAL)')
        self.db.execute('CREATE TABLE IF NOT EXISTS semantic_aliases (key TEXT PRIMARY KEY, legacy_key TEXT NOT NULL, provenance TEXT NOT NULL)')
        self.db.execute('CREATE TABLE IF NOT EXISTS identities (key TEXT PRIMARY KEY, binding TEXT NOT NULL)')
        self.db.execute('CREATE TABLE IF NOT EXISTS diagnostics (key TEXT, at REAL, event TEXT NOT NULL)')
        self.db.execute('CREATE TABLE IF NOT EXISTS cooldowns (model TEXT PRIMARY KEY, until REAL NOT NULL)')
        self.db.commit()

    def get(self, key):
        row = self.db.execute('SELECT payload FROM success WHERE key=?', (key,)).fetchone()
        if row is None:
            alias = self.db.execute('SELECT legacy_key FROM semantic_aliases WHERE key=?', (key,)).fetchone()
            if alias:
                row = self.db.execute('SELECT payload FROM success WHERE key=?', alias).fetchone()
        return json.loads(row[0]) if row else None

    def remember(self, binding):
        key = fingerprint(binding)
        with self.db:
            self.db.execute('INSERT OR IGNORE INTO identities VALUES (?,?)',
                            (key, json.dumps(binding, ensure_ascii=False, sort_keys=True)))
        return key

    def put(self, key, payload):
        existing = self.get(key)
        if existing is not None:
            if existing != payload:
                raise CacheConflict('Refusing to overwrite a successful cache entry')
            return
        with self.db:
            self.db.execute('INSERT INTO success VALUES (?,?)', (key, json.dumps(payload, ensure_ascii=False)))

    def alias(self, binding, legacy_key, provenance):
        payload = self.get(legacy_key)
        if payload is None:
            raise CacheConflict('Legacy entry missing')
        key = self.remember(binding)
        existing = self.get(key)
        if existing is not None and existing != payload:
            raise CacheConflict('Ambiguous successful semantic identity')
        with self.db:
            self.db.execute('INSERT OR IGNORE INTO semantic_aliases VALUES (?,?,?)',
                            (key, legacy_key, json.dumps(provenance, sort_keys=True)))
        return key

    def event(self, key, category, attempt, diagnostic=None):
        with self.db:
            self.db.execute('INSERT INTO attempts VALUES (?,?,?,?)', (key, category, attempt, time.time()))
            if diagnostic is not None:
                self.db.execute('INSERT INTO diagnostics VALUES (?,?,?)', (key, time.time(), json.dumps(diagnostic)))

    def cooldown(self, model, seconds):
        with self.db:
            self.db.execute('INSERT INTO cooldowns VALUES (?,?) ON CONFLICT(model) DO UPDATE SET until=MAX(until,excluded.until)',
                            (model, time.time()+seconds))


class Caller:
    """Single-process pacing, optional rolling token budget, bounded retries.

    All remote attempts, including failures, consume pacing/token reservations.
    Retry-After is a lower bound: defer instead of truncating an excessive wait.
    """
    def __init__(self, cache, config, sleep=time.sleep, clock=time.monotonic,
                 jitter=None, progress=None, max_live_calls=None):
        self.cache, self.config, self.sleep, self.clock = cache, config, sleep, clock
        self.jitter = jitter or random.SystemRandom().uniform
        self.progress = progress or (lambda event: None)
        self.last = {}; self.windows = defaultdict(deque)
        self.not_before = {model: self.clock()+max(0, until-time.time())
                           for model, until in cache.db.execute('SELECT model,until FROM cooldowns')}
        self.live_calls = 0; self.max_live_calls = max_live_calls

    def _wait(self, seconds, event):
        self.progress({**event, 'status': 'waiting', 'wait_seconds': round(seconds, 3)})
        while seconds > 0:
            part = min(30, seconds); self.sleep(part); seconds -= part

    def _pace(self, model, tokens, event):
        interval = self.config.get('per_model_min_interval_seconds', {}).get(model, self.config['rate_limit_seconds'])
        limits = self.config.get('tokens_per_minute', {})
        limit = limits.get(model)
        if limit is not None and tokens > limit:
            raise CallError('request_exceeds_token_budget', 0)
        now = self.clock(); window = self.windows[model]
        while window and now - window[0][0] >= 60:
            window.popleft()
        delay = max(0, interval - (now - self.last[model])) if model in self.last else 0
        cooldown = max(0, self.not_before.get(model, 0)-now)
        if cooldown > self.config.get('max_retry_wait_seconds', 120):
            raise CallError('rate_limit_deferred', 0, {'category': 'rate_limit_deferred',
                            'retry_after_seconds': round(cooldown, 3), 'retry_reason': 'retry_after_exceeds_wait_budget'})
        delay = max(delay, cooldown)
        if limit is not None:
            total = sum(n for _, n in window)
            for at, n in window:
                if total + tokens <= limit:
                    break
                delay = max(delay, 60 - (now-at)); total -= n
        if delay:
            self._wait(delay, {**event, 'retry_reason': 'pacing_or_token_budget'})
        self.last[model] = self.clock()
        window.append((self.clock(), tokens))

    def call(self, binding, fn, validate=lambda value: value, *, question_id=None,
             model='default', estimated_tokens=0, remote=True):
        key = self.cache.remember(binding)
        event = {'question_id': question_id, 'stage': binding.get('stage'), 'model': model}
        cached = self.cache.get(key)
        if cached is not None:
            validate(cached)
            self.progress({**event, 'status': 'cache_hit', 'attempt': 0})
            return cached
        for attempt in range(1, self.config['max_attempts'] + 1):
            attempt_event = {**event, 'attempt': attempt}
            if remote:
                if self.max_live_calls is not None and self.live_calls >= self.max_live_calls:
                    raise CallError('live_call_budget_exhausted', 0)
                try:
                    self._pace(model, estimated_tokens, attempt_event)
                except CallError as exc:
                    self.progress({**attempt_event, 'status': 'deferred', **exc.diagnostic})
                    raise
                self.live_calls += 1
            self.progress({**attempt_event, 'status': 'attempt_start'})
            started = self.clock()
            try:
                payload = fn(); validate(payload); self.cache.put(key, payload)
            except CacheConflict:
                raise
            except Exception as exc:
                diagnostic = diagnose_error(exc)
                diagnostic['elapsed_seconds'] = round(self.clock()-started, 3)
                if diagnostic['retry_after_seconds']:
                    self.not_before[model] = max(self.not_before.get(model, 0), self.clock()+diagnostic['retry_after_seconds'])
                    self.cache.cooldown(model, diagnostic['retry_after_seconds'])
                retry = diagnostic['retryable'] and attempt < self.config['max_attempts']
                if self.max_live_calls is not None and self.live_calls >= self.max_live_calls:
                    retry = False
                base = min(self.config['max_backoff_seconds'], self.config['backoff_seconds'] * 2**(attempt-1))
                factor = self.config.get('jitter_fraction', 0)
                delay = min(self.config['max_backoff_seconds'], base * (1+self.jitter(0, factor)))
                delay = max(delay, diagnostic['retry_after_seconds'] or 0)
                if delay > self.config.get('max_retry_wait_seconds', 120):
                    retry = False
                    diagnostic['retry_reason'] = 'retry_after_exceeds_wait_budget'
                else:
                    diagnostic['retry_reason'] = ('bounded_retry' if retry else
                                                  'attempt_budget_exhausted' if diagnostic['retryable'] else 'non_retryable')
                diagnostic['retry_in_seconds'] = round(delay, 3) if retry else None
                self.cache.event(key, diagnostic['category'], attempt, {**attempt_event, **diagnostic})
                self.progress({**attempt_event, 'status': 'error', **diagnostic})
                if not retry:
                    raise CallError(diagnostic['category'], attempt, diagnostic) from exc
                self._wait(delay, {**attempt_event, 'retry_reason': diagnostic['category']})
                continue
            self.cache.event(key, 'success', attempt)
            self.progress({**attempt_event, 'status': 'success', 'elapsed_seconds': round(self.clock()-started, 3)})
            return payload
        raise AssertionError('unreachable')
