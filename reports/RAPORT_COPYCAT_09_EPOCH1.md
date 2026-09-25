# Raport Copycat 09 — epoca 1

## Training

- Pornire: `copycat_08_epoch1_adapter`, trainabil.
- Exact o epocă, learning rate `2e-5`, seed 42.
- LoRA r=8, alpha=16, dropout=0,05, `q_proj` și `v_proj`.
- 336 exemple; 84 pași de optimizare; loss mediu `0,0960052912`.

## Scoruri Copycat 09

- Editare 04: **36/36**.
- Lecția 05: **8/16** — {'ambiguitate': 0, 'idiom': 1, 'incertitudine': 4, 'ton': 3}.
- Lecția 06: **14/24** — {'ambiguitate_reala': 4, 'neambiguu': 6, 'context_rezolva': 0, 'trei_plus': 4}.
- Lecția 07: **18/24** — {'context_rezolva': 8, 'context_insuficient': 4, 'eliminare_multipla': 5, 'indiciu_irelevant': 1}.
- Lecția 08: **13/32** — {'ambiguu': 6, 'rezolvat': 2, 'indiciu_irelevant': 0, 'eliminare_multipla': 5}.
- Lecția 09: **20/32** — {'eliminare_2_pasi': 6, 'eliminare_3_pasi': 5, 'ambiguitate_ramasa': 5, 'indiciu_irelevant_intercalat': 4}.

## Consistența traseului pe Lecția 09

- Răspuns final corect + traseu corect: **19/32**.
- Răspuns final corect + traseu greșit: **1/32** — F8IR.
- Răspuns final greșit: **12/32**.

## Comparație Lecția 09

| Model | 2 pași /8 | 3+ pași /8 | Ambiguitate /8 | Irelevant /8 | Final /32 | Final+traseu | Final corect, traseu greșit | Greșit |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Copycat 07 epoca 1 | 7 | 5 | 4 | 6 | 22 | 19 | 3 | 10 |
| Copycat 08 epoca 1 | 6 | 3 | 4 | 5 | 18 | 12 | 6 | 14 |
| Copycat 09 epoca 1 | 6 | 5 | 5 | 4 | 20 | 19 | 1 | 12 |

## Comparație pe benchmarkurile vechi

| Model | Editare /36 | L05 /16 | L06 /24 | L07 /24 | L08 /32 |
|---|---:|---:|---:|---:|---:|
| Copycat 07 epoca 1 | 36 | 8 | 14 | 17 | 17 |
| Copycat 08 epoca 1 | 36 | 10 | 10 | 17 | 19 |
| Copycat 09 epoca 1 | 36 | 8 | 14 | 18 | 13 |

## Toate erorile Copycat 09

### lectia_05

#### A1 — altă eroare

**Rezultat:** răspuns greșit

**Prompt:** În «Luca i-a spus lui Matei că tatăl lui pleacă mâine», al cui tată pleacă?

**Răspuns:**  
Tatăl lui Luca pleacă. Pronumele masculin «lui» se referă la Luca.

**Gold:**  
Poate fi tatăl lui Luca sau al lui Matei; enunțul nu decide.

#### A2 — altă eroare

**Rezultat:** răspuns greșit

**Prompt:** În «Am urmărit femeia cu camera video», cine avea camera video?

**Răspuns:**  
Camera video era a lui. «Am» este un pronume masculin singular.

**Gold:**  
Poate fi persoana care urmărea sau femeia urmărită; contextul lipsește.

#### A3 — altă eroare

**Rezultat:** răspuns greșit

**Prompt:** În «Bianca a văzut-o pe Sorina când ieșea din bibliotecă», cine ieșea?

**Răspuns:**  
Sorina ieșea din bibliotecă. Bianca o vedea pe Sorina, deci nu ea ieșea.

**Gold:**  
Poate fi Bianca sau Sorina; propoziția nu lămurește.

#### A4 — altă eroare

**Rezultat:** răspuns greșit

**Prompt:** În «Mara a vorbit cu Dana despre planul ei», al cui era planul?

**Răspuns:**  
Planul era al Mara. Articolul feminin «ea» o identifică pe Mara.

**Gold:**  
Poate fi planul Marei sau al Danei; nu putem stabili fără context.

#### I2 — altă eroare

**Rezultat:** răspuns greșit

**Prompt:** Ce înseamnă «a tăia frunză la câini» în vorbirea de zi cu zi?

**Răspuns:**  
Nu pot determina sensul acestui idiom din informațiile date.

**Gold:**  
Înseamnă să pierzi vremea fără să faci ceva util.

#### I3 — altă eroare

**Rezultat:** răspuns greșit

**Prompt:** Ce înseamnă «a da bir cu fugiții»?

**Răspuns:**  
Nu pot determina sensul acestui idiom din informațiile date.

**Gold:**  
Înseamnă să fugi sau să te retragi când apare o obligație ori o dificultate.

#### I4 — altă eroare

**Rezultat:** răspuns greșit

**Prompt:** Ce înseamnă «a se culca pe o ureche» într-o discuție despre muncă?

**Răspuns:**  
Nu se poate determina sensul din această expresie.

**Gold:**  
Înseamnă să te relaxezi prea devreme și să nu mai fii atent sau să nu mai faci efort.

#### T4 — altă eroare

**Rezultat:** răspuns greșit

**Prompt:** Rescrie ca mesaj firesc către un coleg, fără să pierzi informația: «Nu pot participa la apelul de azi de la 14:30; vă propun mâine la 10:00». Răspunde doar cu mesajul.

**Răspuns:**  
Nu pot participa la apelul de azi de la 14:30; mă propun mâine la 10:00.

**Gold:**  
Nu pot intra în apelul de azi de la 14:30. Putem vorbi mâine la 10:00?

### lectia_06

