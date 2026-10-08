---
titolo: Videogioco "I cinque duchi" — Roadmap per la risistemazione della documentazione
tipo: piano
versione: 0.10
data: 2026-10-08
autore: Pietro Fabbri (con Claude)
documenti collegati: videogioco-5-duchi-audit.md (v0.34), videogioco-5-duchi-gioco.md (v0.9), videogioco-5-duchi-esercizi.md (v0.3), videogioco-5-duchi-meccaniche.md (v0.7), videogioco-5-duchi-tappa-1-01.md (v0.6)
---

# Roadmap: risistemare la documentazione

Decisione di Pietro del 06/10/2026: **prima** si risistema tutta la documentazione e si colmano i buchi rimasti, **poi** si lavora sui livelli, a partire dal rifacimento migliorato della tappa 1-1. Si lavora sempre sul repository GitHub.

Questo documento dice **che cosa va fatto, in che ordine e perché**. Chi riprende il lavoro senza il contesto della conversazione deve poter capire da qui a che punto si è: ogni fase ha uno **stato** e un **criterio di chiusura** verificabile.

## 1. Diagnosi (06/10/2026)

Quattro problemi, in ordine di peso.

1. **Il nucleo di gioco è rimasto indietro.** I documenti che dicono *come si gioca* sono i più vecchi: `curricolo` v0.1 (senza registro delle modifiche), `esercizi` v0.1, `motore-e-grafica` v0.1, `meccaniche` v0.3, `gioco` v0.5. Le decisioni prese dopo sono finite nei documenti trasversali e non sono state riportate nel nucleo, che quindi li contraddice:
   - **ripasso**: `gioco.md` §4.2 prevede 2–4 domande sulle carte in scadenza (Leitner); `ripassi.md` prevede un test d'ingresso di dieci domande casuali;
   - **collezione**: `gioco.md` §3 parla di carte bronzo/argento/oro; `premi.md` e `inventario.md` di premi, salvadanaio e quattro registri;
   - **salvataggio**: cinque documenti parlano ancora di «codice di ripresa»; `meccaniche.md` propone il file `.txt`;
   - **modello di livello**: l'audit cita le «nove componenti del livello», ma nessun documento le raccoglie in uno schema unico.
2. **La storia del lavoro è mescolata al progetto.** Molte sezioni raccontano come è stato trovato un difetto invece di dire che cosa è deciso. L'audit ha 24 sezioni e otto sezioni `3…` stanno dopo il registro delle modifiche; `AGENTS.md` (61 KB) è per metà racconto di lezioni di metodo. Per chi arriva senza contesto la parte normativa è difficile da trovare.
3. **Non tutti i controlli passano.** Su 35 verificatori, quattro non erano verdi il 06/10/2026: `verifica_coerenza.py` (cerca `_commit_coerenza.py`, che non è nel repository), `lingue/verifica_metadati_mancanti.py` (5 esiti per 4 candidati), `lingue/verifica_immagini_oggetti.py` (7 immagini troppo piccole), `verifica_tavolozza.py` (oltre 200 s).
4. **Quattro decisioni bloccanti** aspettano Pietro (`audit.md` §2): B1 livelli linguistici e informatici, B2 voci degli oggetti, B3 LIS, B4 chi guarda le 1120 immagini. Più quindici importanti (§3).

## 2. Le fasi

| Fase | Che cosa | Criterio di chiusura | Stato |
|---|---|---|---|
| 0 | Punto di partenza pulito | Tutti i verificatori verdi, o il motivo scritto per cui uno non può esserlo | **fatta il 06/10/2026** (§3) |
| 1 | Architettura della documentazione | Ogni documento ha un tipo dichiarato; i documenti normativi dicono il presente; lo storico è separato; `AGENTS.md` contiene solo decisioni, convenzioni e procedura | **fatta il 06/10/2026** (§4) |
| 2 | Allineare il nucleo di gioco e scrivere il modello di livello | Nessuna contraddizione fra `gioco`, `esercizi`, `meccaniche`, `motore-e-grafica`, `ripassi`, `premi`, `inventario`, `pedagogia`; esiste `modello-di-livello.md` | **fatta il 07/10/2026** (§5) |
| 3 | Le decisioni di Pietro | Ogni domanda bloccante o importante ha una risposta registrata, oppure è dichiarata rinviata con il perché | **chiusa** l'08/10/2026 (§6) |
| 4 | Colmare i buchi di contenuto | Anno 1 completo nelle schede delle 30 tappe; correzioni già decise applicate; verifiche storiche aperte chiuse o dichiarate | da fare |
| 5 | Rifinitura e README | README breve; numeri e refusi corretti; rimandi chiusi | da fare |
| 6 | Collaudo di portabilità | Verificatori verdi; un agente senza contesto specifica la tappa 1-2 leggendo solo i documenti, e dove indovina si apre un buco | da fare |

