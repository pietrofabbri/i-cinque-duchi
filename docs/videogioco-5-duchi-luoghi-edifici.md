---
titolo: I luoghi e le sagome — che cosa serve per disegnarli davvero
versione: 0.6
data: 2026-10-05
autore: Buffy (per pietrofabbri)
documenti collegati:
  - docs/videogioco-5-duchi-mappe.md
  - docs/videogioco-5-duchi-luoghi.md
  - docs/videogioco-5-duchi-ritratti.md
  - FONTI-E-LICENZE.md
  - AGENTS.md
---

# I luoghi e le sagome

## 0. La domanda, e la risposta breve

«Raccogli i dettagli sui luoghi, in modo che all'atto della creazione si possa
fare un lavoro che rispetti proporzioni, forme, colori rispetto a vie, edifici,
piazze.»

La risposta breve è che **manca un pezzo e non si può comprare**.

Le altezze degli edifici non esistono come dato: misurate sul campo, si trovano
nel 24% dei casi a Milano e nel 3% a Roma (`mappe.md` §5). Nessuna fonte libera
e nessuna fonte a pagamento le dà. Un modello che stima le altezze senza dire
che le stima produce edifici sbagliati con aria di esatti, che è il peggiore dei
due.

Quello che c'è invece, e che nessuno stava usando, è **il terreno**. È un dato
pubblico, libero, preciso, e dice tre cose che in una vista 3/4 si vedono
sempre: quanto scende la strada, da che parte guarda il pendio, e a che altezza
sta la piazza. Una città su un pendio ha edifici che seguono la curva di livello
e si sfalsano a gradini; una città in piano no. Un generatore che non sa
quanto scende la strada produce un Effect.

Il pezzo che manca, e che va costruito, è il **generatore**, non il dato.

## 1. La decisione su ODbL, che era la questione aperta

`mappe.md` §10 Q1 chiedeva: *ODbL entra nel progetto?* È la prima cosa da
rispondere, perché cambia che cosa si può scaricare.

**Sì, entra.** E l'obiezione che di solito si oppone — «ti obbliga a mettere
tutto sotto licenza libera» — **non è corretta**, e vale la pena dirlo perché
decide da metà del lavoro.

ODbL ha due obblighi distinti, e si confondono:

- **Attribuzione.** Ogni uso di dati OpenStreetMap deve mostrare «© OpenStreetMap
  contributors». È un dovere, e basta una riga nei crediti.
- **Condivisione allo stesso modo.** Scatta solo quando si distribuisce un
  **database derivato** — un insieme di dati machine-readable derivato da OSM.

Un gioco che disegna la geometria su schermo non distribuisce un database
derivato: distribuisce un'opera. Quindi **il codice del gioco, i documenti e la
grafica originale restano del progetto**. I file che invece *sono* database
derivati — le geometrie in `dati/mappe/` — devono viaggiare con ODbL e con la
loro dichiarazione. Sono dati, non il gioco.

Cosa si sblocca, in concreto:

| | senza ODbL | con ODbL |
|---|---|---|
| sagome degli edifici fuori Ferrara | solo dove il Comune le pubblica, cioè **Ferrara** | ovunque |
| trenta zone percorribili | di fatto una | tutte |
| attribuzione | — | una riga nei crediti |
| licenza dei file di dati | libera | ODbL, dichiarata |

I vincoli che restano, e che vanno rispettati: **non si può toccare il file
derivato e distribuirlo come proprio**, e ogni distribuzione deve portare la
licenza. Sono due righe nei crediti, non un vincolo sul progetto.

`FONTI-E-LICENZE.md` è aggiornato con la decisione.

## 2. I 95 luoghi, e la scoperta che era dentro la casella

I luoghi del gioco non erano in un file: erano sparsi nelle colonne «Luogo (pin)»
delle trenta tappe di ciascun anno. `sorgenti/luoghi/estrai_luoghi.py` li legge da
lì, perché un inventario scritto a parte può divergere dai documenti, e un
inventario che diverge è un inventario falso.

Ne escono **95 luoghi distinti** su 120 tappe. E qui c'è la scoperta: **41 di
questi non hanno coordinate, e non è colpa della ricerca**. La casella non
 contiene un luogo. Contiene cinque cose diverse:

| `tipo` | Che cos'è | Quanti | Si disegna |
|---|---|---|---|
| `citta` | una città | 48 | mappa, edifici per tipologia ed epoca |
| `percorso` | due o più posti insieme: «Il Cairo e le carovane» | 11 | strada che unisce, con i due capi |
| `situazione` | un contesto, non un posto: «una sala di riunione, 1983» | 11 | **non si disegna** |
| `edificio` | un palazzo, una corte, un convento | 10 | sagoma singola, con la sua cronologia |
| `citta_antica` | Uruk, Tebe, Babilonia | 9 | il rilievo moderno non dice niente: piano separato |
| `porta` | `PT-COL` (Ferrara) | 4 | **non si disegna**: è un'uscita dal nodo |
| `area` | l'Addizione Erculea, la villa dei Gracchi | 2 | polilinea d'area, edifici dentro |

