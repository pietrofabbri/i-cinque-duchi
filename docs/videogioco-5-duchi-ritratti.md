---
titolo: I ritratti dei personaggi — dove vengono e perché sono dichiarati
versione: 0.3
data: 2026-10-03
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
| persone distinte (il catalogo è per persona, non per tappa) | **201** |
| con ritratto autentico, guardato a vista | **135** |
| con emblema | **59** |
| ancora da verificare, quindi **non** mostrate come ritratto | **7** |
| giudizi a vista presi in tutto | 195: 145 accettati, 43 respinti, 7 aperti |
| ritratti ancora da guardare a vista | **0** |
| persone che compaiono in due anni e hanno un solo file | 12 |
| misura | 48×54 px, come il ritratto di Borso |

I numeri di questa tabella sono **calcolati**, non scritti: li stampa
`sorgenti/art/verifica_immagini.py --enumero` e li confronta con i dati. Le 213
persone sono 213 schede perché 12 compaiono in due anni diversi e hanno un solo
file: alfonso i d'este, alfonso ii d'este, biagio rossetti, carlo magno, dosso dossi, ercole ii d'este, isabella d'este, josquin des prez, leon battista alberti, leonardo da vinci, lucrezia borgia, ludovico ariosto. Indicizzando il catalogo per persona quel difetto sparisce da solo:
prima la ricerca scaricava lo stesso file due volte e li contava due.

Le licenze sono **tutte libere**, e il conto esce dai dati senza arrotondare: 97 pubblico dominio, 10 CC BY-SA 3.0, 9 CC BY-SA 4.0, 8 CC BY altri, 6 CC BY-SA 1.0/2.0, 3 CC0, 1 Attribution, 1 No restrictions — 135 in tutto, tutte sui 135 ritratti accettati. Le tessere d'emblema sono opere del progetto e non hanno licenza da dichiarare.

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
| chiudere le **7** immagini ancora da verificare | sono le 7 in cui si vede un ritratto giusto di periodo ma non si può accertare di chi è: il metadato di Commons lo dice, e finché non lo si guarda restano aperte e a schermo c'è un emblema |
| **disegnare** i 66 emblemi | le tessere esistono e sono un segnale dichiarato, ma non sono disegni: ogni emblema deve dire *perché* la persona non ha un volto qui |
| decidere se gli emblemi siano disegni o forme tipografiche | se sono forme, l'anno 1 (maurelio) resta l'unico con disegno |
| ridare le 600 px di partenza | 300 px per le 19 fonti strette non bastano: si può solo rifare la ricerca su una fonte più grande |
| rivedere la P80 | Renata Viganò potrebbe avere un ritratto sotto un'altra forma: la ricerca su Commons non ne ha trovato |

## 7. Il registro delle modifiche

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
legge: 48 persone, non 54 schede, perché 201 compaiono in due anni. Ogni voce
porta l'esito e l'etichetta — il gioco mostra un volto a un ragazzo di tredici
anni e non può farlo senza dire se è una fotografia o una miniatura.

`sorgenti/art/verifica_immagini.py` controlla cinque cose: il file annunciato
esiste ed è un PNG 213×12, in `out/` non c'è nulla che nessuno usa, ogni ritratto ha
un'etichetta dell'elenco, ogni ritratto ha una licenza libera e ogni aperto resta
aperto, e ogni codice di tappa compare una volta sola. Morde su sei difetti
iniettati, uno per uno: `prova_difetto_immagini.py` li inietta e li richiede a
voce.


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
