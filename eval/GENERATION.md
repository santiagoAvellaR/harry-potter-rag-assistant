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
/home/santiago/anaconda3/envs/rag/bin/python eval/run_generation.py
```

`generation_config.yaml` is separate from the frozen retrieval configuration.
Missing credentials produce a blocked versioned result for all 45 questions,
without importing the generation client or making API calls. Generator metadata
access is checked against the configured ID; unavailable original generator or
permission/quota failures halt rather than substituting a model. Different judge
ID `gemini-2.5-flash` is explicitly configured, not automatically discovered or
substituted. Its availability and exact API metadata are recorded when credentials
permit. Metadata access does not guarantee subsequent generation quota. Actual
response metadata (including resolved model version if supplied by the API) is
retained; an unreported API version is not invented. Both models are from Google,
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
Cache keys bind question, model/temperature, full production/judge prompt,
context digest (content/order/metadata), code/configuration hashes, package
versions, API model metadata and frozen dataset/annotation hashes. Accuracy keys
also bind the gold answer and optional-detail rubric. Successful stages commit
transactionally and are reused after interruption; a judge error does not require
regenerating a completed answer. Failures are journaled, never cached as success.
There is an unavoidable crash window after a provider responds but before its
local commit: exactly-once remote billing cannot be guaranteed.

Calls have five-second minimum spacing, at most three attempts, exponential
backoff of five then ten seconds (capped at forty), and a 90-second timeout.
SDK retries are disabled where exposed to avoid multiplying these bounds.
Authentication/model-not-found errors halt immediately; repeated quota errors
halt the run. Successful results remain resumable. Invalid judge JSON/schemas are
retried at most three times and recorded as missing if exhausted. Provider error
text/URLs are not serialized; sanitized categories and attempt counts are used.
The live provider/transport path remains untested when credentials are absent.

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
