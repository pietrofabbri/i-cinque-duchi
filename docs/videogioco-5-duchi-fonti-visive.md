---
titolo: Videogioco "I cinque duchi" — le fonti visive: che cosa il gioco non ha ancora una veste, e dove si prende
versione: 0.17
data: 2026-10-05
autore: Pietro Fabbri (con Claude)
fonte: ricerca su Wikimedia Commons del 02/10/2026; tavolozza da Wikidata e Wikipedia del 03/10/2026; sagome e mura da OpenStreetMap via API standard OSM del 04/10/2026; cime e quote da Natural Earth `geography_regions_elevation_points` del 03/10/2026; verifica dei fondi già in dati/mappe/
documenti collegati: videogioco-5-duchi-ritratti.md (v0.5), videogioco-5-duchi-lingue-immagini.md (v0.3), videogioco-5-duchi-percorsi.md (v0.5), videogioco-5-duchi-mappe.md (v1.3), videogioco-5-duchi-luoghi-edifici.md (v0.4), videogioco-5-duchi-audit.md (v0.23), videogioco-5-duchi-tappa-1-01.md (v0.4), AGENTS.md
dati: dati/fonti_visive/fonti_visive.json (v1, 32 voci, 130 candidati), dati/fonti_visive/attestazione.json (v1, vuoto), dati/fonti_visive/incidenti.json (v1, 3 voci, 6 candidati), dati/fonti_visive/tavolozza.json (v1, 18 voci), dati/edifici_footprint.json (v1, 7322 edifici su 203 aree), dati/ferrara_fondo.json (v1, 14 tratti di mura), dati/ambienti_livelli.json (v2, 150 ambienti), dati/fonti_visive/colori_cartografici.json (v1, 19 voci), dati/altitudine_manifest.json (v1, tre file di cime: 15, 2 e 26 punti)
---

# Le fonti visive

## 0. Che cosa chiede questo documento

Il gioco ha delle immagini per i **personaggi** (213 schede, 138 ritratti autentici) e per gli **oggetti linguistici** (180 voci, 1120 candidati). Ha i **fondi geografici** (19 file Natural Earth). Il 2 ottobre non aveva altro, e non le aveva mai contate.

Questo documento fa quattro cose: **fa l'inventario** di che cosa ha e che cosa non ha una veste grafica; **cerca le fonti** per ciò che manca, con una ricerca vera su Wikimedia Commons; **costruisce** le derivazioni che erano solo un buco dichiarato — la tavolozza, i colori delle carte, le sagome degli edifici, il fondo di Ferrara, gli ambienti dei centocinquanta livelli e le cime con la loro quota, e poi i **mezzi**, le **epigrafi** e gli **incidenti**, che erano i due buchi rimasti; e **giudica l'accuratezza** di tutto questo su tre cose che il progetto chiama *proporzioni, colori, forme*, perché un'immagine «giusta» che viene stirata o scurita mente quanto un'immagine sbagliata.

**Che cosa non è questo documento.** Non sceglie le fonti dei **130 candidati**: sono proposte, e nessuna è stata guardata a vista. Il file `dati/fonti_visive/attestazione.json` è pronto e vuoto, con tutti i campi dichiarati. E non disegna niente: i sei file che ha prodotto sono **dati**, non grafica, e ognuno dichiara la propria fonte e i propri vuoti.

---

## 1. L'inventario: che cosa ha una veste e che cosa no

| Cosa | Stato | Fonte | File nel progetto |
|---|---|---|---|
| **Ritratti dei personaggi** | fatto, 138 su 213, e i restanti 60 hanno un **emblema disegnato** | Commons, con attestazione | `sorgenti/art/out/` (198 PNG a 48×54, uno per persona, più 11 sprite della tappa 1-1 che non sono ritratti: **209 in tutto**) |
| **Immagini degli oggetti linguistici** | proposte, 1120 candidati | Commons | `dati/lingue/immagini_oggetti.json` |
| **Fondi geografici** | fatto, 19 file **di Natural Earth** (la cartella ne ha 25: `dati/mappe_manifest.json`) | **Natural Earth**, pubblico dominio | `dati/mappe/` (1,5 MB) |
| **Unità amministrative del mondo** | fatto, 50 unità | **Natural Earth 10m**, pubblico dominio | `dati/mappe/mondo_admin1.json` |
| **Terreno e rilievo** | fatto per 95 luoghi | **Terrarium/SRTM** | `dati/luoghi_gioco.json`, campo `terreno` |
| **Tavolozza dei colori** | **fatto il 03/10/2026**, 18 voci | Wikidata e Wikipedia | `dati/fonti_visive/tavolozza.json` |
| **Sagome degli edifici** | **rifatto il 04/10/2026**, 7322 edifici su 203 aree | OpenStreetMap, **ODbL** | `dati/edifici_footprint.json` |
| **Fondo di Ferrara** (anno 1) | **fatto il 03/10/2026**, 14 tratti di mura | OpenStreetMap, **ODbL** | `dati/ferrara_fondo.json` |
| **Ambienti dei 150 livelli** | **fatto il 03/10/2026**, 150 su 150 | i documenti del progetto più i tre file sopra | `dati/ambienti_livelli.json` |
| **Colori dei fondi geografici** | **fatto il 03/10/2026**, 19 voci | una scelta dichiarata, non un colore a occhio nel codice | `dati/fonti_visive/colori_cartografici.json` |
| **Cime e quote** | **fatto il 03/10/2026**, 15 + 2 + 26 punti | **Natural Earth**, pubblico dominio | `dati/mappe/mondo_110_altitudine.json` e gli altri due |
| **Mezzi di trasporto** | **fatto il 05/10/2026**: 21 mezzi, 6 con immagine proposta, 10 storici con il vuoto dichiarato e 5 fantastici con il segno | Commons, con scelta sui metadati | `dati/fonti_visive/mezzi.json` |
| **Epigrafi e iscrizioni** | **fatto il 05/10/2026 come dato**: 3 immagini scelte e **zero** testi, con la fonte dichiarata e il divieto di entrare senza testo | Commons per l'immagine, **EDH** per il testo che non è arrivato | `dati/fonti_visive/epigrafi.json` |
| **Incidenti** | **fatto il 05/10/2026 come dato**: 3 voci, una immagine, una col testo al posto e **una che il gioco non usa**, dichiarata con la scansione che lo dimostra | Commons per l'immagine, per il resto i documenti degli anni | `dati/fonti_visive/incidenti.json` |

**Cinque buchi il 2 ottobre, due il 3, e i due che restavano sono chiusi come dati il 5.** Erano cinque, ed erano cinque problemi diversi. Quattro sono chiusi: la **tavolozza**, le **sagome degli edifici**, il **fondo di Ferrara** e gli **ambienti dei centocinquanta livelli**. Restano due, ed è giusto che restino: i **mezzi di trasporto** servono al percorso del duca e sono un problema di *immagini*, non di geometrie; le **epigrafi** servono al latino e sono un problema di *testo*, non di grafica. Nessuna delle due era un buco che si potesse chiudere con uno script, e sono dichiarate in §7.

**Un sesto buco è stato chiuso lo stesso giorno, e non era un buco di immagini mancanti: era un colore che c'era già e stava nel posto sbagliato.** I colori delle carte geografici stavano scritti nel codice del disegnatore, dove nessuno li leggeva (§3.7); mentre li si cercavano è saltato fuori che un file che non aveva niente a che fare stava dentro `dati/mappe/` e faceva crashare il lettore delle mappe (§7, Q4).

**L'ordine in cui sono stati chiusi è quello giusto, ed è dichiarato perché l'ordine è una decisione.** Prima la tavolozza, che è più piccola e serve a tutto il resto; poi le sagome, che sono il buco più grosso; poi il fondo di Ferrara, che dipende dalle sagome; e infine gli ambienti, che non sono una fonte nuova ma l'assemblaggio dei tre precedenti sui centocinquanta livelli. Il quarto non era un quarto buco: era la domanda «e quindi, che cosa si disegna a ogni tappa?», e senza risponderla i primi tre restano tre tavole isolate.

---

## 2. I fondi geografici: che cosa hanno e che cosa manca loro

I **19 file** di `dati/mappe/` vengono da Natural Earth, **pubblico dominio**, in tre scale: 110m per il mondo, 50m per l'Europa, 10m per la penisola. Sono **19 su 25**: gli altri sei sono il file amministrativo del mondo, i tre file delle cime e i due rilievi del terreno, e **`dati/mappe_manifest.json`** dice di ognuno da dove viene — prima del 04/10 nessun file della cartella lo diceva, e per questo il numero dei file era un numero che quattro documenti avevano dato in quattro modi diversi. Non sono GeoJSON: sono un **formato a delta con quantizzazione**, e si leggono solo con `sorgenti/gis/mappe_lettore.py`.

Il conto reale, verificato sui file:

| Scala | File | Dimensione | Che cosa contiene |
|---|---|---|---|
| **Mondo 110m** | 5 file | 111 kB | terre, paesi, regioni, fiumi, laghi |
| **Europa 50m** | 7 file | 652 kB | terre, paesi, regioni, regioni amministrative (1 687 geometrie), 186 città, fiumi, laghi |
| **Penisola 10m** | 7 file | 701 kB | coste, paesi, regioni, regioni fisiche, 622 unità, 212 città, fiumi, laghi |

**I tre limiti che il documento delle mappe dichiara già, e che qui tornano — due risolti, uno ancora vero.**

1. ~~**Le sagome degli edifici non esistono come dato.**~~ **Risolto il 03/10/2026, rifatto il 04/10/2026 perché la geometria era falsa**: `dati/edifici_footprint.json`, 7322 sagome su 203 aree, ognuna con `forma`, `altezza_m` e `fonte_altezza` (`osm_height`, `osm_levels`, `assente`). Vengono da OpenStreetMap, autorizzata il 02/10/2026, e viaggiano con **ODbL**. §3.2.
2. **Le altezze non esistono come dato**: misurate nel 24% dei casi a Milano e nel 3% a Roma. Il progetto risponde con il **terreno** — quota, pendenza, esposizione, rilievo locale misurati su SRTM, con errore medio di 12,6 m su 14 punti noti. Sui 7322 edifici effettivamente presi, l'altezza c'è in 2005 casi (`osm_height`) e si ricava dai piani in altri 1932 (`osm_levels`): **3385 non hanno niente** e diventano un volume neutro dichiarato. §3.2.
3. ~~**Non c'è un file della città di Ferrara.**~~ **Risolto il 03/10/2026**: `dati/ferrara_fondo.json` ha il perimetro delle mura ricostuito da 14 tratti OSM, 8601 m di perimetro e 4,20 km² di area interna, con tutte le 28 tappe 3. ~~**Non c'è un file della città di Ferrara.**~~ **Risolto il 03/10/2026**: `dati/ferrara_fondo.json` ha il perimetro delle mura ricostruito da 14 tratti OSM, 8601 m di perimetro e 4,20 km² di area interna, con tutte le 28 tappe dell'anno 1 che ci cadono dentro. §3.5.

**Il punto 2 resta il punto aperto, ma il 03/10/2026 è stato costruito un file che va nella stessa direzione e va detto con le sue parole.** `dati/mappe/mondo_110_altitudine.json`, `europa_50_altitudine.json` e `penisola_10_altitudine.json` portano le **cime** di Natural Earth con la loro quota: 15, 2 e 26 punti. Sono cime, non luoghi di gioco, e il file lo dichiara: nessun motore può dedurre la quota di una tappa da un elenco di cime. Ma il punto 2 chiedeva se il gioco ha un dato di quota, e adesso l'ha per il primo volta — per il sottosuolo, non per i luoghi.

**Il formato a delta ha una conseguenza visiva che va detta.** La quantizzazione conserva la forma ma perde la continuità della costa: a 110m il mondo è un'approssimazione onesta, ma un giocatore che guarda l'Italia e un che guarda la Spagna vedono coste con la stessa spessore di errore. La regola che ne segue è che **la scala dichiarata va sulla mappa**, così il giocatore sa che cosa sta guardando: 110m per il mondo è una mappa da navigazione, non una carta topografica.

---

## 3. Le fonti cercate, e i file costruiti

La ricerca (`sorgenti/fonti_visive_cerca.py`) ha esaminato **32 voci** in cinque categorie, con termini scelti uno per uno e non tradotti alla cieca. Ha prodotto **130 candidati con licenza libera**. **Delle cinque categorie cercate, tutte e cinque hanno un file di dati**, e sono le cinque righe dell'ultima colonna della tabella: i **mezzi** (§3.1), le **sagome degli edifici** (§3.2), le **epigrafi** (§3.3), gli **incidenti** (§6) e la **tavolozza** (§3.4). Le tre che il 3 ottobre erano ancora senza file — i mezzi, le epigrafi e gli incidenti — le hanno avuti il 5, e ognuno con la sua forma dichiarata dentro.

Fuori dalle categorie della ricerca, i capitoli hanno costruito il resto: il **fondo di Ferrara** (§3.5), gli **ambienti dei centocinquanta livelli** (§3.6), i **colori delle carte** (§3.7) e le **cime con la loro quota** (§3.8) il 3 ottobre; le **sagome dei premi** (§3.10) e i primi **disegni degli ambienti** (§3.9) il 4; **tutti e centocinquanta i disegni** il 5. Di questi prodotti **qui non c'è un numero**, e non per reticenza: un numero che si conta a mano e che nessuno ricalcola è un numero che invecchia, ed è la ragione per cui il titolo di questa sezione ha smesso di dire «gli otto file» mentre la frase due righe sotto diceva «sono sei». Il numero di ciò che è stato costruito è **il numero dei capitoli**, e quello si vede dalla tavola dei contenuti.

| Categoria | Voci | Candidati | Voci senza immagine | File di dati |
|---|---|---|---|---|
| **mezzo** | 16 | 46 | nessuna | `dati/fonti_visive/mezzi.json` |
| **edificio** | 6 | 36 | nessuna | `dati/edifici_footprint.json` |
| **epigrafe** | 3 | 18 | nessuna | `dati/fonti_visive/epigrafi.json` |
| **incidente** | 3 | 6 | **una** (`carestia`), e non è un vuoto: è una voce che nessuna tappa nomina | `dati/fonti_visive/incidenti.json` |
| **colore** | 4 | 24 | nessuna | `dati/fonti_visive/tavolozza.json` |
| **Totale** | **32** | **130** | **una** | ognuna con il suo |

### 3.1 I mezzi di trasporto: il file è costruito il 05/10/2026, e i vuoti sono dieci su sedici

