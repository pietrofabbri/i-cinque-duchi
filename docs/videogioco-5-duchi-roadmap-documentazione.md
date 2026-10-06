---
titolo: Videogioco "I cinque duchi" — Roadmap per la risistemazione della documentazione
versione: 0.1
data: 2026-10-06
autore: Pietro Fabbri (con Claude)
documenti collegati: videogioco-5-duchi-audit.md (v0.25), videogioco-5-duchi-gioco.md (v0.5), videogioco-5-duchi-esercizi.md (v0.1), videogioco-5-duchi-meccaniche.md (v0.3), videogioco-5-duchi-tappa-1-01.md (v0.4)
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
| 0 | Punto di partenza pulito | Tutti i verificatori verdi, o il motivo scritto per cui uno non può esserlo | in corso |
| 1 | Architettura della documentazione | Ogni documento ha un tipo dichiarato; i documenti normativi dicono il presente; lo storico è separato; `AGENTS.md` contiene solo decisioni, convenzioni e procedura | da fare |
| 2 | Allineare il nucleo di gioco e scrivere il modello di livello | Nessuna contraddizione fra `gioco`, `esercizi`, `meccaniche`, `motore-e-grafica`, `ripassi`, `premi`, `inventario`, `pedagogia`; esiste `modello-di-livello.md` | da fare |
| 3 | Le decisioni di Pietro | Ogni domanda bloccante o importante ha una risposta registrata, oppure è dichiarata rinviata con il perché | da fare |
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

## 3. Registro delle modifiche

| Data | Versione | Modifica |
|---|---|---|
| 06/10/2026 | 0.1 | Prima stesura: diagnosi e sei fasi, approvate da Pietro. Fase 0 avviata. |