#### RA1 — altă eroare

**Rezultat:** răspuns greșit

**Prompt:** Nicoleta a întâlnit-o pe Adina după ce ea a terminat programul. Cine a terminat programul?

**Răspuns:**  
Adina a terminat programul. Concordanța masculină o elimină pe Nicoleta.

**Gold:**  
Poate fi Nicoleta sau Adina; pronumele nu decide.

#### RA3 — altă eroare

**Rezultat:** răspuns greșit

**Prompt:** Am descris paznicul cu lanterna. Cine poate avea lanterna?

**Răspuns:**  
Lanterna poate aparține paznicului descris. Nu există alt sens gramatical.

**Gold:**  
Lanterna poate fi instrumentul vorbitorului sau un obiect purtat de paznic.

#### RA4 — altă eroare

**Rezultat:** răspuns greșit

**Prompt:** Anunțul este pentru bibliotecari și arhivari cu experiență. Cui i se poate cere experiență?

**Răspuns:**  
Experiența se poate cere bibliotecarilor sau arhivarilor. Ambii sunt marcați de «și», deci ambele lecturi sunt gramaticale.

**Gold:**  
Doar arhivarilor sau ambelor grupuri.

#### RA8 — altă eroare

**Rezultat:** răspuns greșit

**Prompt:** Au sosit cercetătorii și tehnicienii acreditați. Cine poate fi acreditat?

**Răspuns:**  
Poate fi cercetătorul sau tehnicianul. Marcajul «acreditat» nu elimină niciunul dintre ei.

**Gold:**  
Numai tehnicienii sau ambele grupuri.

#### NA2 — altă eroare

**Rezultat:** răspuns greșit

**Prompt:** Pe bancă erau o geantă și două dosare. Le-am ridicat. Ce am ridicat?

**Răspuns:**  
Am ridicat geanta și două dosare. Toate cele trei obiecte sunt ridicate, deci pluralul este necesar.

**Gold:**  
Cele două dosare, prin pronumele masculin plural.

#### NA7 — altă eroare

**Rezultat:** răspuns greșit

**Prompt:** Contabila i-a informat pe directori că erau așteptați în sală. Cine era așteptat?

**Răspuns:**  
Variante: contabila, directori.  
Indiciu: niciun indiciu suficient.  
Concluzie: ambiguu.

**Gold:**  
Directorii, prin acordul masculin plural.

#### CR1 — altă eroare

**Rezultat:** răspuns greșit

**Prompt:** «Geanta ei era deschisă.» Context: «Ada nu adusese nicio geantă; Lidia și-a pus geanta pe scaun.» A cui era geanta?

**Răspuns:**  
Variante: Ada, Lidia.  
Indiciu: contextul nu o identifică explicit; elimină ambele variante.  
Concluzie: ambiguu.

**Gold:**  
A Lidiei; contextul o exclude pe Ada.

#### CR2 — altă eroare

**Rezultat:** răspuns greșit

**Prompt:** «L-am luat de pe masă.» Context: «Acolo erau un măr și un caiet; mărul a rămas neatins.» Ce am luat?

**Răspuns:**  
Variante: mărul, caietul.  
Indiciu: Contextul nu elimină nicio variantă; ambele sunt la fel de plauzibile.  
Concluzie: ambiguu.

**Gold:**  
Caietul.

#### CR3 — altă eroare

**Rezultat:** răspuns greșit

**Prompt:** «Am urmărit alergătorul cu camera.» Context: «Alergătorul nu avea echipament; eu filmam cursa.» Cine avea camera?

**Răspuns:**  
Variante: eu, alergătorul.  
Indiciu: contextul nu elimină nicio variantă; ambiguu.  
Concluzie: ambiguu.

**Gold:**  
Vorbitorul, care filma.

#### CR4 — altă eroare

**Rezultat:** răspuns greșit

**Prompt:** «Ei i-a revenit premiul.» Context: «Dintre Paula și Dora, Paula fusese descalificată.» Cui i-a revenit premiul?

**Răspuns:**  
Contextul nu stabilește clar cui i-a revenit premiul. Indiciul suplimentar nu ajută la eliminarea uneia dintre opțiuni.

**Gold:**  
Dorei.

### lectia_07

#### I5 — altă eroare

**Rezultat:** răspuns greșit

**Prompt:** Pe peron așteptau trenurile spre Buzău și Ploiești. Am urcat într-unul. Ambele plecau la timp. În care?

**Răspuns:**  
În ambele. Textul nu decide între Buzău și Ploiești.

**Gold:**  
În oricare dintre cele două; punctualitatea nu decide.

#### I6 — altă eroare

**Rezultat:** răspuns greșit

**Prompt:** În dulap erau cămașa lui Eric și puloverul lui Filip. Am împachetat o haină. Ambele erau curate. Ce am împachetat?

**Răspuns:**  
Am împachetat haina. Contextul nu stabilește care haină era cea curată, așa că ambele sunt excluse.

**Gold:**  
Cămașa sau puloverul; faptul că erau curate nu decide.

#### M1 — altă eroare

**Rezultat:** răspuns greșit

**Prompt:** Pe masă erau o riglă, o foarfecă și o radieră. Rigla a rămas pe masă, iar foarfeca era încuiată în sertar. Ce am luat?

**Răspuns:**  
Am luat rigla. Textul o numește explicit, fără nicio ambiguitate.

**Gold:**  
Radiera; celelalte două sunt eliminate separat.

#### D1 — altă eroare

**Rezultat:** răspuns greșit

**Prompt:** Pe masă erau un stilou și un marker. Am folosit unul. Stiloul era albastru. Ce am folosit?

**Răspuns:**  
Am folosit stiloul albastru. Concurenții sunt stiloul și markerul, iar stiloul este eliminat de informația că era albastru.

