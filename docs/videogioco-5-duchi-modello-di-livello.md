---
titolo: Videogioco "I cinque duchi" — Il modello di livello: le parti di un livello, il loro ordine, le regole e la lista di controllo
tipo: normativo
versione: 0.5
data: 2026-10-07
autore: Pietro Fabbri (con Claude)
controllo: python3 sorgenti/verifica_modello.py (K1-K4: NEED e POOL contro il codice degli esercizi, i tipi di livello contro i dati, le parti numerate e i documenti che citano, il numero delle domande)
documenti collegati: videogioco-5-duchi-schema-livelli.md (v1.2), videogioco-5-duchi-gioco.md (v0.9), videogioco-5-duchi-esercizi.md (v0.3), videogioco-5-duchi-meccaniche.md (v0.6), videogioco-5-duchi-tappa-1-01.md (v0.6), videogioco-5-duchi-premi.md (v0.9), videogioco-5-duchi-inventario.md (v0.4), videogioco-5-duchi-ripassi.md (v0.5), videogioco-5-duchi-pedagogia.md (v0.3), videogioco-5-duchi-quadro-trasversale.md (v0.2), videogioco-5-duchi-lingue.md (v0.4), videogioco-5-duchi-audit.md (v0.32)
---

# Il modello di livello

## 0. A che cosa serve, e che cosa copre

Questo documento dice **di che cosa è fatto un livello** del gioco, in che ordine il giocatore ne attraversa le parti, quali numeri lo regolano e quando un livello si può dire pronto. È la lista di controllo con cui si scrivono, o si riscrivono, i 150 livelli. Il primo a essere riscritto con questo modello è la tappa 1-1.

**Che cosa copre.** Il **livello informatico** (`schema-livelli.md`, 150 livelli), nella forma completa dell'anno 1, e che cosa cambia negli anni 2–5 (§6). Il **livello linguistico** ha la sua anatomia in `lingue.md` §2 (nove componenti). **Una tappa contiene sette livelli**: quello di informatica e uno per ciascuna delle sei lingue, ognuno con la propria soglia, e il ragazzo li fa tutti (decisione di Pietro del 07/10/2026, `lingue.md` Q1). **La tappa successiva si apre con la soglia di informatica**; i livelli linguistici hanno una propedeuticità loro, per lingua, e **non hanno un ordine**: sono sparsi nell'ambiente della tappa (decisioni del 07/10/2026, `lingue.md` Q10 e Q11; §2 qui).

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
| 13 | **Chicche** | Elementi interattivi nella zona che non sono livelli: informazioni sul luogo, piccole riflessioni di contorno. **Molto veloci, intelligibili e interattive**: devono intrattenere oltre che portare uno stimolo culturale. Mai valutate; al massimo una porta l'aggancio trasversale | no | `quadro-trasversale.md` §2.2; decisione del 07/10/2026 |
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

Il flusso disegnato qui è quello del **livello informatico**. La tappa intera funziona così (decisioni di Pietro del 07/10/2026, `lingue.md` Q10 e Q11):

- **La tappa è un ambiente con sette ingressi.** Ognuno dei sette livelli — informatica e sei lingue — comincia da un elemento interattivo dell'ambiente, segnato da una **freccia del suo colore** sopra di esso. Il giocatore li fa nell'ordine che vuole.
- **La tappa successiva si apre con la soglia di informatica.** I sei livelli linguistici non la fermano.
- **Ogni lingua ha la sua propedeuticità**: il livello *n* di una lingua si apre solo con **tutti i premi precedenti di quella lingua**. Se una lingua è rimasta indietro, la sua freccia nella tappa nuova dice che cosa manca, e il giocatore può **farsi riportare indietro** alla tappa dove quella lingua si è fermata, se lo desidera. Ogni anno ha un **espediente narrativo** per il ritorno (§9 Q7).
- **Le chicche** stanno nello stesso ambiente, senza freccia di livello (§1, parte 13).
- **I sette colori delle frecce** si prendono dalla tavolozza e devono essere distinguibili fra loro anche per chi ha una discromia (`verifica_tavolozza.py`, A6). *Da fare*: sceglierli e aggiungerli a `dati/fonti_visive/tavolozza.json`.
8. **Uscita.** Attraversando il confine nel punto segnato si torna alla mappa, dove la tappa successiva compare come «?».

