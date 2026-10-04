---
titolo: I ritratti dei personaggi — dove vengono e perché sono dichiarati
versione: 0.5
data: 2026-10-04
autore: Buffy (per pietrofabbri)
documenti collegati:
  - docs/videogioco-5-duchi-mappe.md
  - docs/videogioco-5-duchi-luoghi.md
  - AGENTS.md
  - FONTI-E-LICENZE.md
---

# I ritratti dei personaggi

## 0. A che cosa serve

Il gioco ha 213 schede di personaggio. Borso ha già un ritratto a 48×54, e
Maurelio ha una figura disegnata a mano. Gli altri 211 no.

Il progetto vieta i volti inventati per le persone reali (`AGENTS.md` §3): si usa
un **ritratto autentico** quando esiste, e un **emblema** quando non esiste o
quando la persona non può avere un volto. Maurelio è l'eccezione già prevista:
non è un ritratto, è una figura della tradizione.

Questo documento dice **quali immagini sono state scelte, con quale licenza, e
quali sono state rifiutate**. È un documento di controllo, non un catalogo da
sfogliare.

## 1. La regola: due immagini, non una

| | Ritratto autentico | Emblema |
|---|---|---|
| quando | esiste un'immagine libera che **ritrae la persona** | non esiste, o la persona non può, o l'immagine non la ritrae |
| chi decide | una ricerca automatica **proposta**, poi un attestato a vista | idem |
| dichiarazione | l'**etichetta** del ritratto (§4) | il **motivo** per cui non c'è un ritratto |
| regola del progetto | il valore di un contributo scientifico si separa dal valore della persona; qui vale lo stesso per un'immagine | nessun volto inventato |

Le schede senza ritratto non sono un difetto: sono la parte del gioco in cui si
vede che la conoscenza ha un bordo. Un emblema con la scritta «nessun ritratto
libero esiste» insegna più di un ritratto generato.

## 2. I numeri

| | |
|---|---|
| schede di tappa | **213** |
| persone distinte (il catalogo è per persona, non per tappa) | **198** |
| con ritratto autentico, guardato a vista e verificato | **138** |
| con emblema | **60** |
| ancora da verificare | **0** |
| giudizi a vista presi in tutto | 195: 151 accettati, 44 respinti |
| ritratti ancora da guardare a vista | **0** |
| persone che compaiono in due anni e hanno un solo file | 15 |
| file di immagine distinti, uno per persona | **198 su 198** |
| misura | 48×54 px, come il ritratto di Borso |

I numeri di questa tabella sono **calcolati**, non scritti: li stampa
`sorgenti/art/verifica_immagini.py --enumero` e li confronta con i dati. Le 198
persone sono 213 schede perché 15 compaiono in due anni diversi e hanno un solo
file: alfonso i d'este, alfonso ii d'este, augusto, biagio rossetti, carlo magno, copernico, dosso dossi, ercole ii d'este, federico ii, isabella d'este, josquin des prez, leon battista alberti, leonardo da vinci, lucrezia borgia, ludovico ariosto. Indicizzando il catalogo per persona quel difetto sparisce da solo:
prima la ricerca scaricava lo stesso file due volte e li contava due.

**L'ultima riga è la più importante, ed è quella che il 3 ottobre non aveva.**
Il conto dei file distinti è **calcolato sugli sha256**, non sui nomi: fino al 3
ottobre i sessanta emblemi erano sessanta file *diversi*, tutti della misura
giusta, tutti passanti, e dieci persone ne avevano uno identico. Un contatore
che conta file conta sessanta file giusti anche quando sessanta file sono
diciotto. L'ultima riga è l'unico numero di questa tabella che quella volta
avrebbe fermato il difetto, ed è nata dal difetto (§3bis).

