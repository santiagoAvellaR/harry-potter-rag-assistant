# Phase 1 audit and proposed shortlist

Historical audit at 4c63bc9. Phase 1b applies its 11 EDIT recommendations; see
[VALIDATION_PACKET.md](VALIDATION_PACKET.md) for current wording and evidence
annotations. Statements below about unchanged data and absent sidecar describe
the audit baseline, not the current working dataset.


Audit baseline: `2d87c1e`; branch: `eval-benchmark`. This is an AI audit by Codex,
not human validation. All 60 original IDs, answers, references, and `candidate`
statuses are preserved. The dataset is **unchanged**; proposed editorial and
annotation edits below require review. No Phase 2 code or benchmark run occurred.

## Audit summary

Audited all 60 candidates against their questions, reference answers, scope notes,
and cited evidence. Recommendation: **34 ACCEPT / 11 EDIT / 15 REJECT**.
The proposed 45 comprise the 34 ACCEPT items plus 11 conditional EDIT items.
ACCEPT means recommended for human validation, not already validated. REJECT
means exclude from this shortlist; several rejected items remain useful reserves.

All seven supplied PDFs match the existing manifest hashes. Reopened all 88
existing gold pages individually from the PDFs with Poppler, plus eight new
countercheck/recap pages (96 distinct pages total). Read the questionable recaps
in context using literal searches and direct page text. Local audit extracts and
the opening log stay under ignored `data/output/eval/audit/`. Prior phase renders
were available; this audit used PDF text extraction and did not repeat rendering.

No clear factual contradiction was found in the French reference answers under
their stated scopes. The principal problems are incomplete alternative evidence,
over-specified support sets, category shortcuts and ambiguous answer scope.
No answer or reference was silently replaced. The original requirement to collect
all supporting pages cannot be certified by a targeted rather than exhaustive
corpus reading.

## Full recommendation table

Evidence notation: `B#:#` is **book : physical PDF viewer page (one-based)**;
subtract one for JSON `page`. `S` = stated answer supported on the cited pages;
`G` = grouping/minimality correction needed; `X` = category shortcut or ambiguity;
`N` = negative claim provisional, counterchecked but not proved corpus-wide.
All positive rows were checked for answer correctness, ambiguity, duplication,
wording overlap, and category fit. References shown here preserve the original
list; additional pages and their roles are detailed below. Proper names and
unavoidable event terms are not by themselves leakage.