**Gold:**  
Stiloul sau markerul; culoarea stiloului nu decide.

#### D3 — altă eroare

**Rezultat:** răspuns greșit

**Prompt:** În mapă erau certificatul și diploma. Am scanat un document. Diploma avea margine aurie. Ce am scanat?

**Răspuns:**  
Am scanat diploma. Certificatul nu are margine aurie, iar textul îl elimină.

**Gold:**  
Certificatul sau diploma; marginea nu decide.

#### D4 — altă eroare

**Rezultat:** răspuns greșit

**Prompt:** Două echipe puteau deschide evenimentul. Echipa Est avea tricouri verzi. Cine a deschis?

**Răspuns:**  
Variante: Echipa Est, oricare dintre echipe.  
Indiciu: niciun indiciu suficient.  
Concluzie: ambiguu.

**Gold:**  
Oricare dintre cele două echipe; culoarea nu este eliminatorie.

### lectia_08

#### F1B — altă eroare

**Rezultat:** răspuns greșit

**Prompt:** În dulap erau dosarul și agenda. Am scos un obiect. Dosarul apare apoi în fotografia dulapului închis. Ce variantă este corectă?

**Răspuns:**  
Variante:  
Indiciu: Dosarul este eliminat; apare în fotografie; nu este eliminat.  
Concluzie: nu este eliminat → eliminată.  
Motiv: eliminată elimină toate celelalte; nu este eliminat este eliminat.  
Concluzie: eliminată.  
Variante:  
Indiciu: Dosarul este eliminat; apare în fotografie; nu este eliminat.  
Concluzie: eliminată → eliminată.  
Motiv: eliminată elimină toate celelalte; apare în fotografie este eliminat.  
Concluzie: elimin

**Gold:**  
Variante: dosarul, agenda.  
Indiciu: Dosarul apare apoi în fotografia dulapului închis.; elimină dosarul.  
Concluzie: agenda.

#### F1C — altă eroare

**Rezultat:** răspuns greșit

**Prompt:** În dulap erau dosarul și agenda. Am scos un obiect. Agenda avea copertă maro. Ce variantă este corectă?

**Răspuns:**  
Variante:  
Indicativ: dosarul → eliminat; agenda → rămasă.  
Conjunctiv: dosarul → rămas; agenda → eliminată.  
Conjunctiv: dosarul → rămas; agenda → eliminată.  
Conjunctiv: dosarul → rămas; agenda → eliminată.  
Conjunctiv: dosarul → rămas; agenda → eliminată.  
Conjunctiv: dosarul → rămas; agenda → eliminată.  
Conjunctiv: dosarul → rămas; agenda → eliminată.  
Conjunctiv: dosarul → rămas; agenda → elim

**Gold:**  
Variante: dosarul, agenda.  
Indiciu: Agenda avea copertă maro.; nu elimină nicio variantă.  
Concluzie: ambiguu.

#### F1D — altă eroare

**Rezultat:** răspuns greșit

**Prompt:** Candidații sunt dosarul, agenda, mapa. Dosarul a rămas, iar agenda era pe biroul colegei. Ce variantă rămâne?

**Răspuns:**  
Variante: dosarul, agenda, mapa.  
Indiciu: Dosarul a rămas, iar agenda era pe biroul colegei.; elimină agenda.  
Concluzie: dosarul.

**Gold:**  
Variante: dosarul, agenda, mapa.  
Indiciu: Dosarul a rămas, iar agenda era pe biroul colegei.; elimină celelalte două variante.  
Concluzie: mapa.

#### F2B — altă eroare

**Rezultat:** răspuns greșit

**Prompt:** La ghișeu așteptau Rina și Sanda. Una a fost chemată. Sanda apare în filmare la ghișeu în timpul chemării. Ce variantă este corectă?

**Răspuns:**  
Sanda apare în filmare la ghișeu în timpul chemării.  
Indicată explicit de text.

**Gold:**  
Variante: Rina, Sanda.  
Indiciu: Sanda apare în filmare la ghișeu în timpul chemării.; elimină Sanda.  
Concluzie: Rina.

#### F2C — altă eroare

**Rezultat:** răspuns greșit

**Prompt:** La ghișeu așteptau Rina și Sanda. Una a fost chemată. Rina purta un fular. Ce variantă este corectă?

**Răspuns:**  
Variante: Rina; Sanda.  
Indiciu: Rina purta un fular.; elimină Rina.  
Concluzie: Sanda.

**Gold:**  
Variante: Rina, Sanda.  
Indiciu: Rina purta un fular.; nu elimină nicio variantă.  
Concluzie: ambiguu.

#### F3B — altă eroare

**Rezultat:** răspuns greșit

**Prompt:** Pe tavă erau ceaiul și sucul. A fost servită o băutură. Sucul este consemnat ca rămas pe tavă. Ce variantă este corectă?

**Răspuns:**  
Variante:  
Indicativ: ceaiul → eliminat; sucul → servit → rămas → consemnat → rămas.  
Subjonctiv: ceaiul → eliminat; sucul → servit → rămas → consemnat → eliminat.  
Concluzie: indicativ.

**Gold:**  
Variante: ceaiul, sucul.  
Indiciu: Sucul este consemnat ca rămas pe tavă.; elimină sucul.  
Concluzie: ceaiul.

#### F3C — altă eroare

**Rezultat:** răspuns greșit

**Prompt:** Pe tavă erau ceaiul și sucul. A fost servită o băutură. Ceaiul avea o felie de lămâie. Ce variantă este corectă?

**Răspuns:**  
Variante:  
Indiferent dacă era ceaiul sau sucul, avea o felie de lămâie;  
ceaiul avea o felie de lămâie, sucul era servit.  
Concluzie: indiferent dacă era ceaiul sau sucul, avea o felie de lămâie.

