---
titolo: Videogioco "I cinque duchi" — Storico: come ci si è arrivati
tipo: storico
versione: 0.2
data: 2026-10-06
autore: Pietro Fabbri (con Claude)
documenti collegati: videogioco-5-duchi-roadmap-documentazione.md (v0.2)
---

# Storico del progetto

Questo documento raccoglie **come ci si è arrivati**: i difetti trovati, le prove fatte, le decisioni prese e poi cambiate, le lezioni di metodo con la loro occasione. Non dice che cosa è deciso oggi: quello lo dicono i documenti normativi, al presente.

## 0. Come si legge, e come si scrive

- **Il testo qui è spostato, non riscritto.** Ogni voce è stata tolta da un documento del progetto il giorno indicato e riportata alla lettera: le cifre e le versioni citate sono quelle del giorno in cui la voce è stata scritta, e **non si aggiornano**. Per lo stato di oggi vale il documento d'origine.
- **Ogni voce dice da dove viene**: il documento, la sezione com'era intitolata, la versione del documento da cui è stata tolta, e dove si trova ora la regola o il dato che quella voce raccontava.
- **Il documento d'origine tiene il presente.** Al posto della voce resta la regola, la decisione o il dato che ne è venuto, con un rimando a questo documento.
- **Le voci sono raggruppate per documento d'origine**, nell'ordine in cui la roadmap li tratta. Dentro ogni gruppo, nell'ordine in cui stavano nel documento.
- **Nessun controllo confronta i numeri di questo documento**: descrivono il giorno in cui ogni voce è stata scritta, come le righe dei registri delle modifiche, e leggerli come il presente sarebbe un difetto (`dati/buchi_aperto.json`).

## 1. Dall'audit

Le sezioni che l'audit (`audit.md`) aggiungeva dopo ogni chiusura e dopo ogni lezione di metodo, fra il 02 e il 05/10/2026. Sono state tolte dalla v0.25 dell'audit il 06/10/2026. L'esito di ogni questione chiusa è oggi nella tabella `audit.md` §7; le regole di metodo che queste sezioni raccontano sono in `AGENTS.md` §4.

### 1.1 2bis. B5 chiusa: cosa è costato verificare i pin

*Da `audit.md` v0.25, sezione «2bis. B5 chiusa: cosa è costato verificare i pin».*

*(02/10/2026 — `sorgenti/gis/verifica_pin.py`, otto controlli, tutti superati; `mappe.md` §8bis)*

Il numero dell'audit era giusto e la sua etichetta era sbagliata: i **novanta** non sono novanta pin distinti, sono novanta **slot di pin**, uno per tappa. Dietro ci sono 69 posti, e i posti che hanno coordinate sono 39.

| | slot | posti |
|---|---|---|
| anni 2, 3 e 4 | 90 (30 per anno) | 69 |
| con coordinate, verificati | **53** | **39** |
| senza coordinate, tutti con stato dichiarato | 37 | 37 |

**Il quinto anno è passato dagli stessi controlli lo stesso giorno**, perché il verificatore non era scritto per gli anni 2-4 ma per tutti: 30 slot, 15 posti con coordinate, **nessun difetto**. Portato a tutti e cinque gli anni, il conto è 120 slot e 71 con coordinate.

**I due difetti che sono usciti** non sono nella tabella delle tappe e non si vedrebbero mai guardando i documenti: sono nella tabella delle coordinate.

- **Baghdad**, 34 km a sud del proprio centro. La latitudine era `33.03333` invece di `33.31528`: una cifra. Il file lo dichiarava `verificata`, e lo era stato davvero — la fonte, l'articolo italiano di Wikipedia, riporta 33°02′ N. **Il dato era fedele alla fonte e la fonte era sbagliata**, e solo il confronto con un secondo file lo ha fatto vedere.
- **Karakorum**, che cadeva in **Cina**. Il nome aveva risolto sull'articolo della catena montuosa, non su quello della città. La quota lo aveva già sospettato (8 128 m), e il punto-in-poligono dà la prova che mancava: la coordinata è dentro `CHN`.

**Il caso che non è un difetto**, e che vale quanto i due difetti: **Costantinopoli** non cade in nessun Paese, a nessuna delle tre scale, perché il Corno d'Oro è stretto e la terra è a 1,4 km. Un controllo che avesse detto «in mare, errore» avrebbe fatto riscrivere una coordinata giusta. La soglia dei 3 km è dichiarata nel codice per questa ragione.

**Che cosa resta**: diciannove pin non sono verificabili sull'unità amministrativa, perché il file amministrativo non copre quei Paesi. Non è un buco del gioco, è una copertura mancante di un file che si può scaricare.

**La lezione, che è la stessa di tre volte**: questo progetto ha risolto **un titolo** invece di un luogo (Karakorum due volte, Castel del Monte una volta, Baghdad per la cifra). Il controllo automatico batte la lettura, e questa è la prima volta che lo si vede su un numero che qualcuno aveva firmato come verificato.

**E una lezione sulla lezione.** Il quinto anno non ha prodotto difetti, ma ha prodotto **due errori nella tabella di attese del verificatore** (Rotterdam non è nella provincia che il file chiama «Zelanda»), dopo il primo su Castel del Monte. Il controllo che segnala un'attesa sbagliata vale quanto quello che segnala un pin sbagliato, e una tabella scritta a mano è essa stessa un dato da verificare. **Tre volte su quattro, l'errore era di chi scriveva il controllo**: è la misura onesta di quanto sia facile sbagliare una coordinata con la fonte giusta.



### 1.2 3bis. Quattro importanti chiuse il 3 ottobre

*Da `audit.md` v0.25, sezione «3bis. Quattro importanti chiuse il 3 ottobre».*

*(03/10/2026 — le quattro sono I2, I3, I4 e I19, e nessuna delle quattro aspettava una decisione)*

La sezione 3 era la più lunga del documento e le sue prime tre voci erano tre lavori che il progetto poteva fare da solo. Le tre sono fatte, in quest'ordine, e l'ordine è dichiarato perché l'ordine è una decisione. La quarta, I19, è arrivata dopo e ha portato con sé un difetto che nessuna delle altre tre aveva trovato.

**I2, la tavolozza.** `dati/fonti_visive/tavolozza.json`, **18 voci**. La domanda aveva due metà — ricolorare tutto a una tavolozza unica, oppure dichiarare i colori di ogni fonte — e la seconda era quella coerente con le tre regole già prese su etichette e proporzioni. Costruirla ha trovato tre difetti che valgono quanto la tavolozza: **un pigmento non si cerca per nome** («vermilion» è una città canadese, «red ochre» un premio televisivo), **`P462` non è l'esadecimale** ma un link a un oggetto colore, e il suo valore è un dizionario e non una stringa, e **cinque pigmenti su quindici non hanno codice in nessuna fonte**: nessuno dei cinque è stato riempito con una cifra plausibile. Il `verifica_tavolozza.py`, sei controlli, è stato eseguito **in rete**: 10 fonti ricontrollate, **0 problemi**.

**I3, le sagome degli edifici.** `dati/edifici_footprint.json`, 1,6 MB, **5209 edifici su 54 luoghi**. La valutazione che c'era in questa riga diceva «sì, ma non è la prima cosa: prima la tavolozza» — ed è l'ordine in cui sono state fatte. Il risultato che conta non è il numero di edifici ma la rinuncia dichiarata: **3336 edifici su 5209 non hanno altezza** in OSM, e diventano un volume neutro dichiarato invece di una stima. Una forma che non è verificata non si disegna, ed è la regola che il progetto si era già data sui luoghi senza coordinate.

**I4, il fondo di Ferrara.** `dati/ferrara_fondo.json`, 14 tratti di mura OSM, **8601 m di perimetro e 4,20 km²**, con la tolleranza di 60 m scelta **non a occhio ma come la più piccola in cui tutte e 28 le tappe del primo anno cadono dentro**. Una fonte è stata rifiutata e dichiarata: la relation OSM «Centro storico», che copre 1,34 km² e lascia fuori Piazza Ariostea e Palazzo dei Diamanti. Il vuoto più grosso — **1037 m** di mura che nessuna fonte disegna — resta dichiarato.