| ID | Recommendation | In proposed 45? | Original evidence / status | Reason and required action |
| --- | --- | --- | --- | --- |
| F01 | EDIT | Yes, conditional | B1:95; S/G | Supported, but the yes/no contrast supplies both terms from the answer passage. Propose a neutral open question; see corrections below. |
| F02 | REJECT | No | B1:206; S | Correct, but its award is a sub-answer of M02; retain the synthesis question. |
| F03 | ACCEPT | Yes | B1:149; S | Both powers explicit on one page; gold is paraphrased. Keep immortality conditional on drinking the elixir. |
| F04 | ACCEPT | Yes | B2:51; S | Correct age-specific hazard; no fatal cry attributed to young plants. |
| F05 | REJECT | No | B2:175; S | Correct novel-specific sock/diary sequence, but duplicates the liberation half of C02. |
| F06 | ACCEPT | Yes | B3:24; S | Correct alias and scoped journey; name overlap is a necessary entity cue, not answer leakage. |
| F07 | ACCEPT | Yes | B3:210; S | Both apparition and feared failure explicit; distinct from generic boggart lore. |
| F08 | ACCEPT | Yes | B4:195; S | Dragon and order explicit in draw scene; answer is not supplied by question. |
| F09 | EDIT | Yes, conditional | B4:265; S/G | Correct direct scene; B4 PDF 358 also explicitly recounts Dobby bringing the plant. Add this alternative to future evidence annotations before scoring. |
| F10 | ACCEPT | Yes | B5:216; S | Blood and repeated wound mechanism explicit on the cited continuation page. |
| F11 | REJECT | No | B5:361; S | Supported under its lesson-specific scope; wording closely repeats the explanation. Drop to reduce easy canonical facts. |
| F12 | ACCEPT | Yes | B6:121; S | Reward and twelve-hour duration explicit; asks the promise rather than eventual winner. |
| F13 | ACCEPT | Yes | B6:319; S | Seven soul parts correctly distinguished from seven deliberately made Horcruxes. |
| F14 | ACCEPT | Yes | B7:273; S | Object and voice explicit; limited scope avoids needing the next page’s travel mechanism. |
| F15 | REJECT | No | B7:343; S | Supported, but the broad intention question permits several emotional answers beyond the inscription. Lower priority than F14. |
| R01 | ACCEPT | Yes | B1:54; S | All flavors and nuts explicit; localized sensory detail, answer vocabulary absent from question. |
| R02 | REJECT | No | B1:136; S | Correct localized color; optional removal to reduce Christmas-gift clustering with R07 and M01. |
| R03 | ACCEPT | Yes | B2:70; S | Scies musicales explicit; treat approximate instrument count as optional. |
| R04 | ACCEPT | Yes | B2:94; S | Grapes reported by McGonagall; do not require her inference about Colin’s planned visit. |
| R05 | ACCEPT | Yes | B3:135; S | Order plus Flitwick’s response identify recipient; distinct from adjacent Fudge order. |
| R06 | REJECT | No | B3:286; S | Correct number; shares the exact letter page and event with M05. Retain M05 for scene comparison. |
| R07 | ACCEPT | Yes | B4:225; S | Both color/motif pairs explicit; sufficiently different from M01’s flute despite Christmas setting. |
| R08 | REJECT | No | B4:236, B4:249; S/G | Correct password, but both pages independently suffice; flat recall imposes a redundant-page penalty. Keep as a reserve after evidence-model approval. |
| R09 | ACCEPT | Yes | B5:102; S | Code explicit for Arthur’s visit. B5 612 repeats the code for a different visit, useful as secondary fact evidence but not proof Arthur dialed it. |
| R10 | ACCEPT | Yes | B5:393; S | Ward name and purpose explicit; localized search found one ward-name page, not proof of exhaustive fact rarity. |
| R11 | ACCEPT | Yes | B6:119; S | Exactly the two spoken odors; do not infer the unfinished third odor. |
| R12 | ACCEPT | Yes | B7:98; S | Attraction method, donor and location explicit; answer length exceeds question needs, so method alone should suffice. |
| M01 | ACCEPT | Yes | B1:135, B1:184; S | Sound at first use and later practical use need distinct scenes; later flute mention does not state the initial owl-like sound. |
| M02 | EDIT | Yes, conditional | B1:164, B1:165, B1:205, B1:206; S/G | Supported arithmetic, but B1 164 is scene context, not necessarily a required page; B1 165 alone states the loss and B1 206 permits the award total. Annotate minimal bundles. |
| M03 | EDIT | Yes, conditional | B2:128, B2:129, B2:161; S/G | Supported; separate the accusation, Harry’s inference, and Ginny revelation into evidence needs. The final sentence on B2 161 also recalls the Hagrid capture, so retain detailed accusation wording. |
| M04 | ACCEPT | Yes | B2:42, B2:145; S | Distant scenes establish contrasting autonomous actions; both components needed. |
| M05 | EDIT | Yes, conditional | B3:154, B3:286; S/G | Supported; question leaves the letter’s revelation open-ended (sender, payment, delivery or apology). Specify which mystery the letter resolves. |
| M06 | ACCEPT | Yes | B3:214, B3:253; S | Prediction and actual escape mechanism need different scenes. B3 282 repeats prophecy but omits transformation/handcuff mechanism. |
| M07 | REJECT | No | B4:51, B4:338, B4:339, B4:356; S/G | Two genuine journeys, but four pages mix direct events, continuation, and recap. Answer adds a destination not requested. Drop rather than over-weight Portkey recaps. |
| M08 | EDIT | Yes, conditional | B4:200, B4:270, B4:273; S/G | Supported; B4 270 and 273 are alternative support for the underwater method. Group them under one need. |
| M09 | ACCEPT | Yes | B5:197, B5:318; S | Theory-only policy versus paired practice is a meaningful comparison of distant scenes; core contrast needs both. |
| M10 | ACCEPT | Yes | B5:322, B5:490, B5:510; S | Communication mechanism and penalty are distinct; third page attributes list enchantment to Hermione. Preserve separate claim needs. |
| M11 | EDIT | Yes, conditional | B6:162, B6:255, B6:376; S/G/X | Supported, but B6 374–375 names both victims in a continuous recap and B6 376 links both methods to Dumbledore. Distant scenes are not strictly necessary. Retain only with event-specific detail added and reverified. |
| M12 | REJECT | No | B7:362, B7:525; S | Both facts supported, but juxtaposition asks two largely independent sword facts without requiring a causal connection. Do not imply a documented transfer from Gripsec to Neville. |
| C01 | REJECT | No | B1:95, B6:255, B6:256; S/G/X | Correct facts, wrong strict cross-book claim: B6 PDF 242 repeats the first-lesson origin and antidote explanation. B6 242 + 255–256 suffice without book 1. |
| C02 | ACCEPT | Yes | B2:175, B4:209; S | Full liberation mechanism plus accepted wages/time off need separate evidence. B4 208 summarizes sock liberation but omits diary trick; do not count that as complete support. |
| C03 | EDIT | Yes, conditional | B1:141, B1:144, B7:500, B7:501; S/G | Supported identities; B1 141 and 144 are alternatives for parents, but only 141 explicitly describes the wider family. Split parents from wider family or use 141 as the full-family bundle. |
| C04 | ACCEPT | Yes | B5:684, B7:399, B7:400; S | School detention use comes from B5 note; later rescue attribution and Abelforth’s identity span B7 pages. Meaningful reuse across books. |
| C05 | ACCEPT | Yes | B5:95, B7:137; S | Inability to open medallion established in book 5; book 7 identifies recovery and theft. Event linkage is useful, though book 7 repeats disposal history. |
| C06 | EDIT | Yes, conditional | B1:11, B7:38; S/G/X | Supported lender/mechanic, but B7 38 already names Sirius’s motorcycle and recalls baby Harry. Require a detail unique to the original loan scene, or relabel as a historical comparison with a shortcut caveat. |
| C07 | ACCEPT | Yes | B3:249, B7:336; S | Moral motive in book 3 and hesitation/hand retaliation in book 7 support a causal connection; calling it voluntary rescue would overstate evidence. |
| C08 | REJECT | No | B6:336, B7:454; S/G/X | Correct facts, but B7 PDF 443 recalls placing the wig and diadem on a statue. With B7 454, book 6 is unnecessary for the requested answer; at least the main cross-book dependency collapses. |
| C09 | EDIT | Yes, conditional | B2:68, B2:69, B6:375, B6:376; S/G | Supported; B2 69 alone states Nick’s diversion and successful avoidance of detention, while 68 supplies preceding context. B6 375–376 establish passage and actual entry. Do not require every context page. |
| C10 | REJECT | No | B4:155, B4:200, B7:103, B7:104; S/G | Correct facts, but two independent biographical lookups, broad life-event scope and redundant pages; weak cross-book reasoning. Prefer causal or contrasting items. |
| P01 | ACCEPT | Yes | B1:144; S | Natural mirror synonym; explains temptation and limits rather than copying its formal definition. Word glace has a minor ambiguity resolved by family/reflection context. |
| P02 | ACCEPT | Yes | B2:154; S | Mechanism is paraphrased without naming Memory Charm in question; clear causal answer. |
| P03 | REJECT | No | B3:57, B3:58; S/G | Correct chocolate answer, but the second page is an alternative rather than a necessary continuation; simple synonym replacement gives limited paraphrase challenge. |
| P04 | ACCEPT | Yes | B4:383; S | Role-based question avoids Rita’s name and transformation vocabulary; reveal page supports mechanism and unregistered status. |
| P05 | ACCEPT | Yes | B5:313; S | Purpose-based question avoids room name; single passage explains adaptation and Dobby’s recommendation. |
| P06 | EDIT | Yes, conditional | B6:368, B6:369; S/G | Supported, but B6 369 alone states the fire protection and return to the boat. Page 368 is an alternative/expanded action scene, not automatically required. |
| U01 | ACCEPT | Yes | No gold pages; N | Tent dance not found; book 7 radio music at PDF 312 is a countercheck, not the alleged dance. Human confirmation still required. |
| U02 | REJECT | No | No gold pages; N | B6 4, 7–8 explicitly name Brockdale bridge. The London/film qualifier is too fragile: a reader can reasonably answer the novel event. Not a clean negative. |
| U03 | ACCEPT | Yes | No gold pages; N | B7 69 gives replacement Wilkins identities, not original given names; original names not found in examined parent references. |
| U04 | REJECT | No | No gold pages; N | No complete birthday found; tenure on B5 260 does not establish one. Plausible negative, but drop as an arbitrary exact-date demand; retain as a reserve if a fourth negative is wanted. |
| U05 | ACCEPT | Yes | No gold pages; N | Dobby’s pay (B4 209) and Slughorn’s salary remark (B6 308) do not establish headmaster pay; exact amount not found. |