**Gold:**  
Variante: ceaiul, sucul.  
Indiciu: Ceaiul avea o felie de lămâie.; nu elimină nicio variantă.  
Concluzie: ambiguu.

#### F4B — altă eroare

**Rezultat:** răspuns greșit

**Prompt:** Marius i-a dat lui Nicu stiloul său. Nicu precizează că nu a avut niciodată stilou. Ce variantă este corectă?

**Răspuns:**  
Variante: Marius i-a dat lui Nicu stiloul. Nicu precizează că nu a avut niciodată stilou.  
Indiciu: Nicu precizează că nu a avut niciodată stilou; elimină prima variantă.  
Concluzie: Nicu precizează că nu a avut niciodată stilou.

**Gold:**  
Variante: Marius, Nicu.  
Indiciu: Nicu precizează că nu a avut niciodată stilou.; elimină Nicu.  
Concluzie: Marius.

#### F4C — altă eroare

**Rezultat:** răspuns greșit

**Prompt:** Marius i-a dat lui Nicu stiloul său. Marius este menționat primul. Ce variantă este corectă?

**Răspuns:**  
Variante: Marius i-a dat stiloul lui Nicu. /* */  
Indiciu: Marius este menționat primul; elimină varianta greșită.  
Concluzie: Marius i-a dat stiloul lui Nicu.

**Gold:**  
Variante: Marius, Nicu.  
Indiciu: Marius este menționat primul.; nu elimină nicio variantă.  
Concluzie: ambiguu.

#### F4D — altă eroare

**Rezultat:** răspuns greșit

**Prompt:** Candidații sunt Marius, Nicu, Ovidiu. Marius și-a retras obiectul, iar Nicu spune că stiloul este al lui Ovidiu. Ce variantă rămâne?

**Răspuns:**  
Variante: Marius, Nicu, Ovidiu.  
Indiciu: Nicu spune că stiloul este al lui Ovidiu; elimină Nicu și Ovidiu.  
Concluzie: Marius.

**Gold:**  
Variante: Marius, Nicu, Ovidiu.  
Indiciu: Marius și-a retras obiectul, iar Nicu spune că stiloul este al lui Ovidiu.; elimină celelalte două variante.  
Concluzie: Ovidiu.

#### F5A — altă eroare

**Rezultat:** răspuns greșit

**Prompt:** Două echipe puteau deschide ceremonia. Una a deschis. Ce variantă este corectă?

**Răspuns:**  
Variante:  
Individual: una a deschis → singulară; corectă.  
Grup: ambele au deschis → plural; greșită.  
  
Concluzie: singulară; una a deschis.

**Gold:**  
Variante: echipa Vest, echipa Centru.  
Indiciu: niciun indiciu suficient.  
Concluzie: ambiguu.

#### F5B — altă eroare

**Rezultat:** răspuns greșit

**Prompt:** Două echipe puteau deschide ceremonia. Una a deschis. Procesul-verbal spune că echipa Centru nu a urcat pe scenă. Ce variantă este corectă?

**Răspuns:**  
<echipa Centru> nu urcat pe scenă.  
Indiciu: Procesul-verbal spune că echipa Centru nu a urcat pe scenă.; elimină variantă.  
Final: <echipa Centru> nu urcat pe scenă.

**Gold:**  
Variante: echipa Vest, echipa Centru.  
Indiciu: Procesul-verbal spune că echipa Centru nu a urcat pe scenă.; elimină echipa Centru.  
Concluzie: echipa Vest.

#### F5C — altă eroare

**Rezultat:** răspuns greșit

**Prompt:** Două echipe puteau deschide ceremonia. Una a deschis. Echipa Vest avea uniforme albe. Ce variantă este corectă?

**Răspuns:**  
Echipa Vest avea uniforme albe.  
Indicație: niciuna suficientă.

**Gold:**  
Variante: echipa Vest, echipa Centru.  
Indiciu: Echipa Vest avea uniforme albe.; nu elimină nicio variantă.  
Concluzie: ambiguu.

#### F6B — altă eroare

**Rezultat:** răspuns greșit

**Prompt:** În gară erau trenul rapid și trenul personal. Am urcat într-unul. Trenul personal plecase înainte să ajung. Ce variantă este corectă?

**Răspuns:**  
Variante:  
Indicativ: trenul rapid.  
Contra-indicativ: trenul personal.  
Concluzie: indicativ.  
Motiv: am urcat în trenul rapid, deci nu poate fi trenul personal.

**Gold:**  
Variante: trenul rapid, trenul personal.  
Indiciu: Trenul personal plecase înainte să ajung.; elimină trenul personal.  
Concluzie: trenul rapid.

#### F6C — altă eroare

**Rezultat:** răspuns greșit

**Prompt:** În gară erau trenul rapid și trenul personal. Am urcat într-unul. Trenul rapid era vopsit recent. Ce variantă este corectă?

**Răspuns:**  
Variante:  
Indicativ: trenul rapid.  
Alternativ: trenul personal.  
Contra: vopsit recent; nu este relevant pentru alegere.  
Concluzie: indicativ.

**Gold:**  
Variante: trenul rapid, trenul personal.  
Indiciu: Trenul rapid era vopsit recent.; nu elimină nicio variantă.  
Concluzie: ambiguu.

#### F6D — altă eroare

**Rezultat:** răspuns greșit

**Prompt:** Candidații sunt rapid, personal, accelerat. Rapidul fusese anulat, iar personalul plecase. Ce variantă rămâne?

**Răspuns:**  
Variante: candidații sunt rapid, personal, accelerat; rapidul fusese anulat, iar personalul plecase.  
Indiciu: niciun indiciu suficient.  
Concluzie: ambiguu.