**Il buco era più grande di quanto il documento dicesse, e la riga che lo dichiarava era quella giusta a metà.** La ricerca del 2 ottobre aveva coperto **undici** mezzi e il capitolo li chiamava «undici mezzi»: era vero. Ma il gioco ne usa **ventuno**, e quei due numeri non erano mai stati confrontati. Dieci mezzi storici —crociera, moto, sci, elicottero, monopattino— **non sono mai stati cercati**, e nessuno se ne accorse, perché la tabella contava le voci cercate e non i mezzi del gioco. È la stessa malattia di un numero vero che guarda il numero sbagliato.

`sorgenti/mezzi_fonti.py` costruisce `dati/fonti_visive/mezzi.json`: **una riga per ogni mezzo che `percorsi_mezzi.py` sa usare**, cioè ventuno righe, e ogni riga è una delle tre forme che il progetto ammette — un'immagine, un vuoto con la sua ragione, o il segno di un mezzo fantastico.

| | |
|---|---|
| Mezzi del gioco | **21**: 16 storici e **5** fantastici (ippogrifo, drago, sirena, carro di delfini, carro di serpenti) |
| Con immagine proposta | **11**: mulo, galera, nave, carovana, diligenza, treno, crociera, aereo, moto, sci, monopattino |
| Storici **senza** immagine | **5**, e nessuno dei cinque per mancanza di ricerca: **sono stati cercati tutti e cinque** |
| Fantastici con segno dedicato | **5**, e nessuna immagine: sono creature |
| Candidati esaminati | **46**, tutti quelli della ricerca del 02/10 più i cinque del 05/10 |

**Le sei immagini, con l'attribuzione calcolata e la riserva dichiarata quando c'è.**

| Mezzo | Immagine | Autore, anno | La riserva, che è la parte difficile |
|---|---|---|---|
| mulo | la mulattiera del **San Gottardo** di Peter Birmann | Peter Birmann, 1805 | è del 1805 e non del Quattrocento, ma dice «bestia da soma delle vie postali» meglio di qualunque altra |
| galera | la **galera del Provveditore d'Armata** | autore non dichiarato, 1700 | 735×516 px: la più piccola del lotto, e l'autore non c'è |
| nave | i **carricchi portoghesi** di Patinir | autore non dichiarato, 1540 | il gioco descrive un veliero latino e questo è portoghese: la somiglianza è dichiarata |
| carovana | la **carovana del sale** dell'Adrar | autore non dichiarato, 1965 | **una fotografia del 1965**, non un dipinto: e il gioco non promette immagini d'epoca per la carovana |
| diligenza | la **diligenza di Tarascon** di Van Gogh | Vincent van Gogh, 1888 | fra i candidati c'era anche la stampa di Abel Hold, che si è deciso di non usare |
| treno | la **ferrovia marmifera di Carrara** del 1890 | L'Eco del Carrione, 1890 | 641×393 px: può stare solo come icona |
| **crociera** | la **Queen Elizabeth** del 1940 | Cunard White Star Line, anni Quaranta | **una cartolina**, non una fotografia: la pagina lo dichiara |
| **aereo** | la **Constellation della TWA** in volo | NACA, **senza data** | la pagina dichiara «Unknown date» e il file porta «senza data» invece di un anno inventato |
| **moto** | una **Honda Cub del 1953** | DrReload, 2016 | la foto è del 2016 e il mezzo del 1953: la data dichiarata è quella della foto |
| **sci** | uno **slalom diagonale del 1955** | Fyyfabian, 1955-04-01 | il nome contiene una vocale scandinava e resta com'è |
| **monopattino** | una **Vespa 125 del 1953** | Peprovira, 2016 | della stessa coppia di fotografie ne esiste un'altra, scelta dichiarata |

**I cinque vuoti, uno per mezzo e con la ragione.** Sono quelli che la ricerca **ha cercato e ha respinto**, e la ragione è diversa per ciascuno.

| Mezzo | Che cosa è stato cercato e perché è stato respinto |
|---|---|
| **a piedi** | un sentiero di pellegrini di oggi e un conchiglio: nessuno dei due è «un uomo solo, con la bisaccia» |
| **cavallo** | tre dei quattro candidati sono la Cappella dei Magi, che è un corteo di trecento persone, e il quarto è una batteria d'artiglieria: nessuno dei quattro è un cavallo |
| **carrozza** | la carrozza americana del 1922 e tre guide turistiche: nessuna carrozza di corte |
| **pipa** | l'unico candidato è **il rospo del genere *Pipa***: la parola che si cerca è la pianta, e il termine con le due parole che non si confondono ha dato solo cataloghi botanici e un erbario del 1901 |
| **elicottero** | un Bell 47 a **455×319** e una squadriglia di elicotteri a **1109×785**: il gioco non mostra mezzi a due cifre di lato, e un'immagine che il motore deve ingrandire di sei volte è un'immagine rotta |

**I cinque fantastici non hanno immagine e non la devono avere.** Ippogrifo, drago, sirena e i due carri sono creature del *Furioso*: la regola dei luoghi fantastici in `AGENTS.md` dice già che vanno disegnati a mano sulla carta del gioco con un segno dedicato. Il file porta quel segno in un campo suo, e il controllo vieta che un mezzo fantastico abbia un'immagine — perché la prima volta che si troverà un drago dipinto del Quattrocento, la tentazione sarà di metterlo, e sarà sbagliata in un modo che nessun numero registra.

**La scelta è sui metadati, non a vista, e il file lo dichiara.** L'agente non può vedere un'immagine, e il progetto vieta che una scelta sia inventata: qui ogni scelta porta **il motivo per cui quel candidato corrisponde a ciò che `percorsi_mezzi.py` descrive**, e resta una proposta finché Pietro non la guarda. È la stessa regola dei 180 oggetti linguistici, e la stessa attesa a vista.

### 3.2 Le sagome degli edifici: costruite il 03/10/2026

La fonte è **OpenStreetMap**, autorizzata il 02/10, con ODbL e l'attribuzione «© OpenStreetMap contributors». La ricerca del 02/10 aveva trovato 36 fotografie di edifici italiani — il Duomo di Ferrara, il Castello Estense, Palazzo Schifanoia, San Stefano — ma quelle sono **foto, non sagome**: servono al documentario, non al disegno. La sagoma che il motore disegna è un'altra cosa, ed è **un estratto dei building di OSM per i 54 luoghi che hanno coordinate**, in formato delta come le mappe.

`dati/edifici_footprint.json` è di **2.75 MB** e contiene **7322 edifici su 203 aree interrogate**. Le aree non sono più solo le città del registro: sono i **centocinquanta pin dei livelli** più le 188 città, perché i pin del registro sono città intere e i ventotto punti dell'anno 1 stanno fra 204 e 1422 metri dal pin di Ferrara — a chiedere solo le città il file diceva «Ferrara ha centoquattro edifici» e le tappe non ne avevano nessuno.

| | |
|---|---|
| Aree interrogate | **203**: i pin dei livelli più 188 luoghi del registro |
| Edifici tenuti | **7322** |
| Edifici agganciati a un livello | **2632 record su 134 livelli distinti** |
| Edifici agganciati a un luogo | **4690 record** |
| Aree senza edificio, dichiarate | **15**, ognuna con il suo stato in `luoghi_senza_edifici` |
| Altezza misurata (`osm_height`) | **2005** |
| Altezza dai piani (`osm_levels` × 3,2 m/piano) | **1932**, che è una stima dichiarata e non una misura |
| Senza altezza: **volume neutro dichiarato** | **3385** |
| Ingombro reale delle sagome | minimo **1.2 m²**, mediano **247 m²**, massimo **35141 m²** |

**Edifici scartati, e ogni scarto ha un motivo dichiarato:** 14 anello_troppo_corto, 1788 anonimo_e_piccolo, 2 forma_perdita_nell_arrotondamento, 23 fuori_raggio, 9193 oltre_tetto_area, 1 semplificato_troppo, 84 troppo_piccolo_per_disegnare.

**Il difetto che è costato più caro, e che nessuno vedeva.** La prima versione del file scriveva la forma con `round(x / Q)` invece di `round(x * Q)`: divideva per cento un numero che era già in metri, e ogni vertice finiva a zero. Il file dichiarava **5209 sagome** e quei 5209 erano veri — erano 5209 edifici, con nome, altezza e fonte. Ma la **geometria era un punto**: l'ingombro più grande in tutto il file misurava cinque centimetri quadrati, la superficie di una monetina. Un conteggio vero e una forma falsa nello stesso file, e la cosa più insidiosa che ci fosse, perché il numero è la parte che un umano guarda.

**Due difetti minori sulla stessa riga, trovati solo dopo che la forma c'era.** La semplificazione a tolleranza fissa cancellava gli edifici piccoli: un'area di due metri con una tolleranza di un metro e mezzo si riduceva a un quarto della sua area reale, e la forma e il `area_m2` del record dicevano due cose diverse. Ora la tolleranza non scende sotto un ventesimo della dimensione maggiore dell'anello. E il confronto della perdita era fatto contro l'area della figura *semplificata* invece che contro quella *dichiarata*: misurava la perdita della quantizzazione contro la perdita della semplificazione, e le due si coprivano a vicenda.

E due difetti di interrogazione, che vengono prima. **Le tre istanze di Overpass rispondono 504**, e la correzione è stata cambiare fonte e non aspettare: ora si interroga l'**API standard OSM** (`api/0.6/map?bbox=`) attraverso `scarica_osm.py`, che restituisce lo **stesso formato** di Overpass perché a valle non cambiasse niente. Il prezzo dichiarato è una richiesta per pin invece di una per gruppo: ogni risposta è completa o assente e il file dice quale, mentre prima una richiesta si spezzava a metà senza che nessuno lo sapesse. E `id` arrivava come stringa dallo XML dove Overpass dava un intero: un `TypeError` alla prima tappa, che è il tipo di difetto che si vede subito e quindi non è pericoloso.

**Perché i controlli ci sono, e che cosa hanno morso.** `verifica_sagome.py` fa tre controlli: **S1**, ogni forma racchiude la stessa area che il record dichiara, entro un fattore due per lato; **S2**, nessuna sagoma degenere sotto il metro quadro di ingombro; **S3**, `fonte_altezza` è una delle tre dichiarate e «assente» non porta metri. Sul file rotto S1 e S2 trovavano **5209 problemi su 5209** e l'ingombro massimo era **0,0 m²**: il controllo vedeva esattamente il difetto che nessuno vedeva. Sul file rigenerato dà **0**.

**Le quattro regole, tutte dichiarate nel file, perché un buco travestito da geometria è il peggiore dei difetti.**

1. **Due raggi, e non uno, perché un luogo e un livello non sono la stessa cosa.** Un **luogo** del registro è una città intera: si guarda entro 250 m, che è `raggio_m`, e si tiene fino a 140 edifici. Un **livello** è una zona percorribile di ottanta metri per sessanta al massimo, e per farlo il raggio non è scritto ma **calcolato dalla diagonale della griglia più un margine di 20 m**: va da 51 metri di una porta a 121 di un paesaggio, e il tetto è 40. Chiedere 250 metri a tutte voleva dire portare in giro tre quarti degli edifici fuori dalla zona: dati veri che il motore non può mostrare, che è la stessa cosa di nessun dato, solo più pesante.
2. **Cosa è «significativo»**: ha un nome, ha un wikidata, ha un'altezza o dei piani, è di una categoria che il gioco sa nomincare, è patrimonio, oppure ha più di 120 m² di area. Un capannone senza nome e senza misure non viene disegnato come se fosse un palazzo.
3. **Il tetto è dichiarato e si vede nel conto**: i più grandi si tengono e gli altri si dichiarano come scarto. Oltre, il centro di Londra mangia il file per una sola tappa.
4. **Altezza assente non si stima.** L'edificio esce con `altezza_m: null` e `fonte_altezza: "assente"`, e il motore ne fa un **volume neutro**. È la stessa regola di §4.3 e la stessa dei 41 luoghi che non hanno coordinate perché non sono luoghi: *un volume che non sa niente si dichiara, non si indovina*.