## 3. La bottega e la soglia: i numeri

| Regola | Valore | Fonte |
|---|---|---|
| Gradini | **0** esempio animato (3–4 schermate, senza valutazione) · **1** Riconosci (una decisione) · **2** Trasforma (il concetto applicato a un caso) · **3** Collega (più passaggi, si misura la coerenza) | `esercizi.md` §1 |
| Esercizi giusti per superare un gradino (`NEED`) | **4** | `esercizi.md` §1 |
| Pool di ogni gradino (`POOL`) | **5 × NEED = 20** esercizi equivalenti, estratti a caso senza ripetizioni; nessun contenuto ripetuto nella pool; seme diverso per studente e per rigenerazione | `esercizi.md` §1 |
| Quando un esercizio conta | gradini 1 e 2: se è giusto; gradino 3: se l'esito è giusto (E = 1) **e** la coerenza dei passaggi è almeno 0,7 | `tappa-1-01.md` §5 |
| **Soglia del livello** | **4 esercizi validi al gradino 3** | `tappa-1-01.md` §5 |
| Soglia di una prova | **non c'è più**: le prove di corte sono abolite (07/10/2026, §9 Q3) | — |
| Errori | due errori consecutivi aprono la pausa (il pulsante per ripartire si attiva dopo 4 s); nei gradini 2 e 3, dopo la pausa si torna al gradino precedente con un'istanza nuova | `esercizi.md` §1, `tappa-1-01.md` §5 |
| Risposte troppo veloci | al gradino 3, una risposta in meno di 6 s è segnalata nel report, senza penalità | `tappa-1-01.md` §5 |
| Punteggio dell'istanza | indice di processo P = 0,50·C + 0,20·f(A) + 0,15·g(H) + 0,15·h(T); punti = difficoltà × E × P. Pesi da tarare sul prototipo | `meccaniche.md` §2.3 |
| Tasso di successo atteso | circa 80–85% | `gioco.md` §2.4 |

**Meccanismi.** Si usano con il tocco o il clic, senza trascinamenti obbligatori, così funzionano anche sul telefono. In una tappa nessun meccanismo compare più di due volte di fila, e ogni tappa introduce almeno un meccanismo nuovo rispetto alla precedente. Il catalogo è in `esercizi.md` §2. **Il principio «prevedi prima di vedere»** vale ovunque si possa: il giocatore si impegna su una previsione prima che il gioco mostri il risultato, e la previsione entra nella coerenza (`meccaniche.md` §2.1).

**Perché lo fai.** Ogni livello, prima della bottega, dice al giocatore in una riga **a che cosa gli serve**, fuori dal gioco: è il principio di trasparenza di `pedagogia.md` §1, e la condizione perché le parti obbligatorie siano capite e non subite (decisione del 07/10/2026, §9 Q5).

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
| `prova` (prova di corte) — **abolito il 07/10/2026** | 15: x-10, x-20, x-30 di ogni anno | Il tipo non esiste più (§9 Q3). I 15 livelli restano al loro posto, con il loro luogo e il loro personaggio, ma vanno **riscritti come livelli normali con un argomento proprio**: fino ad allora i dati portano ancora `prova`, e questa riga dice quanti sono. È lavoro della fase 4 (`roadmap-documentazione.md`) |
| tappa **a mani nude** | 10: x-15 e x-30 (`pedagogia.md` §3) | Non è un tipo di livello: è **una sfida in più dentro la tappa**, che resta una tappa normale con i suoi sette livelli. Come si fa in concreto è la proposta §9 Q8 |

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