**Gold:**  
Variante: rapid, personal, accelerat.  
Indiciu: Rapidul fusese anulat, iar personalul plecase.; elimină celelalte două variante.  
Concluzie: accelerat.

#### F7C — altă eroare

**Rezultat:** răspuns greșit

**Prompt:** În mapă erau biletul roșu și biletul albastru. Am validat unul. Biletul roșu avea un colț îndoit. Ce variantă este corectă?

**Răspuns:**  
Variante:  
Indicativ: biletul roșu; eliminabil: niciuna.  
Contra: biletul albastru; eliminabil: știm că nu este cel validat.  
Concluzie: elimină eliminabilul și alege restul; știm că biletul roșu are un colț îndoit, deci este cel validat.

**Gold:**  
Variante: biletul roșu, biletul albastru.  
Indiciu: Biletul roșu avea un colț îndoit.; nu elimină nicio variantă.  
Concluzie: ambiguu.

#### F8A — altă eroare

**Rezultat:** răspuns greșit

**Prompt:** Luca și Matei depuseseră fiecare câte un proiect. Unul dintre proiecte a fost selectat. Ce variantă este corectă?

**Răspuns:**  
Variante:  
Luca și Matei au depus fiecare câte un proiect. → (1)  
Unul dintre proiecte a fost selectat; există două proiecte. → (0)  
  
Concluzie: (1)

**Gold:**  
Variante: proiectul lui Luca, proiectul lui Matei.  
Indiciu: niciun indiciu suficient.  
Concluzie: ambiguu.

#### F8C — altă eroare

**Rezultat:** răspuns greșit

**Prompt:** Luca și Matei depuseseră fiecare câte un proiect. Unul dintre proiecte a fost selectat. Luca vorbește primul. Ce variantă este corectă?

**Răspuns:**  
Variante:  
Luca: Am depus proiectul meu.  
Matei: Am depus proiectul meu.  
Final: Luca: Am depus proiectul meu.  
Motiv: Luca vorbește primul; propoziția lui este selectată.

**Gold:**  
Variante: proiectul lui Luca, proiectul lui Matei.  
Indiciu: Luca vorbește primul.; nu elimină nicio variantă.  
Concluzie: ambiguu.

### lectia_09

#### F1D3 — dovadă relevantă ignorată

**Rezultat:** răspuns final greșit

**Prompt:** Candidații sunt mapa de in, mapa de carton, mapa cu elastic, mapa transparentă. Procesul-verbal spune că mapa de carton nu a fost selectat. Procesul-verbal spune că mapa transparentă nu a fost selectat. Procesul-verbal spune că mapa de in nu a fost selectat. Urmărește eliminările în ordine și stabilește concluzia.

**Răspuns:**  
Candidați: mapa de in, mapa de carton, mapa cu elastic, mapa transparentă.  
Indiciu 1: Procesul-verbal spune că mapa de carton nu a fost selectat → elimină mapa de carton.  
Rămân: mapa de in, mapa cu elastic, mapa transparentă.  
Indiciu 2: Procesul-verbal spune că mapa transparentă nu a fost selectat → elimină mapa transparentă.  
Rămân: mapa de in, mapa cu elastic.  
Indiciu 3: niciun indiciu suplimentar, eliminările sunt epuizate → concluzie: ambiguu între mapa de in și mapa cu elastic.

**Gold:**  
Candidați: mapa de in, mapa de carton, mapa cu elastic, mapa transparentă.  
Indiciu 1: Procesul-verbal spune că mapa de carton nu a fost selectat → elimină mapa de carton.  
Rămân: mapa de in, mapa cu elastic, mapa transparentă.  
Indiciu 2: Procesul-verbal spune că mapa transparentă nu a fost selectat → elimină mapa transparentă.  
Rămân: mapa de in, mapa cu elastic.  
Indiciu 3: Procesul-verbal spune că mapa de in nu a fost selectat → elimină mapa de in.  
Rămâne: mapa cu elastic.  
Concluzie: mapa cu elastic.

#### F1AM — concluzia nu corespunde traseului

**Rezultat:** răspuns final greșit

**Prompt:** Candidații sunt mapa de in, mapa de carton, mapa cu elastic, mapa transparentă. Procesul-verbal spune că mapa de in nu a fost selectat. Procesul-verbal spune că mapa transparentă nu a fost selectat. Urmărește eliminările în ordine și stabilește concluzia.

**Răspuns:**  
Candidați: mapa de in, mapa de carton, mapa cu elastic, mapa transparentă.  
Indiciu: Procesul-verbal spune că mapa de in nu a fost selectat.  
Concluzie: mapa de in, .  
Indiciu: Procesul-verbal spune că mapa transparentă nu a fost selectat.  
Concluzie: , mapa transparentă.  
Combinată: mapa de in, .  
Răspuns: /*mapa de in*/.

**Gold:**  
Candidați: mapa de in, mapa de carton, mapa cu elastic, mapa transparentă.  
Indiciu 1: Procesul-verbal spune că mapa de in nu a fost selectat → elimină mapa de in.  
Rămân: mapa de carton, mapa cu elastic, mapa transparentă.  
Indiciu 2: Procesul-verbal spune că mapa transparentă nu a fost selectat → elimină mapa transparentă.  
Rămân: mapa de carton, mapa cu elastic.  
Nu există alt indiciu suficient.  
Concluzie: ambiguu între mapa de carton și mapa cu elastic.

#### F1IR — indiciu irelevant folosit

**Rezultat:** răspuns final greșit

**Prompt:** Candidații sunt mapa de in, mapa de carton, mapa cu elastic, mapa transparentă. Procesul-verbal spune că mapa cu elastic nu a fost selectat. mapa de in are un nume mai scurt. Procesul-verbal spune că mapa de carton nu a fost selectat. Procesul-verbal spune că mapa transparentă nu a fost selectat. Urmărește eliminările în ordine și stabilește concluzia.