### Fase 0 · Punto di partenza pulito

Portare a verde i quattro verificatori rossi, o dichiarare per iscritto perché uno non può esserlo. Lo stato raggiunto è la linea di base: ogni fase successiva si misura contro di essa.

### Fase 1 · Architettura della documentazione

- Quattro tipi di documento, con regole diverse: **normativi** (che cosa è deciso, al presente), **cataloghi** (dati e tabelle, generati), **audit** (domande aperte), **storico** (come ci si è arrivati).
- Il racconto dei difetti trovati esce dai documenti normativi e va nello storico: non si perde nulla, cambia dove sta scritto.
- `AGENTS.md` si riduce a decisioni, convenzioni e procedura; le lezioni di metodo vanno in un documento di metodo.
- L'audit si riordina: sezioni in ordine, una scheda per questione, le chiuse in fondo.

### Fase 2 · Allineare il nucleo di gioco

È la fase che prepara il rifacimento della tappa 1-1.

- Riscrivere `gioco`, `esercizi`, `meccaniche` e `motore-e-grafica` incorporando `ripassi`, `premi`, `inventario` e `pedagogia`.
- Ogni contraddizione si risolve con una scelta esplicita; dove la scelta spetta a Pietro, diventa una domanda della fase 3 e non si inventa.
- Scrivere **`modello-di-livello.md`**: lo schema unico di un livello (componenti, flusso, esercizi, soglia, premio, ripasso, visioni, dati), che vale come lista di controllo per i 150 livelli.
- Aggiornare `curricolo` (che non ha il registro delle modifiche) e `tappa-1-01` (che indica come implementazione un file che non esiste).

### Fase 3 · Le decisioni di Pietro

Le quattro bloccanti, le quindici importanti e le domande nate nella fase 2, ognuna con opzioni, conseguenze e una raccomandazione. Prima quelle che toccano l'anno 1 e il modello di livello, e la B1, che decide la forma di ogni tappa.

### Fase 4 · Colmare i buchi di contenuto

In ordine di vicinanza al gioco:

1. **Anno 1**: coordinate delle tappe 27 e 30, la tappa 1-30 affidata a «La città» (P93), le schede complete delle 30 tappe secondo il modello di livello.
2. **Correzioni già decise e mai applicate** (`luoghi.md` §3): il pin di Mansa Musa (Cairo, non Timbuctù) e Marconi (Pontecchio, non Bologna).
3. **Verifiche storiche aperte**, a partire dalla V1 sul decreto del 1510 (`anno3-europa.md` §12).
4. **Dati degli anni 2–4 in `dati/`** e catalogo esteso dei facoltativi: si possono rimandare, non servono per l'anno 1.

### Fase 5 · Rifinitura e README