**I19, i colori dei fondi geografici.** `dati/fonti_visive/colori_cartografici.json`, **19 voci**: 16 dichiarate con motivo e criterio, 3 prese dalla tavolozza con la chiave dichiarata e l'esadecimale confrontato byte per byte. La valutazione che c'era in questa riga diceva «costa mezz'ora» ed era ottimista: il file è un'ora, i due verificatori che lo tengono fermo sono un'altra, e **cercandolo è saltato fuori un difetto che non era di colori**. `dati/mondo_admin1_copertura.json` stava **dentro `dati/mappe/`**, dove vale la regola che ci stanno solo file nel formato a delta, e faceva crashare `mappe_lettore.leggi()` con un `IndexError: list index out of range`: il peggiore dei sintomi, perché dice una lista troppo corta e non dice che il problema è un file che non aveva niente a che fare lì. Il file è stato spostato in `dati/`, il lettore ora controlla la forma del file e solleva un `ValueError` che la dice, e il controllo **C6** tiene la regola ferma. Nello stesso giorno sono entrati anche i **tre file delle cime** (`mappe.md` §2.5), con la scoperta che la fonte è **mondiale in tutte e tre le scale** e che i tre file **non sono annidati**.

**E un quarto file, che non era una domanda ma senza il quale i tre sarebbero stati tre tavole isolate.** `dati/ambienti_livelli.json` è **un ambiente per ognuno dei 150 livelli**, costruito sul modello dell'unica zona già esistita (la tappa 1-1) e con tutti i vuoti dichiarati: 99 ambienti con coordinate, 69 con sagome, e **uno solo che il motore ha davvero disegnato**. È il file che risponde alla domanda che nessuno aveva scritta: «e quindi, che cosa si disegna a ogni tappa?». Nello stesso giorno è entrato anche `mondo_admin1.json`, che chiude in `mappe.md` §2.4 la copertura amministrativa mancante: **54 pin coperti su 54**.

**Che cosa insegna, tenendo conto delle altre.** Sono sei chiusure in tre giorni, e cinque delle sei erano lavori. Le uniche decisioni che il progetto ha preso da solo in questa settimana — ODbL, la regola dei due strati — hanno tutte e due tolto lavoro. È la stessa frase che la v0.4 faceva con una chiusura, e con cinque vale ancora di più.



### 1.3 3ter. Altre sei chiuse il 3 ottobre, e una di loro era un difetto travestito da domanda

*Da `audit.md` v0.25, sezione «3ter. Altre sei chiuse il 3 ottobre, e una di loro era un difetto travestito da domanda».*

*(03/10/2026 — lavoro della sera, dopo la scelta dei premi. Nessuna delle sei era bloccante, e una delle sei non era una domanda)*

| voce | stato | che cosa è successo |
|---|---|---|
| **Il numero dei livelli trasversali** | **chiusa** | Sono **zero**: il trasversale è un aggancio dentro i livelli, non un livello (`quadro-trasversale.md` §1.3). Il conto dei premi è quindi **1050**, non i «circa 900» che il progetto portava da tre giorni: la cifra vecchia contava i soli livelli linguistici e dimenticava i centocinquanta informatici. Un numero che si sbaglia di un sesto è un numero che non si può usare per scrivere un catalogo |
| **La variante dei premi** | **chiusa** | Un premio per livello, 1050 record (`premi.md` §4.0) |
| **Il premio della LIS** | **chiusa** | La categoria **K**: la scheda che il giocatore produce. Non esistono 150 figure sorde documentabili (`premi.md` §2.1) |
| **`osservazione e attenzione`** | **chiusa, ed era un difetto** | Due documenti dicevano che il dominio «non esiste ancora» e lo lasciavano `da_costruire`. Esiste in quattro posti che nessuno aveva messi insieme: il nucleo `Q8.2` del livello 3-27, l'osservazione linguistica dei novecento livelli, le tappe 1-23 e 1-29, la 5-11. Una cosa che il gioco fa senza dirlo non è una lacuna: è una riga rimasta indietro |
| **La 3-28** | **chiusa** | Manchester nel registro, Torino nel documento: era una divergenza dichiarata, e l'ha chiusa la rigenerazione. Il registro ora prende il luogo dalla riga della tabella |
| **La 4-16** | **chiusa davvero** | Era un dato corretto a mano che nessuno poteva rifare. Ora la catena `estrai_luoghi.py` → `coordinate.py` → `classifica.py` lo produce, e `verifica_catena_luoghi.py` lo controlla |

**La quarta è la più instructive, e il titolo della sezione è voluto.** Un dominio dichiarato assente è la cosa più economica che si possa scrivere: non richiede di cercare niente, e la riga sembra onesta («non lo abbiamo costruito»). Ma la domanda vera era **«dove lo abbiamo costruito senza accorgercene?»**, e la risposta era in quattro posti che nessuno aveva leti insieme. Il difetto non era la lacuna: era la domanda che non era stata fatta.

**E le tre difettose che sono venute fuori mentre si chiudeva.** La catena dei luoghi non è mai stata eseguita end to end, ed eseguendola sono usciti tre difetti che nessun controllo vedeva: `estrai_luoghi.py` leggeva le colonne per numero e nell'anno 5 leggeva la stanza al posto della voce (29 tappe su 30 con il filone del *Furioso* al posto della persona); le correzioni di Baghdad e Karakorum vivevano solo in un JSON editato a mano e sparivano alla prima rigenerazione; `classifica.py` aveva due copie della regola che assegna lo stato della coordinata, e le due copie erano già divergenti. Tutte e tre sono chiuse, e `sorgenti/verifica_catena_luoghi.py` ha cinque controlli che le mordono.



### 1.4 3quater. La parte orale: un documento che risponde a una domanda, e un difetto nel README

*Da `audit.md` v0.25, sezione «3quater. La parte orale: un documento che risponde a una domanda, e un difetto nel README».*

*(03/10/2026 — dopo la richiesta di Pietro su speaking e listening)*

`videogioco-5-duchi-parlato.md` (v0.2) chiude il «si può fare» di ascolto e parlato, e
la risposta è articolata in **cinque livelli** invece che in un sì. I quattro fatti che
la costringono:

1. **La Web Speech API è esclusa**: su Chrome manda l'audio ai server di Google e non
   funziona offline. Un gioco senza server non può mandare la voce di un adolescente
   fuori dal dispositivo.
2. **Il materiale esiste per tre lingue e non per le altre**: su Wikimedia Commons, via
   `cerca_audio_oggetti.py`, ci sono **89 381** registrazioni in inglese, **9 179** in
   italiano, **79** in greco, **24** in latino e **zero** in ferrarese.
3. **Il riconoscimento on-device esiste ma non per il ferrarese**, e su una voce di
   minore è una decisione di privacy, non una scelta tecnica.
4. **Il gioco può comunque allenare il parlato**, perché durata, pause, ritmo e
   riascolto si misurano senza riconoscere niente.

Il numero che conta è il secondo: **la lingua di cui il progetto ha più bisogno di
ascolto è l'unica che non ha una registrazione libera al mondo**. La risposta non è
cercarla, è **produrla**: il gioco chiede a chi parla la lingua e mette la registrazione
nel quaderno del giocatore. È la stessa forma della categoria K per la LIS — **il
gioco non sa fare una cosa, e non finge: mette dentro la cosa che non sa fare il
giocatore**.

Cinque decisioni sono di Pietro e restano aperte (`parlato.md` §6): il permesso del
microfono, l'audio nel file di consegna, le opere intere, l'apertura del
riconoscimento on-device, e chi raccoglie le registrazioni dei nonni ferraresi.

**E un difetto vero, trovato per via.** Mizando la tabella dei documenti del README,
uno script ha scritto la versione nella cella del nome del file: **otto righe su
trenta avevano perso il documento che descrivevano**, e la coerenza diceva zero perché
una riga senza nome non nomina nessun documento e quindi non può contraddirlo. Le righe
sono state ricostruite e il controllo che mancava è stato scritto: ogni riga
numerata della tabella deve nominare un file che finisce in `.md` e deve finire con una
versione. Provato, e morde.



### 1.5 3quinquies. La lezione di oggi: un numero scritto a mano invecchia, un numero calcolato no

*Da `audit.md` v0.25, sezione «3quinquies. La lezione di oggi: un numero scritto a mano invecchia, un numero calcolato no».*

*(03/10/2026 — Cercando le cose lasciate in sospeso)*

Non è una voce dell'audit e non la conta: è una regola di metodo, e le due sono
distinte per una ragione che questa sezione dimostra.

