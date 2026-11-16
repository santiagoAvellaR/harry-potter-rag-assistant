# Evidence annotation sidecar (phase 1b)

Current freeze (2026-11-16): Santiago approved the 45 selected questions and their
wording for retrieval evaluation. Selected records now have `status: validated`;
the other 15 remain candidates. This does **not** record independent owner
verification of every evidence page or annotation. Evidence `human_review` stays
`pending`. See [dataset_freeze.json](dataset_freeze.json) for scope and hashes.
The phase-1 narrative below is historical where it describes pending selection.


`evidence_annotations.json` is a review artifact, not a benchmark harness. It
selects 45 of the 60 candidates by stable ID. Excluded candidates remain intact
in questions.jsonl; a reader must use `proposed_ids` rather than silently treating
all 60 as the proposed cohort. Selection is not validation. All question statuses
remain `candidate`, and all annotation `human_review` values are `pending`.

The file binds annotations to the exact questions.jsonl SHA-256. The existing
corpus manifest binds page references to the seven PDF hashes. Any approved
question edit requires updating that binding and refreshing the validation packet.
The exact field changes against audit baseline 4c63bc9 are in
`phase1b_changes.json`. No existing flat gold_pages were removed or added.

## Schema and semantics

Top-level fields are `schema_version`, `audit_baseline`, `questions_sha256`,
`selection_status`, `proposed_ids`, `excluded_ids`, `u04_decision`, and
`annotations` (an object keyed by exactly the proposed IDs).

Each annotation contains:

- `needs`: required French answer components. Each has `claim`, `required: true`,
  and nonempty `any_of` routes. All needs are complementary (AND).
- Each route has a nonempty `all_of` list of page references. Routes are
  alternatives (OR). Within a route, pages are complementary (AND).
- `context_only`: references useful for scene identification, not extra answer
  requirements. They must not also occur in a support route for that question.
- `counterchecks`: references used to investigate negative questions, never gold
  relevance. Answerable questions have no counterchecks; negatives have no needs
  or context-only pages and have empty flat gold_pages.
- `evidence_complete: false`: exhaustive evidence discovery is not claimed.
- `human_review: "pending"` and English `notes`: scope and review cautions.

Every reference is exactly `{source, page}` using the PDF basename and zero-based
physical page index. Viewer page = index + 1. No excerpt, quotation, chunk, image
or model result belongs in this file. Need claims are short paraphrases.

A need's mandatory pages are the intersection of pages in all its sufficient
routes; this is derivable rather than duplicated as a potentially inconsistent
field. A route with several pages requires those pages together. Reusing a page
across several needs is allowed (for example, P06 PDF 369 covers both repulsion
and embarkation). A single need may join inseparable facts across a page boundary
(C03's four appearances). Some simple single-page questions have one combined
need containing their full short reference answer.

Historical flat pages must appear somewhere in the sidecar's support or
context-only references for a selected answerable question. Additional support
pages are allowed without altering historical flat labels. Currently these are
F09 book 4 PDF 358 and M06 book 3 PDF 282. Optional answer elaborations in R03
and R12 do not become mandatory merely by being in gold_answer; the annotation
notes specify the scope. Human review can revise that scope before any run.

## Metric compatibility

This change implements annotations only. Flat Recall@k retains its original
page-union definition and historical labels; no metric is implemented, renamed,
or calculated. The sidecar must not silently replace that denominator. A page
classified context-only here still remains in the historical flat list. A newly
recorded alternative can satisfy a need without matching a historical flat page.
These known mismatches are explicitly presented for approval in the packet.

Future evidence-need coverage, if approved, would be a separate result. The human
must approve bundles, answer requirements and metric policy before the dataset
is frozen. Even complete annotated page coverage does not prove retrieved chunk
support, and a targeted reading does not prove there are no undiscovered recaps.

## Validation

From the repository root (Python standard library only):

```bash
python3 eval/check_annotations.py
python3 eval/check_annotations.py --verify-pdfs
```

The first command checks structure, selection, review-packet consistency, source
bounds, annotation roles, hashes, and preservation relative to the baseline.
It does not need the novels. The second also requires the original seven local
PDFs and Poppler: verifies their hashes/page counts and independently reopens each
referenced physical page, including selected historical labels and U04's tenure
countercheck. Text and opening hashes go to ignored
`data/output/eval/phase1b/`; no project module or model is imported. Missing PDFs
cause failure; nothing is downloaded or substituted. These are structural and
file-integrity checks, not semantic validation or retrieval metrics.
