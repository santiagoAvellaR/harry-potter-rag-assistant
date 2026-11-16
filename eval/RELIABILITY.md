# Phase 2B execution reliability

The interrupted run is `2026-11-16T123106Z_f209eb3b.json`. It recorded 4/45
successful generations, 1/45 faith judgments and 0/45 accuracy judgments. Both
model metadata calls succeeded. The generator remains gemini-3.1-flash-lite
(temperature 0.2) and judge gemini-3.8-flash (requested temperature 0). Production
RAG code, retrieval baseline and approved questions are unchanged.

## What the original evidence establishes

The SQLite journal has 19 `transient_api_error` and 2 `quota_or_rate_limit`
attempts. Its 11 success entries comprise 4 contexts, 4 answers, 1 faith verdict
and 2 model metadata responses. Local context successes are not API calls. The
old journal stored no status code, exception subtype, headers or response details.
It is impossible to retrospectively distinguish the 19 timeouts/5xx attempts or
the two minute/day quota failures. Do not relabel them from elapsed timing alone.
There were no recorded invalid-judge-output attempts; one real faith verdict
validated. This is not evidence of a broken JSON schema.

The four cached contexts contain 22,672–26,094 characters before source headers;
successful generations reported 11,296–13,067 actual input tokens. Recorded
metadata advertised 1,048,576 input tokens for both models. Thus these requests
were below the advertised context-window limit. Long prompts still consume TPM,
and both metadata responses indicate thinking support. Some failed attempts were
near the previous 90-second timeout. Timeout pressure, thinking latency, server
overload and TPM throttling are plausible explanations, not established causes.
The actual project's active quotas are not known from metadata alone.

