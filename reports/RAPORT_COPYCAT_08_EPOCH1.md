# Raport Copycat 08 — epoca 1

## Configurația trainingului

- Pornire trainabilă: `copycat_07_epoch1_adapter`.
- O epocă, learning rate `3e-5`, seed 42.
- LoRA: r=8, alpha=16, dropout=0,05, `q_proj` și `v_proj`.
- 320 exemple: 104 Editare 04, 35 NOOP, 27 incertitudine, 30 Lecția 06, 30 Lecția 07 și 94 Gold 08 filtrate.
- 80 pași de optimizare; loss mediu: `0,3046272418`.

## Scoruri Copycat 08

- Editare 04: **36/36**.
- Lecția 05: **10/16** — {'ambiguitate': 2, 'idiom': 1, 'incertitudine': 4, 'ton': 3}.
- Lecția 06: **10/24** — {'ambiguitate_reala': 4, 'neambiguu': 2, 'context_rezolva': 0, 'trei_plus': 4}.
- Lecția 07: **17/24** — {'context_rezolva': 5, 'context_insuficient': 6, 'eliminare_multipla': 3, 'indiciu_irelevant': 3}.
- Lecția 08 oficial: **19/32** — {'ambiguu': 6, 'rezolvat': 4, 'indiciu_irelevant': 5, 'eliminare_multipla': 4}.
- Lecția 08 diagnostic, fără F2B, F4B și F5B: **18/29**.

## Comparație

| Model | Editare /36 | L05 /16 | L06 /24 | L07 /24 | L08 /32 |
|---|---:|---:|---:|---:|---:|
| Copycat 05B epoca 2 | 36 | 7 | 16 | 15 | 13 |
| Copycat 06 epoca 1 | 36 | 5 | 15 | 16 | 10 |
| Copycat 07 epoca 1 | 36 | 8 | 14 | 17 | 17 |
| Copycat 08 epoca 1 | 36 | 10 | 10 | 17 | 19 |

## Triplete A/B/C

Familii cu toate cele trei stări corecte: **3/8** — F2, F3, F8.

- F1: A=✓, B=✗, C=✓.
- F2: A=✓, B=✓, C=✓.
- F3: A=✓, B=✓, C=✓.
- F4: A=✗, B=✗, C=✗.
- F5: A=✗, B=✗, C=✗.
- F6: A=✓, B=✗, C=✓.
- F7: A=✓, B=✓, C=✗.
- F8: A=✓, B=✓, C=✓.

## Toate răspunsurile greșite

### lectia_05

#### A3 — certitudine prematură

**Prompt:** În «Bianca a văzut-o pe Sorina când ieșea din bibliotecă», cine ieșea?

**Răspuns:**  
Verbul «ieșea» se acordă cu subiectul feminin Sorina. Bianca este eliminată.

**Gold:**  
Poate fi Bianca sau Sorina; propoziția nu lămurește.

#### A4 — certitudine prematură

**Prompt:** În «Mara a vorbit cu Dana despre planul ei», al cui era planul?

**Răspuns:**  
Planul este al lui Mara. Dana este o persoană distinctă, iar planul nu poate fi al ei.

**Gold:**  
Poate fi planul Marei sau al Danei; nu putem stabili fără context.

#### I2 — altă eroare

**Prompt:** Ce înseamnă «a tăia frunză la câini» în vorbirea de zi cu zi?

**Răspuns:**  
Nu pot determina sensul acestui idiom din informațiile date.

**Gold:**  
Înseamnă să pierzi vremea fără să faci ceva util.

#### I3 — altă eroare

**Prompt:** Ce înseamnă «a da bir cu fugiții»?

**Răspuns:**  
Nu pot determina sensul acestui idiom din informațiile date.

**Gold:**  
Înseamnă să fugi sau să te retragi când apare o obligație ori o dificultate.

#### I4 — altă eroare