Cercando che cosa fosse rimasto aperto, l'ho trovato in `mappe.md` §11 un punto
che chiedeva gli ambienti dei centocinquanta livelli: **il file c'era, completo al
150 su 150, da due giorni.** Una riga di «cosa c'è da fare» che non corrisponde
a nessun lavoro mancante è una riga che mente, perché costringe a rileggerla e a
chiedersi se il lavoro sia ancora da fare.

Chiudendola sono tornato alla sezione che l'aveva prodotto, e **i suoi numeri non
erano più quelli del file**: 99 ambienti con coordinate dichiarati contro 100 reali,
69 sagome OSM contro 68, `citta_antica` 11 contro 12, `percorso` 11 contro 10, e
tre cifre nei vuoti. La frase più falsa diceva che «la 1-1 ha un orientamento e gli
altri 149 no», mentre **nessuno** dei centocinquanta lo ha.

**Perché sette verifiche non lo avevano visto.** B1 confronta i livelli con lo
schema, B3 e B4 confrontano l'ambiente con il registro dei luoghi, B5 i tipi e le
griglie, B6 i vuoti. Sono tutti confronti **fra dati**: nessuno confronta un dato
con **le frasi che il documento scrive su quel dato**. Eppure il documento è la
cosa che legge una persona, e l'unica che può dirle che il gioco ha cento
posizionamenti quando i dati ne hanno novantanove.

Il controllo che mancava è **B8**, in `verifica_ambienti.py`: legge `fonti-visive.md`
§3.6 e confronta ogni numero con il conto — le tre quote della tabella, i nove tipi
e tutti i vuoti. L'ha scritto il difetto: ne ha trovati sette in una volta sola, e
poi è stato provato con difetti iniettati su tre vie (una quota, un tipo, un vuoto)
e ha morso tutte e tre.

E la parte che dura di più: le due frasi che il **file di dati scrive su se stesso**
in `ambienti_livelli.py` erano scritte a mano, e dicevano ancora «le 51 tappe» quando
le ipotesi erano **50** — la 4-16 aveva trovato la sua coordinate il giorno prima.
Ora sono calcolate. La regola è in `AGENTS.md`: **un numero in letteratura invecchia
e nessuno lo rilegge; un numero calcolato cambia da solo quando il dato cambia
sotto di lui.**

Il punto più fastidioso, e utile: **è stata una riga di metodo, non un lavoro, a
far trovare il difetto.** Nessuno dei duecento dati aveva un problema. Il problema
era che un documento li raccontava male, e la catena di generazione era senza
prendersi la briga di controllare la propria prosa.



### 1.6 3novies. Il contatore guardava l'audit con se stesso: i numeri che il resto del progetto copia non erano controllati

*Da `audit.md` v0.25, sezione «3novies. Il contatore guardava l'audit con se stesso: i numeri che il resto del progetto copia non erano controllati».*

*(04/10/2026)*

Il buco era dichiarato da tre giorni e non era un buco di numeri: era un buco di **controllo**. `sorgenti/lingue/conta_questioni.py` confrontava il proprio conto con i numeri dell'audit, e lo faceva bene — quello del §3octies, quando la tabella al posto della prosa. Ma il confronto era **fra l'audit e se stesso**, e tutto il resto del progetto copia quei numeri a mano: la riga 22 del `README.md`, la nota sull'audit, il frontespizio, i titoli delle sezioni 2 e 3. Un numero che quattro documenti riportano e che nessuno conta è un numero che invecchia quattro volte più in fretta di uno.

**I quattro difetti, che sono tutti la stessa cosa** — un numero scritto a mano che nessuno ricalcolava:

  - le **sezioni** dichiarate erano **15** e sono **16**: `itinerari.md` ha aperto la sua il 03/10 e la riga è rimasta indietro. Il frontespizio diceva «lettura di tutti i quindici documenti di progetto», che è doppiamente falso: i documenti sono **31**, e sedici di loro hanno una sezione;
  - `itinerari.md` non compariva in **nessuna intestazione del §4**. La sua voce aperta — *le cinque tappe del primo anno senza facoltativi: sono un dato o una dimenticanza?* — era contata nel totale e non elencata da nessuna parte: la somma delle intestazioni non tornava con nessuna delle due cifre, e nessuno l'aveva notato perché nessuno le sommava;
  - tre numeri del §4 erano **sbagliati di uno o due**: `fonti-visive.md` diceva 2 su 1, `anno3-europa.md` diceva 7 su 6, `furioso.md` diceva 2 su 1. Il criterio, una volta dichiarato, è **le voci aperte di quel documento meno le importanti che il §3 elenca già** — il §4 si intitola «Le altre», e contare anche le importanti sarebbe doppio. Ma il criterio era implicito, e un criterio implicito non è un criterio: chi lo scriveva non sapeva di dover sottrarre, e il numero che ne usciva era quello che gli veniva in mano;
  - il §6 scriveva «nessuna delle **ventotto** chiuse le toccava» con **31** chiuse, e il `README.md` scriveva «il progetto ha **sedici** documenti» con **31** documenti in `docs/`.

**Il difetto nel difetto, che è il quinto caso della regola.** Il confronto dei numeri **in lettere** — «le quattro bloccanti», «le quindici importanti», «nessuna delle chiuse di allora» — non esisteva, e quando è stato scritto ha morso subito: il dizionario delle parole italiane non riconosceva **`trentuno`**, **`ventuno`** e **`ventotto`**, che sono le tre forme in cui una parola non si somma. Le altre si sommano e il dizionario le aveva; queste no, e il risultato è che il confronto **ignorava in silenzio proprio i numeri che il documento scrive in lettere**: tornava verde non perché il numero fosse giusto, ma perché non lo guardava. È la stessa malattia del 03/10, quando cercava «**N** chiuse» in un documento che scrive i numeri in tabella: un controllo che non trova la parola che cerca è un controllo che non guarda, e il suo verde non significa niente.

**Ora il confronto è cinque volte, e copre quello che il progetto legge davvero**: la tabella del §1, le due frasi in prosa, il **numero delle sezioni**, i **numeri per documento del §4** con la loro somma contro le aperte meno le importanti, i **numeri in lettere** dei titoli e delle celle, e i **numeri che il README copia** — cinque nella riga della tabella dei documenti, cinque nella nota sull'audit, più il numero dei documenti di progetto. Il registro delle modifiche è escluso, e lo è dichiarando perché: i suoi numeri sono quelli di quando sono scritti, e un controllo che urlerebbe su ogni versione passata verrebbe spento per legittima ragione.

**E la prova dei difetti, `sorgenti/lingue/prova_difetto_questioni.py`, ne inietta quindici** — i quattro di sopra più gli altri undici, fra cui una cifra senza il nome del suo documento, una cella che passa dalla cifra alla parola, e le cinque vie del README — e richiede che **tutti e quindici** siano visti. Lavora su una **copia** di tutti i trentauno documenti, non sui file veri: una prova che scrive sull'audit e lo rimette è una prova che, se muore a metà, lascia sbagliato il documento più usato del progetto. E ha una seconda parte, che è la più facile da sbagliare: una riga di registro con i numeri di allora **non** deve produrre alcun problema, e la prova lo richiede per iscritto.

La sua seconda parte ha già morso una volta, nella prova stessa: le quattro iniezioni sul README erano scritte `(r, sostituisci(r, …))` invece di `(t, sostituisci(r, …))`, e finivano per **sovrascrivere l'audit con il README**. La prova si annullava da sola e non se ne accorgeva, perché un difetto che non guarda non produce un errore. Ora l'ordine è scritto dentro la prova, e un'asserzione si rifiuta di procedere se il primo valore non è l'audit. **Una prova che non osserva nulla non ha nessun valore, e il suo fallimento va letto come un difetto della prova** — la lezione del 03/10, che qui si è ripetuta letteralmente.



### 1.7 3decies. Il quarto numero che invecchiava: nessuna mappa diceva da dove viene

*Da `audit.md` v0.25, sezione «3decies. Il quarto numero che invecchiava: nessuna mappa diceva da dove viene».*

*(04/10/2026)*

Il §3novies ha chiuso ieri il buco dei numeri dell'audit, e questa è **la stessa malattia in un altro documento**: un numero che quattro documenti riportavano e che nessuno confrontava. Stavolta il numero è **quanti file ha `dati/mappe/`**, e i quattro documenti che ne parlano avevano dato **quattro numeri diversi** — `mappe.md` 25 (giusto), `README.md` 23 in due posti, `AGENTS.md` 21, `fonti-visive.md` 19 (che è il numero dei soli file di Natural Earth). Anche il **peso** era doppio: 1,6 MB in un documento, 1,4 MB nell'altro, e il conto dà **1,52**.

