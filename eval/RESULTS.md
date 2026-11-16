# Retrieval benchmark — Phase 2A

Run: [2026-11-16T093849Z_a76f1d6a.json](results/2026-11-16T093849Z_a76f1d6a.json). Execution status: **completed**.
Started 2026-11-16T09:38:49.515534+00:00; finished 2026-11-16T09:57:40.258156+00:00.
Code commit: `a76f1d6acf23715af5aad2bc1426becf783527f0`; working tree dirty at launch: `False`.
Dataset SHA-256: `af757856ca15e47238b62bad62be746bbd47d76d49bad3a00ca75fe67e71510f`.

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
| mmr | 42 | 0.286 [0.167, 0.429] | 0.226 [0.113, 0.345] | 0.250 [0.137, 0.375] | 0.212 [0.110, 0.324] | 0.274 [0.155, 0.405] | 0.214 [0.095, 0.333] |
| cosine | 42 | 0.357 [0.214, 0.500] | 0.282 [0.161, 0.413] | 0.294 [0.173, 0.425] | 0.225 [0.122, 0.337] | 0.310 [0.179, 0.440] | 0.262 [0.143, 0.405] |
| bm25_inspired | 42 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |

## Every evaluated prefix

| System | k | Hit | Flat page recall | Evidence-need coverage | All-needs coverage |
| --- | ---: | --- | --- | --- | --- |
| mmr | 1 | 0.143 [0.048, 0.262] | 0.125 [0.036, 0.226] | 0.131 [0.048, 0.238] | 0.119 [0.024, 0.214] |
| mmr | 3 | 0.286 [0.167, 0.429] | 0.226 [0.113, 0.345] | 0.250 [0.131, 0.381] | 0.214 [0.095, 0.333] |
| mmr | 5 | 0.286 [0.167, 0.429] | 0.226 [0.113, 0.345] | 0.250 [0.131, 0.381] | 0.214 [0.095, 0.333] |
| mmr | 12 | 0.333 [0.190, 0.476] | 0.250 [0.137, 0.375] | 0.274 [0.155, 0.405] | 0.214 [0.095, 0.333] |
| cosine | 1 | 0.143 [0.048, 0.262] | 0.125 [0.036, 0.226] | 0.131 [0.048, 0.238] | 0.119 [0.024, 0.214] |
| cosine | 3 | 0.286 [0.167, 0.429] | 0.228 [0.115, 0.349] | 0.238 [0.119, 0.369] | 0.214 [0.095, 0.333] |
| cosine | 5 | 0.357 [0.214, 0.500] | 0.282 [0.161, 0.413] | 0.298 [0.167, 0.429] | 0.262 [0.143, 0.405] |
| cosine | 12 | 0.381 [0.238, 0.524] | 0.294 [0.173, 0.425] | 0.310 [0.179, 0.440] | 0.262 [0.143, 0.405] |
| bm25_inspired | 1 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| bm25_inspired | 3 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| bm25_inspired | 5 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| bm25_inspired | 12 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |

## Category breakdown

Every prefix and category interval is also stored in the result JSON.

| System | Category | n | MRR@12 |
| --- | --- | ---: | --- |
| mmr | cross_book | 7 | 0.230 [0.016, 0.516] |
| mmr | factual_simple | 11 | 0.167 [0.000, 0.379] |
| mmr | multi_passage | 10 | 0.048 [0.000, 0.114] |
| mmr | paraphrase | 5 | 0.100 [0.000, 0.300] |
| mmr | rare_detail | 9 | 0.500 [0.222, 0.778] |
| cosine | cross_book | 7 | 0.262 [0.048, 0.548] |
| cosine | factual_simple | 11 | 0.203 [0.048, 0.400] |
| cosine | multi_passage | 10 | 0.037 [0.000, 0.090] |
| cosine | paraphrase | 5 | 0.100 [0.000, 0.300] |
| cosine | rare_detail | 9 | 0.500 [0.222, 0.778] |
| bm25_inspired | cross_book | 7 | 0.000 [0.000, 0.000] |
| bm25_inspired | factual_simple | 11 | 0.000 [0.000, 0.000] |
| bm25_inspired | multi_passage | 10 | 0.000 [0.000, 0.000] |
| bm25_inspired | paraphrase | 5 | 0.000 [0.000, 0.000] |
| bm25_inspired | rare_detail | 9 | 0.000 [0.000, 0.000] |

