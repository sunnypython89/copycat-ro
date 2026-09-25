# Copycat: evaluare internă a românei naturale

Probele din `probe_copycat_romanian.py` sunt separate de datele de antrenare. Rularea este deterministă (`do_sample=False`). Evaluarea de mai jos este o judecată manuală strictă: răspunsul trebuie să păstreze sensul cerut, să fie firesc în context și să respecte instrucțiunea. Nu reprezintă un procent de „nativitate”.

| Probă | Copycat 04 | Română 01 | Observație |
| --- | --- | --- | --- |
| colocvial | nu | nu | 04 folosește un calc; 01 schimbă problema în una emoțională. |
| idiom | nu | nu | Ambele explică greșit „a bate apa în piuă”. |
| registru | nu | da | 01 simplifică firesc mesajul către coleg. |
| empatie | nu | nu | 04 este prea lung; 01 minimizează trăirea prin „nu-ți mai face griji”. |
| sens | da | nu | 04 distinge nostalgia de dorința imediată de a pleca; 01 răspunde incomplet. |
| ambiguitate | nu | nu | Ambele aleg arbitrar cine are binoclul. |
| conversație | nu | nu | 04 sună prea oficial; 01 este contradictoriu. |
| umor | nu | nu | Glumele sunt nefirești pentru context. |
| diacritice | nu | da | 01 scrie „Mâine” corect. |
| variație | nu | nu | Nu oferă trei formulări distincte și firești. |
| nuanță | da | da | Explică diferența dintre „a zis” și „a promis”. |
| naturalizare | nu | nu | 04 păstrează calcul; 01 schimbă sensul final. |

**Rezultat strict:** Copycat 04: 2/12; Română 01: 3/12. Setul este mic și scorul este orientativ. Progresul la editare exactă, pe cele 8 probe ale lecției 04, este 5/8 (adaptorul 03), 7/8 (adaptorul 04), 8/8 (Română 01). Pe benchmarkul vechi, adaptorul 04 a obținut 36/36, iar Română 01 a coborât la 35/36: a ratat corectarea verbului „vede” în „văd”.

**Concluzie:** varianta Română 01 este o îmbunătățire mică, dar încă nu îndeplinește obiectivul de conversație care sună nativ și are o regresie la editare. Nu trebuie promovată ca versiune principală. Următoarea etapă are nevoie de un set mai mare de dialoguri românești revizuite, cu expresii idiomatice, ambiguități, tonuri diferite și exemple negative de calcuri, plus probe noi ținute complet în afara antrenării.
