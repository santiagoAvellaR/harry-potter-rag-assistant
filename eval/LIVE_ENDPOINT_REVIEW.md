# Live OpenRouter endpoint review — 2026-11-16

No previous Qwen endpoint was queried or retried. The two requested public endpoint
APIs were refreshed directly. Reduced reference-only responses are versioned as
provider_metadata/ernie_live.json and provider_metadata/nemotron_live.json.

| Model | Advertised provider | Structured outputs / temperature | Max prompt tokens | Published TPM |
| --- | --- | --- | --- | --- |
| baidu/ernie-5.5-flash-preview:free | Baidu, tag baidu | Both advertised | Not supplied (null) | Not supplied |
| nvidia/nemotron-3.5-super-vl:free | Nvidia, tag nvidia | Both advertised | 868,928 | Not supplied |

The endpoint names advertise ERNIE snapshot 20261110 and Nemotron snapshot
20261015, respectively. These are catalog labels, not verified inference response
versions. Their advertised context lengths are 1,024,000 and 1,000,000; neither is
a token-per-minute quota. Provider status was 0 and pricing was zero in the API.
No serving performance or request acceptance was measured.

## Preferred provider decision

ERNIE/Baidu was evaluated first. The [terms linked from OpenRouter's Baidu page](https://intl.cloud.baidu.com/en/doc/Agreements/s/bmesahnjh-intl-en),
sections 3A.3.1–3A.3.2, permit storing AI content for service improvement and using
non-personal content for machine-learning improvements. No OpenRouter-specific
exception applicable to this free endpoint was verified. Therefore this review
does not clear sending novel passages to that provider. This is a data-handling
decision for this benchmark, not a claim that an upload is necessarily unlawful.
OpenRouter's [logging documentation](https://openrouter.ai/docs/guides/privacy/provider-logging)
also distinguishes provider training policies and separate free-model settings.

The adapter requests data_collection=deny and pins the exact model and Baidu
provider with fallback disabled. This filter does not prove an acceptable route
exists. Policy clearance requires a documented, source-linked review; it is not
inferred from structured-output support. No inference request was sent to Baidu.
No inference request or automatic fallback was sent to Nvidia. Nvidia's endpoint
was inspected as metadata only; its policy was not cleared or live-tested.

## Other execution blockers

OPENROUTER_API_KEY was absent from both the process environment and ignored .env.
The authenticated account limit endpoint therefore could not be queried. No
account daily remaining requests, provider TPM or per-key burst limit was verified.
Published free-account request allowances must not be presented as this account's
verified quota. The existing 40-attempt local ceiling and ten-request daily reserve
remain enforced. Unknown endpoint TPM continues to block preflight, independently
of credential and policy issues.

The F01 context, French answer, original prompts and schemas are unchanged. Their
hashes are recorded in the preflight artifact. ERNIE's tokenizer was not supplied
by the endpoint; the existing 12,037/517 GPT-OSS token estimates are explicitly
cross-model proxies, not actual ERNIE token counts. Actual response usage and
inference latency are unavailable because **zero inference requests occurred**.
Both faithfulness and accuracy are unexecuted, never zero-scored. There was no
provider API failure to classify: the failure was at preflight.

## Code and verification

The existing adapter now accepts only explicit approved model IDs and includes
selected model_id in its provider-specific semantic cache identity. Automatic
openrouter/free routing is rejected. The CLI defaults to the preferred ERNIE model
for OpenRouter; Nemotron requires explicit selection. Actual response latency,
model/provider identifiers, fingerprint and token usage are retained when a future
permitted request returns. Original Gemini generations/verdicts are not rewritten.

51 offline tests passed, including fixed model/provider pinning, training-policy
routing filter, automatic-routing rejection, strict schemas, daily budget reserve,
429 handling, provider isolation and earlier cache/retry contracts. Existing user
run reports and uncommitted artifacts remain untouched. Production RAG, approved
questions, retrieval settings and Phase 2A remain unchanged.

## Full evaluation decision and next step

The full unchanged benchmark **cannot currently be recommended for this provider
on verified account quotas**, because account quotas are unverified, TPM is
unpublished, credentials are missing and Baidu data reuse was not cleared. No
full-cohort run occurred. Do not switch providers automatically.

First obtain a service-specific no-training/data-use clarification for the chosen
provider and verify actual provider/account quotas with credentials configured
locally. Refresh the same fixed endpoint metadata. Once policy and throughput
preflight pass, make only the paired F01 smoke, stopping on the first error.
Validate both responses with the existing local schemas and inspect their actual
usage/latency before considering homogeneous full-provider judging. With 90
judgments needed before retries, a 40-request/day operating budget would require
at least three quota days if no judgments were reusable; this is planning arithmetic,
not a verified account throughput result.

Final measured preflight: [2026-11-16T142953Z_openrouter_preflight.json](alternative_judge_results/2026-11-16T142953Z_openrouter_preflight.json). All 12 original cache successes remained unchanged.