| System | Category | k | Hit | Flat recall | Need coverage | All needs |
| --- | --- | ---: | --- | --- | --- | --- |
| mmr | cross_book | 1 | 0.143 [0.000, 0.429] | 0.036 [0.000, 0.107] | 0.071 [0.000, 0.214] | 0.000 [0.000, 0.000] |
| mmr | cross_book | 3 | 0.286 [0.000, 0.714] | 0.107 [0.000, 0.250] | 0.143 [0.000, 0.357] | 0.000 [0.000, 0.000] |
| mmr | cross_book | 5 | 0.286 [0.000, 0.714] | 0.107 [0.000, 0.250] | 0.143 [0.000, 0.357] | 0.000 [0.000, 0.000] |
| mmr | cross_book | 12 | 0.429 [0.143, 0.857] | 0.179 [0.036, 0.357] | 0.214 [0.071, 0.429] | 0.000 [0.000, 0.000] |
| mmr | factual_simple | 1 | 0.091 [0.000, 0.273] | 0.091 [0.000, 0.273] | 0.091 [0.000, 0.273] | 0.091 [0.000, 0.273] |
| mmr | factual_simple | 3 | 0.273 [0.000, 0.545] | 0.273 [0.000, 0.545] | 0.273 [0.000, 0.545] | 0.273 [0.000, 0.545] |
| mmr | factual_simple | 5 | 0.273 [0.000, 0.545] | 0.273 [0.000, 0.545] | 0.273 [0.000, 0.545] | 0.273 [0.000, 0.545] |
| mmr | factual_simple | 12 | 0.273 [0.000, 0.545] | 0.273 [0.000, 0.545] | 0.273 [0.000, 0.545] | 0.273 [0.000, 0.545] |
| mmr | multi_passage | 1 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| mmr | multi_passage | 3 | 0.100 [0.000, 0.300] | 0.025 [0.000, 0.075] | 0.050 [0.000, 0.150] | 0.000 [0.000, 0.000] |
| mmr | multi_passage | 5 | 0.100 [0.000, 0.300] | 0.025 [0.000, 0.075] | 0.050 [0.000, 0.150] | 0.000 [0.000, 0.000] |
| mmr | multi_passage | 12 | 0.200 [0.000, 0.500] | 0.075 [0.000, 0.200] | 0.100 [0.000, 0.250] | 0.000 [0.000, 0.000] |
| mmr | paraphrase | 1 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| mmr | paraphrase | 3 | 0.200 [0.000, 0.600] | 0.100 [0.000, 0.300] | 0.200 [0.000, 0.600] | 0.200 [0.000, 0.600] |
| mmr | paraphrase | 5 | 0.200 [0.000, 0.600] | 0.100 [0.000, 0.300] | 0.200 [0.000, 0.600] | 0.200 [0.000, 0.600] |
| mmr | paraphrase | 12 | 0.200 [0.000, 0.600] | 0.100 [0.000, 0.300] | 0.200 [0.000, 0.600] | 0.200 [0.000, 0.600] |
| mmr | rare_detail | 1 | 0.444 [0.111, 0.778] | 0.444 [0.111, 0.778] | 0.444 [0.111, 0.778] | 0.444 [0.111, 0.778] |
| mmr | rare_detail | 3 | 0.556 [0.222, 0.889] | 0.556 [0.222, 0.889] | 0.556 [0.222, 0.889] | 0.556 [0.222, 0.889] |
| mmr | rare_detail | 5 | 0.556 [0.222, 0.889] | 0.556 [0.222, 0.889] | 0.556 [0.222, 0.889] | 0.556 [0.222, 0.889] |
| mmr | rare_detail | 12 | 0.556 [0.222, 0.889] | 0.556 [0.222, 0.889] | 0.556 [0.222, 0.889] | 0.556 [0.222, 0.889] |
| cosine | cross_book | 1 | 0.143 [0.000, 0.429] | 0.036 [0.000, 0.107] | 0.071 [0.000, 0.214] | 0.000 [0.000, 0.000] |
| cosine | cross_book | 3 | 0.429 [0.143, 0.857] | 0.155 [0.036, 0.310] | 0.143 [0.000, 0.357] | 0.000 [0.000, 0.000] |
| cosine | cross_book | 5 | 0.429 [0.143, 0.857] | 0.155 [0.036, 0.310] | 0.143 [0.000, 0.357] | 0.000 [0.000, 0.000] |
| cosine | cross_book | 12 | 0.429 [0.143, 0.857] | 0.155 [0.036, 0.310] | 0.143 [0.000, 0.357] | 0.000 [0.000, 0.000] |
| cosine | factual_simple | 1 | 0.091 [0.000, 0.273] | 0.091 [0.000, 0.273] | 0.091 [0.000, 0.273] | 0.091 [0.000, 0.273] |
| cosine | factual_simple | 3 | 0.273 [0.000, 0.545] | 0.273 [0.000, 0.545] | 0.273 [0.000, 0.545] | 0.273 [0.000, 0.545] |
| cosine | factual_simple | 5 | 0.455 [0.182, 0.727] | 0.455 [0.182, 0.727] | 0.455 [0.182, 0.727] | 0.455 [0.182, 0.727] |
| cosine | factual_simple | 12 | 0.455 [0.182, 0.727] | 0.455 [0.182, 0.727] | 0.455 [0.182, 0.727] | 0.455 [0.182, 0.727] |
| cosine | multi_passage | 1 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| cosine | multi_passage | 3 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| cosine | multi_passage | 5 | 0.100 [0.000, 0.300] | 0.025 [0.000, 0.075] | 0.050 [0.000, 0.150] | 0.000 [0.000, 0.000] |
| cosine | multi_passage | 12 | 0.200 [0.000, 0.500] | 0.075 [0.000, 0.200] | 0.100 [0.000, 0.250] | 0.000 [0.000, 0.000] |
| cosine | paraphrase | 1 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| cosine | paraphrase | 3 | 0.200 [0.000, 0.600] | 0.100 [0.000, 0.300] | 0.200 [0.000, 0.600] | 0.200 [0.000, 0.600] |
| cosine | paraphrase | 5 | 0.200 [0.000, 0.600] | 0.100 [0.000, 0.300] | 0.200 [0.000, 0.600] | 0.200 [0.000, 0.600] |
| cosine | paraphrase | 12 | 0.200 [0.000, 0.600] | 0.100 [0.000, 0.300] | 0.200 [0.000, 0.600] | 0.200 [0.000, 0.600] |
| cosine | rare_detail | 1 | 0.444 [0.111, 0.778] | 0.444 [0.111, 0.778] | 0.444 [0.111, 0.778] | 0.444 [0.111, 0.778] |
| cosine | rare_detail | 3 | 0.556 [0.222, 0.889] | 0.556 [0.222, 0.889] | 0.556 [0.222, 0.889] | 0.556 [0.222, 0.889] |
| cosine | rare_detail | 5 | 0.556 [0.222, 0.889] | 0.556 [0.222, 0.889] | 0.556 [0.222, 0.889] | 0.556 [0.222, 0.889] |
| cosine | rare_detail | 12 | 0.556 [0.222, 0.889] | 0.556 [0.222, 0.889] | 0.556 [0.222, 0.889] | 0.556 [0.222, 0.889] |
| bm25_inspired | cross_book | 1 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| bm25_inspired | cross_book | 3 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| bm25_inspired | cross_book | 5 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| bm25_inspired | cross_book | 12 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| bm25_inspired | factual_simple | 1 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| bm25_inspired | factual_simple | 3 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| bm25_inspired | factual_simple | 5 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| bm25_inspired | factual_simple | 12 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| bm25_inspired | multi_passage | 1 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| bm25_inspired | multi_passage | 3 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| bm25_inspired | multi_passage | 5 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| bm25_inspired | multi_passage | 12 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| bm25_inspired | paraphrase | 1 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| bm25_inspired | paraphrase | 3 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| bm25_inspired | paraphrase | 5 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| bm25_inspired | paraphrase | 12 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| bm25_inspired | rare_detail | 1 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| bm25_inspired | rare_detail | 3 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| bm25_inspired | rare_detail | 5 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |
| bm25_inspired | rare_detail | 12 | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] | 0.000 [0.000, 0.000] |