Il quinto anno è la conferma: 11 delle sue 30 tappe hanno una casella che non è
un luogo, e il documento del quinto anno lo dichiara da subito («l'unico anno in
cui una tappa è un'operazione e non un luogo»). Adesso è anche nei dati.

**Coordinate.** 54 su 95 verificate, e ogni scheda registra **a quale articolo di
Wikipedia il nome ha corrisposto**: senza quel campo, «Roma, Curia» che risolve
sulla Curia romana e «Ferrara, corte» che non risolve su niente sarebbero due
vuoti identici. Le altre 41 hanno uno **stato dichiarato**, mai un vuoto silenzioso:

| stato | Quanti | Significato |
|---|---|---|
| `verificata` | 55 | risolta, con la fonte |
| `non_e_un_luogo` | 23 | è una porta o una situazione: non ha coordinate per definizione |
| `da_geocodificare_wfs` | 7 | è dentro Ferrara: si prende dal WFS del Comune, che c'è |
| `da_geocodificare_a_mano` | 10 | edificio o area: serve un'altra fonte, e si sa quale |

*(erano 54, 24, 7 e 11 il 03/10/2026: il registro è stato rigenerato e i due luoghi che sono cambiati sono Pataliputra, che ha trovato una coordinata verificata, e Manchester, che è uscita perché la tappa 3-28 ora dice Torino.)*

## 3. Lo schema del dettaglio: che cosa deve sapere il motore

Ogni luogo ha questi campi. La regola è che **un campo vuoto è un dato
dichiarato** (motore: non ti fidare, usa il default tipologico e dillo), mentre
un campo riempinto a stima sarebbe una bugia.

| Campo | Che cosa contiene | Chi lo riempie |
|---|---|---|
| `impianto` | forma della piazza, lati, assi, portici, fossato, viali | fonte storica |
| `materiali` | mattone, pietra, marmo, legno, terra — **con il colore** | fonte storica |
| `edifici` | ogni edificio: anno di costruzione, e rifacimenti | fonte storica |
| `cronologia` | che cosa c'era in un dato anno | fonte storica |
| `terreno` | quota, pendenza, esposizione, rilievo | **automatico**, misurato |
| `vuoto` | che cosa non si sa, detto per esteso | a mano |

Il campo che manca in tutti gli schemi precedenti è **`cronologia`**, ed è quello
che rende il gioco onesto. Una tappa che si svolge a Ferrara nel 1450 **non può
usare la piazza di oggi**: nel 1450 la statua di Alessandro VII non c'era (arrivò
nel 1660), il monumento a Vittorio Emanuele II non c'era (1889), e il sagrato non
era stato abbassato (anni Venti del Novecento). Sono tre differenze documentate
nello stesso posto, a trecento anni di distanza. Senza cronologia il gioco mostra
a un ragazzo del 1450 il Novecento.

### Il riferimento compilato: Ferrara

`dati/dettagli_ferrara.json` è il primo record compilato per intero, ed è il
modello. Contiene sette luoghi con la loro cronologia e le fonti. Le cose che
**non** ci sono, e che sono le più importanti, ci sono come vuoti dichiarati:

- le **dimensioni in metri** della piazza del Duomo: non sono nelle fonti usate,
  e non sono state stimate;
- la **pavimentazione** nel 1135 e nel 1450: il *volto* ferrarese è una
  tradizione documentata della città, ma quando fu rifatta questa piazza non lo
  so, e quindi non lo scrivo;
- il **luogo** della fonderia, dell'archivio e della cappella: nessuna fonte usata
  li colloca. Sulla cappella anzi ci sono due candidate documentate (quella ducale
  del Castello, nata per Renata di Francia, e quella di san Giuliano) e scegliere
  senza sapere sarebbe inventare.

Tre vuoti su sette voci, dichiarati uno per uno. È il risultato giusto: il primo
record compilato dice di più sul metodo di dieci record completati a mano.

## 4. La topografia, e perché aiuta più di quanto sembri

Il rilievo si prende dai **Terrarium** di AWS Open Data, derivati da SRTM:
una richiesta HTTP per tassello, **senza registrazione**, e i numeri sono buoni.
`dati/mappe/rilievo_penisola.json` e `rilievo_europa.json` **ci sono**: sono
**212 e 186 righe**, tutte le città dei due file di Natural Earth, misurate il
4 ottobre 2026 da `sorgenti/gis/rilievo.py`, che per ogni città dà quota,
pendenza (m/km), esposizione e rilievo locale.

**La misura non ha bisogno di Pillow, perché il progetto non installa
pacchetti.** Il PNG di Terrarium si decodifica con `zlib` e i cinque filtri di
riga che specifica il formato: quarantacinque righe in
`sorgenti/gis/png_terrarium.py`, un modulo che non importa nessuno e serve a
tutti gli script che misurano. Prima erano due copie dello stesso algoritmo —
`rilievo.py` con Pillow e `rilievo_senza_pil.py` senza — e due copie di un
algoritmo sono due numeri che un giorno divergono.