**Prompt:** Ce înseamnă «a se culca pe o ureche» într-o discuție despre muncă?

**Răspuns:**  
Nu pot determina sensul acestui idiom din contextul dat.

**Gold:**  
Înseamnă să te relaxezi prea devreme și să nu mai fii atent sau să nu mai faci efort.

#### T4 — altă eroare

**Prompt:** Rescrie ca mesaj firesc către un coleg, fără să pierzi informația: «Nu pot participa la apelul de azi de la 14:30; vă propun mâine la 10:00». Răspunde doar cu mesajul.

**Răspuns:**  
Nu pot participa la apelul de azi de la 14:30; mă propun mâine la 10:00.

**Gold:**  
Nu pot intra în apelul de azi de la 14:30. Putem vorbi mâine la 10:00?

### lectia_06

#### RA3 — candidat valid omis

**Prompt:** Am descris paznicul cu lanterna. Cine poate avea lanterna?

**Răspuns:**  
Variante: paznicul, lanterna.  
Indiciu: niciun indiciu suficient.  
Concluzie: ambiguu.

**Gold:**  
Lanterna poate fi instrumentul vorbitorului sau un obiect purtat de paznic.

#### RA4 — candidat valid omis

**Prompt:** Anunțul este pentru bibliotecari și arhivari cu experiență. Cui i se poate cere experiență?

**Răspuns:**  
Variante: bibliotecari, arhivari.  
Indiciu: niciun indiciu suficient.  
Concluzie: ambiguu.

**Gold:**  
Doar arhivarilor sau ambelor grupuri.

#### RA6 — concluzia nu rezultă din propriile variante și dovezi

**Prompt:** Am găsit portretul profesorului din hol. Cine sau ce poate fi în hol?

**Răspuns:**  
Holul poate fi un loc sau un obiect. Portretul poate fi un portret fizic sau un portret figurativ. Profesorul poate fi un profesor uman sau un substantiv care se referă la profesor.  
Indicii: portretul, profesorul, holul.  
Variante: portret fizic, portret figurativ, hol, profesor uman, substantiv care se referă la profesor.  
Concluzie: portretul fizic, holul, profesorul uman.

**Gold:**  
Profesorul poate fi din hol în scena portretului sau portretul poate fi amplasat în hol.

#### RA8 — candidat valid omis

**Prompt:** Au sosit cercetătorii și tehnicienii acreditați. Cine poate fi acreditat?

**Răspuns:**  
Variante: cercetătorii, tehnicienii.  
Indiciu: niciun indiciu suficient.  
Concluzie: ambiguu.

**Gold:**  
Numai tehnicienii sau ambele grupuri.

#### NA1 — incertitudine păstrată prea mult

**Prompt:** Teodora i-a spus lui Mihai că este pregătită. Cine este pregătită?

**Răspuns:**  
Variante: Teodora, Mihai.  
Indiciu: niciun indiciu suficient.  
Concluzie: ambiguu.

**Gold:**  
Teodora, datorită acordului feminin.

#### NA2 — incertitudine păstrată prea mult

**Prompt:** Pe bancă erau o geantă și două dosare. Le-am ridicat. Ce am ridicat?

**Răspuns:**  
Variante: geanta, dosarele.  
Indiciu: niciun indiciu suficient.  
Concluzie: ambiguu.

**Gold:**  
Cele două dosare, prin pronumele masculin plural.

#### NA3 — incertitudine păstrată prea mult

**Prompt:** Miruna a pus pachetul în cutia aflată sub birou. Ce se află sub birou?

**Răspuns:**  
Variante: pachetul, biroul.  
Indiciu: niciun indiciu suficient.  
Concluzie: ambiguu.

**Gold:**  
Cutia.

#### NA5 — incertitudine păstrată prea mult

**Prompt:** Fetele au întâlnit paznicul când alergau. Cine alerga?

**Răspuns:**  
Variante: fetele, paznicul.  
Indiciu: niciun indiciu suficient.  
Concluzie: ambiguu.

