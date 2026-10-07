---
titolo: Videogioco "I cinque duchi" — Il modello di livello: le parti di un livello, il loro ordine, le regole e la lista di controllo
tipo: normativo
versione: 0.2
data: 2026-10-07
autore: Pietro Fabbri (con Claude)
controllo: python3 sorgenti/verifica_modello.py (K1-K4: NEED e POOL contro il codice degli esercizi, i tipi di livello contro i dati, le parti numerate e i documenti che citano, il numero delle domande)
documenti collegati: videogioco-5-duchi-schema-livelli.md (v1.1), videogioco-5-duchi-gioco.md (v0.7), videogioco-5-duchi-esercizi.md (v0.3), videogioco-5-duchi-meccaniche.md (v0.5), videogioco-5-duchi-tappa-1-01.md (v0.6), videogioco-5-duchi-premi.md (v0.9), videogioco-5-duchi-inventario.md (v0.4), videogioco-5-duchi-ripassi.md (v0.4), videogioco-5-duchi-pedagogia.md (v0.2), videogioco-5-duchi-quadro-trasversale.md (v0.2), videogioco-5-duchi-lingue.md (v0.3), videogioco-5-duchi-audit.md (v0.29)
---

# Il modello di livello

## 0. A che cosa serve, e che cosa copre

Questo documento dice **di che cosa è fatto un livello** del gioco, in che ordine il giocatore ne attraversa le parti, quali numeri lo regolano e quando un livello si può dire pronto. È la lista di controllo con cui si scrivono, o si riscrivono, i 150 livelli. Il primo a essere riscritto con questo modello è la tappa 1-1.

**Che cosa copre.** Il **livello informatico** (`schema-livelli.md`, 150 livelli), nella forma completa dell'anno 1, e che cosa cambia negli anni 2–5 (§6). Il **livello linguistico** ha la sua anatomia in `lingue.md` §2 (nove componenti). **Una tappa contiene sette livelli**: quello di informatica e uno per ciascuna delle sei lingue, ognuno con la propria soglia, e il ragazzo li fa tutti (decisione di Pietro del 07/10/2026, `lingue.md` Q1). Che cosa apre la tappa successiva e in che ordine si fanno i sette livelli sono ancora da decidere (`lingue.md` Q10 e Q11).

**Come si legge.** Ogni regola dice da quale documento viene. Le regole di dettaglio restano nei documenti d'origine: qui ci sono le regole che servono per costruire un livello, con il rimando. Dove due documenti si contraddicevano, qui c'è la regola che vale e il §8 dice perché. Dove la scelta spetta a Pietro, la regola è indicata come **provvisoria** e la domanda è nel §9.

## 1. Le parti di un livello

| # | Parte | Che cosa è | Obbligatoria? | Dove si specifica |
|---|---|---|---|---|
| 1 | **Scheda del livello** | Identità e contenuti: `id`, titolo, tipo, nucleo, ripresa, prerequisiti integrati, prerequisiti di altre discipline, nota didattica, due approfondimenti | sì | `schema-livelli.md` §1, `dati/videogioco-5-duchi-livelli.json` |
| 2 | **Tappa** | Il luogo (pin), il personaggio obbligatorio (la voce), la zona percorribile, l'aggancio fra personaggio e argomento | sì | anno 1: `anno1-mappa.md` §2; luoghi: `luoghi.md`; zona: `motore-e-grafica.md` §2 |
| 3 | **Scheda di contesto** | Linea del tempo, tre righe (dove, quando, che cosa succede intorno), chi viene prima e dopo nel tempo, etichetta di attendibilità con la sua frase | sì | `gioco.md` §5 |
| 4 | **Incontro** | Il personaggio parla di sé e della sua epoca, in prima persona, e propone la bottega | sì | `gioco.md` §3.5, `esercizi.md` §3–§4 |
| 5 | **Ripasso a distanza** | 2–4 domande sulle carte delle tappe precedenti il cui intervallo è scaduto, prima della bottega | sì (decisione del 07/10/2026, §9 Q2) | `gioco.md` §4.2 |
| 6 | **Bottega** | Gli esercizi, in quattro gradini con pool casuali | sì | `esercizi.md` §1–§2, §3 qui |
| 7 | **Soglia** | La condizione per proseguire | sì | §3 qui |
| 8 | **Pausa di autoregolazione** | Il cerchio che respira dopo due errori consecutivi | sì (scatta da sola) | `gioco.md` §3.6, `quadro-trasversale.md` §2.2 |
| 9 | **Carta del personaggio** | Ritratto o emblema, motto, concetto, etichetta; entra nella collezione e nel ripasso | sì (decisione del 07/10/2026, §9 Q1) | `gioco.md` §3.1, §4.3; `inventario.md` §1 |
| 10 | **Premio** | Un oggetto vero con tre righe (`chi`, `cosa`, `riflessione`), che va nella salvadanaio | sì, uno per livello | `premi.md` §3–§4 |
| 11 | **Rimando** | La battuta che indica la tappa successiva; si sente solo dopo la soglia | sì | `anno1-mappa.md` §2 |
| 12 | **Visioni** | I due approfondimenti del livello, uno dopo l'altro, con un personaggio facoltativo | no | `gioco.md` §3.4 |
| 13 | **Chicche** | Oggetti da guardare nella zona; al massimo una porta l'aggancio trasversale | no | `quadro-trasversale.md` §2.2 |
| 14 | **Livelli linguistici, oggetto di interazione e test di ingresso** | I sei livelli linguistici della tappa, uno per lingua, ciascuno con le sue nove componenti e la sua soglia; in ciascuno la voce dell'oggetto e le dieci domande del test di ingresso | i sei livelli sì; l'oggetto e il test no | `lingue.md` §2, Q1; `inventario.md` §1; `ripassi.md`. L'ordine nella tappa e che cosa apre la tappa successiva: `lingue.md` Q10, Q11 |
| 15 | **Registrazione** | Che cosa del livello finisce nel file di consegna | sì (automatica) | `meccaniche.md` §1, §4 qui |