**Răspuns:**  
Candidați: mapa de in, mapa de carton, mapa cu elastic, mapa transparentă.  
Indiciu 1: Procesul-verbal spune că mapa cu elastic nu a fost selectat → elimină mapa cu elastic.  
Rămân: mapa de in, mapa de carton, mapa transparentă.  
Indiciu 2: mapa de in are un nume mai scurt → nu elimină nimic.  
Rămân: mapa de carton, mapa transparentă.  
Indiciu 3: Procesul-verbal spune că mapa de carton nu a fost selectat → elimină mapa de carton.  
Rămâne: mapa transparentă.  
Concluzie: mapa transparentă.

**Gold:**  
Candidați: mapa de in, mapa de carton, mapa cu elastic, mapa transparentă.  
Indiciu 1: Procesul-verbal spune că mapa cu elastic nu a fost selectat → elimină mapa cu elastic.  
Rămân: mapa de in, mapa de carton, mapa transparentă.  
Indiciu 2: mapa de in are un nume mai scurt → nu elimină nimic.  
Rămân: mapa de in, mapa de carton, mapa transparentă.  
Indiciu 3: Procesul-verbal spune că mapa de carton nu a fost selectat → elimină mapa de carton.  
Rămân: mapa de in, mapa transparentă.  
Indiciu 4: Procesul-verbal spune că mapa transparentă nu a fost selectat → elimină mapa transparentă.  
Rămâne: mapa de in.  
Concluzie: mapa de in.

#### F3IR — indiciu irelevant folosit

**Rezultat:** răspuns final greșit

**Prompt:** Candidații sunt autobuzul 6, autobuzul 9, autobuzul 13, autobuzul 16. Textul precizează că autobuzul 13 a rămas neatins. autobuzul 6 apare într-o fotografie mai veche. Textul precizează că autobuzul 9 a rămas neatins. Textul precizează că autobuzul 16 a rămas neatins. Urmărește eliminările în ordine și stabilește concluzia.

**Răspuns:**  
Candidați: autobuzul 6, autobuzul 9, autobuzul 13, autobuzul 16.  
Indiciu 1: Textul precizează că autobuzul 13 a rămas neatins → elimină autobuzul 13.  
Rămân: autobuzul 6, autobuzul 9, autobuzul 16.  
Indiciu 2: autobuzul 6 apare într-o fotografie mai veche → nu elimină.  
Rămân: autobuzul 9, autobuzul 16.  
Indiciu 3: Textul precizează că autobuzul 9 a rămas neatins → elimină autobuzul 9.  
Rămâne: autobuzul 16.  
Concluzie: autobuzul 16.

**Gold:**  
Candidați: autobuzul 6, autobuzul 9, autobuzul 13, autobuzul 16.  
Indiciu 1: Textul precizează că autobuzul 13 a rămas neatins → elimină autobuzul 13.  
Rămân: autobuzul 6, autobuzul 9, autobuzul 16.  
Indiciu 2: autobuzul 6 apare într-o fotografie mai veche → nu elimină nimic.  
Rămân: autobuzul 6, autobuzul 9, autobuzul 16.  
Indiciu 3: Textul precizează că autobuzul 9 a rămas neatins → elimină autobuzul 9.  
Rămân: autobuzul 6, autobuzul 16.  
Indiciu 4: Textul precizează că autobuzul 16 a rămas neatins → elimină autobuzul 16.  
Rămâne: autobuzul 6.  
Concluzie: autobuzul 6.

#### F5IR — indiciu irelevant folosit

**Rezultat:** răspuns final greșit

**Prompt:** Candidații sunt oferta K, oferta M, oferta P, oferta R. Contextul spune explicit că oferta P era indisponibil. oferta K este menționat primul. Contextul spune explicit că oferta M era indisponibil. Contextul spune explicit că oferta R era indisponibil. Urmărește eliminările în ordine și stabilește concluzia.

**Răspuns:**  
Candidați: K, M, P, R.  
Indiciu: Contextul spune explicit că oferta P era indisponibil.; elimină P.  
Rămân: K, M, R.  
Indiciu: oferta K este menționat primul.; elimină K.  
Rămân: M, R.  
Indiciu: Contextul spune explicit că oferta R era indisponibil.; elimină R.  
Concluzie: M.

**Gold:**  
Candidați: oferta K, oferta M, oferta P, oferta R.  
Indiciu 1: Contextul spune explicit că oferta P era indisponibil → elimină oferta P.  
Rămân: oferta K, oferta M, oferta R.  
Indiciu 2: oferta K este menționat primul → nu elimină nimic.  
Rămân: oferta K, oferta M, oferta R.  
Indiciu 3: Contextul spune explicit că oferta M era indisponibil → elimină oferta M.  
Rămân: oferta K, oferta R.  
Indiciu 4: Contextul spune explicit că oferta R era indisponibil → elimină oferta R.  
Rămâne: oferta K.  
Concluzie: oferta K.

#### F6D2 — candidat inițial omis

**Rezultat:** răspuns final greșit

**Prompt:** Candidații sunt ușa A, ușa B, ușa C. Documentul confirmă că ușa A fusese deja eliminat. Documentul confirmă că ușa C fusese deja eliminat. Urmărește eliminările în ordine și stabilește concluzia.

**Răspuns:**  
Candidați: ușa B, ușa C.  
Indiciu: Documentul confirmă că ușa A fusese deja eliminat.; eliminările rămase sunt ușa B, ușa C.  
Concluzie: ușa B, ușa C.

**Gold:**  
Candidați: ușa A, ușa B, ușa C.  
Indiciu 1: Documentul confirmă că ușa A fusese deja eliminat → elimină ușa A.  
Rămân: ușa B, ușa C.  
Indiciu 2: Documentul confirmă că ușa C fusese deja eliminat → elimină ușa C.  
Rămâne: ușa B.  
Concluzie: ușa B.