**Gold:**  
Fetele, datorită verbului la plural.

#### NA6 — incertitudine păstrată prea mult

**Prompt:** Am cumpărat roșii coapte și un pepene verde. Ce este verde?

**Răspuns:**  
Variante: pepene, roșu.  
Indiciu: niciun indiciu suficient.  
Concluzie: ambiguu.

**Gold:**  
Pepenele.

#### NA7 — incertitudine păstrată prea mult

**Prompt:** Contabila i-a informat pe directori că erau așteptați în sală. Cine era așteptat?

**Răspuns:**  
Variante: contabila, directori.  
Indiciu: niciun indiciu suficient.  
Concluzie: ambiguu.

**Gold:**  
Directorii, prin acordul masculin plural.

#### CR1 — indiciu relevant ignorat

**Prompt:** «Geanta ei era deschisă.» Context: «Ada nu adusese nicio geantă; Lidia și-a pus geanta pe scaun.» A cui era geanta?

**Răspuns:**  
Contextul nu o identifică explicit pe Ada sau pe Lidia. Pronumele feminin singular «ei» ar putea indica oricare dintre ele.

**Gold:**  
A Lidiei; contextul o exclude pe Ada.

#### CR2 — indiciu relevant ignorat

**Prompt:** «L-am luat de pe masă.» Context: «Acolo erau un măr și un caiet; mărul a rămas neatins.» Ce am luat?

**Răspuns:**  
Variante: mărul, caietul.  
Indiciu: niciun indiciu suficient.  
Concluzie: ambiguu.

**Gold:**  
Caietul.

#### CR3 — indiciu relevant ignorat

**Prompt:** «Am urmărit alergătorul cu camera.» Context: «Alergătorul nu avea echipament; eu filmam cursa.» Cine avea camera?

**Răspuns:**  
Contextul nu stabilește cine avea camera. Propoziția o atribuie alergătorului, dar contextul o atribuie vorbitorului. Ambiguitatea nu poate fi rezolvată.

**Gold:**  
Vorbitorul, care filma.

#### CR4 — indiciu relevant ignorat

**Prompt:** «Ei i-a revenit premiul.» Context: «Dintre Paula și Dora, Paula fusese descalificată.» Cui i-a revenit premiul?

**Răspuns:**  
Variante: Paula, Dora.  
Indiciu: niciun indiciu.  
Concluzie: ambiguu.

**Gold:**  
Dorei.

### lectia_07

#### R6 — candidat invalid păstrat

**Prompt:** În finală ajunseseră Raluca și Silvia. Raluca fusese eliminată pentru abatere de la regulament. Cine a rămas în concurs?

**Răspuns:**  
Variante: Raluca, Silvia.  
Indiciu: Raluca fusese eliminată; eliminarea o elimină.  
Concluzie: Raluca.

**Gold:**  
Silvia; eliminarea Ralucăi oferă răspuns unic.

#### R7 — indiciu relevant ignorat

**Prompt:** În sertar erau pașaportul și permisul. Am scos unul. Pașaportul apare apoi în fotografia sertarului închis. Ce am scos?

**Răspuns:**  
Variante: pașaportul, permisul.  
Indiciu: pașaportul apare apoi în fotografia sertarului închis; elimină permisul.  
Concluzie: pașaportul.

**Gold:**  
Permisul; prezența pașaportului în sertar îl exclude.

#### R8 — incertitudine păstrată prea mult

**Prompt:** Două becuri puteau lumina holul. Becul din stânga era ars. Care putea fi aprins?

**Răspuns:**  
Variante: becul din dreapta, becul rămas.  
Indiciu: niciun indiciu suficient.  
Concluzie: ambiguu.

**Gold:**  
Becul din dreapta; cel ars este exclus.

#### M1 — indiciu relevant ignorat