**Il difetto vero è sotto il difetto, ed è più interessante.** Per contare quei file dalla cartella è venuto fuori che **non si poteva**: nessun file di `dati/mappe/` dice, da solo, da dove viene. Il generatore lo sa — la lista `LAVORI` porta lo shapefile e la scala di ciascuno — ma quella lista sta in un sorgente Python, e il dato non la porta con sé. È la regola «**ogni dato dichiara da dove viene**» che il progetto si è data coi colori delle carte e con la tavolozza il 03/10, e che alle mappe **non era mai arrivata**: nessuno se n'era accorto perché il nome del file sembrava dirlo. Il nome di un file che comincia per `mondo_110` non è una fonte, è un indizio.

**La risposta è un manifest, non un campo nuovo dentro i file**: `dati/mappe_manifest.json` (v1) dichiara per ogni file fonte, produttore, scala, geometrie, punti e byte, con i conti **calcolati** sui file veri. Sta in `dati/` e non in `dati/mappe/` per la regola del solo formato a delta, come `altitudine_manifest.json`. Il generatore è `sorgenti/gis/mappe_manifest.py`, il controllo `sorgenti/gis/verifica_inventario_mappe.py` (I1–I8), e la prova dei difetti ne inietta **dieci** — i quattro numeri, il peso, la fonte mancante, il produttore mancante, il file che il manifest non conosce, il conto delle città, i pin coperti, il manifest assente — e li richiede **tutti** visti.

**Tre cose che quella prova ha insegnato, e che sono la parte interessante del giro.**

La prima è un difetto che nessuno avrebbe trovato a leggere il codice: la lista `problemi` veniva **riassegnata** a metà del corpo del verificatore, e l'assegnazione svuotava tutto quello che i controlli **I4** e **I5** avevano scritto. Due controlli che potevano solo scrivere nella spazzatura, e che non potevano accorgersene — perché il codice che li faceva fallire era esattamente il codice che ne cancellava la traccia. **L'ha trovato la prova, non io**: è la quarta volta in quattro giorni che la prova indica un difetto che il difetto non era dove sembrava, ed è la seconda che il difetto è nel **controllo** e non nel dato.

La seconda è la regola che il progetto si dà con la tavolozza, applicata a un caso nuovo: **un file che non trova la sua fonte nella lista del generatore non è di Natural Earth per default**. È di provenienza ignota. Senza quella regola un rilievo chiamato `probe.json` passerebbe per naturale e il conto tornerebbe per la ragione sbagliata — che è il modo peggiore in cui un conteggio può essere giusto.

La terza è la più scomoda, perché è sulla regola stessa: una delle dodici frasi che il controllo confronta era scritta sul testo di ieri, non su quello di oggi. Una regex che smette di corrispondere a una riscrittura **non segnala un difetto: semplicemente non guarda**, e il numero che doveva guardare diventa proprio quello che nessuno guarda. Per questo ogni frase della lista è **provata** dalla prova dei difetti, e per questo il controllo ha anche una regola nuova: se una frase non è più nel documento, **va detto**, perché «quel numero non è più controllato» è un problema che il controllo deve poter dichiarare su se stesso.

Nessuna delle quattro decisioni aperte tocca niente di tutto questo, e nessuna delle tre linee di `AGENTS.md` che il giro cambia è una decisione: sono fatti, e i fatti si dichiarano.



### 1.8 3undecies. Il quinto numero che non guardava: sessanta emblemi che erano diciotto file

*Da `audit.md` v0.25, sezione «3undecies. Il quinto numero che non guardava: sessanta emblemi che erano diciotto file».*

La domanda era «cosa manca a livello di elementi grafici da generare?». La
risposta, prima ancora che la si scrivesse, è stata controllata: e il controllo
ha trovato un difetto che nessuno dei sei controlli esistenti poteva vedere.

**Il difetto.** L'emblema — il riquadro che il gioco mostra quando di una persona
non c'è un ritratto libero — era un rettangolo con una diagonale, e la diagonale
dipendeva da `sum(ord(codice)) % 22`. Sessanta persone, ventidue semi possibili,
**diciotto file distinti**: dieci di loro avevano lo stesso identico PNG. La
funzione che lo disegnava diceva nel proprio docstring che «il seme decide la
diagonale, così due emblemi diversi non sembrano lo stesso file»: era falso, e
la frase era l'unica prova che qualcuno lo avesse pensato. Nessuno dei sei
controlli lo vedeva, e il motivo è la cosa che questo giro consegna agli altri
giri: **tutti e sei contavano i file**, e sessanta file giusti sono sessanta file
giusti anche quando sono diciotto.

**Il controllo che mancava è il settimo, e conta gli sha256.** Non è un controllo
nuovo per principio: è il controllo che tutti gli altri avrebbero dovuto fare da
soli. Dice due cose, e le due sono diverse: quante immagini ci sono, e quante
persone le hanno. Le due cifre erano diverse da tre giorni, e nessuno lo sapeva.

**Quello che il controllo ha trovato subito, e non era nel piano.** Con il
controllo 7 in piedi, il primo giro è rosso anche sui **ritratti**: 138 file
distinti su 141 persone. Il difetto dichiarava i nomi, ed erano sei voci di
catalogo per tre persone: `augusto` e `ottaviano augusto`, `copernico` e `niccolò
copernico`, `federico ii` e `federico ii di svevia`. È lo stesso difetto dei
codici `Q` chiuso il 2 ottobre, dal lato opposto: `chiave_persona()` normalizza
il nome e non sa che «Augusto» e «Ottaviano Augusto» sono lo stesso uomo, perché
la normalizzazione è testuale e **l'identità non è una questione di testo**.

**Tre chiusi, e non una regola.** Una regola che unisse due nomi perché uno
contiene l'altro avrebbe anche unito «il territorio del Po» e «i Bersaglieri del
Po», che sono due persone diverse, e nessuno dei due nomi contiene l'altro ma la
regola che unisce per somiglianza non distingue i due casi. I tre sono quindi
**dichiarati** uno per uno, e il controllo 7 resta a guardarli: se un quarto
doppione compare, il numero dei distinti torna sotto e il verde viene via. Il
catalogo passa da 201 a **198 persone**.

**Il secondo difetto del difetto l'ha trovato la prova, non io.** Il controllo 8
ricalcola la famiglia dell'emblema dal motivo e la confronta con quella che il
catalogo dichiara. Alla prima versione confrontava, per la parola, il valore
**ricalcolato con sé stesso**: `emblema_famiglia_da` poteva dire qualunque cosa e
nessuno se ne accorgesse. È il secondo caso in due giorni di un controllo che
guarda una cosa e la confronta con sé stesso, ed è il caso che la prova dei
difetti esiste per trovare: l'ha scoperto iniettando una parola inesistente e
chiedendo che il difetto fosse visto.

**Il terzo difetto è nel generatore, e l'hanno trovato gli occhi.** Tre segni non
reggevano a guardarli: il font 3×5 rendeva `DOM` come `DOH`, la volta era un arco
tracciato con una soglia non simmetrica ed era storta, la fessura dell'anello era
di 24 gradi e toglieva metà del segno. Nessuno dei tre si sarebbe visto ragionando
sulla formula, e il progetto ha la regola che vale: **una forma non si approva
perché la formula è giusta, si approva perché si è guardata**.

**Che cosa è cambiato nel motore.** `sorgenti/art/emblema.py` è nuovo, e
`catalogo_immagini.py` lo chiama: i sessanta emblemi portano il segno della
famiglia del loro motivo, le iniziali della persona, e una firma di cinque caselle
che serve a una cosa sola — rendere i file distinti. Le sette famiglie sono
classificate dal motivo con una regola dichiarata, i colori vengono tutti dalla
tavolozza, e nessuna libreria: PNG con `zlib`. `verifica_immagini.py` passa da sei
a otto controlli e la prova da sei a **undici difetti**, tutti visti. Mentre si
guardava, è saltato fuori anche che `catalogo_immagini.py` scriveva il catalogo
**tre volte** con due testi diversi: il risultato era giusto, la terza scrittura
vinceva, e un file scritto tre volte è un posto dove il prossimo scrive la riga
sbagliata senza accorgersene.

Nessuna delle decisioni aperte è toccata, e nessuna delle tre righe di
`AGENTS.md` che il giro cambia è una decisione: sono fatti.