#### F6D3 — concluzia nu corespunde traseului

**Rezultat:** răspuns final greșit

**Prompt:** Candidații sunt ușa A, ușa B, ușa C, ușa D. Documentul confirmă că ușa B fusese deja eliminat. Documentul confirmă că ușa D fusese deja eliminat. Documentul confirmă că ușa A fusese deja eliminat. Urmărește eliminările în ordine și stabilește concluzia.

**Răspuns:**  
Candidați: ușa A, ușa B, ușa C, ușa D.  
Indiciu: Documentul confirmă că ușa B fusese deja eliminat.  
Concluzie: ușa B eliminată; rămân 3 candidați.  
Indiciu: Documentul confirmă că ușa D fusese deja eliminat.  
Concluzie: ușa D eliminată; rămân 2 candidați.  
Indiciu: Documentul confirmă că ușa A fusese deja eliminat.  
Concluzie: ușa A eliminată; rămân 2 candidați.  
Concluzie finală: ușa A, ușa B sau ușa C.

**Gold:**  
Candidați: ușa A, ușa B, ușa C, ușa D.  
Indiciu 1: Documentul confirmă că ușa B fusese deja eliminat → elimină ușa B.  
Rămân: ușa A, ușa C, ușa D.  
Indiciu 2: Documentul confirmă că ușa D fusese deja eliminat → elimină ușa D.  
Rămân: ușa A, ușa C.  
Indiciu 3: Documentul confirmă că ușa A fusese deja eliminat → elimină ușa A.  
Rămâne: ușa C.  
Concluzie: ușa C.

#### F6AM — candidat inițial omis

**Rezultat:** răspuns final greșit

**Prompt:** Candidații sunt ușa A, ușa B, ușa C, ușa D. Documentul confirmă că ușa A fusese deja eliminat. Documentul confirmă că ușa D fusese deja eliminat. Urmărește eliminările în ordine și stabilește concluzia.

**Răspuns:**  
Candidați: ușa B, ușa C, ușa D.  
Indiciu: Documentul confirmă că ușa A fusese deja eliminat.; elimină ușa A.  
Concluzie: rămân 3 candidați.

**Gold:**  
Candidați: ușa A, ușa B, ușa C, ușa D.  
Indiciu 1: Documentul confirmă că ușa A fusese deja eliminat → elimină ușa A.  
Rămân: ușa B, ușa C, ușa D.  
Indiciu 2: Documentul confirmă că ușa D fusese deja eliminat → elimină ușa D.  
Rămân: ușa B, ușa C.  
Nu există alt indiciu suficient.  
Concluzie: ambiguu între ușa B și ușa C.

#### F7IR — indiciu irelevant folosit

**Rezultat:** răspuns final greșit

**Prompt:** Candidații sunt Sonia, Tania, Uliana, Vera. Nota temporală arată că Uliana plecase înainte de decizie. Sonia are un nume mai scurt. Nota temporală arată că Tania plecase înainte de decizie. Nota temporală arată că Vera plecase înainte de decizie. Urmărește eliminările în ordine și stabilește concluzia.

**Răspuns:**  
Candidați: Sonia, Tania, Uliana, Vera.  
Indiciu: Nota temporală arată că Uliana plecase înainte de decizie → elimină Uliana.  
Rămân: Sonia, Tania, Vera.  
Indiciu: Sonia are un nume mai scurt → elimină Sonia.  
Rămân: Tania, Vera.  
Indiciu: Nota temporală arată că Tania plecase înainte de decizie → elimină Tania.  
Rămâne: Vera.  
Concluzie: Vera.

**Gold:**  
Candidați: Sonia, Tania, Uliana, Vera.  
Indiciu 1: Nota temporală arată că Uliana plecase înainte de decizie → elimină Uliana.  
Rămân: Sonia, Tania, Vera.  
Indiciu 2: Sonia are un nume mai scurt → nu elimină nimic.  
Rămân: Sonia, Tania, Vera.  
Indiciu 3: Nota temporală arată că Tania plecase înainte de decizie → elimină Tania.  
Rămân: Sonia, Vera.  
Indiciu 4: Nota temporală arată că Vera plecase înainte de decizie → elimină Vera.  
Rămâne: Sonia.  
Concluzie: Sonia.

#### F8D2 — candidat inițial omis

**Rezultat:** răspuns final greșit

**Prompt:** Candidații sunt raportul lunar, nota internă, procesul-verbal. Posesia este atribuită explicit altui candidat, nu lui raportul lunar. Posesia este atribuită explicit altui candidat, nu lui procesul-verbal. Urmărește eliminările în ordine și stabilește concluzia.

**Răspuns:**  
Candidații sunt raportul lunar, nota internă. Posesia este atribuită explicit altui candidat, nu lui procesul-verbal.  
Indiciu: eliminările sunt marcate cu un punct.  
Concluzie: candidații sunt raportul lunar, nota internă.; procesul-verbal este eliminat.

**Gold:**  
Candidați: raportul lunar, nota internă, procesul-verbal.  
Indiciu 1: Posesia este atribuită explicit altui candidat, nu lui raportul lunar → elimină raportul lunar.  
Rămân: nota internă, procesul-verbal.  
Indiciu 2: Posesia este atribuită explicit altui candidat, nu lui procesul-verbal → elimină procesul-verbal.  
Rămâne: nota internă.  
Concluzie: nota internă.

#### F8D3 — oprire prea devreme

**Rezultat:** răspuns final greșit