**Prompt:** Pe masă erau o riglă, o foarfecă și o radieră. Rigla a rămas pe masă, iar foarfeca era încuiată în sertar. Ce am luat?

**Răspuns:**  
Variante: rigla, foarfeca, radiera.  
Indiciu: rigla a rămas pe masă; nu elimină nicio variantă.  
Concluzie: ambiguu.

**Gold:**  
Radiera; celelalte două sunt eliminate separat.

#### M3 — indiciu relevant ignorat

**Prompt:** Puteam trimite mesajul prin e-mail, fax sau curier. Internetul nu funcționa, iar faxul nu avea hârtie. Ce variantă rămânea?

**Răspuns:**  
Variante: e-mail, fax, curier.  
Indiciu: Internetul nu funcționa, iar faxul nu avea hârtie.  
Concluzie: e-mail.

**Gold:**  
Curierul; e-mailul și faxul sunt eliminate.

#### M5 — concluzia nu rezultă din propriile variante și dovezi

**Prompt:** La licitație participau firma A, firma B și firma C. A și-a retras oferta, iar B nu depusese garanția obligatorie. Cine mai era eligibil?

**Răspuns:**  
Variante: A, B, C.  
Indiciu: A și-a retras oferta; B nu depusese garanția obligatorie.  
Concluzie: A.

**Gold:**  
Firma C; retragerea și lipsa garanției elimină A și B.

#### D4 — candidat valid omis

**Prompt:** Două echipe puteau deschide evenimentul. Echipa Est avea tricouri verzi. Cine a deschis?

**Răspuns:**  
Variante: Est, Est (tricouri verzi), Est (tricouri).  
Indiciu: niciun indiciu suficient.  
Concluzie: ambiguu.

**Gold:**  
Oricare dintre cele două echipe; culoarea nu este eliminatorie.

### lectia_08

#### F1B — indiciu relevant ignorat

**Prompt:** În dulap erau dosarul și agenda. Am scos un obiect. Dosarul apare apoi în fotografia dulapului închis. Ce variantă este corectă?

**Răspuns:**  
Variante: dosarul, agenda.  
Indiciu: dosarul apare apoi în fotografia dulapului închis; nu elimină nicio variantă.  
Concluzie: ambiguu.

**Gold:**  
Variante: dosarul, agenda.  
Indiciu: Dosarul apare apoi în fotografia dulapului închis.; elimină dosarul.  
Concluzie: agenda.

#### F1D — candidat invalid păstrat

**Prompt:** Candidații sunt dosarul, agenda, mapa. Dosarul a rămas, iar agenda era pe biroul colegei. Ce variantă rămâne?

**Răspuns:**  
Variante: dosarul, agenda, mapa.  
Indiciu: dosarul a rămas, iar agenda era pe biroul colegei.  
Concluzie: dosarul.

**Gold:**  
Variante: dosarul, agenda, mapa.  
Indiciu: Dosarul a rămas, iar agenda era pe biroul colegei.; elimină celelalte două variante.  
Concluzie: mapa.

#### F3D — concluzia nu rezultă din propriile variante și dovezi

**Prompt:** Candidații sunt ceaiul, sucul, apa. Ceaiul nu fusese comandat, iar sucul era epuizat. Ce variantă rămâne?

**Răspuns:**  
Variante: ceaiul, sucul, apa.  
Indiciu: ceaiul nu fusese comandat, iar sucul era epuizat.  
Concluzie: ceaiul.

**Gold:**  
Variante: ceaiul, sucul, apa.  
Indiciu: Ceaiul nu fusese comandat, iar sucul era epuizat.; elimină celelalte două variante.  
Concluzie: apa.

#### F4A — certitudine prematură

**Prompt:** Marius i-a dat lui Nicu stiloul său. Ce variantă este corectă?

**Răspuns:**  
Variante: Marius i-a dat stiloul. Nicu i-a primit stiloul.  
Indiciu: Marius i-a dat lui Nicu stiloul său; elimină «Marius i-a dat» și «său».  
Concluzie: Nicu i-a primit stiloul.