## Proposed shortlist and distribution

Exactly **45**, conditional on the edits and evidence protocol approved below. No
reserve is automatically substituted if an edit fails human review.

| Category | Original | Proposed | IDs |
| --- | ---: | ---: | --- |
| `factual_simple` | 15 | 11 | F01, F03, F04, F06, F07, F08, F09, F10, F12, F13, F14 |
| `rare_detail` | 12 | 9 | R01, R03, R04, R05, R07, R09, R10, R11, R12 |
| `multi_passage` | 12 | 10 | M01, M02, M03, M04, M05, M06, M08, M09, M10, M11 |
| `cross_book` | 10 | 7 | C02, C03, C04, C05, C06, C07, C09 |
| `paraphrase` | 6 | 5 | P01, P02, P04, P05, P06 |
| `unanswerable` | 5 | 3 | U01, U03, U05 |

| Book | Original questions citing book | Proposed questions citing book |
| --- | ---: | ---: |
| 1 | 11 | 8 |
| 2 | 9 | 8 |
| 3 | 8 | 6 |
| 4 | 9 | 6 |
| 5 | 9 | 8 |
| 6 | 8 | 6 |
| 7 | 11 | 7 |

Book totals overlap for cross-book items and exclude negative questions; they are
question incidences, not equal sampling weights. The 42 answerable questions
span all seven books. Coverage follows the current references and remains
conditional on the EDIT items retaining their categories. The three negatives
have no gold book assignment: U01 targets book 7, U03 parent references across
books (especially 7), and U05 school employment facts across books (especially
4 and 6). They must not acquire invented relevant pages for coverage accounting.

