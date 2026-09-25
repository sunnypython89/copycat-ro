# Raport pre-training — Lecția 08

Rubrică: verdictul trebuie să fie semantic corect și să nu contrazică indiciul. Repetarea enunțului fără verdict nu primește punct.

## Scoruri

| Model | Ambiguu /8 | Rezolvat /8 | Indiciu irelevant /8 | Eliminare multiplă /8 | Total /32 |
|---|---:|---:|---:|---:|---:|
| Copycat 05B epoca 2 | 3 | 2 | 1 | 7 | 13 |
| Copycat 06 epoca 1 | 3 | 1 | 0 | 6 | 10 |
| Copycat 07 epoca 1 | 3 | 3 | 4 | 7 | 17 |

## Toate răspunsurile greșite

### Copycat 05B epoca 2

#### F1B — contradicție între candidați, indiciu și concluzie

**Prompt:** În dulap erau dosarul și agenda. Am scos un obiect. Dosarul apare apoi în fotografia dulapului închis. Ce variantă este corectă?

**Răspuns brut:** Am scos dosarul. Am scos agenda. Am scos un obiect.

**Gold:**  
Variante: dosarul, agenda.  
Indiciu: Dosarul apare apoi în fotografia dulapului închis.; elimină dosarul.  
Concluzie: agenda.

#### F1C — contradicție între candidați, indiciu și concluzie

**Prompt:** În dulap erau dosarul și agenda. Am scos un obiect. Agenda avea copertă maro. Ce variantă este corectă?

**Răspuns brut:** Am scos agenda. Am scos dosarul.

**Gold:**  
Variante: dosarul, agenda.  
Indiciu: Agenda avea copertă maro.; nu elimină nicio variantă.  
Concluzie: ambiguu.

#### F1D — candidat invalid păstrat

**Prompt:** Candidații sunt dosarul, agenda, mapa. Dosarul a rămas, iar agenda era pe biroul colegei. Ce variantă rămâne?

**Răspuns brut:** Dosarul rămâne, iar agenda era pe biroul colegei.

**Gold:**  
Variante: dosarul, agenda, mapa.  
Indiciu: Dosarul a rămas, iar agenda era pe biroul colegei.; elimină celelalte două variante.  
Concluzie: mapa.

#### F2A — certitudine prematură

**Prompt:** La ghișeu așteptau Rina și Sanda. Una a fost chemată. Ce variantă este corectă?

**Răspuns brut:** Rina a fost chemată.

**Gold:**  
Variante: Rina, Sanda.  
Indiciu: niciun indiciu suficient.  
Concluzie: ambiguu.

#### F2C — indiciu irelevant folosit

**Prompt:** La ghișeu așteptau Rina și Sanda. Una a fost chemată. Rina purta un fular. Ce variantă este corectă?

**Răspuns brut:** Rina a fost chemată. Sanda așteaptă.

**Gold:**  
Variante: Rina, Sanda.  
Indiciu: Rina purta un fular.; nu elimină nicio variantă.  
Concluzie: ambiguu.

#### F3B — indiciu relevant ignorat

**Prompt:** Pe tavă erau ceaiul și sucul. A fost servită o băutură. Sucul este consemnat ca rămas pe tavă. Ce variantă este corectă?

**Răspuns brut:** A fost servită o băutură din ceai sau din suc.

**Gold:**  
Variante: ceaiul, sucul.  
Indiciu: Sucul este consemnat ca rămas pe tavă.; elimină sucul.  
Concluzie: ceaiul.

#### F4A — candidat valid omis

**Prompt:** Marius i-a dat lui Nicu stiloul său. Ce variantă este corectă?

**Răspuns brut:** Marius i-a dat stiloul.

**Gold:**  
Variante: Marius, Nicu.  
Indiciu: niciun indiciu suficient.  
Concluzie: ambiguu.

#### F4B — indiciu relevant ignorat

**Prompt:** Marius i-a dat lui Nicu stiloul său. Nicu precizează că nu a avut niciodată stilou. Ce variantă este corectă?

**Răspuns brut:** Marius i-a dat lui Nicu stiloul. Nicu spune că nu a avut niciodată stilou.

**Gold:**  
Variante: Marius, Nicu.  
Indiciu: Nicu precizează că nu a avut niciodată stilou.; elimină Nicu.  
Concluzie: Marius.