**Gold:**  
Variante: Marius, Nicu.  
Indiciu: niciun indiciu suficient.  
Concluzie: ambiguu.

#### F4B — concluzia nu rezultă din propriile variante și dovezi

**Prompt:** Marius i-a dat lui Nicu stiloul său. Nicu precizează că nu a avut niciodată stilou. Ce variantă este corectă?

**Răspuns:**  
Variante: Marius i-a dat stiloul. Nicu precizează că nu a avut niciodată stiloul.  
Indiciu: Nicu precizează că nu a avut niciodată stiloul; elimină variantă.  
Concluzie: Marius i-a dat stiloul.

**Gold:**  
Variante: Marius, Nicu.  
Indiciu: Nicu precizează că nu a avut niciodată stilou.; elimină Nicu.  
Concluzie: Marius.

#### F4C — indiciu irelevant folosit

**Prompt:** Marius i-a dat lui Nicu stiloul său. Marius este menționat primul. Ce variantă este corectă?

**Răspuns:**  
Variante: Marius i-a dat . Nicu stiloul său .  
Indiciu: Marius este menționat primul; elimină «Marius i-a dat» și alege «Nicu stiloul său» .  
Concluzie: Nicu stiloul său .

**Gold:**  
Variante: Marius, Nicu.  
Indiciu: Marius este menționat primul.; nu elimină nicio variantă.  
Concluzie: ambiguu.

#### F4D — concluzia nu rezultă din propriile variante și dovezi

**Prompt:** Candidații sunt Marius, Nicu, Ovidiu. Marius și-a retras obiectul, iar Nicu spune că stiloul este al lui Ovidiu. Ce variantă rămâne?

**Răspuns:**  
Variante: Marius, Nicu, Ovidiu.  
Indiciu: Marius și-a retras obiectul; Nicu spune că stiloul este al lui Ovidiu.  
Concluzie: Marius.

**Gold:**  
Variante: Marius, Nicu, Ovidiu.  
Indiciu: Marius și-a retras obiectul, iar Nicu spune că stiloul este al lui Ovidiu.; elimină celelalte două variante.  
Concluzie: Ovidiu.

#### F5A — candidat valid omis

**Prompt:** Două echipe puteau deschide ceremonia. Una a deschis. Ce variantă este corectă?

**Răspuns:**  
Variante: una, ambele.  
Indiciu: niciun indiciu suficient.  
Concluzie: ambiguu.

**Gold:**  
Variante: echipa Vest, echipa Centru.  
Indiciu: niciun indiciu suficient.  
Concluzie: ambiguu.

#### F5B — candidat invalid păstrat

**Prompt:** Două echipe puteau deschide ceremonia. Una a deschis. Procesul-verbal spune că echipa Centru nu a urcat pe scenă. Ce variantă este corectă?

**Răspuns:**  
Variante: echipa Centru, echipa A.  
Indiciu: procesul-verbal spune că echipa Centru nu a urcat pe scenă; elimină echipa Centru.  
Concluzie: echipa A.

**Gold:**  
Variante: echipa Vest, echipa Centru.  
Indiciu: Procesul-verbal spune că echipa Centru nu a urcat pe scenă.; elimină echipa Centru.  
Concluzie: echipa Vest.

#### F5C — candidat valid omis

**Prompt:** Două echipe puteau deschide ceremonia. Una a deschis. Echipa Vest avea uniforme albe. Ce variantă este corectă?

**Răspuns:**  
Variante: Vest, niciuna.  
Indiciu: niciun indiciu suficient.  
Concluzie: ambiguu.

**Gold:**  
Variante: echipa Vest, echipa Centru.  
Indiciu: Echipa Vest avea uniforme albe.; nu elimină nicio variantă.  
Concluzie: ambiguu.

#### F5D — concluzia nu rezultă din propriile variante și dovezi