## Evidence semantics and proposed representation

A **required need** is an answer component that must be evidenced. Different
needs are complementary (AND). An **alternative bundle** is one sufficient route
to support a need (OR). Pages within a bundle are complementary only when their
combined content is needed. A context page may identify a speaker or event
without being a separate answer need. “Required page” means present in every
sufficient bundle for that need, not merely adjacent to the event.

Keep `gold_pages` as the immutable provenance union of known support/context
references during this audit. Propose a separately reviewed sidecar, keyed by
stable question ID, with `needs`, each containing a French claim description and
`any_of` bundles of `{source, page}` references. Each bundle's `all_of` list must
be nonempty and sufficient for that claim. An optional `context_only` list records
helpful but non-scored pages; `evidence_complete: false` records remaining search
uncertainty. Sources remain exact basenames and page indices remain zero-based.
For a negative question use `needs: []` and separate countercheck references,
never turn counterchecks into gold relevance. This is a proposal, not a schema
migration or metric implementation.

Example for R08 (abbreviated **JSON indices**, book 4 source basename expanded
from corpus_manifest.json when implemented):

```text
need: password Cedric gives Harry
any_of:
  - all_of: [B4:235]
  - all_of: [B4:248]
```

For M08, require both needs: dragon diversion supported by B4 PDF 200; underwater
breathing supported by either B4 PDF 270 or 273. Do not require both alternative
water pages. For M10, communication on B5 PDF 322 and punishment/attribution on
490 plus 510 are complementary answer needs; a single hit cannot establish the
whole response. Attribute precisely which claim each page supports.

