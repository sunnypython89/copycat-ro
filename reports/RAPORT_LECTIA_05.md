# Lecția 05 — Sens înainte de intervenție

**Stare:** pregătită și evaluată fără antrenare. `copycat_editare_04_adapter` rămâne checkpointul principal; niciun adaptor existent nu a fost modificat.

## Seturi

| Categorie | Candidat `gold_romana_05.jsonl` | Benchmark separat |
| --- | ---: | ---: |
| Ambiguitate | 6 | 4 |
| Expresii idiomatice | 8 | 4 |
| Incertitudine | 6 | 4 |
| Ton colocvial cu sens păstrat | 8 | 4 |
| **Total** | **28** | **16** |

Prompturile celor 16 probe nu apar în niciun fișier `gold_*.jsonl` existent, inclusiv în candidatul 05. Benchmarkul este numai pentru evaluare și trebuie să rămână separat de antrenare.

## Metodă

Același model de bază RoMistral în 4 biți; fiecare întrebare a fost trimisă independent, cu `do_sample=False` și maximum 160 de tokenuri noi. Scorul este o evaluare manuală strictă după criteriul fiecărui exemplu. Parafrazele corecte sunt acceptate; copierea promptului sau schimbarea unui detaliu este eșec. Rezultatele brute sunt în `benchmark_romana_05_results.jsonl`.

## Rezultate

| Categorie | Copycat 04 | Română 01 |
| --- | ---: | ---: |
| Ambiguitate | 0/4 | 0/4 |
| Expresii idiomatice | 1/4 | 0/4 |
| Incertitudine | 3/4 | 3/4 |
| Ton colocvial | 0/4 | 1/4 |
| **Total** | **4/16** | **4/16** |

Scorurile egale ascund comportamente diferite. Copycat 04 înțelege una dintre cele patru expresii, iar Română 01 reformulează corect un mesaj. Ambele ratează toate probele de ambiguitate și inventează un sens pentru «zumbilic».

## Erori exacte — Copycat 04

### A1 · Ambiguitate

**Întrebare:** În «Luca i-a spus lui Matei că tatăl lui pleacă mâine», al cui tată pleacă?

**Răspuns produs, exact:**

```text
Luca i-a spus lui Matei că tatăl lui pleacă mâine.
```

**Referință:** Poate fi tatăl lui Luca sau al lui Matei; enunțul nu decide.

**De ce e greșit:** Repetă enunțul și nu identifică cele două posibile referințe ale lui «lui».

### A2 · Ambiguitate

**Întrebare:** În «Am urmărit femeia cu camera video», cine avea camera video?

**Răspuns produs, exact:**

```text
Nu am informații despre articolul specific „Am urmărit femeia cu camera video”. Cu toate acestea, pe baza titlului, se poate deduce că persoana care a urmărit femeia a avut camera video.
```

**Referință:** Poate fi persoana care urmărea sau femeia urmărită; contextul lipsește.

**De ce e greșit:** Alege arbitrar persoana care urmărește și tratează enunțul ca titlu de articol.

### A3 · Ambiguitate

**Întrebare:** În «Bianca a văzut-o pe Sorina când ieșea din bibliotecă», cine ieșea?

**Răspuns produs, exact:**

```text
Bianca a văzut-o pe Sorina când ieșea din bibliotecă.
```

**Referință:** Poate fi Bianca sau Sorina; propoziția nu lămurește.

**De ce e greșit:** Repetă enunțul, fără să identifice cine putea ieși din bibliotecă.

### A4 · Ambiguitate

**Întrebare:** În «Mara a vorbit cu Dana despre planul ei», al cui era planul?

**Răspuns produs, exact:**

```text
Mara a vorbit cu Dana despre planul ei.
```

**Referință:** Poate fi planul Marei sau al Danei; nu putem stabili fără context.

**De ce e greșit:** Repetă enunțul, fără să identifice ambele posibile referințe ale lui «ei».

### I2 · Expresii idiomatice