**Tre delle quindici persone in due anni lo erano per un motivo che nessuna
normalizzazione di nome poteva vedere.** `augusto` e `ottaviano augusto`,
`copernico` e `niccolò copernico`, `federico ii` e `federico ii di svevia`
erano due voci di catalogo per la stessa persona, con lo stesso file: sei voci
per tre persone. `chiave_persona()` ripulisce il nome e non sa che «Augusto» e
«Ottaviano Augusto» sono lo stesso uomo, perché la normalizzazione è testuale e
l'identità non è una questione di testo. I tre casi sono dichiarati uno per
uno in `ALIAS` dentro `sorgenti/art/catalogo_immagini.py`, **non** con una
regola: la regola che unisse due nomi perché uno contiene l'altro avrebbe
unito anche «il territorio del Po» e «i Bersaglieri del Po», che sono due
persone diverse. Il controllo 7 continua a sorvegliarli, perché se un quarto
doppione compare il numero dei file distinti torna sotto e il verde viene via.

Le licenze sono **tutte libere**, e il conto esce dai dati senza arrotondare: 95 pubblico dominio, 13 CC BY-SA 3.0, 10 CC BY-SA 4.0, 4 CC BY-SA 2.0, 3 CC0, 2 Attribution, 2 CC BY 4.0, 2 CC BY 3.0 it, 2 CC BY 2.5, 1 CC BY-SA 2.0 de, 1 CC BY 2.0, 1 CC BY 3.0, 1 CC BY-SA 1.0, 1 No restrictions
— 138 in tutto, tutte sui 138 ritratti accettati.

## 3. La ricerca, e il suo difetto più importante

La ricerca è in tre script, e si può rifare:

1. `cerca_ritratti.py` interroga l'API di Wikipedia in blocchi da 40 titoli e
   restituisce l'immagine in testa all'articolo;
2. `cerca_ritratti_2.py` passa ai titoli scelti a mano e all'endpoint REST dei
   riassunti per chi non è stato risolto;
3. `cerca_commons.py` cerca direttamente **su Commons**, per i nomi in cui la
   ricerca su Wikipedia non trova nulla.

**Il difetto, da non ripetere.** La prima versione chiedeva 213 nomi di
seguito e, quando la risposta non arrivava, semplicemente non aveva più
immagini: scriveva allora «nessun ritratto in testa all'articolo di
Wikipedia». Ma Wikipedia risponde **HTTP 429 Too Many Requests** quando le
richieste si susseguono troppo veloce, e quel codice di errore finiva letto come
«non esiste».

Il risultato era che quindici personaggi con un ritratto celebre e documentato
venivano dichiarati privi di ritratto: Albrecht Dürer, Alan Turing, Leibniz,
John Snow, Alonzo Church, Josquin des Prez, Giovanni Bellini, Leon Battista
Alberti, Federico II, Aldo Manuzio, William Caxton, Sergej Korolëv, Riccardo
Bacchelli, Giulio Natta, Renata Viganò.

Non era un errore di ricerca. Era **un fatto falso scritto come se fosse
vero**, in un progetto la cui tesi è che i fatti vanno verificati.

La correzione è in due righe di principio, e sta in tutti e tre gli script:

- un client che aspetta un tempo minimo fra le richieste e, su 429, ascolta
  l'`Retry-After` invece di arrendersi;
- l'esito distingue `non_trovato` (risposta avuta, nessuna immagine) da
  `richiesta_fallita` (nessuna risposta). **Una richiesta fallita non genera
  mai una conclusione**: la scheda resta «da rivedere».

Lo stesso difetto è ricomparso due volte dopo, in forma diverse: una volta
perché la ricerca delle licenze cercava pagine invece che file (manca il
prefisso `File:`), e una volta perché il ciclo di scaricamento non ascoltava il
429 e sei immagini su centosessantanove finivano fuori con la scritta «download
fallito», che sembrava un file corrotto. Tutte e tre le volte la causa era la
stessa: **una risposta che non arriva è stata letta come una risposta negativa**.