For later evaluation, retain the originally requested flat page Recall@k under
that exact name and definition for comparability, with explicit warnings. If the
owner approves a second measure, propose **evidence-need coverage**: a need is
covered only when the retrieved page set contains an entire sufficient bundle;
partial bundle coverage is not complete support. Report this separately, along
with all-needs coverage. Do not silently redefine Recall@k. Hit/MRR over the
union indicate some relevant evidence, not answer completeness. Page presence
still cannot prove that the retrieved chunk contains the supporting sentence.
No formulas have been executed and no metrics implemented in this audit.

### Page roles, shortcuts and corrections to approve

- **F09:** B4 PDF 265 directly supports delivery; 358 independently recounts
  Dobby fetching and bringing branchiflore. Add 358 as alternative support,
  without deleting 265. The later page is not required to identify the helper.
- **M02:** B1 PDF 164 locates the incident; 165 states the 150-point loss.
  B1 205 gives Ron's award, but 206 says the two first awards total 100 before
  adding 60 and 10. Thus `[165, 206]` is a sufficient numerical bundle; do not
  mechanically demand all four pages. The causal incident anchor can remain
  context. Human review must decide whether all four individual awards are
  required or merely explanatory additions in the reference answer.
- **M03:** B2 128 supplies the accusation, 129 Harry's conclusion, and 161 the
  manipulation revelation. A need for why he suspects Hagrid can use 128;
  129 corroborates the conclusion. B2 161 also mentions showing Hagrid's capture,
  but does not reproduce the detailed accusation. Preserve that detailed need
  in the wording if this is to remain a distant-scene question.
- **M05:** proposed French wording: *Pourquoi l'Éclair de Feu reçu par Harry
  est-il confisqué, et qui la lettre finale révèle-t-elle comme son donateur ?*
  B3 154 and 286 support the two needs. The “not a trap” interpretation is
  supported by Ron's dialogue on 286, not a literal assertion in Sirius's letter.
  Keep the gift fact; make clear to a future judge that other letter facts are
  not compulsory. No wording change applied to JSONL.
- **M06:** B3 282 is an additional alternative for the prophecy, discovered
  during recap checks. It does not give the exact escape mechanism, which
  remains on 253. Record `[[214], [282]]` for prophecy, `[[253]]` for escape
  (physical pages). Existing evidence is supported but incomplete.
- **M07 (excluded):** B4 51 supports boot; 338 taking trophy, 339 arrival and
  Portkey identification; 356 recaps the latter. For the question's two objects,
  339 alone supports trophy identification, with 356 an alternative. The
  destination belongs to the answer but is not explicitly requested.
- **M08:** use the two-need grouping above; underwater pages are alternatives.
- **M11:** B6 374 ends by naming Katie and Ronald; 375 continues the sentence
  and intended murder accusation, and 376 explicitly names both methods. This
  nearby recap weakens the distant-scene label. Proposed wording adds a detail
  from each event: *Qu'arrive-t-il physiquement à Katie quand elle touche le
  collier et à Ron après l'hydromel, et qui ces deux attaques visaient-elles ?*
  B6 162 describes Katie rising, screaming and falling; 255 describes Ron's
  collapse and convulsions; 376 identifies Dumbledore. Proposed gold addition:
  *Katie s'élève dans les airs, hurle puis retombe ; Ron s'effondre en convulsant
  après avoir bu l'hydromel. Les deux attaques visaient Dumbledore.* Reopen those
  pages together before approving this edit; the original wording stays intact.