**Întrebare:** Ce înseamnă «a tăia frunză la câini» în vorbirea de zi cu zi?

**Răspuns produs, exact:**

```text
„A tăia frunză la câini” este o expresie idiomatică care înseamnă a face ceva care este inutil, inutil sau risipitor. Este adesea folosită pentru a descrie o situație în care cineva încearcă să rezolve o problemă sau să abordeze o sarcină într-un mod care este prea complicat, ineficient sau chiar contraproductiv.

Originea expresiei este neclară, dar se crede că provine din ideea de a tăia frunzele de pe un copac, ceea ce poate fi
```

**Referință:** Înseamnă să pierzi vremea fără să faci ceva util.

**De ce e greșit:** Spune că acțiunea este inutilă, dar nu dă sensul idiomatic de a sta degeaba ori a pierde vremea.

### I3 · Expresii idiomatice

**Întrebare:** Ce înseamnă «a da bir cu fugiții»?

**Răspuns produs, exact:**

```text
„A da bir cu fugiții” este o expresie idiomatică în limba română care înseamnă „a da o lovitură cu pumnul”.
```

**Referință:** Înseamnă să fugi sau să te retragi când apare o obligație ori o dificultate.

**De ce e greșit:** Inventează sensul de lovitură cu pumnul.

### I4 · Expresii idiomatice

**Întrebare:** Ce înseamnă «a se culca pe o ureche» într-o discuție despre muncă?

**Răspuns produs, exact:**

```text
„A se culca pe o ureche” este o expresie idiomatică care înseamnă a fi complet absorbit sau implicat în ceva, adesea până la punctul de a fi distras sau distras de alte lucruri. În contextul discuțiilor despre muncă, ar putea însemna că cineva este atât de concentrat pe un proiect sau sarcină încât nu este conștient de alte aspecte ale muncii sale sau nu este receptiv la feedback sau sugestii.
```

**Referință:** Înseamnă să te relaxezi prea devreme și să nu mai fii atent sau să nu mai faci efort.

**De ce e greșit:** Inventează sensul de concentrare excesivă; expresia indică o relaxare/neglijență prematură.

### U3 · Incertitudine

**Întrebare:** Ce înseamnă «zumbilic» în «Adu zumbilicul»? Nu ai alt context.

**Răspuns produs, exact:**

```text
„Zumbilic” este un termen colocvial care se referă la un tip de mâncare sau gustare, de obicei unul care este ușor de preparat și consumat. În contextul propoziției „Adu zumbilicul”, se referă probabil la un tip de mâncare sau gustare care este ușor de adus sau obținut.
```

**Referință:** Nu pot stabili sensul cuvântului din propoziție; ar putea fi un termen local, un nume sau o invenție. Ar trebui întrebat vorbitorul.

**De ce e greșit:** Inventează o definiție culinară pentru un cuvânt fără sens stabil în context.

### T1 · Ton colocvial

**Întrebare:** Rescrie ca mesaj firesc către un coleg, fără să pierzi informația: «Vă rog să îmi comunicați dacă puteți expedia raportul până joi la ora 16:00». Răspunde doar cu mesajul.

**Răspuns produs, exact:**

```text
Vă rog să îmi comunicați dacă puteți expedia raportul până joi la ora 16:00.
```

**Referință:** Îmi spui, te rog, dacă poți trimite raportul până joi la 16:00?

**De ce e greșit:** Lasă mesajul rigid aproape neschimbat.

### T2 · Ton colocvial

**Întrebare:** Rescrie ca mesaj firesc către un coleg, fără să pierzi informația: «Vă aduc la cunoștință că întâlnirea de marți de la 11:00 se mută în sala 3». Răspunde doar cu mesajul.

**Răspuns produs, exact:**

```text
Hei,

Vă aduc la cunoștință că întâlnirea de marți de la 11:00 se mută în sala 3.

Cel mai bun,
[Numele tău]
```

**Referință:** Întâlnirea de marți, de la 11:00, se mută în sala 3.