**Due cose che non sono parti del livello.** Il **viaggio** (pin, strada e mezzo, `percorsi.md`) è il passaggio da una tappa all'altra, non un pezzo della tappa. La **fascia bianca** (`inventario.md` §1, elemento 7) esiste solo nel quinto anno, alla tappa 5-30 (`anno5-mondo.md` §7.3).

## 2. Il flusso di una tappa (anno 1)

```text
MAPPA ─▶ ENTRA ─▶ CONTESTO ─▶ INCONTRO ─▶ RIPASSO ─▶ BOTTEGA ───────────────▶ SOGLIA ─▶ CARTA e PREMIO ─▶ RIMANDO ─▶ USCITA ─▶ MAPPA
 (zona)  (zona     (scheda)    (dialogo)   (2-4      gradino 0 ▸ 1 ▸ 2 ▸ 3       (§3)                         (battuta)   (freccia
          a piedi)                          domande)   └ pausa dopo 2 errori ┘                                              sul confine)
                                                                                    └── dopo la soglia: VISIONE A1 ─▶ VISIONE A2
                                                                                        chicche: sempre, mai valutate
```

1. **Mappa.** La città con la nebbia; la tappa aperta ha il suo pulsante «Entra» (`anno1-mappa.md` §4bis).
2. **Zona.** Borso si muove a piedi nella cella di Voronoi della tappa, entro 150 m. Un riquadro giallo indica il personaggio da cercare; la «A» compare entro 2,3 m da ciò con cui si può parlare (`tappa-1-01.md` §3).
3. **Contesto e incontro.** La scheda di contesto, poi le battute del personaggio, che termina con la proposta: sì apre la bottega, no la rimanda.
4. **Ripasso.** Dalla seconda tappa in poi, le domande sulle carte in scadenza, al massimo sei per sessione (`gioco.md` §4.2).
5. **Bottega**, fino alla soglia (§3).
6. **Carta e premio**, poi il **rimando**. Dopo la soglia si apre l'uscita verso la tappa successiva e compaiono le visioni.
7. **Visioni.** A1 si apre dopo la soglia, A2 dopo A1. Non servono per proseguire e restano disponibili anche dopo.

Il flusso disegnato qui è quello del **livello informatico**. Nella stessa tappa ci sono i **sei livelli linguistici** (§1, parte 14); dove si collocano rispetto a questo flusso, e se la tappa successiva si apre prima che siano finiti, è `lingue.md` Q10 e Q11.
8. **Uscita.** Attraversando il confine nel punto segnato si torna alla mappa, dove la tappa successiva compare come «?».

## 3. La bottega e la soglia: i numeri