Sono domande per Pietro, emerse allineando il nucleo di gioco. Fino alla risposta valgono le regole provvisorie indicate. La prima, la terza e la quarta cambiano il gioco, e sono anche nell'audit fra le importanti (`audit.md` §3, I20–I22). Il 07/10/2026 Pietro ha risposto alla prima, alla seconda, alla quarta e alla quinta; resta aperta la terza. Le domande nate da quelle risposte sono in §9.1, nella forma `### Q6`: non sono fra le cinque nate dall'allineamento, che il §8 conta.

1. **La carta del personaggio e il premio: restano tutti e due?** — **chiusa il 07/10/2026: tutti e due.** La carta è il personaggio e regge il ripasso; il premio è l'oggetto del livello. Carta e visioni entrano nell'elenco dell'inventario, e la collezione delle carte è un registro personale (`inventario.md` §1, §3). *La domanda com'era posta:* Il prototipo dà una carta per ogni personaggio incontrato (`gioco.md` §3.1), con il motto e il livello di padronanza per il ripasso. Il 03/10 sono arrivati il premio di ogni livello e la salvadanaio (`premi.md` §4), e l'elenco dei sette elementi dell'inventario (`inventario.md` §1) non nomina né la carta né le visioni. *Provvisorio:* tutti e due. La carta è il personaggio e serve al ripasso; il premio è un oggetto che il personaggio non è, perché la prova 3 vieta che il premio sia già nella storia (`premi.md` §3). *Da decidere:* tenerli entrambi e aggiungere carta e visioni all'inventario, oppure far assorbire la carta dal premio, e allora va deciso su che cosa poggia il ripasso.
2. **Il ripasso all'inizio della tappa resta accanto ai test di ingresso?** — **chiusa il 07/10/2026: tutti e due, con ruoli diversi.** Il ripasso Leitner resta obbligatorio e fa parte della soglia della tappa; i test di ingresso restano facoltativi, per le lingue e gli ambiti trasversali (`ripassi.md` §4). *La domanda com'era posta:* `gioco.md` §4.2 mette 2–4 domande sulle carte in scadenza (Leitner) dentro la soglia di ogni tappa; `ripassi.md` ha introdotto dieci domande facoltative ai punti di interazione, per le lingue e gli ambiti trasversali, e dice che non sono la soglia dei livelli informatici (§4). *Provvisorio:* tutti e due, con ruoli diversi. *Da decidere:* se il ripasso Leitner resta obbligatorio, se diventa facoltativo come i test, o se i test lo sostituiscono.
3. **Prove di corte e tappe a mani nude sono la stessa cosa?** — **chiusa il 07/10/2026: le prove di corte sono abolite**, e restano le tappe a mani nude, alle x-15 e x-30 (§6; la proposta concreta è Q8). *La domanda com'era posta:* I dati hanno 15 prove (x-10, x-20, x-30); `pedagogia.md` §3 vuole 10 tappe a mani nude (x-15, x-30), che nei dati non ci sono. Coincidono solo alle x-30. *Provvisorio:* sono due cose distinte; la prova ha la soglia di 5 (`meccaniche.md` §2.3) e le tappe a mani nude non sono ancora costruite. *Da decidere:* se la tappa x-15 resta un livello normale con in più la sfida, se diventa un tipo nuovo, o se le due cose si fondono.
4. **«Nessuna risposta scritta» e gli strumenti veri.** — **chiusa il 07/10/2026: si accetta anche il testo libero**, valutato dal docente nel report e non dal gioco; codice, formule e comandi si verificano eseguendoli (§3). La produzione nelle lingue si fa così. *La domanda com'era posta:* `esercizi.md` §2 e `tappa-1-01.md` §7 vietano le risposte scritte, perché si incollerebbero da un'IA; `gioco.md` §2 chiede di scrivere codice Python, formule, comandi di shell, e `lingue.md` §2 chiede esercizi di produzione. *Provvisorio:* il divieto vale per le risposte in testo libero; codice, formule e comandi si scrivono e si verificano eseguendoli sui dati generati per quello studente (`gioco.md` §2.2). *Da decidere:* se è questa la regola, e come si fa la produzione nelle lingue.
5. **Due campi nuovi nella scheda del livello.** — **chiusa il 07/10/2026: entrano tutti e due**, e in modo pedagogicamente efficace: il giocatore non li può saltare, li deve fare, e deve capire ed essere motivato sul perché. *Come* entrano è la proposta di Q6 qui sotto. *La domanda com'era posta:* `pedagogia.md` §1.4 e §2 propongono `Modalità` (individuale, a coppie, piccolo gruppo) e un catalogo fisso di **processi di pensiero** esercitati. *Da decidere:* se entrano nello schema, prima della riscrittura della tappa 1-1.