**De ce e greșit:** Păstrează formula rigidă și adaugă o încheiere de e-mail care nu era cerută.

### T3 · Ton colocvial

**Întrebare:** Rescrie ca mesaj firesc către un coleg, fără să pierzi informația: «Vă rog să confirmați primirea celor două documente atașate». Răspunde doar cu mesajul.

**Răspuns produs, exact:**

```text
Vă rog să confirmați primirea celor două documente atașate.
```

**Referință:** Îmi confirmi, te rog, că ai primit cele două documente atașate?

**De ce e greșit:** Lasă mesajul rigid neschimbat.

### T4 · Ton colocvial

**Întrebare:** Rescrie ca mesaj firesc către un coleg, fără să pierzi informația: «Nu pot participa la apelul de azi de la 14:30; vă propun mâine la 10:00». Răspunde doar cu mesajul.

**Răspuns produs, exact:**

```text
Nu pot participa la apelul de azi de la 14:30; vă propun mâine la 10:00.
```

**Referință:** Nu pot intra în apelul de azi de la 14:30. Putem vorbi mâine la 10:00?

**De ce e greșit:** Lasă mesajul rigid neschimbat.


## Erori exacte — Română 01

### A1 · Ambiguitate

**Întrebare:** În «Luca i-a spus lui Matei că tatăl lui pleacă mâine», al cui tată pleacă?

**Răspuns produs, exact:**

```text
Luca.
```

**Referință:** Poate fi tatăl lui Luca sau al lui Matei; enunțul nu decide.

**De ce e greșit:** Alege arbitrar pe Luca; poate fi și Matei.

### A2 · Ambiguitate

**Întrebare:** În «Am urmărit femeia cu camera video», cine avea camera video?

**Răspuns produs, exact:**

```text
Femeia avea camera video.
```

**Referință:** Poate fi persoana care urmărea sau femeia urmărită; contextul lipsește.

**De ce e greșit:** Alege arbitrar femeia; camera poate fi și a observatorului.

### A3 · Ambiguitate

**Întrebare:** În «Bianca a văzut-o pe Sorina când ieșea din bibliotecă», cine ieșea?

**Răspuns produs, exact:**

```text
Bianca a văzut-o pe Sorina când ieșea din bibliotecă.
```

**Referință:** Poate fi Bianca sau Sorina; propoziția nu lămurește.

**De ce e greșit:** Repetă enunțul și nu identifică cele două interpretări.

### A4 · Ambiguitate

**Întrebare:** În «Mara a vorbit cu Dana despre planul ei», al cui era planul?

**Răspuns produs, exact:**

```text
Mara.
```

**Referință:** Poate fi planul Marei sau al Danei; nu putem stabili fără context.

**De ce e greșit:** Alege arbitrar pe Mara; planul poate fi și al Danei.

### I1 · Expresii idiomatice

**Întrebare:** Ce înseamnă «a pune carul înaintea boilor»? Spune sensul, nu imaginea literală.

**Răspuns produs, exact:**

```text
Înseamnă să acorzi prioritate ceva ce vrei, în loc să aștepți până te apasă.
```

**Referință:** Înseamnă să faci lucrurile în ordinea greșită, începând cu ce ar trebui să vină mai târziu.

**De ce e greșit:** Nu redă sensul de a face pașii în ordinea greșită.

### I2 · Expresii idiomatice

**Întrebare:** Ce înseamnă «a tăia frunză la câini» în vorbirea de zi cu zi?

**Răspuns produs, exact:**

```text
Înseamnă să spui ceva dur sau nepoliticos.
```

**Referință:** Înseamnă să pierzi vremea fără să faci ceva util.

**De ce e greșit:** Confundă expresia cu o vorbire nepoliticoasă.

### I3 · Expresii idiomatice

**Întrebare:** Ce înseamnă «a da bir cu fugiții»?

**Răspuns produs, exact:**