## Execution and reproducibility

- mmr: completed 42 queries. Index origin: fresh index built by production loader/embedding/store code; app index absent at inspection.
- cosine: completed 42 queries. Index origin: fresh index built by production loader/embedding/store code; app index absent at inspection.
- bm25_inspired: completed 42 queries. Index origin: fresh production TD1->TD3 build.

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

Failure review uses the persisted top-12 context caches, exact gold-page chunks
read from the local Chroma database, the phase-1 page readings, and targeted
production-parser diagnostics. No parameter, query, label or ranking was changed.
The references below are **physical PDF pages starting at one**.

| Question | Observed retrieval | Inspection and defensible interpretation |
| --- | --- | --- |
| F01 (plant identification) | Both systems rank B5:594 first; neither returns B1:95. | The top chunk concerns Rogue, Ombrage and Veritaserum, not the plant. In the exact gold-page chunks, the plant name appears only in the long chunk, at tokenizer position 332 without special tokens, beyond the encoder's 128-token window. This confirms omitted answer vocabulary during embedding and wrong-scene retrieval. It does not establish how much an alternative configuration would improve recall. |
| F13 (soul parts) | Cosine returns B6:319 at rank 5; MMR omits it while retaining B6:320 and 322. | The cosine rank-5 chunk is the first part of the right page and does not contain the requested number. The page's other chunk contains that number starting at token 159, also beyond the 128-token encoder window. A diagnostic replay of the unchanged fetch-50/MMR configuration exactly reproduced the original top-12 hashes: both gold-page chunks were present at candidate ranks 5 and 31, and MMR selected neither. This confirms selection-stage loss, while cosine's page-level success already overstates exact-passage support. This is a concrete chunk/page granularity problem, not proof that cosine could generate the correct answer. |
| R09 (ministry telephone code) | Cosine retrieves B5:101, 103 and 105 but not 102; MMR retrieves 105 but not 102. | The returned chunks describe travel preparations, visitor identification and movement inside the ministry; the code is on 102. One gold-page chunk places its first code digit at token 589; its shorter overlapping chunk places it at token 21, so truncation does not hide the code from every available chunk. The miss is nearby-scene ranking with a page boundary, not evidence that a boundary alone caused it. |
| M03 (Hagrid accusation and Ginny) | Neither system covers any historical gold page; MMR does return B2:160, adjacent to the required revelation on 161. Both rank B4:191 first. | The first chunk is about Harry warning Cedric about dragons and Hagrid's involvement, a different story. No complete accusation/revelation need is covered. This supports narrative/entity confusion and difficulty combining distant evidence. In the classical parser, the question's accusation wording is spell-corrected to an acceptance stem; the subsequent AND filter eliminates all candidates. Do not attribute this to MMR redundancy alone. |
| C03 (mirror and stone appearances) | Both rank B1:75 first; none of B1:141/144 or B7:500–501 is returned. | The top chunk is the train introduction of Drago, Crabbe and Goyle. The ranking does not recover either requested scene, rather than merely failing to stitch together already-present evidence. Cross-book scope and repeated character vocabulary coexist here; their causal contributions were not experimentally isolated. |
| C04 (mirrors and rescue) | Cosine returns B7:400 at rank 2; MMR returns none of the three flat gold pages. Cosine flat Recall@12 is 1/3 but need coverage is 0. | The returned chunk identifies Abelforth and discusses the mirror's purchase, but the jointly required rescue attribution is on B7:399, and the earlier detention use is on B5:684. The top chunk B6:395 is a different account of entry into Hogwarts. This is incomplete complementary evidence; a single page hit does not cover either annotated need in full. |
| C09 (cabinet events) | Both rank B2:69 first but omit B6:375–376. Flat Recall@12 is 1/4; need coverage is 1/2. | The top chunk contains Nick's diversion and Harry's avoided detention. It completely covers the first need; B2:68 is contextual rather than an additional mandatory need. The later repaired-cabinet entry route is missing. This confirms distant-evidence incompleteness and the historical flat denominator's context-page penalty. |
| F07 (boggart exam), classical path | The classical system returns no pages; both vector systems recover its gold page. | The production normalized query intersects eight terms. Its gold page B3:210 lacks the indexed terms corresponding to seeing, during and practical. All eight terms occur somewhere in the corpus, but their conjunction has no matching page. This is directly observed candidate-filter failure, not a measured failure of unrestricted BM25 ranking. F10 is the only nonempty classical query: it returns B5:221 and 226, neither the gold B5:216. |

