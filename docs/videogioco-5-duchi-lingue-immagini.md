---
titolo: Videogioco "I cinque duchi" — le immagini degli oggetti di interazione: dove vengono e perché si dichiarano
versione: 0.2
data: 2026-10-04
autore: Pietro Fabbri (con Claude)
fonte: ricerca su Wikimedia Commons del 02/10/2026
documenti collegati: videogioco-5-duchi-lingue.md (v0.2), videogioco-5-duchi-ritratti.md (v0.5), videogioco-5-duchi-luoghi-edifici.md (v0.4), videogioco-5-duchi-esercizi.md (v0.1), AGENTS.md, FONTI-E-LICENZE.md
dati: dati/lingue/associazioni.json (v1), dati/lingue/immagini_oggetti.json (v1, **il primo giro**, 180 voci, 1120 candidati), dati/lingue/immagini_2.json (v2, **il secondo giro** per il latino, il greco e il ferrarese: 90 voci, 547 candidati), dati/lingue/attestazione_oggetti.json (le scelte a vista; **vuota finché nessuno guarda**), dati/lingue/giudizi_oggetti.json (**da produrre**: i giudizi che Pietro scrive guardando i fogli, che `giudizi_oggetti.py` trasforma in attestazione)
controllo: python3 sorgenti/lingue/verifica_immagini_oggetti.py (G1-G7: copertura, licenze, misura, proporzione, completezza, pertinenza e scivolamento), python3 sorgenti/lingue/cerca_immagini_2.py (il secondo giro, con un controllo di allineamento che si ferma se la tabella dei termini non ha esattamente le trenta voci), python3 sorgenti/lingue/fogli_oggetti.py (i 18 fogli di controllo), python3 sorgenti/lingue/giudizi_oggetti.py (registra i giudizi a vista e li applica all'attestazione)
---

# Le immagini degli oggetti di interazione

## 0. A che cosa serve, e che cosa non è ancora fatto

Il gioco ha seicentottanta voci di oggetto: **trenta per ciascuna delle sei lingue** (`videogioco-5-duchi-lingue.md` §5.4). Ogni voce è la cosa con cui il giocatore interagisce nella tappa facoltativa dell'oggetto: la pizza, un numero romano, un clarinetto, una coppa greca, un campo di raccolta dei proverbi ferraresi.

Questo documento dice **quali immagini esistono per quelle voci, con quale licenza, e quali non esistono**. È un documento di controllo, non un catalogo da sfogliare, ed è gemello di `videogioco-5-duchi-ritratti.md`.

**Che cosa è fatto.** Una ricerca su Wikimedia Commons ha esaminato tutte e 180 le voci con termini scelti uno per uno, non tradotti alla cieca. Ha prodotto **1120 candidati con licenza libera**, di cui il progetto ne ha **respinti 12** per difetto automatico. I dati sono in `dati/lingue/immagini_oggetti.json`.

**Che cosa non è fatto, e conta più del resto.** **Nessuna immagine è stata ancora scelta, e nessuna è stata guardata a vista.** I 1120 candidati sono *proposte*, non scelte. Il controllo automatico verifica licenza, misura e copertura, ma non può sapere se la fotografia del «kykeon» mostra il kykeon o un vaso qualsiasi: se lo chiede, risponde che non lo sa. La scelta la fa una persona, e si registra in `dati/lingue/attestazione_oggetti.json` con etichetta e motivo, come per i ritratti.

**Il difetto più importante del lavoro è in §5**, ed è la ripetizione esatta di un difetto già trovato nei ritratti. Vale la pena leggerlo prima di fidarsi di qualunque numero di questo documento.

---

## 1. La regola: quattro immagini, non una

La regola dei ritratti (`ritratti.md` §1: due immagini, non una) vale per le persone. Per gli oggetti ne servono quattro, perché un oggetto può essere fotografato, dipinto, stampato — o non essere visibile affatto.

| | `foto` | `dipinto` | `stampa` | `nessuna` |
|---|---|---|---|---|
| **quando** | esiste una fotografia libera che mostra l'oggetto | l'oggetto esiste solo in un'opera d'arte | l'oggetto esiste in una fonte a stampa, un manoscritto, una partitura, un'epigrafe | non esiste immagine libera, e l'oggetto va disegnato |
| **esempio** | *la pizza*, *il vino* | *il simposio*, *le coppe dipinte* | *i numeri romani*, *gli auspici* | *i proverbi ferraresi*, *la trasmissione della tecnica* |
| **chi decide** | una ricerca automatica **propone**, poi un attestato a vista | idem | idem | idem |
| **dichiarazione** | l'**etichetta** (§3) e la **licenza** | idem | idem | il **motivo** per cui non c'è immagine |

La quarta categoria non è una sconfitta. È la parte del gioco in cui si vede che la conoscenza ha un bordo, ed è la stessa lezione dei 44 emblemi dei ritratti: una voce con scritto «non esiste immagine libera» insegna più di un'immagine inventata.

**Regola che vale per tutte e quattro.** Nel gioco **non entra un'immagine generata**, per nessun oggetto. Una fotografia di una pizza vera sì; una pizza disegnata dall'IA no. Un dipinto di un simposio sì; un simposio ricostruito no. Il progetto vieta i volti inventati per le persone reali e vieta, per la ragione stessa, gli oggetti inventati: un piatto inventato insegna che le regioni d'Italia hanno piatti che non esistono, il che è una bugia con una bella cornice.

---

## 2. I numeri della ricerca

La ricerca ha girato il 02/10/2026 su Wikimedia Commons, con `sorgenti/lingue/cerca_immagini_oggetti.py`, che chiede a Commons i nomi dei file (`filetype:bitmap`) e ne legge la licenza dalla pagina del file.

| | Italiano | Ferrarese | Latino | Inglese | LIS | Greco | **Totale** |
|---|---|---|---|---|---|---|---|
| voci | 30 | 30 | 30 | 30 | 30 | 30 | **180** |
| con immagini libere | 30 | 0 | 28 | 30 | 30 | 28 | **146** |
| senza immagini libere | 0 | 30 | 2 | 0 | 0 | 2 | **34** |

**I candidati.** 1120 in tutto, 17 licenze diverse, tutte libere:

| Licenza | Candidati |
|---|---|
| CC BY-SA 4.0 | 476 |
| Public domain | 202 |
| CC BY-SA 3.0 | 126 |
| CC0 | 92 |
| CC BY 2.0 | 53 |
| CC BY 4.0 | 53 |
| CC BY-SA 2.0 | 45 |
| CC BY 3.0 | 38 |
| altre nove | 35 |

**I 34 senza immagini** non sono tutti la stessa cosa, e la distinzione conta:

| Lingua | Voci | Perché |
|---|---|---|
| **Ferrarese** | 30 | Le trenta voci **non sono oggetti**: sono campi da rilevare (`lingue.md` §5.4). Non esiste immagine che rappresenti «i proverbi dei mestieri». Non è una ricerca saltata: è una categoria, dichiarata nei dati con il suo motivo. |
| **Latino** | 2 | *L'ispezione delle interiora* e *le formule di protezione*: i termini cercati non danno nulla di libero. Vanno cercati in altre fonti, o dichiarati `nessuna`. |
| **Greco** | 2 | *Il vino di Maronea* e *i vini dirottati*: il primo non ha un'immagine propria (è un vino locale, non un oggetto riconoscibile), il secondo è una pratica di cui non resta documento visivo. |

---

### 2.1 Il secondo giro: cercare la **cosa**, non la **parola**

Il 04/10/2026 la ricerca è stata rifatta per il **latino**, il **greco** e il **ferrarese**, e il principio è cambiato: **si cerca la cosa che si vede, non la parola che la nomina**.

Una voce non è una parola da tradurre: è **la cosa che il ragazzo guarda**. Per «gli auspici» la risposta non è un file che si chiama *auspicia* ma **il lituo dell'augure**, lo strumento che l'augure tiene in mano in mano: è l'oggetto che fa quella cosa. Il primo giro cercava «auspicia» e trovava una **moneta con la scritta SPES**, che è un augurio di speranza e non un auspicio romano. Non era un errore di ricerca: era la ricerca giusta con la domanda sbagliata.

I termini nuovi sono in `sorgenti/lingue/cerca_immagini_2.py`, e sono **scritti a mano**: si dichiara la regola che il progetto dichiara da quattro giorni, cioè che **una ricerca automatica non sceglie, e nemmeno i termini**.

| | Primo giro | Secondo giro |
|---|---|---|
| voci cercate | 146 coperte + 34 scoperte | 90 (LA, EL, FE) |
| candidati delle novanta voci | 417 | **547** |
| voci **senza** nessun candidato | **34** | **6** |

Le trenta voci ferraresi non hanno più zero candidati per caso: hanno candidati per **decisione** (§2.2). Nei fogli di controllo le voci senza nessun candidato sono **3**, e non 6, perché il foglio ripiega sul primo giro quando il secondo non ha dato nulla: sono due numeri veri che descrivono due cose diverse, e quello giusto nella riga che parla del secondo giro è il 6.

**Il numero di voci coperte è migliorato. La correttezza no, e va detto per intero.** Cambiare i termini non è guardare le immagini: `cerca()` prende il **primo termine che dà un risultato**, e un termine come «Roman funeral procession» dà file di qualunque cosa. I nomi che sono tornati, letti uno per uno:

| Voce | Che cosa è tornato |
|---|---|
| **i riti funebri** | un corteo funebre di Carlo V, una processione cavalleresca del Seicento, e **un'elimitrice funebre Rolls Royce** |
| **il fuoco sacro** | un libro del 1900 e due monete di Shapur I |
| **i voti** | stele votive **buddiste** e **frigie**, non romane |
| **gli auspici** | una moneta di un senatore, un libro francese in Rough Draft**, e un lituo — cioè il terzo dei tre è giusto |
| **la maledizione** | tre vere *defixio*, le tavolette di maledizione: l'unica voce centrata |

È la stessa lezione di §5, scritta quattro giorni fa e ripetuta oggi: **una ricerca che restituisce un file non ha trovato l'oggetto**. Il secondo giro ha cambiato la domanda, non ha guardato, e la differenza si vede solo sui nomi — che è il massimo che si può pretendere da una ricerca, e il minimo che basta a sapere che il lavoro di guardare è ancora tutto da fare.

**Una cosa che il secondo giro non può fare, e va detto**: il numero di G7 non è confrontabile fra i due giri. G7 misura se il **nome del file** nomina la voce, e il secondo giro cerca per **concetto**: il file di un rito funebro romano non contiene la parola «funebri» contiene la parola *funeral*. Il numero è quindi **più basso nel secondo giro proprio perché la ricerca è migliore**, e dichiararlo come un peggioramento sarebbe il difetto al contrario: un numero che non misura quello che dice di misurare.

### 2.2 Le trenta voci ferraresi: la cosa che il proverbio riguarda

Le trenta voci ferraresi sono campi di proverbi e modi di dire, e un proverbio non ha immagine. Il 02/10 la risposta era `nessuna` con il motivo dichiarato, e la Q4 chiedeva che cosa fare della tappa ferrarese, che sarebbe stata l'unica senza immagine.

**Pietro ha deciso il 04/10/2026 di associare «qualcosa di evocativo»**, e la scelta è dichiarata perche' è una scelta: alla voce «i proverbi sul tempo» non si mette un'immagine dei proverbi — che non esiste — ma **la Torre dell'Orologio di Ferrara**, che è la cosa di cui il campo parla. Non è l'immagine del proverbio: è **la cosa che il proverbio riguarda**, e quella si può fotografare per davvero.

La regola che ne nasce è dichiarata perché qualcuno la riuserà: **a una voce che non ha un oggetto si può associare la cosa che la voce evoca, e solo se esiste ed è vera**. Un'immagine inventata è esclusa come sempre (`prova 5`): se per «i proverbi sulla fortuna» non ci fosse niente di ferrarese da fotografare, la risposta resta `nessuna` col motivo, e va detto che è una delle quattro categorie e non un buco.


## 3. Le etichette, che sono la parte importante

Ogni immagine che entra nel gioco porta un'etichetta, come i ritratti. Le etichette sono nove, e sono la garanzia che chi guarda un'immagine sappia che cosa sta guardando:

| Etichetta | Quando |
|---|---|
| `fotografia` | scatto fotografico, moderno o d'archivio |
| `immagine_d_archivio` | scatto storico, con data e luogo se disponibili |
| `dipinto` | dipinto su tela, tavola o muro |
| `incisione` | incisione, xilografia, litografia, acquaforte |
| `miniatura` | miniatura di manoscritto |
| `rilievo` | bassorilievo, alto rilievo, scolpito |
| `partitura` | spartito, tablatura, notazione musicale |
| `frammento_antico` | parte di un'opera antica, con il museo e l'inventario |
| `immagine_tratteggiata` | disegno, schizzo, incisione d'epoca |

**Tre regole che le etichette devono rispettare.**

1. **L'etichetta descrive l'immagine, non l'oggetto.** Un'anfora greca fotografata in un museo è `frammento_antico`, non `anfora`: l'anfora è l'oggetto, l'immagine è quello che le hanno fatto.
2. **La data va dichiarata quando c'è.** Un'immagine senza data non è un'immagine storica: è un'immagine che *potrebbe* essere del 1900 o del 2020, e il gioco non può fingere di sapere quale delle due sia.
3. **Il museo e l'inventario, quando ci sono.** Le collezioni museali sono le fonti più serie di questo progetto, e citare il numero d'inventario è ciò che rende un'immagine verificabile da chiunque.

Le stesse regole valgono per l'autore e per la licenza, che ogni scheda mostra (§4).

---
## 4. Misura e proporzione: la parte che riguarda la fedeltà

Una rappresentazione è fedele solo se **non cambia le proporzioni di ciò che rappresenta**. È la regola che vale per i luoghi (`luoghi-edifici.md` §5, il rilievo come risposta alle altezze mancanti) e vale qui con una conseguenza pratica: **le immagini non si stirano mai**.

### 4.1 Le misure

| | Ritratto | Scheda oggetto | Perché |
|---|---|---|---|
| Misura | 48×54 px | **96×72 px** | L'oggetto ha bisogno di poco più di spazio del ritratto, perché si riconosca; il doppio sarebbe una foto a parte |
| Proporzione | 8:9, verticale | **4:3, orizzontale** | La scheda è accanto al testo del livello, non sopra |
| Peso atteso | 1 258 byte in media | **da misurare** | Non ancora misurato: le immagini non sono state scelte |
| Minimo per entrare | — | **160×120 px** | Sotto questa misura il gioco dovrebbe ingrandire, e il gioco non ingrandisce |

### 4.2 La regola del ritaglio, che è la parte difficile

I 1120 candidati hanno rapporti d'aspetto che vanno da **0,14 a 7,00**. Non si possono usare tutti: molti sono strisce, quadrati, o panorami.

La regola che il progetto adotta è di **ritagliare, non stirare**, con due condizioni che rendono la cosa onesta:

1. **Il ritaglio non può togliere l'oggetto.** Se ritagliare in 4:3 toglie il soggetto dalla foto, la foto non entra: si cerca un'altra immagine. Per questo il controllo **G4** verifica, per ciascuna voce, che **esista almeno un candidato usabile con la forma giusta**, e non accetta che tutte le opzioni siano da ritagliare a forza.
2. **Il ritaglio si dichiara.** Ogni scheda che ha subìto un ritaglio lo dice, come si dichiara la cronologia di una piazza (`luoghi-edifici.md` §4: una tappa del 1450 non può mostrare la piazza di oggi). Il giocatore che vede un'immagine ritagliata deve poter sapere che lo è.

**Il risultato del controllo.** Tutte e 146 le voci coperte — cioè tutte, salvo le trenta ferraresi e le quattro senza immagine — hanno **almeno un candidato con la misura e la proporzione giusta**. Non ce n'è nessuna che si può sistemare solo ritagliando a forza.

### 4.3 Quello che la proporzione non risolve

La proporzione corretta rende l'immagine **fedele nelle misure** e non dice niente sulla **sua verità**. Un'immagine stirata mente; un'immagine ritagliata può mentire anche di più, perché toglie il contesto. Perciò il ritaglio è ammesso solo se l'oggetto resta intero e riconoscibile, e la decisione finale resta di chi guarda l'immagine (Q1, §6).

---

## 5. Il difetto più importante: la ricerca ha trovato oggetti sbagliati

Questa sezione è il cuore del documento, e vale più dei numeri di §2.

Una ricerca automatica che «funziona» restituisce un file per ogni voce, e sembra risolto il problema. Non lo risolve. Nel progetto è già successo con i ritratti: la ricerca ha restituito **un gatto per Renata Viganò**, una ceramica iraniana per i mercanti di Ferrara e una parata di soldati di oggi per i Bersaglieri del 1848. Qui è successo di nuovo, in modo più sistematico, e i casi sono due.

**Il primo caso: la parola che significa due cose.** Alla voce **«la correggia»** il file migliore è stato `Antonio Allegri da Correggio.jpg`, cioè il ritratto di un pittore il cui cognome suona come la voce. Alla voce **«gli occhiali»** sono arrivate le foto di una moschea di Istanbul. Non è un errore della ricerca: è la differenza fra cercare una parola e cercare un oggetto.

**Il secondo caso, più grave: la parola giusta nel contesto sbagliato.** Alla voce **«il tè»** (greco, le bevande) il risultato è un mulino olandese e una fattoria, per la confusione fra «tea» e «the» in inglese. Alla voce **«la sete»** (greco) è arrivato un canale nella città di **Sète**, in Francia. Alla voce **«la conservazione»** sono arrivati articoli di **biologia della conservazione**, non la conservazione del vino in una cantina. Alla voce **«i proverbi»** (latino) è arrivata una **Biblia in latino**, che è un testo bellissimo e non è un proverbio. Alla voce **«sabaion»** (dolce piemontese) è arrivata la crema inglese *sabayon*, che è un'altra cosa.

Il controllo **G7** esiste per rendere questi casi visibili senza guardare le immagini: segnala le voci in cui **nessun** candidato contiene né la parola dell'oggetto né quella del termine cercato. Sono **67 voci su 146**, e la distribuzione dice già qualcosa:

| Lingua | Voci a rischio G7 | Su quante coperte |
|---|---|---|
| Italiano | 2 | 30 |
| Latino | **27** | 28 |
| Inglese | 12 | 30 |
| LIS | 9 | 30 |
| Greco | 17 | 28 |

**Il latino è il caso peggiore, e per una ragione che il progetto riconosce già.** Ventisette voci su ventotto sono a rischio, perché i termini latini che ho cercato sono termini **inglesi transliterati** (*haruspex*, *exta hepatum*), e Commons li contiene quasi solo in descrizioni, non nei nomi dei file. Non è un errore della ricerca: è che la ricerca è andata nel posto sbagliato per quella lingua.

**La regola che ne nasce, e che vale per tutto il progetto.**

> **Una ricerca che restituisce un file non ha trovato l'oggetto: ha trovato una parola.** La scelta la fa una persona che guarda l'immagine, e il risultato si registra in `dati/lingue/attestazione_oggetti.json` con etichetta, autore, licenza e **motivo del giudizio**.

È la stessa regola dei ritratti (`AGENTS.md` §3, «una ricerca automatica propone, non decide»), e il progetto l'ha già imparata una volta: quando un `HTTP 429` di Wikipedia venne letto come «nessun ritratto esiste», quindici personaggi con un ritratto celebre furono dichiarati senza. Una risposta che non arriva non è una risposta negativa, e un file che arriva non è la risposta giusta.

---

## 6. I controlli automatici e le questioni aperte

### 6.1 I sette controlli

`sorgenti/lingue/verifica_immagini_oggetti.py` esegue sette controlli su `dati/lingue/immagini_oggetti.json`:

| # | Controllo | Che cosa cerca | Esito |
|---|---|---|---|
| **G1** | Copertura | ogni voce ha candidati, e le trenta ferraresi dichiarano il motivo per cui non ne possono avere | 180 voci, tutte coperte o motivate |
| **G2** | Licenze | ogni candidato ha una licenza libera riconosciuta, e nessuna non commerciale | tutte libere |
| **G3** | Misura | nessun candidato sotto 160×120, che nel gioco verrebbe ingrandito | **4 respinti** |
| **G4** | Proporzione | ogni voce coperta ha almeno un candidato con la forma giusta per la scheda, senza ritaglio forzato | **146 su 146** |
| **G5** | Completezza | autore e indirizzo ci sono in ogni candidato | **8 respinti** |
| **G6** | Pertinenza | quante voci restano da guardare a vista: **146**, perché il controllo automatico non può sapere se l'immagine è dell'oggetto giusto | dichiarato |
| **G7** | Scivolamento | quante voci in cui nessun candidato nomina l'oggetto: **67**, da guardare per prime | avviso, non errore |

Il conto dei dodici problemi è **12 candidati respinti** su 1120, non dodici voci scoperte: tutte e dodici le voci hanno alternative. G7 non è un errore ed è per questo che non fa fallire lo script.

### 6.2 Le questioni aperte

**Q1 — Chi guarda le immagini, e con quale impegno? (chiusa il metodo il 04/10/2026; resta il lavoro)**
Guardare 1120 candidati a vista è un lavoro di ore, non di minuti. La domanda era *chi*, e il 04/10 è risolta: **le guarda Pietro**, io registro. Il metodo è quello dei ritratti ed è scritto: `sorgenti/lingue/fogli_oggetti.py` produce i **18 fogli** (dieci voci per foglio, i tre candidati migliori per voce, con licenza, autore, data e misura in ogni cella), e `sorgenti/lingue/giudizi_oggetti.py` prende i giudizi da `dati/lingue/giudizi_oggetti.json` — **da produrre**, perché quel file lo scrive chi guarda, e finché nessuno guarda non esiste e non deve esistere — e li scrive nell'attestazione **solo se reggono**: esito fra i tre, etichetta fra le nove, categoria fra le quattro, e **motivo di almeno 25 caratteri**. Un motivo più corto è un campo compilato a macchetta, ed è la forma più economica del difetto che il progetto ha imparato a cercare. I fogli non selezionano: mettono in testa i candidati che il loro nome non collega alla voce (`SOSPETTO`), perché un foglio che nasconde i sospetti serve a confermare e non a controllare. Restano da guardare i **180** migliori per voce — e il resto si considera sufficiente. La terza è la più realistica, ma va detto che **non è la stessa cosa**: un campione non attesta il resto.

**Q2 — Le trenta voci di ogni lingua sono confermate? (bloccante)**
Riprende `lingue.md` §7 Q2. Un'immagine cerca la voce giusta, non quella confermata: se le trenta voci cambiano, tutta la ricerca va rifatta. Conviene quindi chiudere Q2 prima di scegliere le immagini, non dopo.

**Q3 — Le fonti del latino e del greco vanno cercate altrove? (parzialmente chiusa il 04/10/2026)**
Il G7 dice che **27 voci latine su 28** hanno solo proposte scoperte per caso. Il 04/10 sono state cercate **di nuovo su Commons**, con i termini che nominano le cose (§2.1), e il latino è passato da **27 voci a rischio su 28** a un numero che il secondo giro non può confrontare (§2.1). Le fonti giuste per le voci che restano senza immagine non sono Commons: sono i **corpus epigrafici** (EDCS, EDR) e le **biblioteche digitali** (Gallica, BEIC). Commons ha le immagini degli oggetti, non le fonti filologiche. Va deciso se aggiungere questi due corpi alle ricerche, il che è un lavoro diverso e va detto.

**Q4 — Che cosa si fa delle trenta voci ferraresi? (chiusa il 04/10/2026)**
Le trenta voci ferraresi non hanno immagine **del proverbio**, che non esiste, e il 04/10 Pietro ha deciso che associano **la cosa che il campo evoca**, se esiste ed è vera (§2.2). Le tappe ferraresi quindi **non sono le uniche senza immagine**, e ogni voce che non trovi niente di ferrarese torna `nessuna` col motivo dichiarato. Va ancora deciso se le tappe ferraresi mostrano qualcos'altro — un'immagine della persona che parla, una trascrizione, il paesaggio — o se dichiarano il vuoto con la stessa regola dei 44 emblemi. La seconda è più onesta, ed è quella che il progetto sceglie di solito.

**Q5 — Le immagini servono solo per le facoltative? (non bloccante)**
Le voci degli oggetti servono alle tappe facoltative, ma gli stessi oggetti compaiono anche nei **testi autentici** dei 900 livelli (`lingue.md` §2: ogni livello ha un testo vero). Una tappa su Cesare ha bisogno di un'immagine della pagina di Cesare, non di una coppa. Le due cose sono diverse, e solo la prima è stata fatta: **le immagini dei testi autentici non sono state cercate**, e sono almeno 900.

**Q6 — Chi ridimensiona, e quando? (non bloccante, tecnica)**
Ridurre a 96×72 gli spinelli di Commons richiede un'immagine minima (§4.1), un taglio che non alteri la proporzione, e una decisione sul formato. Il metodo (`ritratto_reale.py` per i ritratti) esiste già e va ripreso, ma nessuna immagine degli oggetti è ancora stata ridotta, perché nessuna è stata scelta.

---

## 7. Registro delle modifiche

| Data | Versione | Che cosa è cambiato |
|---|---|---|
| 04/10/2026 | 0.2 | **Il secondo giro di ricerca, e i fogli di controllo che non esistevano.** Il latino, il greco e il ferrarese sono stati cercati di nuovo cercando **la cosa che si vede** e non la parola che la nomina: alla voce «gli auspici» il lituo dell'augure, non un file che contiene la parola. Le voci **senza nessun candidato** scendono da **34 a 6** — e a **3** nei fogli, che ripiegano sul primo giro — e i candidati delle novanta voci salgono da **417 a 547**. Il **numero** di voci coperte è migliorato, la **correttezza** no: alla voce «i riti funebri» il secondo giro ha restituito un'elimitrice funebre, e il campione dei nomi è in §2.1. Il primo giro **non è stato toccato**: è la prova di che cosa trovava una ricerca che cercava le parole. La Q1 era bloccante perché **manccavano i fogli di controllo** e senza fogli l'attestazione a vista è impossibile: ora ci sono, **18 fogli** da dieci voci, e la Q1 è risolta nel metodo — le immagini le guarda Pietro, io registro i giudizi e lo script **rifiuta** un giudizio senza motivo, con etichetta fra le nove e file fra i candidati guardati. La Q4 è chiusa: le trenta voci ferraresi associano **la cosa che il proverbio evoca**, se esiste ed è vera. Un difetto trovato in sé stesso: il primo tentativo faceva `zip(nomi, termini)` e quindi cercava **il nome italiano della voce** invece del termine inglese — la stessa malattia del primo giro, e l'ho scritta due volte. |
| 02/10/2026 | 0.1 | Prima stesura. Ricerca su Wikimedia Commons delle **180 voci** degli oggetti di interazione, con termini scelti voce per voce: **1120 candidati** con licenza libera, di cui **12 respinti** per difetto automatico. La regola delle quattro categorie, le etichette, la misura 96×72 e la regola del ritaglio dichiarato. Il difetto della ricerca — 67 voci in cui nessun candidato nomina l'oggetto, fra cui il latino a 27 su 28 — dichiarato per esteso, con i sette controlli che lo rendono visibile. **Nessuna immagine scelta, nessuna guardata a vista**: è dichiarato, ed è la prima questione aperta. |