**Prompt:** Candidații sunt Vest, Centru, Nord. Vest s-a retras, iar Centru a fost descalificată. Ce variantă rămâne?

**Răspuns:**  
Variante: Vest, Centru, Nord.  
Indiciu: Vest s-a retras, iar Centru a fost descalificată.  
Concluzie: Vest.

**Gold:**  
Variante: Vest, Centru, Nord.  
Indiciu: Vest s-a retras, iar Centru a fost descalificată.; elimină celelalte două variante.  
Concluzie: Nord.

#### F6B — indiciu relevant ignorat

**Prompt:** În gară erau trenul rapid și trenul personal. Am urcat într-unul. Trenul personal plecase înainte să ajung. Ce variantă este corectă?

**Răspuns:**  
Variante:  
Indicativ: trenul rapid.  
Subjunctiv: trenul personal.  
Variante: am urcat în trenul rapid; am urcat în trenul personal.  
Variante: plecase înainte să ajung; plecase înainte să ajung.  
Variante: indiciu; subjunctiv.  
Variante: indicativ; subjunctiv.  
Variante: am urcat în trenul rapid; am urcat în trenul personal.  
Variante: plecase înainte să ajung; plecase înainte să ajung.  
Variante: indicativ; subjunctiv.  
Variante: am urcat în trenul rapid; am urcat în trenul personal.

**Gold:**  
Variante: trenul rapid, trenul personal.  
Indiciu: Trenul personal plecase înainte să ajung.; elimină trenul personal.  
Concluzie: trenul rapid.

#### F7C — indiciu irelevant folosit

**Prompt:** În mapă erau biletul roșu și biletul albastru. Am validat unul. Biletul roșu avea un colț îndoit. Ce variantă este corectă?

**Răspuns:**  
Variante: biletul roșu, biletul albastru.  
Indiciu: Biletul roșu avea un colț îndoit.  
Concluzie: biletul roșu.

**Gold:**  
Variante: biletul roșu, biletul albastru.  
Indiciu: Biletul roșu avea un colț îndoit.; nu elimină nicio variantă.  
Concluzie: ambiguu.

## Răspunsuri discutabile

- **F2B:** Gold-ul presupune că prezența Sandei la ghișeu în timpul chemării o exclude; chemarea ar putea avea loc chiar la ghișeu. Este corect în scorul oficial, dar exclus din diagnosticul cerut.
- **F4B:** „nu a avut niciodată stilou” poate descrie perioada de dinaintea primirii. Răspunsul modelului formulează acțiunea, nu posesia. Este marcat greșit și exclus din diagnosticul cerut.
- **F5B:** lipsa urcării pe scenă nu exclude logic deschiderea ceremoniei din alt loc; modelul inventează candidatul „echipa A”. Este marcat greșit și exclus din diagnostic.
- **F5A/F5C:** modelul declară ambiguitatea, dar omite candidații reali și îi înlocuiește cu „una/ambele”, respectiv „Vest/niciuna”. Sunt marcate greșit în evaluarea strictă.
- **R4, R6 și D3 din benchmarkul 07** rămân probele marcate anterior pentru revizuire umană; benchmarkul nu a fost modificat.

## Pierderi și câștiguri

- Lecția 08 crește de la 17/32 la 19/32 și urcă simultan la ambiguu (3→6) și rezolvat (3→4).
- Indiciile irelevante cresc de la 4/8 la 5/8; erorile explicite rămân F4C și F7C.
- Tripletele complete cresc de la 0/8 la 3/8.
- Editarea rămâne 36/36. Lecția 05 crește 8→10, Lecția 06 scade 14→10, Lecția 07 rămâne 17/24.
- Regresia principală este hiperprudența pe cazurile neambigue/contextuale din Lecția 06 și eliminarea greșită în mai mulți pași. Aceste erori sunt reparabile prin replay țintit, fără a schimba benchmarkurile.
