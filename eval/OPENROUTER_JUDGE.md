# Fixed OpenRouter free judge: blocked endpoint preflight

The optional provider is OpenRouter, fixed model qwen/qwen3.8-27b:free. The adapter
never uses openrouter/free. Generation remains Gemini gemini-3.1-flash-lite at
0.2. Approved questions, production code, original evaluation prompts, contexts,
answers and Phase 2A remain unchanged.

## Observed availability and tokens

On 2026-11-16, the public [model endpoint API](https://openrouter.ai/api/v1/models/qwen/qwen3.8-27b:free/endpoints)
returned the model record with **endpoints: []**. A reduced, reference-only
snapshot is saved in provider_metadata/openrouter_qwen_free.json. No serving
provider, request-size limit, TPM or structured-output capability could be
verified. The advertised context capacity is not a throughput measurement.
Preflight therefore blocks inference. This does not claim that the model ID is
invalid or permanently unavailable.

The public Qwen/Qwen3.8-27B tokenizer was downloaded without weights, pinned to
revision 37561816e66b5b9153b1b64c10968c18c1e6f4a0, and kept under ignored
data/output/eval/tokenizers/qwen3.8-27b/. SHA-256 fingerprints are recorded in
the result artifact. Counting the unchanged cached F01 request locally produced:

| Stage | Request characters | Exact local Qwen content tokens | Schema tokens | Estimated input with 128-token overhead |
| --- | ---: | ---: | ---: | ---: |
| Faithfulness | 29,023 | 12,030 | 152 | 12,310 |
| Accuracy | 1,575 | 331 | 64 | 523 |

These are not backend usage measurements: actual server chat templates, schema
handling, output/reasoning token usage and deployed tokenizer revision are
unknown. Schema tokens are a hypothetical strict-output budget, not evidence
that a serving endpoint supports that schema. The earlier GPT-OSS proxy preflight
is retained locally under ignored preflight_history/ and superseded by these Qwen counts.

**No paired inference smoke was performed**, since endpoint/throughput preflight
did not pass. Both stages remain unexecuted, not score zero. No model revision,
provider identity or live output validity is claimed. All 12 successful cache
payloads present before this task remained unchanged.

## Adapter, caching and limits

OPENROUTER_API_KEY is read only from environment or ignored .env. The existing
provider-neutral factory, local verdict validators, sanitized error classifier,
bounded Caller and persistent cooldown mechanism are reused. Endpoint parameters
are inspected: temperature 0 is sent only when advertised; strict json_schema is
used when structured_outputs is advertised, otherwise advertised JSON-object mode
or the original JSON-instructing prompt is used. Local schema validation always
runs. Endpoint identity and supported parameters bind judge cache identity along
with provider, fixed model, schema hash, exact request/context and dataset.
Gemini/Groq judgments cannot satisfy these keys; no mixed aggregate is produced.
Operational throughput metadata is excluded from semantic judge identity.

Routing pins one advertised provider with fallbacks disabled. Unknown TPM blocks
rather than assuming unlimited throughput. Before a requested smoke, public
endpoint metadata is refreshed. A paired smoke makes at most one attempt per
stage and stops after **any** first-stage failure; there are no automatic retries
inside this pair. Error bodies, keys, source passages and full answers are never
published. Response model/provider, optional fingerprint and usage are retained
only when actually returned.

The documented [free account limit](https://openrouter.ai/docs/api/reference/limits)
is 50 inference requests/day and 20/minute for free models. The implementation
reserves 10 daily requests: a persistent local ledger allows at most 40 attempts,
including failures, and checks the account's free-model remaining quota before
every submission. Unknown remaining quota or ten-or-fewer remaining requests
blocks inference. Other account traffic can race this check, so use one process
and leave the reserve intact. Retry-After is handled by the common cooldown path;
daily 429 signals are distinguished from transient throttling.

## Tests and resumption

49 offline tests passed, covering fixed routing, parameter negotiation, provider
cache isolation, daily reserve, 429/Retry-After, original cache preservation and
existing schema/retry contracts. No OpenRouter inference or full-cohort execution
occurred. Existing user-run report, audit CSV and uncommitted historical artifacts
were left untouched.

```bash
# Requires the local public tokenizer files described above:
python eval/run_alternative_judge.py --provider openrouter \
  --endpoint-snapshot eval/provider_metadata/openrouter_qwen_free.json
# Only after endpoint and throughput checks become possible:
python eval/run_alternative_judge.py --provider openrouter --smoke
```

Do not resume the full benchmark now. Refresh the endpoint catalog; require an
actual provider, sufficient request-level/TPM capacity and known account budget.
Then run only the paired F01 smoke and review both verdicts. Rejudge all answers
with this provider before producing a homogeneous aggregate. Forty-five responses
require 90 successful judge calls before retries; with the 40/day operating budget,
at least three quota days would be needed without reusable OpenRouter judgments.
Availability, latency and actual throughput are unverified, so suitability for the
unchanged full evaluation is **not established**. No automatic full-run mode is
added by this task.

Observed final artifact: [2026-11-16T141050Z_openrouter_preflight.json](alternative_judge_results/2026-11-16T141050Z_openrouter_preflight.json).

To reproduce the tokenizer setup without downloading model weights, run in the
existing RAG environment (install eval/requirements-judge.txt first):

```python
import hashlib, json, urllib.request
from pathlib import Path
result = json.loads(Path('eval/alternative_judge_results/2026-11-16T141050Z_openrouter_preflight.json').read_text())
manifest = result['tokenizer']
folder = Path('data/output/eval/tokenizers/qwen3.8-27b')
folder.mkdir(parents=True, exist_ok=True)
for name, digest in manifest['files'].items():
    url = f"https://huggingface.co/{manifest['model']}/resolve/{manifest['revision']}/{name}"
    data = urllib.request.urlopen(url).read()
    assert hashlib.sha256(data).hexdigest() == digest
    (folder / name).write_bytes(data)
(folder / 'manifest.json').write_text(json.dumps(manifest, indent=2))
```