#### F4C — certitudine prematură

**Prompt:** Marius i-a dat lui Nicu stiloul său. Marius este menționat primul. Ce variantă este corectă?

**Răspuns brut:** Marius i-a dat stiloul lui Nicu.

**Gold:**  
Variante: Marius, Nicu.  
Indiciu: Marius este menționat primul.; nu elimină nicio variantă.  
Concluzie: ambiguu.

#### F5A — candidat valid omis

**Prompt:** Două echipe puteau deschide ceremonia. Una a deschis. Ce variantă este corectă?

**Răspuns brut:** A deschis ceremonia.

**Gold:**  
Variante: echipa Vest, echipa Centru.  
Indiciu: niciun indiciu suficient.  
Concluzie: ambiguu.

#### F5B — negație/excepție pierdută

**Prompt:** Două echipe puteau deschide ceremonia. Una a deschis. Procesul-verbal spune că echipa Centru nu a urcat pe scenă. Ce variantă este corectă?

**Răspuns brut:** A deschis echipa Centru.

**Gold:**  
Variante: echipa Vest, echipa Centru.  
Indiciu: Procesul-verbal spune că echipa Centru nu a urcat pe scenă.; elimină echipa Centru.  
Concluzie: echipa Vest.

#### F5C — indiciu irelevant folosit

**Prompt:** Două echipe puteau deschide ceremonia. Una a deschis. Echipa Vest avea uniforme albe. Ce variantă este corectă?

**Răspuns brut:** Echipa Vest a deschis ceremonia.

**Gold:**  
Variante: echipa Vest, echipa Centru.  
Indiciu: Echipa Vest avea uniforme albe.; nu elimină nicio variantă.  
Concluzie: ambiguu.

#### F6B — indiciu relevant ignorat

**Prompt:** În gară erau trenul rapid și trenul personal. Am urcat într-unul. Trenul personal plecase înainte să ajung. Ce variantă este corectă?

**Răspuns brut:** Am urcat în trenul personal. Trenul rapid plecase înainte să ajung.

**Gold:**  
Variante: trenul rapid, trenul personal.  
Indiciu: Trenul personal plecase înainte să ajung.; elimină trenul personal.  
Concluzie: trenul rapid.

#### F6C — contradicție între candidați, indiciu și concluzie

**Prompt:** În gară erau trenul rapid și trenul personal. Am urcat într-unul. Trenul rapid era vopsit recent. Ce variantă este corectă?

**Răspuns brut:** Am urcat în trenul rapid.  
  
Am urcat în trenul personal.

**Gold:**  
Variante: trenul rapid, trenul personal.  
Indiciu: Trenul rapid era vopsit recent.; nu elimină nicio variantă.  
Concluzie: ambiguu.

#### F7A — candidat valid omis

**Prompt:** În mapă erau biletul roșu și biletul albastru. Am validat unul. Ce variantă este corectă?

**Răspuns brut:** Am validat unul dintre bilete.

**Gold:**  
Variante: biletul roșu, biletul albastru.  
Indiciu: niciun indiciu suficient.  
Concluzie: ambiguu.

#### F7B — incertitudine păstrată prea mult

**Prompt:** În mapă erau biletul roșu și biletul albastru. Am validat unul. Aparatul consemnează că biletul albastru nu a fost validat. Ce variantă este corectă?

**Răspuns brut:** Am validat unul dintre bilete. Aparatul consemnează că biletul albastru nu a fost validat.

**Gold:**  
Variante: biletul roșu, biletul albastru.  
Indiciu: Aparatul consemnează că biletul albastru nu a fost validat.; elimină biletul albastru.  
Concluzie: biletul roșu.

#### F7C — candidat valid omis

**Prompt:** În mapă erau biletul roșu și biletul albastru. Am validat unul. Biletul roșu avea un colț îndoit. Ce variantă este corectă?

**Răspuns brut:** Am validat unul dintre bilete. Biletul roșu avea un colț îndoit.

**Gold:**  
Variante: biletul roșu, biletul albastru.  
Indiciu: Biletul roșu avea un colț îndoit.; nu elimină nicio variantă.  
Concluzie: ambiguu.

#### F8A — candidat valid omis

**Prompt:** Luca și Matei depuseseră fiecare câte un proiect. Unul dintre proiecte a fost selectat. Ce variantă este corectă?