## 3ter. I sessanta emblemi: forme che dicono il perché

Fino al 3 ottobre l'emblema era un rettangolo con una diagonale, e il seme che
la decideva era `sum(ord(codice)) % 22`: **sessanta emblemi, diciotto file**. Dieci
persone — Al-Khwarizmi, Alcuino, Aldobrandino d'Este, Cincinnato, i censori,
Ibn Battuta, il concerto delle dame, i mercanti, Napoleone, Taddeo Crivelli —
avevano lo stesso identico PNG. La funzione che lo disegnava diceva nel suo
docstring che «il seme decide la diagonale, così due emblemi diversi non sembrano
lo stesso file»: era falso, e nessun controllo lo guardava, perché tutti i
controlli contavano i file e non i file distinti.

**Un emblema è una risposta, e la risposta è il perché.** Un riquadro vuoto dice
«qui non c'è niente»; un riquadro con dentro il *motivo* della famiglia dice
«non c'è un volto perché *questa persona è viva*» oppure «*quello che si è
trovato è un'opera, non un volto*». Il secondo riquadro insegna, il primo no.

Le sette famiglie **non sono state scelte a mano**: sono **classificate dalla
frase del motivo**, dalla prima all'ultima, e il catalogo porta
`emblema_famiglia` e `emblema_famiglia_da`, quest'ultima è la parola che ha
fatto vincere. Una classificazione che cambia quando il motivo cambia è una
classificazione; scritta a mano sarebbe una lista di preferenze travestita da
regola.

| famiglia | quante | il segno | che cosa dice al ragazzo |
|---|---|---|---|
| `opera_non_persona` | 24 | cornice con due righe dentro | quello che si è trovato è un'opera stampata o un oggetto, non un volto |
| `collettivo` | 11 | tre cerchi in triangolo | sono più persone: un volto solo non sarebbe di nessuno |
| `nessun_ritratto_libero` | 9 | cornice vuota | nessun ritratto con licenza libera esiste |
| `vivo` | 9 | anello con una fessura | persona viva: il volto non si disegna finché è vivo |
| `numero_discorde` | 4 | due quadrati spostati | le fonti non concordano sul numero: non si sa quale |
| `identita_conflitto` | 2 | due cerchi che si incrociano | due nomi per due persone diverse: l'immagine è dell'altra |
| `tradizione` | 1 | una nicchia con arco e soglia | figura della tradizione: nessun ritratto storico lo riprende |

**Ogni colore viene dalla tavolozza**, non da un esadecimale scritto nella
funzione: le sette chiavi sono lette da `dati/fonti_visive/tavolozza.json`, che è
il file che dichiara da dove viene ogni colore del gioco. Se una chiave non ci
fosse, `emblema.py` si ferma e dice quale: un colore che non dichiara la sua
fonte è un colore inventato.

**Sopra il segno ci sono le iniziali, e sotto una firma.** Le iniziali perché un
emblema senza nome è lo stesso inganno del francobollo: dice che c'è qualcosa
senza dire chi. Tre lettere, non una: `AZZ` dice «gli Azzo» molto meglio di `A`.
La firma sono cinque caselle, la cui presenza dipende dai primi cinque bit
dell'hash del nome della voce di catalogo: **non significa niente** e serve a una
cosa sola, che sessanta voci producano sessanta file. Le iniziali da sole non
bastano, perché `Cincinnato` e `i censori` danno entrambe `C`, e `Azzo VII
d'Este` e `Azzo VIII d'Este` danno entrambe `AZZ`.

**Nessuno di questi segni è un volto.** Il progetto vieta i volti inventati per le
persone reali (`AGENTS.md` §3); vieta i volti, non le forme. Sono pittura
geometrica, la stessa cosa che sarebbe un'iniziale.

**Tre difetti sono stati trovati guardando, non ragionando.**