**Il numero che questa sezione dichiarava non era verificabile, e il vero
errore è più grande.** «Verificato su 14 punti ad altitudine nota, errore medio
assoluto 12,6 m» non aveva nessuno dietro: i quattordici punti erano scelti a
mano e i loro numeri erano scritti a mano nella stessa frase che li dichiarava.
Adesso il riferimento lo chiede qualcun altro — **Wikidata**, proprietà `P2044`,
cercando **la stessa città per posizione e non per nome** — e il conto lo rifa
`sorgenti/gis/verifica_rilievo.py` su **32 punti** campionati fra le 398 città:
**errore medio assoluto 32,9 m**, **massimo 155 m**, **otto errori sopra i 50 m**.
Le nove città del campione che Wikidata non conosce o non quota restano fuori,
e il file le dichiara per nome: un campione di trentadue punti su quarantuno è
un campione, uno di quarantuno su quarantuno con i mancanti riempiti a mano
sarebbe una bugia.

**I 155 m che restano non vengono dal pixel.** Il difetto dell'indice del pixel
è corretto (è quello descritto sotto); quello che resta è che **la coordinata
di una città non è il suo centro**: Catanzaro ha un riferimento di 342 m e legge
187 m, Potenza ha 819 m e legge 724 m, e sono due città su un pendio, dove a
pochi chilometri la quota cambia di quelle cifre. Algeri è il caso inverso —
riferimento 0 m, misura 72 m — ed è l'unico in cui il numero più grossolano è
il riferimento: è restato com'è, perché un dato esterno non si sceglie per
quanto assomiglia a quello che si vorrebbe.

**Due città si chiamano uguale, e il file le tiene entrambe.** Nel file delle
città di Natural Earth `Ragusa` è in Italia e in Croazia e `Kasserine` è due
volte in Tunisia: la chiave di un punto non può essere il nome, e ora è la
coppia di coordinate. Restano **50 coppie** di righe a meno di 700 metri l'una
dall'altra — è la fonte a metterle lì accanto, non il misuratore — e il
verificatore le conta e le dice invece di far finta che non ci siano.

Il primo errore di questa tabella è stato di **132,6 m**, e la causa è da
raccontare: per l'indice del pixel dentro il tassello usavo il resto della
divisione per 16, che è l'indice di un *tassello* a livello superiore, non di un
*pixel* — il tassello ha 256 pixel, non 16. Leggevo un punto diverso da quello
richiesto, e i numeri erano sbagliati di qualche centinaio di metri senza che
nulla lo segnalasse. Il Duomo di Firenze leggeva 254 m (è a 50), piazza Grande ad
Aosta 1 085 m (è a 583). Il metodo corretto calcola il pixel **globale** e sottrae
l'origine del tassello, ed è stato verificato leggendo il profilo del tassello: la
riga del Duomo dà 57–72 m e quella di Aosta 581–583 m.

**Cosa ne fa il generatore delle sagome**, in ordine di quanto conta:

1. **le altezze sfalsate** — un edificio appoggiato su una strada in pendio sta a
   un'altezza diversa dal vicino, e se il terreno non sale la fila di edifici
   sembra una fila di cartoni;
2. **il profilo contro il cielo** — è la sagoma della città, ed è metà della
   percezione di una vista 3/4; dipende dal rilievo, non dagli edifici;
3. **la pendenza della copertura** — un tetto a capriate su un pendio ripido
   diventa un tetto a padiglione, e su un pendio dolce resta a falda;
4. **l'esposizione** — la facciata che guarda a nord gela, quella a sud si scalda:
   decide finestre, aggetto e ombra portata, ed è geometria vera, non una scelta
   estetica;
5. **l'altezza minima di impianto** — in un terreno sotto il livello del mare
   l'edificio sta su un rialzo, e la piazza sta su una quota precisa: a Ferrara la
   differenza è di pochi metri e si vede.

Il rilievo **non** dà l'altezza di un singolo edificio, e non finge di darla. Per
quello si usa il modello a tre livelli che `mappe.md` §5.1 ha già, e che resta
giusto: `lidar` dove c'è, `osm` dove c'è, `stimata` altrove — **con la fonte
dichiarata in faccia all'edificio**, come i campi `attendibilita` e `manca` del
registro dell'anno 4.

## 5. Una regola che si è fatta pagare quattro volte

**Una richiesta che non arriva non è una risposta negativa.**

È successo quattro volte in due giorni, sempre nella stessa forma. Wikipedia
risponde `HTTP 429` a raffica; l'errore non è un codice di stato ma un corpo
vuoto; il codice che lo riceveva non lo distingueva da una risposta vera e
scriveva l'assenza come un fatto. Le quattro volte:

| Dove | Che cosa è stato scritto | Che cosa era vero |
|---|---|---|
| `cerca_ritratti.py` | «nessun ritratto in testa all'articolo» per 15 personaggi | Dürer, Turing, Leibniz, John Snow, Josquin, Bellini hanno tutti un ritratto |
| `ripara_licenze.py` | «file non letto su Commons» per 8 file | i file c'erano, cercati come pagine invece che come file |
| `ritratto_reale.py` | «download fallito» per 6 immagini | i file c'erano, era un 429 non ascoltato |
| `coordinate.py` | «nessun articolo» per 30 luoghi | Uruk, Tebe, Xianyang, Qufu hanno le coordinate |

