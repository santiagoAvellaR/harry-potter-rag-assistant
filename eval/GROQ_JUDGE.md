# Optional GroqCloud judge

Production Gemini generation (gemini-3.1-flash-lite, temperature 0.2), questions,
retrieval contexts/settings and Phase 2A remain unchanged. This adapter only judges
existing cached answers. It never retrieves or generates answers. Existing live
run reports and audit CSV are not overwritten. No full-cohort command is added or
executed by this change.

## Interface and methodology

Install evaluation-only requirements in your chosen environment:

```bash
python -m pip install -r eval/requirements-judge.txt
python eval/run_alternative_judge.py --provider groq --question F01
# Only if the preflight permits the complete paired requests:
python eval/run_alternative_judge.py --provider groq --question F01 --smoke
```

The default is offline token preflight; --smoke permits at most two inference
attempts, one per stage. GROQ_API_KEY is read from the environment or ignored .env,
never logged. The provider-neutral callable also supports --provider gemini using
the original evaluator adapter. The original Gemini runner remains available.
The optional tokenizer's public vocabulary may require a first-use download.
No source PDFs or novel data are downloaded.

Groq uses openai/gpt-oss-120b, temperature 0, OpenAI-compatible HTTPS chat
completions with strict JSON schema. All fields are required and objects disallow
additional properties. Existing judge prompts, claim extraction/support labels,
uncertain/empty-claim treatment, accuracy labels and abstention definitions are
unchanged. Existing local semantic validators still run after structured decoding;
JSON/schema errors remain errors, never score zero. The exact numbered context
and cached generated answer are sent unchanged, without truncation or summarizing.
The transport adds a strict schema, which is an explicit provider-specific
methodological difference. No schema fallback or model substitution occurs.

Judge keys include provider, model, temperature, schema hash, exact request,
context/answer inputs, dataset bindings and semantic validator identity. Existing
Gemini judge entries cannot satisfy Groq keys. Previously evaluated answers must
therefore be rejudged with Groq; no aggregate combines providers. This bounded
runner exports separate stage results, not a mixed quality aggregate. Original
opaque generation keys are recovered through the existing verified migration;
only judge configuration changes, never generation identity or successful payloads.

No provider SDK retry layer is introduced. Groq's HTTP status and Retry-After feed
the existing bounded retry/cooldown logic. Explicit TPD/RPD exhaustion is classified
as daily quota; TPM throttling remains retryable. Groq operational cooldown scopes use
provider:model, so Gemini exhaustion cannot block Groq. Gemini retains its original
model scope to honor existing persisted cooldowns. Smoke is one attempt per
stage, two total, with 65-second spacing and persistent cooldowns; explicit daily
exhaustion stops the second attempt. Response model alias, optional system
fingerprint and actual token usage are retained when available. These are not
claimed to pin an immutable backend model revision.

## Measured F01 suitability

On 2026-11-16 the exact cached requests were encoded using tiktoken 0.14.0,
o200k_harmony. Content and schema BPE counts are computed locally; the extra
128-token chat/server-schema allowance is an estimate. Backend input usage and
output/reasoning usage are unavailable without inference. Output tokens are not
included in these estimates.

| Stage | Content BPE tokens | Schema BPE tokens | Estimated input including overhead |
| --- | ---: | ---: | ---: |
| Faithfulness | 11,757 | 152 | 12,037 |
| Accuracy | 325 | 64 | 517 |

[Groq's published free-tier table](https://console.groq.com/docs/rate-limits)
lists GPT-OSS 120B at 8,000 TPM, 200,000 TPD, 30 RPM and 1,000 RPD. Limits apply
at organization level and actual organization exceptions may differ. No actual
organization quota was queried. The input alone already exceeds published TPM
for faithfulness; output/reasoning only adds demand. Waiting between requests
does not make this oversized single request compatible. TPD limits additionally
require budgeting across the remaining questions and outputs; no 45-question
token total has been measured or fabricated.

The model's [131,072-token context window](https://console.groq.com/docs/model/openai/gpt-oss-120b)
can accommodate the request, but context capacity does not establish throughput.
[Strict schema support](https://console.groq.com/docs/structured-outputs) is
documented for this model. The model is technically a candidate on an account
with sufficient verified quotas, but the **published free tier is unsuitable for
the unchanged full evaluation**, since F01 alone cannot pass the input gate.
A full run is not recommended. Higher organization throughput and daily budget
would need verification, followed by the paired smoke test and homogeneous
rejudging of all generated answers. Do not shorten the benchmark context to fit.

## Actual execution and checks

Offline preflight executed; no Groq inference, answer generation or retrieval
call was made. The paired smoke was blocked before credential use. No Groq model
version, account access, schema decoding quality or accuracy verdict is claimed
as live-verified. The output artifact records missing stages, not zero scores.
All 12 original successes present at the start of this task remained byte-identical.

43 offline tests passed: strict schemas and transport payload, provider/model/
schema/input cache isolation, Groq daily versus minute limits, Retry-After and
throughput gate, plus existing cache/retry/metric tests. The API adapter was tested
with a fake HTTP transport; this does not establish live model availability.
Code and token-only results are versioned; contexts, generated answers, keys,
private semantic manifests and token vocabulary stay outside committed artifacts.

Latest committed-source token preflight: [2026-11-16T135941Z_groq_preflight.json](alternative_judge_results/2026-11-16T135941Z_groq_preflight.json).