| Regola | Valore | Fonte |
|---|---|---|
| Gradini | **0** esempio animato (3–4 schermate, senza valutazione) · **1** Riconosci (una decisione) · **2** Trasforma (il concetto applicato a un caso) · **3** Collega (più passaggi, si misura la coerenza) | `esercizi.md` §1 |
| Esercizi giusti per superare un gradino (`NEED`) | **4** | `esercizi.md` §1 |
| Pool di ogni gradino (`POOL`) | **5 × NEED = 20** esercizi equivalenti, estratti a caso senza ripetizioni; nessun contenuto ripetuto nella pool; seme diverso per studente e per rigenerazione | `esercizi.md` §1 |
| Quando un esercizio conta | gradini 1 e 2: se è giusto; gradino 3: se l'esito è giusto (E = 1) **e** la coerenza dei passaggi è almeno 0,7 | `tappa-1-01.md` §5 |
| **Soglia del livello** | **4 esercizi validi al gradino 3** | `tappa-1-01.md` §5 |
| Soglia di una prova | **5 esercizi validi al gradino 3**, **provvisoria** (§9 Q3) | `meccaniche.md` §2.3 |
| Errori | due errori consecutivi aprono la pausa (il pulsante per ripartire si attiva dopo 4 s); nei gradini 2 e 3, dopo la pausa si torna al gradino precedente con un'istanza nuova | `esercizi.md` §1, `tappa-1-01.md` §5 |
| Risposte troppo veloci | al gradino 3, una risposta in meno di 6 s è segnalata nel report, senza penalità | `tappa-1-01.md` §5 |
| Punteggio dell'istanza | indice di processo P = 0,50·C + 0,20·f(A) + 0,15·g(H) + 0,15·h(T); punti = difficoltà × E × P. Pesi da tarare sul prototipo | `meccaniche.md` §2.3 |
| Tasso di successo atteso | circa 80–85% | `gioco.md` §2.4 |

**Meccanismi.** Si usano con il tocco o il clic, senza trascinamenti obbligatori, così funzionano anche sul telefono. In una tappa nessun meccanismo compare più di due volte di fila, e ogni tappa introduce almeno un meccanismo nuovo rispetto alla precedente. Il catalogo è in `esercizi.md` §2. **Il principio «prevedi prima di vedere»** vale ovunque si possa: il giocatore si impegna su una previsione prima che il gioco mostri il risultato, e la previsione entra nella coerenza (`meccaniche.md` §2.1).

**Risposte** (decisione di Pietro del 07/10/2026, §9 Q4). Le risposte possono essere anche **in testo libero**. Il testo libero non lo valuta il gioco: finisce nel file di consegna e lo **valuta il docente**, nel report. Codice, formule e comandi si scrivono e il gioco li verifica **eseguendoli** sui dati generati per quello studente (`gioco.md` §2.2). I meccanismi a scelta, ordine, collegamento e manipolazione (`esercizi.md` §2) restano la forma della bottega dove il gioco deve sapere da solo se la risposta è giusta, cioè sempre per la soglia.

**Il quinto gradino.** Il trasferimento dello stesso concetto in un contesto diverso, che `gioco.md` §2.4 chiamava quinto gradino, non è un gradino della bottega: sta negli approfondimenti, cioè nelle visioni.

## 4. Che cosa resta al giocatore e al docente

| Che cosa | Dove va | Fonte |
|---|---|---|
| La carta del personaggio, al livello bronzo, con il primo ripasso il giorno dopo | collezione e ripasso a distanza | `gioco.md` §3.1, §4.2 |
| Il premio, con le tre righe | salvadanaio | `premi.md` §4.1–§4.2 |
| Stato, punti, indice di processo, tempo, tentativi, errori, suggerimenti del livello | file di consegna, dettaglio per livello | `meccaniche.md` §1.2–§1.3 |
| I semi delle istanze affrontate | file di consegna (per rigenerarle in classe) | `meccaniche.md` §2.2, §2.5 |
| Le risposte in testo libero, con la consegna a cui rispondono | file di consegna, per la valutazione del docente; il gioco non le valuta | §3 qui |
| Gli indicatori da guardare (esito giusto con coerenza bassa, tempi implausibili) | file di consegna, come spunti per un colloquio e mai come sanzioni | `meccaniche.md` §2.4 |

## 5. Testo, linguaggio, grafica

**Quantità di testo** (`esercizi.md` §3), per anno:

| Anno | Battute per scena | Parole per battuta | Parole per consegna | Scena più lunga |
|---|---|---|---|---|
| 1 | ≤ 4 | ≤ 18 | ≤ 10 | ≈ 60 parole |
| 2 | ≤ 5 | ≤ 25 | ≤ 15 | ≈ 100 parole |
| 3 | ≤ 6 | ≤ 35 | ≤ 20 | ≈ 180 parole |
| 4 | ≤ 7 | ≤ 45 | ≤ 25 | ≈ 300 parole |
| 5 | libero, a pagine | ≤ 60 | ≤ 30 | ≈ 500 parole |