La correzione è sempre la stessa, due righe: il client ascolta il `Retry-After`, e
l'esito distingue **`non_trovato`** (risposta avuta, niente) da **`richiesta_fallita`**
(nessuna risposta). Una richiesta fallita non chiude mai una scheda: la lascia
`da_rifare`. È in `AGENTS.md`, e va tenuto in tutti gli script che parlano con
qualcosa.

## 6. Gli interni: che cosa si può davvero attraversare

**La domanda.** L'anno 1 si gioca dentro Ferrara, in trenta edifici reali. Di
quegli edifici il progetto ha la **sagoma** — il poligono da OpenStreetMap —
e non ha l'interno: il giocatore vede una facciata e non ci entra. Che cosa si
può scrivere, senza inventare?

**La risposta breve: le stanze che la fonte nomina una per una.** Non un
catalogo di interni e non una pianta: quello che Wikimedia Commons dichiara,
con il nome che dà alla fonte, e con quante fotografie libere ci sono. Il file
è `dati/interni_edifici.json` (38 kB), il generatore è
`sorgenti/interni_edifici.py`, i controlli sono `sorgenti/verifica_interni.py`.

| | |
|---|---|
| edifici dell'anno 1 | 30 |
| con una categoria di Commons | 23 |
| **con almeno una stanza** | **11** |
| stanze trovate | 41 |
| stanze con almeno una fotografia libera | 41 |
| fotografie, tutte con licenza libera dichiarata | 830 |
| edifici dichiarati senza categoria, con il perché | 7 |
| categorie di Commons condivise da più tappe | 1 |

### 6.1 Gli interni che si possono attraversare

| Tappa | Edificio | Stanze | Foto libere | Le stanze, con il nome che dà la fonte |
|---|---|---|---|---|
| `1-4` | Museo della Cattedrale (ex San Romano) | 1 | 75 | Cloister |
| `1-7` | Palazzo Municipale e Volto del Cavallo | 2 | 61 | Camerino delle Duchesse, Sala Arazzi |
| `1-8` | Castello Estense | 18 | 342 | Alfonso I d'Este's Camerino d'Alabastro, Anticamera del Governo, Camerino dei baccanali, Chapel, Dungeon, Kitchens, Sala Gotica 1, Sala degli stemmi, Sala dei Comuni, Sala dei Paesaggi, Sala del Governo, Sala dell'Aurora, Sala della Devoluzione, Sala delle Geografie o Marchesana, Sala di Ettore e Andromaca, Saletta dei Giochi, Saletta dei Veleni, Salone dei Giochi |
| `1-10` | Palazzo Paradiso (Biblioteca Ariostea) | 5 | 53 | Anatomical theater, Sala Agnelli, Sala Riminaldi, Sala dei Falconi, Sala di Ercole |
| `1-12` | Casa Romei | 2 | 90 | Courtyard, Secondary Courtyard |
| `1-13` | Monastero del Corpus Domini | 1 | 11 | Sala del Coro |
| `1-14` | Monastero di Sant'Antonio in Polesine | 1 | 3 | Cloister |
| `1-15` | Palazzo Schifanoia | 8 | 149 | Hall of the battles, Hall of the busts, Hall of the white eagle, Room of Leonello, Room of the double lancet windows, Sala conferenze, Sala delle Virtù, Salone dei Mesi |
| `1-16` | Palazzo Bonacossi | 1 | 4 | Courtyard |
| `1-17` | Palazzina Marfisa d'Este | 1 | 36 | Loggia degli Aranci |
| `1-25` | Casa di Ludovico Ariosto | 1 | 6 | Courtyard |

### 6.2 Perché la fonte è Commons e non un'altra

Un blog di viaggi dice «il castello ha delle sale», e non si può codificare.
Commons ha `Category:Castello Estense (Ferrara) - Chapel`, e si può. È la stessa
fonte che il progetto usa già per le sagome, per i ritratti e per le immagini
degli oggetti, ed è l'unica che **distingue una stanza dall'altra con un nome
proprio** dentro una categoria. E le categorie sono fatte una per ambiente: la
fonte non scrive «il castello ha delle sale» in un paragrafo, apre una
sottocategoria per ciascuna.

Le fotografie sono tutte con licenza libera dichiarata: CC BY-SA 4.0 (473), CC BY-SA 3.0 (302), CC BY 3.0 (15), Public domain (13), CC BY-SA 2.5 (9), CC BY 2.5 it (7), CC BY-SA 2.0 (7), CC0 (3), CC BY 2.5 (1). La licenza si
**legge dai metadati di ciascun file** e non si deduce dalla presenza della
fotografia — una foto senza licenza non è un bene libero, e il progetto lo sa
già per gli oggetti, dove dodici candidati sono stati respinti per metadati
mancanti.

### 6.3 Il metodo, e le quattro regole che tengono

Il nome che il gioco scrive e il nome che Commons scrive sono due nomi
diversi, e il primo metodo — il titolo esatto — lasciava 7 edifici su
30 senza categoria. Le regole che tengono, in ordine:

1. **prima per titolo esatto**, con 5 qualificatori provati in
   ordine (NOME (Ferrara) - Interior, NOME - Interior, NOME (Ferrara), NOME, NOME, Ferrara); poi **per ricerca**, sui nomi che il registro
   ricava dal nome dell'edificio: la parte fra parentesi, la parte prima dei due
   punti, la parte prima di una congiunzione. «Palazzo Turchi di Bagno e Orto
   Botanico» è un palazzo e un orto in una voce sola, e nessuna delle due metà è
   il nome di una categoria. Vince il primo candidato che risponde **e parla
   dell'edificio**: dev'essere la categoria dell'edificio, non una collezione
   di opere che lo riguardano;
2. **la città.** Il gioco gioca a Ferrara, e una categoria è accettata solo se
   dichiara Ferrara o nessuna città. Senza questa regola il Museo del
   Risorgimento e della Resistenza di Ferrara era diventato quello di Vicenza,
   e poi il Vittoriano di Roma: stesso nome, tre città, e il file sceglieva il
   più conosciuto. Anche le sottocategorie si guardano: il Teatro Comunale di
   Ferrara su Commons ha il nome di quello di Treviso, e la città che lo
   dichiara è in una sottocategoria;
3. **la stanza è una stanza se il nome lo dice**: prima escludendo, e ogni
   esclusione porta il motivo (23 motivi), poi cercando una parola di
   ambiente fra le 63 parole di `parole_di_ambiente`, in italiano e in
   inglese. Le esclusioni si guardano sul nome **intero** della categoria e le
   inclusioni sul nome **ripulito** dell'edificio, perché il nome dell'edificio
   ci mette dentro parole di ambiente — «Museo» nel nome del Museo Casa Romei —
   che non sono quelle di nessuna stanza;
4. **la licenza si confronta dopo aver tolto spazi, trattini e punti.** Il nome
   breve della fonte è `CC BY-SA 4.0` e la chiave del progetto era
   `cc-by-sa-4.0`: un trattino di differenza e il confronto non agganciava
   niente. Le prime due esecuzioni contavano **3 immagini libere su 663**,
   tutte e tre CC0, e avevano respinto 385 fotografie CC BY-SA 4.0. Il numero
   era giusto e il verdetto falso.

### 6.4 Che cosa non c'è, e perché non c'è

| | |
|---|---|
| 12 edifici con categoria ma senza stanze | la fonte non divide gli interni uno per uno: le sottocategorie ci sono e sono tutte scartate con il motivo, che si legge in `non_stanze` |
| 7 edifici senza categoria | nessun nome provato e nessun candidato parlano dell'edificio; il perché è per ciascuno, in `vuoto` |
| le **dimensioni** delle stanze | nessuna fonte libera del progetto le dà per iscritto: restano vuote finché non si rileva |
| il **campo `stanza`** di `luoghi_gioco.json` | è un luogo narrativo del Furioso («il bosco dove Orlando perde il senno»), non un ambiente visitabile: le due cose non si sommano e non si confondono |

### 6.5 I controlli, e che cosa hanno visto

Sette controlli in `sorgenti/verifica_interni.py`, tutti a exit 0:

| | |
|---|---|
| **I1** | ogni tappa dell'anno 1 c'è negli interni, una volta sola, col suo argomento |
| **I2** | i numeri del riepilogo sono contati sul file, non dichiarati |
| **I3** | le stanze sono stanze per la regola scritta, e ogni esclusione dice perché |
| **I4** | le licenze sono fra quelle accettate e i numeri delle immagini tornano |
| **I5** | ogni assenza dice perché, e nessuna è un edificio mai cercato |
| **I6** | le categorie sono di Ferrara, e se stanno su più tappe il file lo dichiara |
| **I7** | i numeri che questo capitolo dichiara sono quelli che il file ha |

`--difetti` inietta **11 difetti** e li vede tutti. Sono voluti anche
quelli che non riguardano il numero: una categoria di un'altra città spacciata
per edificio, una categoria di opere spacciata per stanza, una categoria
condivisa fra due tappe e non dichiarata. Un difetto che cambia una cifra si
vede anche senza il difetto che cambia una parola.

**I7 è nato da una riga di questo capitolo che era rimasta ferma.** La
riga 6.6 diceva che il chiostro di Sant'Antonio in Polesine «era stato scartato
per una regola sul nome» — vera quando fu scritta, e falsa quando la regola
fu corretta e il chiostro tornò (tappa 1-14). Nessuno l'aveva riletta: è la
malattia di questa sessione nella forma più semplice, **una riga scritta una
volta e non riscritta**, e la cura non è rileggerla ogni volta: è un controllo
che confronta i numeri del capitolo con quelli del file, per etichetta.

Il difetto che lo prova è voluto, ed è l'unico che la prova non inietta nei
dati: **scrive il capitolo alterato in un file temporaneo**, lo fa guardare e
poi lo cancella. La prova non tocca mai il documento vero.

**Quattro difetti veri, nessuno visibile a occhio**, tutti e quattro della
stessa forma — un numero giusto e una frase sbagliata. Li elenca il registro
qui sotto; il più grave è il terzo: il file scriveva, sotto il nome del museo
che il gioco mostra, le stanze di un museo omonimo di un'altra città. Il
numero di stanze era giusto e l'edificio falso.