**Răspuns brut:** Luca și Matei au depus fiecare câte un proiect. Unul dintre proiecte a fost selectat.

**Gold:**  
Variante: proiectul lui Luca, proiectul lui Matei.  
Indiciu: niciun indiciu suficient.  
Concluzie: ambiguu.

#### F8C — candidat valid omis

**Prompt:** Luca și Matei depuseseră fiecare câte un proiect. Unul dintre proiecte a fost selectat. Luca vorbește primul. Ce variantă este corectă?

**Răspuns brut:** Luca: Am depus proiectul.  
  
Matei: Și eu am depus unul.

**Gold:**  
Variante: proiectul lui Luca, proiectul lui Matei.  
Indiciu: Luca vorbește primul.; nu elimină nicio variantă.  
Concluzie: ambiguu.

### Copycat 06 epoca 1

#### F1A — certitudine prematură

**Prompt:** În dulap erau dosarul și agenda. Am scos un obiect. Ce variantă este corectă?

**Răspuns brut:** Am scos dosarul. Agenda este un substantiv plural, deci nu poate fi obiectul singular.

**Gold:**  
Variante: dosarul, agenda.  
Indiciu: niciun indiciu suficient.  
Concluzie: ambiguu.

#### F1B — indiciu relevant ignorat

**Prompt:** În dulap erau dosarul și agenda. Am scos un obiect. Dosarul apare apoi în fotografia dulapului închis. Ce variantă este corectă?

**Răspuns brut:** Dosarul este obiectul scos. Agenda nu este menționată în fotografie. Varianta corectă este:  
  
Dosarul era în dulap.

**Gold:**  
Variante: dosarul, agenda.  
Indiciu: Dosarul apare apoi în fotografia dulapului închis.; elimină dosarul.  
Concluzie: agenda.

#### F1C — indiciu irelevant folosit

**Prompt:** În dulap erau dosarul și agenda. Am scos un obiect. Agenda avea copertă maro. Ce variantă este corectă?

**Răspuns brut:** Am scos agenda. Dosarul nu este obiectul scos.

**Gold:**  
Variante: dosarul, agenda.  
Indiciu: Agenda avea copertă maro.; nu elimină nicio variantă.  
Concluzie: ambiguu.

#### F1D — candidat invalid păstrat

**Prompt:** Candidații sunt dosarul, agenda, mapa. Dosarul a rămas, iar agenda era pe biroul colegei. Ce variantă rămâne?

**Răspuns brut:** Dosarul este singurul care rămâne, deoarece agenda și mapa sunt pluralizate.

**Gold:**  
Variante: dosarul, agenda, mapa.  
Indiciu: Dosarul a rămas, iar agenda era pe biroul colegei.; elimină celelalte două variante.  
Concluzie: mapa.

#### F2A — certitudine prematură

**Prompt:** La ghișeu așteptau Rina și Sanda. Una a fost chemată. Ce variantă este corectă?

**Răspuns brut:** «A fost chemată» este singular, deci Rina este cea chemată.

**Gold:**  
Variante: Rina, Sanda.  
Indiciu: niciun indiciu suficient.  
Concluzie: ambiguu.

#### F2B — indiciu relevant ignorat

**Prompt:** La ghișeu așteptau Rina și Sanda. Una a fost chemată. Sanda apare în filmare la ghișeu în timpul chemării. Ce variantă este corectă?

**Răspuns brut:** Filmarea arată că Sanda a fost chemată. Rina nu este exclusă, dar Sanda este confirmată.

**Gold:**  
Variante: Rina, Sanda.  
Indiciu: Sanda apare în filmare la ghișeu în timpul chemării.; elimină Sanda.  
Concluzie: Rina.

#### F2C — indiciu irelevant folosit

**Prompt:** La ghișeu așteptau Rina și Sanda. Una a fost chemată. Rina purta un fular. Ce variantă este corectă?

**Răspuns brut:** «A fost chemată» se potrivește cu Rina, care purta un fular.

**Gold:**  
Variante: Rina, Sanda.  
Indiciu: Rina purta un fular.; nu elimină nicio variantă.  
Concluzie: ambiguu.

#### F3A — altă eroare

**Prompt:** Pe tavă erau ceaiul și sucul. A fost servită o băutură. Ce variantă este corectă?