**Linguaggio** (`esercizi.md` §4): frasi corte, un'idea per frase, «tu», niente tono infantile; conferme sobrie («Sì.», «Esatto.»); «Non ancora» invece di «Sbagliato», con la soluzione giusta in verde; termini tecnici spiegati la prima volta con un esempio. **I personaggi parlano solo di sé e della propria epoca**, mai di Borso. Gli articoli della Costituzione si citano alla lettera, con il numero (`quadro-trasversale.md` §2.2).

**Grafica** (`motore-e-grafica.md`): vista dall'alto in 3/4; 1 tessera = 1,25 m = 16 px; figure 16 × 24 px; ritratti 48 × 54 px nei dialoghi. Una persona ha un **ritratto autentico** se esiste un'immagine libera che la ritrae davvero, altrimenti un **emblema**: mai un volto inventato (`ritratti.md` §1). Le visioni hanno il tono seppia. Colori dei livelli del sapere nell'anno 1: dato arancio, informazione blu, conoscenza verde, saggezza viola (`esercizi.md` §5).

**Misure contro la copia** (`meccaniche.md` §2.6.2, `tappa-1-01.md` §7): selezione, copia e menu contestuale disattivati; filigrana con nome, istanza e ora; istanze diverse per studente e per tentativo; un passo visibile alla volta.

## 6. I tipi di livello, e che cosa cambia negli anni

**Tipi** (`dati/videogioco-5-duchi-livelli.json`, campo `tipo`):

| Tipo | Quanti | Che cosa cambia |
|---|---|---|
| `normale` | 135 | il modello di questo documento |
| `prova` (prova di corte) | 15: x-10, x-20, x-30 di ogni anno | integra i livelli precedenti; alcune hanno anche un argomento nuovo (`schema-livelli.md` §6); soglia più alta (§3); nell'anno 1 ogni prova è anche il momento di «ripercorrere la strada» (`gioco.md` §4.3) |
| tappa **a mani nude** | 10: x-15 e x-30 (`pedagogia.md` §3) | due o tre minuti, nessun aiuto, nessuno strumento; si riparte senza penalità. **Non è ancora nei dati**, e il suo rapporto con le prove è la domanda §9 Q3 |

**Gli anni.** Il modello vale per tutti e cinque gli anni; cambiano il protagonista, il luogo che si attraversa e il modo in cui la tappa arriva:

| Anno | Chi gioca | Che cosa si attraversa | Che cos'è una tappa | Dove si legge |
|---|---|---|---|---|
| 1 | Borso | Ferrara dentro le mura, a piedi | un luogo con il suo personaggio | `anno1-mappa.md` |
| 2 | Ercole I | la carta d'Italia a strati | un pin letto a una certa profondità; chi agisce fuori dalla penisola entra da una porta | `anno2-penisola.md` §0.1 |
| 3 | il giocatore; Alfonso I è la guida | la corte di Ferrara | una risorsa che arriva sulla tavola | `anno3-europa.md` §0.1 |
| 4 | il giocatore; Ercole II commenta | l'archivio della corte | un documento da catalogare, che lascia una riga nel registro | `anno4-mondo.md` §0.2, §7 |
| 5 | il giocatore; Alfonso II guida | il cantiere dell'Addizione Erculea, nel tempo | un numero con il suo errore; la stanza del *Furioso* | `anno5-mondo.md` §0.2, `furioso.md` §2 |

## 7. Lista di controllo: quando un livello è pronto

Un livello è pronto quando **tutte** queste cose sono vere. Le prime sette sono di contenuto, le altre di costruzione.