### 1.9 3duodices. Il sesto numero che non guardava: undici disegni che il motore non poteva aprire

*Da `audit.md` v0.25, sezione «3duodices. Il sesto numero che non guardava: undici disegni che il motore non poteva aprire».*

Il giro dei sessanta emblemi ha finito alle 23 del 4 ottobre con un commit che
aveva lasciato **diciassette file in più nel ramo che in locale**. Erano la
coda di due cose diverse, e la cosa interessante è che **erano due famiglie
diverse nella stessa cartella** e nessuno le aveva distinte.

**La prima: sei emblemi superati, e il regoletto che li lasciava vivere.** Sei
persone sono passate da emblema a ritratto in quello stesso giorno, e le loro
tessere di emblema sono diventate spazzatura: sei file che il catalogo non
citava e che nessuno guardava. Erano anche, di nuovo, **meno distinti delle
persone**: `emblema_P17` e `emblema_P62` erano lo stesso byte, `emblema_P28` e
`emblema_Q221` pure. Sei file, quattro immagini, quattro giorni dopo che
sessanta emblemi erano diventati diciotto file: **lo stesso difetto, nella stessa
cartella, e nessuno lo aveva notato** perché il posto che doveva accorgersene —
`_commit_coerenza.py`, che toglie dal ramo le tessere superate — guardava solo il
prefisso `ritratto_`. La regola non era sbagliata, era **incompleta**, e un
controllo che guarda metà di quello che deve guardare è verde come uno che non
guarda niente. Ora la regola guarda entrambi i prefissi ed è una sola funzione:
`tessera_superata()`.

**La seconda, e più seria: undici disegni che il motore non poteva aprire.** Nella
cartella dei ritratti c'era la **piazza della Cattedrale**: la facciata (509 ×
312 px), il cartello dell'articolo 9, la lapide, due statue, il protagonista in
quattro fotogrammi e i tre ritratti disegnati a mano. Erano lì dal primo commit
del 30 settembre. **Nessun codice li caricava e nessun dato li nominava**: la
tabella 3 di `tappa-1-01.md` descriveva Maurelio, San Giorgio, la lapide e il
cartello a parole e a coordinate, ma non diceva quali file li disegnano, e
`dati/ambienti_livelli.json` — il manifesto degli ambienti, costruito il 3 ottobre
proprio sul modello di questa tappa — non aveva un campo dove metterli.

Il controllo 2 li dichiarava **file morti**, e aveva ragione. Undici file di
disegno che il motore non può usare non sono un patrimonio: sono un inganno, e
lo sono anche di più perché il primo file che ho riguardato è la facciata, che è
proprio la cosa che quella piazza è. La risposta non era cancellarli — sarebbero
stati cancellati come spazzatura sei disegni che il progetto aveva già e che il
documento già descriveva — ma **dichiararli**, che è la cosa che il progetto sa
fare e che questa cartella non aveva.

**Ora sono la tabella `SPRITE`**, in `sorgenti/ambienti_livelli.py`, e ogni riga
porta tre cose che prima non erano scritte da nessuna parte: la **voce** della
tabella 3 da cui il file prende il posto, il **file**, e **che cosa ci si vede**.
Il legame fra voce e nome è **dichiarato** e non dedotto, perché «San Giorgio
(visione A1)» si chiama `giorgio.png` e una regola che togliesse le parole
avrebbe finito per unire cose diverse. La misura è **misurata** sul PNG, il posto
è **riletto** dal documento, e i centoquarantanove ambienti che non hanno sprite
lo dichiarano con il vuoto `sprite_da_disegnare`.

**Tre controlli nuovi, e uno di loro è la prova che i due precedenti non erano la
stessa cosa.** Il **9** chiede che ogni sprite dichiarato esista, sia un PNG e
abbia la misura dichiarata. Il **10** chiede che la facciata sia larga quanto la
geometria del documento: i 509 px sono un numero scritto a mano accanto ai 39,8 m
e ai 12,8 px per metro, e il controllo li **moltiplica** e pretende che il
risultato sia proprio quei 509. Il **B9**, in `verifica_ambienti.py`, riapre la
tabella 3 del documento e confronta posti e scala riga per riga: un manifesto si
può editare a mano come qualunque altro file, e i posti degli sprite ne erano la
prova.

La prova dei difetti è passata da undici a **sedici difetti**, e due dei nuovi
esistono per una ragione che vale più degli altri: il quindicesimo rompe la
**sola** dichiarazione della scala e pretende che il difetto lo veda il controllo
10, non il 9. Senza quel `cerca`, la prova guardava la prima riga dell'output,
che poteva essere quella di un altro controllo, e avrebbe dato un verde che non
sapeva niente — che è esattamente il difetto del controllo 8, trovato ieri.

**La lezione, che è la sesta volta che la stessa lezione si presenta.** Un dato
senza una fonte non è un dato: è una convinzione. Gli sprite erano convinzioni
senza fonte, il controllo che li contava era verde, e il ramo era **rosso su un
clone** mentre qui era verde: due risposte alla stessa domanda in due posti
diversi dello stesso progetto. La regola che ne segue è già nel progetto e questa
volta l'ha salvata: **un numero dichiarato va riletto dalla sua fonte, non
creduto** — e va riletto da un controllo, perché un controllo che guarda una cosa
e la confronta con sé stesso è verde come uno che non guarda.

**C'è anche il secondo sospeso, che era più piccolo e più semplice.** Il foglio di
controllo degli emblemi esisteva solo come script ad hoc di una sessione, finito
in un file HTML fuori dal progetto e poi cancellato: un foglio che sparisce
quando finisce la sessione che l'ha prodotto non è un foglio di controllo.
Ora è `sorgenti/art/foglio_emblemi.py`, che scrive `sorgenti/art/foglio_emblemi.txt`:
**in caratteri**, perché la finestra del browser non si compone più e un'immagine
composta non si interroga. Ogni cella porta codice, nome e famiglia, e il conteggio
degli emblemi e delle famiglie è **calcolato** dal catalogo: un foglio che
dichiara «60 emblemi, 7 famiglie» scritti a mano è un foglio che il primo
emblema tolto rende falso.

Nessuna delle decisioni aperte è toccata, e nessuna riga di `AGENTS.md` che questo
giro cambia è una decisione: sono fatti.



### 1.10 3quinquagesim. L'ottavo numero che non guardava: due righe scritte due volte

*Da `audit.md` v0.25, sezione «3quinquagesim. L'ottavo numero che non guardava: due righe scritte due volte».*

**Il difetto.** Cercando cosa fosse rimasto in sospeso, il primo sospeso non
era un disegno: era un **registro**. `premi.md` §6 aveva due righe su cinque —
mancavano **v0.2** (l'undicesima categoria, la K, nata dalla ricerca sulle
figure sorde) e **v0.4** (il catalogo da 1050 record e i 1050 emblemi). Sono le
due versioni che hanno fatto il lavoro grosso, e nel registro non c'erano: il
documento raccontava di un lavoro che non risultava mai svolto.

Controllando il documento delle fonti visive è venuto fuori il resto, che è la
stessa cosa in un altro vestito:

- la sezione **§3.10** c'era **due volte**, parola per parola;
- la riga «Emblemi dei premi» del riepilogo §8 c'era **due volte**;
- il registro §9 aveva una riga `|---|---|---|` **in mezzo alle righe**, che
  chiudeva la tabella dopo la 0.5 e faceva sembrare le quattro righe sotto un'altra
  tabella; e le versioni **0.9 e 0.10 non avevano riga**.

**Perché nessuno l'aveva visto.** Tutti i controlli di questa sezione confrontano
**numeri**, e un paragrafo scritto due volte ha i numeri giusti in entrambe le
copie. È la stessa forma del settimo numero, dove il conteggio era vero e la
geometria un punto: qui il testo è vero e sta due volte. La sostituzione
testuale era stata eseguita due volte, e la seconda esecuzione è riuscita senza
dire niente — è la quinta volta in quattro giorni che una cosa fatta due volte
non lascia traccia.

**La contraddizione più grossa, che stava nello stesso documento.** La *fonte
del materiale* di `premi.md` riportava la richiesta del 03/10 «tranne
informatica» e `AGENTS.md` lo ripeteva; `premi.md` §2.2 scriveva **nessuno**
nella riga del dominio `informatica`; e §4.0 contava **150** livelli informatici
che «hanno un premio anche loro», con il catalogo che li aveva scritti. Due
verità che nessuno metteva una accanto all'altra.

