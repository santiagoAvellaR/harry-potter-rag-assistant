# Candidate review — phase 1

Current freeze (2026-11-16): Santiago approved the 45 selected questions and their
wording for retrieval evaluation. Selected records now have `status: validated`;
the other 15 remain candidates. This does **not** record independent owner
verification of every evidence page or annotation. Evidence `human_review` stays
`pending`. See [dataset_freeze.json](dataset_freeze.json) for scope and hashes.
The phase-1 narrative below is historical where it describes pending selection.


All 60 entries are **candidates**, not a validated benchmark. No retrieval or generation scores have been calculated.

Write `accept`, `edit`, or `reject` in the Decision column and explain changes in Reviewer notes. Check the French reference answer and English scope notes in [questions.jsonl](questions.jsonl) as well as the PDF pages. Links below open your local PDFs; they are intentionally absent from the public repository. **PDF means the viewer page (one-based); JSON means the stored page index (zero-based).** Browser PDF fragments may be ignored; use the displayed page number if needed.

Acceptance should confirm that the question sounds natural, the reference answer is correct, every answer component is supported, the pages are complete, and the category fits. For `multi_passage` and `cross_book`, verify that a single recap elsewhere does not suffice for the complete answer. For `rare_detail`, assess rarity of the fact, not merely of a spelling. Add any overlooked supporting pages before approval. Avoid retaining near-duplicate questions if removing one improves coverage.

For `unanswerable`, the listed pages below are **counterchecks, not gold evidence**. A failed literal search is not proof of absence. Reject or rewrite an item if you know a novel passage that answers it.

Select 40–50 on editorial and evidence quality grounds **before any benchmark run**. An `edit` decision requires review of the amended wording and references. After your explicit approval, only retained, approved entries will receive `status: validated`; the initial candidates remain available in Git history. No automatic promotion is performed.

| Category | Candidates |
| --- | ---: |
| `factual_simple` | 15 |
| `rare_detail` | 12 |
| `multi_passage` | 12 |
| `cross_book` | 10 |
| `paraphrase` | 6 |
| `unanswerable` | 5 |

| Book | Candidates citing this book |
| --- | ---: |
| 1 | 11 |
| 2 | 9 |
| 3 | 8 |
| 4 | 9 |
| 5 | 9 |
| 6 | 8 |
| 7 | 11 |

Book counts overlap for cross-book questions and exclude unanswerable items.

Review alternative evidence especially in R08, M07, M08, C03, C10, and P03. The requested flat page-recall metric counts all listed pages, even when two pages independently support the same fact. This is a known measurement limitation, not a reason to quietly omit verified evidence. F02/M02 and F05/C02 also share sub-answers; consider this when selecting the final subset. U02 is particularly sensitive to its London qualifier: the novel does name Brockdale bridge.