### 6.6 Cosa c'è da fare con questi interni

| | |
|---|---|
| **le 41 stanze come ambienti di gioco** | il campo che manca è `ambiente`: percorso, uscita, che cosa si può fare dentro |
| i 12 edifici con categoria ma senza stanze | le sottocategorie ci sono e sono scartate tutte, con il motivo in `non_stanze`. I motivi, contati sul file: nessuna parola di ambiente nel nome della stanza: il nome non dichiara che sia una stanza (22 volte), le immagini storiche non sono un interno (3 volte), il nome comincia col nome di un'istituzione: è la stessa cosa detta altrimenti, non un ambiente fra gli ambienti (3 volte). Le esclusioni si guardano una per una: il chiostro di Sant'Antonio in Polesine era fra le vittime di una regola sbagliata sul nome ed è tornato quando la regola è stata corretta (tappa 1-14) |
| le **piante** | nessuna fonte libera le dà: il WFS del Comune dà sagomi, non muri interni |
| **le fotografie scaricate** | qui si interroga e si decide, come in `cerca_ritratti.py`: il download è un'altra fase |

## 7. Cosa c'è da fare

| | |
|---|---|
| **compilare i 48 `citta`** con lo stesso schema di Ferrara | il lavoro vero, e non è breve: ognuna vuole impianto, cronologia e fonti |
| i 7 luoghi di Ferrara dal **WFS del Comune** | le coordinate sono lì, e le sagome anche |
| i 10 `da_geocodificare_a_mano` | Roma (Curia, Campidoglio, villa dei Gracchi), Bolzano, Squillace, Bethesda, Londra |
| i 9 `citta_antica` | Uruk, Tebe, Babilonia, Elea: servono piante ricostruite, non il rilievo moderno |
| **il generatore delle sagome** | è la vera lacuna: senza, le altezze restano stimate ovunque fuori Ferrara |
| ~~scaricare `rilievo_penisola.json` e `rilievo_europa.json`~~ **fatto il 04/10/2026** | **212 + 186 = 398 città** misurate e verificate: `sorgenti/gis/verifica_rilievo.py`, sei controlli |
| le **dimensioni** delle piazze | nessuna fonte le dà per iscritto: o si rilevano dal WFS o restano vuote |

## 8. Il registro delle modifiche

### v0.6 — 05/10/2026

**Una riga di questo capitolo era rimasta ferma, e la cura è un controllo che
confronta i numeri del capitolo con quelli del file.**

La riga 6.6 — «i dodici edifici con categoria ma senza stanze» — diceva che il
chiostro di Sant'Antonio in Polesine «c'è ma era stato scartato per una regola
sul nome». La frase era vera quando fu scritta; la regola è stata corretta
nello stesso giorno e il chiostro è tornato, nella tappa 1-14. Nessuno l'aveva
riletta, perché **una riga scritta una volta e non riscritta non lascia traccia
nei controlli dei numeri**: il dato muove, la frase no, e nessuno li confronta.

Il **controllo I7** confronta i numeri che la sezione §6 dichiara con quelli
che `dati/interni_edifici.json` ha, per etichetta e non per posizione, e li
confronta anche quando il numero sta nella cella che porta l'etichetta («i 12
edifici con categoria ma senza stanze») e non in quella dopo. Guarda anche il
numero dei controlli che questo capitolo dichiara in prosa. Il difetto che lo
prova scrive il capitolo alterato in un file temporaneo, lo fa guardare e poi
lo cancella: **la prova non tocca mai il documento vero**.

La riga 6.6 non è stata corretta a mano ma **riscritta dal file**: i motivi di
esclusione degli edifici che hanno una categoria e nessuna stanza sono contati
sul dato, così la riga non può invecchiare un secondo giro. E il paragrafo
sui difetti diceva «Tre difetti veri» raccontandone uno solo, mentre il
registro ne elenca quattro: due numeri che non tornavano fra loro nello stesso
capitolo, che è la stessa malattia detta in un'altra lingua.

### v0.5 — 05/10/2026

**Gli interni degli edifici dell'anno 1, presi dalla fonte, e quattro difetti
che il conto dei numeri non avrebbe mai visti.**

L'anno 1 si gioca dentro trenta edifici reali di Ferrara e il progetto ne
aveva solo le sagome: il giocatore vedeva una facciata e non entrava. La
raccolta guarda le trenta tappe su Wikimedia Commons, che è l'unica fonte che
*distingue una stanza dall'altra con un nome proprio* dentro una categoria, e
scrive quello che la fonte dichiara: 41 stanze in 11 edifici, con
830 fotografie e la licenza di ciascuna letta dai metadati. Quello che la
fonte non dichiara resta dichiarato vuoto, con il perché: 7 edifici
senza categoria e 12 con categoria ma senza stanze, e ogni esclusione
porta il motivo.

Quattro difetti, tutti della stessa forma — un numero giusto e una frase
sbagliata:

- **385 fotografie CC BY-SA 4.0 respinte per un trattino.** Il confronto fra la
  chiave `cc-by-sa-4.0` e il nome breve della fonte `CC BY-SA 4.0` non
  agganciava niente: tre sole immagini libere su 663, tutte e tre CC0. Ora il
  confronto passa da una normalizzazione e tutte e 663 sono libere.
