#!/usr/bin/env python3
"""Render numerical retrieval results without copying corpus text into documentation."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def cell(group, key):
    v=group['metrics'][key]
    lo,hi=v['ci95']
    return f"{v['mean']:.3f} [{lo:.3f}, {hi:.3f}]"


def render(path):
    r=json.loads(path.read_text())
    complete={name:s for name,s in r['systems'].items() if s['status']=='completed'}
    s=f'''# Retrieval benchmark — Phase 2A

Run: [{path.name}](results/{path.name}). Execution status: **{r['execution_status']}**.
Started {r['started_utc']}; finished {r['finished_utc']}.
Code commit: `{r['commit']}`; working tree dirty at launch: `{r['git_dirty']}`.
Dataset SHA-256: `{r['dataset_sha256']}`.

Santiago approved the 45-question selection and wording on 2026-11-16. He did
not independently validate every PDF evidence page or sidecar bundle. The labels
remain AI-authored and AI-checked, with evidence review pending. Exactly 42
answerable questions are evaluated; U01/U03/U05 are excluded from every retrieval
aggregate. No generation, Gemini call, faithfulness score or judge result exists.
This is an individual follow-up to the original team project.

## Global comparison

Cells are macro means with 95% question-bootstrap percentile intervals.
MRR is truncated at rank 12; a relevant result below 12 counts as a miss.

| System | n | Hit@5 | Flat Recall@5 | Flat Recall@12 | MRR@12 | Need coverage@12 | All needs@12 |
| --- | ---: | --- | --- | --- | --- | --- | --- |
'''
    for name,o in complete.items():
        g=o['global']
        s+=f"| {name} | {g['n']} | "+' | '.join(cell(g,k) for k in ['hit@5','recall@5','recall@12','mrr','need_coverage@12','all_needs@12'])+' |\n'
    s+='\n## Every evaluated prefix\n\n| System | k | Hit | Flat page recall | Evidence-need coverage | All-needs coverage |\n| --- | ---: | --- | --- | --- | --- |\n'
    for name,o in complete.items():
        for k in r['config']['ks']:
            s+=f'| {name} | {k} | '+' | '.join(cell(o['global'],f'{m}@{k}') for m in ['hit','recall','need_coverage','all_needs'])+' |\n'
    s+='\n## Category breakdown\n\nEvery prefix and category interval is also stored in the result JSON.\n\n| System | Category | n | MRR@12 |\n| --- | --- | ---: | --- |\n'
    for name,o in complete.items():
        for c,g in o['categories'].items():s+=f"| {name} | {c} | {g['n']} | {cell(g,'mrr')} |\n"
    s+='\n| System | Category | k | Hit | Flat recall | Need coverage | All needs |\n| --- | --- | ---: | --- | --- | --- | --- |\n'
    for name,o in complete.items():
        for c,g in o['categories'].items():
            for k in r['config']['ks']:
                s+=f'| {name} | {c} | {k} | '+' | '.join(cell(g,f'{m}@{k}') for m in ['hit','recall','need_coverage','all_needs'])+' |\n'
    s+='\n## Execution and reproducibility\n\n'
    for name,o in r['systems'].items():
        if o['status']!='completed':s+=f"- {name}: **{o['status']}** — {o.get('reason','unknown')}. No full-cohort metrics reported.\n"
        else:
            p=o['index_verification']
            s+=f"- {name}: completed {o['completed_questions']} queries. Index origin: {p['origin']}.\n"
    s+='''
MMR uses the production retriever, k=12 and fetch_k=50, with its library default
lambda=0.5. Cosine uses the same Chroma collection and embedding object. In the
installed langchain_community Chroma adapter, MMR selects a diverse subset but
returns that subset in candidate similarity order, not greedy selection order.
The harness preserves this exact production ordering. All prefix metrics use the
single returned top-12 list; MMR is not rerun with a different k for each prefix.
Cosine uses Chroma HNSW similarity search, not a separate exhaustive nearest-
neighbor scan. The cached sentence-transformer has a 128-token sequence limit;
long chunks may be truncated during embedding, without changing the 2,500-character
chunking configuration. This is a model property, not a benchmark adjustment.

The existing app vector index and classical artifacts were absent at inspection.
Fresh local builds use the production loader, embeddings, store and TD1→TD3
pipeline. The Chroma build uses batches only for insertion limits. Source/text
hashes and page pairs are compared against fresh PDF extraction, collection cosine
metadata is checked, and every stored vector is compared with recomputation using
the cached model weights. Corpus and embedding-file SHA-256 hashes and maximum
vector discrepancy are recorded in the numerical artifact. Subsequent vector
runs repeat these checks; classical reuse requires its code/artifact hash receipt.
These checks identify this fresh baseline, not an unavailable historical team index.

The classical comparison is **BM25-inspired**, not standard BM25. It keeps the
production parser, spell correction, boolean filtering and scoring (k1=1.2, no
length normalization, title weight=3). It returns pages rather than chunks. The
adapter adds ascending numeric ID only for equal-score ties, whose production
order otherwise depends on set iteration. It does not relax boolean matches,
change query terms or substitute another BM25 implementation.

Run from the repository root in the recorded environment:

```bash
python -m unittest discover -s eval/tests -v
python eval/check_annotations.py
PYTHONHASHSEED=42 python eval/run_benchmark.py --build-index
python eval/write_report.py --result eval/results/<run>.json
```

`--build-index` permits absent local indexes to be built; it never downloads the
PDFs. Embedding assets must already be cached at the configured revision. No .env
is loaded. Network access is disabled for model loading and no Gemini client is
constructed. CPU execution uses one Torch thread and fixed seeds; the package
versions, actual source hashes and configuration are recorded. HNSW approximate
search, software/hardware differences and tie behavior may still affect a rebuilt
index. This is a reproducible baseline procedure, not a promise of bit-identical
HNSW results on every machine. Context caches stay under data/output/ and are not
published; committed results contain references and hashes only.

Bootstrap: for each system/global or category group, draw 10,000 samples of n
questions with replacement from its n scored questions, compute the macro mean,
and take the 2.5th and 97.5th percentiles using NumPy linear quantiles. Seed 42 is
reset per group; metric columns share resamples. Intervals are conditional on this
small fixed editorial cohort. They are not population guarantees or significance
tests of system differences; category intervals are especially unstable. Groups with all-zero or all-one observed values can have
zero-width percentile intervals; these do not establish zero population uncertainty. A
bootstrap cannot remove shared-event dependence or annotation uncertainty.

## Metric interpretation and limitations

Flat recall deduplicates covered `(PDF basename, zero-based physical page)` pairs
and divides by the historical flat gold-page count. Hit asks for at least one
historical relevant page, and MRR uses the original chunk rank; repeated chunks
from a page occupy ranks. Classical results each occupy one page rank, so equal k
is not equal context volume. Negative questions have no recall denominator and
are excluded, not assigned zero.

Evidence-need coverage is separately named: a need is covered if any annotated
route has all its pages present; needs complement each other. All-needs coverage
is one only when every required need is covered. Some one-page needs combine
several facts, while other questions have several needs, so need granularity is
an editorial choice. A page shared by multiple needs can satisfy all of them.
Partial route support does not count as a complete need. No content entailment
is checked by these page-level measures.

Historical flat labels retain context-only pages (notably M02/M03/C09), redundant
alternatives (M08/C03), and omissions of known alternatives (F09 PDF 358; M06 PDF
282). Thus flat recall can understate sufficient evidence retrieval, while a hit
on a context-only page may overstate support. Need coverage also depends on the
still provisional annotation bundles. Full page coverage may retrieve chunks
that do not contain the required passage. Physical PDF pages are specific to the
fingerprinted editions; printed page labels differ. The AI drafted and audited
labels; the owner approved questions/selection without independent exhaustive
page review. Familiar-scene selection, small size and related events limit external
validity. No pipeline parameter was tuned after observing these results.

## Inspected retrieval failures

Inspection details (references, hashes and diagnostic counts, without passages)
are in [diagnostics_2026-11-16_a76f1d6a.json](results/diagnostics_2026-11-16_a76f1d6a.json).
See the separately recorded review below. Failure causes require inspecting the
local retrieved chunks and gold pages; page misses alone cannot establish a
chunk-boundary, vocabulary or MMR-redundancy cause.
'''
    analysis=ROOT/'eval/FAILURE_REVIEW.md'
    if analysis.exists():s+='\n'+analysis.read_text()
    s+='''
## Verification actually performed

- Nine hand-calculated unit tests passed, including duplicates, empty retrieval,
  invalid/missing references, complementary bundles, alternatives, context labels,
  shared support and deterministic bootstrap bounds.
- Frozen-dataset/annotation checks passed with all 45 owner-approved selections,
  unchanged wording/flat references and pending independent evidence review.
- All 126 per-question metric vectors and every global/category bootstrap
  interval were recomputed from the saved page-only rankings and matched exactly.
- All seven PDF hashes matched. The index held 4,387 chunks over 2,697 nonempty
  pages; all stored vectors matched recomputation (maximum absolute discrepancy
  2.98e-7). Classical raw XML matched fresh production parsing.
- All local corpus/index/context artifacts were confirmed ignored; only the
  two data placeholders are tracked. No production app/source/ignore-rule diff
  exists against e201796. No production refactor was required; Streamlit itself
  was not launched during this retrieval-only task.

## Remaining Phase 2B work

Human review of retrieval results and evidence labels; then, only with explicit
authorization, generation caching/retries, independent-model claim-level fidelity
and correctness judging, negative-question abstention evaluation, and the 15-item
human judge audit. None of those stages has been implemented or executed here.
'''
    (ROOT/'eval/RESULTS.md').write_text(s)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--result',type=Path,required=True)
    render(p.parse_args().result)
