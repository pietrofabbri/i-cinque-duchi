---
titolo: Videogioco "I cinque duchi" — i premi: undici categorie di oggetti, undisciplina ciascuna, e le quattro prove che un premio deve superare
tipo: normativo
versione: 0.9
data: 2026-10-07
autore: Pietro Fabbri (con Claude)
fonte del materiale: richiesta di Pietro del 03/10/2026, superata sull'informatica il 04/10/2026 (v0.5: i centocinquanta livelli informatici hanno un premio come gli altri, e il catalogo sale a 1050); richiesta di Pietro del 03/10/2026 («per ogni livello, per ogni disciplina, tranne informatica, occorre stabilire dei premi... per il ferrarese potrebbero essere figurine di ferraresi illustri che non vengono citati nella storia, per la lingua italiana poeti e autori italiani, poi i premi potrebbero essere dipinti, sculture, opere architettoniche... pensa a cosa potrebbe essere associato come ricompensa al compimento di ciascun livello»), con le regole gia prese su etichette, oggetti di interazione, luoghi e licenze
dati: dati/lingue/associazioni.json (v1, le 180 voci: trenta per lingua, sei lingue); dati/fonti_visive/fonti_visive.json e dati/lingue/immagini_oggetti.json (le schede con etichetta e licenza, da cui i premi prendono la provenienza); dati/premi.json (v2, il catalogo dei premi: **1050 record**, uno per livello, con la categoria letta da §2, **l'elemento interattivo da cui il livello viene** e i campi dell'oggetto dichiarati vuoti, §5.1 e §5.2); sorgenti/art/out/premi/premi_foglio.png (v2, i 1050 emblemi in un foglio solo, e `premi_indice.json` che dice dove sta ognuno e quale elemento interattivo porta, §5.3); sorgenti/art/out/premi/forme_prova.png (v2, le undici forme alla scala reale, per poterle guardare)
controllo: python3 sorgenti/premi_catalogo.py (scrive `dati/premi.json` e si ferma se due chiavi coincidono, se una categoria non è fra quelle dichiarate o se il conto non è 1050), python3 sorgenti/art/verifica_premi_emblemi.py (Q1-Q7: le chiavi sono distinte, ogni tessera è dentro il foglio e il foglio si decodifica, le tessere sono tutte diverse sha per sha, ogni categoria usata ha una forma che produce pixel e un perché, ogni tessera corrisponde a un premio, e **le cinque caselle della firma portano il numero dell'elemento interattivo, riletto dai pixel**; con --difetti ne inietta sette e ne pretende sette visti), python3 sorgenti/verifica_premi.py (P1-P8: le categorie sono chiuse e senza buchi, ogni disciplina ha almeno una categoria primaria, i sei ambiti della sfida a mani nude hanno ciascuno un premio possibile, nessuna categoria e' assegnata a una disciplina che il progetto non ha, la sezione delle prove **non descrive un premio generato come una cosa lecita** e dice che cosa vieta, e i quattro campi dell'oggetto sono `null` **in tutti e millecinquanta i record** e dichiarati tali in `vuoto`, **ogni record porta l'elemento interattivo e l'argomento che `lingue.md` dà per quel livello**, le trenta voci sono dichiarate in due file che devono dire la stessa cosa, e **nessun rimando a una prova che §3 non dichiara**)
documenti collegati: videogioco-5-duchi-inventario.md (v0.2, gli elementi interattivi e i quattro registri personali), videogioco-5-duchi-lingue.md (v0.2, le sei lingue e i 900 livelli), videogioco-5-duchi-lingue-immagi.md (v0.2, le 180 voci, le quattro immagini e le nove etichette), videogioco-5-duchi-quadro-trasversale.md (v0.2, i quattro ambiti e le arti per anno), videogioco-5-duchi-ritratti.md (v0.5, la regola del ritratto autentico e dell'emblema), videogioco-5-duchi-pedagogia.md (v0.2, il vantaggio tangibile e la lacuna «osservazione e attenzione»), videogioco-5-duchi-ripassi.md (v0.4), videogioco-5-duchi-luoghi.md (v0.7), FONTI-E-LICENZE.md, AGENTS.md
---

# I premi

## 0. Che cosa è un premio, in una frase

È **un oggetto vero che il ragazzo guarda e che gli dice che cosa sa adesso**. Non una medaglia, non un punto, non una promessa: un'opera che esiste, che ha un autore o una data, e che si può aprire e guardare.

La definizione è stretta di proposito, e segue il principio del progetto: **un premio che non ha a che fare con il contenuto del livello è un premio decorativo**. Il vantaggio deve essere tangibile e non promesso (`pedagogia.md` §1.2): il vantaggio qui non è il premio, è **la cosa che il premio fa vedere**.

## 1. Le undici categorie

L'elenco è **chiuso**, e l'undicesima è nata oggi per una ragione che è in §2.1. Una dodicesima non si aggiunge quando manca un premio: si usa una delle undici o si dichiara il vuoto.

| # | categoria | che cosa è | che cosa serve per ottenerlo |
|---|---|---|---|
| **A** | Figure e ritratti | una persona raffigurata, con nome e date | la regola di `ritratti.md`: autentico o emblema, e tre etichette dichiarate |
| **B** | Pittura | dipinto, affresco, mosaico, miniatura | fonte libera, autore, data quando esiste, museo e numero d'inventario |
| **C** | Scultura | statua, bassorilievo, erma, busto | foto libera, autore, data, luogo |
| **D** | Architettura | edificio, piazza, giardino, ponte, strada | foto, data, e **la ragione per cui quell'edificio** |
| **E** | Opere scritte | manoscritto, prima edizione, pagina stampata, partitura | digitalizzazione o immagine del frontespizio, con l'istituzione che la espone |
| **F** | Epigrafi e iscrizioni | lastra, cippo, tabella, bassorilievo con testo | foto della pietra e **trascrizione del testo**, che è metà del premio |
| **G** | Musica | spartito, strumento, disco | partitura in pubblico dominio o registrazione con licenza |
| **H** | Teatro e cinema | locandina, fotogramma, scenografia, manifesto | **diritti**: molte opere moderne sono ancora protette e non si possono usare |
| **I** | Documenti e leggi | la pagina che ha cambiato una regola | immagine del documento, data, e il luogo in cui è stato scritto |
| **J** | Emblemi e stemmi | il simbolo che dichiara un valore | origine, significato, e chi lo ha adottato |
| **K** | Scheda prodotta dal giocatore | **la voce propria**: per la lingua dei segni, la scheda che il giocatore ha scritto, con il segno del livello e la sua frase | nessuna fonte esterna: è il giocatore, ed è l'unico premio che non si può copiare |

Le categorie **E** e **F** esistono perché sono le uniche due che si possono **leggere**. Un premio che si può leggere vale doppio in un percorso di lingue: il ragazzo non la guarda, la **usa**.

## 2. Le associazioni

Una tabella sola, undici righe. La colonna «da escludere» è la parte che vale: dice che cosa **non** si abbina, e il perché.

| disciplina | primaria | secondaria | da escludere, e perché |
|---|---|---|---|
| **Italiano** | **E** — manoscritti e prime edizioni; **A** — poeti e scrittori | **B** per i testi che hanno un'immagine | un dizionario o una grammatica: un oggetto che si compra e non si guarda non premia nessuno |
| **Ferrarese** | **A** — figure di ferraresi illustri **non citati nella storia**; **D** — architettura ferrarese | **B** (Ortolano, Dosso Dossi, Garofalo), **C** (monumenti cittadini) | **le trenta figure delle 30 tappe dell'anno 1**: il premio deve essere la scoperta, non il ripasso |
| **Latino** | **F** — epigrafi latine; **E** — edizioni | **A** — scrittori romani; **D** — architettura romana | qualsiasi premio **da guardare e non da leggere**: il percorso latino è *leggere senza tradurre*, e un'immagine lo contraddice |
| **Inglese** | **E** — prime edizioni in inglese; **H** — cinema (è l'arte principale dell'anno 4, `quadro-trasversale.md` §1) | **A** — autori di lingua inglese | quiz, ricette, giochi da tavolo: un premio che è un esercizio travestito |
| **Lingua dei segni** | **K** — la scheda che il giocatore produce | **A** — le poche figure sorde documentate, quando sono verificabili | **tutto ciò che è scelto per essere famoso invece che per essere della comunità**. Il catalogo non può essere scritto: `lingue.md` Q4 dichiara che una lingua dei segni non si scrive a tavolino, e un premio sì |
| **Greco** | **B** — mosaici e pittura vasare; **C** — statue; **F** — epigrafi greche | **E** — manoscritti bizantini; **D** — acropoli e Partenone | per l'ultimo terzo del percorzo (il greco moderno) servono opere **contemporanee**: solo antichità significa che tremila anni di percorso finiscono in un museo del passato |
| **Diritto** | **I** — Costituzione, codici, trattati | **D** — architettura delle istituzioni | il concetto di legge in astratto: il premio è **una pagina con una data** |
| **Etica** | **I** — la Dichiarazione universale dei diritti umani; **J** — stemmi | **B** — dipinti allegorici | niente senza oggetto: un premio etico che non si può indicare con il dito non è un premio |
| **Filosofia** | **A** — i filosofi; **B** — le allegorie (le lezioni di filosofia di Rembrandt, Goya, Magnasco) | **E** — prime edizioni | l'opera filosofica in astratto: non ha un'immagine, e si premia **il dipinto che la illustra** |
| **Psicologia** | **A** — chi ha descritto il fenomeno (Freud, Kahneman, Tversky); **B** — l'immagine dell'esperimento | — | un esercizio di rilassamento: sarebbe un premio che il gioco stesso dovrebbe fare per primo |
| **Osservazione e attenzione** | **D** — la pianta e la sua soglia, l'unica cosa che si guarda con attenzione | **B** — i dipinti che obbligano a guardare davvero | era **da_costruire** fino al 03/10/2026, quando è risultato che il dominio non mancava: il gioco ci lavorava già in quattro posti (`quadro-trasversale.md` §1.3). Niente che si possa guardare di fretta |

L'ultima riga era `da_costruire`, ed era un difetto: il dominio `osservazione e attenzione` **esiste già** in quattro posti del progetto (`quadro-trasversale.md` §1.3, che porta le prove). La riga è chiusa dal 03/10/2026 e il dominio ha il suo premio: la pianta di una città vista dalla torre, cioè la categoria `D`.

### 2.1 Il premio della lingua dei segni: perché non può essere una persona

*(decisione di Pietro del 03/10/2026: «esistono 150 figure di sordi importanti? a prescindere, cambiamo premio».)*

**La risposta è no, e il numero la dice: non esistono centocinquanta figure sorde storiche documentabili.** Le fonti enciclopediche che il progetto usa nominano i pionieri — l'Abbé de l'Épée, Laurent Cler, e in Italia Lorenzo Mordini e chi ha scritto i primi manuali — cioè **poche decine**, non centocinquanta, e molte non hanno una fonte che regga la prova 1. La ragione non è la memoria delle persone: è che una lingua dei segni è stata per secoli **invisibile**, e le sue figure non sono state registrate dai documenti che il progetto può usare.

Con un premio per livello, la lingua dei segni dovrebbe avere **centocinquanta premi** (centocinquanta livelli, sei lingue per anno). Con poche decine di figure documentate, la prova 4 — **nessun duplicato** — sarebbe violata cinque volte per nome.

**Il premio cambia, e cambia in meglio.** È la **categoria K**: la scheda che il giocatore ha prodotto lui. Per ogni livello superato della lingua dei segni il giocatore riceve **una pagina del proprio quaderno**: il segno che quel livello ha insegnato, con la **frase che ha scritto lui**, e la data. Nessun premio del progetto è più suo di questo.

Tre ragioni, e la terza è quella che tiene:

1. **è l'unico premio che non si può copiare** — tutto il resto si trova su Wikimedia Commons, questo no;
2. **è il premio giusto per una lingua**: imparare la LIS non è guardare, è produrre. Un premio che ti fa produrre la lingua è l'unico che non sia un premio decorativo;
3. **non ha il problema della fonte**: le altre dieci categorie hanno tutte una fonte da dichiarare e una licenza da verificare, e questa ha solo il giocatore.

**Quello che resta aperto, e non è un premio**: la **forma del segno** nel quaderno. Il gioco non può disegnare la LIS — la `lingue.md` Q4 dichiara che una lingua dei segni non si scrive a tavolino, e un disegno fatto dal progetto sarebbe esattamente l'errore che quella domanda vieta. Quindi la scheda del quaderno porta **lo spazio** (un riquadro, una riga, la data) e **la riga di descrizione** che il livello fornisce, e **il segno lo mette il giocatore** — in un'altra parte del file, o a mano sulla pagina stampata. Va dichiarato che il gioco non sa disegnare la propria lingua dei segni: è il più grande limite che ha, ed è giusto che sia scritto.


### 2.2 I sei domini della sfida a mani nude, e che cosa possono avere come premio

| dominio | premio possibile | stato |
|---|---|---|
| `informatica` | **nessuno**, ma non perché l'informatica sia senza premio: **D**, come `osservazione e attenzione`, e i suoi centocinquanta premi sono nel catalogo (§4.0). Nella sfida a mani nude il premio è **la prestazione**, e nessuna delle sei discipline ne prende | dichiarato |
| `logica` | **nessuno**: non ha un oggetto proprio, e non è un premio che si possa guardare | dichiarato |
| `calcolo mentale e stime` | **nessuno**, per la stessa ragione | dichiarato |
| `linguistica e testo` | **E** e **F**: le due categorie che si leggono | possibile |
| `Costituzione e cittadinanza` | **I**, lo stesso premio di Diritto | possibile |
| `osservazione e attenzione` | **D** — la pianta e la sua soglia | chiuso |

Cinque dei sei domini **non prendono un premio nella tappa a mani nude**, e la ragione è la stessa per tutti e cinque: nella sfida si guarda, e un premio da guardare sarebbe un premio che la tappa rende inutile. Non è un difetto, è la differenza fra un gioco che premia e un gioco che premia **qualcosa**: un dominio senza premio nella tappa si dichiara come tale, e la tappa vale per la prestazione.

**Quello che non va confuso: un dominio senza premio nella tappa è una disciplina senza premi.** L'informatica ne ha **centocinquanta**, di categoria `D`: la riga dice «nessuno» per la **sfida**, non per il catalogo, e la ragione per cui la richiesta del 03/10 («tranne informatica») è stata superata il 04/10/2026. Un documento che dice «nessuno» in una tabella e poi conta centocinquanta record nello stesso documento non ha una svista: ha due verità che non si guardano, ed è il difetto che questa versione chiude.


## 3. Le quattro prove che un premio deve superare

Un premio entra nel catalogo solo se le passa tutte e quattro. Le prove sono corto, e ognuna ha una ragione.

| # | prova | perché serve |
|---|---|---|
| **1. Esiste, e si può vedere** | l'opera esiste, l'immagine è libera di diritti, e porta etichetta, autore e data | il progetto vieta le immagini generate e i volti inventati (`lingue-immagini.md` §1): un premio inventato insegna che esistono opere che non esistono |
| **2. Insegna il livello** | chi ha superato quel livello, guardando il premio, deve **riconoscere** in esso qualcosa di ciò che ha imparato | senza questa prova il premio è una decorazione, e la verifica non potrebbe mai dire che sia giusto |
| **3. Non è già nella storia** | l'opera non compare già nella storia della tappa, e non è già il pin o la stanza | se è già nella storia il premio non aggiunge niente: il ragazzo l'ha già visto e il premio diventa un ricordo |
| **4. Non è un duplicato** | due livelli diversi non hanno lo stesso premio | due premi uguali sono uno solo, e il secondo livello è stato trattato come se avesse qualcosa in più |

**Le prove sono quattro, e questo numero conta.** Il rimando al divieto girava in **quattro file** del progetto e puntava alla quinta prova, che questo documento non dichiara: le prove sono **quattro** e il divieto di generare è nella **prima** — *l'opra esiste, l'immagine è libera di diritti, e il progetto vieta le immagini generate*. I rimandi sono corretti. Il controllo **P8** legge le quattro righe della tabella e rifiuta ogni rimando a una prova che non c'è: è il difetto che `AGENTS.md` chiama *un numero vero che guarda il numero sbagliato*, e nessuno se n'era accorto perché una frase che punta a una prova inesistente si legge come le altre.

La prova 3 è quella che Pietro ha scritto lui, per il ferrarese, e vale per tutte le discipline: **il premio è la scoperta**. Per l'anno 1 la cosa è facile e per gli anni dopo è impossibile: le trenta figure di Ferrara sono già tutte nella storia, e i premi dell'anno 1 sono quindi architettura (`D`) e pittura (`B`), non persone.

## 4. La cardinalità, decisa: un premio per livello, e una salvadanaio

*(decisione di Pietro, 03/10/2026: «un livello compiuto per ogni premio: il giocatore lo mette in una sorta di salvadanaio».)*

La scelta è fra le tre di questa tabella, ed è la più pesante:

| variante | quanti premi | esito |
|---|---|---|
| **un premio per livello** | **1050** (vedi §4.0) | **scelta**: il livello ha la sua ricompensa, e la ricompensa ha un posto dove stare |
| un premio per voce | 180 | scartata: le stesse trenta voci attraversano cinque anni e non distinguono i livelli |
| un premio per anno e disciplina | circa 50 | scartata: il ragazzo riceve quarantacinque cose in cinque anni |

### 4.0 Il numero è esatto: 1050, non «circa 900»

Il «circa» era una dichiarazione di buco, non una cifra: `quadro-trasversale.md` non dichiarava quanti livelli aggiungessero i suoi quattro ambiti, e senza quel dato le tre varianti di cardinalità non erano confrontabili. Il dato è **zero**, e la ragione è nel testo dello stesso quadro: il trasversale **non aggiunge materie** (§0) e «compare solo dove si collega in modo naturale alla tappa e non è mai contenuto valutato». Un aggancio dentro un livello non è un livello.

Quindi il catalogo ha un numero solo:

| | quanti |
|---|---|
| livelli informatici | 150 (`schema-livelli.md`, uno per tappa) |
| livelli linguistici | 900 (sei lingue × trenta × cinque anni) |
| livelli dei quattro ambiti trasversali | **0**: sono agganci, e `quadro-trasversale.md` §1.3 lo dichiara per il quinto (osservazione e attenzione) che non ha neanche un programma |
| **totale dei livelli** | **1050** |
| **premi, con la variante scelta** | **1050**, meno quelli di discipline che non hanno un oggetto proprio (§2.2) |

Il numero dei premi è dunque **1050 e non 900**: la cifra che girava nel progetto contava i soli livelli linguistici e dimenticava i centocinquanta informatici, che hanno un premio anche loro. La correzione cambia la dimensione del catalogo di circa un sesto, ed è il motivo per cui il conto andava chiuso prima di scrivere `dati/premi.json`, che è **da produrre** e che senza questo numero sarebbe stato scritto corto di centocinquanta record.

### 4.1 La salvadanaio, e perché non è un'immagine

Il premio non viene mostrato e basta: **va in un registro che il giocatore possiede**, la salvadanaio, ed è uno dei cinque registri personali dell'inventario (`inventario.md` §3). Tre ragioni, e la terza è quella che conta:

1. **è il catalogo personale**: non «hai vinto 340 premi», ma «ecco i 340 oggetti che hai imparato», ognuno con le sue tre righe;
2. **è consultabile**: si apre quando si vuole, serve per il ripasso e serve per la consegna;
3. **non è un'immagine**: una salvadanaio con dentro le foto dei premi sarebbe un inventario di icone. **La salvadanaio contiene i premi, non le loro immagini**, e le immagini sono in `lingue-immagini.md`, ciascuna con la sua etichetta e la sua licenza.

### 4.2 Le tre righe che ogni premio porta

Ogni premio porta una scheda di **tre righe brevi**, nella lingua del gioco, e la terza è quella che rende il premio un premio:

| riga | che cosa contiene | esempio |
|---|---|---|
| **`chi`** | chi è, in una riga: nome, date, e perché è qui | «Ambedkar, 1891–1956, giurista: ha scritto la Costituzione dell'India» |
| **`cosa`** | che cosa ha fatto, e **quale fatto**, non generico | «ha scritto il rapporto sui diritti dei Dalit, che nel suo Paese erano legge» |
| **`riflessione`** | che cosa sarebbe diverso oggi, e perché è vero | «senza quel testo, la Costituzione indiana non avrebbe i diritti che ha» |

**La terza riga non è una formula, è una prova.** Il modello «se non ci fosse stato lui oggi non potremmo…» è la **forma**, e vale solo per i premi che sono persone. Per un oggetto — una pizza, un'epigrafe, un documento — la riflessione è della stessa sostanza e non della stessa frase: «senza questa lapide non sapremmo che quel nome esisteva». **Se la riflessione si può scrivere senza pensarci, il premio è decorativo** e non entra (`pedagogia.md` §1.2).

## 5. Cosa c'è da fare

1. ~~**Il numero dei livelli trasversali**~~ **chiusa il 03/10/2026**: sono **zero**, dichiarato in `quadro-trasversale.md` §1.3, e il conto dei livelli è **1050** (§4.0).
2. ~~**La variante scelta**~~ **chiusa il 03/10/2026**: un premio per livello, Pietro.
3. ~~**Il catalogo `dati/premi.json`**~~ **parzialmente chiuso il 05/10/2026**: il file esiste, con i **1050 record**, la **categoria riletta da §2** e — dalla v0.6 — **l'elemento interattivo e l'argomento del livello** (§5.1, §5.2), ma i campi che descrivono l'oggetto — `premio`, `fonte`, `licenza`, `perche_prova_2` — sono `null` con il perché in `vuoto`, e senza quei campi non è un catalogo di premi: è la parte che si può scrivere senza inventare niente. **Quello che resta non è un blocco di questo capitolo**: è la ricerca della fonte, e la sua prova più dura è la **3** (*non è già nella storia*), che per i centocinquanta premi dell'anno 1 è la ragione per cui sono architettura e pittura e non persone. Il campo `licenza` non è una delle quattro prove: è un dato del record, dichiarato in `vuoto` come gli altri tre.
4. ~~**La LIS**~~ **chiusa il 03/10/2026** (§2.1): il premio non è una persona ma la scheda che il giocatore produce, la categoria **K**. Quello che resta aperto non è il premio, è `lingue.md` Q4 — **la forma del segno nel quaderno**, che il gioco non può disegnare.
5. ~~**Il quinto dominio**~~ **chiusa il 03/10/2026**: `pedagogia.md` §3 e `premi.md` §2.2 lo davano per assente e non lo era — esisteva in quattro posti (`quadro-trasversale.md` §1.3) e ha preso il suo premio, la categoria `D`.

### 5.1 Che cosa c'è del catalogo, e che cosa manca

*(05/10/2026 — `dati/premi.json` e `sorgenti/premi_catalogo.py`, v2.)*

Il file ha **1050 record**, uno per livello: 1050 ÷ 7 = 150 informatici più 900 linguistici, il conto di §4.0. Ogni record porta `chiave`, `livello`, `lingua`, `disciplina`, `categoria`, `argomento`, `voce`, `elemento_numero`, `elemento_interattivo`, `argomento_del_livello` e `elemento_da`. **Nessuno di questi campi è scritto a mano**: la categoria è la colonna «primaria» della tabella di §2 riletta dal documento, e i tre campi dell'elemento vengono da `associazioni.json` e da `lingue.md` §6, come dice §5.2.

**Quello che non c'è, e perché è dichiarato.** I campi `premio`, `fonte`, `licenza` e `perche_prova_2` sono `null`, e `vuoto` dice perché: *la prova 1 vieta che un premio sia generato*. Un oggetto con una fonte inventata non è un premio, è un placeholder che ha superato le quattro prove senza averle fatte. Il file può quindi essere letto ma non usato come salvadanaio: dice **quanti** premi ci devono essere e **di che categoria** sono, non **che cosa** sono.

**Due difetti che il generatore ha trovato in sé stesso, prima di scrivere.**

- **Il livello informatico aveva il codice lingua `IT`**, che è anche la lingua italiana: due record con la chiave `1-1-IT`, e il conto diceva 1050 senza che nessuno guardasse le chiavi. Ora l'informatica ha `INFO` e l'italiano `IT`, e il generatore **si ferma** se due chiavi coincidono, prima di scrivere.
- **La sezione di `lingue.md` si cercava per posizione.** Le sei sezioni §6.1–§6.6 dicevano, nell'ordine, `cibi`, `detti popolari`, `superstizioni`, `musiche`, `artigianato tipico`, `bevande`, e il generatore leggeva la sesta sezione per il greco. Se un giorno l'ordine cambiasse — o se una lingua cambiasse oggetto senza che le righe si spostassero — gli argomenti di duecentocinquanta livelli sarebbero sbagliati e nessuno guarderebbe niente, perché il conto dei 150 per lingua tornerebbe lo stesso. Ora la sezione si trova **per l'oggetto di interazione che dichiara**, e il generatore si ferma se non ce n'è una. Il controllo fa il contrario: prende la sezione **per posizione** e verifica l'oggetto. Se i due non coincidono, i due controlli non possono sbagliare insieme.
- **Sei categorie su undici non hanno nessun livello**: `A`, `C`, `G`, `H`, `I`, `J`. Non è un catalogo incompleto: sono le primarie delle cinque discipline che il progetto dichiara **senza livelli propri** — §4.0 dice che i livelli trasversali sono **zero**. Il campo `categorie_senza_livelli` e il suo `perche` ci sono perché un conto che mostra cinque lettere su undici senza spiegazione sembra un buco.

### 5.2 Il legame col livello e coll'elemento interattivo

*(05/10/2026 — `dati/premi.json` v2, `sorgenti/premi_catalogo.py`, `sorgenti/verifica_premi.py` P6 e P7.)*

Il divieto della prova 1 non si aggira e non si nasconde: **`premio` resta `null`**. Ma un catalogo di millecinquanta record che porta solo una categoria e un `null` non dice niente del livello, e la richiesta è che i premi siano **coerenti con il livello e con gli elementi interattivi da cui provengono**. La coerenza si costruisce quindi sul **legame**, che è la cosa che il progetto conosce per davvero, e non sull'oggetto, che va cercato con una fonte.

Ogni record linguistico porta tre campi che vengono da due documenti, non da una scelta:

| campo | che cosa è | da dove viene |
|---|---|---|
| `elemento_interattivo` | la voce della lingua, quella con cui il giocatore interagisce a ogni tappa: `2-14-IT` → **la piadina** | `dati/lingue/associazioni.json`, la voce 14 delle trenta di cibi |
| `argomento_del_livello` | **l'argomento che quel livello insegna**: `2-14-IT` → *14. Discorso diretto e indiretto* | la cella 2-14 della tabella di `lingue.md` §6.1 |
| `elemento_numero` | il numero della voce, che è anche quello che la firma dell'emblema porta disegnato (§5.3) | la posizione della voce nella lista |

Il risultato è che la coerenza è **controllabile** e non dichiarata: `2-14-IT` non porta una piadina perché qualcuno ha deciso che sulla tappa 14 dell'italiano si può regalare una piadina, e la porta perché `lingue.md` dice che alla tappa 14 dell'italiano si parla di discorso diretto e indiretto e `associazioni.json` dice che la voce 14 dell'italiano è la piadina. **Cambiare uno dei due documenti cambia il catalogo, e i controlli se ne accorgono.**

**Le trenta voci sono dichiarate due volte, e i due file devono dire la stessa cosa.** `associazioni.json` le propone (di Pietro, `fonte_voci: proposta`), `immagini_oggetti.json` le elenca (`risultati[180]`): il generatore le confronta voce per voce e **si ferma** se una sola diverge, perché in quel caso non si sa quale delle due sia giusta. Il confronto dà **zero divergenze su centottanta**. Il controllo **P7** rifà la stessa verifica sul file scritto, e il generatore e il controllo non condividono il codice: se i due dessero lo stesso risultato per costruzione, il controllo non guarderebbe niente.

Una terza declinazione della stessa sigla è dichiarata perché è un numero che sembra sbagliato: i due file dicono **`SI`** per la lingua dei segni e il catalogo dice **`LIS`**. La mappa `{"SI": "LIS"}` è nel generatore e nel controllo, e i due la dichiarano per conto loro.

**L'informatica non ha elemento, e non se lo prende in prestito.** Le trenta voci sono delle lingue; i centocinquanta livelli informatici non hanno una voce fra le trenta. I loro tre campi sono `null` e `vuoto` lo dichiara: *l'argomento è quello del livello*. Un default che avesse riempito quei campi con una voce qualsiasi avrebbe fatto sembrare il catalogo completo e avrebbe insegnato al ragazzo che l'informatica è una lingua.

**Due numeri, calcolati e non scritti.** `elementi_riepilogo` dichiara `voci: 180`, `livelli_con_elemento: 180` e `usi_per_voce: [5]`: ogni voce è usata **cinque volte**, una per anno, perché le trenta voci attraversano i cinque anni e la tabella di `lingue.md` ha trenta righe per cinque colonne. Il generatore **si ferma** se le voci non sono 180 o se una tabella non dà 150 argomenti per lingua.

### 5.3 Gli emblemi: il simbolo della categoria, non l'oggetto

*(05/10/2026 — `sorgenti/art/emblema_premi.py`, `sorgenti/art/digiti.py`, v2.)*

Poiché l'oggetto non esiste, **non si disegna il premio**: si disegna il **suo simbolo**, cioè la categoria. Undici forme dichiarate una per categoria, in `emblema.segno()` accanto ai sette segni delle famiglie e non al posto loro: quelli dicono *perché qui non c'è il volto*, questi dicono *che cosa è l'oggetto*, e un dipinto e una legge non possono avere la stessa forma. Ogni forma porta il **perché sta con quella categoria**, nell'indice e in Q5.

La tessera è quella di `emblema.py`: bordo in inchiostro, segno della categoria in alto, **anno, numero della tappa su due cifre e sigla della lingua** al centro, firma di cinque caselle in basso.

**La firma porta il numero dell'elemento interattivo, non un hash.** Cinque caselle in base due stanno fino a 31 e gli elementi sono trenta, quindi il numero ci sta per intero: la tessera dice **da quale elemento interattivo viene** senza dirlo a lettere, e lo dice anche per l'informatica, che non ha una voce fra le trenta e per cui il numero è quello della tappa. `emblema.firma` — quella che prende l'hash del nome — resta per i ritratti delle persone, dove l'unica cosa da distinguere è il nome. La regola è scritta in **un posto solo**, `emblema_premi.numero_della_firma`, ed è il disegnatore e il controllo aimplementarla, non a copiarla. Le sigle sono dichiarate (`INFO`→`IN`, `IT`→`IT`, `FE`→`FE`, `LA`→`LA`, `EN`→`EN`, `LIS`→`SG`, `EL`→`EL`) e il generatore si ferma se due lingue ne prendono la stessa: le prime tre lettere non bastavano, perché `IT` e `INFO` cominciano per I, `LA` e `LIS` per L, `EN` ed `EL` per E.

**Un foglio solo: 1502×1962.** La misura e il numero di byte li stampa il controllo e vengono da `premi_indice.json`, non sono scritti qui: un dimensione scritta a mano nella prosa è un numero che invecchia. Millettocinquanta file da 48×54 sarebbero millettocinquanta richieste solo per pubblicarli, e il rate limit di GitHub non le fa passare. L'indice dice **dove sta ogni tessera** (`x`, `y`), così il motore estrae il pezzo che gli serve. È una scelta dichiarata, non un risparmio nascosto.

**Due difetti che Q3 ha visto al primo giro, e che il progetto aveva già imparato a cercare.**

- **Il font aveva solo le ventisei lettere.** `FONT.get("2", [])` restituisce una lista **vuota** e senza dire niente, e il numero della tappa semplicemente non veniva disegnato: `1-1-FE` e `1-2-FE` erano la stessa tessera. Le dieci cifre sono ora in `digiti.py`, con la stessa griglia cinque per sette delle lettere.
- **Il numero della tappa da solo non basta.** `1-2` e `2-2` hanno entrambi il numero 2. Con l'anno davanti e la tappa su due cifre, `1-2` dice «102SG» e `2-2` dice «202SG».

Il primo difetto è la terza volta in quattro giorni che si presenta: `AGENTS.md` dice *un carattere che il font non ha è un disegno che non c'è*, e `FONT.get` con un secondo argomento di default è esattamente il modo di non accorgersene.

### 5.4 I sette controlli degli emblemi, e i sette difetti

`sorgenti/art/verifica_premi_emblemi.py` fa **Q1** (le 1050 chiavi sono distinte e il numero è quello di §4.0), **Q2** (ogni tessera sta dentro il foglio e il foglio si decodifica con la misura dichiarata), **Q3** (le tessere sono **tutte distinte**, sha per sha), **Q4** (ogni categoria usata ha una forma dichiarata **che produce pixel**), **Q5** (ogni tessera dice perché quella forma), **Q6** (ogni tessera corrisponde a un premio, per chiave) e **Q7** (le cinque caselle portano il numero dell'elemento interattivo).

**Q7 è il controllo che guarda i pixel, ed è l'unico dei sette che lo fa.** Gli altri sei confrontano due file; Q7 rilegge la firma **dal foglio** e la confronta col catalogo. Se l'avesse chiesto all'indice, l'indice e il controllo avrebbero detto la stessa frase e il difetto del disegno sarebbe passato: è la parte indipendente che vale di più.

Q3 è il controllo che ha morso due volte, ed è quello che conta: trecento dei 1050 premi hanno la **stessa categoria** e quindi la stessa forma, e se la firma non rompesse le collisioni sarebbero centocinquanta file identici. I sette difetti iniettati sono **sette su sette visti**, verde prima e dopo — e la prova **rilegge il foglio dal disco** prima di dichiararsi a posto, perché chiedere alla griglia che essa stessa ha alterato significa chiedere a sé stessa.

### 5.5 Il quinto controllo non guardava, e non lo sapeva

`sorgenti/verifica_premi.py` faceva **P1** (le categorie sono A..K), **P2** (ogni disciplina ha una categoria primaria), **P3** (i sei domini della sfida a mani nude hanno ciascuno un premio o una dichiarazione di vuoto), **P4** (nessuna disciplina abbinata è inventata) e **P5** (nessun premio può essere un'opera generata o un'immagine senza licenza).

**P5 non guardava niente, e la prova è nel suo stesso codice.** Aveva un blocco `if …: pass` — un `if` che non fa niente, scritto come se lo facesse — e poi due frasi richieste al documento, una delle quali (`l'elenco è **chiuso**`) non esiste in nessuna parte di `premi.md`. Sopra tutto stampava una frase che il documento non diceva: «il campo licenza è fra le prove». La parola `licenza` **non compare in nessuna delle quattro righe** della tabella di §3. Il numero era giusto e la frase no: è la stessa forma del difetto della prova inesistente, e nessuno se n'era accorto perché un controllo che non può fallire e un controllo che non c'è fanno la stessa cosa sulla carta.

Riscritto, P5 guarda tre cose, e ognuna in un posto diverso:

1. **la sezione delle prove**, non tutto il documento: le tre frasi vietate non devono comparirci *come qualcosa che un premio può essere*. Il documento intero le contiene solo per spiegare perché non si possono usare, quindi il controllo di prima non poteva accorgersi di niente;
2. **che il divieto ci sia**: se dalla sezione delle prove sparisce la frase che dice che cosa vieta, è un difetto — un controllo che vieta senza dire che cosa vieta non vieta niente;
3. **tutti e 1050 i record**, non il primo: i quattro campi dell'oggetto devono essere `null` **e** dichiarati in `vuoto`. La versione di prima guardava `premi[0]` e dichiarava di guardare il catalogo; un oggetto inventato nel record numero quattro passava, e in un catalogo di millecinquanta record il primo è l'unico che non parla.

**P5 è diventato una funzione** e non un blocco dentro `main()`, ed è per questo che si può provare: i suoi due difetti — il divieto che sparisce dalle prove, e un oggetto inventato nel quarto record — sono **entrambi visti**, e la prova chiama la stessa funzione che il controllo chiama. Il primo difetto sta deliberatamente nel quarto record e non nel primo: un difetto che sta nel primo si vede anche per caso, e una prova che passa per caso non prova niente.

La stessa lezione vale per la **firma delle tessere** (§5.4, Q7): l'unico controllo che guardava i pixel era l'unico che poteva accorgersi di un difetto nel disegno, e gli altri sei confrontavano due file che avevano la stessa fonte.

## 6. Registro delle modifiche
- **v0.9 (07/10/2026)**: La salvadanaio è uno dei cinque registri personali: la collezione delle carte è il quinto (07/10/2026).

- **v0.8 (05/10/2026)**: **Il rimando è l'unica cosa che cambia.** Un documento collegato è salito di versione e questo rimando è rimasto indietro: la riga è sbagliata e non sembra, perché un rimando che cita una versione superiore a quella vera sembra un rimando fermo. Qui dentro non cambia nient'altro — e si scrive lo stesso, perché una riga che cambia è una riga che cambia.
- **v0.7 (05/10/2026)**: **il quinto controllo non guardava niente, e non lo sapeva.** `verifica_premi.py` aveva `if …: pass` — un `if` che non fa niente, scritto come se lo facesse — e richiedeva al documento una frase (`l'elenco è **chiuso**`) che non esiste in nessuna parte di `premi.md`. Poi stampava «il campo `licenza` è fra le prove», e la parola `licenza` **non compare in nessuna delle quattro righe** di §3: il numero era giusto e la frase no, che è la stessa forma del difetto della prova inesistente corretto ieri. Riscritto: guarda la **sezione delle prove** e non tutto il documento (le frasi vietate compaiono nel documento intero solo per spiegare perché non si possono usare, quindi il controllo non poteva mai accorgersi di niente), richiede che **il divieto ci sia**, e guarda **tutti e 1050 i record** invece di `premi[0]` — un oggetto inventato nel quarto passava, e in un catalogo di millecinquanta record il primo è l'unico che non parla. **P5 è diventato una funzione** e non un blocco dentro `main()`, ed è per questo che si può provare: i suoi due difetti sono **entrambi visti**, e il primo sta deliberatamente nel quarto record perché un difetto nel primo si vede anche per caso. Difetti di P5 ora **5/5**. Un **refuso in tre generatori**: `prem.md` invece di `premi.md`, quattro rimandi a un file che non esiste — lo stesso difetto del rimando alla prova inesistente, e per la stessa ragione non faceva rumore. Un `else: tessere = tessere` nel verificatore degli emblemi, cioè un `else` che diceva di non fare niente scrivendolo. La voce 3 di §5 si contraddiceva: diceva «parzialmente chiuso» e due frasi dopo «i due blocchi di §5 sono chiusi, quindi il catalogo si può scrivere», che è la risposta alla domanda che la voce stessa si era appena data.
- **v0.6 (05/10/2026)**: **i premi sono legati al livello, senza che l'oggetto smetta di mancare.** Il divieto della prova 1 resta e `premio` resta `null`: quello che si aggiunge è il **legame**, cioè la parte che il progetto conosce. Ogni record linguistico porta `elemento_interattivo`, `elemento_numero` e `argomento_del_livello`, letti da `associazioni.json` e da `lingue.md` §6, e `2-14-IT` porta la **piadina** con l'argomento **14. Discorso diretto e indiretto**. Le trenta voci sono dichiarate in due file e i due devono dire la stessa cosa: il generatore e il controllo **P7** li confrontano voce per voce, con zero divergenze su centottanta, e l'informatica non ha elemento perché non ne ha uno e `vuoto` lo dichiara. Nuovi **P6** e **P7**, sintesi **7/7**. La **firma delle tessere** non porta più l'hash del nome ma il **numero dell'elemento interattivo**: cinque caselle in base due e trenta elementi, il numero ci sta per intero. Nuovo **Q7**, che è l'unico controllo che **rilegge i pixel** del foglio invece di confrontare due file, con il difetto **F7** che altera il disegno tenendo indici e catalogo corretti: sette difetti, sette visti. **Un difetto in più, che nessuno dei due generatori aveva visto**: la sezione di `lingue.md` si cercava **per posizione**, e se l'ordine delle sei sezioni fosse cambiato gli argomenti di duecentocinquanta livelli sarebbero stati sbagliati senza che il conto dei 150 per lingua se ne accorgesse; ora la sezione si trova **per l'oggetto che dichiara** e il controllo fa il contrario. E un **rimando pendente**: quattro file del progetto rimandavano alla **quinta** prova, e le prove di §3 sono **quattro** — il divieto di generare è nella **prima**. I rimandi sono corretti e il controllo **P8** rifiuta da ora in poi ogni rimando a una prova che §3 non dichiara.
- **v0.5 (04/10/2026)**: **tre cose che il documento diceva e non era vero.** Il titolo prometteva **dieci categorie** e §1 ne aveva undici dalla v0.2. La **fonte del materiale** riportava la richiesta del 03/10 «tranne informatica», e `AGENTS.md` lo ripeteva — ma §4.0 contava **1050** premi, cioè **centocinquanta informatici**, e il catalogo li aveva scritti: due verità che nessuno metteva uno accanto all'altro. Pietro ha deciso il 04/10/2026 che **l'informatica ha un premio per tappa come le altre discipline**, quindi la richiesta è superata e il numero è **1050**. §2.2 resta *senza* premio per l'informatica, ma adesso la ragione è dichiarata: è la **sfida a mani nude**, dove il premio è la prestazione, e non l'assenza di premi nel catalogo. Con la stessa occasione due **forme mai guardate** sono state ridisegnate guardandole: `figura_su_piedistallo` chiedeva a `_quadrato` un rettangolo con il bordo superiore sotto quello inferiore, quindi la funzione non scriveva niente e la statua era **un obelisco**; `scudo` divideva l'altezza per mezzo riquadro, il contatore non superava mai 1 e la punta non si stringeva mai, quindi lo scudo era **un rettangolo**. Le undici forme hanno ora un foglio alla scala reale (`forme_prova.png`), perché sei di esse non hanno nessun livello e quindi nessuna tessera: senza il foglio sarebbero state disegnate e mai viste.
- **v0.4 (04/10/2026)**: **il catalogo e gli emblemi sono esistiti senza una riga di registro.** `dati/premi.json` ha **1050 record**, uno per livello, con la **categoria riletta** dalla tabella di §2 e i campi che descrivono l'oggetto dichiarati `null` con il perché (§5.1). Gli emblemi sono **1050 tessere in un foglio solo** di 1502×1962, con l'indice che dice dove sta ognuna (§5.2). Due difetti sono usciti guardando: **il font aveva solo le ventisei lettere** e `FONT.get("2", [])` restituiva il vuoto, quindi il numero della tappa non veniva disegnato e tessere di livelli diversi erano identiche; e **due categorie su cinque hanno la stessa forma**, quindi la firma di cinque caselle è quella che tiene le tessere distinte. Sei controlli **Q1–Q6**, sei difetti iniettati e **sei visti** (§5.3). Questa versione scrive quello che era successo: il registro era la parte che mancava, ed è la parte che nessuno legge e che invecchia più in fretta di tutte.
- **v0.3 (03/10/2026)**: **il numero dei premi è chiuso, ed era sbagliato di un sesto.** Aggiunto §4.0: i livelli dei quattro ambiti trasversali sono **zero** — il trasversale è un aggancio dentro i livelli, non un livello — quindi i livelli sono 150 informatici più 900 linguistici, cioè **1050**, e non i «circa 900» che il progetto portava da tre giorni. La cifra vecchia contava i soli livelli linguistici e dimenticava i centocinquanta informatici, che hanno un premio anche loro: è la ragione per cui il conto andava chiuso prima di scrivere `dati/premi.json`. Nello stesso giorno è chiusa la riga `osservazione e attenzione`: **non era un dominio da costruire, era un dominio che il progetto aveva già** in quattro posti (`quadro-trasversale.md` §1.3), e ha preso il suo premio — la categoria `D`, la pianta e la sua soglia. Le quattro cose da fare scendono a una: scrivere il catalogo.
- **v0.2 (03/10/2026)**: **le categorie sono diventate undici, e la undicesima è nata da una ricerca.** Pietro ha chiesto «esistono 150 figure sorde importanti? a prescindere, cambiamo premio». La risposta, con le fonti del progetto, è che **non**: le figure documentabili sono poche decine, e con un premio per livello la prova 4 — nessun duplicato — sarebbe stata violata cinque volte per nome. Il premio della lingua dei segni è quindi cambiato: è la **categoria K**, la scheda che il giocatore produce, l'unico premio che non si può copiare. Nello stesso giorno la cardinalità è decisa — **un premio per livello**, la salvadanaio dei quattro registri personali (`inventario.md` §3.1), e le **tre righe** che ogni premio porta: `chi`, `cosa`, `riflessione`. Quella versione non aveva la sua riga qui: il registro saltava dalla v0.1 alla v0.3 e nessuno se n'era accorto.
- **v0.1 (03/10/2026)**: prima stesione. Dieci categorie chiuse, undici discipline con la loro associazione e la colonna «da escludere», quattro prove di ammissione, tre varianti di cardinalità con i numeri accanto. Le tre cose che il documento dichiara e non risolve: **la cardinalità** (che è di Pietro), **il numero dei livelli trasversali** (che il progetto non ha) e **la LIS** (che non si scrive a tavolino). Una riga della tabella — `osservazione e attenzione` — è la stessa lacuna che `pedagogia.md` §3 aveva trovata nelle sei categorie della sfida a mani nude, e le due vanno chiuse insieme o non si chiudono.
