# Phase 2B generation and judging

The retrieval baseline at 3191452, RESULTS.md, config.yaml and its numerical
artifacts are immutable for this phase. The approved 45 question/gold records and
evidence references are unchanged. The owner approved selection and wording;
independent human verification of every evidence page is still not claimed.

Run with the existing environment and a local GOOGLE_API_KEY (GEMINI_API_KEY is
also accepted), either in the environment or .env. Never pass keys in command
arguments or commit them:

```bash
/home/santiago/anaconda3/envs/rag/bin/python -m unittest discover -s eval/tests -v
/home/santiago/anaconda3/envs/rag/bin/python eval/run_generation.py --check-cache
/home/santiago/anaconda3/envs/rag/bin/python eval/run_generation.py --smoke-question F01 --max-live-calls 2
# Run the full cohort only after reviewing the smoke diagnostics:
/home/santiago/anaconda3/envs/rag/bin/python eval/run_generation.py --run-full
```

`generation_config.yaml` is separate from the frozen retrieval configuration.
No full run starts without explicit `--run-full`. Smoke mode requires a compatible
cached answer and never retrieves or generates an answer. Missing credentials
leave evaluations missing. Full preflight checks the original model ID, while
smoke mode reuses verified historical metadata and records that it did not
perform fresh metadata calls. Unavailable original generator or judge access
halts; no model is substituted. Distinct judge ID `gemini-3.8-flash` is configured.
Both requested temperature and model metadata are recorded, including versions
only when actually supplied by the API; metadata access does not establish quota.
A provider-version change during full preflight stops for review. Both models are from Google,
so distinct model IDs do not remove provider-family bias.

## Original production semantics

Generator is gemini-3.1-flash-lite, temperature 0.2. Production DEFAULT_PROMPT_TEMPLATE
is used verbatim. It asks for French answers, use of supplied context and honest
ignorance when the answer is absent. Context is formatted by the original
HarryPotterRAGChain._format_docs: numbered source, PDF basename and zero-based
page followed by exact chunk content, joined by two newlines. No truncation,
paraphrasing or reordering is introduced by the harness.

The original prompt -> ChatGoogleGenerativeAI -> StrOutputParser components are
invoked separately to retain API response/version metadata that the production
string parser discards. This is the same generation transformation as chain.chain;
production query() would repeat retrieval and would not expose response metadata.
Only transport timeout/retry handling is controlled by the harness. Production
app.py, chain.py, prompts, embedding settings and MMR are untouched.

For the 42 answerable questions the original Phase 2A MMR context caches are
replayed, checking each chunk hash and ordered source/page pair against the
frozen result. Full original metadata and chunk content are retained privately.
The three negatives have no Phase 2A context; their first MMR invocation uses the
existing index and original chain retriever (12 chunks, fetch 50). Its exact
ordered documents are checkpointed before generation. Missing cached baseline
contexts or a changed corpus/RAG source causes a setup error rather than a silent
new retrieval baseline. The existing index should be retained from Phase 2A;
no index is rebuilt here. Phase 2A already checked every stored vector; this
runner checks corpus/source hashes but does not independently reverify every
index vector again. Index drift after that verification remains a limitation.

## Persistence and retries

The SQLite cache under ignored data/output/eval/generation/ stores exact context,
full response and provider metadata, raw judge verdicts and a per-attempt journal.
Semantic cache keys bind question, model/temperature, full production/judge prompt,
context digest (content/order/metadata and exact formatted context), API model
name/version, API package versions, production chain behavior and frozen dataset/
annotation hashes. Accuracy binds gold answer and optional-detail rubric. Judge
keys also bind exact JSON request serialization, output MIME type and validator
AST. Timeout, pacing, retry settings and whole harness/configuration file hashes
are provenance, not semantic cache inputs. Operational-only edits reuse successful
results. Prompt, model, context, dataset, schema or relevant behavior changes do not.

Legacy opaque keys are reconstructed from verified historical run/Git bindings;
additive aliases recover the original payloads without replacing them. Unknown
historical runner behavior or mismatched provenance is rejected. New identities
are recorded privately. See [RELIABILITY.md](RELIABILITY.md) for compatibility
checks. Successful stages commit transactionally and survive interruption;
failures remain journaled separately and never become score zero.
There is an unavoidable crash window after a provider responds but before its
local commit: exactly-once remote billing cannot be guaranteed.

