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