**Prompt:** Candidații sunt raportul lunar, nota internă, procesul-verbal, inventarul. Posesia este atribuită explicit altui candidat, nu lui nota internă. Posesia este atribuită explicit altui candidat, nu lui inventarul. Posesia este atribuită explicit altui candidat, nu lui raportul lunar. Urmărește eliminările în ordine și stabilește concluzia.

**Răspuns:**  
Candidați: raportul lunar, nota internă, procesul-verbal, inventarul.  
Indiciu 1: Posesia este atribuită explicit altui candidat, nu lui nota internă → elimină nota internă.  
Rămân: raportul lunar, procesul-verbal, inventarul.  
Indiciu 2: Posesia este atribuită explicit altui candidat, nu lui inventarul → elimină inventarul.  
Rămân: raportul lunar, procesul-verbal.  
Concluzie: nu este stabilită o concluzie suficientă.

**Gold:**  
Candidați: raportul lunar, nota internă, procesul-verbal, inventarul.  
Indiciu 1: Posesia este atribuită explicit altui candidat, nu lui nota internă → elimină nota internă.  
Rămân: raportul lunar, procesul-verbal, inventarul.  
Indiciu 2: Posesia este atribuită explicit altui candidat, nu lui inventarul → elimină inventarul.  
Rămân: raportul lunar, procesul-verbal.  
Indiciu 3: Posesia este atribuită explicit altui candidat, nu lui raportul lunar → elimină raportul lunar.  
Rămâne: procesul-verbal.  
Concluzie: procesul-verbal.

#### F8AM — candidat eliminat reapare

**Rezultat:** răspuns final greșit

**Prompt:** Candidații sunt raportul lunar, nota internă, procesul-verbal, inventarul. Posesia este atribuită explicit altui candidat, nu lui raportul lunar. Posesia este atribuită explicit altui candidat, nu lui inventarul. Urmărește eliminările în ordine și stabilește concluzia.

**Răspuns:**  
Candidați: raportul lunar, nota internă, procesul-verbal, inventarul.  
Indiciu: Posesia este atribuită explicit altui candidat, nu lui raportul lunar.;  
Concluzie: nota internă sau procesul-verbal.  
Indiciu: Posesia este atribuită explicit altui candidat, nu lui inventarul.;  
Concluzie: raportul lunar, nota internă sau procesul-verbal.  
Concluzie finală: raportul lunar, nota internă sau procesul-verbal.

**Gold:**  
Candidați: raportul lunar, nota internă, procesul-verbal, inventarul.  
Indiciu 1: Posesia este atribuită explicit altui candidat, nu lui raportul lunar → elimină raportul lunar.  
Rămân: nota internă, procesul-verbal, inventarul.  
Indiciu 2: Posesia este atribuită explicit altui candidat, nu lui inventarul → elimină inventarul.  
Rămân: nota internă, procesul-verbal.  
Nu există alt indiciu suficient.  
Concluzie: ambiguu între nota internă și procesul-verbal.

#### F8IR — oprire prea devreme

**Rezultat:** răspuns final corect + traseu greșit

**Prompt:** Candidații sunt raportul lunar, nota internă, procesul-verbal, inventarul. Posesia este atribuită explicit altui candidat, nu lui procesul-verbal. raportul lunar este descris cu litere albastre. Posesia este atribuită explicit altui candidat, nu lui nota internă. Posesia este atribuită explicit altui candidat, nu lui inventarul. Urmărește eliminările în ordine și stabilește concluzia.

**Răspuns:**  
Candidați: raportul lunar, nota internă, procesul-verbal, inventarul.  
Indiciu 1: Posesia este atribuită explicit altui candidat, nu lui procesul-verbal → elimină procesul-verbal.  
Rămân: raportul lunar, nota internă, inventarul.  
Indiciu 2: raportul lunar este descris cu litere albastre → nu elimină nimic.  
Rămân: raportul lunar, nota internă, inventarul.  
Indiciu 3: Posesia este atribuită explicit altui candidat, nu lui nota internă → elimină nota internă.  
Rămân: raportul lunar, inventarul.  
Concluzie: raportul lunar.

**Gold:**  
Candidați: raportul lunar, nota internă, procesul-verbal, inventarul.  
Indiciu 1: Posesia este atribuită explicit altui candidat, nu lui procesul-verbal → elimină procesul-verbal.  
Rămân: raportul lunar, nota internă, inventarul.  
Indiciu 2: raportul lunar este descris cu litere albastre → nu elimină nimic.  
Rămân: raportul lunar, nota internă, inventarul.  
Indiciu 3: Posesia este atribuită explicit altui candidat, nu lui nota internă → elimină nota internă.  
Rămân: raportul lunar, inventarul.  
Indiciu 4: Posesia este atribuită explicit altui candidat, nu lui inventarul → elimină inventarul.  
Rămâne: raportul lunar.  
Concluzie: raportul lunar.

## Interpretare

- Față de Copycat 08, Lecția 09 recuperează eliminările secvențiale: pe categoriile 2+3 pași urcă de la 9/16 la 11/16, iar pe Lecția 07 eliminarea multiplă urcă de la 3/6 la 5/6.
- Nu depășește Copycat 07 pe verdictul final al benchmarkului 09: 20/32 față de 22/32. Ambele au 19/32 trasee complet corecte; Copycat 09 are mai puține răspunsuri corecte obținute prin traseu greșit.
- Câștigul Lecției 08 la prag nu se păstrează: benchmarkul 08 scade de la 19/32 la 13/32, în special la indicii irelevante și variante rezolvate.
- Modelul nu forțează sistematic un singur răspuns: păstrează corect ambiguitatea în 5/8 probe după eliminări. Totuși, indiciile irelevante rămân fragile, cu numai 4/8 verdicte finale și 3/8 trasee corecte.
- Nu au fost identificate exemple Gold sau benchmark 09 discutabile pentru un vorbitor nativ; toate eliminările sunt formulate explicit.
