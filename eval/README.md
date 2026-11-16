# Reproducible evaluation — candidate dataset

Phase 1b: [VALIDATION_PACKET.md](VALIDATION_PACKET.md) contains the current 45-item
proposal and applied corrections. [EVIDENCE.md](EVIDENCE.md) documents the annotation
sidecar. All 60 original candidates remain available; none are validated. The
earlier methodology below describes phase 1; SHORTLIST.md is the historical audit.


**Phase 1 only: human validation is pending.** The 60 entries in
[questions.jsonl](questions.jsonl) all have `status: "candidate"`. No benchmark
metrics, model answers, judge verdicts, or confidence intervals exist yet.
See [SHORTLIST.md](SHORTLIST.md) for the Phase 1 audit and proposed 45-question
cohort; its recommendations are pending human approval.
Start with [REVIEW.md](REVIEW.md) to accept, edit, or reject candidates and retain
40–50 validated questions before implementing and running the benchmark.

This evaluation is an individual follow-up to the original team project.
Codex (an AI assistant) drafted the questions and reference answers and inspected
the evidence. The repository owner has not yet validated them. The reviewer name,
date, and final selection must be recorded after that review, not inferred from
providing the PDFs.

## Dataset contract

Each UTF-8 JSONL record contains exactly these fields:

| Field | Meaning |
| --- | --- |
| `id` | Stable candidate ID; do not renumber retained entries. |
| `question` | A reader-style question in French. |
| `category` | `factual_simple`, `rare_detail`, `multi_passage`, `cross_book`, `paraphrase`, or `unanswerable`. |
| `gold_answer` | One or two French sentences, written in our own words. |
| `gold_pages` | A list of `{source, page}` references; empty only for unanswerable candidates. |
| `notes` | English scope, annotation rationale, and review cautions. |
| `status` | Currently `candidate`; only explicit human approval permits `validated`. |

`source` is the exact PDF basename, including the unusual spelling in the sixth
filename. Normalize retrieval paths to basenames when matching them later.
`page` is the **zero-based physical PDF page index**, matching the RAG loader's
page convention. The PDF viewer page is `page + 1`. Printed page labels, chapter
numbers, and the classic engine's one-based page IDs are different conventions.
The review table supplies both physical viewer pages and stored indices.

[corpus_manifest.json](corpus_manifest.json) records SHA-256 fingerprints and
physical page counts for the seven supplied PDFs, together with the app's
baseline commit. The files have respectively 208, 177, 288, 386, 694, 415, and 541
pages. Do not silently use another edition: pagination would invalidate the gold
references. All seven are below the classic parser's 1,000-page ID boundary.

## How the candidates were built and checked

1. Extract the supplied PDFs using Poppler `pdftotext 25.03.0 -layout`, preserving
   form-feed page boundaries. Keep these extracts under `data/output/eval/`.
2. Locate candidate scenes by direct reading and literal searches. No project
   retriever, embeddings, Chroma index, BM25 output, Gemini answer, or retrieval
   score was used to choose or amend the questions.
3. Draft French questions and short reference answers separately from the
   passage wording. Cover both familiar events and localized details, across all
   seven novels; avoid book introductions/interviews as gold evidence.
4. Read the full extracted text of every cited page. Reopen each cited physical
   page independently with `pdftotext -f N -l N -layout` and compare it with the
   initial extraction. All **88 distinct gold pages** matched. Render every one
   with `pdftoppm` and inspect the labeled page contact sheets as an additional
   pagination/content check. These are AI evidence checks, not human validation.
5. Include page continuations when the answer crosses a physical page boundary;
   include verified alternative supporting occurrences found during the review.
   Search for possible counterexamples to unanswerable questions and leave those
   questions explicitly subject to human review.

This is an editorially constructed sample, not a random sample of pages or a
sample of real user traffic. Familiar scene leads informed some searches; the
absence of retriever-based selection does **not** make the sample unbiased.
Rarity and completeness are provisional annotations. The corpus was not read
exhaustively sentence by sentence, and literal search cannot certify that no
additional paraphrased answer or retrospective recap exists. Add any overlooked
support during human review, before observing system performance.