- **C01 (excluded):** add B6 242 as an alternative explanation if retained as
  a reserve. It explicitly recalls Rogue's first lesson, including goat origin.
  Do not label the item intrinsically cross-book merely because the annotator
  chose to cite book 1. Would need relabeling or a redesigned dependency.
- **C02:** B4 208 is a recap of sock liberation, but does not give the diary
  enclosure. It can support a coarse freedom claim, not the complete mechanism
  required by the current answer. B2 175 remains necessary for that detail;
  B4 209 supplies accepted wages/time off and the more generous rejected offer.
- **C03:** B1 144 suffices for parents, but the full extended-family description
  is on 141. These are not equivalent bundles for every word of the gold answer.
  Propose asking explicitly for parents versus the four named appearances and
  dropping the extended-family requirement, or keep 141 as the full-family
  bundle and 144 as partial support. B7 500–501 complement each other for all
  four identities. Choose one policy before validation; do not delete evidence.
- **C04:** B5 684 supports detention communication; B7 399 establishes sending
  Dobby while 400 identifies Abelforth and provenance of his mirror. These are
  complementary, unlike R08's alternative single pages.
- **C06:** B7 38 names Sirius's bike and recalls infant Harry, so an ownership
  question would collapse to one page. Propose making the original scene's
  precise role explicit: *Qui dit avoir emprunté la moto pour amener Harry bébé,
  à qui l'a-t-il empruntée, et qui la modifie avant le dernier départ de Privet
  Drive ?* Proposed gold: *Hagrid explique l'avoir empruntée à Sirius Black.
  Arthur Weasley la modifie avant le dernier départ de Harry.* B1 11 supports
  the explicit loan report; B7 38 supports later work. Still a comparison of
  events, not proof that every possible answer route spans books.
- **C08 (excluded):** B7 443 repeats placing wig/diadem on the statue; it does
  not repeat every cupboard/book detail. The main requested earlier use can
  nevertheless be inferred there without book 6. Retain book 6 provenance,
  but do not claim the original question tests a necessary cross-book route.
- **C09:** B2 69 directly states Nick's diversion and Harry's lack of detention;
  68 provides incident context and identifies the cabinet type. B6 375 explains
  paired-cabinet repair and 376 confirms actual entry. Review minimal bundles
  claim by claim rather than requiring all context pages. No unsupported claim
  that the two book events explicitly establish the same physical cabinet.
- **C10 (excluded):** B4 155 and 200 alternatively establish school. B7 103–104
  span vows and marriage declaration. Joint lookup is factually sound, but
  weaker synthesis than the retained causal/contrast questions.
- **P03 (excluded):** B3 57 offers chocolate; 58 consumes it and discusses its
  effect. For identification of the food either page can suffice.
- **P06:** B6 369 is sufficient for protection through embarkation; 368 depicts
  the initial rescue. Treat 369 as a sufficient bundle, and 368 as support for
  the narrower repulsion claim, not an independently mandatory page.

The ACCEPT items also require normal human checks. In particular, R12's method
question should not require the optional donor location; F13's “seven parts”
should not be scored as seven intentional Horcruxes; F04 is about young plants;
R11's omitted third odor must remain omitted. These are judge-rubric clarifications,
not demonstrable errors warranting changes to the candidate records.

## Unanswerable audit and lexical leakage

U01, U03 and U05 are the proposed negatives. A correct abstention need not prove
corpus-wide absence: distinguish “not in the supplied context” from “never occurs
in the novels.” The reference answers assert broader absence and therefore need
human confirmation before validation. U01 is a false scene premise; U03 and U05
are missing specifications. Three items provide little statistical power and
are not a complete adversarial negative taxonomy.

