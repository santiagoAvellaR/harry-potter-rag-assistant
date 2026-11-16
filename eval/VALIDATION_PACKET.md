# Phase 1b human validation packet

Audit baseline: `4c63bc9`. **45 proposed questions, zero validated.**
All 60 candidates remain in questions.jsonl with stable IDs; this packet and the
sidecar explicitly identify the proposed cohort. Excluded items remain available
for review, not silently removed or accepted. SHORTLIST.md is the historical
audit; this packet supersedes its proposed wording and pending implementation
statements. No benchmark or LLM execution has occurred.

The repository owner authorized preparation, not human acceptance. Codex drafted
and audited these annotations. A human must verify the French wording, answers,
page roles and category labels, and approve the selected IDs before Phase 2.
No reviewer name or date is inferred. All decisions below are blank deliberately.

Dataset SHA-256: `6ab5e2ec21b5d0ea9b7ad80b0441149f7e3835cf34a1c2959f1ece88fa4532ea`.

## How to review evidence

Each link gives the physical PDF viewer page starting at one and the JSON index
starting at zero. Sources are exact basenames in corpus_manifest.json. Links need
the seven local PDFs; none are published. No novel passages are included here.

All listed needs are required answer components and complement each other (AND).
Within a need, routes are alternatives (OR); within each route, pages are jointly
required (AND). A page shared by all routes of a need is mandatory for that need
under the known annotations. This is an annotation claim, not proof that no other
support exists. Context-only pages help identify a scene but do not supply a
separate required answer component. Counterchecks for negatives are never gold
relevance. Every annotation has `evidence_complete: false` and pending human
review: targeted reading cannot certify exhaustive alternative support.

**Flat Recall@k remains unchanged:** the fraction of the existing gold_pages
covered in top-k, deduplicating page pairs, will retain that definition. The
sidecar does not replace, prune, or redefine gold_pages. Supplemental routes
(F09 PDF 358 and M06 PDF 282) are visible in the sidecar but absent from the
unchanged historical flat lists. A correct answer found only there can still be
a flat-metric miss. Context-only historical pages remain in the flat denominator.
The human reviewer must approve this comparability policy or explicitly amend
and freeze the flat labels before any run. No metric implementation is included.
A future evidence-need measure would be separate and requires explicit approval.
Page presence cannot guarantee that a retrieved chunk includes the actual support.

## Cohort distribution

| Category | Proposed | IDs |
| --- | ---: | --- |
| `factual_simple` | 11 | F01, F03, F04, F06, F07, F08, F09, F10, F12, F13, F14 |
| `rare_detail` | 9 | R01, R03, R04, R05, R07, R09, R10, R11, R12 |
| `multi_passage` | 10 | M01, M02, M03, M04, M05, M06, M08, M09, M10, M11 |
| `cross_book` | 7 | C02, C03, C04, C05, C06, C07, C09 |
| `paraphrase` | 5 | P01, P02, P04, P05, P06 |
| `unanswerable` | 3 | U01, U03, U05 |

| Book | Proposed answerable questions citing book |
| --- | ---: |
| 1 | 8 |
| 2 | 8 |
| 3 | 6 |
| 4 | 6 |
| 5 | 8 |
| 6 | 6 |
| 7 | 7 |

Book counts overlap across cross-book items; negatives have no gold book.
Excluded IDs: F02, F05, F11, F15, R02, R06, R08, M07, M12, C01, C08, C10, P03, U02, U04.
U04 stays excluded: the B5 PDF 260 tenure statement and targeted birthday searches
are insufficient to establish absence throughout the novels. No 46th item was
added just to meet a count. U01, U03 and U05 remain provisional negatives requiring
human confirmation, with their distinct confounders visible below.

## Changes applied relative to the audit baseline

All original gold_pages, IDs, categories and statuses are preserved. Only the
11 audited EDIT records changed, in the fields recorded verbatim as before/after
values in [phase1b_changes.json](phase1b_changes.json). Interpret that log together
with the reasons and evidence below. The other 49 parsed records are unchanged. For grouping-only corrections, French wording remains unchanged.

| ID | Applied correction | Evidence checked (physical pages) |
| --- | --- | --- |
| F01 | Open question and direct plant answer replace leading binary contrast. | B1 95 |
| F09 | Required answer limited to helper and plant; alternative recap annotated. | B4 265, 358 |
| M02 | Gold now contains requested totals only; individual awards optional; scene and Ron award page context-only. | B1 164–165, 205–206 |
| M03 | Explicit detailed accusation replaces vague reason for suspicion; inference page becomes context. | B2 128–129, 161 |
| M05 | Letter question explicitly asks donor; gold no longer attributes Ron's reassurance to the letter. | B3 154, 286 |
| M08 | Separate dragon need and water need; two water pages become alternatives. | B4 200, 270, 273 |
| M11 | Ask physical effects on Katie and Ron plus intended target; update gold to prevent nearby name recap shortcut. | B6 162, 255, 374–376 |
| C03 | Ask parents and four stone appearances; remove extended-family requirement and distinguish alternatives from page continuation. | B1 141, 144; B7 500–501 |
| C06 | Explicit loan reporter and lender added; gold states Hagrid's report. | B1 11; B7 38 |
| C09 | Early cabinet scene is context; diversion need and later paired-cabinet mechanism separated. | B2 68–69; B6 375–376 |
| P06 | Fire repulsion and protection to boat distinguished; PDF 369 suffices for both, 368 for repulsion only. | B6 368–369 |

M06's unchanged question also receives the already-audited prophecy alternative
B3 PDF 282 in the new sidecar. R03's approximate instrument count and R12's donor
location are optional elaborations, not additional answer requirements.

## Pending global human decisions

- Approve the 45 IDs or specify removals/reserve additions; approve the 11 edits.
- Approve every support bundle and context-only classification. Confirm M11
  now requires distant physical-effect descriptions. Confirm C06's explicit loan
  report justifies its cross-book label despite ownership inferable in book 7.
- Confirm M03 cannot be fully answered by its late recap alone. Other unlocated
  recaps remain possible for all scene comparisons.
- Confirm novel-only unanswerability of U01/U03/U05. A model may abstain because
  the retrieved context lacks an answer; it need not prove whole-corpus absence.
- Approve retaining historical flat labels, with their redundancy/context bias,
  versus a documented pre-run label revision. Decide separately on future
  evidence-need coverage; no change to flat Recall is implied by this sidecar.
- Check naturalness, category balance, rarity and remaining event dependence.
  This small, editorially selected sample is not representative of user traffic.

Reviewer: ____________________  Review date: ____________________

Approved IDs / conditions: ____________________

## Question-by-question review

### F01 — factual_simple

**Question:** Quelle plante Rogue désigne-t-il lorsqu'il parle du tue-loup pendant son premier cours ?

**Reference answer:** Il s'agit de l'aconit, également appelé napel.