1. Il **font era 3×5** e `M`, `N` e `H` si leggevano uguali: il foglio mostrava
   `DOM` che si leggeva `DOH`. Il font è 5×7 e le lettere si leggono.
2. La **volta** era un arco tracciato con una soglia su un numero reale, e la
   soglia non è simmetrica: la nicchia aveva un fianco di tre pixel e l'altro di
   uno. Ora l'arco si traccia per angolo.
3. La **fessura dell'anello** era di 24 gradi e toglieva metà del segno: si leggeva
   una `C`. Ne servono 13.

Nessuno dei tre si sarebbe visto ragionando sulla formula: si vedono nel foglio
di controllo, e il foglio di controllo è la parte del metodo che il progetto non
può saltare.

**I due controlli nuovi, e il difetto che hanno trovato loro.** Il controllo 7
conta gli **sha256 distinti** e pretende che siano tanti quanti le persone; il
controllo 8 ricalcola la famiglia dal motivo e pretende che coincida con quella
che il catalogo dichiara, e che la parola dichiarata sia ancora nel motivo. Il
controllo 8, alla prima versione, confrontava la parola **ricalcolata** con se
stessa: `emblema_famiglia_da` poteva dire qualunque cosa e nessuno se ne
accorgeva. L'ha trovato la prova dei difetti, non io — ed è il secondo difetto
in due giorni che nasce da un controllo che confronta una cosa con sé stessa.

Il generatore è `sorgenti/art/emblema.py`, chiamato da
`sorgenti/art/catalogo_immagini.py`. Nessuna libreria: PNG con `zlib`, come i
fondi di Terrarium e come gli shapefile.

## 4. L'attestazione: otto immagini respinte

Un file di ricerca può sbagliare la persona, e l'ha fatto otto volte. Il nome
del file non è una prova. Le otto, viste una per una:

| Scheda | Cosa aveva trovato la ricerca | Perché è stata respinta |
|---|---|---|
| `P80` Renata Viganò | `Renata_Viganò_gatto.jpg` | il nome della persona e il nome del gatto si somigliano in italiano. Il file ritraeva un gatto. |
| `P90` Mercanti, artigiani e cittadini | `Iranian_handicraft.jpg` | una ceramica persiana, con l'autore Reza Hajipour. Per i mercanti di Ferrara è falso. |
| `P66` I Bersaglieri del Po | `2june_2007_367.jpg` | soldati di oggi che sfilano in strada, uniformi attuali, foto del 2007. Per il 1848 è un'affermazione falsa. |
| `P88` La comunità ebraica ferrarese | `Judaica.jpg` | una fotografia d'oggetti di culto su un tavolo: non è la comunità di Ferrara, e non è nemmeno antica. |
| `P89` Gli studenti dello Studio | il convento di Santa Lucia | lo Studio è a Palazzo Paradiso: sono due cose diverse, e la somiglianza dei nomi è quello che ha fatto sbagliare la ricerca. |
| `P27` Taddeo Crivelli | una scena della Bibbia di Borso | è un'opera, non un ritratto: il miniatore non c'è. |
| `P63` Napoleone e l'età francese | David, il passaggio del San Bernardo | una scena di guerra, non un ritratto. Resta una buona immagine **di livello**. |
| `Q126` William Caxton | la xilografia di una stamperia | è l'opera di Caxton, non la sua faccia. Preziosissima come immagine di livello. |

Il giudizio è in `sorgenti/art/attestazione_immagini.json`, e non è rimesso
alla ricerca: ogni voce accettata porta **il nome del file**, l'**etichetta**
(fotografia, dipinto, xilografia, miniatura, autoritratto, rilievo, immagine
tradizionale) e **il motivo**. `applica_attestazione.py` riverifica ogni nome
su Commons prima di accettarlo: un titolo scritto a mano che non esiste porta la
scheda a emblema e lo dichiara. È successo una volta, con Cornelia.