Rechecked B7 69 (replacement parent names), B7 312 (a song briefly heard while
Ron seeks a radio program), B5 260 (McGonagall teaching tenure), and salary
counterchecks from REVIEW.md. U02 is rejected because its bridge premise is
close to a named novel event; U04 is a reserve, not a claim that a birthday was
found. No film title, song name, or external biography was used as gold evidence.

Most factual items contain natural entity anchors. F01's binary contrast is the
strongest wording cue: propose *Quelle plante Rogue désigne-t-il lorsqu'il parle
du tue-loup pendant son premier cours ?* with the existing aconite answer
accepted. This edit must be human-approved. Names such as Amortentia, a specific
exam, or a tournament task do not disclose the requested odor, fear or method.
The five retained paraphrase items avoid key answer terms, but are editorial
judgments rather than measured lexical-distance guarantees. No embeddings,
retrieval-based difficulty selection, or overlap threshold was used.

## Human decisions required before Phase 2

1. Approve/edit/reject each recommendation, especially the 11 conditional EDIT
   items. Decide whether revised M11 and C06 meet the intended reasoning labels.
   If either fails, select an explicitly reviewed reserve or accept fewer than
   45 rather than relabeling it silently.
2. Approve the evidence-need sidecar proposal, full/partial support distinctions,
   and whether to report an additional measure alongside unchanged flat page
   recall. Complete alternative-evidence searches for retained items before
   freezing references; the sidecar has not been created.
3. Confirm novel-only absence for U01/U03/U05 and decide whether three negatives
   are enough. Restoring U04 would produce 46; it needs explicit approval.
4. Check French naturalness, fact-level rarity, and whether the shortlist reduces
   related-event dependence sufficiently. F01/C01 and R06/M05 clustering is reduced
   by exclusions; related scenes still remain (e.g. M11 and other book-6 potions
   items). Do not infer independence from different IDs.
5. Record human reviewer identity/date and approved final IDs in REVIEW.md only
   after review. No human cells have been filled by this audit. Any later JSONL
   edits should preserve IDs and log old/new values; only explicit approval may
   change statuses to `validated`.

## Checks and methodological limits

Actually performed: UTF-8 JSONL parsing; exact schema, unique IDs/questions,
category counts, all-candidate status, page bounds, no duplicate page pairs,
source-basename membership; seven PDF SHA-256 checks; independent reopening of
all existing gold pages and targeted extra pages; 60-row recommendation coverage,
45-item membership/counts and book-incidence consistency; unchanged dataset hash
against phase-1 Git content; review-link existence; Git ignore checks for local
copyright artifacts; staged whitespace and changed-file inspection before commit.
Checks use Python standard library, Poppler and Git. No RAG or evaluation module
was imported or executed.

The existing judge returns a global model-estimated faithfulness score and a
relevance score, not explicit supported-claim counts or gold-answer correctness;
errors are encoded as zero. It cannot establish these labels. The classical
experimental evaluator's empty manual sets and index-derived fallback labels
are not independent semantic relevance judgments. Neither evaluator was run.

This remains a small, author-selected AI-drafted dataset audited by the same AI
assistant, with familiar-scene and event-cluster bias. Rarity is not exhaustively
counted and negatives are not proved absent by search. Later recalls may compress
multi-scene questions into nearby passages. Page relevance can reward a wrong
chunk on a right page and differs between editions. Multiple questions share
characters, motifs and sometimes pages; future question-level intervals will not
remove those dependencies or annotation uncertainty. No performance claim,
confidence interval, model output, or automated judge verdict exists here.

## Change log and stop point

Only `eval/SHORTLIST.md` and a navigation link in `eval/README.md` change.
`questions.jsonl`, REVIEW.md, corpus_manifest.json, the app and all pipeline
parameters are unchanged. Recommended edits are intentionally reviewable here,
not automatically applied to the candidate dataset. Existing evidence is preserved,
including excluded candidates. The complete proposed cohort is the category table
above; recommendations are not human validation.

**STOP: Phase 1 audit only. Explicit human approval is required before Phase 2.**