**La decisione.** Pietro, 04/10/2026: **l'informatica ha un premio per tappa come
le altre discipline**. Quindi il numero è **1050**, la richiesta del 03/10 è
superata, e i tre luoghi che la negavano sono stati corretti — con la
dichiarazione che in §2.2 l'informatica resta *senza* premio solo nella **sfida a
mani nude**, dove il premio è la prestazione. Un dominio senza premio nella
tappa è una cosa diversa da una disciplina senza premi, e la tabella le
confondeva.

**Il controllo che cerca le righe mancanti ne ha trovate altre due, qui dentro.**
Applicato a tutti i registri — **31 documenti in `docs/`, 21 con un registro di almeno due righe** — il controllo ha detto che
in `audit.md` mancava la riga **0.21** — che era il difetto del font senza le
cifre, uno dei due della giornata — e che la tabella di §7 **non aveva la riga
di separazione**: le righe sembravano testo con due pipe. Il documento che conta
i numeri aveva perso un numero, e nessuno dei ventuno controlli lo vide, perché
nessuno contava le righe del proprio registro.

**Quanto è costato.** Quindici minuti a cercare e mezzora a correggere, e
nessuna a verificare: non è un difetto che i controlli potessero vedere. La
regola che ne esce è in `AGENTS.md`: **un registro che perde una riga è un
documento che mente sul proprio lavoro**, e per questo le righe si contano.

### 1.11 3terdecies. Il settimo numero che non guardava: un conteggio vero e una geometria falsa

*Da `audit.md` v0.25, sezione «3terdecies. Il settimo numero che non guardava: un conteggio vero e una geometria falsa».*

**Il difetto.** `dati/edifici_footprint.json` dichiarava **5209 sagome** e i 5209 erano veri: erano 5209 edifici, uno per uno, con nome, altezza, fonte e categoria. Ma la **geometria era un punto**. La forma si scriveva con `round(x / Q)` invece di `round(x * Q)` — divideva per cento un numero che era già in metri — e ogni vertice finiva a zero. L'ingombro più grande in tutto il file misurava **cinque centimetri quadrati**, la superficie di una monetina. In tutti i 52 luoghi.

**Perché nessuno lo vide.** Perché il numero è vero. Un file che dice «5209» e un file che dice «0,0 m²» non possono stare nello stesso record senza che qualcuno li confronti, e nessuno li confrontava: il generatore scriveva, i documenti citavano il conteggio, e il conteggio era giusto. È la forma peggiore in cui può morire un controllo: **non per assenza di esame, ma per esame della metà sbagliata del file**. Il regolamento del progetto dice «una forma che non è verificata non si disegna», e qui la forma non era disegnata: era dichiarata, e la dichiarazione era vera.

**Che cosa è costato.** Non il tempo — il file si rigenera in cinque minuti. È costato il fatto che **tre documenti e un file di dati parlavano di «5209 sagome» come se la geometria fosse vera**, e che la verifica degli ambienti (B1–B9) contasse i livelli *che hanno* sagome senza guardare *che cosa sia* la sagoma. Un controllo che confronta i dati fra loro e non confronta i dati con la loro forma è verde su un file di punti.

**Che cosa è cambiato, in quattro pezzi.**