**Historical flat gold_pages:** [B1 PDF 95 / JSON 94](../data/input/harry-potter-1-lecole-des-sorciers.pdf#page=95)

**Required need 1:** Il s'agit de l'aconit, également appelé napel.

- Route 1 (all listed pages together): [B1 PDF 95 / JSON 94](../data/input/harry-potter-1-lecole-des-sorciers.pdf#page=95)

**Context-only:** None

**Negative counterchecks:** None

**Annotation note:** Sufficient support checked locally; exhaustive alternative search and human validation pending.

**Scope note:** Phase 1b: neutral open question replaces a leading yes/no contrast; PDF 95 explicitly identifies both plant names.

**Human decision (accept / edit / reject):** ____________________

**Human evidence/category corrections:** ____________________

### F03 — factual_simple

**Question:** Quels sont les deux pouvoirs de la Pierre philosophale que découvre Hermione dans sa lecture ?

**Reference answer:** Elle peut changer les métaux en or et produire un élixir qui permet de prolonger la vie indéfiniment.

**Historical flat gold_pages:** [B1 PDF 149 / JSON 148](../data/input/harry-potter-1-lecole-des-sorciers.pdf#page=149)

**Required need 1:** Elle peut changer les métaux en or et produire un élixir qui permet de prolonger la vie indéfiniment.

- Route 1 (all listed pages together): [B1 PDF 149 / JSON 148](../data/input/harry-potter-1-lecole-des-sorciers.pdf#page=149)

**Context-only:** None

**Negative counterchecks:** None

**Annotation note:** Sufficient support checked locally; exhaustive alternative search and human validation pending.

**Scope note:** Both properties occur in the same passage; do not require the original wording.

**Human decision (accept / edit / reject):** ____________________

**Human evidence/category corrections:** ____________________

### F04 — factual_simple

**Question:** Pourquoi les élèves doivent-ils se protéger les oreilles en rempotant les jeunes mandragores ?

**Reference answer:** Leurs cris peuvent les assommer pendant plusieurs heures. À cet âge, les plantes ne tuent pas encore par leur cri.

**Historical flat gold_pages:** [B2 PDF 51 / JSON 50](../data/input/harry-potter-2-la-chambre-des-secrets.pdf#page=51)

**Required need 1:** Leurs cris peuvent les assommer pendant plusieurs heures. À cet âge, les plantes ne tuent pas encore par leur cri.

- Route 1 (all listed pages together): [B2 PDF 51 / JSON 50](../data/input/harry-potter-2-la-chambre-des-secrets.pdf#page=51)

**Context-only:** None

**Negative counterchecks:** None

**Annotation note:** Sufficient support checked locally; exhaustive alternative search and human validation pending.

**Scope note:** Distinguish young plants from the lethal cry of mature mandrakes.

**Human decision (accept / edit / reject):** ____________________

**Human evidence/category corrections:** ____________________

### F06 — factual_simple

**Question:** Sous quelle identité Harry se présente-t-il lorsqu'il monte dans le Magicobus après sa fugue ?

**Reference answer:** Il emprunte le nom de Neville Londubat pour ne pas être reconnu.

**Historical flat gold_pages:** [B3 PDF 24 / JSON 23](../data/input/harry-potter-3-le-prisonnier-dazkaban.pdf#page=24)

**Required need 1:** Il emprunte le nom de Neville Londubat pour ne pas être reconnu.

- Route 1 (all listed pages together): [B3 PDF 24 / JSON 23](../data/input/harry-potter-3-le-prisonnier-dazkaban.pdf#page=24)

**Context-only:** None

**Negative counterchecks:** None

**Annotation note:** Sufficient support checked locally; exhaustive alternative search and human validation pending.

**Scope note:** Scope: first Magicobus journey, not the later wedding disguise.

**Human decision (accept / edit / reject):** ____________________

**Human evidence/category corrections:** ____________________

### F07 — factual_simple

**Question:** Que voit Hermione face à l'épouvantard pendant l'examen pratique de Lupin ?

**Reference answer:** Elle voit le professeur McGonagall lui annoncer qu'elle a échoué à tout.

**Historical flat gold_pages:** [B3 PDF 210 / JSON 209](../data/input/harry-potter-3-le-prisonnier-dazkaban.pdf#page=210)

**Required need 1:** Elle voit le professeur McGonagall lui annoncer qu'elle a échoué à tout.

- Route 1 (all listed pages together): [B3 PDF 210 / JSON 209](../data/input/harry-potter-3-le-prisonnier-dazkaban.pdf#page=210)

**Context-only:** None

**Negative counterchecks:** None

**Annotation note:** Sufficient support checked locally; exhaustive alternative search and human validation pending.

**Scope note:** The exam scene explicitly identifies both the apparition and its message.

**Human decision (accept / edit / reject):** ____________________

**Human evidence/category corrections:** ____________________

### F08 — factual_simple

**Question:** Quel dragon Harry tire-t-il au sort pour la première épreuve du Tournoi, et dans quel ordre doit-il passer ?

**Reference answer:** Il tire le Magyar à pointes et doit passer en quatrième position.

**Historical flat gold_pages:** [B4 PDF 195 / JSON 194](../data/input/harry-potter-4-la-coupe-de-feu.pdf#page=195)

**Required need 1:** Il tire le Magyar à pointes et doit passer en quatrième position.

- Route 1 (all listed pages together): [B4 PDF 195 / JSON 194](../data/input/harry-potter-4-la-coupe-de-feu.pdf#page=195)

**Context-only:** None

**Negative counterchecks:** None

**Annotation note:** Sufficient support checked locally; exhaustive alternative search and human validation pending.

**Scope note:** Draw scene; both requested facts are on one page.

**Human decision (accept / edit / reject):** ____________________

**Human evidence/category corrections:** ____________________

### F09 — factual_simple

**Question:** Qui apporte à Harry de quoi respirer sous l'eau juste avant la deuxième épreuve, et que lui donne-t-il ?

**Reference answer:** Dobby lui apporte de la branchiflore pour lui permettre de respirer sous l'eau.

**Historical flat gold_pages:** [B4 PDF 265 / JSON 264](../data/input/harry-potter-4-la-coupe-de-feu.pdf#page=265)

**Required need 1:** Dobby apporte la branchiflore.

- Route 1 (all listed pages together): [B4 PDF 265 / JSON 264](../data/input/harry-potter-4-la-coupe-de-feu.pdf#page=265)
- Route 2 (all listed pages together): [B4 PDF 358 / JSON 357](../data/input/harry-potter-4-la-coupe-de-feu.pdf#page=358)

**Context-only:** None

**Negative counterchecks:** None

**Annotation note:** Sufficient support checked locally; exhaustive alternative search and human validation pending.

**Scope note:** Phase 1b: PDF 265 directly supports helper and plant; PDF 358 supplies an alternative recap in evidence_annotations.json. Eating instruction is not required by this question. Original flat gold_pages preserved.

**Human decision (accept / edit / reject):** ____________________

**Human evidence/category corrections:** ____________________

### F10 — factual_simple

**Question:** Que fait la plume d'Ombrage à Harry pendant ses retenues ?

**Reference answer:** Elle écrit avec le sang de Harry et grave en même temps les mots au dos de sa main. La plaie se referme puis se rouvre lorsqu'il recommence.

**Historical flat gold_pages:** [B5 PDF 216 / JSON 215](../data/input/harry-potter-5-lordre-du-phoenix.pdf#page=216)

**Required need 1:** Elle écrit avec le sang de Harry et grave en même temps les mots au dos de sa main. La plaie se referme puis se rouvre lorsqu'il recommence.

- Route 1 (all listed pages together): [B5 PDF 216 / JSON 215](../data/input/harry-potter-5-lordre-du-phoenix.pdf#page=216)

**Context-only:** None

**Negative counterchecks:** None

**Annotation note:** Sufficient support checked locally; exhaustive alternative search and human validation pending.

**Scope note:** The repeated action is fully described on this page; the preceding page starts the scene.

**Human decision (accept / edit / reject):** ____________________

**Human evidence/category corrections:** ____________________

### F12 — factual_simple

**Question:** Que promet Slughorn à l'élève qui réussira le mieux le philtre de Mort Vivante lors de son premier cours ?

**Reference answer:** Il promet un petit flacon de Félix Felicis, contenant de quoi bénéficier de douze heures de chance.

**Historical flat gold_pages:** [B6 PDF 121 / JSON 120](../data/input/harry-potter-6-le-prince-de-sang-mecc82lecc81.pdf#page=121)

**Required need 1:** Il promet un petit flacon de Félix Felicis, contenant de quoi bénéficier de douze heures de chance.

- Route 1 (all listed pages together): [B6 PDF 121 / JSON 120](../data/input/harry-potter-6-le-prince-de-sang-mecc82lecc81.pdf#page=121)

**Context-only:** None

**Negative counterchecks:** None

**Annotation note:** Sufficient support checked locally; exhaustive alternative search and human validation pending.

**Scope note:** Reward and duration are both explicit; not a question about who eventually wins.

**Human decision (accept / edit / reject):** ____________________

**Human evidence/category corrections:** ____________________

### F13 — factual_simple

**Question:** Dans le véritable souvenir de Slughorn, en combien de parties Jedusor envisage-t-il de diviser son âme ?

**Reference answer:** Il envisage sept parties, car il attribue une puissance magique particulière au nombre sept.

**Historical flat gold_pages:** [B6 PDF 319 / JSON 318](../data/input/harry-potter-6-le-prince-de-sang-mecc82lecc81.pdf#page=319)

**Required need 1:** Il envisage sept parties, car il attribue une puissance magique particulière au nombre sept.

- Route 1 (all listed pages together): [B6 PDF 319 / JSON 318](../data/input/harry-potter-6-le-prince-de-sang-mecc82lecc81.pdf#page=319)

**Context-only:** None

**Negative counterchecks:** None

**Annotation note:** Sufficient support checked locally; exhaustive alternative search and human validation pending.

**Scope note:** Seven soul fragments must not be confused with seven intentionally created Horcruxes.

**Human decision (accept / edit / reject):** ____________________

**Human evidence/category corrections:** ____________________

### F14 — factual_simple

**Question:** Par quel objet Ron entend-il Hermione prononcer son nom après avoir quitté ses amis ?

**Reference answer:** Il entend sa voix à travers le Déluminateur qu'il garde dans sa poche.

**Historical flat gold_pages:** [B7 PDF 273 / JSON 272](../data/input/harry-potter-7-les-reliques-de-la-mort.pdf#page=273)

**Required need 1:** Il entend sa voix à travers le Déluminateur qu'il garde dans sa poche.

- Route 1 (all listed pages together): [B7 PDF 273 / JSON 272](../data/input/harry-potter-7-les-reliques-de-la-mort.pdf#page=273)

**Context-only:** None

**Negative counterchecks:** None

**Annotation note:** Sufficient support checked locally; exhaustive alternative search and human validation pending.

**Scope note:** Only identify the object and the voice; the following page is needed for a full account of the return, which is not asked here.

**Human decision (accept / edit / reject):** ____________________

**Human evidence/category corrections:** ____________________

### R01 — rare_detail

**Question:** Quelle glace Hagrid offre-t-il à Harry pendant leurs premiers achats sur le chemin de Traverse ?

**Reference answer:** C'est une glace au chocolat et à la fraise, avec des noisettes.

**Historical flat gold_pages:** [B1 PDF 54 / JSON 53](../data/input/harry-potter-1-lecole-des-sorciers.pdf#page=54)

**Required need 1:** C'est une glace au chocolat et à la fraise, avec des noisettes.

- Route 1 (all listed pages together): [B1 PDF 54 / JSON 53](../data/input/harry-potter-1-lecole-des-sorciers.pdf#page=54)

**Context-only:** None

**Negative counterchecks:** None

**Annotation note:** Sufficient support checked locally; exhaustive alternative search and human validation pending.

**Scope note:** Localized food detail; review rarity at the fact level, not occurrences of the word ice cream.

**Human decision (accept / edit / reject):** ____________________

**Human evidence/category corrections:** ____________________

### R03 — rare_detail

**Question:** Quels instruments accompagnent la danse des fantômes à la fête de Nick Quasi-Sans-Tête ?

**Reference answer:** Les musiciens jouent d'une trentaine de scies musicales.

**Historical flat gold_pages:** [B2 PDF 70 / JSON 69](../data/input/harry-potter-2-la-chambre-des-secrets.pdf#page=70)

**Required need 1:** Les musiciens jouent d'une trentaine de scies musicales.

- Route 1 (all listed pages together): [B2 PDF 70 / JSON 69](../data/input/harry-potter-2-la-chambre-des-secrets.pdf#page=70)

**Context-only:** None

**Negative counterchecks:** None

**Annotation note:** Approximate instrument count is optional; musical saws is the required identification.

**Scope note:** Localized party detail; the approximate number is optional for correctness.

**Human decision (accept / edit / reject):** ____________________

**Human evidence/category corrections:** ____________________

### R04 — rare_detail

**Question:** Quel fruit retrouve-t-on près de Colin Crivey après sa pétrification ?

**Reference answer:** On retrouve une grappe de raisins près de lui.

**Historical flat gold_pages:** [B2 PDF 94 / JSON 93](../data/input/harry-potter-2-la-chambre-des-secrets.pdf#page=94)

**Required need 1:** On retrouve une grappe de raisins près de lui.

- Route 1 (all listed pages together): [B2 PDF 94 / JSON 93](../data/input/harry-potter-2-la-chambre-des-secrets.pdf#page=94)

**Context-only:** None

**Negative counterchecks:** None

**Annotation note:** Sufficient support checked locally; exhaustive alternative search and human validation pending.

**Scope note:** McGonagall reports the fruit; her inference about his intended visit is not part of the answer.

**Human decision (accept / edit / reject):** ____________________

**Human evidence/category corrections:** ____________________

### R05 — rare_detail

**Question:** Quelle boisson Rosmerta sert-elle à Flitwick lors de la conversation que Harry écoute caché aux Trois Balais ?

**Reference answer:** Elle lui sert un soda au sirop de cerise, accompagné d'une boule de glace et d'une ombrelle.

**Historical flat gold_pages:** [B3 PDF 135 / JSON 134](../data/input/harry-potter-3-le-prisonnier-dazkaban.pdf#page=135)

**Required need 1:** Elle lui sert un soda au sirop de cerise, accompagné d'une boule de glace et d'une ombrelle.

- Route 1 (all listed pages together): [B3 PDF 135 / JSON 134](../data/input/harry-potter-3-le-prisonnier-dazkaban.pdf#page=135)

**Context-only:** None

**Negative counterchecks:** None

**Annotation note:** Sufficient support checked locally; exhaustive alternative search and human validation pending.

**Scope note:** The reply identifies Flitwick as the recipient; not Fudge's adjacent order.

**Human decision (accept / edit / reject):** ____________________

**Human evidence/category corrections:** ____________________

### R07 — rare_detail

**Question:** Comment reconnaître les deux chaussettes que Dobby tricote pour Harry à Noël, l'année du Tournoi ?

**Reference answer:** L'une est rouge et décorée de balais volants ; l'autre est verte et porte des motifs de Vifs d'or.

**Historical flat gold_pages:** [B4 PDF 225 / JSON 224](../data/input/harry-potter-4-la-coupe-de-feu.pdf#page=225)

**Required need 1:** L'une est rouge et décorée de balais volants ; l'autre est verte et porte des motifs de Vifs d'or.

- Route 1 (all listed pages together): [B4 PDF 225 / JSON 224](../data/input/harry-potter-4-la-coupe-de-feu.pdf#page=225)

**Context-only:** None

**Negative counterchecks:** None

**Annotation note:** Sufficient support checked locally; exhaustive alternative search and human validation pending.

**Scope note:** Both colors and motifs are needed; distinguish this gift from Harry's and Ron's gifts to Dobby.

**Human decision (accept / edit / reject):** ____________________

**Human evidence/category corrections:** ____________________

### R09 — rare_detail

**Question:** Quel numéro Arthur Weasley compose-t-il dans la cabine téléphonique pour entrer au ministère avec Harry ?

**Reference answer:** Il compose le 62442.

**Historical flat gold_pages:** [B5 PDF 102 / JSON 101](../data/input/harry-potter-5-lordre-du-phoenix.pdf#page=102)

**Required need 1:** Il compose le 62442.

- Route 1 (all listed pages together): [B5 PDF 102 / JSON 101](../data/input/harry-potter-5-lordre-du-phoenix.pdf#page=102)

**Context-only:** None

**Negative counterchecks:** None

**Annotation note:** Sufficient support checked locally; exhaustive alternative search and human validation pending.

**Scope note:** Scope: Arthur's visit with Harry; the later visit led by Harry is outside the question's event scope.

**Human decision (accept / edit / reject):** ____________________

**Human evidence/category corrections:** ____________________

### R10 — rare_detail

**Question:** Dans quelle salle de Sainte-Mangouste Arthur Weasley est-il hospitalisé après l'attaque du serpent ?

**Reference answer:** Il est dans la salle Dai Llewellyn, réservée aux morsures graves.

**Historical flat gold_pages:** [B5 PDF 393 / JSON 392](../data/input/harry-potter-5-lordre-du-phoenix.pdf#page=393)

**Required need 1:** Il est dans la salle Dai Llewellyn, réservée aux morsures graves.

- Route 1 (all listed pages together): [B5 PDF 393 / JSON 392](../data/input/harry-potter-5-lordre-du-phoenix.pdf#page=393)

**Context-only:** None

**Negative counterchecks:** None

**Annotation note:** Sufficient support checked locally; exhaustive alternative search and human validation pending.

**Scope note:** Literal search for the ward name found one page in book 5. This page contains both the reception directions and the sign on the door; fact-level rarity remains subject to review.

**Human decision (accept / edit / reject):** ____________________

**Human evidence/category corrections:** ____________________

### R11 — rare_detail

**Question:** Quelles sont les deux odeurs qu'Hermione nomme avant de s'interrompre en parlant de l'Amortentia ?

**Reference answer:** Elle cite l'herbe fraîchement coupée et le parchemin neuf.

**Historical flat gold_pages:** [B6 PDF 119 / JSON 118](../data/input/harry-potter-6-le-prince-de-sang-mecc82lecc81.pdf#page=119)

**Required need 1:** Elle cite l'herbe fraîchement coupée et le parchemin neuf.

- Route 1 (all listed pages together): [B6 PDF 119 / JSON 118](../data/input/harry-potter-6-le-prince-de-sang-mecc82lecc81.pdf#page=119)

**Context-only:** None

**Negative counterchecks:** None

**Annotation note:** Sufficient support checked locally; exhaustive alternative search and human validation pending.

**Scope note:** Only the two odors she actually names; do not fill the unfinished third item from films or other sources.

**Human decision (accept / edit / reject):** ____________________

**Human evidence/category corrections:** ____________________

### R12 — rare_detail

**Question:** Comment Fred se procure-t-il les cheveux utilisés pour déguiser Harry au mariage ?

**Reference answer:** Il prend par un sortilège d'Attraction quelques cheveux d'un jeune Moldu roux qui habite le village voisin de Loutry Ste Chaspoule.

**Historical flat gold_pages:** [B7 PDF 98 / JSON 97](../data/input/harry-potter-7-les-reliques-de-la-mort.pdf#page=98)

**Required need 1:** Fred se procure les cheveux avec un sortilège d'Attraction.

- Route 1 (all listed pages together): [B7 PDF 98 / JSON 97](../data/input/harry-potter-7-les-reliques-de-la-mort.pdf#page=98)

**Context-only:** None

**Negative counterchecks:** None

**Annotation note:** Donor description and village in the gold answer are optional elaboration; method is required.

**Scope note:** Localized preparation detail; the repeated alias Barny is deliberately not the target fact.

**Human decision (accept / edit / reject):** ____________________

**Human evidence/category corrections:** ____________________

### M01 — multi_passage

**Question:** Quel son produit le cadeau de Hagrid lorsque Harry l'essaie à son premier Noël, et à quoi lui sert-il lorsqu'il retourne auprès de Touffu ?

**Reference answer:** La flûte en bois produit un son qui évoque un hibou. Harry en joue plus tard pour endormir Touffu et permettre l'accès à la trappe.

**Historical flat gold_pages:** [B1 PDF 135 / JSON 134](../data/input/harry-potter-1-lecole-des-sorciers.pdf#page=135); [B1 PDF 184 / JSON 183](../data/input/harry-potter-1-lecole-des-sorciers.pdf#page=184)

**Required need 1:** Le premier essai de la flûte évoque le cri d'un hibou.

- Route 1 (all listed pages together): [B1 PDF 135 / JSON 134](../data/input/harry-potter-1-lecole-des-sorciers.pdf#page=135)

**Required need 2:** Harry joue pour endormir Touffu et accéder à la trappe.

- Route 1 (all listed pages together): [B1 PDF 184 / JSON 183](../data/input/harry-potter-1-lecole-des-sorciers.pdf#page=184)

**Context-only:** None

**Negative counterchecks:** None

**Annotation note:** Sufficient support checked locally; exhaustive alternative search and human validation pending.

**Scope note:** Two scenes 49 PDF pages apart. Merely recalling that Hagrid gave Harry a flute does not answer the sound-at-first-use part.

**Human decision (accept / edit / reject):** ____________________

**Human evidence/category corrections:** ____________________

### M02 — multi_passage

**Question:** Combien de points Gryffondor perd-il à cause de la sortie nocturne liée à Norbert, puis combien Dumbledore lui ajoute-t-il au banquet final ?

**Reference answer:** La sortie nocturne coûte cent cinquante points à Gryffondor. Dumbledore ajoute ensuite cent soixante-dix points au banquet final.

**Historical flat gold_pages:** [B1 PDF 164 / JSON 163](../data/input/harry-potter-1-lecole-des-sorciers.pdf#page=164); [B1 PDF 165 / JSON 164](../data/input/harry-potter-1-lecole-des-sorciers.pdf#page=165); [B1 PDF 205 / JSON 204](../data/input/harry-potter-1-lecole-des-sorciers.pdf#page=205); [B1 PDF 206 / JSON 205](../data/input/harry-potter-1-lecole-des-sorciers.pdf#page=206)

**Required need 1:** Gryffondor perd 150 points.

- Route 1 (all listed pages together): [B1 PDF 165 / JSON 164](../data/input/harry-potter-1-lecole-des-sorciers.pdf#page=165)

**Required need 2:** Le banquet apporte 170 points à Gryffondor.

- Route 1 (all listed pages together): [B1 PDF 206 / JSON 205](../data/input/harry-potter-1-lecole-des-sorciers.pdf#page=206)

**Context-only:** [B1 PDF 164 / JSON 163](../data/input/harry-potter-1-lecole-des-sorciers.pdf#page=164); [B1 PDF 205 / JSON 204](../data/input/harry-potter-1-lecole-des-sorciers.pdf#page=205)

**Negative counterchecks:** None

**Annotation note:** Only totals are required; the earlier scene and Ron's individual award are context, not extra scored needs.

**Scope note:** Phase 1b: only the two requested totals are required. PDF 165 states the loss; PDF 206 permits the final total (100 + 60 + 10). PDFs 164 and 205 are context only for this answer, preserved in flat gold_pages.

**Human decision (accept / edit / reject):** ____________________

**Human evidence/category corrections:** ____________________

### M03 — multi_passage

**Question:** De quoi Jedusor accuse-t-il précisément Hagrid dans le souvenir qui trompe Harry, et comment explique-t-il ensuite le rôle de Ginny dans les nouvelles attaques ?

**Reference answer:** Le souvenir montre Jedusor accusant Hagrid de garder une créature meurtrière, ce qui pousse Harry à le croire responsable de l'ancienne ouverture. Jedusor révèle ensuite qu'il a manipulé Ginny pour ouvrir la Chambre et lancer les attaques récentes.

**Historical flat gold_pages:** [B2 PDF 128 / JSON 127](../data/input/harry-potter-2-la-chambre-des-secrets.pdf#page=128); [B2 PDF 129 / JSON 128](../data/input/harry-potter-2-la-chambre-des-secrets.pdf#page=129); [B2 PDF 161 / JSON 160](../data/input/harry-potter-2-la-chambre-des-secrets.pdf#page=161)

**Required need 1:** Jedusor accuse Hagrid de garder une créature qui aurait tué une élève.

- Route 1 (all listed pages together): [B2 PDF 128 / JSON 127](../data/input/harry-potter-2-la-chambre-des-secrets.pdf#page=128)

**Required need 2:** Jedusor manipule Ginny pour ouvrir la Chambre et lancer les attaques.

- Route 1 (all listed pages together): [B2 PDF 161 / JSON 160](../data/input/harry-potter-2-la-chambre-des-secrets.pdf#page=161)

**Context-only:** [B2 PDF 129 / JSON 128](../data/input/harry-potter-2-la-chambre-des-secrets.pdf#page=129)

**Negative counterchecks:** None

**Annotation note:** PDF 129 corroborates Harry's mistaken inference. The question now requires the detailed accusation rather than a generic capture recap.

**Scope note:** Phase 1b: explicitly asks for the accusation about keeping a murderous creature, not merely the capture recalled on PDF 161. PDF 128 supports the accusation, 129 corroborates Harry's false conclusion, and 161 supports manipulation of Ginny. These are not all independently required pages.

**Human decision (accept / edit / reject):** ____________________

**Human evidence/category corrections:** ____________________

### M04 — multi_passage

**Question:** Comment la voiture des Weasley traite-t-elle Harry et Ron après l'accident à leur arrivée à Poudlard, puis lors de leur rencontre avec les araignées ?

**Reference answer:** Après l'accident, elle les expulse avec leurs bagages et s'en va. Plus tard, elle vient les chercher au milieu des araignées et les ramène jusqu'à la lisière de la forêt.

**Historical flat gold_pages:** [B2 PDF 42 / JSON 41](../data/input/harry-potter-2-la-chambre-des-secrets.pdf#page=42); [B2 PDF 145 / JSON 144](../data/input/harry-potter-2-la-chambre-des-secrets.pdf#page=145)

**Required need 1:** La voiture expulse les garçons et leurs bagages puis s'en va.

- Route 1 (all listed pages together): [B2 PDF 42 / JSON 41](../data/input/harry-potter-2-la-chambre-des-secrets.pdf#page=42)

**Required need 2:** Elle les sauve des araignées et les conduit à la lisière.

- Route 1 (all listed pages together): [B2 PDF 145 / JSON 144](../data/input/harry-potter-2-la-chambre-des-secrets.pdf#page=145)

**Context-only:** None

**Negative counterchecks:** None

**Annotation note:** Sufficient support checked locally; exhaustive alternative search and human validation pending.

**Scope note:** Compare two autonomous actions in distant scenes; do not require the name of the tree from an earlier page.

**Human decision (accept / edit / reject):** ____________________

**Human evidence/category corrections:** ____________________

### M05 — multi_passage

**Question:** Pourquoi l'Éclair de Feu reçu par Harry est-il confisqué, et qui la lettre finale révèle-t-elle comme son donateur ?

**Reference answer:** McGonagall le fait vérifier parce qu'Hermione soupçonne Sirius Black de l'avoir envoyé avec un mauvais sort. La lettre révèle que Sirius est bien le donateur.

**Historical flat gold_pages:** [B3 PDF 154 / JSON 153](../data/input/harry-potter-3-le-prisonnier-dazkaban.pdf#page=154); [B3 PDF 286 / JSON 285](../data/input/harry-potter-3-le-prisonnier-dazkaban.pdf#page=286)

**Required need 1:** Le balai est confisqué pour vérifier un possible mauvais sort, Hermione soupçonnant Sirius.

- Route 1 (all listed pages together): [B3 PDF 154 / JSON 153](../data/input/harry-potter-3-le-prisonnier-dazkaban.pdf#page=154)

**Required need 2:** Sirius révèle être le donateur.

- Route 1 (all listed pages together): [B3 PDF 286 / JSON 285](../data/input/harry-potter-3-le-prisonnier-dazkaban.pdf#page=286)

**Context-only:** None

**Negative counterchecks:** None

**Annotation note:** Sufficient support checked locally; exhaustive alternative search and human validation pending.

**Scope note:** Phase 1b: limits the letter question to donor identity. PDF 154 supports inspection and suspicion; PDF 286 supports donor. Payment, apology and Ron's reassurance about enchantment are not required.

**Human decision (accept / edit / reject):** ____________________

**Human evidence/category corrections:** ____________________

### M06 — multi_passage

**Question:** Quelle annonce Trelawney fait-elle sur le serviteur de Voldemort à l'examen, et comment Pettigrow échappe-t-il ensuite à ses gardiens ?

**Reference answer:** Elle annonce qu'avant minuit le serviteur se libérera pour rejoindre son maître et l'aider à retrouver sa puissance. Pettigrow neutralise Ron puis se transforme en rat, glisse hors de sa menotte et s'enfuit.

**Historical flat gold_pages:** [B3 PDF 214 / JSON 213](../data/input/harry-potter-3-le-prisonnier-dazkaban.pdf#page=214); [B3 PDF 253 / JSON 252](../data/input/harry-potter-3-le-prisonnier-dazkaban.pdf#page=253)

**Required need 1:** Le serviteur se libérera avant minuit et aidera Voldemort à retrouver sa puissance.

- Route 1 (all listed pages together): [B3 PDF 214 / JSON 213](../data/input/harry-potter-3-le-prisonnier-dazkaban.pdf#page=214)
- Route 2 (all listed pages together): [B3 PDF 282 / JSON 281](../data/input/harry-potter-3-le-prisonnier-dazkaban.pdf#page=282)

**Required need 2:** Pettigrow neutralise Ron et s'échappe en rat hors de sa menotte.

- Route 1 (all listed pages together): [B3 PDF 253 / JSON 252](../data/input/harry-potter-3-le-prisonnier-dazkaban.pdf#page=253)

**Context-only:** None

**Negative counterchecks:** None

**Annotation note:** Sufficient support checked locally; exhaustive alternative search and human validation pending.

**Scope note:** The later retrospective discussion summarizes the prophecy but not the escape mechanism requested here.

**Human decision (accept / edit / reject):** ____________________

**Human evidence/category corrections:** ____________________

### M08 — multi_passage

**Question:** Quelles méthodes Cedric utilise-t-il pour détourner son dragon, puis pour pouvoir rester sous l'eau pendant la deuxième épreuve ?

**Reference answer:** Il transforme une pierre en chien pour distraire le dragon. Dans le lac, il respire grâce à une bulle qui entoure sa tête.

**Historical flat gold_pages:** [B4 PDF 200 / JSON 199](../data/input/harry-potter-4-la-coupe-de-feu.pdf#page=200); [B4 PDF 270 / JSON 269](../data/input/harry-potter-4-la-coupe-de-feu.pdf#page=270); [B4 PDF 273 / JSON 272](../data/input/harry-potter-4-la-coupe-de-feu.pdf#page=273)

**Required need 1:** Cedric transforme une pierre en chien pour distraire le dragon.

- Route 1 (all listed pages together): [B4 PDF 200 / JSON 199](../data/input/harry-potter-4-la-coupe-de-feu.pdf#page=200)

**Required need 2:** Il respire sous l'eau grâce à une bulle autour de sa tête.

- Route 1 (all listed pages together): [B4 PDF 270 / JSON 269](../data/input/harry-potter-4-la-coupe-de-feu.pdf#page=270)
- Route 2 (all listed pages together): [B4 PDF 273 / JSON 272](../data/input/harry-potter-4-la-coupe-de-feu.pdf#page=273)

**Context-only:** None

**Negative counterchecks:** None

**Annotation note:** Sufficient support checked locally; exhaustive alternative search and human validation pending.

**Scope note:** Phase 1b: complementary needs are dragon diversion (PDF 200) and underwater breathing (either PDF 270 OR 273). The two water pages are alternatives, not jointly required. See evidence_annotations.json; flat gold_pages unchanged.

**Human decision (accept / edit / reject):** ____________________

**Human evidence/category corrections:** ____________________

### M09 — multi_passage

**Question:** En quoi le premier entraînement dirigé par Harry s'oppose-t-il à la méthode qu'Ombrage défend pour préparer les BUSE ?

**Reference answer:** Ombrage affirme que l'étude de la théorie suffit, sans entraînement préalable aux sortilèges. Harry fait au contraire pratiquer le désarmement aux élèves par équipes de deux.

**Historical flat gold_pages:** [B5 PDF 197 / JSON 196](../data/input/harry-potter-5-lordre-du-phoenix.pdf#page=197); [B5 PDF 318 / JSON 317](../data/input/harry-potter-5-lordre-du-phoenix.pdf#page=318)

**Required need 1:** Ombrage soutient qu'une préparation théorique suffit.

- Route 1 (all listed pages together): [B5 PDF 197 / JSON 196](../data/input/harry-potter-5-lordre-du-phoenix.pdf#page=197)

**Required need 2:** Harry fait pratiquer le désarmement par équipes de deux.

- Route 1 (all listed pages together): [B5 PDF 318 / JSON 317](../data/input/harry-potter-5-lordre-du-phoenix.pdf#page=318)

**Context-only:** None

**Negative counterchecks:** None

**Annotation note:** Sufficient support checked locally; exhaustive alternative search and human validation pending.

**Scope note:** Contrast the policy stated in class with the actual first practice session, not a general opinion about either teacher.

**Human decision (accept / edit / reject):** ____________________

**Human evidence/category corrections:** ____________________

### M10 — multi_passage

**Question:** Quels dispositifs Hermione met-elle en place pour annoncer les réunions de l'A.D. discrètement et pour sanctionner une dénonciation ?

**Reference answer:** Elle relie de faux Gallions par un sortilège pour transmettre la date et l'heure des réunions. Elle ensorcelle aussi la liste des membres : la dénonciation de Marietta fait apparaître sur son visage des boutons formant le mot cafard.

**Historical flat gold_pages:** [B5 PDF 322 / JSON 321](../data/input/harry-potter-5-lordre-du-phoenix.pdf#page=322); [B5 PDF 490 / JSON 489](../data/input/harry-potter-5-lordre-du-phoenix.pdf#page=490); [B5 PDF 510 / JSON 509](../data/input/harry-potter-5-lordre-du-phoenix.pdf#page=510)

**Required need 1:** Des faux Gallions liés transmettent la date et l'heure des réunions.

- Route 1 (all listed pages together): [B5 PDF 322 / JSON 321](../data/input/harry-potter-5-lordre-du-phoenix.pdf#page=322)

**Required need 2:** Marietta porte des boutons formant le mot cafard après sa dénonciation.

- Route 1 (all listed pages together): [B5 PDF 490 / JSON 489](../data/input/harry-potter-5-lordre-du-phoenix.pdf#page=490)

**Required need 3:** Hermione a ensorcelé la liste des membres.

- Route 1 (all listed pages together): [B5 PDF 510 / JSON 509](../data/input/harry-potter-5-lordre-du-phoenix.pdf#page=510)

**Context-only:** None

**Negative counterchecks:** None

**Annotation note:** Sufficient support checked locally; exhaustive alternative search and human validation pending.

**Scope note:** Three complementary facts: communication mechanism, observed punishment, and attribution of the list enchantment to Hermione.

**Human decision (accept / edit / reject):** ____________________

**Human evidence/category corrections:** ____________________

### M11 — multi_passage

**Question:** Qu'arrive-t-il physiquement à Katie quand elle touche le collier et à Ron après l'hydromel, et qui ces deux attaques visaient-elles ?

**Reference answer:** Katie s'élève dans les airs, hurle puis retombe ; Ron s'effondre en convulsant après avoir bu l'hydromel. Les deux attaques visaient Dumbledore.

**Historical flat gold_pages:** [B6 PDF 162 / JSON 161](../data/input/harry-potter-6-le-prince-de-sang-mecc82lecc81.pdf#page=162); [B6 PDF 255 / JSON 254](../data/input/harry-potter-6-le-prince-de-sang-mecc82lecc81.pdf#page=255); [B6 PDF 376 / JSON 375](../data/input/harry-potter-6-le-prince-de-sang-mecc82lecc81.pdf#page=376)

**Required need 1:** Katie s'élève, hurle puis retombe.

- Route 1 (all listed pages together): [B6 PDF 162 / JSON 161](../data/input/harry-potter-6-le-prince-de-sang-mecc82lecc81.pdf#page=162)

**Required need 2:** Ron s'effondre en convulsant après avoir bu l'hydromel.

- Route 1 (all listed pages together): [B6 PDF 255 / JSON 254](../data/input/harry-potter-6-le-prince-de-sang-mecc82lecc81.pdf#page=255)

**Required need 3:** Dumbledore était la cible des deux attaques.

- Route 1 (all listed pages together): [B6 PDF 376 / JSON 375](../data/input/harry-potter-6-le-prince-de-sang-mecc82lecc81.pdf#page=376)

**Context-only:** None

**Negative counterchecks:** None

**Annotation note:** Sufficient support checked locally; exhaustive alternative search and human validation pending.

**Scope note:** Phase 1b: adds event-specific physical effects to avoid the nearby victim-name recap on PDFs 374-376. PDF 162 describes Katie, 255 describes Ron, and 376 establishes the intended target; each need is complementary.

**Human decision (accept / edit / reject):** ____________________

**Human evidence/category corrections:** ____________________

### C02 — cross_book

**Question:** Comment Dobby obtient-il sa liberté chez les Malefoy, puis quelles conditions de travail accepte-t-il à Poudlard ?

**Reference answer:** Il devient libre lorsque Lucius jette la chaussette dans laquelle Harry avait mis le journal et qu'il la récupère. À Poudlard, il accepte un Gallion par semaine et un jour de congé par mois, après avoir refusé une offre plus généreuse.

**Historical flat gold_pages:** [B2 PDF 175 / JSON 174](../data/input/harry-potter-2-la-chambre-des-secrets.pdf#page=175); [B4 PDF 209 / JSON 208](../data/input/harry-potter-4-la-coupe-de-feu.pdf#page=209)

**Required need 1:** Harry place le journal dans une chaussette que Lucius jette et que Dobby récupère, le libérant.

- Route 1 (all listed pages together): [B2 PDF 175 / JSON 174](../data/input/harry-potter-2-la-chambre-des-secrets.pdf#page=175)

**Required need 2:** Dobby accepte un Gallion par semaine et un jour de congé par mois après avoir refusé davantage.

- Route 1 (all listed pages together): [B4 PDF 209 / JSON 208](../data/input/harry-potter-4-la-coupe-de-feu.pdf#page=209)

**Context-only:** None

**Negative counterchecks:** None

**Annotation note:** Sufficient support checked locally; exhaustive alternative search and human validation pending.

**Scope note:** Compare liberation and paid employment; F05 overlaps the first sub-answer. Preserve the actual accepted terms, not Dumbledore's initial offer.

**Human decision (accept / edit / reject):** ____________________

**Human evidence/category corrections:** ____________________

### C03 — cross_book

**Question:** Quels parents Harry voit-il dans le miroir lors de son premier Noël à Poudlard, et quelles sont les quatre personnes qui lui apparaissent grâce à la pierre avant qu'il rejoigne Voldemort dans la forêt ?

**Reference answer:** Dans le miroir, il voit son père et sa mère, James et Lily. La Pierre de Résurrection fait apparaître James, Lily, Sirius et Lupin auprès de lui.

**Historical flat gold_pages:** [B1 PDF 141 / JSON 140](../data/input/harry-potter-1-lecole-des-sorciers.pdf#page=141); [B1 PDF 144 / JSON 143](../data/input/harry-potter-1-lecole-des-sorciers.pdf#page=144); [B7 PDF 500 / JSON 499](../data/input/harry-potter-7-les-reliques-de-la-mort.pdf#page=500); [B7 PDF 501 / JSON 500](../data/input/harry-potter-7-les-reliques-de-la-mort.pdf#page=501)

**Required need 1:** Harry voit son père et sa mère dans le miroir.

- Route 1 (all listed pages together): [B1 PDF 141 / JSON 140](../data/input/harry-potter-1-lecole-des-sorciers.pdf#page=141)
- Route 2 (all listed pages together): [B1 PDF 144 / JSON 143](../data/input/harry-potter-1-lecole-des-sorciers.pdf#page=144)

**Required need 2:** La pierre fait apparaître James, Lily, Sirius et Lupin.

- Route 1 (all listed pages together): [B7 PDF 500 / JSON 499](../data/input/harry-potter-7-les-reliques-de-la-mort.pdf#page=500); [B7 PDF 501 / JSON 500](../data/input/harry-potter-7-les-reliques-de-la-mort.pdf#page=501)

**Context-only:** None

**Negative counterchecks:** None

**Annotation note:** The parents' names are identification aliases, not an extra requirement for the mirror page to spell both given names. All four stone appearances need the two-page bundle.

**Scope note:** Phase 1b: parents rather than extended family are required. Either PDF 141 or 144 supports the parents; PDFs 500 and 501 together establish the four stone appearances. No permanent resurrection is implied.

**Human decision (accept / edit / reject):** ____________________

**Human evidence/category corrections:** ____________________

### C04 — cross_book

**Question:** À quoi James et Sirius utilisaient-ils leurs miroirs quand ils étaient élèves, et qui se sert ensuite de l'un d'eux pour envoyer du secours à Harry chez les Malefoy ?

**Reference answer:** James et Sirius communiquaient ainsi lorsqu'ils étaient en retenue dans des endroits différents. Plus tard, Abelforth surveille Harry par le miroir et lui envoie Dobby pour le secourir.

**Historical flat gold_pages:** [B5 PDF 684 / JSON 683](../data/input/harry-potter-5-lordre-du-phoenix.pdf#page=684); [B7 PDF 399 / JSON 398](../data/input/harry-potter-7-les-reliques-de-la-mort.pdf#page=399); [B7 PDF 400 / JSON 399](../data/input/harry-potter-7-les-reliques-de-la-mort.pdf#page=400)

**Required need 1:** James et Sirius utilisaient leurs miroirs pour communiquer pendant des retenues séparées.

- Route 1 (all listed pages together): [B5 PDF 684 / JSON 683](../data/input/harry-potter-5-lordre-du-phoenix.pdf#page=684)

**Required need 2:** Abelforth utilise le miroir et envoie Dobby secourir Harry.

- Route 1 (all listed pages together): [B7 PDF 399 / JSON 398](../data/input/harry-potter-7-les-reliques-de-la-mort.pdf#page=399); [B7 PDF 400 / JSON 399](../data/input/harry-potter-7-les-reliques-de-la-mort.pdf#page=400)

**Context-only:** None

**Negative counterchecks:** None

**Annotation note:** Sufficient support checked locally; exhaustive alternative search and human validation pending.

**Scope note:** James's school use is in Sirius's note; the later recognition and identification of Abelforth straddle a page boundary. Use the French name Abelforth.

**Human decision (accept / edit / reject):** ____________________

**Human evidence/category corrections:** ____________________

### C05 — cross_book

**Question:** Quelle difficulté rencontre le groupe avec le médaillon pendant le nettoyage du square Grimmaurd, et qui Kreattur accuse-t-il plus tard de l'avoir volé ?

**Reference answer:** Personne ne parvient à ouvrir le lourd médaillon pendant le nettoyage. Kreattur révèle ensuite l'avoir récupéré, puis accuse Mondingus Fletcher de l'avoir volé.

**Historical flat gold_pages:** [B5 PDF 95 / JSON 94](../data/input/harry-potter-5-lordre-du-phoenix.pdf#page=95); [B7 PDF 137 / JSON 136](../data/input/harry-potter-7-les-reliques-de-la-mort.pdf#page=137)

**Required need 1:** Personne ne parvient à ouvrir le médaillon pendant le nettoyage.

- Route 1 (all listed pages together): [B5 PDF 95 / JSON 94](../data/input/harry-potter-5-lordre-du-phoenix.pdf#page=95)

**Required need 2:** Kreattur l'a récupéré puis Mondingus l'a volé.

- Route 1 (all listed pages together): [B7 PDF 137 / JSON 136](../data/input/harry-potter-7-les-reliques-de-la-mort.pdf#page=137)

**Context-only:** None

**Negative counterchecks:** None

**Annotation note:** Sufficient support checked locally; exhaustive alternative search and human validation pending.

**Scope note:** The fifth-book page establishes the inability to open it; the seventh-book page establishes recovery and theft.

**Human decision (accept / edit / reject):** ____________________

**Human evidence/category corrections:** ____________________

### C06 — cross_book

**Question:** Qui dit avoir emprunté la moto pour amener Harry bébé, à qui l'a-t-il empruntée, et qui la modifie avant le dernier départ de Harry de Privet Drive ?

**Reference answer:** Hagrid explique l'avoir empruntée à Sirius Black. Arthur Weasley la modifie avant le dernier départ de Harry.

**Historical flat gold_pages:** [B1 PDF 11 / JSON 10](../data/input/harry-potter-1-lecole-des-sorciers.pdf#page=11); [B7 PDF 38 / JSON 37](../data/input/harry-potter-7-les-reliques-de-la-mort.pdf#page=38)

**Required need 1:** Hagrid rapporte avoir emprunté la moto à Sirius.

- Route 1 (all listed pages together): [B1 PDF 11 / JSON 10](../data/input/harry-potter-1-lecole-des-sorciers.pdf#page=11)

**Required need 2:** Arthur a modifié la moto avant le dernier départ.

- Route 1 (all listed pages together): [B7 PDF 38 / JSON 37](../data/input/harry-potter-7-les-reliques-de-la-mort.pdf#page=38)

**Context-only:** None

**Negative counterchecks:** None

**Annotation note:** Book 7 identifies Sirius's motorcycle but does not reproduce the original explicit loan report. Cross-book necessity remains a human decision; inference can create a shortcut.

**Scope note:** Phase 1b: asks for the explicit loan report on book 1 PDF 11, not merely ownership inferable from book 7 PDF 38. The latter supports Arthur's modifications. Historical comparison; human review must still assess shortcut risk and cross-book label.

**Human decision (accept / edit / reject):** ____________________

**Human evidence/category corrections:** ____________________

### C07 — cross_book

**Question:** Pourquoi Harry empêche-t-il la mise à mort de Pettigrow dans la Cabane hurlante, et comment cette dette intervient-elle lors de leur affrontement au manoir Malefoy ?

**Reference answer:** Harry veut éviter que les meilleurs amis de son père deviennent des meurtriers. Au manoir, il rappelle à Pettigrow qu'il lui a sauvé la vie : Pettigrow hésite, relâche son étreinte, puis sa main d'argent se retourne contre lui et l'étrangle.

**Historical flat gold_pages:** [B3 PDF 249 / JSON 248](../data/input/harry-potter-3-le-prisonnier-dazkaban.pdf#page=249); [B7 PDF 336 / JSON 335](../data/input/harry-potter-7-les-reliques-de-la-mort.pdf#page=336)

**Required need 1:** Harry veut éviter que les amis de son père deviennent des meurtriers.

- Route 1 (all listed pages together): [B3 PDF 249 / JSON 248](../data/input/harry-potter-3-le-prisonnier-dazkaban.pdf#page=249)

**Required need 2:** Le rappel de sa dette fait hésiter Pettigrow puis la main d'argent l'étrangle.

- Route 1 (all listed pages together): [B7 PDF 336 / JSON 335](../data/input/harry-potter-7-les-reliques-de-la-mort.pdf#page=336)

**Context-only:** None

**Negative counterchecks:** None

**Annotation note:** Sufficient support checked locally; exhaustive alternative search and human validation pending.

**Scope note:** Connect Harry's stated moral reason in the Shrieking Shack with Pettigrew's later hesitation; do not invent a conscious rescue plan.

**Human decision (accept / edit / reject):** ____________________

**Human evidence/category corrections:** ____________________

### C09 — cross_book

**Question:** Pourquoi Nick fait-il casser une armoire par Peeves pendant la deuxième année de Harry, et comment Drago exploite-t-il une armoire réparée lors de sa sixième année ?

**Reference answer:** Nick veut détourner Rusard pour épargner une punition à Harry. Drago rétablit le passage entre l'armoire de Poudlard et celle de Barjow et Beurk pour faire entrer les Mangemorts.

**Historical flat gold_pages:** [B2 PDF 68 / JSON 67](../data/input/harry-potter-2-la-chambre-des-secrets.pdf#page=68); [B2 PDF 69 / JSON 68](../data/input/harry-potter-2-la-chambre-des-secrets.pdf#page=69); [B6 PDF 375 / JSON 374](../data/input/harry-potter-6-le-prince-de-sang-mecc82lecc81.pdf#page=375); [B6 PDF 376 / JSON 375](../data/input/harry-potter-6-le-prince-de-sang-mecc82lecc81.pdf#page=376)

**Required need 1:** Nick détourne Rusard pour éviter une punition à Harry.

- Route 1 (all listed pages together): [B2 PDF 69 / JSON 68](../data/input/harry-potter-2-la-chambre-des-secrets.pdf#page=69)

**Required need 2:** Drago répare la liaison entre les deux armoires pour faire entrer les Mangemorts.

- Route 1 (all listed pages together): [B6 PDF 375 / JSON 374](../data/input/harry-potter-6-le-prince-de-sang-mecc82lecc81.pdf#page=375); [B6 PDF 376 / JSON 375](../data/input/harry-potter-6-le-prince-de-sang-mecc82lecc81.pdf#page=376)

**Context-only:** [B2 PDF 68 / JSON 67](../data/input/harry-potter-2-la-chambre-des-secrets.pdf#page=68)

**Negative counterchecks:** None

**Annotation note:** Sufficient support checked locally; exhaustive alternative search and human validation pending.

**Scope note:** Phase 1b: book 2 PDF 69 suffices for Nick's diversion and avoided detention; PDF 68 is context. Book 6 PDFs 375-376 jointly establish paired-cabinet repair and confirmed entry. No unsupported physical-cabinet identity claim. See sidecar; flat gold_pages unchanged.

**Human decision (accept / edit / reject):** ____________________

**Human evidence/category corrections:** ____________________

### P01 — paraphrase

**Question:** Pourquoi la glace devant laquelle Harry retrouve sa famille risque-t-elle de lui faire oublier sa propre vie ?

**Reference answer:** Elle donne à voir ce que l'on désire le plus profondément, sans garantir que cela soit réel ou possible. On peut s'y perdre au point de négliger la vie réelle.

**Historical flat gold_pages:** [B1 PDF 144 / JSON 143](../data/input/harry-potter-1-lecole-des-sorciers.pdf#page=144)

**Required need 1:** Elle donne à voir ce que l'on désire le plus profondément, sans garantir que cela soit réel ou possible. On peut s'y perdre au point de négliger la vie réelle.

- Route 1 (all listed pages together): [B1 PDF 144 / JSON 143](../data/input/harry-potter-1-lecole-des-sorciers.pdf#page=144)

**Context-only:** None

**Negative counterchecks:** None

**Annotation note:** Sufficient support checked locally; exhaustive alternative search and human validation pending.

**Scope note:** Paraphrase target: the Mirror of Erised explanation; question avoids its proper name and the passage's desire formulation.

**Human decision (accept / edit / reject):** ____________________

**Human evidence/category corrections:** ____________________

### P02 — paraphrase

**Question:** Comment Lockhart a-t-il bâti sa célébrité sur des aventures qu'il n'avait pas vécues sans être démenti par leurs véritables héros ?

**Reference answer:** Il recueillait le récit des exploits d'autres sorciers, puis effaçait leurs souvenirs. Il pouvait ensuite publier ces histoires en s'en attribuant le mérite.

**Historical flat gold_pages:** [B2 PDF 154 / JSON 153](../data/input/harry-potter-2-la-chambre-des-secrets.pdf#page=154)

**Required need 1:** Il recueillait le récit des exploits d'autres sorciers, puis effaçait leurs souvenirs. Il pouvait ensuite publier ces histoires en s'en attribuant le mérite.

- Route 1 (all listed pages together): [B2 PDF 154 / JSON 153](../data/input/harry-potter-2-la-chambre-des-secrets.pdf#page=154)

**Context-only:** None

**Negative counterchecks:** None

**Annotation note:** Sufficient support checked locally; exhaustive alternative search and human validation pending.

**Scope note:** Paraphrase target: stolen achievements and Memory Charms; avoid requiring the spell's name.

**Human decision (accept / edit / reject):** ____________________

**Human evidence/category corrections:** ____________________

### P04 — paraphrase

**Question:** L'année du Tournoi, comment la journaliste bannie de l'école arrive-t-elle quand même à surprendre les confidences des élèves ?

**Reference answer:** Rita Skeeter prend la forme d'un scarabée pour écouter discrètement les conversations. C'est une Animagus qui n'a pas déclaré ce pouvoir.

**Historical flat gold_pages:** [B4 PDF 383 / JSON 382](../data/input/harry-potter-4-la-coupe-de-feu.pdf#page=383)

**Required need 1:** Rita Skeeter prend la forme d'un scarabée pour écouter discrètement les conversations. C'est une Animagus qui n'a pas déclaré ce pouvoir.

- Route 1 (all listed pages together): [B4 PDF 383 / JSON 382](../data/input/harry-potter-4-la-coupe-de-feu.pdf#page=383)

**Context-only:** None

**Negative counterchecks:** None

**Annotation note:** Sufficient support checked locally; exhaustive alternative search and human validation pending.

**Scope note:** Paraphrase target: Rita's covert listening; avoids using her name, beetle, or Animagus in the question.

**Human decision (accept / edit / reject):** ____________________

**Human evidence/category corrections:** ____________________

### P05 — paraphrase

**Question:** Quel endroit du château Dobby conseille-t-il pour réunir les élèves à l'abri des professeurs, et pourquoi peut-il convenir à des usages très différents ?

**Reference answer:** Il conseille la Salle sur Demande, qui se manifeste quand on en a vraiment besoin. Son contenu s'adapte à ce que recherche la personne qui la trouve.

**Historical flat gold_pages:** [B5 PDF 313 / JSON 312](../data/input/harry-potter-5-lordre-du-phoenix.pdf#page=313)

**Required need 1:** Il conseille la Salle sur Demande, qui se manifeste quand on en a vraiment besoin. Son contenu s'adapte à ce que recherche la personne qui la trouve.

- Route 1 (all listed pages together): [B5 PDF 313 / JSON 312](../data/input/harry-potter-5-lordre-du-phoenix.pdf#page=313)

**Context-only:** None

**Negative counterchecks:** None

**Annotation note:** Sufficient support checked locally; exhaustive alternative search and human validation pending.

**Scope note:** Paraphrase target: the room's need-dependent contents; no need to retrieve its location or entrance ritual.

**Human decision (accept / edit / reject):** ____________________

**Human evidence/category corrections:** ____________________

### P06 — paraphrase

**Question:** Dans la caverne, qu'est-ce qui tient à distance les morts sortis de l'eau et permet à Harry et Dumbledore de regagner leur embarcation ?

**Reference answer:** Dumbledore crée un cercle de feu qui repousse les cadavres et les protège jusqu'au bateau.

**Historical flat gold_pages:** [B6 PDF 368 / JSON 367](../data/input/harry-potter-6-le-prince-de-sang-mecc82lecc81.pdf#page=368); [B6 PDF 369 / JSON 368](../data/input/harry-potter-6-le-prince-de-sang-mecc82lecc81.pdf#page=369)

**Required need 1:** Le feu de Dumbledore repousse les cadavres.

- Route 1 (all listed pages together): [B6 PDF 368 / JSON 367](../data/input/harry-potter-6-le-prince-de-sang-mecc82lecc81.pdf#page=368)
- Route 2 (all listed pages together): [B6 PDF 369 / JSON 368](../data/input/harry-potter-6-le-prince-de-sang-mecc82lecc81.pdf#page=369)

**Required need 2:** Le cercle de feu les protège jusqu'au bateau.

- Route 1 (all listed pages together): [B6 PDF 369 / JSON 368](../data/input/harry-potter-6-le-prince-de-sang-mecc82lecc81.pdf#page=369)

**Context-only:** None

**Negative counterchecks:** None

**Annotation note:** PDF 369 alone covers both needs; 368 supports repulsion only and is not required for full answer support.

**Scope note:** Phase 1b: book 6 PDF 369 alone supports fire protection and return to the boat. PDF 368 supports the narrower fire-repulsion need but not the full embarkation answer. Sidecar separates these needs; flat gold_pages unchanged.

**Human decision (accept / edit / reject):** ____________________

**Human evidence/category corrections:** ____________________

### U01 — unanswerable

**Question:** Quelle chanson Harry et Hermione écoutent-ils à la radio lorsqu'ils dansent ensemble sous la tente ?

**Reference answer:** Les romans ne racontent pas cette danse et ne donnent donc pas de chanson à identifier.

**Historical flat gold_pages:** None

**Context-only:** None

**Negative counterchecks:** [B7 PDF 105 / JSON 104](../data/input/harry-potter-7-les-reliques-de-la-mort.pdf#page=105); [B7 PDF 108 / JSON 107](../data/input/harry-potter-7-les-reliques-de-la-mort.pdf#page=108); [B7 PDF 268 / JSON 267](../data/input/harry-potter-7-les-reliques-de-la-mort.pdf#page=268); [B7 PDF 273 / JSON 272](../data/input/harry-potter-7-les-reliques-de-la-mort.pdf#page=273); [B7 PDF 279 / JSON 278](../data/input/harry-potter-7-les-reliques-de-la-mort.pdf#page=279); [B7 PDF 312 / JSON 311](../data/input/harry-potter-7-les-reliques-de-la-mort.pdf#page=312); [B7 PDF 316 / JSON 315](../data/input/harry-potter-7-les-reliques-de-la-mort.pdf#page=316); [B7 PDF 317 / JSON 316](../data/input/harry-potter-7-les-reliques-de-la-mort.pdf#page=317)

**Annotation note:** No relevant gold pages. Counterchecks are possible confounders, never proof of exhaustive absence. Human confirmation of novel-only unanswerability is required.

**Scope note:** Film-scene premise. Checked seventh-book dance and radio references; PDF 312 does mention a briefly heard song, but no Harry/Hermione dance. Absence remains a human-review claim, not proof from a failed literal search.

**Human decision (accept / edit / reject):** ____________________

**Human evidence/category corrections:** ____________________

### U03 — unanswerable

**Question:** Quels sont les prénoms des deux parents d'Hermione avant qu'elle ne modifie leurs souvenirs ?

**Reference answer:** Les romans ne donnent pas leurs prénoms d'origine. Les identités qu'Hermione leur attribue après avoir modifié leurs souvenirs ne répondent pas à cette question.

**Historical flat gold_pages:** None

**Context-only:** None

**Negative counterchecks:** [B1 PDF 135 / JSON 134](../data/input/harry-potter-1-lecole-des-sorciers.pdf#page=135); [B2 PDF 32 / JSON 31](../data/input/harry-potter-2-la-chambre-des-secrets.pdf#page=32); [B7 PDF 69 / JSON 68](../data/input/harry-potter-7-les-reliques-de-la-mort.pdf#page=69)

**Annotation note:** No relevant gold pages. Counterchecks are possible confounders, never proof of exhaustive absence. Human confirmation of novel-only unanswerability is required.

**Scope note:** Original given names, not the later identities Wendell and Monica Wilkins; inspect the seventh-book account and earlier parent references.

**Human decision (accept / edit / reject):** ____________________

**Human evidence/category corrections:** ____________________

### U05 — unanswerable

**Question:** Quel est le montant exact, en Gallions, du salaire mensuel de Dumbledore comme directeur de Poudlard ?

**Reference answer:** Les romans ne donnent pas le montant de son salaire mensuel.

**Historical flat gold_pages:** None

**Context-only:** None

**Negative counterchecks:** [B4 PDF 209 / JSON 208](../data/input/harry-potter-4-la-coupe-de-feu.pdf#page=209); [B6 PDF 308 / JSON 307](../data/input/harry-potter-6-le-prince-de-sang-mecc82lecc81.pdf#page=308)

**Annotation note:** No relevant gold pages. Counterchecks are possible confounders, never proof of exhaustive absence. Human confirmation of novel-only unanswerability is required.

**Scope note:** Do not confuse Dumbledore's salary with the wages he offers Dobby or other financial references; negative search cannot by itself establish absence.

**Human decision (accept / edit / reject):** ____________________

**Human evidence/category corrections:** ____________________

## Execution and stop point

Performed standard-library structure/reference checks and direct per-page Poppler
extraction of 101 distinct pages: all 88 original gold pages, additional sidecar
references and negative counterchecks, including U04's tenure countercheck.
All seven PDF hashes and physical page counts match the manifest. Local opening logs and text
are ignored under data/output/eval/phase1b/. These checks verify files/pagination,
not the human correctness of claims or corpus-wide completeness.

The sidecar format and its invariant checks are documented in EVIDENCE.md.
The exact change log supports review against 4c63bc9. REVIEW.md's question column
is synchronized with current candidate wording; its decision cells remain blank.
No passages, PDF images, embeddings or stores were committed. No retrieval,
Gemini, generation, metric computation, app changes or ignore-rule changes occurred.

**STOP for explicit human approval before Phase 2.**