**Răspuns brut:** Ceaiul și sucul sunt două băuturi. Varianta (a) este corectă.

**Gold:**  
Variante: ceaiul, sucul.  
Indiciu: niciun indiciu suficient.  
Concluzie: ambiguu.

#### F3C — candidat valid omis

**Prompt:** Pe tavă erau ceaiul și sucul. A fost servită o băutură. Ceaiul avea o felie de lămâie. Ce variantă este corectă?

**Răspuns brut:** Ceaiul și sucul sunt două băuturi. Ceaiul avea o felie de lămâie este o descriere a ceaiului.

**Gold:**  
Variante: ceaiul, sucul.  
Indiciu: Ceaiul avea o felie de lămâie.; nu elimină nicio variantă.  
Concluzie: ambiguu.

#### F4B — negație/excepție pierdută

**Prompt:** Marius i-a dat lui Nicu stiloul său. Nicu precizează că nu a avut niciodată stilou. Ce variantă este corectă?

**Răspuns brut:** Nicu nu a avut niciodată stilou este o afirmație contradictorie. Marius a dat stiloul lui Nicu, așa că Nicu trebuie să fi avut-o. Varianta corectă este: Nicu precizează că nu a avut niciodată stiloul.

**Gold:**  
Variante: Marius, Nicu.  
Indiciu: Nicu precizează că nu a avut niciodată stilou.; elimină Nicu.  
Concluzie: Marius.

#### F4C — certitudine prematură

**Prompt:** Marius i-a dat lui Nicu stiloul său. Marius este menționat primul. Ce variantă este corectă?

**Răspuns brut:** Marius este subiectul, iar Nicu este indirect. Varianta corectă este:  
  
Marius i-a dat lui Nicu stiloul său.

**Gold:**  
Variante: Marius, Nicu.  
Indiciu: Marius este menționat primul.; nu elimină nicio variantă.  
Concluzie: ambiguu.

#### F4D — contradicție între candidați, indiciu și concluzie

**Prompt:** Candidații sunt Marius, Nicu, Ovidiu. Marius și-a retras obiectul, iar Nicu spune că stiloul este al lui Ovidiu. Ce variantă rămâne?

**Răspuns brut:** Marius și-a retras obiectul, iar Nicu spune că stiloul este al lui Ovidiu. Varianta rămasă este cea a lui Nicu.

**Gold:**  
Variante: Marius, Nicu, Ovidiu.  
Indiciu: Marius și-a retras obiectul, iar Nicu spune că stiloul este al lui Ovidiu.; elimină celelalte două variante.  
Concluzie: Ovidiu.

#### F5A — candidat valid omis

**Prompt:** Două echipe puteau deschide ceremonia. Una a deschis. Ce variantă este corectă?

**Răspuns brut:** «Una» este singular, deci se potrivește cu deschiderea singulară.

**Gold:**  
Variante: echipa Vest, echipa Centru.  
Indiciu: niciun indiciu suficient.  
Concluzie: ambiguu.

#### F5B — negație/excepție pierdută

**Prompt:** Două echipe puteau deschide ceremonia. Una a deschis. Procesul-verbal spune că echipa Centru nu a urcat pe scenă. Ce variantă este corectă?

**Răspuns brut:** Procesul-verbal spune că echipa Centru nu a deschis ceremonia. Varianta corectă este aceea.

**Gold:**  
Variante: echipa Vest, echipa Centru.  
Indiciu: Procesul-verbal spune că echipa Centru nu a urcat pe scenă.; elimină echipa Centru.  
Concluzie: echipa Vest.

#### F5C — indiciu irelevant folosit

**Prompt:** Două echipe puteau deschide ceremonia. Una a deschis. Echipa Vest avea uniforme albe. Ce variantă este corectă?

**Răspuns brut:** Echipa Vest este singura care poate fi identificată prin uniformele albe. Varianta corectă este:  
  
Echipa Vest a deschis ceremonia.

**Gold:**  
Variante: echipa Vest, echipa Centru.  
Indiciu: Echipa Vest avea uniforme albe.; nu elimină nicio variantă.  
Concluzie: ambiguu.

#### F6B — indiciu relevant ignorat

**Prompt:** În gară erau trenul rapid și trenul personal. Am urcat într-unul. Trenul personal plecase înainte să ajung. Ce variantă este corectă?