Un README breve (che cos'è, come si gioca, mappa dei documenti, stato), i numeri contraddittori corretti (per esempio 59 e 67 controlli senza prova nella stessa pagina), i refusi, i rimandi incrociati.

### Fase 6 · Collaudo di portabilità

Tutti i verificatori verdi, e una prova a freddo: un agente senza contesto legge solo la documentazione e deve specificare la tappa 1-2. Dove sbaglia o deve indovinare, c'è un buco.

## 3. Linea di base (fase 0, 06/10/2026)

Su 35 verificatori, **34 sono verdi** e **uno esce con il codice 2**, che vuol dire «non eseguito, e lo dico»: è `verifica_tavolozza.py`, il cui controllo A4 rilegge i colori su Wikidata e Wikipedia, e la macchina su cui è stata fatta la fase 0 non raggiunge quei siti. Con `--offline` i suoi altri cinque controlli sono verdi, e la prova del difetto ne vede sei su sei. A4 va rifatto da una macchina con la rete.

I quattro rossi del 06/10/2026 e che cosa erano:

| Verificatore | Che cosa era | Che cosa è stato fatto |
|---|---|---|
| `verifica_coerenza.py` | Il controllo «file pubblicati» leggeva gli elenchi di `_commit_coerenza.py`, uno script di pubblicazione locale di una sessione precedente che non è mai entrato nel repository | Da quando si pubblica con git, l'elenco dei pubblicabili è `git ls-files`: un file che git non traccia non arriva nel ramo. La prova con un file non tracciato in `docs/` lo vede |
| `lingue/verifica_metadati_mancanti.py` | M1 confrontava i 4 candidati respinti oggi con i 5 esiti registrati il 05/10: il quinto, `Red wine cap.jpg`, era un rifiuto nostro chiuso leggendo la chiave `Attribution`, e da allora ha l'autore | M1 confronta gli insiemi: ogni respinto di oggi ha un esito, e un esito che non è più respinto deve essere un rifiuto nostro. Le due prove (un esito tolto, una classe falsa) sono viste |
| `lingue/verifica_immagini_oggetti.py` | Dal 05/10 i 7 candidati troppo piccoli, che il capitolo dichiara respinti per merito, erano contati fra i problemi: il verificatore era rosso per sempre | Uno scarto per merito è un esito elencato e contato (G8); uno scarto per fonte resta un problema |
| `verifica_tavolozza.py` | Senza rete verso Wikidata restava appeso per ore (cinque tentativi da 60 s per ogni voce) | Una sola prova di raggiungibilità prima di A4: se la fonte non risponde, lo dice subito ed esce con 2 |

## 4. Bilancio della fase 1 (06/10/2026)

**Che cosa è fatto.**

- **Ogni documento dichiara il suo tipo** (`tipo:` nell'intestazione): `normativo`, `catalogo`, `audit`, `storico`, `piano`. `verifica_coerenza.py` lo controlla («tipi dei documenti»).
- **Lo storico esiste** (`storico.md`) e contiene, alla lettera e con la provenienza, il racconto tolto da nove documenti e da `AGENTS.md`. Nei documenti d'origine resta la regola o lo stato di oggi. Un controllo riga per riga ha confermato, a ogni spostamento, che nessuna riga si è persa.
- **L'audit è in ordine**: §0–§6 come prima, §7 «Le questioni chiuse» con esito e posto di ogni chiusura, §8 il registro. Da 120 585 a 63 744 caratteri.
- **Le regole di metodo sono in `metodo.md`**, al presente e ciascuna con il controllo che la fa rispettare. `AGENTS.md` le richiama e torna a decisioni, convenzioni e procedura.
- **Due strumenti nuovi**: `sorgenti/nuova_versione.py` (versione, registro, README e rimandi in un colpo) e `sorgenti/allinea_conti_readme.py` (i conti del README dai verificatori, non a mano). E una regola nuova: aggiornare un rimando di versione non alza la versione di chi lo contiene.
- **Tre errori di fatto corretti in `AGENTS.md`**: l'errore del rilievo (32,9 m su 32 punti, non 12,6 m su 14), un'etichetta illeggibile, un rimando a una sezione che non esiste più.

**Che cosa la fase 1 lascia, e dove va.**

| Che cosa | Perché non ora | Dove va |
|---|---|---|
| Paragrafi di racconto **dentro** sezioni normative (non sezioni intere) | Toglierli senza riscrivere la sezione lascerebbe frasi monche | Fase 2 per il nucleo di gioco, fase 5 per gli altri documenti, quando ogni documento viene riscritto |
| I registri delle modifiche molto lunghi (`fonti-visive`, `mappe`, `luoghi-edifici`, `ritratti`) | Sono storia per costruzione, stanno in fondo e sono esclusi dai confronti | Restano dove sono |
| Le «Note» del `README.md` | Il README si riscrive per intero | Fase 5 |
| `AGENTS.md` §3 mescola decisioni di Pietro e istruzioni operative datate | Separarle richiede di decidere, per ognuna, se è ancora valida: è il lavoro della fase 2 | Fase 2 |
| `lingue-immagini.md` §5 e `luoghi-edifici.md` §2 hanno titoli da racconto | Il contenuto è normativo, e i numeri sono letti dai controlli | Fase 5, solo il titolo |

## 5. Bilancio della fase 2 (07/10/2026)

**Che cosa è fatto.**

- **`modello-di-livello.md` esiste**: le quindici parti di un livello con la fonte di ognuna, il flusso della tappa, i numeri della bottega e della soglia, i tipi di livello e gli anni, e la **lista di controllo** con cui si riscrive la tappa 1-1. Lo tiene fermo un verificatore nuovo, `verifica_modello.py` (K1–K4), con la prova del difetto.
- **Dodici contraddizioni fra il nucleo di gioco e i documenti successivi**: sette risolte e scritte nel §8 del modello, cinque diventate domande (§9 del modello), di cui tre importanti nell'audit (I20–I22); la dodicesima è B1. `gioco`, `esercizi`, `meccaniche`, `inventario`, `tappa-1-01`, `curricolo` e `motore-e-grafica` sono allineati e rimandano al modello.
- **`AGENTS.md` §3 è diviso** in decisioni di Pietro (§3.1) e regole per tema (§3.2). Tre decisioni scritte come questioni aperte erano chiuse dal 02/10/2026 (il Novecento nell'anno 3, `S66` e il presente nell'anno 4) e ora dicono la decisione. Lo stato delle questioni non si scrive più lì ma solo nell'audit.
- **`prova_difetto_questioni.py` non ha più numeri scritti dentro**: li legge dall'audit, e una nuova sezione di questioni non la rompe più.

**Che cosa la fase 2 lascia, e dove va.**

| Che cosa | Dove va |
|---|---|
| Le cinque domande del modello e le altre bloccanti e importanti | Fase 3: è la lista da portare a Pietro, in ordine: B1, poi I20–I22, poi le due del §4 dell'audit sul modello |
| La riscrittura completa di `gioco.md` ed `esercizi.md` al presente, togliendo le parti che il modello ormai dice meglio | Dopo la fase 3: senza le risposte, riscriverle significherebbe decidere al posto di Pietro |
| I paragrafi di racconto rimasti dentro le sezioni normative degli altri documenti | Fase 5 |

## 6. Fase 3: le decisioni (chiusa l'08/10/2026)

**Decise da Pietro il 07/10/2026**, e scritte nei documenti:

| Domanda | Decisione | Dove è scritta |
|---|---|---|
| B1 · livelli linguistici e informatici | Sette livelli per tappa: informatica e sei lingue, ognuno con la sua soglia, tutti da fare | `lingue.md` Q1, `modello-di-livello.md` §0–§2, `audit.md` §2 e §7 |
| I20 · carta e premio | Tutti e due; carta e visioni entrano nell'inventario, la collezione delle carte è il quinto registro | `modello-di-livello.md` §9, `inventario.md` §1 e §3 |
| Ripasso a distanza e test di ingresso | Tutti e due: il ripasso Leitner è obbligatorio nella soglia, i test sono facoltativi | `modello-di-livello.md` §9, `gioco.md` |
| I22 · risposte scritte | Testo libero ammesso, valutato dal docente; per la soglia solo risposte che il gioco corregge da solo | `modello-di-livello.md` §3, `esercizi.md`, `meccaniche.md` |

**Decise da Pietro nel pomeriggio del 07/10/2026**:

| Domanda | Decisione | Dove è scritta |
|---|---|---|
| I23 · che cosa apre la tappa successiva | La soglia di informatica; il livello *n* di una lingua richiede tutti i premi precedenti di quella lingua; si può tornare indietro, con un espediente narrativo per anno | `lingue.md` Q10, `modello-di-livello.md` §2 |
| I24 · ordine dei sette livelli | Nessun ordine: ingressi sparsi nell'ambiente, segnati da frecce di sette colori, accanto a chicche interattive brevi che intrattengono | `lingue.md` Q11, `modello-di-livello.md` §1–§2 |
| Modalità e processi di pensiero | Entrano nella scheda, non si possono saltare, e il giocatore deve capire perché li fa | `modello-di-livello.md` §9 Q5 |

**Decise da Pietro la sera del 07/10/2026**: la proposta Q6 su processi di pensiero e modalità, con 5 livelli su 30 a coppie o di gruppo per ciascuno dei sette ambiti, anche in informatica; l'abolizione delle prove di corte (I21).

**Approvate da Pietro la sera del 07/10/2026**: le cinque proposte di espediente narrativo (I25) e la tappa a mani nude in concreto (Q8). 

**Decise da Pietro la sera del 07/10/2026**, e con loro la fase 3 si chiude quasi tutta: B3 (LIS da materiali online, comunità dopo l'anno 1), B4 (le immagini le sceglie Pietro con uno strumento del progetto), e tredici importanti — il percorso segue le tappe con un senso narrativo (I1), il testo autentico (I5), il greco (I6), il modulo con Niccolò III (I7), il conto degli esercizi (I8), le fonti del latino e del greco (I9), le Nuove Indicazioni (I11), il 1945 e la biologia come facoltativi (I13, I14), la tratta (I15), i ritorni come risorsa (I16), il `.txt` con firma (I17), il prodotto a sé (I18). I10 e I12 sono rinviate con il motivo. Principio di Pietro: **ora si decide l'ossatura; i dettagli si esplorano livello per livello.**

**Chiusa l'08/10/2026 con B2.** Pietro ha rivisto le voci: confermato ciò che non ha commentato, le segnalazioni le ha risolte il progetto, e l'italiano ha un piatto tipico per ogni tappa. Nella stessa revisione due regole nuove: i fatti interessanti si segnalano, e un personaggio citato e non ancora incontrato diventa una scheda interattiva con un'immagine (`modello-di-livello.md` §5). **La fase 3 è chiusa**, e si passa alla fase 4.

**Dove si riprende (08/10/2026, mattina).** Lo strumento di scelta delle immagini (B4) è scritto (`sorgenti/lingue/scelta/`) ma non ancora pubblicato. Le miniature sono scaricate per greco e inglese, l'italiano a 841 su 1007, la LIS in corso, il latino da fare: stanno nella cartella `Progetti/i-cinque-duchi-miniature` del computer di Pietro e in `verifica/miniature/` dell'ambiente di lavoro (fuori dal ramo, si rigenerano). Per finire: completare le miniature (`miniature_parallelo.py` sul computer di Pietro, `miniature.py` qui, a 2,5 secondi per file); **dividere l'italiano per anno**, perché il suo file supera i 16 MB che una pagina pubblicata accetta per file; generare la pagina (`genera_pagina.py`), pubblicarla con le miniature accanto, e dare il link a Pietro. Poi riportare le scelte in `dati/lingue/attestazione_oggetti.json`.

**Lavoro per la fase 4 nato da queste decisioni**: raccogliere i proverbi ferraresi da fonti pubblicate, perché Pietro li riveda; lo strumento per scegliere le immagini, con le miniature scaricate da una macchina che raggiunge Commons; acquisire le Nuove Indicazioni 2026 e rifare la verifica di copertura; scrivere per ogni anno il senso narrativo del percorso; le facoltative del 1945 e della biologia nell'anno 5 e la scheda d'atlante sul colonialismo nell'anno 3; il modulo con Niccolò III, dopo l'anno 1.

**Lavoro per la fase 4 nato da queste decisioni**, senza altre domande: riscrivere i 15 livelli ex prova di corte come livelli normali con un argomento proprio (`schema-livelli.md` §6); scegliere in ogni anno i 5 livelli su 30 a coppie o di gruppo per ciascun ambito; scegliere i sette colori delle frecce dalla tavolozza; scrivere i campi `processi` e `modalità` nella scheda di ogni livello.

## 7. Registro delle modifiche

| Data | Versione | Modifica |
|---|---|---|
| 06/10/2026 | 0.1 | Prima stesura: diagnosi e sei fasi, approvate da Pietro. Fase 0 avviata. |
| 06/10/2026 | 0.2 | Fase 0 chiusa: linea di base (§3), quattro verificatori rossi riportati a verde o dichiarati. |
| 06/10/2026 | 0.3 | Fase 1 chiusa: il bilancio (§4) dice che cosa è fatto e che cosa la fase lascia alle fasi successive, con il perché. |
| 07/10/2026 | 0.4 | Fase 2 chiusa: il bilancio (§5) dice che cosa è fatto e che cosa resta per le fasi successive. |
| 07/10/2026 | 0.5 | Fase 3 in corso: le quattro decisioni di Pietro del 07/10/2026, le due domande nate da B1 e l'ordine delle prossime (§6). |
| 07/10/2026 | 0.6 | Fase 3: le decisioni del pomeriggio del 07/10/2026 (I23, I24, modalità e processi) e il nuovo ordine delle domande. |
| 07/10/2026 | 0.7 | Fase 3: le decisioni della sera del 07/10/2026, le due proposte da approvare e il lavoro che ne viene per la fase 4. |
| 07/10/2026 | 0.8 | Approvate le due proposte; restano B2, B3, B4 e le quindici importanti per chiudere la fase 3. |
| 07/10/2026 | 0.9 | Fase 3 quasi chiusa: le decisioni della sera del 07/10/2026, resta B2; il lavoro per la fase 4. |
| 08/10/2026 | 0.10 | Fase 3 chiusa l'08/10/2026 con B2; le due regole nuove della revisione (curiosità, personaggi citati). |