Google documents independent RPM, input-TPM and daily limits applied per project,
not per API key: [rate limits](https://aistudio.google.com/docs/rate-limits).
Five-second request pacing cannot guarantee compliance with those dimensions.
Google recommends bounded exponential backoff with jitter for retryable 429/5xx:
[troubleshooting](https://aistudio.google.com/docs/troubleshooting).

## Safe diagnostics and operational policy

`generation_runtime.py` walks exception causes because LangChain wraps Google
ClientError for 4xx responses. It retains only an allowlist: numeric HTTP status,
category, retryable flag, quota scope, Retry-After/RetryInfo delay, elapsed time,
DNS-failure flag and retry reason. It never logs error text, URLs, headers,
provider bodies, credentials, answers or context. No inference from a generic
429 to daily exhaustion is made. Explicit daily quota identifiers stop retries.
HTTP 500, 502, 503 and 504, local timeout, invalid JSON, schema errors and transport
errors are distinct. Non-transient 4xx and unknown errors stop immediately.

Defaults: generator spacing 15 seconds, judge spacing 30 seconds, HTTP timeout
180 seconds, three attempts, backoff 15 then 30 seconds with up to 25% positive
jitter, backoff cap 60 seconds. Retry-After can exceed that cap: wait as instructed
or defer if it exceeds the 120-second wait budget. Persisted model cooldowns
also apply to subsequent stages/restarts. Local rolling estimated-token budgets
are optional and unset until the actual project quotas are supplied; estimates
are characters/2, not actual token counts. Other project traffic remains outside
this process's control. Full resume stops after the first exhausted stage failure.
The original production prompts, context length, model sampling/thinking settings
and retrieval parameters are not adjusted.

SDK inspection confirmed max_retries=0 becomes one underlying HTTP attempt in
the installed google-genai 2.8.0 client. Hidden SDK retries are not multiplied
by the harness. Progress reports question ID, stage, attempt, cache hit/success,
sanitized failure and retry reason, alongside completed cache counts.

## Cache compatibility and preservation

Before changes, a private SQLite backup and key/payload-SHA inventory were stored
under ignored data/output/eval/generation/backups/. All 11 original successful
payloads must stay byte-identical. The success table is append-only; a conflicting
put raises CacheConflict instead of replacing data. New semantic aliases and
private binding records are additive.

The legacy migration reconstructs every original opaque key using the historical
run's code/configuration hashes, package versions and complete model metadata.
Historical Git blobs must match those recorded hashes; only the inspected legacy
runner is supported. Production chain hash, prompts and validator ASTs are
checked. Context content/order/page references match the frozen Phase 2A ranking.
Current API package versions, model settings and frozen dataset/annotation hashes
must match. No entry is matched merely by question ID or model name.

Verified aliases then use semantic inputs: requested model/temperature, provider
name/version, prompt, exact input/serialization, context content/order/metadata,
dataset/annotations, production-chain behavior, relevant API packages and judge
validator behavior. Operational configuration and whole harness source hashes
remain recorded as provenance but do not invalidate semantic successes. Future
semantic behavior/parameter changes must be included in the identity contract.
Unknown provenance, changed schema/prompt/model/gold/context or conflicting
payloads never get silently promoted. All original keys remain usable.

The real offline compatibility check recovered **4 contexts, 4 answers and 1 faith
verdict**, zero accuracy verdicts, without adding or changing any success payload.
All seven PDF hashes and frozen question/annotation bindings matched before that
check. Offline tests cover migration after a timeout/config hash change, semantic
mismatches, unknown legacy behavior, append-only protection, error classes,
quota scopes, Retry-After across restarts, jitter, pacing and hard call budgets.

## Bounded smoke test

Smoke command (one existing answer, no regeneration or retrieval):

```bash
/home/santiago/anaconda3/envs/rag/bin/python eval/run_generation.py \
  --smoke-question F01 --max-live-calls 2
```

It requires a semantically compatible cached generation and verified historical
metadata for the configured judge. It performs no model-metadata API calls,
uses at most one live faith call and one live accuracy call, and reuses any
successful verdict already present. Both stages have schema validation. An
explicit daily quota/auth/model failure stops the second stage. A transient
faith failure may still allow the single accuracy attempt, subject to cooldown.

Smoke artifacts go to eval/reliability_results/ with exact code/configuration
hashes. They contain no answer/context/claim text, only statuses, sanitized
errors, reference-only verdicts, token metadata and cache-preservation checks.
The smoke does not overwrite the interrupted run JSON, GENERATION_RESULTS.md or
judge_audit.csv. No full cohort is run automatically.

Actual smoke executions (implementation `8b2971e`):

| Execution | Faith | Accuracy | Provider requests | New answers/retrievals |
| --- | --- | --- | ---: | ---: |
| [Sandbox probe](reliability_results/2026-11-16T131913Z_8b2971e2_smoke.json) | DNS transport failure | DNS transport failure | 0 reached Gemini; 2 local invoke attempts | 0 / 0 |
| [Network-enabled smoke](reliability_results/2026-11-16T132003Z_8b2971e2_smoke.json) | HTTP 429, explicit daily quota exhausted | Not attempted after daily quota | 1 | 0 / 0 |

The network-enabled response supplied a **67,195-second** provider retry delay.
The persisted cooldown ends at approximately **2026-11-17 08:00 UTC (09:00 Paris)**.
The current failure mechanism is therefore a real daily quota block, not a JSON
parser failure. It does not identify the historical 19 transient failures or prove
that the original two quota failures had the same scope. Accuracy remains
untested against the live provider. No prompt/schema/model fallback was attempted.
The sandbox probe is not evidence of provider overload; it failed local DNS and
was rerun with network permission under the same two-attempt smoke bound.

Both artifacts recorded 4 cached answers, 1 cached faith verdict and 0 cached
accuracy verdicts afterwards. All 11 original success payloads remain byte-identical;
only aliases, private binding records, sanitized diagnostic events and a provider
cooldown were added. No full benchmark was run. Raw smoke JSON is retained as
emitted: the quota-blocked artifact has no accuracy entry because the loop stopped
at faith; this table explicitly records that it was not attempted. The follow-up
implementation also emits an explicit not_attempted entry for skipped stages and
prioritizes the non-retryable quota reason over the wait-budget reason.

**38 deterministic tests passed** after those reporting refinements. A second real
offline cache check after the code changes still recovered 4 answers and 1 verdict,
without API calls or cache loss. All seven PDF hashes and frozen dataset bindings
matched; production RAG code and Phase 2A artifacts were unchanged. Source whitespace
checks passed for this task's files. Existing interrupted-run report, CSV and JSON
remain untouched by this task and are not included in these commits.

## Recommended resumption gate

1. **Do not resume all 45 questions now.** Current daily quota has not reset.
   After the recorded cooldown (conservatively after 2026-11-17 08:01 UTC /
   09:01 Paris), first repeat the same two-call judge-only smoke. Require both
   actual faith and accuracy verdicts before considering full resumption.
   Read the smoke artifact and safe diagnostics. Confirm all original successes
   are preserved. A successful smoke demonstrates one request of each judge type,
   not that 45-question throughput or judge validity is established.
2. If daily quota is exhausted or a long Retry-After is returned, wait for its
   reset/deadline; changing an API key does not change a project quota. Check
   actual project limits in AI Studio. Set tokens_per_minute only from those
   limits, leaving room for other traffic. Do not shorten contexts or tune prompts.
3. After at least a full minute without project traffic (and all provider cooldowns
   satisfied), explicitly run the cache check, then resume if the diagnostics
   warrant it. Start only one process:

```bash
/home/santiago/anaconda3/envs/rag/bin/python eval/run_generation.py --check-cache
/home/santiago/anaconda3/envs/rag/bin/python eval/run_generation.py --run-full
```

Full preflight checks live metadata versions and stops for review if they changed
from the verified historical run. It hydrates all successful checkpoints before
new calls, reuses successes, and stops on the first stage that exhausts retries.
Missing evaluations remain missing, never score zero. Review actual responses
and human-audit columns after enough evaluations complete; no judge-human
agreement or final generation-quality claim follows from this smoke alone.