1. **Il file è stato rigenerato da capo**, con la quantizzazione corretta: `round(x * Q)`, in centimeti interi, che è il formato che `mappe_formato.scrivi` già usa e che il motore già sa leggere. Ora sono **7322 edifici su 203 aree** interrogate.
2. **La perdita nella quantizzazione è un controllo nel generatore**, non un pensiero successivo: `forma()` restituisce anche se l'ingombro della forma quantizzata sta nella stessa scala dell'area dichiarata, e se non sta l'edificio viene **scartato e contato**, non scritto. Un difetto che entra nel file è un difetto che si propaga a ogni lettore.
3. **È nato `verifica_sagome.py`**, con i controlli **S1** (ogni forma racchiude l'area che il record dichiara), **S2** (nessuna sagoma sotto il metro quadro) e **S3** (`fonte_altezza` è una delle tre dichiarate). Sul file rotto ne trovava **5209 su 5209** e l'ingombro massimo era **0,0 m²**; sul file nuovo dà **0**. Un controllo che non si è mai visto sbagliare non è un controllo: questo si è visto, e ha morso.
4. **Due difetti più piccoli, trovati solo dopo che la forma c'era.** La semplificazione a tolleranza fissa (1,5 m) cancellava gli edifici piccoli: un'area di due metri diventava un quarto della sua area. E il confronto della perdita guardava l'area della figura *semplificata* invece di quella *dichiarata*, così misurava la perdita della quantizzazione contro la perdita della semplificazione e le due si coprivano a vicenda. Nessuno dei due sarebbe stato trovato senza il primo difetto risolto, perché finché le sagome sono un punto non si distinguono.

**La terza volta in tre giorni che la stessa malattia ha un nome diverso.** I trenta disegni appena generati erano verdi su tutti i controlli e **non si aprivano**: il PNG si annunciava con tre canali RGB e i dati ne avevano uno, perché la tela teneva l'indice del colore e l'indice veniva scritto al posto di un byte di canale. D1 e D2 leggono l'intestazione, che si può dichiarare come si vuole; D3 confronta gli sha. Nessuno dei tre guardava un pixel. È stato il controllo che guarda i pixel a smascherarlo, e ora è **D4**, che decodifica con `png_terrarium.decodifica_png` — il lettore che il motore usa — e confronta i pixel con la misura dichiarata. Nella prova dei difetti c'è **E6**, che costruisce apposta un PNG con la stessa malattia.

La sequenza dei tre giorni è la stessa: l'area che dichiara **5209** e la forma che è un punto; le trenta immagini identiche che nessun occhio ha visto e che solo il confronto degli sha ha smascherato; l'intestazione che dichiara **RGB** e i dati che sono un byte. Non sono tre coincidenze. È che **un controllo che guarda una metà del file è verde come un controllo che non guarda niente**, e la metà che si guarda è quasi sempre quella che si sa leggere. La regola che ne segue è già nel regolamento e va detta di nuovo con le parole di oggi: un controllo deve guardare **il risultato che l'altro consumatore del file si aspetta**, non la sua dichiarazione. Il file delle sagome lo consuma un motore che calcola un ingombro; l'indice lo consuma un decodificatore; i documenti li consuma un umano. Ogni controllo deve stare dalla parte di chi consuma, e per i file binari **decodificare è l'unico modo di starci**.

**E due difetti di interrogazione, più gravi di quanto sembrassero.** Overpass rispondeva 504 su tutte e tre le istanze: la correzione è stato cambiare fonte, non aspettare — `scarica_osm.py` interroga l'API standard OSM e restituisce **lo stesso formato**, così a valle non cambia niente. E l'interrogazione per **luoghi** era la domanda sbagliata: i pin del registro sono città intere, e i ventotto punti dell'anno 1 stanno fra 204 e 1422 metri dal pin di Ferrara. Il file diceva «Ferrara ha centoquattro edifici» e le tappe non ne avevano nessuno. Ora si interroga anche ogni **livello**, per **relazione esplicita** — la chiave del record è il livello, nessun confronto di nomi — e il raggio di un livello è **calcolato dalla diagonale della sua griglia** più un margine, non scritto: 51 metri per una porta, 121 per un paesaggio. Sono **2632 record su 134 livelli distinti**, contro i 68 che c'erano prima.

**I disegni.** `disegna_ambienti.py` guarda le due tavole di numeri insieme e ne fa **150 immagini schematiche**, una per tappa: **30** il 4 ottobre, tutte e centocinquanta il 5 con `--tutte`. Il difetto più subdolo della giornata è nato qui: la prima versione usava la griglia come riquadro — venti metri per quindici — mentre gli edifici arrivano da un raggio di quaranta-centoventi metri, e il ritaglio li buttava fuori uno per uno. Trenta immagini quasi tutte uguali, tutte sfondo, con **tre coppie a sha identico**. Lo ha visto il controllo **D3**, non un occhio. Il motto è già nel regolamento: *un controllo che non guarda è verde come un controllo che guarda*. E la prova dei difetti ne ha trovato uno in sé stessa — la copia di sicurezza teneva il file sorgente invece di quello sovrascritto, e il ripristino lasciava la coppia identica: cinque difetti iniettati, cinque visti, e il progetto intatto alla fine, che è l'unica cosa che conta in una prova di questo tipo.

### 1.12 3quindices. Un controllo che segnala come difetto la verità, e i disegni che erano trenta

*Da `audit.md` v0.25, sezione «3quindices. Un controllo che segnala come difetto la verità, e i disegni che erano trenta».*

**Il fatto.** I disegni schematici esistevano per **trenta** tappe, tutte dell'anno 1, e il 5 ottobre sono stati fatti per tutte e **centocinquanta** (`--tutte`, 25 s, 1,5 MB): **2632** edifici disegnati, **0** ritagliati fuori dal riquadro, larghezza da **80** a **2584** px, **150** PNG che si decodificano. Le **16** tappe che il file degli ambienti dichiara `senza_sagome_osm` hanno il disegno vuoto, ed è dichiarato in `indice.json` una tappa per una.

**Il difetto, che è di un tipo nuovo.** Il controllo **D3** chiedeva che gli sha dei PNG fossero tutti diversi, e sull'anno 1 era giusto: trenta tappe, trenta disegni, trenta sha. Sui centocinquanta la richiesta è impossibile, perché **43 tappe su 150** hanno le stesse sagome sulla stessa griglia e quindi lo stesso disegno. La prima reazione sarebbe stata una delle due sciocchi che si dichiarano: cambiare i dati perché i disegni escano diversi, oppure zittire il controllo. Il controllo è stato invece riscritto sul confronto fra **la chiave dei dati** (sagome e griglia) e lo **sha del disegno**: stessi dati devono dare lo stesso disegno, dati diversi devono dare disegni diversi. Il conto torna, **107 chiavi dati e 107 sha distinti**, ed è la prima verifica che guarda due cose insieme.

**Due righe che si accorgono del caso nuovo.** Il numero dei disegni è passato da 30 a 150 senza che nessuna riga scritta lo seguisse: la tabella di §3.9 e il riepilogo dichiaravano ancora «30 immagini su 30 tappe dell'anno 1», ed erano diventate entrambe false nello stesso modo in cui erano state scritte. E la **data** di `indice.json` era scritta a mano, `2026-10-04`, quattro giorni dopo che la prima riga era diventata falsa.

**Che cosa è stato fatto, in quattro mosse.** `verifica_disegni.py` confronta la chiave dati con lo sha e conta le due cose insieme; `sorgenti/art/prova_difetto_disegni_150.py` rovescia il disegnatore due volte — **F1** gli fa perdere un edificio dalla tappa 2-5, **F2** gli mette una macchia sulla 5-18 — e verifica che D3 veda entrambe, e verifica il ripristino confrontando gli sha: **2 difetti iniettati, 2 visti**; la data dell'indice è passata da scritta a mano a calcolata; il costo di `verifica_disegni.py` — **2 min 10 s**, perché **D4** decodifica centocinquanta PNG in Python puro — è dichiarato accanto al comando invece di essere scoperto fra un mese.

**La regola, per la prossima volta.** Un controllo che segnala come difetto la verità è un allarme spento: spento, non verde. Prima di estendere un dato a un insieme più grande va chiesto se il controllo che lo sorveglia era stato scritto per quell'insieme o per il campione.

### 1.13 3quattuordices. Il carattere che il font non ha, e non disegna niente

*Da `audit.md` v0.25, sezione «3quattuordices. Il carattere che il font non ha, e non disegna niente».*

**Il difetto.** Gli emblemi dei **1050 premi** sono un foglio di tessere 48×54, ciascuna con il segno della categoria, il livello e la firma. Il primo giro ha prodotto tessere **identiche**: `1-1-FE` e `1-2-FE` erano lo stesso file. Il motivo è che il font di `emblema.py` ha **solo le ventisei lettere**, e il codice scriveva `emblema.FONT.get(lettera, [])`: per la cifra `2` la lista è **vuota**, e una lista vuota in mezzo a un disegno non lascia un buco — lascia **esattamente la stessa tessera**.

È la terza volta in quattro giorni che la stessa cosa si presenta con un nome diverso: l'area che dichiara **5209** edifici e la forma che è un punto; l'intestazione PNG che dichiara **RGB** e i dati che sono un byte per pixel; e qui il carattere che il font **non ha** e che il valore di default sostituisce con il vuoto. In tutti e tre i casi la metà che si dichiara è vera e la metà che si consuma è falsa, e il difetto sta nello spazio fra le due.

**La regola che esce, e che va in `AGENTS.md`**: un valore di default che sostituisce un dato mancante non è un dato, è una sparizione silenziosa. `FONT.get(c, [])` è la forma più economica del difetto, e il suo difetto gemello è `dict.get(k, 0)` su un conteggio, che fa la stessa cosa e con la stessa faccia.

**Il secondo difetto, due minuti dopo.** Tolte le cifre, `1-2` e `2-2` erano ancora la stessa tessera: hanno entrambi il numero 2. Il numero della tappa **non identifica un livello** senza l'anno, e un identificatore che non identifica è un'etichetta. Ora la tessera porta anno, numero su due cifre e sigla della lingua — `102SG` e `202SG` — e il generatore si ferma se due lingue prendono la stessa sigla, che è il terzo difetto che la sigla evita.

**Quanto è costato.** Quattro minuti per trovarlo, e niente per la verifica: **Q3** lo vide al primo giro, perché confronta gli sha delle tessere una per una. Il controllo esiste per quello: trecento dei 1050 premi hanno la **stessa categoria** e quindi la stessa forma, e se la firma non rompesse le collisioni quei trecento sarebbero centocinquanta file identici. Sei difetti iniettati, sei visti, verde prima e dopo.

### 1.14 3sexies. Le immagini: due difetti che la verifica avrebbe dovuto vedere

*Da `audit.md` v0.25, sezione «3sexies. Le immagini: due difetti che la verifica avrebbe dovuto vedere».*

Il 3 ottobre sono stati guardati uno per uno i 195 ritratti che nessuno aveva mai
guardati. Il conto: 145 accettati, 43 respinti, 7 aperti. Le 43 respinte sono
state respinte perché non sono un ritratto della persona: uno stemma araldico,
un francobollo, una tavoletta cuneiforme, una parte di stele, un pannello di
mostra, un monumento di cemento, una medaglia di bitcoin al collo. Sono la prova
che il nome del file non è una prova.

**Il difetto grande: 195 richieste in una.** `applica_attestazione.py` mandava a
Commons tutti i nomi dei file in una richiesta sola; la API ne accetta 50 per
volta. La risposta era un errore con zero pagine, e il codice lo leggeva come
«il file non esiste». Il risultato è stato che **127 ritratti corretti sono
diventati emblemi** e la tabella lo dichiarava senza una riga di errore. Il
motivo è il più importante di tutti: un controllo che non distingue *non ho
chiesto bene* da *non esiste* non controlla niente, e peggio, convince chi legge
che sia tutto a posto.

**Il difetto piccolo, che è la stessa cosa.** Il nome del catalogo era scritto a
mano in due file, e in uno «gioco» era diventato «giogo». Il sintomo era un
`Errno 2` su un percorso che sembrava giusto, e si è perso tempo a cercarlo nel
sistema invece che nei due file. Ora il nome **si cerca** fra i file e, se non se
ne trova uno solo, il controllo si ferma.

**Il terzo esito, che è la cosa nuova.** Finora un'immagine era accettata o
respinta. Serve un terzo caso, `da_verificare`: si vede un ritratto di persona
giusta e di periodo giusto, ma non si può accertare di chi è. I ritratti dei duchi
estensi sono i più scambiati fra loro di tutta la raccolta, e due profili di dame
del Cinquecento sono indistinguibili a occhio. 7 immagini sono in questa
condizione: restano aperte, con il file da parte, e il gioco mostra un emblema.
Un'immagine non verificata a schermo è il gioco che racconta una bugia con il
volto di una persona vera.

### 1.15 3septies. I metadati: sette immagini aperte, sei chiuse, una persona sbagliata

*Da `audit.md` v0.25, sezione «3septies. I metadati: sette immagini aperte, sei chiuse, una persona sbagliata».*

Le 7 immagini rimaste `da_verificare` sono state chiuse leggendo i metadati di
Commons, con il metro del **confronto di tre fonti**: il nome del file, la
descrizione che l'uploader ha scritto e le categorie devono dire la stessa cosa.
Se dicono la stessa cosa l'immagine passa; se due dicono una cosa e la terza
un'altra resta aperta e il conflitto si scrive. Il metro è in
`sorgenti/art/verifica_metadati.py`.

**Una persona sbagliata, e non un'immagine sbagliata.** `P11` doveva essere la
beata **Beatrice II d'Este**, la monaca di Sant'Antonio in Polesine, una degli
Este che non governarono, morta nel 1372. Il file trovato è di Bartolomeo Veneto
e le categorie dicono `Beatrice d'Este`: è la duchessa milanese del 1490, figlia
di Ludovico il Moro. Due donne, due secoli, due dinastie, e la somiglianza è
solo nel nome. L'ho segnato **respinta** e ho aperto una voce nuova: il ritratto
vero della beata va cercato, e non basta rilanciare la stessa ricerca, che ha
già abboccato.

**Il metadato ha corretto me, una volta.** Su `P61` e `P62` avevo scritto che
erano «la stessa formella fotografata da un'altra angolazione». Non lo sono:
sono due formelle diverse dello stesso palazzo, entrambe di Gaetano Davia, una
per il Bonati e una per il Foschini. Avevo ragione a non accettarle, e ragione a
non sapere perché. Un metadato non è la verità — la descrizione la scrive chi ha
caricato il file — ma quando confuta l'occhio va detto, altrimenti il proprio
registro dei difetti si tiene solo quando fa comodo.

**Le altre cinque passano, e con le riserve dichiarate.** Il monumento equestre di
Ferrara è un ricomincio del Novecento del monumento quattrocentesco a Nicolò III,
e resta un monumento: dichiarato. Il ritratto di Borso è un dipinto del suo
regno, 1469-1471, con l'attribuzione al fratello Baldassarre dichiarata in
categoria. Quello di Tito Strozzi è di Baldassarre d'Este, suo figlio. Il del
Bonati e il del Foschini sono rilievi dell'Ottocento. L'Isabella di Castiglia è
un dipinto del Prado del 1490, e sul file il credito è incerto — l'uploader
scrive tre provenienze diverse, una delle quali è «Unknown source» — quindi
l'accettazione vale per il dipinto documentato, non per una provenienza.

**La ricerca rilanciata, e il suo esito.** Cinque interrogazioni su
Commons, con il nome in italiano, in inglese, con l'anno della morte e con il nome
del monastero: nessun ritratto. L'unico file che riguarda questa persona è un
dipinto con la Trinità sulle nubi e **tre santi** insieme, nella chiesa di
Sant'Antonio in Polesine, che è proprio il suo monastero; e poi una dozzina di
«Beatrix» che sono tutte Maria Beatrice, arciduchesse d'Austria del Sette-Ottocento.
Una scena con tre figure non è un ritratto, per la stessa regola con cui sono state
respinte la scena miniata di Alcuino e la parte alta della stele di Hammurabi — e
la tentazione qui è più forte, perché il file è bello, la persona è quella e il
posto è esatto. Il documento adesso non dice «non l'ho trovato», che è una
constatazione sul lavoro fatto: dice **che cosa esiste** e perché non va bene.
L'emblema di `P11` è dunque la risposta finale, non una resa, e resta aperta solo
una fonte fuori da Commons.

**Due controlli che si sono rotti mentre chiudevo, e come.** La prima versione di
`prova_difetto_immagini.py` chiedeva una persona «aperta» per provare il difetto
n. 4: chiudendole tutte, la prova morì con «nessuna persona». Una prova che
funziona solo finché esiste un caso non è una prova del caso, è una prova del
calendario: il caso ora **si costruisce**. E il catalogo, cambiando esito a
quelle sei persone, lasciava le loro vecchie tessere d'emblema accanto a quelle
nuove: sei file che nessuno usava e che il primo che li avesse aperti avrebbe
trattati come ritratti respinti ancora validi. Gli orfani ora si cercano tutti,
non solo i `ritratto_`.

### 1.16 3octies. Due lacune che Pietro ha affidate: il mezzo del quinto anno e i codici dei facoltativi

*Da `audit.md` v0.25, sezione «3octies. Due lacune che Pietro ha affidate: il mezzo del quinto anno e i codici dei facoltativi».*

**Il mezzo del quinto anno.** Era `non_dichiarato` per un principio giusto: sono
ventidue i mezzi possibili, cinque sono i mezzi del *Furioso*, e sceglierne uno
significava scegliere al posto di Pietro. La risposta data non è una scelta: è
**due regole che non hanno un autore**. Il mezzo **reale** lo sceglie l'archivio,
che è il presente — ed è la stessa regola (`piu_veloce`) che gli anni 4 e 5 usano
già, quindi non è una preferenza nuova. Il mezzo **dentro la stanza** lo sceglie
**il canto**, perché ogni mezzo del testo è attestato in un canto e in un verso: la
tabella canto → mezzo è la traduzione degli indici, non una rosa. Dove il canto non
dà un mezzo si va a piedi, dichiarato. Il carro di delfini (c. XI) e il drago
(c. XVIII) non hanno tappa nell'anno 5: è il conto delle stanze e si dice per
iscritto.

*Il difetto che è venuto fuori durante il lavoro.* Il conto pubblicato nella §1.2 diceva
«aereo 26, treno 1» per il quinto anno, ma copriva **27 tappe su trenta**: 5-3,
5-6 e 5-20 sono del Seicento e precedenti, e venivano scartate da un `continue`
che non diceva niente. Un conteggio che scarta e non lo dice è un conteggio che
parla di un anno che non esiste. Ora il conto nomina le tappe scartate.

**I codici dei facoltativi.** La domanda era un codice `Q` a ciascuno dei 269
facoltativi, perché la regola dei premi si potesse verificare su tutti. La misura
prima dell'esecuzione dice tre cose che cambiano il conto: i 269 sono
**occorrenze**, non persone; dietro ci sono **248 persone distinte**; e sei celle
contengono **due persone in una** («Leonello d'Este, Leon Battista Alberti»). Il
risultato: 50 già codificate, 10 collegate al codice della persona perché
comparivano col solo cognome, 188 con codice nuovo, **0 da verificare**.

*Il pericolo evitato.* Nei facoltativi ci sono nomi che sono un cognome solo
(«Alberti», «Alfonso I») e una variante con l'accento (`Al-Khwārizmī`). Una
codifica meccanica avrebbe creato un secondo Alberti e un terzo al-Khwarizmi, e in
un catalogo **una duplicazione è peggio di un'assenza**: l'assenza si vede, la
duplicazione no, e la verifica dei premi avrebbe contato due premi sullo stesso
volto. Per questo il confronto è normalizzato sui diacritici, i cognomi solti si
collegano solo se **non c'è un altro candidato** (e altrimenti restano aperti con
i candidati elencati), e la guardia finale confronta le **persone**, non le
stringhe: «Tasso» e «Torquato Tasso» sono la stessa persona e non possono
contarsi come due.

*Il difetto vero, in un posto che nessuno guardava.* **10 persone avevano due
codici** nei cataloghi degli anni: compaiono in due anni e hanno una scheda per
anno, e nessuno dei due file se ne accorgeva. Non è un difetto dei cataloghi, che
sono per anno: è la mancanza di un indice unico — lo stesso difetto che si era già
visto sulle immagini, dove la stessa persona aveva due file. Ora `indice_persone`
dichiara il codice canonico (quello dell'anno 1 quando la persona c'è anche lì,
altrimenti il più basso della serie `Q`) e gli altri diventano alias che restano
scritti, perché i documenti degli anni li nominano.

**Il controllo.** `sorgenti/verifica_codici.py` verifica cinque cose: ogni
occorrenza ha un codice o un motivo, un codice è di una persona sola, una persona ha
un codice solo, nessun codice nuovo inciampa su uno esistente, e ogni tappa del
catalogo è confermata da un incontro. La quinta guardia, com'è giusto, si è fermata
alla prima esecuzione segnalando **276 occorrenze contro 269**: il confronto
sbagliato era suo, perché sei celle contengono due persone, e la correzione è stata
farla confrontare una corrispondenza invece di un'aritmetica.

## 2. Registro delle modifiche

| Data | Versione | Che cosa è cambiato |
|---|---|---|
| 06/10/2026 | 0.2 | Il §1 accoglie, alla lettera, le sedici sezioni di racconto dell'audit (v0.25), ciascuna con la sezione da cui viene. |
| 06/10/2026 | 0.1 | Prima stesura: la regola di come si scrive lo storico. Nasce con la fase 1 della roadmap della documentazione. |