- **un museo di un'altra città sotto il nome di quello che il gioco mostra.**
  Il Museo del Risorgimento e della Resistenza esiste a Vicenza e a Roma; il
  file aveva preso il Vittoriano, che è il più conosciuto dei tre. Ora la città
  si guarda nel titolo e nelle sottocategorie, e il gioco gioca a Ferrara.
- **un criterio di una parola sola.** «Cattedrale di San Giorgio» finiva sul
  Museo della Cattedrale: una parola su due. Ora ne servono due quando il nome
  del gioco ne ha due.
- **un metodo sbagliato, dichiarato giusto.** Le stanze si cercavano dentro la
  categoria dell'edificio: su Commons stanno in una categoria separata che si
  chiama `... - Interior`, e la prima esecuzione aveva reso **una stanza su
  trenta edifici**.

E due numeri che invecchiavano da soli, del genere di difetto che questa
sessione ha già trovato tre volte: il blocco `metodo` scriveva «tre
qualificatori» quando erano 5, e il contatore delle parole di
ambiente diceva «66» per un pattern che ne contiene 63. Entrambi sono ora
generati dalla regola che descrivono.

Le regole nuove hanno un costo, e va detto: hanno fatto perdere qualche voce.
`Museo Boldini` era una stanza del Palazzo Massari, ed è una stanza che non
esiste — è il museo che sta dentro il palazzo, detto due volte. Lo stesso per
`Museo Casa Romei` e per le categorie di quadinti e mobili. Sono state scartate
con il motivo, e il file le mostra in `non_stanze`: una lista scartata senza
dire perché sembra una lista arbitraria.

Le tre tappe della Certosa sono parti di un complesso solo e finiscono sulla
categoria unica del complesso. È giusto, ma il file lo dichiara in
`categorie_condivise` e il controllo I6 lo pretenderebbe anche: una cosa
ripetuta senza traccia è un numero che si crede due volte.


### v0.4 — 04/10/2026

**I due file di rilievo che il documento prometteva dal 2 ottobre esistono, e
produrli ha trovato tre difetti che nessuno dei controlli precedenti vedeva.**

- **`rilievo.py` scriveva un nome di città che non è un nome.** Le città di
  Natural Earth hanno le proprietà in un dizionario, e la riga che sceglieva il
  nome (`props[0] se isinstance(props, list) else props`) scriveva il
  **dizionario intero** al posto del nome: un file pieno di righe intitolate
  «{NAME: Ferrara, ADM0NAME: Italy}». I numeri giusti con il titolo che non è
  un titolo, che è il difetto più difficile da vedere guardando i numeri;
- **la fusione dei file accodava ogni città quattro volte.** Il batch scrive il
  file ogni venti città con tutti i punti misurati finora, e la fusione li
  aggiungeva a quelli già dentro senza chiederlo: il conto diceva **408 città su
  212**. E il rimedio per mettere i punti a posto — ripulire per nome — ne
  **perdeva due**, perché Ragusa e Kasserine sono due città ciascuna. La chiave di
  un punto ora è la coppia di coordinate, e `--riprendi` ripara il file prima di
  riprendere il batch;
- **`rilievo.py` e `rilievo_senza_pil.py` erano due copie dello stesso algoritmo**,
  una con Pillow e una senza: due numeri che un giorno divergono. Il
  decodificatore è ora un modulo solo, `png_terrarium.py`, e il batch e la prova
  danno lo stesso valore per costruzione, non per verifica.

**Il numero dichiarato da due giorni era falso, e il vero errore è maggiore.**
«14 punti, errore medio 12,6 m» non aveva dietro nessun riferimento:
i punti e i loro numeri erano scelti a mano nella stessa frase che li dichiarava.
Ora il riferimento viene da **Wikidata** (`P2044`), cercando la stessa città per
posizione, e `verifica_rilievo.py` ricalcola tutto: **32 punti, errore medio
32,9 m, massimo 155 m**. Il verificatore legge anche la cifra scritta qui e la
confronta: se le due divergono, è un difetto, non un aggiornamento.

**Un numero scritto a mano che era sbagliato di 543 metri.** Il campo `terreno`
del registro dei luoghi era l'ultimo campo compilato a mano, ed era stato
misurato con la versione di `rilievo.py` che leggeva il pixel sbagliato:
**Torino a 785 m**, che non è Torino ma una collina a sette chilometri, e la
città è a 239 m. Le altre 54 erano giuste per caso, perché sono città in piano e
su un piano il pixel sbagliato dà quasi la stessa risposta: è la parte peggiore di
un difetto di coordinate, passa quasi sempre e quando sbaglia sbaglia di
mezzo chilometro. Ora `terreno` non è più di mano: lo produce
`sorgenti/luoghi/terreno.py`, che ha anche riempito Pataliputra, che non ce
l'aveva.

Il controllo che tiene tutto è `sorgenti/gis/verifica_rilievo.py`, sei controlli:
i campi che il documento promette, **le righe contro le città di partenza** (è
il primo che avrebbe visto i duplicati), i numeri plausibili con un punto sotto
il mare e uno sopra i mille metri, le città che si somigliano dette per nome,
l'errore contro il riferimento confrontato anche con la cifra di qui, e la
stessa città misurata due volte (registro e file delle città) entro la
tolleranza dichiarata.

