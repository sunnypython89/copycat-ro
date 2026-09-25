# Raport de progres — Copycat

**Data:** 22 septembrie 2026  
**Obiectiv:** Copycat să editeze textul românesc precis și, ulterior, să poarte conversații care sună firesc pentru un vorbitor nativ.

## Unde suntem

Există două versiuni noi, păstrate separat:

1. **Copycat 04 — editare precisă.** Antrenat pe 104 exemple, în 4 epoci. Este cea mai bună versiune verificată pentru editarea strictă.
2. **Copycat Română 01 — primă încercare de conversație naturală.** Antrenat separat pe 145 exemple (104 de editare și 41 de exprimare naturală), în 4 epoci. Este experimental; nu îl considerăm încă versiunea principală.

Ambele folosesc modelul de bază `OpenLLM-Ro/RoMistral-7b-Instruct-2025-04-23` și adaptoare LoRA. Modelul de bază și adaptoarele anterioare nu au fost suprascrise. Antrenarea și inferența s-au făcut local pe NVIDIA GeForce RTX 3080 Ti. Nu a fost folosită cheia OpenAI API pentru aceste rulări.

## Rezultate comparabile

| Probă | Copycat 03 | Copycat 04 | Română 01 |
| --- | ---: | ---: | ---: |
| Micro-lecția 04: elimină exact apariția cerută, 8 exemple nevăzute | 5/8 | 7/8 | 8/8 |
| Benchmarkul vechi de editare, 36 exemple | 35/36 | 36/36 | 35/36 |
| Română firească, 12 situații separate, evaluare manuală strictă | — | 2/12 | 3/12 |

Scorul de 12 probe măsoară răspunsuri concrete la conversație, expresii idiomatice, ton, sens, diacritice și formulări naturale. **Nu este un procent de „nativitate”.** Setul este mic, iar evaluarea este orientativă. Rulările au folosit generare deterministă (`do_sample=False`).

## Ce s-a îmbunătățit

- Copycat 04 a eliminat eroarea anterioară la cuvântul „rapid” și a trecut toate cele 36 de teste vechi.
- Română 01 a trecut toate cele 8 cazuri ale micro-lecției 04. A simplificat corect un mesaj prea oficial și a adăugat diacriticele într-o propoziție unde Copycat 04 le ratase.

## Ce încă nu merge

- Română 01 a explicat greșit expresia „a bate apa în piuă”.
- La propoziția „L-am văzut pe Andrei cu binoclul”, ambele versiuni au ales arbitrar cine are binoclul, fără să recunoască ambiguitatea.
- Răspunsurile conversaționale pot suna rigide, pot rata tonul cerut sau pot schimba sensul.
- Română 01 a pierdut un test vechi: nu a corectat „vede” în „văd” în propoziția cerută. Prin urmare, câștigul mic la naturalețe vine cu o regresie la editare.

## Decizie

**Copycat 04 rămâne reperul pentru editare. Română 01 rămâne un experiment.** Nu îl consider încă suficient de natural pentru testul comun promis. Nu are sens să declarăm obiectivul atins pe baza câtorva exemple memorate sau a pierderii mici la antrenare.

## Următorul ciclu propus

1. Construim un set mai mare de dialoguri românești revizuite manual, în special pentru expresii idiomatice, ambiguități, ton colocvial și rescriere fără calcuri.
2. Păstrăm probe noi complet în afara antrenării și mărim evaluarea; cele 12 probe actuale sunt prea puține pentru o concluzie solidă.
3. Antrenăm un adaptor nou, fără să suprascriem versiunile 04 sau Română 01.
4. Promovăm noua variantă numai dacă îmbunătățește clar conversația **și** nu pierde la testele de editare.
5. Când trece acest prag intern, îl testăm împreună în conversație și introducem corecturile tale în următoarea lecție.

## Fișiere utile din proiect

- `gold_editare_04.jsonl` — 104 exemple pentru lecția 04.
- `train_copycat_04.py` și `copycat_editare_04_adapter/` — antrenarea și adaptorul de editare.
- `gold_romana_naturala_01.jsonl`, `train_copycat_romana_01.py` și `copycat_romana_naturala_01_adapter/` — prima variantă conversațională.
- `benchmark_copycat_04.py`, `benchmark_copycat_04_results.jsonl`, `benchmark_copycat_04_on_romana_01_results.jsonl` — micro-lecția și comparația.
- `benchmark_copycat_03_on_romana_01_results.jsonl` — regresia pe testele vechi.
- `probe_copycat_romanian.py`, `probe_copycat_romanian_04.jsonl`, `probe_copycat_romanian_01_results.jsonl`, `EVALUARE_ROMANA.md` — probele și evaluarea conversațională.

**Comanda pentru o testare viitoare a variantei experimentale:** din folderul `.`, rulează `python -u chat_copycat_romana_01.py`. Recomand să așteptăm următorul ciclu înainte de testul comun.