### 9.1 Domande nate dalle decisioni del 07/10/2026

### Q6 — Come entrano i processi di pensiero e la modalità — **chiusa il 07/10/2026**

**La decisione di Pietro.** La proposta qui sotto è approvata, con una correzione sulla modalità: **coppie e gruppi ci sono anche in informatica**. In ogni anno, per **ciascuno dei sette ambiti** (informatica e le sei lingue), **5 livelli su 30** si fanno a coppie o in piccolo gruppo; gli altri 25 sono individuali. Il terzo punto della modalità qui sotto (informatica sempre individuale) è quindi **superato**, e vale questo:

- **Il compagno può essere anche a distanza.** Ognuno riceve sul suo dispositivo una parte dei dati, generata dal suo seme, e i due si scambiano un codice breve a voce o per messaggio: il gioco lo verifica senza server. Così un livello a coppie si può fare anche a casa.
- **Un livello di informatica a coppie fa parte della soglia** come gli altri, e quindi la tappa successiva aspetta che sia fatto. Il report dice al docente quali livelli aspettano un compagno.
- **Quali livelli** sono a coppie e di gruppo si sceglie guardando l'obiettivo (un livello di argomentazione sì, uno di esercizio individuale no), mai alle tappe a mani nude, e si scrive nella scheda: è lavoro della fase 4.

*La proposta com'era scritta:*

Pietro ha deciso che i due campi entrano e che il giocatore non li deve poter saltare (Q5). Questa è la proposta di come, da approvare o correggere.