1. La scheda del livello (§1, parte 1) è completa in `dati/videogioco-5-duchi-livelli.json` e combacia con `schema-livelli.md`.
2. Luogo, personaggio e aggancio sono quelli della tabella delle tappe dell'anno, e il luogo ha superato la regola di `luoghi.md` (tipo di legame dichiarato).
3. I fatti storici usati sono verificati, e i dubbi sono scritti nella scheda del personaggio (`note_verifica`).
4. Il dialogo del personaggio rispetta i limiti di testo dell'anno e parla solo di sé.
5. Gli obiettivi di apprendimento sono scritti, al massimo tre, ciascuno verificabile da almeno un gradino.
6. Esiste una specifica della tappa, un file `docs/videogioco-5-duchi-tappa-<anno>-<NN>.md` per livello, con le sezioni della tappa 1-1 (`tappa-1-01.md`): scheda, obiettivi, zona, incontro, bottega, soglia, visioni, misure contro la copia, report.
7. Il premio è scelto e supera le quattro prove (`premi.md` §3), con le tre righe scritte.
8. Ogni gradino ha i suoi generatori, e una pool di 20 senza ripetizioni (lo controlla `buildPool`).
9. I meccanismi rispettano la regola di varietà (§3), e almeno uno è nuovo rispetto alla tappa precedente.
10. Le due visioni sono costruite e corrispondono ai due approfondimenti della scheda.
11. Le immagini usate (ritratti, emblemi, sprite) sono dichiarate, con licenza e fonte, e passano i controlli (`art/verifica_immagini.py`, `verifica_ambienti.py`).
12. Il prototipo è rigenerato (`sorgenti/build_mappa_html.py`) e un test automatico in `sorgenti/test/` gioca la tappa dall'inizio alla fine senza errori.
13. Tutti i verificatori sono verdi (`metodo.md` §4).

## 8. Da dove vengono le regole: le contraddizioni risolte

Il 07/10/2026 il nucleo di gioco e i documenti scritti dopo si contraddicevano in dodici punti. La regola del progetto è che **vale il documento più recente** (`AGENTS.md` §2), e così sono stati risolti i primi sei; il settimo non era una contraddizione fra documenti ma un errore interno. Gli altri cinque sono domande per Pietro (§9), e la dodicesima è B1.