Default minimum start spacing is 15 seconds for generator calls and 30 seconds
for judge calls, per model. Requests use a 180-second HTTP timeout and at most
three attempts, with exponential backoff (15 then 30 seconds), up to 25% positive
jitter, capped at 60 seconds. Retry-After/RetryInfo are respected even beyond the
backoff cap; a requested wait above 120 seconds defers the call rather than
retrying too early. These cooldowns survive a process restart. Optional per-model
rolling input-token budgets must come from actual project quotas; character/2
estimates used for reservations are heuristics, not tokenizer measurements.
The local rolling token window does not survive restart; wait a full minute and
account for other project traffic before resuming. Unknown quotas are not invented.

HTTP 429, each 500/502/503/504 status, transport timeouts, invalid JSON and invalid
schemas are separately diagnosed, including wrapped provider exceptions. Explicit
daily quota exhaustion, authentication, missing models and ordinary 4xx errors
are not retried. Unknown 429 scope stays unknown. Full resume stops at the first
exhausted stage; smoke tries at most once per stage with a total of two live judge
calls. Smoke can still test accuracy after a transient faith failure, while a
persisted provider cooldown may defer it. SDK retries are disabled so these call
budgets are meaningful. Sanitized JSON progress includes ID, stage, attempt,
completion counts and retry reason, with no raw error bodies, URLs or keys.

## Judge schema and interpretation

Faithfulness and accuracy use separate calls. Faithfulness sees question, actual
context and answer, **no gold answer**. It extracts atomic factual claims and
returns for each a French paraphrase, supported/unsupported/uncertain verdict,
and numbered chunk references. Supported claims require at least one valid
in-context chunk number. Schema checks reject bad types, missing/extra keys,
invalid verdicts, duplicate claims and out-of-range evidence references. Structural
validation does not prove that extraction is exhaustive or evidence entails claims.
The existing production evaluator's estimated global scores are not reused.

Faithfulness = supported / total factual claims. Unsupported and uncertain both
remain in the denominator. No factual claims -> null, excluded from the macro
mean with the excluded count reported; a pure abstention is not automatically
faithful. API/judge errors -> missing, never zero. The global and category macro
means use 10,000 question resamples, seed 42, percentile 95% intervals, excluding
missing and no-claim scores. Raw denominator/claim counts are reported, since
successful-only intervals may be biased by incomplete execution. Micro claim
counts are diagnostics, not a substitute for macro faithfulness.

Accuracy sees question, generated answer, approved French gold and scope/optional
rubric; it accepts equivalent wording and labels correct/partial/incorrect.
Pure abstention has null accuracy and is counted separately, especially for
answerable questions. Faithfulness does not establish correctness: a faithfully
repeated irrelevant fact can still be incorrect. Both judge abstention decisions
are preserved, and disagreement counts are reported rather than silently resolved.
For U01/U03/U05, appropriate abstention requires both recognizing missing support
and the context genuinely lacking sufficient support, according to the context
judge. Raw successful/total-judged counts and all three planned negatives are
reported. Missing judgments never enter the denominator as failed abstentions.

## Human audit and publication

Seed 42 samples 15 completed responses from sorted successful IDs. With fewer
than 15, export all available, and report the shortfall. With none, the committed
CSV is explicitly 15 pending question slots, not 15 evaluated responses. Its
answer/verdict/manual cells remain empty; filling them with synthetic answers
would misrepresent execution. Full exact audit is local at
`data/output/eval/generation/judge_audit.csv`; eval/judge_audit.csv is its public
review copy. Exact eight-word matches to retrieved source chunks cause the whole
public answer to be withheld, while the local answer remains intact. This is a
conservative overlap check, not a copyright clearance guarantee for text quoted
from outside retrieved context. Human review is required before publishing any
actual generated text. Public result JSON omits full context and factual-claim
text; private cache retains them. Judge evidence references publish only chunk
numbers, source basenames and pages, never evidence excerpts. No judge-human
agreement is computed before Santiago fills the manual columns.

Offline tests exercise success-cache recovery, invalidation, bounded failures,
retry/backoff and rate limiting, claim ratios including uncertain/empty claims,
strict schemas, accuracy/abstention aggregation, audit sampling and overlap
redaction. Mocked tests cannot establish live API availability or judge quality.
See GENERATION_RESULTS.md and generation_results/ for the actually executed
status, and keep Phase 2A artifacts unchanged. No optimization is authorized here.