**Răspuns brut:** Am urcat în trenul personal. Varianta corectă este cea care se potrivește cu timpul trecut al verbului.

**Gold:**  
Variante: trenul rapid, trenul personal.  
Indiciu: Trenul personal plecase înainte să ajung.; elimină trenul personal.  
Concluzie: trenul rapid.

#### F6C — indiciu irelevant folosit

**Prompt:** În gară erau trenul rapid și trenul personal. Am urcat într-unul. Trenul rapid era vopsit recent. Ce variantă este corectă?

**Răspuns brut:** Am urcat în trenul rapid. Varianta corectă este cea care se potrivește cu acordul subiect-verb.

**Gold:**  
Variante: trenul rapid, trenul personal.  
Indiciu: Trenul rapid era vopsit recent.; nu elimină nicio variantă.  
Concluzie: ambiguu.

#### F7A — candidat valid omis

**Prompt:** În mapă erau biletul roșu și biletul albastru. Am validat unul. Ce variantă este corectă?

**Răspuns brut:** Am validat unul. Varianta corectă este cea care se potrivește cu regulile gramaticale ale limbii române.

**Gold:**  
Variante: biletul roșu, biletul albastru.  
Indiciu: niciun indiciu suficient.  
Concluzie: ambiguu.

#### F7B — incertitudine păstrată prea mult

**Prompt:** În mapă erau biletul roșu și biletul albastru. Am validat unul. Aparatul consemnează că biletul albastru nu a fost validat. Ce variantă este corectă?

**Răspuns brut:** Am validat unul. Aparatul consemnează că biletul albastru nu a fost validat.

**Gold:**  
Variante: biletul roșu, biletul albastru.  
Indiciu: Aparatul consemnează că biletul albastru nu a fost validat.; elimină biletul albastru.  
Concluzie: biletul roșu.

#### F7C — indiciu irelevant folosit

**Prompt:** În mapă erau biletul roșu și biletul albastru. Am validat unul. Biletul roșu avea un colț îndoit. Ce variantă este corectă?

**Răspuns brut:** Am validat unul dintre bilete. Biletul roșu este singurul validat.

**Gold:**  
Variante: biletul roșu, biletul albastru.  
Indiciu: Biletul roșu avea un colț îndoit.; nu elimină nicio variantă.  
Concluzie: ambiguu.

#### F8B — incertitudine păstrată prea mult

**Prompt:** Luca și Matei depuseseră fiecare câte un proiect. Unul dintre proiecte a fost selectat. Matei declară că proiectul său nu a fost selectat. Ce variantă este corectă?

**Răspuns brut:** Proiectul lui Matei nu a fost selectat. Luca nu poate fi exclus în mod direct.

**Gold:**  
Variante: proiectul lui Luca, proiectul lui Matei.  
Indiciu: Matei declară că proiectul său nu a fost selectat.; elimină proiectul lui Matei.  
Concluzie: proiectul lui Luca.

#### F8C — candidat valid omis

**Prompt:** Luca și Matei depuseseră fiecare câte un proiect. Unul dintre proiecte a fost selectat. Luca vorbește primul. Ce variantă este corectă?

**Răspuns brut:** «Fiecare a depus un proiect. Unul a fost selectat.» este corect.

**Gold:**  
Variante: proiectul lui Luca, proiectul lui Matei.  
Indiciu: Luca vorbește primul.; nu elimină nicio variantă.  
Concluzie: ambiguu.

### Copycat 07 epoca 1

#### F1B — indiciu relevant ignorat

**Prompt:** În dulap erau dosarul și agenda. Am scos un obiect. Dosarul apare apoi în fotografia dulapului închis. Ce variantă este corectă?

**Răspuns brut:** «Am scos dosarul.» este corect. Agenda nu poate fi scoasă în fotografie.

**Gold:**  
Variante: dosarul, agenda.  
Indiciu: Dosarul apare apoi în fotografia dulapului închis.; elimină dosarul.  
Concluzie: agenda.

#### F1D — candidat invalid păstrat

**Prompt:** Candidații sunt dosarul, agenda, mapa. Dosarul a rămas, iar agenda era pe biroul colegei. Ce variantă rămâne?

**Răspuns brut:** Dosarul a rămas. Agenda este eliminată de «era» și de prepoziția «pe biroul colegei».