**I due difetti del 3 ottobre, che il 4 sono diventati un altro.** Il primo giro interrogava Overpass in gruppi spezzati: con aree concatenate sulla stessa riga l'API risponde `HTTP 400: ';' expected - '(' found`, e con gruppi da sei c'è stato un `504`, per cui `overpass_spezzato()` dimezzava il gruppo e riprovava. Il secondo difetto era che **la prima versione del file aveva il conto sbagliato in un modo invisibile**: interrogare 54 luoghi in un colpo è più semplice e non finisce, e alla prima interruzione si perdeva tutto. Da qui il flag `--riprendi`.

Il 4 ottobre Overpass era saturo su tutte e tre le istanze, e la correzione è stata cambiare fonte invece di aspettare. Il terzo difetto **è stato scritto male e nessuno lo vide**, ed è quello descritto sopra: la quantizzazione. Il quarto è comparso solo quando le sagome hanno cominciato a essere vere — dieci edifici con l'altezza dichiarata ma di mezzo metro quadro, che il generatore teneva e che il verifica non poteva accettare. Nessuno dei due sarebbe stato trovato senza l'altro: la quantizzazione è invisibile finché le sagome sono tutte un punto, e i dieci edifici minuscoli sono invisibili finché le sagome sono vere.

### 3.3 Le epigrafi: il testo manca, e la fonte che lo tiene è chiusa a noi

**Un'epigrafe non è un'immagine: è un testo, e il testo è la parte che il gioco usa.** Le tre voci hanno **diciotto** immagini e **zero** testi, e la differenza è tutta qui: l'epigrafe è la domanda di ripasso (`ripassi.md` §2), è il premio **F** del latino e il **C** del greco (`premi.md` §2.1), ed è l'unica cosa che distingue un'epigrafe da una fotografia di un sasso. Senza testo l'epigrafe non è un premio: è un'illustrazione, e le illustrazioni le fa il progetto con le sue sagome.

`sorgenti/epigrafi_fonti.py` costruisce `dati/fonti_visive/epigrafi.json`: tre voci con l'immagine proposta e **il testo dichiarato mancante**, con la fonte da cui arriva. Il buco non è chiuso, e il file non finge: dice che **zero** epigrafi entrano nel gioco e perché.

| | |
|---|---|
| Voci | **3**: lapide, lastra, iscrizione |
| Candidati esaminati | **18**, tutti quelli della ricerca del 02/10, nessuno nuovo |
| Con immagine scelta | **3**, e tutte e tre senza testo |
| Con trascrizione e traduzione | **0** |
| Che entrano nel gioco | **0**, e nessuna può entrarci finché i due campi sono vuoti |

**Le tre fonti sono state interrogate il 5 ottobre e hanno tutte detto di no, in tre modi diversi.**

| Fonte | Che cosa le si chiede | Che cosa ha risposto |
|---|---|---|
| **Wikidata** | il testo dell'iscrizione | **63048** voci hanno la proprietà che rimanda alla scheda epigrafica, ma è un **identificatore numerico**, non il testo; e solo **15** hanno anche una traduzione |
| **Wikimedia Commons** | il testo nella pagina del file | il campo `inscriptions` del template è **vuoto**: l'immagine c'è, il testo no (verificato su tre file) |
| **EDH**, la fonte giusta | la trascrizione di 82 000 iscrizioni latine | **protezione anti-robot** a ogni richiesta, pagina e API, su due domini |

**Perché i campi sono `null` e non compilati.** Il progetto vieta che un testo sia scritto dal progetto: una trascrizione o una traduzione redatte qui sarebbero un testo generato, che è la stessa cosa che il progetto vieta per le immagini degli oggetti. Il file indica la fonte — **EDH**, con EDR ed EAGLE come alternative per italiano e greco — e il modo per recuperarla quando si lascia interrogare: **l'identificatore in Wikidata P1415**, che è il numero con cui EDH chiama l'iscrizione.

**La regola, che è la consegna vera di questa sezione**: un'epigrafe entra nel gioco **solo con la sua trascrizione e la sua traduzione**; `verifica_fonti_visive.py` lo vieta (`E2`), e oggi lo vieta a tutte e tre. Il che significa che i premi F del latino e C del greco restano senza immagine finché EDH non risponde — ed è un fatto dichiarato, non un lavandino.

**Le tre immagini scelte, e perché quella.** La **lapide** è la stele di Sosibia (Boston, 3460×5352 px), che è una persona nota e la forma che il gioco usa; la **lastra** è il rilievo funerario del Metropolitan più grande fra i sei simili che la ricerca ha portato; l'**iscrizione** è l'iscrizione cretese di Eleutherna che **proibisce l'eccesso di vino**, scelta perché è l'unica delle diciotto che promette un testo traducibile. Tutte e tre senza testo, e tutte e tre con la riserva scritta.

### 3.4 Il colore: la tavolozza, costruita il 03/10/2026

Quattro voci, ventiquattro candidati, e nessuna tavolozza. Il gioco aveva **tre sistemi di immagini che non concordavano fra loro**: i 213 ritratti, i 1120 candidati degli oggetti, e i fondi geografici. Senza una tavolozza, ogni immagine porta i suoi colori e la scena diventa un muro.

Le quattro voci cercano appunto i **campionari**: le terre d'oliva del paesaggio ferrarese, le tinte dei manoscritti miniati, i motivi dei tessili, i colori degli affreschi. Una tavolozza non si sceglie a occhio: si costruisce da una fonte e si dichiara.

`dati/fonti_visive/tavolozza.json` è **18 voci** e nasce da una scelta di principio, che è quella delle tre regole già prese su etichette e proporzioni: **non si ricolora tutto a una tavolozza unica, si dichiara il colore di ogni fonte**. Le 18 voci si dividono in tre gruppi, e il file dichiara quale dei tre sia:

| Provenienza | Voci | Che cosa è |
|---|---|---|
| `wikidata_p465` | **5** | l'esadecimale dichiarato da Wikidata per un pigmento storico |
| `wikipedia_infobox` | **5** | il campo «color» dell'infobox di un artista, cioè il colore che *quell'artista* usava |
| dichiarata a mano | **3** | terre, bianco calce e fondo di scena: non hanno un codice in nessuna fonte, e il gioco dichiara che sono una scelta |
| stato del gioco | **5** | verde rame, giallo, oro, inchiostro, e i tre colori di stato (ok, attenzione, errore): non sono pigmenti, sono **la grammatica del gioco** |

**I tre difetti che la costruzione ha trovato, e che sono la parte instructive del lavoro.**

1. **Il colore di un pigmento non si cerca per nome.** La ricerca su Wikidata per «vermilion» restituisce una **città della provincia di Alberta**; «red ochre» restituisce un **premio televisivo**; «minium» restituisce **un'alga**. I pigmenti hanno nomi che il motore di ricerca non distingue dagli omonimi. La correzione è che gli **identificatori Wikidata sono espliciti** nella fonte: `tavolozza_campioni.py` non cerca, dichiara.
2. **`P462` non è l'esadecimale: è un link a un oggetto «colore».** Il percorso giusto è a due tappe: pigmento → `P462` → oggetto colore → `P465` → esadecimale. E il valore di `P462` è un **dizionario** (`{"entity-type": "item", ...}`), non una stringa: senza controllarne il tipo finisce nel file come colore, e un dizionario non è un colore.
3. **Cinque pigmenti su quindici non hanno esadecimale da nessuna parte**: il bianco di piombo, l'azzurrite, la malachite, l'orpimento e il giallo di piombo e stagno. Non si è tirata fuori una terna di cifre plausibili: sono in `pigmenti_senza_colore_macchina` con la prova, e le voci ricostruite su altri pigmenti.

**Le due dichiarazioni che rendono il file onesto.** `senza_colore_dichiarato` è **vuoto**: nessuna voce ha un colore inventato. E `campioni_guardati` è **zero**, come i 130 candidati: i campionari non sono stati aperti, e il file non finge di averli guardati.

`dati/fonti_visive/tavolozza_candidati.json` porta, accanto alle 18 voci, le **altre dichiarazioni** trovate (per esempio il vermiglio è `E34234` su Wikidata e `FF4000` sull'infobox: due fonti che dicono cose diverse, entrambe vere, e la scelta va motivata) e le **famiglie di colori senza voce** (i tessili e gli affreschi): dichiarare che manca una voce è diverso dal non averci pensato.

`sorgenti/verifica_tavolozza.py` è il controllo: sei verifiche (A1–A6), con `--offline` per quando la rete non c'è. Eseguito **in rete il 03/10/2026**: 10 fonti ricontrollate, **0 problemi**.

### 3.5 Il fondo di Ferrara: costruito il 03/10/2026

`dati/ferrara_fondo.json` è il fondo cittadino dell'anno 1, e nasce da una domanda che sembrava di disegno e si è rivelata di misura: **che cosa è «dentro le mura»?**

La fonte sono i **14 tratti** che OpenStreetMap ha per `barrier=city_wall` intorno a Ferrara (ODbL, `(c) OpenStreetMap contributors`). OSM non ha l'anello delle mura: ha tratti, con dei vuoti. Il vuoto più grosco è di **1037 m** fra gli ultimi due estremi, e nessuna fonte lo disegna.

**La scelta non è stata fatta a occhio, e questo è il punto.** I tratti sono stati uniti a catena entro una tolleranza, e la tolleranza è stata scelta così: **si tiene la più piccola in cui tutte le tappe del primo anno cadono dentro**. La scala completa è nel file, e i cinque passi sono tutti dichiarati:

| Tolleranza | Vertici | Area interna | Tappe fuori |
|---|---|---|---|
| 5 m | 93 | 0,13 km² | 27 su 28 |
| 15 m | 51 | 0,24 km² | 28 su 28 |
| 25 m | 51 | 0,74 km² | 26 su 28 |
| 40 m | 51 | 1,44 km² | 19 su 28 |
| **60 m** | **54** | **4,20 km²** | **0** |

Il risultato: perimetro **8601 m**, area interna **4,20 km²** contro i 4,8 km² storici, e **28 tappe su 28 dentro**, zero sul bordo, zero fuori. Le due tappe che non hanno coordinate (1-27 e 1-30) sono dichiarate fuori dal controllo: non si possono verificare, e il file non finge che siano dentro.

**Una fonte è stata rifiutata, ed è la più interessante.** OSM ha una relation che si chiama `3875619 «Centro storico»`, sembra fatta apposta e copre 1,34 km². Ma **13 tappe su 28 stanno fuori**, fra cui Piazza Ariostea, Palazzo dei Diamanti e Porta degli Angeli: un perimetro che esclude la piazza dei Diamanti non è il perimetro delle mura, per quanto sia chiamato centro storico. Il nome giusto è la fonte sbagliata, ed è registrata in `fonti_rifiutate` con la prova.

**Un difetto che la scala delle tolleranze ha nascosto, e che va dichiarato.** La prima versione del controllo di «dentro» lavorava in gradi con un raggio di 0,5 — cioè **55 km**: ogni tappa risultava «sul bordo», e la scala delle tolleranze non discriminava niente. Il calcolo di distanza su sferoide è stato corretto, e la tabella qui sopra è quella vera.

Il file dichiara anche i suoi tre limiti: nessun tratto porta `start_date`, quindi **il file non sa quando ogni tratto di mura è stato costruito e non lo deduce**; le mura di origine e quelle dell'Addizione Erculea non sono distinguibili, e il quinto anno lavora sulla stessa area; e la zona percorribile è l'interno delle mura più un margine di 60 m oltre la linea, oltre il quale c'è la nebbia.

### 3.6 Gli ambienti dei centocinquanta livelli: costruiti il 03/10/2026

Il quarto file non è una fonte nuova: è la risposta alla domanda che i primi tre lasciavano senza risposta. **`dati/ambienti_livelli.json` è un ambiente per ognuno dei 150 livelli, 150 su 150**, nell'ordine 1-1, 1-2, … 5-30, ed è costruito sul modello dell'unica zona già esistita: la piazza della Cattedrale di `videogioco-5-duchi-tappa-1-01.md` §3.

Un ambiente porta: il livello, l'argomento, la voce (il personaggio), il luogo, le coordinate, il **tipo** di ambiente con la sua griglia, le sagome che ci sono, il fondo (solo per l'anno 1), la paletta, l'orientamento e — se non si sa — i suoi **vuoti dichiarati**.

**Come sono costruiti, e perché da tre fonti diverse.** L'anno 1 prende le coordinate da `anno1-mappa.md` §3, che le ha già verificate sui numeri civici del Comune; gli anni 2-5 prendono il luogo da `dati/luoghi_gioco.json`, campo `tappe`, che collega livello e luogo **per relazione esplicita e non per confronto di nomi**: confrontare nomi è la tecnica che ha fatto cadere Karakorum sulla catena montuosa, e qui non si rifà.

| | |
|---|---|
| Ambienti | **150** su 150 attesi, nessuno mancante |
| Con coordinate | **100** |
| Con sagome OSM | **134** |
| Già costruiti (quelli che il motore ha disegnato) | **1**, la tappa 1-1 |
| Sprite dichiarati | **11**, tutti della tappa 1-1 |

I **nove tipi** di ambiente e quante volte compare ciascuno: `citta` 65, `edificio` 32, `citta_antica` 12, `percorso` 10, `situazione` 11, `paesaggio` 7, `porta` 5, `area` 5, `piazza` 3.

**Il tipo non è indovinato in silenzio.** Ogni ambiente dichiara in `tipo_da` da dove viene il suo tipo: dal campo `tipo` del registro dei luoghi quando c'è, e da una **parola chiave** quando non c'è (`cattedrale` → edificio, `piazza` → piazza). Le griglie — colonne, righe, metri per tessera, nove tabelle diverse — sono una **scelta di progetto, non un dato di una fonte**, e stanno tutte nel file perché il motore le legga e nessuno le riscriva nel codice.

**I vuoti sono tutti dichiarati, uno per uno**, e sono la parte più utile del file: `orientamento_non_dichiarato` **150** (**nessuno** dei centocinquanta ha un orientamento dichiarato, e dichiararlo vuol dire che il motore non deve sceglierlo da solo), `senza_sagome_osm` **16**, `coordinate_non_e_un_luogo` **23**, `coordinate_da_geocodificare_a_mano` **14**, `coordinate_da_geocodificare_wfs` **11**, `sole_sagome_senza_altezza` **29**, `senza_coordinate` **2**, `nessun_luogo_dichiarato` **2**. E i due vuoti degli sprite: `sprite_da_disegnare` **149** (tutti gli ambienti tranne la 1-1) e `sprite_nessun_codice_li_produce` **1** (la 1-1 ha i suoi undici file, ma sono un disegno del primo prototipo e nessun codice li rifà).

**Gli sprite della tappa 1-1: undici file che nessuno dichiarava.** Nella stessa cartella dei ritratti, `sorgenti/art/out/`, la piazza della Cattedrale aveva la facciata (509 × 312 px), il cartello dell'art. 9, la lapide, due statue, il protagonista in quattro fotogrammi e tre ritratti disegnati a mano. Erano lì dal primo commit, e **nessun codice li caricava e nessun dato li nominava**: il controllo 2 di `art/verifica_immagini.py` li dichiarava file morti, e aveva ragione — un disegno che il motore non può usare non è un patrimonio, è un inganno. Ora sono la tabella `SPRITE` di `sorgenti/ambienti_livelli.py`: ogni riga dice la **voce** della tabella 3 di `tappa-1-01.md` da cui prende il posto, il file, che cosa ci si vede, e la **misura misurata sul PNG** (non scritta). I posti non sono copiati: sono riletti dal documento, e il controllo **B9** li rilettura a ogni verifica e li confronta, perché un manifesto si può editare a mano come qualunque altro file.

**La facciata è la prova che la scala è vera.** La riga «Scala» del documento dichiara «1 tessera = 1,25 m = 16 px» e «facciata larga 39,8 m (509 px)». I **12,8 px per metro** sono un quoziente e i 509 sono un prodotto: il controllo 10 di `verifica_immagini.py` moltiplica i due e pretende che il risultato sia proprio quei 509 e che `facciata.png` sia largo quanto. Se i due numeri del documento non tornassero fra loro, il difetto sarebbe nel documento — e si vedrebbe lì, prima che a schermo.

`sorgenti/verifica_ambienti.py` è il controllo: le verifiche da **B1** a **B9**, **tutte superate il 04/10/2026**. **B7** è nato con le ipotesi di coordinata e chiede a ogni ambiente di dire da quale dei due file prende il punto da disegnare. **B8** è nato da un difetto vero di questa sezione: i numeri qui sopra erano stati scritti a mano e avevano smesso di corrispondere al file — 99 coordinate dichiarate contro 100 reali, 69 sagome contro 68, `citta_antica` 11 contro 12 — senza che nessuna verifica lo vedesse, perché tutte le altre confrontano i dati fra loro e non i dati con quello che il documento scrive. B8 confronta ogni numero di questa sezione con il conto e li ha fatti tornare; le due frasi che il file scrive su se stesso (il numero delle ipotesi, la presenza di orientamenti) ora sono **calcolate** in `ambienti_livelli.py` e non più scritte a mano, che è l’unico perché non invecchino di nuovo. B9 è nato il 04/10/2026 dalla stessa malattia su un file diverso: i posti degli sprite stavano nel manifesto come dei numeri, presi dal documento una volta il 3 ottobre, senza che nessuno li rileggesse.

---

### 3.7 I colori delle carte: costruiti il 03/10/2026

I fondi di Natural Earth non hanno colori: sono geometrie, e il colore glielo decide il motore. La Q4 chiedeva se quei colori dovessero stare **in un file** o **nel codice**, e la risposta è stata un file: `dati/fonti_visive/colori_cartografici.json`, **19 voci**.

**Un colore entra in questo file in due modi, e solo due**, ed è la stessa regola della tavolozza applicata un passo oltre:

| Da dove | Voci | Che cosa dichiara la voce |
|---|---|---|
| dalla **tavolozza** | **3** (`lago`, `etichetta_mappa`, `fondo_gioco`) | la `chiave_tavolozza`, e il controllo ne confronta l'esadecimale **byte per byte** con `tavolozza.json` |
| **dichiarata qui** | **16** | il `motivo` (che cosa è) e il `criterio` (perché proprio questo colore) |

Non esiste un terzo modo, ed è il punto: **nessun colore entra perché stava già nel codice**, e nessuno entra per assomiglianza a un altro.

**La regola che le carte hanno e le immagini non hanno.** Ogni categoria che ha un riempimento ha anche un bordo, e i due si dichiarano insieme: una categoria con il riempimento e senza il bordo è un file che non sa come si disegna, e una con il bordo e senza il riempimento è una linea senza forma.

**Le tre categorie che non hanno un riempimento, e perché è una scelta.** Le **terre emerse** e le **regioni fisiche** si disegnano col solo bordo e lasciano trasparente il fondo della carta: riempirle nasconderebbe i Paesi che ci stanno sopra, e i deserti si distinguono dal Paese che li contiene non riempiendoli. Le **50 unità amministrative del mondo** non hanno un colore proprio e usano quelli di Stato, perché un'unità amministrativa è un Paese come un altro.

**I due colori che il file dichiara ma nessuno disegna, e perché sono dichiarati lo stesso.** `fondo_gioco` è il fondo della scena e non della pagina di verifica: la carta del gioco ci sta sopra e i due bianchi sporchi devono essere lo stesso, ma nessuna delle dodici pagine di verifica lo disegna. Il **colore della nebbia** invece **non è dichiarabile** e sta in `non_dichiarati`: sta nel prototipo generato, che in questo checkout non c'è, e dichiararlo sarebbe dichiarare un colore che nessuno ha potuto misurare.

**Il difetto vero che è saltato fuori cercandoli, e che non era di colori.** `dati/mondo_admin1_copertura.json` — il file che dichiara come le 50 unità amministrative sono state scelte fra le 4596 della fonte, con quale tolleranza e quali sette che hanno avuto bisogno di una riserva, e quali dei 54 pin ci cadono dentro — stava **dentro `dati/mappe/`**, dove vale la regola che ci stanno solo file nel formato a delta, perché `dati/mappe/` si legge solo con `mappe_lettore.py`. Un JSON valido in quella cartella faceva **crashare il lettore** con un `IndexError: list index out of range`, che è il peggiore dei sintomi: dice una lista troppo corta e non dice che il problema è un file che non aveva niente a che stare lì. Il file è stato spostato in `dati/` — dove è un dato e non una mappa — il lettore ora controlla la forma del file e solleva un `ValueError` che lo dice, e il controllo **C6** tiene la regola ferma.

### 3.8 Le cime e le loro quote: costruite il 03/10/2026

`dati/mappe/mondo_110_altitudine.json`, `europa_50_altitudine.json` e `penisola_10_altitudine.json` portano le **cime** di Natural Earth con la quota sul livello del mare. Sono **15, 2 e 26 punti**, in formato a delta come tutte le altre mappe, e `dati/altitudine_manifest.json` dichiara il conto della fonte accanto al conto del file: 19 punti in entrata e 15 nel file da 110 m, 86 e 2, 711 e 26.

**La scoperta che vale più dei tre file, e che nessuno dei numeri nasconde.** La fonte si chiama `geography_regions_elevation_points` ed è **mondiale in tutte e tre le scale**: la scala è il dettaglio, non l'estensione. Il file da 50 m elenca 86 cime su tutto il globo e solo due in Europa, da longitudine −167 a +160; quello da 10 m ne elenca 711 di cui 26 nel riquadro della penisola. Il manifest lo dichiara in `la_scala_e_l_estensione`, perché un file chiamato «europa» che contiene il Kilimangiaro è un file che mente una volta sola, e quella volta basta.

**E da qui segue la seconda scoperta, che è quella pericolosa: i tre file non sono annidati.** Nessuna delle 15 cime mondiali cade nel riquadro della penisola, e nessuna delle 26 cime della penisola è fra le 15 del mondo: sono **selezioni diverse della stessa fonte globale a dettagli diversi**, non tre risoluzioni dello stesso elenco. Un gioco che li trattasse come piu' e meno risoluzioni sbaglierebbe, e sbaglierebbe invisibilmente, perché tutti i numeri sono giusti.

**Quello che il file non è, dichiarato perché è la parte che si legge.** Non è un modello del terreno: fra due cime c'è solo il vuoto di questa fonte, e nessun motore può dedurre la quota di una tappa da queste cifre. Non è la quota di una città, e il campo `name` lo dice per ogni punto. E la quota è **quella che la fonte scrive**: l'Everest è a **8848 m**, che è il valore del 1954, mentre dal 2020 la quota ufficiale è 8848,86 m. Il file non corregge e non nasconde — è il caso di scuola del quinto anno, dove ogni numero porta con sé l'errore e la data in cui è stato misurato.

**Il lavoro tecnico che ha reso possibile tutto questo è una funzione.** `sorgenti/gis/shapefile_lettore.py` sapeva leggere **poligoni** (`parti()`) e non sapeva leggere un **punto**. La funzione nuova `punti()` legge le forme 1 (`Point`, con X e Y a offset 4) e 8 (`MultiPoint`, che ha un bounding box di 32 byte e il numero dei punti all'offset 36, coi punti che cominciano a 40): la trappola è che il MultiPoint ha *dentro* i punti una struttura che sembrava quella di un poligono, e leggerla con il codice dei poligoni dà coordinate che hanno l'aria di essere giuste.

---

### 3.9 I disegni degli ambienti: i trenta dell'anno 1 il 04/10/2026, tutti e centocinquanta il 05/10/2026

`dati/ambienti_livelli.json` e `dati/edifici_footprint.json` erano due tavole di numeri, e nessuno le guardava insieme. `sorgenti/art/disegna_ambienti.py` le guarda insieme e ne fa un'immagine per tappa: **150 disegni**, uno per tappa, in `sorgenti/art/out/ambienti/`, con l'indice in `indice.json`. I primi **30** (anno 1) il 4 ottobre, tutti e centocinquanta il 5: l'anno 1 era un campione scelto per guardare dentro il disegnatore, non un traguardo.

**Il comando è `--tutte`, e va detto perché ha un'insidia.** `--anno N` scrive lo stesso `indice.json` con dentro solo quell'anno: si può così perdere di vista che gli altri quattro anni non sono disegnati, e trovarsi un indice con trenta voci che si dichiara "i disegni" mentre i file ne hanno centocinquanta. `--tutte` riscrive l'indice per tutte le centocinquanta tappe, e l'indice è la prova che il conto è quello giusto.

**Che cosa si disegna, e che cosa non si disegna.** Ogni edificio è il **rettangolo che occupa** visto dalla zona, ritagliato ai bordi, con l'altezza che il dato dichiara. Non è la facciata: la facciata c'è nel file, ma a questa scala è più grande della zona e ritagliarla lascia un bordo obliquo, non un edificio. Il disegno è dunque **schematico**, e lo dice nell'indice: dice quanti edifici ci sono, quanto sono alti e dove stanno, non com'è fatto il tetto. **Un'altezza non dichiarata non si stima**: esce un volume neutro di `NEUTRO_M` metri, che è un'altezza dichiarata e non quella giusta.

**Il riquadro non è scritto.** È l'**inviluppo delle sagome del livello**, calcolato dai dati, con la griglia come minimo. Ed è qui che è nato il difetto più subdolo della giornata: la prima versione usava la griglia come riquadro, cioè la zona percorribile — venti metri per quindici — mentre gli edifici si interrogano entro un raggio di quaranta-centoventi metri. Il ritaglio li buttava fuori uno per uno e il risultato erano trenta immagini quasi tutte uguali, tutte sfondo: **tre coppie avevano lo stesso sha**. Lo ha visto il controllo **D3**, che confrontava gli sha, e non un occhio. Il motto è quello di `AGENTS.md`: *un controllo che non guarda è verde come un controllo che guarda*.

**Sui centocinquanta, però, D3 era diventato il controllo sbagliato.** Se chiede «gli sha sono tutti diversi?», su un anno intero la risposta è no e non può esserlo: le tappe che condividono luogo e griglia condividono disegno, e sono **43 su 150**. Un controllo che segnala come difetto la verità costringe a due sciocchi: o si falsano i dati perché i disegni escano diversi, o si zittisce il controllo. D3 è stato riscritto il 5 ottobre per confrontare **la chiave dei dati** — le sagome del livello più la sua griglia, in `chiave_dati()` di `sorgenti/art/verifica_disegni.py` — con lo sha del PNG: *stessi dati devono dare stesso disegno, dati diversi devono dare disegni diversi*. Il conto torna esattamente, **107 chiavi dati e 107 sha distinti su 150**, ed è un controllo che guarda due cose e non una.

**Un controllo che non è mai stato provato non è un controllo.** `sorgenti/art/prova_difetto_disegni_150.py` rovescia il disegnatore due volte e verifica che D3 lo veda: **F1** fa perdere un edificio a `2-5`, che allora eredita il disegno di `2-8` — «il disegnatore perde qualcosa»; **F2** mette una macchia su `5-18`, che ha gli stessi dati di altre tre tappe ma un file più piccolo — «il disegnatore aggiunge qualcosa che nei dati non c'è». Iniettati **2**, visti **2**, e il ripristino è verificato sugli sha. Un difetto che il controllo non trova è un difetto che il controllo non ha.

**Cosa costa, dichiarato.** `verifica_disegni.py` impiega **2 minuti e 10 secondi** per esecuzione, perché **D4** decodifica tutti e centocinquanta i PNG in Python puro per guardare i colori. È lento, ed è dichiarato invece che nascosto: un controllo che costa un minuto e mezzo e non lo dichiara viene saltato entro un mese.
| | |
|---|---|
| Disegni | **150**, uno per ogni tappa, su 150 |
| Chiavi dati diverse | **107** su 150: 107 tappe hanno sagome e griglia loro, e le altre **43** sono la stessa tappa vista due volte |
| SHA distinti | **107** su 150: **uguagliano le chiavi dati**, cioè nessuna tappa con dati diversi ha lo stesso disegno, e nessuna tappa con gli stessi dati ha un disegno diverso |
| Edifici disegnati | **2632** |
| Edifici ritagliati fuori dal riquadro | **0** |
| Larghezza | da **80** a **2584** pixel, secondo l'inviluppo |
| Punti per metro | **4**, dichiarati, gli stessi dei sprite della tappa 1-1 |
| PNG che si decodificano | **150 su 150**, con quattro colori dalla tavolozza |
| Tappe con disegno vuoto | **16**, dichiarate una per una in `indice.json` (`senza_sagome`), perché sono le tappe che `dati/ambienti_livelli.json` dichiara `senza_sagome_osm` |

**I colori vengono dalla tavolozza, e il file lo dichiara**: sfondo `EDE4D3`, inchiostro `2B2622`, terra `CC7722` e oro `B08D3E`, presi da `dati/fonti_visive/tavolozza.json` e scritti nell'indice. Un colore scritto nel codice del disegnatore sarebbe un colore che vive in un posto solo, che è il difetto che `verifica_colori.py` (C1) guarda.

**Quattro controlli e sei difetti iniettati.** `verifica_disegni.py` fa **D1** (ogni file promesso esiste ed è un PNG), **D2** (ogni PNG ha la misura che l'indice dichiara, **riletta dall'intestazione** e non presa da dove è stata scritta), **D3** (due livelli non hanno lo stesso sha) e **D4** (il file **si decodifica davvero**). `prova_difetto_disegni.py` rompe il **file vero** e lo rimette subito, e pretende che ogni difetto venga visto dal controllo giusto: **sei su sei**.

**D4 è nato perché D1 e D2 erano verdi su un file che non si apriva.** I trenta PNG della prima versione avevano l'intestazione che dichiarava tre canali RGB e i dati ne avevano **uno solo**: la tela teneva l'indice del colore e l'indice veniva scritto come se fosse un byte di canale. Un file ben formato, della giusta dimensione, con l'intestazione che passa — e che `png_terrarium.decodifica_png`, il lettore che il motore usa, **non riusciva ad aprire**. I tre controlli guardavano tutti l'intestazione, che si può dichiarare come si vuole; è stato il controllo che **guarda i pixel** a smascherarlo. È la terza volta in tre giorni che questo progetto incontra la stessa malattia — l'area che dice 5209 e la forma che è un punto, le trenta immagini identiche e nessun occhio, l'intestazione che dice RGB e i dati che sono un byte — e la risposta è sempre la stessa: **un controllo che guarda una metà del file è verde come un controllo che non guarda niente**.

La prova ha trovato un difetto in sé stessa, ed è il secondo della giornata: la copia di sicurezza teneva il PNG **sorgente** invece di quello **sovrascritto**, e il ripristino copiava 1-11 su 1-12 lasciandoli identici. Il sintomo era che il verificatore non tornasse verde dopo la prova, ed è la prova che dovesse accorgersene: una prova che non rimette a posto il progetto non è una prova, è un danno.

### 3.10 Gli emblemi dei premi: generati il 04/10/2026

`dati/premi.json` ha **1050 record**, uno per livello (150 informatici più 900 linguistici, il conto di `premi.md` §4.0). L'**oggetto** del premio non esiste — la prova 1 vieta che sia generato — quindi non si disegna il premio ma il **suo simbolo**: la categoria, `A` figure fino a `K` la scheda del giocatore. **1050 tessere in un foglio 1502×1962**, con l'indice che dice dove sta ognuna.

Le **undici forme sono dichiarate una per categoria** in `emblema.segno()`, accanto ai sette segni delle famiglie e non al posto loro: quelli dicono *perché qui non c'è il volto*, questi dicono *che cosa è l'oggetto*. Nessuna è un volto e nessuna è un ritratto — è il limite che il progetto mette a tutta la grafica — e ogni forma porta il **perché sta con quella categoria**, che è il controllo **Q5**.

**Solo 5 categorie su undici hanno tessere**, e le altre 6 non hanno livelli: sono le primarie delle cinque discipline che `premi.md` §4.0 dichiara senza livelli propri. È una conseguenza dichiarata, non un buco, e il catalogo lo dice in `categorie_senza_livelli`.

**I due difetti che Q3 ha visto al primo giro, e che vale la pena ricordare insieme.** Il font aveva **solo le ventesei lettere**: `FONT.get("2", [])` restituisce una lista **vuota** e senza dire niente, e il numero della tappa non veniva disegnato — `1-1-FE` e `1-2-FE` erano la stessa tessera. E il numero della tappa **da solo non basta**: `1-2` e `2-2` hanno entrambi il 2, e serve l'anno davanti. Le dieci cifre sono ora in `sorgenti/art/digiti.py`, sulla stessa griglia cinque per sette delle lettere.

Il primo difetto è la terza volta in quattro giorni che si presenta sotto una forma diversa — l'area che dichiara 5209 e la forma che è un punto, l'intestazione RGB con un byte per pixel, il carattere che il font non ha e non disegna niente. La regola che ne esce è in `AGENTS.md`: **un valore di default che sostituisce un dato mancante non è un dato, è una sparizione silenziosa**, e `FONT.get(c, [])` ne è la forma più economica.

Sei controlli da **Q1** a **Q6** e **sei difetti iniettati, sei visti**; la prova rilegge il foglio dal disco prima di dichiararsi a posto, perché chiedere alla griglia che lei stessa ha alterato significa chiedere a sé stessa.

## 4. Accuratezza: proporzioni, colori, forme

È la parte che il progetto chiama *solita accuratezza*, e le tre parole hanno tre significati tecnici.

### 4.1 Proporzioni

**La regola che vale per tutte le fonti: nessuna immagine si stira.** Ogni immagine entra nella sua scheda con la sua proporzione, e se non c'entra si ritaglia — dichiarando il ritaglio (`lingue-immagini.md` §4.2).

| Che cosa | Proporzione | Perché |
|---|---|---|
| Ritratto | 8:9, verticale, 48×54 | la persona sta in piedi |
| Scheda oggetto | 4:3, orizzontale, 96×72 | l'oggetto si vede di lato |
| **Carta geografica** | **la proiezione della fonte** | una carta geografica ha un rapporto che dipende dalla latitudine: stenderla in 4:3 mente sulle distanze |
| **Sagoma di edificio** | **quella di OSM** | la facciata ha le sue proporzioni, e sono un fatto storico |

**Il caso della carta geografica è il più serio.** I file di Natural Earth sono in coordinate geografiche, e il motore li proietta. Se la proiezione non è dichiarata, le distanze appaiono sbagliate e non c'è modo di accorgersene guardando. La regola che ne segue è che **ogni carta porta la proiezione scritta**, come porta la scala.

### 4.2 Colori

**Il problema.** Un dipinto del Quattrocento ha i colori che ha adesso, che sono diversi da quelli del Quattrocento; una fotografia d'archivio è in una pellicola che sbiadisce; una stampa ottocentesca è carta, non colore. Se si mettono insieme senza dichiarare, il gioco ha **tre sistemi cromatici** e non lo sa.

**La regola che il progetto si dà, e che è quella dei ritratti**: ogni immagine porta un'**etichetta** che dice che cosa è (`fotografia`, `dipinto`, `incisione`, `miniatura`, `rilievo`, `stampa`). Un'incisione non è una fotografia e non viene trattata come una fotografia.

**La regola nuova, che riguarda la tavolozza.** Se le fonti hanno colori che non concordano, il gioco deve scegliere: o usa i colori della fonte e dichiara che sono quelli, oppure applica una **tavolozza unica** e dichiara che l'immagine è ricolorata. La seconda è più bella e meno fedele; la prima è più fedele e meno bella.

**La scelta è la prima, ed è dichiarata in un posto solo**: `dati/fonti_visive/tavolozza.json`. È la stessa scelta che il progetto aveva già fatto tre volte — per i ritratti, per le etichette, per le proporzioni — e che resta la coerente: **ogni fonte porta i suoi colori e li dichiara**, e il gioco non ricolora il dipinto di Cavallini per farlo quadrare con la miniatura. Un posto solo perché due persone che colorano lo stesso dipinto in due modi diversi producono due giochi.

**La stessa regola, un passo oltre, per le carte geografici.** La scelta della tavolozza riguarda le immagini; i fondi di Natural Earth non hanno colori propri e il gioco deve dargliene. La domanda del 2 ottobre era se quei colori stessero **in un file** o **nel codice**, e la risposta è che dal 3 ottobre stanno in un file: `dati/fonti_visive/colori_cartografici.json`, 17 voci (§3.7). La regola è la stessa — ogni colore dice da dove viene — e in più ne vale una che le carte hanno e le immagini non hanno: **una categoria che ha un riempimento ha anche un bordo, e i due si dichiarano insieme**.

### 4.3 Forme

La forma è il contorno, e per il gioco è la cosa più difficile, perché **la forma di un edificio non è un'immagine: è una geometria**.

| Elemento | Che cosa serve | Fonte | Stato |
|---|---|---|---|
| Costa, fiumi, confini | geometrie | Natural Earth | fatto |
| Unità amministrative del mondo | geometrie del primo livello | Natural Earth 10m | fatto, 50 unità |
| Rilievo del terreno | quota e pendenza | SRTM / Terrarium | fatto per 95 luoghi |
| **Sagoma di un edificio** | **geometria della facciata** | **OSM building** | **fatto: 7322 record su 203 aree** |
| **Perimetro delle mura di Ferrara** | **poligono di chiusura** | **OSM `city_wall`** | **fatto: 14 tratti, 4,20 km²** |
| **Ortofoto aerea** | non serve: il gioco è 3/4 disegnato | — | — |

**La regola sulla forma, che è quella del progetto sui luoghi**: una forma che non è verificata **non si disegna**. Se di un edificio non si sa la pianta, si disegna un volume neutro e la scheda dice che è un volume neutro — che è la regola dei 41 luoghi che non hanno coordinate perché non sono luoghi (`luoghi-edifici.md` §1) e che ora vale anche per i **3385 edifici su 7322** che escono da OSM senza altezza.

---
## 5. Il difetto della ricerca, che è il più istruttivo del lavoro

La ricerca su Commons ha sbagliato in modi diversi, e sono tre, e vanno dichiarati tutti.

**Il primo difetto: la parola con due sensi.** Alla voce **«pipa»** (che nel Cinquecento è una pianta, la *Tabernaemontana elegans*, da cui si faceva la bevanda), la ricerca ha restituito **il rospo del genere *Pipa***, che è un anfibio sudamericano del Settecento. È lo stesso errore della «correggia» che diventava il pittore Correggio (`lingue-immagini.md` §5): una parola è una parola, non un oggetto.

**Il secondo difetto: la parola giusta, il contesto sbagliato.** Alla voce **«aereo»** (il mezzo di trasporto) è arrivata una foto di un **volo turistico sugli aerei da giardinaggio** di un'azienda italiana. Alla voce **«carrozza»** è arrivata una carrozza **americana del 1922**, che è del gioco del quinto anno travestita di mezzo del Quattrocento. Alla voce **«tavolozza affreschi»** è arrivato un autoritratto di Alessandro Allori, che è un dipinto ma non una tavolozza.

**Il terzo difetto, che è il più serio: la fonte giusta usata male.** Alla voce **«cavallo»** la ricerca ha restituito **la Cappella dei Magi di Benozzo Gozzoli** — che è una delle pitture più belle del Quattrocento italiano, ed è un *corteo di cavalieri a cavallo*, non un cavallo. Usata così com'è, l'immagine del mezzo di trasporto mostra un corteo di trecento persone.

**La regola che ne nasce è la stessa di sempre, e questa volta è verificata su cinque categorie diverse**: una ricerca che restituisce un file non ha trovato l'oggetto, ha trovato una parola. Le tre regole del progetto su questo punto sono ora tutte prese, non dichiarate:

| Progetto | Regola | Dove |
|---|---|---|
| Ritratti | un nome di file non è una prova | `ritratti.md` §1 |
| Oggetti linguistici | nessun candidato nomina l'oggetto → va guardato per primo | `lingue-immagini.md` §5 |
| **Fonti visive** | **una parola che ha due sensi va cercata con due parole** | questo documento, §5 |

**E la correzione pratica, che è la più utile di tutte**: il termine di ricerca di una voce, quando la parola è ambigua, va riscritto con **due parole che non possono confondersi**. Per la pipa: *Tabernaemontana elegans botanical*, non *pipa*. Per l'aereo: *early airliner 1950s*, non *aereo*. Per la carrozza: *Renaissance court carriage*, non *carrozza*. La ricerca va rifatta su quei termini, e il risultato va nel file con i termini accanto, come è già (`fonti_visive.json`, campo `termini`).

**La ricerca è stata rifatta il 5 ottobre, e l'istruzione era rimasta in sospeso perché non diceva di essere una scadenza.** Un'istruzione che non viene eseguita è un'istruzione che non esiste, e questa era scritta al passato come se fosse stata fatta: *la ricerca va rifatta* è un futuro, e in un documento che ha un registro delle modifiche un futuro non eseguito è un buco che non ha nome.

| Voce | Termine prescritto | Che cosa è venuto fuori |
|---|---|---|
| **aereo** | *early airliner 1950s* | **una Constellation della TWA in volo** alla fine degli anni Cinquanta: il buco è chiuso, e i due candidati del volo giardinaggio erano davvero sbagliati |
| **crociera** | *ocean liner* | **la Queen Elizabeth del 1940**, che è una cartolina: entra con la riserva scritta |
| **moto** | *vintage motorcycle 1950s* | **una Honda Cub del 1953** in un museo: entra |
| **sci** | *skiing 1950s* | **uno slalom diagonale del 1955** con la scuola di sci: entra |
| **monopattino** | *Vespa scooter 1950s* | **una Vespa 125 del 1953**: entra |
| **pipa** | *Tabernaemontana elegans botanical* | solo cataloghi botanici ed erbari: **il vuoto resta e la ragione è scritta** |
| **carrozza** | *Renaissance court carriage* | nessun file che mostri una carrozza di corte: **il vuoto resta** |
| **cavallo** | un cavallo, non un corteo | nessuna immagine utile: **il vuoto resta** |
| **elicottero** | *helicopter 1950s* | un Bell 47 a 455×319 e una squadriglia a 1109×785: **il vuoto resta, e la ragione è la misura** |

**Che cosa insegna, e perché conta più dei cinque mezzi.** Cinque bucci su nove si chiudono con una ricerca fatta bene, e i quattro che restano hanno tutti una ragione che non è «non ho trovato»: sono **una pianta cercata con il nome di un animale**, **una carrozza che è di un altro secolo**, **un cavallo che è un corteo**, **un elicottero che è troppo piccolo per essere mostrato**. Un buco con la ragione è un buco che aspetta una decisione; un buco senza ragione è un buco che aspetta che qualcuno se ne accorga, e di solito non succede.

**Una cosa da dichiarare, perché è un limite della sessione e non del metodo**: la ricerca è stata fatta con gli strumenti che avevano rete, non con `fonti_visive_cerca.py`, che dal processo non ne aveva. I candidati portano licenza, autore e misura **presi dalla pagina del file**, non ricordati; e un candidato di cui la licenza non è stata verificata **non è entrato**, che è la regola del progetto. Il file di ricerca porta la nota che lo dice.

---

## 6. I due vuoti dichiarati, e come stanno adesso

**Il vuoto era reale, e non era il buco che sembrava.** Il capitolo scriveva che l'incendio dell'archivio e la carestia «non hanno immagini d'epoca libere che le illustrino» e che il vuoto è reale. Il vuoto è reale, e la ricerca del 5 ottobre ne dà la misura: **0** risultati per l'incendio dell'archivio di Ferrara, **0** per l'incendio di una biblioteca antica in italiano, **14** per `burning of books fire engraving` — e i due che sono incisioni del Cinquecento mostrano un episodio leggendario, i libri gettati nel fuoco, non un archivio ducale. Per la carestia: **0** in italiano e **3** in inglese, che sono un mito di Giunone, una pianta di assedio del 1573 e un manoscritto di liuto. Ma la domanda dentro la domanda era un'altra, ed era quella giusta: **che cosa mostra il gioco quando un incendio è in scena?**

La risposta era già scritta nei documenti degli anni, e non è un'immagine. Le tre tappe che nominano un incendio sono la **4-3**, la **4-10** e la **4-13**, e nessuna delle tre ha una fiamma:

| Tappa | Che cosa dice dell'incendio | Che cosa mostra, cioè il suo emblema |
|---|---|---|
| **4-3** Qin Shi Huang | l'incendio dei libri del 213 a.C. è la **memoria**: «l'uomo che bruciò i libri» | un peso di bronzo con tre stampigliature uguali |
| **4-10** Ercole II d'Este | l'incendio dell'archivio del gennaio 1534 è una **ricostruzione**, e la domanda è che cosa manca di un archivio | uno scaffale vuoto con un cartellino scritto a metà |
| **4-13** Ipazia | l'incendio è la **memoria**, «un racconto di secoli dopo», e la verifica **V2** vieta di usarlo come fatto | un frammento di stele con tre righe di tre scritture diverse |

Tre tappe, tre oggetti, nessuna fiamma: **il gioco non rappresenta l'incendio, rappresenta l'oggetto che l'incendio ha lasciato.** È la forma che `mezzi.json` chiama `segno` e che il progetto ha già deciso per l'*Africa* del *Furioso* — il testo al posto dell'immagine. Perciò la voce `incendio` non è un vuoto dichiarato: è una voce con la forma **`testo`**, e la scheda porta il testo della fonte mentre la tappa porta il suo emblema, che il progetto disegna.

**La carestia invece è un buco di una forma diversa, ed è il difetto vero di questa chiusura.** Nessuna delle centocinquanta tappe la nomina: la scansione dei blocchi di persona dei cinque documenti degli anni non trova la parola in nessuno. La voce era stata cercata il 2 ottobre per completezza della categoria, e nessuno se ne accorse perché il numero che si guardava era un altro — è **M1 nella categoria sbagliata**, la stessa malattia dei dieci mezzi mai cercati. Il file la dichiara **`non_usata`**, e la prova sta accanto al numero: `persone_scansionate` e `tappe_che_nominano_l_evento` sono calcolati sui documenti, non ricordati.

| | |
|---|---|
| Voci della categoria `incidente` | **3**: incendio, carestia, moria |
| Candidati esaminati | **6**, tutti quelli della ricerca del 02/10, nessuno nuovo |
| Con immagine scelta | **1**, la moria, con l'attribuzione calcolata |
| Col testo al posto | **1**, l'incendio |
| Voci che il gioco non usa | **1**, la carestia |
| Persone scandite | **120**, i blocchi di persona dei cinque documenti degli anni |
| Tappe che nominano | **6**: 4-3, 4-10 e 4-13 l'incendio; 3-22, 4-27 e 5-9 la moria |
| Senza i confini di parola | **120**, e sono tutti: la parola «moria» sta dentro «memoria» |

**L'ultima riga è il difetto che la scansione ha trovato, e la quarta volta che il progetto incontra la stessa lezione.** Cercata come sottostringa, la voce `moria` viene fuori in tutti i **120** blocchi invece dei **tre** che sono suoi, perché `memoria` è in ogni scheda. Il progetto lo aveva già scritto — «una parola che ha due sensi va cercata con due parole», §5 — e questa volta la parola ambigua era nel **codice che conta le tappe**, non in una ricerca su Commons. I due numeri stanno nella stessa riga e il file li dichiara entrambi: `senza_confini_di_parola` vale `null` dove la scansione sbagliata non trova di più, perché **un numero che non differisce non è una prova**.

**La moria è l'unica delle tre che ha un'immagine, e l'ha perché il gioco la nomina.** È un'incisione di **Marcantonio Raimondi**, `Marcantonio - A plague scene, H,3.46.jpg`, **2500×2005** px, pubblico dominio, **senza data** nella pagina: la data si dichiara e non si indovina, come sull'aereo. È la più grande delle tre stampe della stessa serie (2500×2005, 2500×1942, 1600×1254) e sceglierne una è una scelta fra sorelle, dichiarata. Le altre due tappe che nominano la peste sono del 1854 e del 1858 e mostrano un diagramma e una mappa, non un'epidemia: **l'immagine serve alla scheda della voce, non alla scena**.

**Che cosa era deciso e non scritto, cioè il difetto di forma di questa sezione.** `AGENTS.md` scriveva dal 5 ottobre: «un vuoto si dichiara, non si riempie: l'incendio e la carestia non hanno immagine d'epoca libera, e si rappresentano con la fonte testuale, come si è fatto per l'*Africa* del *Furioso*». Qui, invece, la stessa decisione era **annunciata come da decidere** — «c'è una seconda possibilità, e va decida» — e la frase si interrompeva a metà, dopo «e per la carestia». È la quinta volta che una cosa è stata scritta al passato in un documento e al futuro in un altro: la stessa forma del *la ricerca va rifatta* di due versioni fa, e l'unico difetto che la rende invisibile è che nessun controllo confronta una decisione con il documento che la chiede. Da oggi la decisione sta qui, che è il posto che la chiedeva, e `AGENTS.md` rimanda a qui.

**Le misure sono del 5 ottobre e sono fatte con gli strumenti che avevano rete**, non con `fonti_visive_cerca.py`, che dal processo non ne ha: il file lo dichiara voce per voce, con l'interrogazione e il numero che ha risposto.

---

## 6bis. I mezzi e le epigrafi: che cosa è chiuso e che cosa no

**I due buchi che restavano sono chiusi come dati il 5 ottobre, e nessuno dei due è chiuso come immagini.** La differenza è dichiarata perché i due titoli sembrano uguali e non lo sono.

| Buco | Che cosa c'è adesso | Che cosa manca |
|---|---|---|
| **mezzi** | `dati/fonti_visive/mezzi.json`: **21 righe, una per mezzo del gioco**, con **11 immagini proposte**, 5 vuoti motivati e 5 segni fantastici | **cinque mezzi storici senza immagine**, tutti e cinque cercati il 05/10 e respinti con la ragione scritta |
| **epigrafi** | `dati/fonti_visive/epigrafi.json`: 3 immagini scelte, **la regola** (niente epigrafe senza trascrizione e traduzione) e **la fonte** del testo | **il testo**: EDH risponde anti-robot, e quindi **zero** epigrafi entrano nel gioco, e i premi F del latino e C del greco restano senza immagine finche' non arriva |

**Chiuso come dati** vuol dire che ogni voce ha una risposta scritta: un'immagine, un vuoto con la sua ragione, o un segno. Un buco chiuso come dati non si dimentica e non si confonde con uno chiuso come immagini, che è la forma più insidiosa di buco chiuso: sembra risolto e il motore non ha niente da mostrare.

## 7. Le questioni aperte

**Q1 — ~~La tavolozza va prodotta o no?~~ CHIUSA il 03/10/2026**

Il gioco aveva tre sistemi cromatici che non concordano, e finché la tavolozza non c'era
ogni immagine entrava con i suoi colori: il risultato non era un gioco, era un mosaico. La
domanda aveva due metà: **si ricolora tutto a una tavolozza unica** (più bello, meno
fedele) **oppure si dichiara ogni fonte con i suoi colori** (più fedele, meno bello)?
**La seconda**, che è quella che il progetto aveva già scelto tre volte: per i ritratti,
per le etichette, per le proporzioni.

La tavolozza è `dati/fonti_visive/tavolozza.json`, **18 voci**, costruita da fonti e non a occhio: §3.4 e §4.2. La verifica `sorgenti/verifica_tavolozza.py` (sei controlli, A1–A6) è stata eseguita **in rete** il 03/10/2026: dieci fonti ricontrollate, **0 problemi**.

**Q2 — ~~Le sagome degli edifici si costruiscono adesso?~~ CHIUSA il 03/10/2026**

Era il buco più grande, ed era bloccante per gli anni 2-5. Il file c'è: `dati/edifici_footprint.json`, **7322 edifici su 203 aree**, in formato delta, con `forma`, `altezza_m` e `fonte_altezza` — §3.2.

**La metà della domanda che riguardava i 95 luoghi è stata corretta, e il motivo va scritto**: non sono 95. Sono **54**, i luoghi che hanno coordinate. Gli altri 41 non sono luoghi (porte di gioco, percorsi fra due città, situazioni) e non hanno niente da sagomare; costruire sagome per loro avrebbe significato inventare il posto in cui si disegna un non luogo. E i 3336 edifici senza altezza diventano un **volume neutro dichiarato**, non una stima.

**Q3 — ~~Il fondo di Ferrara si costruisce?~~ CHIUSA il 03/10/2026**

L'anno 1 è l'anno in cui la copertura è gratuita e la mappa è piccola, e non aveva un file. Il perimetro delle mura è in `dati/ferrara_fondo.json`: 14 tratti OSM, 8601 m di perimetro, 4,20 km² di area interna, con la tolleranza di 60 m scelta perché è la più piccola in cui **tutte e 28 le tappe** ci cadono dentro — §3.5.

**Il perimetro che `motore-e-grafica.md` dice di usare non è un file che si poteva scaricare**, ed è il fatto più utile di questa chiusura: nessuna fonte pubblica ha il perimetro ufficiale delle mura di Ferrara. Quello che c'è è un anello di tratti con dei vuoti, e il vuoto più grosso — **1037 m** — resta senza disegno ed è dichiarato nel file.

**Q4 — ~~I colori dei fondi geografici.~~ CHIUSA il 03/10/2026**

I 19 file Natural Earth hanno proprietà e categorie, ma non colori: il colore lo decideva il motore. La domanda era se quei colori dovessero essere **dichiarati in un file** — così ogni tappa sa che cosa sta mostrando — o restare nel codice, dove nessuno li legge. **La tavolozza copriva metà della domanda**: i colori di stato e di scena c'erano già (`ok`, `attenzione`, `errore`, `sfondo`, `inchiostro`), ma quelli per **categoria cartografica** — terra, mare, confine, città — stavano nel codice. Ora stanno in `dati/fonti_visive/colori_cartografici.json`, **19 voci**: 16 dichiarate con motivo e criterio, 3 prese dalla tavolozza con la chiave dichiarata e l'esadecimale confrontato byte per byte. §3.7.

**Il punto interessante della chiusura è che cercando i colori è saltato fuori un difetto che non era di colori**, ed è la parte che resta da questa domanda: un file che non aveva niente a che fare stava nella cartella sbagliata e faceva crashare il lettore delle mappe. La storia è in §3.7.

**I due controlli che tengono la cosa ferma.** `sorgenti/verifica_colori.py` fa **sette verifiche, C1–C7**: gli esadecimali sono ben formati e le chiavi univoche (C1); le tre voci prese dalla tavolozza **dicono il vero**, confronto byte per byte (C2); le 16 dichiarate portano motivo e criterio (C3); **nessun colore vive solo nel codice** (C4); ogni voce è usata o dichiarata fra le non disegnate (C5); `dati/mappe/` contiene **solo file a delta** (C6); e ogni file di mappa ha colori che lo riguardano, su una tabella di copertura di 18 file (C7). **0 problemi**, e la prova negativa c'è: cinque difetti iniettati danno cinque problemi segnalati.

E `sorgenti/gis/verifica_mappe_disegno.py`, che **non scrive più i colori nel proprio codice ma li legge dal file**, ha reso dodici pagine di verifica. Il suo difetto di prima è instructive: scriveva `fill="F6FAFC"` invece di `fill="#F6FAFC"`, cioè dodici pagine bellissime e senza un colore, perché l'esadecimale senza il cancelletto in SVG non è un colore. È dichiarato nel suo docstring, perché un difetto che si corregge e si dimentica torna.

**Q5 — Chi guarda i 130 candidati?**

Come per gli oggetti linguistici: nessuno è stato guardato a vista, e il file di attestazione è pronto e vuoto. La differenza rispetto agli oggetti è che qui i 130 candidati sono pochi e molto diversi fra loro, e sono **le fonti che decidono l'aspetto del gioco**: scegliere male la carrozza del Quattrocento si vede in tutto il secondo anno.

---

## 8. Il riepilogo, che è la parte che serve

| | |
|---|---|
| Categorie senza veste grafica | il 02/10 erano **cinque**: mezzo, sagome, mappa di Ferrara, epigrafi, tavolozza. Il 03/10 sono **due**: mezzo ed epigrafi. Il 05/10 sono **zero senza una risposta scritta**: mezzo ed epigrafi hanno un file ciascuno, con i vuoti dichiarati dentro |
| Candidati cercati su Commons | **130**, in 32 voci |
| Voci senza immagine | **zero**: nessuna voce è senza una risposta scritta. Una è dichiarata **non usata** (la carestia, che nessuna tappa nomina), una ha **il testo al posto** (l'incendio), una ha l'immagine (la moria) |
| Candidati scelti a vista | **zero**, e dichiarato |
| Fondi geografici già pronti | **19 file**, 1,5 MB, Natural Earth, pubblico dominio |
| Tavolozza | **fatto**: 18 voci, 10 da fonti automatiche, 3 dichiarate, 5 di stato |
| Sagome degli edifici | **rifatto il 04/10/2026**: 7322 edifici su 203 aree, di cui 2632 record su 134 livelli; **3385 senza altezza** e a volume neutro |
| Fondo di Ferrara | **fatto**: 14 tratti, 8601 m di perimetro, 4,20 km², 28 tappe su 28 dentro |
| Ambienti dei livelli | **fatti**: 150 su 150, di cui 100 con coordinate verificate e **134 con sagome** |
| Colori delle carte | **fatti**: 19 voci dichiarate, di cui 3 prese dalla tavolozza; nessun colore vive solo nel codice |
| Cime e quote | **fatte**: 15 + 2 + 26 punti su tre scale, con la scoperta che la fonte è **mondiale in tutte e tre** e i tre file non sono annidati |
| Quanti ambienti il motore ha disegnato | **uno**, la tappa 1-1 |
| Emblemi dei premi | **fatti il 04/10/2026**: 1050 tessere in un foglio, undici forme dichiarate, 5 categorie in uso |
| Disegni degli ambienti | **fatti il 05/10/2026**: **150 immagini schematiche su 150 tappe**, 2632 edifici disegnati, **16 tappe vuote dichiarate**, e D3 riscritto sul confronto fra **chiave dati e sha**: 107 chiavi dati, 107 sha distinti |
| Mezzi di trasporto | **fatto il 05/10/2026**: 21 mezzi, **11 con immagine** dopo la ricerca del 05/10, **5** storici con il vuoto motivato, 5 fantastici con il segno |
| Epigrafi | **fatto il 05/10/2026 come dato**: 3 immagini, **zero** testi, la fonte dichiarata e il divieto di entrare senza testo |
| Incidenti | **chiusi il 05/10/2026 come dato**: 3 voci, **1** immagine, **1** col testo al posto e **1** non usata dal gioco, con la scansione dei 120 blocchi di persona che lo dimostra: **6 tappe** nominano un incidente, e nessuna delle tre che nominano un incendio ha una fiamma |
| Lavoro più grande che resta | i **130 candidati** da guardare a vista, i **cinque mezzi** senza immagine (tutti cercati e respinti) e i **cinquantuno** ambienti senza coordinate |
| Lavoro più grande che manca *fra i dati* | nessuno: ogni buco ha il suo file e il suo controllo, e le frasi che li nominano sono controllate come si controllano i numeri (`V1`–`V3`) |

---

## 9. Registro delle modifiche
- **v0.17 (05/10/2026)**: **un rimando che puntava a una prova che non esiste.** Il capitolo sui premi diceva «la prova 5 vieta che l'oggetto sia generato», e `premi.md` §3 dichiara **quattro** prove: il divieto è nella **prima**. Il numero è corretto e la frase si leggeva come le altre, quindi è il difetto che `AGENTS.md` chiama *un numero vero che guarda il numero sbagliato*. Il rimando è corretto e il controllo **P8** di `sorgenti/verifica_premi.py` legge le quattro righe della tabella e rifiuta da qui in poi ogni rimando a una prova inesistente, in questo capitolo come in tutti gli altri.
- **v0.16 (05/10/2026)**: **tre numeri falsi nella stessa sezione, e nessuno dei sette controlli che c'erano li guardava.** Il titolo della §3 diceva «gli otto file costruiti», la frase due righe sotto diceva «sono sei, e sei è il numero che dice §8», e il riepilogo ripetiva «i sei file ci sono e sono verificati»: tre numeri, tutti e tre veri il giorno in cui sono stati scritti, nessuno dei tre mosso quando sono diventati falsi, e nessuno dei sette controlli — **M1–M7, E1–E4** — guardava quella frase, quel titolo o quella riga. È la malattia di sempre nella forma più semplice: *una riga scritta due volte, o non scritta, non lascia traccia nei controlli dei numeri*, e qui la riga era un **titolo**.
  - **la cura non è stata correggere i numeri: è stata toglierli.** Il titolo ora non porta un numero, la frase non dice più «sono sei», e al loro posto ci sono **i nomi dei file** — che si possono controllare. Un numero ripetuto in due posti è la malattia; toglierne uno è la cura, e l'altro si toglie anche;
  - **la tabella delle categorie ha una quinta colonna, `File di dati`**, con il file che ogni categoria cercata ha prodotto: `mezzi.json`, `edifici_footprint.json`, `epigrafi.json`, `incidenti.json`, `tavolozza.json`. Le cinque righe sono l'unico posto in cui la cosa si dichiara, e **il capitolo non porta più nessun totale**;
  - **tre controlli nuovi, V1–V3**, tutti e tre di una sola idea: *i tre posti in cui il capitolo nomina un file*. **V1** la tabella delle categorie dice il file che ogni categoria ha prodotto, e quel file esiste; se la cella dice `nessuno`, dice anche perché. **V2** ogni capitolo della §3 dichiara nel proprio testo almeno un file che esiste: un capitolo che non costruisce niente deve dirlo. **V3** ogni percorso citato nella riga `dati:` del frontespizio esiste. La prova ne inietta **diciassette** difetti e li vede **tutti e diciassette**;
  - **V2 è nato verde, e la prova lo ha detto**: il ciclo che gira sui capitoli guardava il pezzo di §3 che finisce **prima** del primo capitolo, quindi non conteneva nessun capitolo e non guardava niente. È la terza volta che il difetto vero è un controllo che guarda il posto sbagliato, e la seconda che lo dice la prova e non il giudizio — il messaggio «la prova non ha provato» è nato per questo;
  - **due difetti della prova, dichiarati perché sono la regola nuova**: il difetto di **V1** colpiva la prima occorrenza della stringa, che è la tabella dell'inventario in §1 e non quella delle categorie in §3, quindi il controllo non aveva niente da vedere; e il difetto di **V2** rompeva `mezzi.json` in un capitolo che dichiara **due** percorsi, così che il secondo restava vivo e il capitolo continuava a dichiarare un file che esiste — che è la regola stessa del controllo. Le tre iniezioni ora colpiscono il posto giusto: nella sezione giusta, nel capitolo che dichiara un solo percorso, e nel frontespizio che è la prima riga che si legge;
  - **un difetto di V3, che è il più instructive**: nel frontespizio i percorsi sono in chiaro, non fra apici backtick, e la regex del capitolo li richiedeva. Il controllo era verde **perché non leggeva una parola** di quello che dichiara — un controllo che non guarda è verde come un controllo che guarda, e questa volta la prova non c'entra: era il controllo a essere muto.

- **v0.15 (05/10/2026)**: **i due vuoti erano dichiarati da quattro giorni, e la dichiarazione era giusta sul numero e sbagliata sulla domanda.** «L'incendio e la carestia non hanno immagine d'epoca libera»: il vuoto è reale, e la ricerca del 5 lo conferma con la misura (**0** risultati per l'incendio dell'archivio, **0** per quello di una biblioteca antica, **14** per le incisioni di libri che bruciano — e mostrano un episodio leggendario, non un archivio; **0** e **3** per la carestia). Ma la domanda giusta non era *che immagine ha un incendio*: era **che cosa mostra il gioco quando un incendio è in scena**. La risposta era già scritta nei documenti degli anni.
  - **le tre tappe che nominano un incendio non hanno una fiamma**: la 4-3 (Qin Shi Huang) ha per emblema un **peso di bronzo**, la 4-10 (Ercole II) uno **scaffale vuoto con un cartellino scritto a metà**, la 4-13 (Ipazia) un **frammento di stele**. Il gioco rappresenta **l'oggetto che l'incendio ha lasciato**, ed è la forma che il progetto chiama «il testo al posto dell'immagine». La voce `incendio` non è un vuoto: è la forma **`testo`**;
  - **la carestia è un buco di una forma diversa, ed è il difetto vero**: nessuna delle centocinquanta tappe la nomina. Una voce cercata e non usata è **M1 nella categoria sbagliata** — il numero che si guardava era un altro. Ora è dichiarata **`non_usata`**, con `persone_scansionate` e `tappe_che_nominano_l_evento` calcolati sui cinque documenti degli anni;
  - **`dati/fonti_visive/incidenti.json`**, costruito da `sorgenti/incidenti_fonti.py`: 3 voci, 6 candidati, **1** immagine (un'incisione di Marcantonio Raimondi, 2500×2005 px, pubblico dominio, **senza data** dichiarata, scelta fra tre stampe della stessa serie), **1** col testo al posto e **1** non usata. La rigenerazione dà un file identico;
  - **sei controlli nuovi, I1–I6**, in `sorgenti/verifica_fonti_visive.py`: I1 una riga per ogni voce cercata, I2 una forma sola fra le tre e la sua ragione, I3 l'immagine fra i candidati con l'attribuzione calcolata, **I4 la dichiarazione «nessuna tappa la usa» deve essere vera** — la scansione è rifatta dal verificatore sul documento e il conto del file deve coincidere, I5 ogni tappa dichiarata esiste fra i centocinquanta livelli e **l'emblema del file è quello che il documento dell'anno dichiara per quella tappa**, I6 i numeri di §6 sono quelli del file. La prova ne inietta **quattordici** difetti e li vede **tutti e quattordici**;
  - **quattro difetti della strada, dichiarati perché sono la regola nuova**: la scansione del verificatore chiamava una variabile locale `sezione`, che in Python è una funzione dello stesso modulo usata da M5 ed E4 — il nome assegnato in un punto della funzione è locale in tutta la funzione, e le verifiche precedenti avrebbero smesso di trovarla; il primo blocco di persona di ogni anno si mangiava mezzo documento, perché finiva alla successiva intestazione di persona e non alla successiva intestazione qualunque, e il conto che ne era uscito era di tre persone più delle vere; l'emblema della 3-22 era stato scritto a mano ed era sbagliato — l'emblema è **l'albero con dieci rami**, non quello che avevo indovinato — ed è la prova che la regola «un numero non si scrive a mano» vale anche per un oggetto; e il numero della scansione sbagliata era in letteratura **duecento** dove la scansione ne trova **120**: un numero in prosa che nessuno ricalcola è un numero che invecchia, e l'unica correzione è scrivere quello che la macchina ha contato;
  - **la decisione era presa e non scritta, e la frase si interrompeva a metà.** `AGENTS.md` scriveva dal 5 «si rappresentano con la fonte testuale, come si è fatto per l'*Africa* del *Furioso*»; qui la stessa decisione era annunciata come **da decidere**, e la sezione finiva dopo «e per la carestia». È la quinta volta che una cosa è al passato in un documento e al futuro in un altro, e l'unico difetto che la rende invisibile è che nessun controllo confronta una decisione con il documento che la chiede.

- **v0.14 (05/10/2026)**: **la ricerca che il capitolo prescriveva era rimasta in sospeso, e nessuno se ne accorse perché era scritta al passato.** Il §5 fin dal 2 ottobre diceva *la ricerca va rifatta su quei termini*: un futuro, in un documento che ha un registro delle modifiche, e un futuro non eseguito è un buco che non ha nome. Rifatta il 5: **cinque buchi su nove si chiudono** e gli altri quattro hanno tutti una ragione che non è «non ho trovato».
  - **cinque mezzi che non erano mai stati cercati** hanno un'immagine: la **crociera** è la Queen Elizabeth del 1940, l'**aereo** la Constellation della TWA in volo, la **moto** una Honda Cub del 1953, gli **sci** uno slalom diagonale del 1955, il **monopattino** una Vespa 125 del 1953. Il file dei mezzi passa da **6 a 11** immagini su 21;
  - **i cinque vuoti che restano sono stati cercati e respinti**, e la ragione è diversa per ciascuno: un rospo al posto della pianta, una carrozza americana al posto di corte, la Cappella dei Magi al posto del cavallo, un conchiglio al posto del viandante, e un elicottero a **455×319** che il motore dovrebbe ingrandire di sei volte;
  - **la ricerca è stata fatta con gli strumenti che avevano rete**, non con `fonti_visive_cerca.py`, che dal processo non ne aveva: il file di ricerca lo dichiara, e **un candidato di cui la licenza non è stata verificata non è entrato**;
  - **i numeri delle voci e dei candidati sono passati da 27/125 a 32/130** in tre posti — la tabella delle categorie, il frontespizio e il riepilogo — e nessuno dei tre si sarebbe mosso da solo. È il **M7** nuovo in `verifica_fonti_visive.py`: tre posti, un numero solo, e il controllo li confronta tutti e tre col file. La prova ne inietta **otto** difetti e li vede **tutti e otto**;
  - **due difetti trovati nella strada, dichiarati perché sono la regola nuova**: l'attribuzione tirava fuori l'anno con una regex, e da «1940s (cartolina)» ricavava **l'anno di caricamento del file** — un'attribuzione con una data falsa è peggio di un'attribuzione senza data; e nel file che avevo scritto c'era la parola **`per`** al posto di **`for`**, sette caratteri che lo rendono non compilabile. Non è un errore di logica e non si vede se non si compila: **dopo aver scritto un file, `py_compile` va girato sempre**, anche quando il file sembra giusto.

- **v0.13 (05/10/2026)**: **gli ultimi due buchi chiusi come dati, e il numero che li nascondeva era vero.** I mezzi di trasporto avevano **undici** immagini proposte e il gioco ne usa **ventuno**: dieci storici non erano mai stati cercati, e nessuno se ne accorgeva, perché la tabella contava le voci cercate e non i mezzi del gioco. È la stessa malattia di un numero vero che guarda il numero sbagliato, e per questo il controllo nuovo confronta il file con **`percorsi_mezzi.py`**, non con se stesso.
  - **`dati/fonti_visive/mezzi.json`**, costruito da `sorgenti/mezzi_fonti.py`: **21 righe**, una per mezzo, e ogni riga è una delle tre forme ammesse — **6** immagini proposte con l'attribuzione **calcolata** e la riserva dichiarata, **10** storici con il vuoto e la sua ragione (fra cui i **5** mai cercati), **5** fantastici con il segno dedicato e nessuna immagine, perché sono creature;
  - **`dati/fonti_visive/epigrafi.json`**, costruito da `sorgenti/epigrafi_fonti.py`: 3 immagini scelte e **zero** testi, e il testo mancante è dichiarato con la **fonte** che lo tiene (**EDH**, con l'identificatore P1415 di Wikidata che la rende recuperabile) e con la misura delle tre fonti interrogate il 5: Wikidata dà 63048 identificatori e 15 traduzioni ma non il testo, Commons ha il campo `inscriptions` vuoto, EDH risponde anti-robot su due domini e sull'API. **Nessuna epigrafe entra nel gioco**, e il controllo lo vieta finché trascrizione e traduzione non ci sono: i premi **F** del latino e **C** del greco restano senza immagine, ed è un fatto dichiarato;
  - **`sorgenti/verifica_fonti_visive.py`**, dieci controlli **M1–M6** ed **E1–E4**: M1 confronta il file con i mezzi del gioco, M2 pretendere che l'immagine sia fra i candidati della ricerca, M3 che ogni mezzo abbia **una** delle tre forme e che il vuoto abbia la ragione, M4 che nessun mezzo fantastico abbia un'immagine, M5 ed E4 che i numeri scritti in §3.1 e §3.3 siano quelli del file, M6 che l'attribuzione ci sia e la licenza sia libera, E1 che ogni voce abbia la sua immagine, **E2 che nessuna epigrafe entri senza testo**, E3 che nessun testo sia scritto dal progetto. La prova ne inietta **sette** uno alla volta e li vede **tutti e sette**;
  - **due difetti della prova, dichiarati perché sono la regola nuova**: la prima versione accettava che un difetto fosse visto da un controllo diverso dal suo — l'M4 iniettava un'immagine a un mezzo fantastico e la segnalava **M2** — e la seconda leggeva il numero sbagliato della riga, perche' la funzione cercava la prima cifra dopo una frase che finiva col grassetto; ne stampava sei difetti, tutti suoi, dei quali nessuno era un difetto del documento;
  - **R5 in `verifica_registri.py`**: nessuna intestazione di sezione scritta due volte. Il difetto che l'ha motivato era **mio**, di oggi: riscrivendo questo stesso elenco del registro avevo lasciato `## 9. Registro delle modifiche` due volte di fila, e quattro controlli non lo vedevano perche' guardano le righe e non le intestazioni.

- **v0.12 (05/10/2026)**: **i trenta disegni dell'anno 1 erano verdi, e D3 era diventato il controllo sbagliato.** Estesi i disegni a tutte e centocinquanta le tappe (`python3 sorgenti/art/disegna_ambienti.py --tutte`, 25 s, 1,5 MB, **2632** edifici disegnati, **0** ritagliati fuori, larghezza da **80** a **2584** px, **150** PNG decodificati). Le **16** tappe senza sagome restano vuote e sono dichiarate una per una: un disegno vuoto che non sa di essere vuoto è più peggio di un disegno che non c'è. Ma il controllo **D3** non poteva restare com'è: chiedeva che gli sha fossero tutti diversi, e sui centocinquanta la risposta è no e non può essere sì — le tappe con le stesse sagome sulla stessa griglia sono **43 su 150** e condividono il disegno. Un controllo che segnala come difetto la verità non è un controllo, è un allarme spento.
  - **D3 è riscritto in `sorgenti/art/verifica_disegni.py`**: confronta la **chiave dei dati** (sagome + griglia, funzione `chiave_dati()`) con lo sha del PNG — stessi dati, stesso disegno; dati diversi, disegno diverso. Il conto torna: **107 chiavi dati, 107 sha distinti su 150**;
  - **la prova del difetto è nuova, `sorgenti/art/prova_difetto_disegni_150.py`**: rovescia il disegnatore due volte (F1 perde un edificio dalla 2-5, F2 macchia la 5-18), verifica che D3 veda entrambi i difetti e verifica il ripristino confrontando gli sha. **2 iniettati, 2 visti**;
  - **la data dell'indice non è più scritta a mano**: `indice.json` scriveva `2026-10-04` mentre i centocinquanta disegni sono del 5; ora è calcolata. È un numero, e i numeri scritti a mano invecchiano;
  - **il costo è dichiarato**: `verifica_disegni.py` impiega **2 min 10 s** per esecuzione perché D4 decodifica tutti i PNG in Python puro. È lento, e si dichiara invece di fingere che sia veloce.
  - **l'insidia di `--anno N`** è dichiarata accanto al comando: scrive lo stesso `indice.json` con dentro un anno solo, e un indice con trenta voci che si dichiara "i disegni" fa perdere di vista gli altri quattro anni. Si usa `--tutte`.

- **v0.11 (04/10/2026)**: **tre righe scritte due volte, e un registro che si chiudeva a metà.** La sezione §3.10 e la riga «Emblemi dei premi» del riepilogo §8 erano ciascuna in duplice copia, parola per parola: la sostituzione che le aveva scritte era stata eseguita due volte e nessun controllo se n'era accorto, perché i numeri erano giusti in entrambe le copie. Nel registro §9 c'era una riga `|---|---|---|` **in mezzo alle righe**: chiudeva la tabella dopo la 0.5 e le quattro righe sotto sembravano un'altra tabella. E le versioni **0.9 e 0.10 non avevano riga**, cioè i due difetti più importanti della giornata — il font senza le cifre e le forme disegnate senza guardarle — erano spariti dal registro mentre erano nel testo. Il modulo è quello di sempre, nella quinta forma: una riga scritta due volte è un numero contato due volte, e un numero contato due volte è un documento che mente sul suo stesso lavoro.

- **v0.4 (03/10/2026)**: **i numeri di §3.6 erano scritti a mano, e non erano più quelli del file.** Il controllo che sorveglia gli ambienti ne aveva sette, e tutti e sette confrontavano i dati fra loro: nessuno confrontava il dato con **le righe scritte qui**. Così la sezione dichiarava **99** ambienti con coordinate quando il file ne ha **100**, **69** con sagome OSM quando ne ha **68**, `citta_antica` **11** contro **12** e `percorso` **11** contro **10**, e i vuoti erano tre cifre sotto: `senza_sagome_osm` 81 contro 82, `coordinate_non_e_un_luogo` 24 contro 23, `nessun_luogo_dichiarato` non citato. La dichiarazione più falsa era un’altra: la sezione scriveva che «la 1-1 ha un orientamento e gli altri 149 no», mentre **nessuno** dei centocinquanta lo ha — la 1-1 compresa. Tutte le verifiche passavano, ed è la ragione per cui il difetto è rimasto due giorni in un documento che si dichiara costruito.
  - **B8 è il controllo nuovo**, in `sorgenti/verifica_ambienti.py`: legge questa sezione e confronta ogni numero con il conto — le tre quote della tabella, i nove tipi e tutti i vuoti. Lo ha scritto il difetto: ne ha trovati sette in una volta sola;
  - **le due frasi che il file scrive su se stesso non sono più scritte a mano.** In `sorgenti/ambienti_livelli.py` il numero delle ipotesi era «le 51 tappe» quando le ipotesi erano già **50** (la 4-16 aveva trovato la sua), e l’orientamento era dato per dichiarato sulla 1-1. Ora entrambe le frasi sono calcolate: la regola è che **un numero in letteratura invecchia e nessuno lo rilegge**, mentre un numero calcolato cambia da solo quando il dato cambia sotto;
  - la lezione che resta è la stessa di `verifica_coerenza.py`: i controlli devono guardare **anche le frasi scritte**, non solo i file. Un dato che nessuno confronta con la sua descrizione è un dato che può dire due cose diverse nello stesso giorno.

| Data | Versione | Che cosa è cambiato |
|---|---|---|
| 04/10/2026 | 0.10 | **Il catalogo dei premi è esistito, e con lui undici forme disegnate senza guardarle.** `dati/premi.json` ha **1050 record** con i campi dell'oggetto dichiarati vuoti (la prova 1 vieta di generare un premio), e gli emblemi sono **1050 tessere in un foglio solo** di 1502×1962. Sei controlli **Q1–Q6** con sei difetti iniettati e sei visti. Ma sei delle undici categorie non hanno nessun livello e quindi nessuna tessera: erano state disegnate **senza che nessuno le guardasse**, ed è guardando che si è visto che `figura_su_piedistallo` era un obelisco e `scudo` un rettangolo. |
| 04/10/2026 | 0.9 | **I mille e cinquanta emblemi erano tessere identiche.** Il font del progetto aveva solo le **ventisei lettere** e le dieci cifre erano in un file che nessuno leggeva: `FONT.get("2", [])` restituisce una lista **vuota** e senza dire niente, quindi il numero della tappa non veniva disegnato e `1-1-FE` e `1-2-FE` erano lo stesso file. Le cifre sono ora in `sorgenti/art/digiti.py` e il controllo **Q3** confronta i sha di tutte le 1050 tessere. |
| 04/10/2026 | 0.8 | **I trenta disegni erano verdi su tutti i controlli e non si aprivano.** Il PNG si annunciava RGB e ne scriveva un byte per pixel: la tela teneva l'indice del colore e l'indice finiva nel file come byte di canale. D1 e D2 leggono l'intestazione, che si può dichiarare come si vuole, e D3 confronta gli sha — nessuno dei tre guardava i pixel. È nato **D4**, che decodifica il file con `png_terrarium.decodifica_png` e confronta i pixel con la misura dichiarata, e **E6** nella prova dei difetti, che costruisce apposta un PNG con la stessa malattia. I colori ora vengono da `dati/fonti_visive/tavolozza.json` e sono dichiarati nell'indice: sfondo EDE4D3, inchiostro 2B2622, terra CC7722, oro B08D3E. **Sei difetti iniettati, sei visti.** |
| 04/10/2026 | 0.7 | **Il file delle sagome aveva il conto giusto e la geometria distrutta.** `dati/edifici_footprint.json` scriveva la forma con `round(x / Q)` invece di `round(x * Q)`: divideva per cento un numero che era già in metri, e ogni vertice finiva a zero. I **5209** edifici erano veri, uno per uno, e la loro sagoma era un punto: l'ingombro più grande in tutto il file misurava cinque centimetri quadrati. Un numero vero e una forma falsa nello stesso file, e la parte che un umano guarda è proprio quella che era vera. Oggi il file è stato **rigenerato da capo**: **7322 edifici su 203 aree** — i centocinquanta pin dei livelli più le 188 città, perché i pin del registro sono città intere e le tappe dell'anno 1 sono a più di due cento metri dal pin di Ferrara, e il file diceva «Ferrara ha centoquattro edifici» mentre le tappe non ne avevano nessuno. Sono tre difetti nuovi, trovati solo dopo che la forma c'era: la **toleranza di semplificazione fissa** cancellava gli edifici piccoli (un'area di due metri con una toleranza di un metro e mezzo diventava un quarto della sua area), il **confronto della perdita** guardava l'area semplificata invece di quella dichiarata, e **dieci edifici** con l'altezza ma di mezzo metro quadro passavano la soglia. Due verificatori nuovi: `verifica_sagome.py` (**S1–S3**, che sul file rotto trovava 5209 problemi su 5209 e ora dà 0) e `verifica_disegni.py` (**D1–D3**). |
| 04/10/2026 | 0.6 | **Undici file di disegno che il motore non poteva usare, e sei che nessuno guardava.** Nella cartella dei ritratti c'era la piazza della Cattedrale — facciata, cartello, lapide, due statue, il protagonista in quattro fotogrammi, tre ritratti a mano — e nessun codice li caricava e nessun dato li nominava: il controllo 2 li dichiarava morti e aveva ragione. Sono ora la tabella `SPRITE`, con la voce della tabella 3 da cui prendono il posto e la misura **misurata sul PNG**; i posti sono riletti dal documento e il controllo **B9** li rilettura (§3.6). Nello stesso giorno i **sei emblemi superati** — le persone passate da emblema a ritratto — sono spariti dalla cartella: erano sei file e quattro immagini distinte, cioè lo stesso difetto dei sessanta emblemi che erano diciotto file, quattro giorni prima. Restano due famiglie diverse in `out/`: **198** PNG per le persone e **11** sprite, **209** in tutto, e il controllo 2 sa dire quale è quale invece di contare. La facciata diventa un controllo: i suoi 509 px sono il prodotto dei 39,8 m del documento per i 12,8 px per metro della scala, e se i due numeri del documento non tornassero fra loro si vedrebbe lì. |
| 04/10/2026 | 0.5 | **La riga dei ritratti era un numero invecchiato, e la riga degli emblemi era un buco che si era chiuso da solo.** La tabella di §1 diceva «169 su 213» e «169 PNG a 48×54»: il 169 era il conto del 1 ottobre, quando quarantatre immagini erano ancora aperte, e nessun controllo lo confrontava con i dati. Ora dice **138 su 213** e i **198 PNG, uno per persona**, e aggiunge che i 60 emblemi sono **disegni** e non tessere (`ritratti.md` §3ter). La riga non è un abbellimento: fino al 3 ottobre i sessanta emblemi erano diciotto file distinti e dieci persone ne avevano uno identico, e qui la tabella ne contava sessanta senza che nessuno guardasse se fossero gli stessi. |
| 03/10/2026 | 0.3 | **La Q4 è chiusa, e cercando i colori delle carte è saltato fuori un difetto che non era di colori.** I colori per categoria cartografica stavano scritti nel codice del disegnatore: ora sono `dati/fonti_visive/colori_cartografici.json`, **19 voci**, 16 dichiarate con motivo e criterio e 3 prese dalla tavolozza con l'esadecimale confrontato byte per byte, con la regola che **una categoria con il riempimento ha anche il bordo** e le tre che il riempimento non ce l'hanno, dichiarate una per una (§3.7). **Il difetto vero**: `dati/mappe/mondo_admin1_copertura.json stava dentro `dati/mappe/`, dove vale la regola che ci stanno solo file a delta, e faceva crashare il lettore con un `IndexError` che non diceva niente; il file è stato spostato in `dati/`, il lettore ora controlla la forma del file e solleva un `ValueError` che la dice, e il controllo **C6** tiene la regola ferma. **Le cime con la quota** (`mondo_110_altitudine`, `europa_50_altitudine`, `penisola_10_altitudine`: 15, 2 e 26 punti, più `dati/altitudine_manifest.json`), con le due scoperte che i numeri non nascondono: la fonte è **mondiale in tutte e tre le scale** — il file da 50 m elenca 86 cime da longitudine −167 a +160 e solo due in Europa — e **i tre file non sono annidati**, perché sono selezioni diverse della stessa fonte globale (§3.8). Per costruirli è servita la funzione `punti()` in `sorgenti/gis/shapefile_lettore.py`, che legge `Point` e `MultiPoint`, e il difetto che porta con sé è che il `MultiPoint` ha dentro i punti una struttura che sembrava quella di un poligono. Due verificatori nuovi: `verifica_colori.py` (**C1–C7**, con cinque difetti iniettati che danno cinque problemi) e `verifica_altitudine.py` (**D1–D7**, con sei difetti che ne danno sette); `verifica_mappe_disegno.py` è stato riscritto perché **legga** i colori dal file invece di scriverli nel proprio codice, e il suo difetto di prima (`fill="F6FAFC"` senza il cancelletto: dodici pagine senza un colore) è dichiarato nel docstring. Delle cinque questioni resta **solo la Q5**. |
| 03/10/2026 | 0.2 | **Quattro dei cinque buchi sono chiusi, e sono chiusi con quattro file di dati.** **La tavolozza** (`dati/fonti_visive/tavolozza.json`, 18 voci: 5 da Wikidata, 5 dall'infobox di un artista, 3 dichiarate, 5 di stato), costruita da fonti e non a occhio, con tre difetti dichiarati: **un pigmento non si cerca per nome** («vermilion» è una città canadese), **`P462` non è l'esadecimale** ma un link a un oggetto colore — e il suo valore è un dizionario, non una stringa — e **cinque pigmenti su quindici non hanno codice da nessuna parte**, nessuno dei quali è stato riempito con una cifra plausibile. **Le sagome degli edifici** (`dati/edifici_footprint.json`, 1,6 MB, **5209 edifici su 54 luoghi**, 588 con altezza misurata, 1285 ricavata dai piani, **3336 a volume neutro dichiarato**), con le quattro regole dichiarate e i due difetti dell'interrogazione a Overpass. **Il fondo di Ferrara** (`dati/ferrara_fondo.json`, 14 tratti, 8601 m, **4,20 km²**, 28 tappe su 28 dentro) con la tolleranza di 60 m scelta **non a occhio ma come più piccola in cui tutte le tappe cadono dentro**, la scala completa dei cinque passi nel file, e **una fonte rifiutata e dichiarata**: la relation OSM «Centro storico», che lascia fuori Piazza Ariostea e Palazzo dei Diamanti. **Gli ambienti dei centocinquanta livelli** (`dati/ambienti_livelli.json`, **150 su 150**, nove tipi, nove griglie dichiarate come scelta di progetto, tutti i vuoti dichiarati uno per uno), costruiti sul modello della tappa 1-1 e per relazione esplicita fra livello e luogo, non per confronto di nomi. Sei controlli nuovi, due verificatori: `verifica_tavolozza.py` (A1–A6, eseguito **in rete**, 0 problemi) e `verifica_ambienti.py` (B1–B6, 0 problemi). Le Q1, Q2 e Q3 sono chiuse; restano Q4 e Q5. |
| 02/10/2026 | 0.1 | Prima stesura. Inventario delle fonti visive: il gioco ha i ritratti (213), i fondi geografici (19 file Natural Earth, 1,4 MB) e i 1120 candidati degli oggetti linguistici; **non ha** i mezzi di trasporto, le sagome degli edifici, il fondo di Ferrara, le epigrafi e la tavolozza. Ricerca su Commons di 27 voci in cinque categorie: **125 candidati**, due vuoti dichiarati (incendio, carestia). Le tre regole sull'accuratezza — proporzioni, colori, forme — con il caso serio della proiezione delle carte, che non dichiarata mente sulle distanze. I tre difetti della ricerca, con la pipa che è diventata un rospo e la Cappella dei Magi che è un corteo, e la correzione pratica: **le parole ambigue si cercano con due parole**. Cinque questioni aperte. |
