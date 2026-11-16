# Phase 2B generation evaluation — blocked execution

Run: [2026-11-16T105449Z_ca7bbd8d.json](generation_results/2026-11-16T105449Z_ca7bbd8d.json), implementation commit
`ca7bbd8d4e50db796afbe51af02055b0236c616c`. Phase 2A [retrieval results](RESULTS.md) remain frozen at
baseline `3191452`.

## Actual execution

The runner executed local preflight and exited with status 2 because neither
`GOOGLE_API_KEY` nor `GEMINI_API_KEY` was available in the environment or local
`.env`. **No retrieval, model-access, generation or judge API call was made.**
All 45 question records explicitly have `not_run_missing_credentials` status;
none is silently omitted or scored zero.

| Measure | Observed execution | Quality estimate |
| --- | --- | --- |
| Generation completion | 0/45 (0%) | Execution count only |
| Faithfulness evaluations | 0/45 | Unavailable; no mean or 95% CI |
| Answer accuracy evaluations | 0/45 | Unavailable; no correct/partial/incorrect percentages |
| Negative-question abstention | 0 judged of 3 planned | Unavailable; no percentage |
| Response-level failure analysis | No generated responses | Unavailable |

The JSON contains zero **counts of observed verdicts**, null accuracy/abstention
percentages and an empty faithfulness estimate. These are missing evaluations,
not evidence of incorrect answers or failed abstentions. U01, U03 and U05 remain
separate negatives; no retrieval recall was computed for them in Phase 2B.
There are no observed remote API failures, because no remote request was made.

## Configuration and independence

The production generator is `gemini-3.1-flash-lite`, temperature 0.2, using the
unchanged French production prompt and original context formatter. The configured
judge is `gemini-2.5-flash`, temperature 0, with separate claim-support and
reference-answer accuracy calls. Neither model's current availability, quota or
resolved API version could be checked. The JSON records requested identifiers and
installed package versions, not invented API versions. Independent model judging
is **configured but unexecuted**; both identifiers belong to the same provider.
No substitution occurred.

The implemented runner replays exact ordered Phase 2A MMR contexts for the 42
answerable questions and caches original MMR retrieval for the three negatives.
That generation path did not execute here. The local success cache supports
resumption and separate generation/judge checkpoints, bounded retries and rate
limiting. See [GENERATION.md](GENERATION.md) and
[generation_config.yaml](generation_config.yaml) for full definitions. Uncertain
claims remain in the faithfulness denominator; answers with no factual claims
have null faithfulness. Abstentions and execution errors are separate from
incorrect factual answers.

## Category execution breakdown

| Category | Planned | Generated | Faith judged | Accuracy judged |
| --- | ---: | ---: | ---: | ---: |
| cross_book | 7 | 0 | 0 | 0 |
| factual_simple | 11 | 0 | 0 | 0 |
| multi_passage | 10 | 0 | 0 | 0 |
| paraphrase | 5 | 0 | 0 | 0 |
| rare_detail | 9 | 0 | 0 | 0 |
| unanswerable | 3 | 0 | 0 | 0 |

## Checks performed

- **24 deterministic tests passed**: 15 generation/cache/judge tests and the 9
  existing retrieval-metric tests. Provider calls were mocked, never executed.
- Structural checks passed for all 45 statuses, missing-score denominators,
  U01/U03/U05 membership, 15 unique pending audit slots and empty manual cells.
- All seven original PDF SHA-256 values matched the corpus manifest. Approved
  question and annotation hashes matched the freeze. The execution artifact's
  code/configuration hashes matched the implementation files.
- A diff against `3191452` confirmed no changes to app.py, src/, approved
  questions/references, the dataset freeze, retrieval config, Phase 2A RESULTS.md
  or numerical retrieval artifacts. Local generation/audit/cache paths are ignored.

The first CLI attempt at `9972e32` failed locally during optional-package version
capture before creating results or making API calls. Commit `ca7bbd8` fixed this
and added a regression test; the linked artifact is the subsequent completed
credential preflight. No model result was lost or replaced.

## Pending human review and execution

[judge_audit.csv](judge_audit.csv) contains **15 pending sampled question slots**
(seed 42), with empty answers, verdicts and manual columns. It does not constitute
an audit of 15 responses. No judge-human agreement is reported. The local audit
copy is under ignored data/output/eval/generation/; no new answer or context was
generated. The future public audit withholds detected source-overlap answers;
actual generated text still needs human copyright review before publication.

Provide credentials locally, rerun the documented command, then review actual
answers, claim evidence and accuracy verdicts. Current results cannot support a
CV claim about generation quality. Santiago approved question selection/wording;
this does not claim independent human verification of every evidence annotation.
Small-sample, editorial-selection and judge-provider biases remain, and there
are only three negative questions. Response error analysis and the human audit
remain pending. Production behavior and retrieval parameters were not optimized.