**Gold:**  
Variante: dosarul, agenda, mapa.  
Indiciu: Dosarul a rămas, iar agenda era pe biroul colegei.; elimină celelalte două variante.  
Concluzie: mapa.

#### F2A — certitudine prematură

**Prompt:** La ghișeu așteptau Rina și Sanda. Una a fost chemată. Ce variantă este corectă?

**Răspuns brut:** «A fost chemată» este singular, deci se potrivește cu Rina.

**Gold:**  
Variante: Rina, Sanda.  
Indiciu: niciun indiciu suficient.  
Concluzie: ambiguu.

#### F2C — certitudine prematură

**Prompt:** La ghișeu așteptau Rina și Sanda. Una a fost chemată. Rina purta un fular. Ce variantă este corectă?

**Răspuns brut:** «A fost chemată» este singular, deci se potrivește cu Rina. Fularul este un detaliu inutil.

**Gold:**  
Variante: Rina, Sanda.  
Indiciu: Rina purta un fular.; nu elimină nicio variantă.  
Concluzie: ambiguu.

#### F3B — incertitudine păstrată prea mult

**Prompt:** Pe tavă erau ceaiul și sucul. A fost servită o băutură. Sucul este consemnat ca rămas pe tavă. Ce variantă este corectă?

**Răspuns brut:** Poate fi ceaiul sau sucul. Textul nu decide.

**Gold:**  
Variante: ceaiul, sucul.  
Indiciu: Sucul este consemnat ca rămas pe tavă.; elimină sucul.  
Concluzie: ceaiul.

#### F4A — candidat valid omis

**Prompt:** Marius i-a dat lui Nicu stiloul său. Ce variantă este corectă?

**Răspuns brut:** «Să» este forma masculină a pronumelui, deci este corectă.

**Gold:**  
Variante: Marius, Nicu.  
Indiciu: niciun indiciu suficient.  
Concluzie: ambiguu.

#### F4B — altă eroare

**Prompt:** Marius i-a dat lui Nicu stiloul său. Nicu precizează că nu a avut niciodată stilou. Ce variantă este corectă?

**Răspuns brut:** «Niciodată» este singular, deci se potrivește cu «nu a avut niciodată». Marius este subiectul implicit al «a avut», deci stiloul este cel dat.

**Gold:**  
Variante: Marius, Nicu.  
Indiciu: Nicu precizează că nu a avut niciodată stilou.; elimină Nicu.  
Concluzie: Marius.

#### F4C — certitudine prematură

**Prompt:** Marius i-a dat lui Nicu stiloul său. Marius este menționat primul. Ce variantă este corectă?

**Răspuns brut:** Marius este donatorul; stiloul este obiectul. Varianta corectă este:  
  
Marius i-a dat stiloul lui Nicu.

**Gold:**  
Variante: Marius, Nicu.  
Indiciu: Marius este menționat primul.; nu elimină nicio variantă.  
Concluzie: ambiguu.

#### F5A — candidat valid omis

**Prompt:** Două echipe puteau deschide ceremonia. Una a deschis. Ce variantă este corectă?

**Răspuns brut:** «A deschis» este singular, deci se potrivește cu «una».

**Gold:**  
Variante: echipa Vest, echipa Centru.  
Indiciu: niciun indiciu suficient.  
Concluzie: ambiguu.

#### F6A — candidat valid omis

**Prompt:** În gară erau trenul rapid și trenul personal. Am urcat într-unul. Ce variantă este corectă?

**Răspuns brut:** «Am urcat într-unul» este o construcție singulară, deci se potrivește cu «trenul» singular.

**Gold:**  
Variante: trenul rapid, trenul personal.  
Indiciu: niciun indiciu suficient.  
Concluzie: ambiguu.

#### F6B — contradicție între candidați, indiciu și concluzie

**Prompt:** În gară erau trenul rapid și trenul personal. Am urcat într-unul. Trenul personal plecase înainte să ajung. Ce variantă este corectă?

**Răspuns brut:** «Am urcat în trenul personal.» este corect. Trenul personal a plecat, deci nu poate fi cel ales.

**Gold:**  
Variante: trenul rapid, trenul personal.  
Indiciu: Trenul personal plecase înainte să ajung.; elimină trenul personal.  
Concluzie: trenul rapid.

