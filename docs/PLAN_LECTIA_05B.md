# Lecția 05B — plan pentru revizuire, fără training

## Artefact candidat

`gold_romana_05b.jsonl` conține cele 75 de înregistrări din `gold_romana_05.jsonl`, păstrate identic și în aceeași ordine, plus 92 de exemple noi:

- 35 `noop`: 20 `strict_noop` (ținta este deja corectă, textul rămâne identic) și 15 `targeted_edit` (se execută numai schimbarea cerută; greșelile din jur rămân).
- 45 `idiom`: 15 grupuri de contrast, fiecare cu două contexte figurate diferite și un context literal pentru aceeași expresie. Perechi apropiate semantic includ „a pune paie pe foc” / „a turna gaz pe foc” și „a ridica ștacheta” / „a coborî ștacheta”; „a se da la fund” și „a arunca prosopul” cer distingerea evitării de renunțare.
- 12 `incertitudine`: termenul nu primește nicio definiție sau ipoteză când textul nu oferă dovezi.

Total candidat: 167 exemple. Categoriile finale sunt: ambiguitate 20, idiom 65, incertitudine 27, ton 20, noop 35.

## Verificări înainte de training

1. Confirmați că primele 75 de înregistrări sunt egale, câmp cu câmp, cu Gold 05 revizuit.
2. Verificați ID-urile, prompturile și perechile prompt/răspuns pentru duplicate exacte și după normalizarea spațiilor, majusculelor și punctuației.
3. Comparați prompturile cu cele 16 probe din `benchmark_romana_05.jsonl` și cele 36 de probe din `benchmark_copycat_03_on_04.py`. Nu includeți vreun prompt de benchmark în training.
4. Verificați că niciun exemplu nou nu conține expresiile exacte din cele patru probe idiomatice ale benchmarkului 05.
5. Revizuiți manual NOOP pentru modificări necerute și răspunsurile de incertitudine pentru ipoteze fără dovezi. `IN07` și, într-o măsură mai mică, `IN08` din Gold 05 existent merită discutate: oferă posibile etichete pentru termeni necunoscuți, deși mesajele nu le confirmă. Sunt păstrate identic conform cererii.

## Primul experiment propus

- Punct de pornire: modelul de bază RoMistral în 4 biți, apoi `PeftModel.from_pretrained(base, "copycat_editare_04_adapter", is_trainable=True)`. Se continuă **aceleași greutăți LoRA** ale Copycat 04; nu se pornește de la Copycat 05 și nu se creează un LoRA nou peste unul înghețat.
- Optimizați numai parametrii cu `requires_grad=True`. Folosiți `model.train()` și gradient checkpointing; nu apelați `merge_and_unload()`.
- Date: cele 167 exemple din Gold 05B și replay cu toate cele 104 exemple din `gold_editare_04.jsonl`. Amestecați la fiecare epocă, cu seed fix. Total 271 exemple/epocă, fără benchmarkuri.
- Learning rate: `5e-5`; maximum 2 epoci în primul experiment. Păstrați mascarea tokenurilor promptului, acumulare de gradient 4, batch 1 și lungime maximă 384, pentru comparabilitate cu 05.
- Salvați exclusiv în `copycat_05b_adapter` după ce ați verificat că directorul nu există; `copycat_editare_04_adapter` și `copycat_05_adapter` rămân intacte. Înregistrați loss-ul pe epoci și hashurile datelor.
- Evaluați pe benchmarkurile existente, nemodificate: 36 de probe de editare și 16 probe Lecția 05, cu aceleași setări de generare folosite pentru 04/05. Mențineți Copycat 04 principal până când un adaptor nou obține 36/36 la editare și depășește clar 4/16 la Lecția 05.

**Stare:** doar date și plan; trainingul 05B nu a fost pornit.