| ID | Category | Candidate question | Pages to inspect | Decision | Reviewer notes |
| --- | --- | --- | --- | --- | --- |
| F01 | `factual_simple` | Quelle plante Rogue désigne-t-il lorsqu'il parle du tue-loup pendant son premier cours ? | [B1 PDF 95 / JSON 94](../data/input/harry-potter-1-lecole-des-sorciers.pdf#page=95) |  |  |
| F02 | `factual_simple` | Pourquoi Neville reçoit-il des points lors du banquet qui clôt la première année de Harry, et combien ? | [B1 PDF 206 / JSON 205](../data/input/harry-potter-1-lecole-des-sorciers.pdf#page=206) |  |  |
| F03 | `factual_simple` | Quels sont les deux pouvoirs de la Pierre philosophale que découvre Hermione dans sa lecture ? | [B1 PDF 149 / JSON 148](../data/input/harry-potter-1-lecole-des-sorciers.pdf#page=149) |  |  |
| F04 | `factual_simple` | Pourquoi les élèves doivent-ils se protéger les oreilles en rempotant les jeunes mandragores ? | [B2 PDF 51 / JSON 50](../data/input/harry-potter-2-la-chambre-des-secrets.pdf#page=51) |  |  |
| F05 | `factual_simple` | Comment Harry amène-t-il Lucius Malefoy à libérer Dobby à la fin de sa deuxième année ? | [B2 PDF 175 / JSON 174](../data/input/harry-potter-2-la-chambre-des-secrets.pdf#page=175) |  |  |
| F06 | `factual_simple` | Sous quelle identité Harry se présente-t-il lorsqu'il monte dans le Magicobus après sa fugue ? | [B3 PDF 24 / JSON 23](../data/input/harry-potter-3-le-prisonnier-dazkaban.pdf#page=24) |  |  |
| F07 | `factual_simple` | Que voit Hermione face à l'épouvantard pendant l'examen pratique de Lupin ? | [B3 PDF 210 / JSON 209](../data/input/harry-potter-3-le-prisonnier-dazkaban.pdf#page=210) |  |  |
| F08 | `factual_simple` | Quel dragon Harry tire-t-il au sort pour la première épreuve du Tournoi, et dans quel ordre doit-il passer ? | [B4 PDF 195 / JSON 194](../data/input/harry-potter-4-la-coupe-de-feu.pdf#page=195) |  |  |
| F09 | `factual_simple` | Qui apporte à Harry de quoi respirer sous l'eau juste avant la deuxième épreuve, et que lui donne-t-il ? | [B4 PDF 265 / JSON 264](../data/input/harry-potter-4-la-coupe-de-feu.pdf#page=265) |  |  |
| F10 | `factual_simple` | Que fait la plume d'Ombrage à Harry pendant ses retenues ? | [B5 PDF 216 / JSON 215](../data/input/harry-potter-5-lordre-du-phoenix.pdf#page=216) |  |  |
| F11 | `factual_simple` | Selon l'explication donnée au cours de Hagrid, qui peut voir les Sombrals ? | [B5 PDF 361 / JSON 360](../data/input/harry-potter-5-lordre-du-phoenix.pdf#page=361) |  |  |
| F12 | `factual_simple` | Que promet Slughorn à l'élève qui réussira le mieux le philtre de Mort Vivante lors de son premier cours ? | [B6 PDF 121 / JSON 120](../data/input/harry-potter-6-le-prince-de-sang-mecc82lecc81.pdf#page=121) |  |  |
| F13 | `factual_simple` | Dans le véritable souvenir de Slughorn, en combien de parties Jedusor envisage-t-il de diviser son âme ? | [B6 PDF 319 / JSON 318](../data/input/harry-potter-6-le-prince-de-sang-mecc82lecc81.pdf#page=319) |  |  |
| F14 | `factual_simple` | Par quel objet Ron entend-il Hermione prononcer son nom après avoir quitté ses amis ? | [B7 PDF 273 / JSON 272](../data/input/harry-potter-7-les-reliques-de-la-mort.pdf#page=273) |  |  |
| F15 | `factual_simple` | Que souhaite faire savoir Harry à ceux qui verront la tombe de Dobby ? | [B7 PDF 343 / JSON 342](../data/input/harry-potter-7-les-reliques-de-la-mort.pdf#page=343) |  |  |
| R01 | `rare_detail` | Quelle glace Hagrid offre-t-il à Harry pendant leurs premiers achats sur le chemin de Traverse ? | [B1 PDF 54 / JSON 53](../data/input/harry-potter-1-lecole-des-sorciers.pdf#page=54) |  |  |
| R02 | `rare_detail` | De quelle couleur est le premier pull de Noël que Mrs Weasley tricote pour Harry ? | [B1 PDF 136 / JSON 135](../data/input/harry-potter-1-lecole-des-sorciers.pdf#page=136) |  |  |
| R03 | `rare_detail` | Quels instruments accompagnent la danse des fantômes à la fête de Nick Quasi-Sans-Tête ? | [B2 PDF 70 / JSON 69](../data/input/harry-potter-2-la-chambre-des-secrets.pdf#page=70) |  |  |
| R04 | `rare_detail` | Quel fruit retrouve-t-on près de Colin Crivey après sa pétrification ? | [B2 PDF 94 / JSON 93](../data/input/harry-potter-2-la-chambre-des-secrets.pdf#page=94) |  |  |
| R05 | `rare_detail` | Quelle boisson Rosmerta sert-elle à Flitwick lors de la conversation que Harry écoute caché aux Trois Balais ? | [B3 PDF 135 / JSON 134](../data/input/harry-potter-3-le-prisonnier-dazkaban.pdf#page=135) |  |  |
| R06 | `rare_detail` | Quel numéro de coffre Sirius utilise-t-il pour payer l'Éclair de Feu offert à Harry ? | [B3 PDF 286 / JSON 285](../data/input/harry-potter-3-le-prisonnier-dazkaban.pdf#page=286) |  |  |
| R07 | `rare_detail` | Comment reconnaître les deux chaussettes que Dobby tricote pour Harry à Noël, l'année du Tournoi ? | [B4 PDF 225 / JSON 224](../data/input/harry-potter-4-la-coupe-de-feu.pdf#page=225) |  |  |
| R08 | `rare_detail` | Quel mot de passe Cedric donne-t-il à Harry pour entrer dans la salle de bains des préfets ? | [B4 PDF 236 / JSON 235](../data/input/harry-potter-4-la-coupe-de-feu.pdf#page=236); [B4 PDF 249 / JSON 248](../data/input/harry-potter-4-la-coupe-de-feu.pdf#page=249) |  |  |
| R09 | `rare_detail` | Quel numéro Arthur Weasley compose-t-il dans la cabine téléphonique pour entrer au ministère avec Harry ? | [B5 PDF 102 / JSON 101](../data/input/harry-potter-5-lordre-du-phoenix.pdf#page=102) |  |  |
| R10 | `rare_detail` | Dans quelle salle de Sainte-Mangouste Arthur Weasley est-il hospitalisé après l'attaque du serpent ? | [B5 PDF 393 / JSON 392](../data/input/harry-potter-5-lordre-du-phoenix.pdf#page=393) |  |  |
| R11 | `rare_detail` | Quelles sont les deux odeurs qu'Hermione nomme avant de s'interrompre en parlant de l'Amortentia ? | [B6 PDF 119 / JSON 118](../data/input/harry-potter-6-le-prince-de-sang-mecc82lecc81.pdf#page=119) |  |  |
| R12 | `rare_detail` | Comment Fred se procure-t-il les cheveux utilisés pour déguiser Harry au mariage ? | [B7 PDF 98 / JSON 97](../data/input/harry-potter-7-les-reliques-de-la-mort.pdf#page=98) |  |  |
| M01 | `multi_passage` | Quel son produit le cadeau de Hagrid lorsque Harry l'essaie à son premier Noël, et à quoi lui sert-il lorsqu'il retourne auprès de Touffu ? | [B1 PDF 135 / JSON 134](../data/input/harry-potter-1-lecole-des-sorciers.pdf#page=135); [B1 PDF 184 / JSON 183](../data/input/harry-potter-1-lecole-des-sorciers.pdf#page=184) |  |  |
| M02 | `multi_passage` | Combien de points Gryffondor perd-il à cause de la sortie nocturne liée à Norbert, puis combien Dumbledore lui ajoute-t-il au banquet final ? | [B1 PDF 164 / JSON 163](../data/input/harry-potter-1-lecole-des-sorciers.pdf#page=164); [B1 PDF 165 / JSON 164](../data/input/harry-potter-1-lecole-des-sorciers.pdf#page=165); [B1 PDF 205 / JSON 204](../data/input/harry-potter-1-lecole-des-sorciers.pdf#page=205); [B1 PDF 206 / JSON 205](../data/input/harry-potter-1-lecole-des-sorciers.pdf#page=206) |  |  |
| M03 | `multi_passage` | De quoi Jedusor accuse-t-il précisément Hagrid dans le souvenir qui trompe Harry, et comment explique-t-il ensuite le rôle de Ginny dans les nouvelles attaques ? | [B2 PDF 128 / JSON 127](../data/input/harry-potter-2-la-chambre-des-secrets.pdf#page=128); [B2 PDF 129 / JSON 128](../data/input/harry-potter-2-la-chambre-des-secrets.pdf#page=129); [B2 PDF 161 / JSON 160](../data/input/harry-potter-2-la-chambre-des-secrets.pdf#page=161) |  |  |
| M04 | `multi_passage` | Comment la voiture des Weasley traite-t-elle Harry et Ron après l'accident à leur arrivée à Poudlard, puis lors de leur rencontre avec les araignées ? | [B2 PDF 42 / JSON 41](../data/input/harry-potter-2-la-chambre-des-secrets.pdf#page=42); [B2 PDF 145 / JSON 144](../data/input/harry-potter-2-la-chambre-des-secrets.pdf#page=145) |  |  |
| M05 | `multi_passage` | Pourquoi l'Éclair de Feu reçu par Harry est-il confisqué, et qui la lettre finale révèle-t-elle comme son donateur ? | [B3 PDF 154 / JSON 153](../data/input/harry-potter-3-le-prisonnier-dazkaban.pdf#page=154); [B3 PDF 286 / JSON 285](../data/input/harry-potter-3-le-prisonnier-dazkaban.pdf#page=286) |  |  |
| M06 | `multi_passage` | Quelle annonce Trelawney fait-elle sur le serviteur de Voldemort à l'examen, et comment Pettigrow échappe-t-il ensuite à ses gardiens ? | [B3 PDF 214 / JSON 213](../data/input/harry-potter-3-le-prisonnier-dazkaban.pdf#page=214); [B3 PDF 253 / JSON 252](../data/input/harry-potter-3-le-prisonnier-dazkaban.pdf#page=253) |  |  |
| M07 | `multi_passage` | Quels objets Harry touche-t-il pour voyager par Portoloin sur la colline de Têtafouine, puis à la fin du labyrinthe du Tournoi ? | [B4 PDF 51 / JSON 50](../data/input/harry-potter-4-la-coupe-de-feu.pdf#page=51); [B4 PDF 338 / JSON 337](../data/input/harry-potter-4-la-coupe-de-feu.pdf#page=338); [B4 PDF 339 / JSON 338](../data/input/harry-potter-4-la-coupe-de-feu.pdf#page=339); [B4 PDF 356 / JSON 355](../data/input/harry-potter-4-la-coupe-de-feu.pdf#page=356) |  |  |
| M08 | `multi_passage` | Quelles méthodes Cedric utilise-t-il pour détourner son dragon, puis pour pouvoir rester sous l'eau pendant la deuxième épreuve ? | [B4 PDF 200 / JSON 199](../data/input/harry-potter-4-la-coupe-de-feu.pdf#page=200); [B4 PDF 270 / JSON 269](../data/input/harry-potter-4-la-coupe-de-feu.pdf#page=270); [B4 PDF 273 / JSON 272](../data/input/harry-potter-4-la-coupe-de-feu.pdf#page=273) |  |  |
| M09 | `multi_passage` | En quoi le premier entraînement dirigé par Harry s'oppose-t-il à la méthode qu'Ombrage défend pour préparer les BUSE ? | [B5 PDF 197 / JSON 196](../data/input/harry-potter-5-lordre-du-phoenix.pdf#page=197); [B5 PDF 318 / JSON 317](../data/input/harry-potter-5-lordre-du-phoenix.pdf#page=318) |  |  |
| M10 | `multi_passage` | Quels dispositifs Hermione met-elle en place pour annoncer les réunions de l'A.D. discrètement et pour sanctionner une dénonciation ? | [B5 PDF 322 / JSON 321](../data/input/harry-potter-5-lordre-du-phoenix.pdf#page=322); [B5 PDF 490 / JSON 489](../data/input/harry-potter-5-lordre-du-phoenix.pdf#page=490); [B5 PDF 510 / JSON 509](../data/input/harry-potter-5-lordre-du-phoenix.pdf#page=510) |  |  |
| M11 | `multi_passage` | Qu'arrive-t-il physiquement à Katie quand elle touche le collier et à Ron après l'hydromel, et qui ces deux attaques visaient-elles ? | [B6 PDF 162 / JSON 161](../data/input/harry-potter-6-le-prince-de-sang-mecc82lecc81.pdf#page=162); [B6 PDF 255 / JSON 254](../data/input/harry-potter-6-le-prince-de-sang-mecc82lecc81.pdf#page=255); [B6 PDF 376 / JSON 375](../data/input/harry-potter-6-le-prince-de-sang-mecc82lecc81.pdf#page=376) |  |  |
| M12 | `multi_passage` | Que réclame Gripsec pour aider Harry à entrer chez Gringotts, et comment Neville obtient-il l'arme avec laquelle il abat Nagini à la fin ? | [B7 PDF 362 / JSON 361](../data/input/harry-potter-7-les-reliques-de-la-mort.pdf#page=362); [B7 PDF 525 / JSON 524](../data/input/harry-potter-7-les-reliques-de-la-mort.pdf#page=525) |  |  |
| C01 | `cross_book` | D'où vient le bézoard décrit par Rogue pendant la première année, et comment Harry en utilise-t-il un pour secourir Ron en sixième année ? | [B1 PDF 95 / JSON 94](../data/input/harry-potter-1-lecole-des-sorciers.pdf#page=95); [B6 PDF 255 / JSON 254](../data/input/harry-potter-6-le-prince-de-sang-mecc82lecc81.pdf#page=255); [B6 PDF 256 / JSON 255](../data/input/harry-potter-6-le-prince-de-sang-mecc82lecc81.pdf#page=256) |  |  |
| C02 | `cross_book` | Comment Dobby obtient-il sa liberté chez les Malefoy, puis quelles conditions de travail accepte-t-il à Poudlard ? | [B2 PDF 175 / JSON 174](../data/input/harry-potter-2-la-chambre-des-secrets.pdf#page=175); [B4 PDF 209 / JSON 208](../data/input/harry-potter-4-la-coupe-de-feu.pdf#page=209) |  |  |
| C03 | `cross_book` | Quels parents Harry voit-il dans le miroir lors de son premier Noël à Poudlard, et quelles sont les quatre personnes qui lui apparaissent grâce à la pierre avant qu'il rejoigne Voldemort dans la forêt ? | [B1 PDF 141 / JSON 140](../data/input/harry-potter-1-lecole-des-sorciers.pdf#page=141); [B1 PDF 144 / JSON 143](../data/input/harry-potter-1-lecole-des-sorciers.pdf#page=144); [B7 PDF 500 / JSON 499](../data/input/harry-potter-7-les-reliques-de-la-mort.pdf#page=500); [B7 PDF 501 / JSON 500](../data/input/harry-potter-7-les-reliques-de-la-mort.pdf#page=501) |  |  |
| C04 | `cross_book` | À quoi James et Sirius utilisaient-ils leurs miroirs quand ils étaient élèves, et qui se sert ensuite de l'un d'eux pour envoyer du secours à Harry chez les Malefoy ? | [B5 PDF 684 / JSON 683](../data/input/harry-potter-5-lordre-du-phoenix.pdf#page=684); [B7 PDF 399 / JSON 398](../data/input/harry-potter-7-les-reliques-de-la-mort.pdf#page=399); [B7 PDF 400 / JSON 399](../data/input/harry-potter-7-les-reliques-de-la-mort.pdf#page=400) |  |  |
| C05 | `cross_book` | Quelle difficulté rencontre le groupe avec le médaillon pendant le nettoyage du square Grimmaurd, et qui Kreattur accuse-t-il plus tard de l'avoir volé ? | [B5 PDF 95 / JSON 94](../data/input/harry-potter-5-lordre-du-phoenix.pdf#page=95); [B7 PDF 137 / JSON 136](../data/input/harry-potter-7-les-reliques-de-la-mort.pdf#page=137) |  |  |
| C06 | `cross_book` | Qui dit avoir emprunté la moto pour amener Harry bébé, à qui l'a-t-il empruntée, et qui la modifie avant le dernier départ de Harry de Privet Drive ? | [B1 PDF 11 / JSON 10](../data/input/harry-potter-1-lecole-des-sorciers.pdf#page=11); [B7 PDF 38 / JSON 37](../data/input/harry-potter-7-les-reliques-de-la-mort.pdf#page=38) |  |  |
| C07 | `cross_book` | Pourquoi Harry empêche-t-il la mise à mort de Pettigrow dans la Cabane hurlante, et comment cette dette intervient-elle lors de leur affrontement au manoir Malefoy ? | [B3 PDF 249 / JSON 248](../data/input/harry-potter-3-le-prisonnier-dazkaban.pdf#page=249); [B7 PDF 336 / JSON 335](../data/input/harry-potter-7-les-reliques-de-la-mort.pdf#page=336) |  |  |
| C08 | `cross_book` | À quoi Harry utilise-t-il le vieux diadème lorsqu'il cache le livre du Prince, et qu'est-ce qui détruit finalement ce diadème pendant la bataille ? | [B6 PDF 336 / JSON 335](../data/input/harry-potter-6-le-prince-de-sang-mecc82lecc81.pdf#page=336); [B7 PDF 454 / JSON 453](../data/input/harry-potter-7-les-reliques-de-la-mort.pdf#page=454) |  |  |
| C09 | `cross_book` | Pourquoi Nick fait-il casser une armoire par Peeves pendant la deuxième année de Harry, et comment Drago exploite-t-il une armoire réparée lors de sa sixième année ? | [B2 PDF 68 / JSON 67](../data/input/harry-potter-2-la-chambre-des-secrets.pdf#page=68); [B2 PDF 69 / JSON 68](../data/input/harry-potter-2-la-chambre-des-secrets.pdf#page=69); [B6 PDF 375 / JSON 374](../data/input/harry-potter-6-le-prince-de-sang-mecc82lecc81.pdf#page=375); [B6 PDF 376 / JSON 375](../data/input/harry-potter-6-le-prince-de-sang-mecc82lecc81.pdf#page=376) |  |  |
| C10 | `cross_book` | Quelle école Fleur représente-t-elle au Tournoi des Trois Sorciers, et quelle famille rejoint-elle ensuite par son mariage ? | [B4 PDF 155 / JSON 154](../data/input/harry-potter-4-la-coupe-de-feu.pdf#page=155); [B4 PDF 200 / JSON 199](../data/input/harry-potter-4-la-coupe-de-feu.pdf#page=200); [B7 PDF 103 / JSON 102](../data/input/harry-potter-7-les-reliques-de-la-mort.pdf#page=103); [B7 PDF 104 / JSON 103](../data/input/harry-potter-7-les-reliques-de-la-mort.pdf#page=104) |  |  |
| P01 | `paraphrase` | Pourquoi la glace devant laquelle Harry retrouve sa famille risque-t-elle de lui faire oublier sa propre vie ? | [B1 PDF 144 / JSON 143](../data/input/harry-potter-1-lecole-des-sorciers.pdf#page=144) |  |  |
| P02 | `paraphrase` | Comment Lockhart a-t-il bâti sa célébrité sur des aventures qu'il n'avait pas vécues sans être démenti par leurs véritables héros ? | [B2 PDF 154 / JSON 153](../data/input/harry-potter-2-la-chambre-des-secrets.pdf#page=154) |  |  |
| P03 | `paraphrase` | Dans le train vers Poudlard, quelle gourmandise Lupin propose-t-il à Harry pour l'aider à se remettre de son malaise ? | [B3 PDF 57 / JSON 56](../data/input/harry-potter-3-le-prisonnier-dazkaban.pdf#page=57); [B3 PDF 58 / JSON 57](../data/input/harry-potter-3-le-prisonnier-dazkaban.pdf#page=58) |  |  |
| P04 | `paraphrase` | L'année du Tournoi, comment la journaliste bannie de l'école arrive-t-elle quand même à surprendre les confidences des élèves ? | [B4 PDF 383 / JSON 382](../data/input/harry-potter-4-la-coupe-de-feu.pdf#page=383) |  |  |
| P05 | `paraphrase` | Quel endroit du château Dobby conseille-t-il pour réunir les élèves à l'abri des professeurs, et pourquoi peut-il convenir à des usages très différents ? | [B5 PDF 313 / JSON 312](../data/input/harry-potter-5-lordre-du-phoenix.pdf#page=313) |  |  |
| P06 | `paraphrase` | Dans la caverne, qu'est-ce qui tient à distance les morts sortis de l'eau et permet à Harry et Dumbledore de regagner leur embarcation ? | [B6 PDF 368 / JSON 367](../data/input/harry-potter-6-le-prince-de-sang-mecc82lecc81.pdf#page=368); [B6 PDF 369 / JSON 368](../data/input/harry-potter-6-le-prince-de-sang-mecc82lecc81.pdf#page=369) |  |  |
| U01 | `unanswerable` | Quelle chanson Harry et Hermione écoutent-ils à la radio lorsqu'ils dansent ensemble sous la tente ? | Counterchecks only: [B7 PDF 105 / JSON 104](../data/input/harry-potter-7-les-reliques-de-la-mort.pdf#page=105); [B7 PDF 108 / JSON 107](../data/input/harry-potter-7-les-reliques-de-la-mort.pdf#page=108); [B7 PDF 268 / JSON 267](../data/input/harry-potter-7-les-reliques-de-la-mort.pdf#page=268); [B7 PDF 273 / JSON 272](../data/input/harry-potter-7-les-reliques-de-la-mort.pdf#page=273); [B7 PDF 279 / JSON 278](../data/input/harry-potter-7-les-reliques-de-la-mort.pdf#page=279); [B7 PDF 312 / JSON 311](../data/input/harry-potter-7-les-reliques-de-la-mort.pdf#page=312); [B7 PDF 316 / JSON 315](../data/input/harry-potter-7-les-reliques-de-la-mort.pdf#page=316); [B7 PDF 317 / JSON 316](../data/input/harry-potter-7-les-reliques-de-la-mort.pdf#page=317) |  |  |
| U02 | `unanswerable` | Quel pont londonien voit-on s'effondrer sous l'attaque des Mangemorts au début du Prince de sang-mêlé ? | Counterchecks only: [B6 PDF 4 / JSON 3](../data/input/harry-potter-6-le-prince-de-sang-mecc82lecc81.pdf#page=4); [B6 PDF 7 / JSON 6](../data/input/harry-potter-6-le-prince-de-sang-mecc82lecc81.pdf#page=7); [B6 PDF 8 / JSON 7](../data/input/harry-potter-6-le-prince-de-sang-mecc82lecc81.pdf#page=8) |  |  |
| U03 | `unanswerable` | Quels sont les prénoms des deux parents d'Hermione avant qu'elle ne modifie leurs souvenirs ? | Counterchecks only: [B1 PDF 135 / JSON 134](../data/input/harry-potter-1-lecole-des-sorciers.pdf#page=135); [B2 PDF 32 / JSON 31](../data/input/harry-potter-2-la-chambre-des-secrets.pdf#page=32); [B7 PDF 69 / JSON 68](../data/input/harry-potter-7-les-reliques-de-la-mort.pdf#page=69) |  |  |
| U04 | `unanswerable` | Quelle est la date de naissance exacte de Minerva McGonagall, avec le jour, le mois et l'année ? | Counterchecks only: [B5 PDF 260 / JSON 259](../data/input/harry-potter-5-lordre-du-phoenix.pdf#page=260) |  |  |
| U05 | `unanswerable` | Quel est le montant exact, en Gallions, du salaire mensuel de Dumbledore comme directeur de Poudlard ? | Counterchecks only: [B4 PDF 209 / JSON 208](../data/input/harry-potter-4-la-coupe-de-feu.pdf#page=209); [B6 PDF 308 / JSON 307](../data/input/harry-potter-6-le-prince-de-sang-mecc82lecc81.pdf#page=308) |  |  |

Reviewer name: ____________________

Review date: ____________________

Approved final IDs / edited-file reference: ____________________

Do not enter a human validation date until this review has actually happened.