The candidate distribution is 15 factual, 12 rare-detail, 12 multi-passage,
10 cross-book, 6 paraphrase, and 5 unanswerable questions. Book coverage is shown
in REVIEW.md; a cross-book question contributes to more than one book. The six
paraphrase items are standalone low-lexical-overlap formulations, not duplicates
of another factual question in the set. Difficulty labels are editorial, not
measured results.

## Relevance and annotation limitations to preserve in the report

The existing loader splits each page separately into chunks of up to 2,500
characters with 500 characters of overlap. It does not join pages. Therefore a
chunk can match a single `(source, page)` pair; several chunks may map to the same
page. Later page-recall must deduplicate covered pages, while preserving chunk
ranks for Hit@k and reciprocal rank. This behavior was inspected in the source;
no LangChain extraction or retrieval run was performed during phase 1.

A continuous passage crossing a page boundary is still `factual_simple`,
`rare_detail`, or `paraphrase`, according to the question; `multi_passage` means
distant scenes in one novel. `cross_book` combines evidence from different novels.
Reviewers must check that a later summary does not make a supposedly multi-scene
question answerable from one passage.

The requested **flat gold-page set mixes complementary and alternative evidence**.
For example, the password in R08 is supported independently on two pages. Page
recall counts both, so retrieving one sufficient page would yield a hit but
incomplete page coverage. M07, M08, C03, C10, and P03 have similar alternatives or
retellings noted in their records. Do not conceal this by reporting page recall
as answer completeness or by dropping alternative evidence after seeing results.
No alternative-set scoring extension has been implemented; the requested metric
is unchanged. This issue should be settled or explicitly accepted at review.

Some candidates share evidence or sub-answers (notably F02/M02 and F05/C02).
The final selection should reduce unnecessary duplication. A future bootstrap
over questions will quantify variability in this small annotated set, not remove
author selection bias, annotation uncertainty, or dependence between related
questions.

Unanswerable claims are limited to the seven novels. U01 has a film-scene premise;
the novel does contain radio broadcasts and a briefly heard song, which is not
evidence of the proposed dance. U02 needs particular scrutiny because the novel
names Brockdale bridge, whereas the question specifies the London scene. U03
asks for original names, not the invented Wilkins identities. U04 cannot be
answered from teaching tenure alone, and U05 cannot be answered from Dobby's pay
or Slughorn's remarks about his own salary. The review table links these
counterchecks without putting them into `gold_pages`.

## Local artifacts and reproducibility

Source PDFs, bulk extracts, per-page text, rendered page images, and the local
verification log stay in `data/input/` or `data/output/eval/`. The existing
`.gitignore` excludes the PDFs and everything under `data/output/` except its
placeholder. Only questions, paraphrased reference answers, reference metadata,
and documentation belong in Git. Do not force-add any local corpus artifacts.

To reopen an evidence page locally, from the repository root:

```bash
mkdir -p data/output/eval
pdftotext -f 95 -l 95 -layout \
  data/input/harry-potter-1-lecole-des-sorciers.pdf \
  data/output/eval/book1-pdf95.txt
pdftoppm -f 95 -l 95 -singlefile -scale-to 1400 -png \
  data/input/harry-potter-1-lecole-des-sorciers.pdf \
  data/output/eval/book1-pdf95
```

This example corresponds to JSON `page: 94`. Neither command uses the RAG
pipeline. The dataset itself is the fixed reproducible artifact; its editorial
creation was not a seeded random sampling procedure.

## Execution status and next gate

Executed: PDF inventory and hashes; page-preserving text extraction; literal
search and evidence reading; independent reopening and rendering of gold pages;
JSONL/schema/category/page-reference checks; checks that corpus artifacts remain
ignored by Git.

Not executed: indexing, retrieval benchmarks, generation, LLM judging, bootstrap
confidence intervals, judge audit sampling, or Streamlit startup. The app and its
parameters were not modified, so no app refactor was needed. The environment's
`python3` does not currently have `pypdf` installed; Poppler sufficed for dataset
preparation. Dependency setup and runtime verification belong to the next phase.

**Stop here for the owner's review.** After validation, implement the CLI harness
and metric tests, freeze the dataset hash and runtime configuration, and run the
existing pipeline unchanged. Only real completed executions may populate
`RESULTS.md`, result JSON files, or the root README's benchmark summary.