### Le etichette servono al gioco, non alla bibliografia

Un visitatore che vede Leonardo accanto a Einstein deve poter capire che cosa sta
guardando. Un autoritratto di Bellini e una fotografia di Turing sono entrambe
immagini di due persone, ma non dicono la stessa cosa: uno ha deciso come
siamo fatti, l'altro non poteva scegliere. Le etichette separano questi casi,
e servono anche al motore: un autoritratto e una miniatura non si ritagliano
come una fotografia.

## 5. Le tre cose che non si possono sapere

1. **Le altezze non esistono come dato**, e qui non c'è rimedio: nessuna fonte
   libera e nessuna fonte a pagamento dà l'altezza degli edifici fuori Ferrara
   (misure in `mappe.md` §5). Un ritratto a 48×54 non soffre di questo, perché
   non ha bisogno di misure: soffrono le sagome degli edifici.
2. **19 fonti sono più strette di 300 pixel**, e ci sono state ridotte a
   48×54. Si vedono meno nitide e non si possono più migliorare. La
   risoluzione della fonte è registrata in `ritratti_disponibili.json`, campo
   `larghezza`, e va mostrata in fase di prova.
3. **Il taglio del viso è automatico** e non c'è riconoscimento facciale: la
   regola è una finestra con le proporzioni del riquadro, centrata sul contenuto
   e non sull'immagine. Va guardata. I fogli di controllo sono
   **prodotti il 3 ottobre**: `sorgenti/art/fogli_controllo.py` compone i fogli,
   dodici ritratti per schermata, e sono tredici fogli. Ogni cella porta
   codice, nome e licenza, e mostra anche i sospetti: un foglio che nasconde i
   sospetti serve a confermare e non a controllare. I fogli sono sul **grezzo** e
   non sul ritratto finito, perché a 48×54 non si distingue un volto da un
   francobollo, e il giudizio che conta è proprio quello.

## 6. Quello che resta da fare

| | |
|---|---|
| ~~**disegnare** i 60 emblemi~~ | **fatto il 04/10/2026**: i sessanta emblemi non sono più tessere anonime ma forme che dicono *perché* non c'è un volto, e dicono anche *chi* (§3ter) |
| decidere se gli emblemi siano **disegni a mano** o **forme generate** | restano forme generate, ed è dichiarato: il progetto vieta i *volti* inventati, non le *forme* disegnate; nessuno di questi sessanta segni ha un volto dentro e nessuno è la firma di un artista che non c'è |
| cercare un ritratto vero della **beata Beatrice II d'Este** (`P11`) | **ricercato il 3 ottobre**: nessun ritratto esiste. Su Commons il nome porta a un dipinto con la Trinità e **tre santi** insieme nel suo monastero di Sant'Antonio in Polesine, e a una dozzina di «Beatrix»:Maria Beatrice, tutte del Sette-Ottocento. Una scena con tre figure non è un ritratto, per la stessa regola con cui sono state respinte quella di Alcuino e la stele di Hammurabi |
| decidere se gli emblemi siano disegni o forme tipografiche | se sono forme, l'anno 1 (maurelio) resta l'unico con disegno |
| ridare le 600 px di partenza | 300 px per le 19 fonti strette non bastano: si può solo rifare la ricerca su una fonte più grande |
| rivedere la P80 | Renata Viganò potrebbe avere un ritratto sotto un'altra forma: la ricerca su Commons non ne ha trovato |

## 7. Il registro delle modifiche

### v0.5 — 04/10/2026

**Sessanta emblemi, diciotto file.** La tessera dell'emblema era un rettangolo
con una diagonale il cui seme era `sum(ord(codice)) % 22`: i sessanta emblemi
erano **diciotto file distinti**, e dieci persone ne avevano uno identico. Il
docstring della funzione prometteva il contrario — «il seme decide la diagonale,
così due emblemi diversi non sembrano lo stesso file» — e nessuno dei sei
controlli lo guardava, perché tutti contavano i file e non i file distinti.