Additional label diagnostic: P06 retrieves B6:369 at rank 2 under both vector
systems. That page covers both fire repulsion and protection to the boat, giving
need/all-needs coverage 1, but flat recall is 1/2 because B6:368 is also listed.
The unchanged historical labels therefore penalize sufficient known evidence.
Conversely F13 shows that retrieving the right page can reward an insufficient
chunk. No labels were changed after discovering either effect.

Across all 42 queries, MMR has **2 duplicate-page rank slots out of 504**, versus
**4 out of 504** for cosine. This is a small observed reduction in repeated pages,
not evidence that duplicates dominate failures. MMR loses useful historical pages
on F10/F13/M01 but gains pages on M04/C02; its net flat recall is lower in this
run. These observations support a selection trade-off, not an overall diversity
benefit or a statistically established superiority of cosine.

The classical system produces empty rankings on **41 of 42** questions; its only
two returned pages are non-gold. Its zero scores describe this exact parser,
spelling/stemming and boolean-prefiltered pipeline. No OR fallback was introduced.
A general claim that BM25 cannot answer these questions would be unsupported.

The README hypotheses receive mixed support: distant evidence and exact detail
ranking do fail in inspected cases; redundancy is small rather than dominant;
chunk/page boundaries and 128-token embedding truncation have concrete examples.
No controlled ablation establishes the improvement available from different
chunk sizes, overlap, embeddings, query decomposition or diversification. These
would be separate future experiments on a separate development set.

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