**Processi di pensiero** (il catalogo chiuso di `pedagogia.md` §2: scomporre, astrarre, formulare un modello, distinguere un fatto da una fonte, valutare un'affermazione, riconoscere un pregiudizio, argomentare e confutare, controllare un risultato con un altro metodo):

- **Ogni livello dichiara uno o due processi** nella scheda (campo `processi`), sempre insieme al nucleo e mai al posto suo.
- **Il processo si nomina al giocatore** all'ingresso della bottega, con la riga «perché lo fai» (§3): per esempio, «Qui alleni a *scomporre*: è quello che fai quando un problema è troppo grande per essere risolto tutto insieme».
- **Non si salta, perché conta nella soglia**: al gradino 3 almeno un esercizio chiede di riconoscere il processo usato («come ci sei arrivato?», a scelta, corretta dal gioco), e la risposta entra nella coerenza dei passaggi, che fa parte della soglia (§3).
- **Il passaggio fra domini è esplicito**: quando lo stesso processo torna in un livello linguistico della stessa tappa o di una successiva, il gioco lo dice («hai già scomposto un numero alla Cattedrale: adesso scomponi una frase»). È la regola di `pedagogia.md` §2: un processo compare in almeno due domini, e il passaggio non si lascia al caso.

**Modalità** (`individuale`, `a coppie`, `piccolo gruppo`, `pedagogia.md` §1.4):

- **Ogni livello dichiara la modalità** nella scheda, scelta guardando l'obiettivo: un livello di argomentazione sta in gruppo, un livello di codice no.
- **Un livello a coppie o di gruppo non si può fare da soli**: ogni giocatore riceve sul suo dispositivo una parte diversa dei dati (dal suo seme), e la soluzione richiede di metterle insieme. Il gioco verifica con un codice breve che ciascuno inserisce, senza server.
- **Una tensione da decidere.** A casa un livello a coppie non si può fare, e la tappa successiva si apre con la soglia di informatica. *Proposta*: i livelli di **informatica restano individuali**, e le modalità a coppie e di gruppo si usano nei **livelli linguistici e nelle parti trasversali**, che non fermano il percorso; il report dice al docente quali livelli aspettano un compagno, e in classe si fanno insieme.

### Q7 — L'espediente narrativo per tornare indietro, anno per anno — **chiusa il 07/10/2026: le cinque proposte sono approvate**

Pietro le ha approvate così come sono scritte qui sotto. Prima di metterle nei dati vanno fatte le tre verifiche indicate in fondo.

Chi è rimasto indietro in una lingua può farsi riportare alla tappa dove si è fermato (§2). Pietro ha chiesto un **espediente narrativo per ogni anno**, coerente con come l'anno si attraversa. Queste sono le cinque proposte (07/10/2026), da approvare o correggere.

**Le regole comuni.** Il ritorno è **sempre una scelta del giocatore**, mai imposto. Lo offre la freccia della lingua rimasta indietro, che nella tappa nuova dice che cosa manca e dove. Il ritorno porta **solo** alla tappa in cui quella lingua si è fermata, e da lì si torna con un gesto alla tappa da cui si era partiti. Nessun espediente cambia le regole dell'anno: negli anni 3, 4 e 5 il duca non viaggia, e il ritorno non lo fa viaggiare.

| Anno | Come si attraversa | L'espediente | Che cosa vede il giocatore |
|---|---|---|---|
| anno 1 | Borso a piedi per Ferrara | **Il paggio con il registro.** Un paggio della corte, figura collettiva e senza nome, segue Borso e tiene il conto di ciò che è rimasto in sospeso. Ferrara si attraversa a piedi, e le zone già aperte restano aperte: tornare è solo camminare | Il paggio si avvicina: «Messere, alla Loggia dei Merciai il latino è rimasto a metà». Sulla mappa la zona si illumina e Borso ci va a piedi |
| anno 2 | Ercole I sulla carta d'Italia a strati | **Il dispaccio senza risposta.** La corte estense corrispondeva con gli ambasciatori per lettera; nel gioco una lettera rimasta senza risposta richiama Ercole al pin da cui era partita, letto alla stessa profondità | Arriva una lettera sigillata; aprendola, la carta torna allo strato e al pin di quella tappa |
| anno 3 | La corte, dove le risorse arrivano sulla tavola; Alfonso I guida | **La risorsa riportata in tavola.** Ciò che è passato dalla corte è annotato nel suo inventario, e il guardarobiere lo riporta sulla tavola. Il duca non si muove: è la risorsa che torna | Il guardarobiere entra con l'oggetto della tappa passata e lo posa sulla tavola; la tappa si riapre lì |
| anno 4 | L'archivio, dove arrivano i documenti; Ercole II commenta | **Il fascicolo riaperto.** Nel registro che il giocatore costruisce la riga della lingua rimasta indietro è incompleta; l'archivio conserva tutto, e il fascicolo si riprende dallo scaffale | Una riga del registro lampeggia a metà; cliccandola, il fascicolo esce dallo scaffale e la tappa si riapre |
| anno 5 | Il cantiere che si sposta nel tempo; le stanze del *Furioso* | **La Luna di Astolfo.** Nel *Furioso* Astolfo sale sulla Luna, dove si trova tutto ciò che si è perso in terra, e recupera il senno di Orlando (canto XXXIV). Il livello lasciato indietro è una cosa persa: si va a riprenderla sulla Luna | Un'ampolla con il nome della lingua; toccandola si sale sulla Luna — nel poema Astolfo ci arriva dal Paradiso terrestre sul carro di Elia — e da lì si scende nella stanza della tappa da cui la lingua manca |

**Da verificare prima di scriverli nei dati.** Per l'anno 2, che la corrispondenza diplomatica degli Este sia documentata nella forma usata (i dispacci degli ambasciatori); per l'anno 5, la citazione del canto XXXIV si sceglie e si verifica con `sorgenti/furioso/costruisci_citazioni.py` e `verifica_citazioni.py`, come le altre trenta, e non si scrive a memoria (`furioso.md`); il carro di Elia non è fra i mezzi del quinto anno (`percorsi.md` §1) e va aggiunto, o il viaggio va mostrato senza mezzo. Per l'anno 3, che la Guardaroba estense e il suo inventario siano documentati nella forma usata.

### Q8 — La tappa a mani nude in concreto — **chiusa il 07/10/2026: la proposta è approvata**

Pietro l'ha approvata così come è scritta qui sotto.

Le tappe a mani nude sono dieci, alla quindicesima e alla trentesima di ogni anno (`pedagogia.md` §3). Questa è la proposta di come si giocano.

**Che cos'è.** Una sfida breve **dentro** la tappa, che resta una tappa normale con i suoi sette livelli. Serve a richiamare dalla memoria, senza aiuti, quello che si è imparato fin lì: è l'effetto test (`gioco.md` §4) nella sua forma più pura.

**Le regole.**

- **Dove.** Ha un suo ingresso nell'ambiente, segnato da un segno proprio diverso dalle sette frecce dei livelli. Per la narrazione è una sfida della corte, con una forma diversa in ogni anno.
- **Quando conta.** È **obbligatoria**: la tappa successiva si apre quando la soglia di informatica è superata **e** la sfida è stata fatta. Conta **averla fatta**, non il punteggio: nessuna soglia di risposte giuste.
- **Durata.** Due minuti nel primo anno, tre dal secondo, come i test di ingresso (`ripassi.md`).
- **A mani nude vuol dire:** niente console Python, niente foglio di calcolo, niente calcolatrice, niente suggerimenti, niente richiamo all'origine, niente carte da consultare. Una domanda alla volta, risposte con il tocco.
- **Che cosa chiede.** Domande estratte a caso dai livelli già superati, di **tutti e sette gli ambiti**, e dai sei domini della banca di `pedagogia.md` §3: logica, calcolo mentale e stime, informatica, linguistica e testo, Costituzione e cittadinanza, osservazione e attenzione. L'ultima domanda è sempre **«ripercorri la strada»**: rimettere in ordine sulla mappa luoghi e personaggi della mezza annata. È il metodo dei loci (`gioco.md` §4.3), che prima stava nelle prove di corte.
- **Durante, nessuna reazione.** Il gioco non dice «giusto» o «sbagliato» domanda per domanda. Alla fine mostra l'elenco: che cosa sai, che cosa no, e per ogni domanda il livello da cui viene, come i test di ingresso.
- **Interruzione.** Si riparte senza penalità e senza reazione visibile (`ripassi.md` R5).
- **Nel file di consegna.** Risposte, tempi e il confronto con la sfida precedente: è il dato che il docente guarda per vedere che cosa resta senza aiuti.

**Esempi.**

*Tappa 1-15 (anno 1, dopo i livelli da 1-1 a 1-14; due minuti):*

- *Informatica.* Otto interruttori: «Accendi i bit per scrivere 13». (1-3, 1-5)
- *Calcolo mentale.* «1 KiB sono quanti byte?» — 1000 · 1024 · 1048. (1-7)
- *Stime.* «Con 8 bit per canale RGB, quanti colori diversi?» — circa 256 · circa 65 mila · circa 16 milioni. (1-12)
- *Logica.* «Sommi due numeri di 8 bit e il risultato ha 9 cifre: che cosa è successo?» — overflow · errore di battitura · niente. (1-8)
- *Osservazione.* La facciata della Cattedrale compare per cinque secondi e sparisce: «Di che colore erano i leoni del protiro?» (zona della 1-1)
- *Costituzione.* «La Repubblica tutela il paesaggio e il … della Nazione» — patrimonio storico e artistico · territorio · popolo. (chicca della 1-1, art. 9)
- *Linguistica.* Una domanda da un livello linguistico già superato, per esempio dall'italiano: «Quale di queste parole è un verbo?» — *tavolo* · *correre* · *veloce*.
- *Ripercorri la strada.* I personaggi delle tappe 1-1–1-14 su una striscia: rimettili nell'ordine in cui li hai incontrati.

*Tappa 1-30 (fine del primo anno):* «In `=A1*$B$1` copiata una riga più in basso, che cosa diventa?» (1-26); «`chmod 755`: chi può scrivere?» (1-24); «FF in esadecimale vale…» (1-6); un'immagine di 100 × 100 pixel a 24 bit: circa quanti kB? (1-7, 1-13); e la strada delle tappe 1-15–1-29.

*Tappa 5-15 (anno 5, tre minuti):* «Un algoritmo quadratico impiega 1 s su 1000 elementi: su 10 000?» — 10 s · 100 s · 1000 s; «2 alla 40 è circa…» — mille miliardi · un milione · un miliardo; e, come vuole l'anno 5, una stima con il suo errore da scegliere fra tre intervalli (`anno5-mondo.md` §6).

## 10. Registro delle modifiche

| Data | Versione | Che cosa è cambiato |
|---|---|---|
| 07/10/2026 | 0.5 | Q7 e Q8 chiuse: Pietro ha approvato le cinque proposte di espediente narrativo e la proposta della tappa a mani nude (07/10/2026). Il modello non ha più domande aperte. |
| 07/10/2026 | 0.4 | **Decisioni di Pietro della sera del 07/10/2026.** Q3 chiusa: le prove di corte sono abolite; i 15 livelli diventano normali, da riscrivere (§6). Q6 chiusa: la proposta su processi e modalità è approvata, con 5 livelli su 30 a coppie o di gruppo per ciascuno dei sette ambiti, anche in informatica, e il compagno anche a distanza. Q7: le cinque proposte di espediente narrativo, da approvare. Nuova Q8: la tappa a mani nude in concreto, con esempi per 1-15, 1-30 e 5-15. |
| 07/10/2026 | 0.3 | **Decisioni di Pietro del 07/10/2026 sulla forma della tappa.** La tappa è un ambiente con sette ingressi segnati da frecce colorate, in ordine libero; la tappa successiva si apre con la soglia di informatica; ogni lingua ha la sua propedeuticità e si può tornare indietro (§2). Le chicche sono interattive, brevi, e devono intrattenere (§1). Ogni livello dice al giocatore perché lo fa (§3). Q5 chiusa: modalità e processi di pensiero entrano e non si saltano. Nuove: Q6, la proposta di come entrano, e Q7, l'espediente narrativo per tornare indietro in ogni anno. |
| 07/10/2026 | 0.2 | **Tre domande chiuse dalle decisioni di Pietro del 07/10/2026.** Q1: carta e premio restano tutti e due, e carta e visioni entrano nell'inventario. Q2: il ripasso Leitner resta obbligatorio nella soglia, i test di ingresso restano facoltativi. Q4: si accetta anche il testo libero, valutato dal docente nel report; codice, formule e comandi si verificano eseguendoli. E B1: una tappa contiene sette livelli (§0, §1 parte 14, §2). Restano aperte Q3 e Q5. |
| 07/10/2026 | 0.1 | Prima stesura (fase 2 della roadmap): le quindici parti di un livello, il flusso della tappa, i numeri della bottega e della soglia, che cosa resta al giocatore e al docente, testo e grafica, i tipi di livello e gli anni, la lista di controllo, le sette contraddizioni risolte e le cinque domande per Pietro. |