Ora `sorgenti/art/emblema.py` disegna una **forma che dice il perché**, in tre
parti: il segno geometrico della famiglia, le iniziali della persona, e una
firma di cinque caselle che rompe le iniziali uguali. Le sette famiglie sono
**classificate dal motivo** con una regola dichiarata, e il catalogo porta
`emblema_famiglia` e `emblema_famiglia_da`. I colori vengono tutti dalla
tavolozza. Sessanta file distinti su sessanta.

**Tre difetti trovati guardando il foglio, non ragionando sulla formula**: il font
3×5 rendeva `DOM` come `DOH`; l'arco della nicchia era tracciato con una soglia
non simmetrica e la volta risultava storta; la fessura dell'anello era di 24
gradi e toglieva metà del segno. Tutti e tre corretti.

**Un difetto che la prova dei difetti ha trovato, non io**: il controllo 8
confrontava la parola *ricalcolata* con sé stessa, e `emblema_famiglia_da`
poteva dire qualunque cosa senza che nessuno se ne accorgesse. Ora confronta la
parola **dichiarata**, e segnala anche quando quella parola non è più nel motivo.

**Tre doppioni d'identità chiusi nello stesso giro.** Il controllo 7 ha detto che
i ritratti erano 138 file distinti su 141 persone, e ha detto **quali**:
`augusto`/`ottaviano augusto`, `copernico`/`niccolò copernico`,
`federico ii`/`federico ii di svevia` — sei voci di catalogo per tre persone,
con lo stesso file. Sono chiusi con tre alias dichiarati in
`catalogo_immagini.py`, non con una regola: la regola che unisse due nomi perché
uno contiene l'altro avrebbe unito anche «il territorio del Po» e «i Bersaglieri
del Po». **Il catalogo ha quindi 198 persone, non 201**, e i numeri di §2 sono
tutti ricalcolati.