#### F6C — indiciu irelevant folosit

**Prompt:** În gară erau trenul rapid și trenul personal. Am urcat într-unul. Trenul rapid era vopsit recent. Ce variantă este corectă?

**Răspuns brut:** «Am urcat în trenul rapid.» este corectă. Trenul personal nu este menționat ca fiind vopsit recent.

**Gold:**  
Variante: trenul rapid, trenul personal.  
Indiciu: Trenul rapid era vopsit recent.; nu elimină nicio variantă.  
Concluzie: ambiguu.

#### F7A — certitudine prematură

**Prompt:** În mapă erau biletul roșu și biletul albastru. Am validat unul. Ce variantă este corectă?

**Răspuns brut:** «Am validat unul» este singular, deci biletul singular este biletul roșu.

**Gold:**  
Variante: biletul roșu, biletul albastru.  
Indiciu: niciun indiciu suficient.  
Concluzie: ambiguu.

#### F7B — incertitudine păstrată prea mult

**Prompt:** În mapă erau biletul roșu și biletul albastru. Am validat unul. Aparatul consemnează că biletul albastru nu a fost validat. Ce variantă este corectă?

**Răspuns brut:** «Am validat unul.» este o construcție gramaticală validă. Aparatul consemnează că biletul albastru nu a fost validat.

**Gold:**  
Variante: biletul roșu, biletul albastru.  
Indiciu: Aparatul consemnează că biletul albastru nu a fost validat.; elimină biletul albastru.  
Concluzie: biletul roșu.

#### F8C — candidat valid omis

**Prompt:** Luca și Matei depuseseră fiecare câte un proiect. Unul dintre proiecte a fost selectat. Luca vorbește primul. Ce variantă este corectă?

**Răspuns brut:** «Unul dintre proiecte» este corect. Luca nu poate selecta proiectul, deci nu poate fi vorbitorul.

**Gold:**  
Variante: proiectul lui Luca, proiectul lui Matei.  
Indiciu: Luca vorbește primul.; nu elimină nicio variantă.  
Concluzie: ambiguu.

## Analiza familiilor contrastive

### Copycat 05B epoca 2

- Ambiguul reușește, versiunea rezolvată eșuează: F1, F3, F6.
- Rezolvatul reușește, dar versiunea ambiguă inventează certitudine: F2, F8.
- Influențat explicit de indiciul irelevant: F2C, F5C.

### Copycat 06 epoca 1

- Ambiguul reușește, versiunea rezolvată eșuează: F4, F6, F8.
- Rezolvatul reușește, dar versiunea ambiguă inventează certitudine: F3.
- Influențat explicit de indiciul irelevant: F1C, F2C, F5C, F6C, F7C.

### Copycat 07 epoca 1

- Ambiguul reușește, versiunea rezolvată eșuează: F1, F3.
- Rezolvatul reușește, dar versiunea ambiguă inventează certitudine: F2, F5.
- Influențat explicit de indiciul irelevant: F6C.

## Probe și exemple pentru revizuire umană

- **Benchmark F2B:** prezența Sandei la ghișeu „în timpul chemării” nu exclude fără echivoc că ea este persoana chemată; poate fi chemată verbal și să rămână acolo. Gold-ul poate fi prea sigur.
- **Benchmark F4B:** afirmația că Nicu nu a avut niciodată stilou face lectura posesivă foarte improbabilă, dar momentul primirii poate constitui chiar prima posesie. Gold-ul depinde de interpretarea temporală.
- **Benchmark F5B:** faptul că echipa Centru nu a urcat pe scenă nu exclude strict deschiderea ceremoniei din alt loc. Gold-ul folosește o presupunere despre desfășurarea ceremoniei.
- **Gold G21B și G22B:** acordul din propoziția următoare rezolvă cazul numai dacă presupunem că subiectul continuă să fie același. Legătura discursivă ar putea fi făcută mai explicită.
- **Gold G25A–C:** posesivul din „raftul ei” admite două lecturi, dar unii vorbitori pot prefera puternic referentul feminin apropiat. Preferința nu este dovadă, conform obiectivului lecției.
- **Gold G05B:** absența echipamentului la paznic elimină camera numai dacă „cu camera” exprimă posesia/folosirea echipamentului în acel moment; aceasta este lectura urmărită, dar merită validare nativă.