### v0.3 — 03/10/2026

**Il registro dei luoghi è stato rifatto dalla catena, e i numeri sono cambiati per un motivo buono.** `verificata` da 54 a **55**, `non_e_un_luogo` da 24 a **23**, `da_geocodificare_a_mano` da 11 a **10**. Le due mosse sono Pataliputra, che ha trovato una coordinata verificata (25.6125 N 85.12833 E) quando il geocodificatore l'ha cercata, e Manchester, che esce dal registro perché la tappa 3-28 ora dice Torino (Primo Levi) e non Manchester (Turing). Karakorum non è più un caso dichiarato a parte: la correzione che il controllo dei pin aveva trovato il 2 ottobre sta ora in `dati/luoghi_correzioni.json` e viene riapplicata a ogni rigenerazione.

La correzione che conta è un'altra, ed è quella che ha reso necessaria la prima: **`estrai_luoghi.py` leggeva le colonne per numero, e l'anno 5 ha una colonna in più** — la stanza, fra il pin e la voce — quindi in ventinove tappe su trenta il campo `voce` conteneva il filone del *Furioso* invece della persona. Ora la tabella si legge per intestazione. E il registro non è più un file che si corregge a mano: `aggiorna_registro.py` lo rifa unendo i dati nuovi a quelli che si compilano a mano, perché la versione di prima cancellava il terreno misurato, i dettagli e i trenta binomi pin/stanza del quinto anno.


### v0.2 — 02/10/2026

Controllo di coerenza su tutto il progetto. Tre correzioni, tutte sulla stessa
riga: le **coordinate**. I dati hanno **54 luoghi con coordinate**, dei quali **53
verificati** e uno dichiarato `da_verificare` (Karakorum, il caso dei 8 128 m
descritto sotto): il documento li chiamava tutti e 54 «verificate», che è vero
solo se si ammette che una verifica può fallire. Ora il numero è giusto e il
caso dichiarato è detto. Le **41 coordinate mancanti** erano giuste: sono i 24
luoghi che non sono un luogo, i 10 da geocodificare a mano e i 7 da interrogare
al WFS. Terza correzione: `rilievo_penisola.json` e `rilievo_europa.json` sono
dichiarati **da produrre** e non dati per esistenti: lo script c'è, l'esecuzione
no, e un documento che promette un file inesistente è un documento che un giorno
farà perdere mezz'ora a qualcuno.

### v0.1 — 02/10/2026

Prima stesura. Creati `sorgenti/luoghi/estrai_luoghi.py`, `coordinate.py`,
`classifica.py`, `sorgenti/gis/rilievo.py`; `dati/luoghi_estratti.json`,
`luoghi_geo.jsonl`, `luoghi_gioco.json`, `dettagli_ferrara.json`.

Contenuto: i 95 luoghi del gioco con tappe e anni, 55 coordinate con la fonte e
l'articolo risolto — tutte quante verificate, Karakorum compresa, che il
controllo ha preso con la quota e non con il titolo (v. sotto) —, la
classificazione in sette tipi, la decisione su
ODbL, lo schema del dettaglio con il campo `cronologia`, e il primo record
compilato per intero (Ferrara, sette luoghi, tre vuoti dichiarati).

Cinque difetti trovati e corretti lungo il cammino, tutti verificati contro dati
noti e non a occhio:

1. l'indice del pixel dentro il tassello era quello di un tassello: errore medio
   di 132,6 m, sceso a **12,6 m** con il calcolo del pixel globale;
2. l'estrazione leggeva la colonna sbagliata nell'anno 4, e per venti minuti
   l'inventario ebbe trenta nomi di persone al posto di trenta luoghi — visto
   perché nessuno di quei nomi ha coordinate;
3. tredici edifici e aree erano classificati come «città»;
4. il `429` letto come assenza, per la quarta volta (§5);
5. l'inventario non poteva essere rifatto, perché la colonna del luogo cambia nome
   fra gli anni (`Luogo (pin)` e `Pin`) e le colonne extra non erano dichiarate:
   ora la tabella è letta **per intestazione**, con il perché della correzione
   accanto. È la correzione che il 03/10/2026 ha reso necessaria per un motivo
   nuovo: l'anno 5 ha una colonna in più (la stanza) e il numero fisso leggeva
   la stanza al posto della voce, in ventinove tappe su trenta.

Aggiunto dopo: il **rilievo dei 55 luoghi** con coordinate, e la sua
verifica ha trovato un settimo difetto. **Karakorum è a 8 128 m**: il nome ha
risolto sull'articolo «Karakorum» e il titolo combacia, ma quello non è la
capitale mongola di Gengis Khan, è un altro luogo omonimo. È l'unico caso in cui
il controllo l'ha preso **la quota e non il titolo**, e la scheda porta
`coord_stato: da_verificare`. Il rilievo, insomma, non serve solo a disegnare: fa
anche da controllo sulla geocodificazione, ed è l'unico controllo che l'ha preso.