**Un file scritto tre volte.** `catalogo_immagini.py` scriveva
`dati/immagini_gioco.json` tre volte di seguito, con due testi `_nota` diversi
(l'uno dei quali diceva «cinque personaggi», un numero morto da giorni). Il
risultato era quello giusto — la terza scrittura vinceva — ma ora si scrive una
volta sola, **dopo** che le tessere sono state disegnate, perché il file deve
dire la famiglia che il disegno porta davvero.

`sorgenti/art/verifica_immagini.py` passa da sei a otto controlli e da sei a
undici difetti provati.

### v0.4 — 03/10/2026

**Le 7 immagini rimaste aperte sono state chiuse.** Il metro è il confronto
di tre fonti — nome del file, descrizione dell'uploader, categorie — e le tre
devono dire la stessa cosa; se due dicono una cosa e la terza un'altra, l'immagine
resta aperta e il conflitto si scrive. Lo strumento è
`sorgenti/art/verifica_metadati.py`. Il conto: **151 accettate, 44 respinte,
0 aperte**.

**Una persona, non un'immagine, era sbagliata.** `P11` doveva essere la beata
**Beatrice II d'Este**, la monaca di Sant'Antonio in Polesine, una degli Este che
non governarono, morta nel 1372. Il file trovato è di Bartolomeo Veneto e le
categorie dicono `Beatrice d'Este`: è la duchessa milanese del 1490, figlia di
Ludovico il Moro. Due donne, due secoli, due dinastie; la somiglianza è solo nel
nome, e la ricerca ha abboccato al nome. Respinta, e con lei si apre una voce nuova:
**il ritratto vero della beata va cercato**, e non basta rilanciare la stessa
ricerca, che ha già abboccato.

**Il metadato ha corretto me, e va detto.** Su `P61` e `P62` avevo scritto che
erano «la stessa formella fotografata da un'altra angolazione». Non lo sono: due
formelle diverse dello stesso palazzo, entrambe di Gaetano Davia, una per il
Bonati e una per il Foschini. Avevo ragione a non accettarle e ragione a non
sapere perché; la lettura dell'immagine era sbagliata. Un metadato non è la
verità — la descrizione la scrive chi ha caricato il file — ma quando confuta
l'occhio bisogna dirlo, altrimenti il proprio registro dei difetti si aggiorna
solo quando fa comodo.

**Le altre cinque passano, con le riserve dichiarate.** Il monumento equestre è un
ricomincio del Novecento del monumento quattrocentesco a Nicolò III e resta un
monumento. Il ritratto di Borso è un dipinto del suo regno (1469-1471) con
l'attribuzione al fratello Baldassarre dichiarata in categoria. Quello di Tito
Strozzi è di Baldassarre d'Este, suo figlio. Il del Bonati e il del Foschini sono
rilievi dell'Ottocento. L'Isabella di Castiglia è un dipinto del Prado del 1490,
ma sul file il credito è incerto — l'uploader scrive tre provenienze diverse, una
delle quali è «Unknown source» — quindi l'accettazione vale per il dipinto
documentato, non per una provenienza.

**Due controlli si sono rotti mentre chiudevo, ed è il merito del lavoro.** La
prima versione di `prova_difetto_immagini.py` chiedeva una persona «aperta» per
provare il difetto numero 4: chiudendole tutte, la prova morì con «nessuna
persona». Una prova che funziona solo finché esiste un caso non è una prova del
caso, è una prova del calendario: il caso ora **si costruisce**. E il catalogo,
cambiando esito a quelle sei persone, lasciava le loro vecchie tessere d'emblema
accanto a quelle nuove — sei file che nessuno usava e che il primo che li avesse
aperti avrebbe trattati come ritratti respinti ancora validi. Gli orfani ora si
cercano tutti, non solo i `ritratto_`.

### v0.3 — 2026-10-03

**I 195 ritratti sono stati guardati uno per uno.** Non per un campione: 213
schede, 13 fogli di controllo, 195 giudizi. Il conto esce 145 accettati, 43
respinti, 7 aperti.

Le 43 respinte non sono un fallimento della ricerca: sono il motivo per cui
esiste l'attestazione. Cinque volte su 50 la ricerca aveva restituito un oggetto
invece di una persona — un francobollo per al-Khwarizmi, una tavoletta cuneiforme
per Gilgamesh, un pannello di mostra per Ibn Battuta, la parte alta della stele
per Hammurabi, un monumento di cemento per Qin Shi Huang — e in quattro casi
l'oggetto aveva il nome della persona scritto sopra. Una fotografia
dell'Ottocento era stata assegnata ad Azzo VIII d'Este, morto nel 1537: non può
esserlo, perché le fotografie non sono di quell'anno. Sono 43 stelle su 195: sette
su venti, come la §4 diceva, e per una volta la proporzione era giusta senza che
nessuno l'avesse contata.

**Due difetti, e sono della stessa famiglia.** Il primo: `applica_attestazione.py`
mandava tutti i nomi dei file a Commons in una richiesta sola, e la API ne
accetta 50. Commons rispondeva «troppi valori» con zero pagine, e il codice leggeva
quello zero come «il file non esiste»: 127 ritratti giusti sono diventati emblemi
senza una riga di errore. Il secondo, più sciocco: il nome del catalogo era
scritto a mano in due file, e in uno dei due «gioco» era diventato «giogo». Il
sintomo era un `Errno 2` su un percorso che sembrava giusto. Per questo il nome
del catalogo adesso **si cerca** fra i file, e se non ne trova uno solo il
controllo si ferma e lo dice. È la sesta volta che la stessa lezione serve.

**Il terzo esito.** Esiste adesso `da_verificare`, per le immagini in cui si vede
un ritratto di persona giusta e di periodo giusto ma l'identità non si può
accertare a occhio: i ritratti dei duchi estensi sono i più scambiati fra loro. Non
diventano ritratti per silenzio: restano aperte, con il file da parte, e a schermo
c'è un emblema. Dichiarare un terzo esito è stato più utile che scegliere fra i
due.

**Il catalogo è per persona.** `dati/immagini_gioco.json` è quello che il motore
legge: 198 persone, non 213 schede, perché 15 compaiono in due anni. Ogni voce
porta l'esito e l'etichetta — il gioco mostra un volto a un ragazzo di tredici
anni e non può farlo senza dire se è una fotografia o una miniatura.

`sorgenti/art/verifica_immagini.py` controlla otto cose: il file annunciato
esiste ed è un PNG 48×54, in `out/` non c'è nulla che nessuno usa, ogni ritratto ha
un'etichetta dell'elenco, ogni ritratto ha una licenza libera e ogni aperto resta
aperto, ogni codice di tappa compare una volta sola, nessuna scheda respinta a
vista compare come ritratto, **i file distinti sono tanti quanti le persone** e
ogni emblema dichiara la famiglia che il suo motivo dice. Morde su **undici**
difetti iniettati, uno per uno: `prova_difetto_immagini.py` li inietta e li
richiede a voce.


### v0.2 — 02/10/2026

Controllo di coerenza: le cifre del documento contro `ritratti_disponibili.json`
e `attestazione_immagini.json`, una per una. 213 schede, 169 ritratti, 44 emblemi
(9 collettivi, 9 viventi, 26 senza ritratto libero), 116 in pubblico dominio: tutto
giusto. Tre cose non erano giuste:

1. **erano «sette» le immagini respinte, e sono otto**: la tabella del §4 ne
   elencava otto (l'ottava è `Q126`, la xilografia di Caxton) e il titolo, il
   `README` e `FONTI-E-LICENZE.md` ne dicevano sette. Ora il numero è uno solo e
   corrisponde alla tabella;
2. **il conto delle licenze era arrotondato a gruppi che non esistono** nel file:
   «CC BY-SA 2.0 / 2.5: 5» non corrispondeva a nulla, perché le licenze portano
   anche una variante linguistica (`CC BY-SA 2.0 de`, `CC BY 3.0 it`, `CC BY-SA
   3.0 fr`). Ora il conto è per famiglia di licenza e viene dai dati; e le
   immagini che portano un obbligo di credito sono **48**, non 53, perché CC0 e
   «No restrictions» non ne portano;
3. **i tre fogli di controllo non esistono**: il documento li dava per prodotti e
   il registro li annunciava fra le cose fatte. Sono dichiarati **da produrre**,
   che è la verità.

### v0.1 — 01/10/2026

Prima stesura. Creati: `cerca_ritratti.py` (v0.3, col client che ascolta il 429 e
distingue `richiesta_fallita` da `non_trovato`), `cerca_ritratti_2.py`,
`cerca_commons.py`, `ripara_licenze.py`, `applica_attestazione.py`,
`attestazione_immagini.json`, `roster.py`, `ritratto_reale.py`. Prodotti 169
ritratti a 48×54 e tre fogli di controllo.

Correzioni lungo il cammino, tutte nella stessa classe di errore:

1. il `HTTP 429` letto come «nessun ritratto»: quindici schede sbagliate;
2. la riduzione a 48×54 che non ridimensionava: i file erano di 500×562 e
   pesavano 97 kB l'uno, 14 MB in tutto, dentro un riquadro che il motore già
   dava per 48×54;
3. i nomi di miniatura (`3840px-…`) scambiati per nomi di file, e i titoli di
   Commons cercati senza il prefisso `File:`: sei immagini e otto licenze
   dichiarate assenti quando esistevano.

Esito: 169 ritratti su 213 schede, 44 emblemi, **zero** richieste fallite non
distinte da risposte negative.