```text
Înseamnă să începi să faci ceva, dar foarte încet.
```

**Referință:** Înseamnă să fugi sau să te retragi când apare o obligație ori o dificultate.

**De ce e greșit:** Nu redă fuga din fața obligației sau dificultății.

### I4 · Expresii idiomatice

**Întrebare:** Ce înseamnă «a se culca pe o ureche» într-o discuție despre muncă?

**Răspuns produs, exact:**

```text
Înseamnă să te abați complet de la subiect.
```

**Referință:** Înseamnă să te relaxezi prea devreme și să nu mai fii atent sau să nu mai faci efort.

**De ce e greșit:** Confundă expresia cu abaterea de la subiect.

### U3 · Incertitudine

**Întrebare:** Ce înseamnă «zumbilic» în «Adu zumbilicul»? Nu ai alt context.

**Răspuns produs, exact:**

```text
Înseamnă să aduci ceva.
```

**Referință:** Nu pot stabili sensul cuvântului din propoziție; ar putea fi un termen local, un nume sau o invenție. Ar trebui întrebat vorbitorul.

**De ce e greșit:** Nu admite că sensul cuvântului nu se poate stabili; răspunde tautologic.

### T1 · Ton colocvial

**Întrebare:** Rescrie ca mesaj firesc către un coleg, fără să pierzi informația: «Vă rog să îmi comunicați dacă puteți expedia raportul până joi la ora 16:00». Răspunde doar cu mesajul.

**Răspuns produs, exact:**

```text
Îmi trimiți, te rog, raportul până joi la ora 16:00?
```

**Referință:** Îmi spui, te rog, dacă poți trimite raportul până joi la 16:00?

**De ce e greșit:** Transformă întrebarea despre posibilitatea de a trimite raportul într-o cerere directă de trimitere.

### T3 · Ton colocvial

**Întrebare:** Rescrie ca mesaj firesc către un coleg, fără să pierzi informația: «Vă rog să confirmați primirea celor două documente atașate». Răspunde doar cu mesajul.

**Răspuns produs, exact:**

```text
Am primit cele două documente atașate.
```

**Referință:** Îmi confirmi, te rog, că ai primit cele două documente atașate?

**De ce e greșit:** Schimbă perspectiva: declară că a primit documentele în loc să ceară confirmarea primirii.

### T4 · Ton colocvial

**Întrebare:** Rescrie ca mesaj firesc către un coleg, fără să pierzi informația: «Nu pot participa la apelul de azi de la 14:30; vă propun mâine la 10:00». Răspunde doar cu mesajul.

**Răspuns produs, exact:**

```text
Nu pot intra în apel azi la 14:30. Îmi trimiți mâine la 10:00?
```

**Referință:** Nu pot intra în apelul de azi de la 14:30. Putem vorbi mâine la 10:00?

**De ce e greșit:** Păstrează prima informație, dar schimbă propunerea de apel într-o cerere neclară de trimitere.

## Propunere pentru structura antrenării 05

1. Tratați cele 28 de exemple din `gold_romana_05.jsonl` ca **set candidat**, nu ca dovadă că generalizarea este deja posibilă. Revizuiți-le lingvistic înainte de orice antrenare.
2. Extindeți fiecare categorie cu contexte și formulări variate, fără a copia cele 16 probe. Pentru ambiguitate, răspunsurile trebuie să numească două lecturi; pentru idiomuri, sensul figurat; pentru incertitudine, limita informației; pentru ton, toate detaliile originale.
3. Când există suficiente exemple revizuite, combinați noul set cu exemplele de editare din `gold_editare_04.jsonl` ca protecție împotriva uitării abilității de editare. Păstrați și o validare separată, cu exemple noi.
4. Rulați benchmarkul 05 și benchmarkurile vechi pe un adaptor **nou**, fără a suprascrie Copycat 04. Promovați-l numai dacă îmbunătățește sensul și tonul fără regresie la editare.

**Nicio antrenare nu a fost pornită pentru Lecția 05.**