| # | Che cosa | I due documenti | Che cosa vale |
|---|---|---|---|
| 1 | Gradini della bottega | `gioco.md` §2.4 (28/09: cinque gradini, dall'esempio svolto al trasferimento) e `esercizi.md` §1 (30/09: gradini 0–3) | i gradini 0–3 di `esercizi.md`, che sono anche quelli costruiti; il trasferimento va negli approfondimenti, come `gioco.md` stesso diceva |
| 2 | Soglia | `curricolo.md` §3.1 (27/09) e `meccaniche.md` §2.3 (28/09): *k* = 3 istanze consecutive; `esercizi.md` §1 (30/09) e `tappa-1-01.md` §5: 4 esercizi validi al gradino 3 | 4 esercizi validi al gradino 3 (§3) |
| 3 | Misura del ritratto sulla carta | `gioco.md` §3.1 (48 × 48) e `motore-e-grafica.md`, `ritratti.md` (48 × 54) | 48 × 54 |
| 4 | Misura delle figure nella zona | `esercizi.md` §5 (12 × 16) e `motore-e-grafica.md` §0 (16 × 24), con gli sprite della tappa 1-1 | 16 × 24, che è la misura dei file |
| 5 | Premi dell'informatica | `inventario.md` §4 (03/10: «uno per livello, meno l'informatica») e `premi.md` §4.0 con `AGENTS.md` (04/10: l'informatica ha un premio per tappa) | un premio per ogni livello, informatica compresa: 1050 |
| 6 | La fascia bianca | `inventario.md` §1 (elemento di ogni livello) e `anno5-mondo.md` §7.3 (sei fasce alla tappa 5-30) | la fascia esiste solo nell'anno 5, alla tappa 5-30: `anno5-mondo.md` è il documento che la definisce |
| 7 | Visioni della tappa 1-1 | `tappa-1-01.md` §6 dava posizioni e campi diversi dalla tabella del §3 dello stesso documento e dal codice | valgono la tabella del §3 e il codice: San Giorgio a (3,6; 2,6), la lapide a (−13; 1,6), campi Autore, Data, Luogo, Soggetto |

## 9. Questioni aperte

Sono domande per Pietro, emerse allineando il nucleo di gioco. Fino alla risposta valgono le regole provvisorie indicate. La prima, la terza e la quarta cambiano il gioco, e sono anche nell'audit fra le importanti (`audit.md` §3, I20–I22). Il 07/10/2026 Pietro ha risposto alla prima, alla seconda e alla quarta; restano aperte la terza e la quinta.

1. **La carta del personaggio e il premio: restano tutti e due?** — **chiusa il 07/10/2026: tutti e due.** La carta è il personaggio e regge il ripasso; il premio è l'oggetto del livello. Carta e visioni entrano nell'elenco dell'inventario, e la collezione delle carte è un registro personale (`inventario.md` §1, §3). *La domanda com'era posta:* Il prototipo dà una carta per ogni personaggio incontrato (`gioco.md` §3.1), con il motto e il livello di padronanza per il ripasso. Il 03/10 sono arrivati il premio di ogni livello e la salvadanaio (`premi.md` §4), e l'elenco dei sette elementi dell'inventario (`inventario.md` §1) non nomina né la carta né le visioni. *Provvisorio:* tutti e due. La carta è il personaggio e serve al ripasso; il premio è un oggetto che il personaggio non è, perché la prova 3 vieta che il premio sia già nella storia (`premi.md` §3). *Da decidere:* tenerli entrambi e aggiungere carta e visioni all'inventario, oppure far assorbire la carta dal premio, e allora va deciso su che cosa poggia il ripasso.
2. **Il ripasso all'inizio della tappa resta accanto ai test di ingresso?** — **chiusa il 07/10/2026: tutti e due, con ruoli diversi.** Il ripasso Leitner resta obbligatorio e fa parte della soglia della tappa; i test di ingresso restano facoltativi, per le lingue e gli ambiti trasversali (`ripassi.md` §4). *La domanda com'era posta:* `gioco.md` §4.2 mette 2–4 domande sulle carte in scadenza (Leitner) dentro la soglia di ogni tappa; `ripassi.md` ha introdotto dieci domande facoltative ai punti di interazione, per le lingue e gli ambiti trasversali, e dice che non sono la soglia dei livelli informatici (§4). *Provvisorio:* tutti e due, con ruoli diversi. *Da decidere:* se il ripasso Leitner resta obbligatorio, se diventa facoltativo come i test, o se i test lo sostituiscono.
3. **Prove di corte e tappe a mani nude sono la stessa cosa?** I dati hanno 15 prove (x-10, x-20, x-30); `pedagogia.md` §3 vuole 10 tappe a mani nude (x-15, x-30), che nei dati non ci sono. Coincidono solo alle x-30. *Provvisorio:* sono due cose distinte; la prova ha la soglia di 5 (`meccaniche.md` §2.3) e le tappe a mani nude non sono ancora costruite. *Da decidere:* se la tappa x-15 resta un livello normale con in più la sfida, se diventa un tipo nuovo, o se le due cose si fondono.
4. **«Nessuna risposta scritta» e gli strumenti veri.** — **chiusa il 07/10/2026: si accetta anche il testo libero**, valutato dal docente nel report e non dal gioco; codice, formule e comandi si verificano eseguendoli (§3). La produzione nelle lingue si fa così. *La domanda com'era posta:* `esercizi.md` §2 e `tappa-1-01.md` §7 vietano le risposte scritte, perché si incollerebbero da un'IA; `gioco.md` §2 chiede di scrivere codice Python, formule, comandi di shell, e `lingue.md` §2 chiede esercizi di produzione. *Provvisorio:* il divieto vale per le risposte in testo libero; codice, formule e comandi si scrivono e si verificano eseguendoli sui dati generati per quello studente (`gioco.md` §2.2). *Da decidere:* se è questa la regola, e come si fa la produzione nelle lingue.
5. **Due campi nuovi nella scheda del livello.** `pedagogia.md` §1.4 e §2 propongono `Modalità` (individuale, a coppie, piccolo gruppo) e un catalogo fisso di **processi di pensiero** esercitati. *Da decidere:* se entrano nello schema, prima della riscrittura della tappa 1-1.

## 10. Registro delle modifiche

| Data | Versione | Che cosa è cambiato |
|---|---|---|
| 07/10/2026 | 0.2 | **Tre domande chiuse dalle decisioni di Pietro del 07/10/2026.** Q1: carta e premio restano tutti e due, e carta e visioni entrano nell'inventario. Q2: il ripasso Leitner resta obbligatorio nella soglia, i test di ingresso restano facoltativi. Q4: si accetta anche il testo libero, valutato dal docente nel report; codice, formule e comandi si verificano eseguendoli. E B1: una tappa contiene sette livelli (§0, §1 parte 14, §2). Restano aperte Q3 e Q5. |
| 07/10/2026 | 0.1 | Prima stesura (fase 2 della roadmap): le quindici parti di un livello, il flusso della tappa, i numeri della bottega e della soglia, che cosa resta al giocatore e al docente, testo e grafica, i tipi di livello e gli anni, la lista di controllo, le sette contraddizioni risolte e le cinque domande per Pietro. |
