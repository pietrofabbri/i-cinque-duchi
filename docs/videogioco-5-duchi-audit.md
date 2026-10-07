---
titolo: Videogioco "I cinque duchi" — audit delle questioni aperte: la lista operativa
tipo: audit
versione: 0.33
data: 2026-10-07
autore: Pietro Fabbri (con Claude)
fonte: lettura di tutti i documenti di progetto che portano una sezione «Questioni aperte» (sedici), verificata da sorgenti/lingue/conta_questioni.py, che confronta anche i numeri che il README copia da qui
documenti collegati: videogioco-5-duchi-lingue.md (v0.6), videogioco-5-duchi-lingue-immagini.md (v0.9), videogioco-5-duchi-percorsi.md (v0.7), videogioco-5-duchi-fonti-visive.md (v0.21), videogioco-5-duchi-furioso.md (v0.7), videogioco-5-duchi-luoghi.md (v0.7), videogioco-5-duchi-mappe.md (v1.6), videogioco-5-duchi-anno5-mondo.md (v0.8), videogioco-5-duchi-percorsi.md (v0.7), videogioco-5-duchi-anno4-mondo.md (v0.7), videogioco-5-duchi-anno3-europa.md (v0.6), videogioco-5-duchi-anno2-penisola.md (v0.3), videogioco-5-duchi-anno1-ferrara.md (v0.3), videogioco-5-duchi-curricolo.md (v0.4), videogioco-5-duchi-gioco.md (v0.9), videogioco-5-duchi-meccaniche.md (v0.7), AGENTS.md
---

# Audit delle questioni aperte: la lista

## 0. Che cosa c'è in questo documento

La **lista operativa** di tutte le questioni aperte del progetto: che cosa si deve decidere, che cosa si può fare, e **chi decide**.

Ogni voce ha quattro cose: la **domanda** in una riga, il **pro**, il **contro**, la **valutazione** (che è la mia, e come tale si può confutare), e la **responsabilità** (chi decide: Pietro, il progetto, una comunità, un'istituzione).

Il documento è verificato da `sorgenti/lingue/conta_questioni.py`, che confronta il proprio conto con i numeri scritti qui.

## 1. Il conto

| | |
|---|---|
| Documenti con una sezione «Questioni aperte» | **17** |
| Voci enumerate | **128** |
| **Chiuse** | **60** |
| **Aperte** | **68** |
| Di cui bloccanti | una |
| Di cui importanti (cambiano il gioco) | due |
| Di cui minori (si possono rimandare) | le altre |

**Il criterio**, dichiarato perché un numero senza criterio non è un dato. Una **voce** è un punto numerato, un `### Q1` o una riga di tabella della sezione «Questioni aperte». Una voce è **chiusa** se porta la marcatura nella sua **prima riga** — «chiusa», «risolto», «ratificata», «confermata» — e non in tutto il corpo, perché una voce aperta spiega dentro il corpo quale parte è stata chiusa.

**Una voce non è sempre una domanda.** In `lingue.md` Q3 ci sono due sotto-voci dentro una sola domanda. Le **128 voci non sono 128 domande**.

**Una sola delle sessanta chiuse è bloccante**: **B1**, chiusa il 07/10/2026 con la decisione di Pietro sui sette livelli per tappa. Delle bloccanti di un tempo, altre due non sono mai state domande: erano lavori, e sono stati fatti — i novanta pin il 02/10/2026, la tavolozza, le sagome, il fondo di Ferrara e i colori delle carte il 03/10/2026 (§7). Le decisioni prese hanno tolto lavoro, non lo hanno aggiunto.


## 2. Una bloccante

È l'unica che ferma qualcosa: le tappe dell'oggetto aspettano la revisione delle voci. Ognuna delle bloccanti ha una scheda. **B1, B3 e B4** sono chiuse con decisioni di Pietro, l'ultima il 07/10/2026; **B5** era un lavoro e non una domanda. Tutte sono anche fra le chiuse (§7).

---

### B1 · I livelli linguistici e quelli informatici sono lo stesso livello o due? — **chiusa il 07/10/2026**

`lingue.md` §7 Q1 · **Decisione di Pietro**: due sistemi paralleli nella stessa tappa. **Ogni tappa contiene sette livelli**, quello di informatica e uno per ciascuna delle sei lingue, ognuno con la propria soglia, e il ragazzo li fa tutti. Il conto dei premi resta 1050. Le due conseguenze ancora da decidere sono fra le importanti: **I23** (che cosa apre la tappa successiva) e **I24** (l'ordine dei sette livelli e il tempo di una tappa). La scheda com'era, con la spiegazione in parole semplici e le tre proposte, è nello storico (`storico.md` §1.18).

---

### B2 · Le trenta voci di ogni oggetto sono confermate?

`lingue.md` §7 Q2 e `lingue-immagini.md` §6.2 Q2 · **pro**: le voci esistono e sono lavorate; confermarle sblocca 1120 candidati già cercati. **contro**: per il ferrarese non sono un elenco ma **campi da rilevare**, e la fonte non è stabilita (chi raccoglie, con che metodo, con quale consenso); un proverbo scritto a tavolino è un proverbo italiano in maschera. **valutazione**: va chiusa **prima** di scegliere le immagini, altrimenti si rifà la ricerca; per le altre cinque lingue è una revisione di trenta voci, per il ferrarese è un progetto. **responsabilità**: Pietro, e per il ferrarese **anche chi raccoglierà i proverbi**. **blocca**: B4, e le tappe facoltative degli oggetti.

**Decisioni di Pietro del 07/10/2026, per chiuderla.** Le voci delle cinque lingue le rivede lui su una pagina con le segnalazioni del progetto; **il ferrarese lo raccoglie il progetto** da fonti pubblicate e citate, e lui lo rivede (`lingue.md` Q2). La domanda si chiude con la revisione.

### B3 · La LIS nel gioco: chi insegna, e con quali materiali? — **chiusa il 07/10/2026**

`lingue.md` §7 Q4 · **Decisione di Pietro**: la LIS usa **soltanto materiali online**, con licenza libera e il testo italiano accanto quando c'è. Pietro ha un contatto con persone sorde, e **la comunità si coinvolge dopo l'anno 1**. La scheda com'era è nello storico (`storico.md` §1.21).

### B4 · Chi guarda le 1120 immagini degli oggetti? — **chiusa il 07/10/2026**

`lingue-immagini.md` §6.2 Q1 · **Decisione di Pietro**: le guarda lui, già dal 04/10, e il progetto gli prepara **uno strumento pratico e veloce** per scegliere: una pagina con le candidate di ogni voce affiancate e la scelta con un tocco. Si usa dopo la revisione delle voci (B2). La scheda com'era è nello storico (`storico.md` §1.21).

### B5 · I novanta pin degli anni 2, 3 e 4 sono verificati? — **chiusa il 02/10/2026**

Non è più una bloccante: l'esito è in **§7**, il racconto nello storico (`storico.md` §1). Era l'unica delle cinque che non aspettava nessuna decisione, ed è l'unica che il progetto poteva chiudere da solo.


## 3. Le due importanti

Quelle che, se risposte male, cambiano il gioco. In ordine di peso.

| # | Domanda | Pro | Contro | Valutazione | Chi decide |
|---|---|---|---|---|---|
| I1 | ~~**Il percorso del duca è l'ordine delle tappe o un giro a parte?**~~ **chiusa il 07/10/2026** (`percorsi.md` Q1) | — | — | **Decisione di Pietro: il percorso segue l'ordine delle tappe.** Nessun giro a parte; la storia di ogni anno deve dare un senso ai posti e al loro ordine | Pietro |
| I2 | ~~**La tavolozza va prodotta?**~~ **chiusa il 03/10/2026** (`fonti-visive.md` Q1) | — | — | **Fatta**: 18 voci in `dati/fonti_visive/tavolozza.json`, e la scelta è quella prevista: dichiarare i colori di ogni fonte, non ricolorare tutto | Il progetto |
| I3 | ~~**Le sagome degli edifici si costruiscono?**~~ **chiusa il 03/10/2026** (`fonti-visive.md` Q2) | — | — | **Fatte**: 5209 sagome su 54 luoghi in `dati/edifici_footprint.json`, nell'ordine previsto (prima la tavolozza) | Il progetto |
| I4 | ~~**Il fondo di Ferrara si costruisce?**~~ **chiusa il 03/10/2026** (`fonti-visive.md` Q3) | — | — | **Fatto**: 14 tratti di mura, 4,20 km², in `dati/ferrara_fondo.json`; il perimetro ufficiale non esisteva in nessuna fonte e l'anello è stato ricostruito con la tolleranza che contiene tutte le tappe | Il progetto |
| I5 | ~~**Che cosa è un «testo autentico» nelle sei lingue?**~~ **chiusa il 07/10/2026** (`lingue.md` Q3) | — | — | **Decisione di Pietro**: un testo che esiste fuori dal gioco, con la sua fonte; mai scritto dal progetto; e sempre usato con un'azione, perché l'attenzione è rara. Le ipotesi per lingua sono in `lingue.md` Q3 | Pietro |
| I6 | ~~**Il greco moderno ha una linea propria?**~~ **chiusa il 07/10/2026** (`lingue.md` Q5) | — | — | **Decisione di Pietro: nessuna linea propria**; al più un accenno in una o due lezioni. Il greco punta su etimologia, radici, indoeuropeo, cultura e filosofia | Pietro |
| I7 | ~~**Che cosa succede se il giocatore non sa l'italiano?**~~ **chiusa il 07/10/2026** (`lingue.md` Q7) | — | — | **Decisione di Pietro**: un modulo d'ingresso più semplice con Niccolò III, prima di Borso, per qualsiasi lingua di partenza; si costruisce dopo l'anno 1 | Pietro |
| I8 | ~~**Quanti esercizi fanno le trenta voci?**~~ **chiusa il 07/10/2026** (`lingue.md` Q8) | — | — | **Decisione di Pietro: trenta voci, sapendo il costo.** I facoltativi di informatica hanno quattro domande per gradino senza pool; il conto si fa livello per livello, per ciascun ambito | Pietro |
| I9 | ~~**Le fonti del latino e del greco vanno cercate altrove?**~~ **chiusa il 07/10/2026** (`lingue-immagini.md` Q3) | — | — | **Decisione di Pietro: sì**, corpus epigrafici (EDCS, EDR) e biblioteche digitali | Pietro |
| I10 | **Le immagini servono solo per le facoltative?** (`lingue-immagini.md` Q5) | Le tappe sui testi autentici hanno bisogno di immagini diverse (la pagina di Cesare, non una coppa) | Sono almeno 900 immagini, e nessuna è stata cercata | **Rinviata il 07/10/2026, ed è un lavoro del progetto, non una domanda**: le immagini dei testi autentici si cercano livello per livello, quando si scrive il testo | Il progetto |
| I11 | ~~**Le Nuove Indicazioni 2026 vanno acquisite?**~~ **chiusa il 07/10/2026** (`curricolo.md`) | — | — | **Decisione di Pietro: si acquisiscono.** È un lavoro: trovare il testo ufficiale della sezione Informatica, rifare il §6 del curricolo e la verifica di copertura | Pietro |
| I12 | **Quanto dura un livello?** (`curricolo.md`) | Ogni livello deve durare da 5 minuti a qualche ora; senza stima non si sa se 150 livelli stanno in 5 anni | La stima dipende dal prototipo, che non c'è | **Rinviata il 07/10/2026**: la durata si misura sul prototipo della tappa 1-1 riscritta; prima non c'è niente da misurare | Il progetto |
| I13 | ~~**Il 1945 non è una tappa.**~~ **chiusa il 07/10/2026** (`anno5-mondo.md` §13) | — | — | **Decisione di Pietro**: Roosevelt, Cassin e Lauterpacht entrano come facoltativi | Pietro |
| I14 | ~~**Il buco della biologia nel quinto anno.**~~ **chiusa il 07/10/2026** (`anno5-mondo.md` §13) | — | — | **Decisione di Pietro**: medicina, vaccini, antibiotici, DNA e genetica entrano come facoltativi | Pietro |
| I15 | ~~**La tratta e l'imperialismo nell'anno 3.**~~ **chiusa il 07/10/2026** (`anno3-europa.md` §13) | — | — | **Decisione di Pietro**: il limite si dichiara, e si aggiunge una scheda d'atlante sul colonialismo | Pietro |
| I16 | ~~**Leonardo in due anni.**~~ **chiusa il 07/10/2026** (`anno3-europa.md` §13) | — | — | **Decisione di Pietro: è perfetto così.** I ritorni sono una risorsa: il gioco fa riferimento agli anni passati, nella storia e negli argomenti, e altri ritorni vanno bene | Pietro |
| I17 | ~~**Il formato del file di consegna.**~~ **chiusa il 07/10/2026** (`meccaniche.md`) | — | — | **Decisione di Pietro**: `.txt` con una firma che rende la consegna verificabile | Pietro |
| I18 | ~~**Il gioco è un modulo della piattaforma gamificata o un prodotto a sé?**~~ **chiusa il 07/10/2026** (`meccaniche.md`, `curricolo.md`) | — | — | **Decisione di Pietro: prodotto a sé**, con i requisiti della piattaforma come caso particolare | Pietro |
| I19 | ~~**I colori dei fondi geografici.**~~ **chiusa il 03/10/2026** (`fonti-visive.md` Q4) | — | — | **Fatto**: `dati/fonti_visive/colori_cartografici.json`, 17 voci (16 dichiarate con motivo e criterio, 3 prese dalla tavolozza con l'esadecimale confrontato byte per byte), la regola che **una categoria con il riempimento ha anche il bordo**, e `verifica_colori.py` (C1–C7). **Cercandoli è saltato fuori un difetto che non era di colori**: `mondo_admin1_copertura.json` stava dentro `dati/mappe/` e faceva crashare il lettore | Il progetto |
| I20 | ~~**La carta del personaggio e il premio: restano tutti e due?**~~ **chiusa il 07/10/2026** (`modello-di-livello.md` Q1) | — | — | **Decisione di Pietro: tutti e due.** La carta è il personaggio e regge il ripasso, il premio è l'oggetto del livello; carta e visioni sono nell'elenco dell'inventario, e la collezione delle carte è il quinto registro (`inventario.md` §1, §3) | Pietro |
| I21 | ~~**Prove di corte e tappe a mani nude sono la stessa cosa?**~~ **chiusa il 07/10/2026** (`modello-di-livello.md` Q3) | — | — | **Decisione di Pietro: le prove di corte sono abolite.** I 15 livelli diventano normali e vanno riscritti con un argomento proprio; restano le tappe a mani nude alle x-15 e x-30, e la loro forma concreta è la proposta Q8 del modello | Pietro |
| I22 | ~~**«Nessuna risposta scritta» e gli strumenti veri**~~ **chiusa il 07/10/2026** (`modello-di-livello.md` Q4) | — | — | **Decisione di Pietro: si accetta anche il testo libero.** Lo valuta il docente nel report, non il gioco; per la soglia contano solo risposte che il gioco corregge da solo, e codice, formule e comandi si verificano eseguendoli (`modello-di-livello.md` §3) | Pietro |
| I23 | ~~**Che cosa apre la tappa successiva: la soglia di informatica, o tutte e sette?**~~ **chiusa il 07/10/2026** (`lingue.md` Q10) | — | — | **Decisione di Pietro**: la tappa successiva si apre con la soglia di informatica; per il livello *n* di una lingua servono tutti i premi precedenti di quella lingua, e si può tornare indietro con un espediente narrativo per anno (I25) | Pietro |
| I24 | ~~**L'ordine dei sette livelli in una tappa, e il tempo di una tappa**~~ **chiusa il 07/10/2026** (`lingue.md` Q11) | — | — | **Decisione di Pietro**: nessun ordine; i sette livelli sono sparsi nell'ambiente, ognuno con una freccia del suo colore, accanto a chicche interattive brevi. Il tempo si misura sul prototipo (I12) | Pietro |
| I25 | ~~**L'espediente narrativo per tornare indietro, anno per anno**~~ **chiusa il 07/10/2026** (`modello-di-livello.md` Q7) | — | — | **Decisione di Pietro: le cinque proposte sono approvate.** Prima di metterle nei dati restano tre verifiche di fatto (anni 2, 3 e 5) | Pietro |


## 4. Le altre, in sintesi

Le **restanti**: minori, o già decise nella sostanza e che aspettano solo l'esecuzione. Chi decide è Pietro quasi sempre, e dove è il progetto è perché non è una domanda ma un lavoro.

**Il numero di ogni intestazione è il conto delle voci aperte di quel documento meno le importanti che il §3 elenca già**, e `sorgenti/lingue/conta_questioni.py` lo confronta: il §4 si intitola «Le altre», e un numero che contasse anche le importanti sarebbe doppio. Ogni documento con voci aperte deve comparire in un'intestazione — `itinerari.md` c'era rimasto fuori fino al 04/10/2026, e la sua voce era contata ma non elencata da nessuna parte. Le cifre fuori dalle parentesi sono nomi, non conteggi: il 3 di «Anno 3» non è un numero di voci.

### Sistema linguistico (`lingue.md` 6, `lingue-immagini.md` 2)

| Domanda | Chi decide |
|---|---|
| Il confronto fra le sei lingue è obbligatorio o a rotazione? Il calcolo dà il 17% del totale | Pietro |
| I confronti filologici sono vincolanti, e come li si controlla | Pietro |
| Le trenta voci ferraresi: che tappa hanno, se non hanno immagine | Pietro |
| Chi ridimensiona le immagini scelte a 96×72, e quando | Il progetto |
| Il livello 30 di ogni lingua è un compito: che cosa produce, e con quale criterio di superamento | Pietro |

### Percorsi (`percorsi.md` 5)

| Domanda | Chi decide |
|---|---|
| Il giro si chiude a Ferrara? Costo 10-101 giorni di viaggio che il gioco non fa pagare | Pietro |
| Il mezzo cambia dentro l'anno? Nel quarto anno è il mezzo di chi porta il documento | Pietro |
| Le facoltative continentali si aprono sul ritorno | Pietro |
| I buchi continentali degli anni 3, 4 e 5 | Pietro |
| Il tempo di viaggio è un esercizio giocabile o una dichiarazione | Pietro |

### Fonti visive (`fonti-visive.md` 1)

| Domanda | Chi decide |
|---|---|
| Chi guarda i 125 candidati delle fonti visive | Io o Pietro |
| Le due facoltative continentali dell'anno 4 si aprono sul ritorno | Pietro |

### Anno 1 (`anno1-ferrara.md` 7) e curricolo (`curricolo.md` 4)

| Domanda | Chi decide |
|---|---|
| Il narratore: che ruolo hanno gli altri duchi nel percorso | Pietro |
| Renzo Ravenna e le 20 schede aggiunte: approvare o scartare | Pietro |
| La mappa digitale di Ferrara che Pietro deve fornire | Pietro |
| Le fonti primarie, scheda per scheda | Il progetto |
| La verifica storica complessiva, con un collega o con l'Archivio di Stato | Pietro **e un istituto** |
| Il secondo linguaggio tipizzato (C++ o Java) al 3º o 4º anno | Pietro |
| Il rapporto con la piattaforma gamificata (vedi I18) | Pietro |
| L'allineamento interdisciplinare con le programmazioni reali di classe | Pietro **e i colleghi** |
| Le fonti storiche del §4 | Il progetto |

### Anno 2 (`anno2-penisola.md` 8)

| Domanda | Chi decide |
|---|---|
| La carta intera alla fine dell'anno: si aprono tutti gli strati insieme | Pietro |
| Tre collettivi su trenta tappe: alternativa (a) o (b) | Pietro |
| Il bilancio degli agganci: 13 forti e 17 medi | Pietro |
| La colonna stratigrafica sempre visibile a schermo | Pietro |
| Il materiale dal 1500 in poi | Pietro |
| Le persone viventi (Cristoforetti) | Pietro |
| Le fonti del materiale | Il progetto |
| Le «visioni» dell'anno 1 nell'anno 2 | Pietro |

### Anno 3 (`anno3-europa.md` 6), anno 4 (`anno4-mondo.md` 4), anno 5 (`anno5-mondo.md` 7)

| Domanda | Chi decide |
|---|---|
| Il bilancio degli agganci: 21 forti, 9 medi, e tre forse troppo forti | Pietro |
| Persone viventi (von der Leyen, Merkel, Macron): solo emblemi | Pietro |
| Le sei aggiunte (Josquin, Bellini, Dürer, Manuzio, Caxton, Levi) | Pietro |
| La corte come unico luogo percorribile: la alternativa è il visitatore-inviato | Pietro |
| La regola di AGENTS.md sul duca guida dal terzo anno (già scritta, va tenuta allineata) | Il progetto |
| I tre agganci «forti» da rivedere dell'anno 4 | Pietro |
| La tappa 4-10 e l'incendio dell'archivio | Pietro |
| Chi è il protagonista del quinto anno: dentro il *Furioso*, con la regola dei due strati (parzialmente risolta) | Pietro |
| Il quinto anno e l'anno 3: come si dividono il Novecento | Pietro |
| I facoltativi che il gioco non può mettere in tabella | Il progetto |
| I quattro agganci da rivedere del quinto anno | Pietro |
| Le previsioni con la data: si rileggono fra dieci anni, e con quale formato | Pietro |
| Il posto di F11 nel registro del gioco | Pietro |

### Luoghi (`luoghi.md` 2), mappe (`mappe.md` 3), *Furioso* (`furioso.md` 1), gioco (`gioco.md` 4), meccaniche (`meccaniche.md` 5)

| Domanda | Chi decide |
|---|---|
| Le undici facoltative continentali: proposte e non schede | Pietro |
| Il tipo di legame dei ventisei pin del quinto anno | Pietro |
| Il vincolo di 20 000 abitanti per mostrare una città | Pietro |
| Le trenta zone percorribili: tutte, o solo dove il luogo è lo spazio del gioco | Pietro |
| Il file delle regioni amministrative: intero o ridotto | Il progetto |
| Le ventisei stanze senza coordinata: la regola che le dichiara | Pietro |
| I motti e i dialoghi delle trenta tappe | Pietro |
| Confermare la tappa 1-30 (P93, la città) | Pietro |
| Verificare che v86 e Pyodide funzionino sui computer del laboratorio e sui Chromebook | Il progetto **e il laboratorio** |
| Per 1-25 e 1-26: strumento nel gioco, file caricato, o entrambi | Pietro |
| I pesi e le soglie del meccaniche §2.3, calibrati sul prototipo | Il progetto |
| Quanti eventi di dettaglio conservare nel codice di ripresa | Il progetto |
| Lo strumento del docente: subito o dopo il prototipo | Pietro |
| Safe Exam Browser e la proposta al regolamento d'istituto sui dispositivi indossabili | Pietro **e l'istituto** |
| La specifica della modalità accessibile | Il progetto **e il progetto di accessibilità del gioco** |

### Itinerari (`itinerari.md` 1)

| Domanda | Chi decide |
|---|---|
| Le cinque tappe del primo anno senza facoltativi: sono un dato o una dimenticanza? Se sono un dato, va scritto perché sono cinque e non tre | Pietro |


## 5. Le domande che sono due

Tre questioni compaiono in due documenti, e una è la stessa identica:

| La domanda | Dove | Nota |
|---|---|---|
| Le trenta voci sono confermate | `lingue.md` Q2 = `lingue-immagini.md` Q2 | Una risposta sola chiude due |
| Una linea che attraversa gli anni senza essere una tappa | `lingue.md` Q5 = `anno5-mondo.md` | Stessa idea, risposta data per gli anni 3-4 e non per le lingue antiche |
| I codici `Q` dei personaggi | `anno3` Q6 = `anno4` Q5 = `anno5` Q4 | **L'unica ridondanza che funziona**: confermati in tutti e tre i documenti e concordanti. È la prova che funziona quando qualcuno la controlla |


## 6. La sequenza che chiude tutto

Resta una bloccante, e la catena si è accorciata.

**B2** (voci confermate) viene **prima** di **B4** (chi guarda le immagini): cercare le immagini prima di aver confermato le voci è lavoro da rifare. **B1**, che decideva quanti tipi di tappa esistono e quindi se B4 aveva senso, è chiusa il 07/10/2026: ogni tappa ha sei livelli linguistici, e le immagini degli oggetti servono a tutti e sei.

La catena è: **B2 → la scelta delle immagini**. B4 è chiusa (le immagini le guarda Pietro, con uno strumento che il progetto prepara) e B3 anche (la LIS usa materiali online; la comunità si coinvolge dopo l'anno 1).

> **Mentre si decide, si costruisce quello che si può costruire.** Le tappe informatiche non aspettano le bloccanti: mappa, pin, ambienti, mezzi e luoghi si costruiscono senza le loro risposte, e molte delle chiusure del §7 erano lavori, non domande.

## 7. Le questioni chiuse

Le questioni che questo documento ha seguito fino alla chiusura, con l'esito in una riga e il posto dove sta oggi il risultato. **Come** sono state chiuse — i difetti trovati per strada, le prove, le lezioni — è nello storico (`storico.md` §1), alla lettera.

Il conto delle voci chiuse del §1 è un'altra cosa: lo fa `conta_questioni.py` sulle sezioni «Questioni aperte» dei documenti, e non legge questa tabella.

| Voce | Chiusa il | Esito | Dove sta oggi |
|---|---|---|---|
| **B5** · i pin degli anni 2, 3 e 4 sono verificati? | 02/10/2026 | Era un lavoro e non una domanda: i pin sono slot, uno per tappa, e dietro ci sono meno posti distinti; otto controlli automatici e due coordinate corrette (Baghdad, Karakorum) | `mappe.md` §8bis, `sorgenti/gis/verifica_pin.py` |
| **B1** · i livelli linguistici e quelli informatici sono lo stesso livello o due? | 07/10/2026 | Decisione di Pietro: sette livelli per tappa, informatica e sei lingue, ognuno con la sua soglia; il ragazzo li fa tutti | `lingue.md` Q1, `modello-di-livello.md` §0–§2 |
| **I20** · la carta del personaggio e il premio | 07/10/2026 | Decisione di Pietro: tutti e due; carta e visioni entrano nell'inventario, la collezione delle carte è il quinto registro | `modello-di-livello.md` §9 Q1, `inventario.md` §1, §3 |
| **I22** · «nessuna risposta scritta» e gli strumenti veri | 07/10/2026 | Decisione di Pietro: testo libero ammesso, valutato dal docente; per la soglia solo risposte corrette dal gioco | `modello-di-livello.md` §3, §9 Q4 |
| **I23** · che cosa apre la tappa successiva | 07/10/2026 | Decisione di Pietro: la soglia di informatica; le lingue hanno una propedeuticità loro e si può tornare indietro | `lingue.md` Q10, `modello-di-livello.md` §2 |
| **I24** · ordine dei sette livelli e tempo della tappa | 07/10/2026 | Decisione di Pietro: ordine libero, ingressi sparsi nell'ambiente con frecce colorate, chicche interattive brevi | `lingue.md` Q11, `modello-di-livello.md` §1–§2 |
| I campi `Modalità` e processi di pensiero | 07/10/2026 | Decisione di Pietro: entrano, e non si possono saltare; il *come* è una proposta da approvare (`modello-di-livello.md` Q6) | `modello-di-livello.md` §9 Q5 |
| **I21** · prove di corte e tappe a mani nude | 07/10/2026 | Decisione di Pietro: prove di corte abolite; restano le tappe a mani nude | `modello-di-livello.md` §6, §9 Q3 e Q8 |
| Come entrano processi di pensiero e modalità | 07/10/2026 | Decisione di Pietro: proposta approvata; 5 livelli su 30 a coppie o di gruppo per ciascuno dei sette ambiti, anche in informatica | `modello-di-livello.md` §9 Q6 |
| **I25** · l'espediente narrativo per tornare indietro | 07/10/2026 | Decisione di Pietro: approvate le cinque proposte (paggio, dispaccio, risorsa in tavola, fascicolo, Luna di Astolfo); restano tre verifiche di fatto | `modello-di-livello.md` §9 Q7 |
| La tappa a mani nude in concreto | 07/10/2026 | Decisione di Pietro: approvata la proposta (sfida obbligatoria dentro la tappa, conta averla fatta, due o tre minuti senza strumenti) | `modello-di-livello.md` §9 Q8 |
| **B3** · la LIS: chi insegna, con quali materiali | 07/10/2026 | Solo materiali online; la comunità sorda si coinvolge dopo l'anno 1 | `lingue.md` Q4 |
| **B4** · chi guarda le immagini degli oggetti | 07/10/2026 | Pietro, con uno strumento di scelta che il progetto prepara | `lingue-immagini.md` §6.2 Q1 |
| **I1** · il percorso del duca | 07/10/2026 | Il percorso segue l'ordine delle tappe | `percorsi.md` Q1 |
| **I5** · il testo autentico | 07/10/2026 | Un testo che esiste fuori dal gioco, con la sua fonte; mai scritto dal progetto; e sempre usato con un'azione, perché l'attenzione è rara | `lingue.md` Q3 |
| **I6** · il greco moderno | 07/10/2026 | Nessuna linea propria; al più un accenno in una o due lezioni | `lingue.md` Q5 |
| **I7** · chi non sa l'italiano | 07/10/2026 | Un modulo d'ingresso più semplice con Niccolò III, prima di Borso, per qualsiasi lingua di partenza; si costruisce dopo l'anno 1 | `lingue.md` Q7 |
| **I8** · il numero degli esercizi degli oggetti | 07/10/2026 | Trenta voci, sapendo il costo | `lingue.md` Q8 |
| **I9** · le fonti del latino e del greco | 07/10/2026 | Sì, corpus epigrafici (EDCS, EDR) e biblioteche digitali | `lingue-immagini.md` §6.2 Q3 |
| **I11** · le Nuove Indicazioni 2026 | 07/10/2026 | Si acquisiscono | `curricolo.md` §7 |
| **I13** · anno 5: il 1945 | 07/10/2026 | Roosevelt, Cassin e Lauterpacht entrano come facoltativi | `anno5-mondo.md` §13 |
| **I14** · anno 5: la biologia | 07/10/2026 | Medicina, vaccini, antibiotici, DNA e genetica entrano come facoltativi | `anno5-mondo.md` §13 |
| **I15** · anno 3: la tratta e l'imperialismo | 07/10/2026 | Il limite si dichiara, e si aggiunge una scheda d'atlante sul colonialismo | `anno3-europa.md` §13 |
| **I16** · Leonardo in due anni, e i ritorni | 07/10/2026 | Resta obbligatorio in due anni: i ritorni sono una risorsa, con riferimenti agli anni passati | `anno3-europa.md` §13 Q7, §6.4 |
| **I17** · il formato del file di consegna | 07/10/2026 | `.txt` con una firma che rende la consegna verificabile | `meccaniche.md` §3 |
| **I18** · modulo o prodotto a sé | 07/10/2026 | Prodotto a sé, con i requisiti della piattaforma come caso particolare | `meccaniche.md` §3 |
| Il ripasso a distanza accanto ai test di ingresso | 07/10/2026 | Decisione di Pietro: tutti e due, con ruoli diversi; il ripasso Leitner è obbligatorio nella soglia, i test sono facoltativi | `modello-di-livello.md` §9 Q2, `gioco.md` §4.2 |
| **I2** · la tavolozza | 03/10/2026 | Si dichiarano i colori di ogni fonte invece di ricolorare tutto: ogni colore ha la sua fonte | `dati/fonti_visive/tavolozza.json`, `fonti-visive.md` §3 |
| **I3** · le sagome degli edifici | 03/10/2026 | Sagome da OpenStreetMap; un edificio senza altezza misurata diventa un volume neutro dichiarato, non una stima | `dati/edifici_footprint.json`, `fonti-visive.md` §3 |
| **I4** · il fondo di Ferrara | 03/10/2026 | Le mura da OpenStreetMap, con la tolleranza più piccola che tiene dentro tutte le tappe del primo anno | `dati/ferrara_fondo.json`, `fonti-visive.md` §3 |
| **I19** · i colori delle carte | 03/10/2026 | Ogni categoria con il riempimento ha anche il bordo; i colori presi dalla tavolozza sono confrontati byte per byte | `dati/fonti_visive/colori_cartografici.json` |
| Il numero dei livelli trasversali | 03/10/2026 | Zero: il trasversale è un aggancio dentro i livelli, non un livello | `quadro-trasversale.md` §1.3 |
| La variante dei premi | 03/10/2026 | Un premio per livello | `premi.md` §4 |
| Il premio della LIS | 03/10/2026 | La categoria K: la scheda che il giocatore produce | `premi.md` §2.1 |
| «Osservazione e attenzione» | 03/10/2026 | Era un difetto, non una lacuna: il dominio esiste nel nucleo `Q8.2` del livello 3-27, nell'osservazione linguistica, nelle tappe 1-23, 1-29 e 5-11 | `schema-livelli.md`, `lingue.md` §4 |
| La 3-28 | 03/10/2026 | Il registro dei luoghi prende il luogo dalla riga della tabella del documento | `sorgenti/luoghi/estrai_luoghi.py` |
| La 4-16 | 03/10/2026 | Il dato non è più corretto a mano: lo produce la catena dei luoghi | `sorgenti/verifica_catena_luoghi.py` |
| Ascolto e parlato: si può fare? | 03/10/2026 | Sì, su cinque livelli; la Web Speech API è esclusa perché manda l'audio fuori dal dispositivo | `parlato.md` |
| Il mezzo del quinto anno | 03/10/2026 | Due regole senza autore: il mezzo reale lo sceglie l'archivio, quello dentro la stanza lo sceglie il canto | `itinerari.md` §2 |
| I codici dei facoltativi | 03/10/2026 | Un codice per persona e non per occorrenza, con l'indice delle persone che hanno due codici | `dati/videogioco-5-duchi-facoltativi.json`, `sorgenti/verifica_codici.py` |

## 8. Registro delle modifiche

| Data | Versione | Che cosa è cambiato |
|---|---|---|
| 07/10/2026 | 0.33 | **La fase 3 si chiude quasi tutta.** B3 e B4 chiuse; chiuse tredici importanti (I1, I5–I9, I11, I13–I18); I10 e I12 rinviate con il motivo. Resta una bloccante, B2, che si chiude con la revisione delle voci. Conto: 128 voci, 60 chiuse, 68 aperte, 1 bloccante, 2 importanti (decisioni di Pietro del 07/10/2026). |
| 07/10/2026 | 0.32 | I25 chiusa e la tappa a mani nude decisa (approvazioni di Pietro del 07/10/2026); il modello di livello non ha più domande aperte e il suo blocco esce dal §4. Conto: 128 voci, 46 chiuse, 82 aperte, 3 bloccanti, 15 importanti. |
| 07/10/2026 | 0.31 | **Decisioni di Pietro della sera del 07/10/2026.** I21 chiusa: prove di corte abolite, restano le tappe a mani nude. Approvata la proposta su processi di pensiero e modalità, con 5 livelli su 30 a coppie o di gruppo per ciascuno dei sette ambiti. I25 ha le cinque proposte di espediente narrativo, da approvare; nel §4 la proposta Q8 sulla tappa a mani nude. Conto: 128 voci, 44 chiuse, 84 aperte, 3 bloccanti, 16 importanti. |
| 07/10/2026 | 0.30 | **Altre decisioni di Pietro del 07/10/2026.** I23 chiusa: la tappa successiva si apre con la soglia di informatica, le lingue hanno una propedeuticità loro. I24 chiusa: i sette livelli non hanno ordine e sono sparsi nell'ambiente. I campi Modalità e processi di pensiero entrano. Nuova I25: l'espediente narrativo per tornare indietro, anno per anno; nel §4 la proposta Q6 del modello da approvare. Conto: 127 voci, 42 chiuse, 85 aperte, 3 bloccanti, 17 importanti. |
| 07/10/2026 | 0.29 | **Le decisioni di Pietro del 07/10/2026.** B1 chiusa: sette livelli per tappa, e le bloccanti passano da quattro a tre, con la catena B2 → B4. I20 (carta e premio) e I22 (testo libero) chiuse; nuove importanti I23 (che cosa apre la tappa successiva) e I24 (ordine dei sette livelli e tempo della tappa), da `lingue.md` Q10 e Q11. Il ripasso a distanza esce dal §4. Le quattro chiusure sono nella tabella del §7; la scheda di B1 com'era è in `storico.md` §1.18. Conto: 125 voci, 39 chiuse, 86 aperte. |
| 07/10/2026 | 0.28 | Tre importanti nuove, I20–I22 (carta e premio, prove e tappe a mani nude, risposte scritte e strumenti veri), e una sezione del §4 per le altre due domande del modello di livello; il conto passa a 123 voci in 17 sezioni, 35 chiuse e 88 aperte, perché il modello aggiunge cinque voci e in `gioco.md` la ricerca dei ritratti è chiusa. |
| 06/10/2026 | 0.27 | Il §6 dice la catena delle bloccanti e la regola «mentre si decide, si costruisce» al presente; il racconto di B5 e delle chiusure del 03/10, con il rimando al §3bis che non esiste più, è in `storico.md` §1.17. Con questa versione l'audit è in ordine: sezioni da §0 a §8, una scheda per questione, le chiuse in §7 e il registro in fondo (fase 1 della roadmap). |
| 06/10/2026 | 0.26 | **Il racconto esce, le questioni restano.** Le sedici sezioni aggiunte dopo ogni chiusura e ogni lezione di metodo (2bis, da 3bis a 3quinquagesim, 3octies), circa 59 000 caratteri, sono state spostate alla lettera in `storico.md` §1 (fase 1 della roadmap). Al loro posto c'è il §7, «Le questioni chiuse»: voce, data, esito in una riga e dove sta oggi il risultato. Il registro è il §8, e la riga della v0.1, rimasta in fondo al file dopo le sezioni di racconto, è tornata nel registro. I rimandi a §2bis e §3bis puntano al §7. |
| 05/10/2026 | 0.25 | **Il rimando e' l'unica cosa che cambia.** `fonti-visive.md` e' salito a v0.20 e `mappe.md` a v1.5, e le due citazioni di questo frontmatter erano ferme alla versione di prima: un rimando fermo sembla un rimando fermo, e invece punta a un testo che non e' piu' quello. |
| 05/10/2026 | 0.24 | **Il rimando è l'unica cosa che cambia.** Un documento collegato è salito di versione e questo rimando è rimasto indietro: la riga è sbagliata e non sembra, perché un rimando che cita una versione superiore a quella vera sembra un rimando fermo. Qui dentro non cambia nient'altro — e si scrive lo stesso, perché una riga che cambia è una riga che cambia. |
| 05/10/2026 | 0.23 | **Il nono numero che non guardava: i disegni erano trenta e nessuna riga se ne è accorta.** Estesi a tutte e **centocinquanta** le tappe (`--tutte`: **2632** edifici, **0** ritagliati, **150** PNG decodificati, **16** tappe vuote dichiarate). **D3** però chiedeva sha tutti diversi, e sui centocinquanta la risposta è no e non può essere sì: **43 tappe su 150** hanno le stesse sagome sulla stessa griglia. Un controllo che segnala come difetto la verità è un allarme spento. Riscritto sul confronto fra **chiave dati e sha** (`chiave_dati()`): **107 chiavi dati, 107 sha distinti**. Nuova la prova `prova_difetto_disegni_150.py` (**F1** perde un edificio dalla 2-5, **F2** macchia la 5-18): **2 iniettati, 2 visti**, ripristino verificato sugli sha. La data di `indice.json` è passata da scritta a mano a **calcolata**, e il costo di `verifica_disegni.py` (**2 min 10 s**, D4 decodifica i PNG in Python puro) è dichiarato. **E in più, lo stesso difetto in un'altra frase: le questioni chiuse sono 34 e la prosa ne scriveva 31.** `conta_questioni.py`, che confronta l'audit con sé stesso, lo segnalava: la tabella di §1 dichiarava **31** chiuse e **87** aperte, la frase di apertura e la citazione del §6 dicevano «nessuna delle trentuno chiuse», il `README.md` copiava **31 e 87** in due posti, e l'intestazione del §4 dichiarava **4** voci per `lingue-immagini.md` contro **1** del conto. Cinque numeri invecchiati, e nessuno falso per errore di metodo: erano falsi perché le chiusure degli ultimi giorni avevano fatto crescere il conto e non la prosa. Riallineati al **34 / 84**, e nella voce di registro storica che citava la frase in lettere il numero **è sparito**, che è la lezione che quella voce stessa contiene. §3quindices. |
| 04/10/2026 | 0.22 | **L'ottavo numero che non guardava: due righe scritte due volte e un registro che aveva perso due versioni.** `premi.md` §6 aveva due righe su cinque — mancavano **v0.2** e **v0.4**, cioè la categoria K e tutto il catalogo con gli emblemi. In `fonti-visive.md` la sezione **§3.10** e la riga «Emblemi dei premi» erano ciascuna in **duplice copia**, e il registro aveva una riga di separazione **in mezzo alle righe** più le versioni **0.9 e 0.10 assenti**. Nello stesso documento, la *fonte* e `AGENTS.md` dicevano «tranne informatica» e §2.2 scriveva «nessuno», mentre §4.0 ne contava **150**:  Pietro ha deciso il 04/10 che l'informatica ha un premio per tappa, il numero resta **1050** e i tre luoghi che lo negavano sono corretti. |
| 04/10/2026 | 0.21 | **Il carattere che il font non ha, e non disegna niente.** Gli emblemi dei 1050 premi erano un foglio di tessere 48×54 e il primo giro le ha prodotte **identiche**: `1-1-FE` e `1-2-FE` erano lo stesso file. Il font del progetto aveva solo le **ventisei lettere**, e `FONT.get("2", [])` restituisce una lista **vuota** e senza dire niente, quindi il numero della tappa semplicemente non veniva disegnato. Le dieci cifre sono ora in `sorgenti/art/digiti.py`. Il secondo difetto, due minuti dopo: `1-2` e `2-2` hanno entrambi il numero 2, quindi l'anno va davanti e la tappa va su due cifre. La regola che esce è in `AGENTS.md`: un valore di default che sostituisce un dato mancante non è un dato, è una sparizione silenziosa. |
| 04/10/2026 | 0.20 | **Un PNG che si annuncia come un'immagine e non lo è, con tre controlli verdi.** I disegni degli ambienti avevano l'intestazione RGB e un byte per pixel: la tela teneva l'indice del colore e l'indice finiva nel file al posto di un byte di canale. `verifica_immagini.py` e i tre controlli sui disegni guardavano l'intestazione e lo sha, e il file passava. È stato `png_terrarium.decodifica_png` — il lettore che il motore usa — a non aprirlo. **D4** è il controllo nuovo: decodifica il file e confronta i pixel con la misura dichiarata, e **E6** lo prova iniettando proprio quel difetto. I colori vengono ora dalla tavolozza e sono dichiarati nell'indice. La stessa malattia del file delle sagome (il conto vero e la forma falsa) e delle trenta immagini identiche: **un controllo che guarda una metà del file è verde come un controllo che non guarda niente.** |
| 04/10/2026 | 0.19 | **Il settimo numero che non guardava, e il più subdolo: il conteggio delle sagome era vero e la geometria era un punto.** `dati/edifici_footprint.json` dichiarava **5209 sagome** e i 5209 erano veri — 5209 edifici con nome, altezza e fonte — ma la forma si scriveva con `round(x / Q)` invece di `round(x * Q)`, e ogni vertice finiva a zero: l'ingombro più grande misurava **cinque centimetri quadrati**. Nessuno lo vide perché il numero, la parte che un umano guarda, era giusto. Il file è stato rigenerato (**7322 edifici su 188 aree**, interrogando anche i 150 pin dei livelli, non solo le città: i pin del registro sono città intere e le tappe dell'anno 1 sono a più di due cento metri dal pin di Ferrara). La perdita nella quantizzazione è ora un controllo **alla fonte**: l'edificio la cui forma non sta nella scala dell'area dichiarata viene scartato e contato. `verifica_sagome.py` (**S1–S3**) sul file rotto ne trovava **5209 su 5209** e ora dà 0. `disegna_ambienti.py` fa i **30 disegni schematici** dell'anno 1 e `verifica_disegni.py` (**D1–D3**) li sorveglia; è stato D3 a vedere che tre coppie di immagini erano identiche, perché il riquadro era la griglia del livello e il ritaglio buttava fuori tutti gli edifici. Cinque difetti iniettati, cinque visti, e una prova che aveva un difetto suo — la copia di sicurezza teneva il sorgente invece del file sovrascritto. §3terdecies. |
| 04/10/2026 | 0.18 | **Diciassette file che il commit precedente aveva lasciato nel ramo, e due famiglie diverse nella stessa cartella.** Sei erano **emblemi superati** — le persone passate da emblema a ritratto — e la regola che li toglieva dal ramo guardava solo il prefisso `ritratto_`: sei file, quattro immagini distinte, lo stesso difetto dei sessanta emblemi di quattro giorni prima. Gli altri **undici erano i disegni della piazza della Cattedrale** — facciata, cartello, lapide, due statue, il protagonista in quattro fotogrammi, tre ritratti a mano — e nessun codice li caricava e nessun dato li nominava: il controllo 2 li chiamava file morti e aveva ragione. Ora sono la tabella `SPRITE` di `sorgenti/ambienti_livelli.py`, col posto riletto dalla tabella 3 di `tappa-1-01.md` e la misura misurata sul PNG; tre controlli nuovi (**9**, **10**, **B9**) e la prova dei difetti da undici a **sedici**, due dei quali pretendono che a mordere sia il controllo giusto e non un altro che morde per caso. In `out/` restano due famiglie — 198 per le persone, 11 sprite — e il controllo 2 sa dire quale è quale invece di contare. Chiude anche il secondo sospeso: il **foglio degli emblemi** è ora `sorgenti/art/foglio_emblemi.py` e il suo file `sorgenti/art/foglio_emblemi.txt`, in caratteri, con i numeri calcolati. |
| 04/10/2026 | 0.17 | **Sessanta emblemi che erano diciotto file, e il controllo che non c'era.** L'emblema era un rettangolo con una diagonale il cui seme era `sum(ord(codice)) % 22`: sessanta persone, **diciotto file distinti**, dieci persone con lo stesso identico PNG. Nessuno dei sei controlli lo vedeva, perché tutti contavano i file e non i file distinti. Nuovi: il **controllo 7** (gli sha256 distinti devono essere tanti quanti le persone, e il difetto si dichiara con i nomi) e il **controllo 8** (ogni emblema dichiara la famiglia, ricalcolata dal motivo, e la parola che l'ha fatta vincere); `sorgenti/art/emblema.py`, che disegna il segno geometrico della famiglia, le iniziali e la firma, con i colori letti dalla tavolozza e senza librerie. Il controllo 7 ha trovato subito anche **tre doppioni d'identità fra i ritratti** — `augusto`/`ottaviano augusto`, `copernico`/`niccolò copernico`, `federico ii`/`federico ii di svevia`, sei voci per tre persone — chiusi con tre alias **dichiarati** in `catalogo_immagini.py` e non con una regola che avrebbe unito anche «il territorio del Po» e «i Bersaglieri del Po». Il catalogo passa a **198 persone** e 138 ritratti. Il secondo difetto l'ha trovato la prova, non io: il controllo 8 confrontava la parola ricalcolata **con sé stessa**. Il terzo l'hanno trovato gli occhi, guardando il foglio: font 3×5 che rendeva `DOM` come `DOH`, arco della volta tracciato con una soglia non simmetrica, fessura dell'anello di 24 gradi che toglieva metà del segno. La prova dei difetti passa da sei a **undici**. Dettaglio in §3undecies. |
| 04/10/2026 | 0.16 | **Il quarto numero che invecchiava, e il più semplice di tutti: quanti file ha `dati/mappe/`.** Quattro documenti ne parlavano e avevano dato **quattro numeri diversi** — 25 (`mappe.md`), 23 (`README.md`, due volte), 21 (`AGENTS.md`), 19 (`fonti-visive.md`, che è il conto dei soli file di Natural Earth) — e il peso era doppio: 1,6 MB e 1,4 MB su un conto di **1,52**. Nessuno li confrontava. Il difetto vero è sotto: **nessun file di quella cartella dichiarava da dove viene**, perché il generatore tiene la fonte in una lista Python e il dato non la porta con sé. Nuovi `dati/mappe_manifest.json` (v1, con conti calcolati sui file veri e regge di stare in `dati/` e non in `dati/mappe/`), `sorgenti/gis/mappe_manifest.py`, `sorgenti/gis/verifica_inventario_mappe.py` (I1–I8, dodici frasi in quattro documenti) e `sorgenti/gis/prova_difetto_mappe_manifest.py` (dieci difetti iniettati, tutti visti). Il difetto più subdolo è stato **nel controllo**: la lista `problemi` veniva riassegnata a metà del corpo e l'assegnazione svuotava I4 e I5, due controlli che potevano solo scrivere nella spazzatura. Dettaglio in §3decies.
| 04/10/2026 | 0.15 | **Il contatore confrontava l'audit con se stesso, e quattro numeri che quattro documenti riportavano non li contava nessuno.** `conta_questioni.py` ora confronta cinque cose: la tabella del §1, le due frasi in prosa, **il numero delle sezioni**, i **numeri per documento del §4** con la loro somma, i **numeri in lettere** e **i numeri che il README copia**; il registro delle modifiche è escluso, dichiarando perché. I quattro difetti trovati sono nelle versioni: sezioni 15 su **16**, `itinerari.md` fuori da ogni intestazione del §4 (la sua voce era contata e non elencata), `fonti-visive.md` 2 su **1**, `anno3-europa.md` 7 su **6**, `furioso.md` 2 su **1**, il §6 con **ventotto** chiuse su **31**, il `README.md` con **sedici** documenti su **31**. Il quinto difetto è nel confronto stesso: il dizionario delle parole italiane non riconosceva **`trentuno`**, **`ventuno`** e **`ventotto`** — le tre forme in cui una parola non si somma — e il confronto delle lettere **ignorava in silenzio i numeri che il documento scrive in lettere**. Nuovi: `sorgenti/lingue/prova_difetto_questioni.py`, quindici difetti iniettati tutti richiesti a essere visti, su una copia di tutti i documenti, più la prova che il registro **non** viene morso. Dettaglio in §3novies.
| 03/10/2026 | 0.14 | **Le due lacune che Pietro aveva affidate sono chiuse, e nessuna delle due si è chiusa scegliendo.** Il **mezzo del quinto anno** non era una scelta fra ventidue mezzi: era una domanda su che cosa si dichiara quando la risposta è di qualcun altro. La risposta sono **due strati** — il mezzo reale, che è l'archivio e dunque il presente (`aereo` 30 su 30), e il mezzo della stanza, che è quello attestato dal canto (a piedi 21, carro di serpenti 4, ippogrifo 3, sirena 2) — e il carro di delfini e il drago restano senza tappa, dichiarato. I **codici dei facoltativi** rendono la regola della `premi.md` verificabile su tutti: i 269 sono occorrenze e dietro ci sono **248 persone**, 50 già codificate, 10 collegate, 188 nuovi fino a **Q519**, zero da verificare.
  - **il difetto che il mezzo ha smascherato**: `percorsi_mezzi.py` pubblicava «aereo 26, treno 1» per il quinto anno coprendo **27 tappe su 30**; le tre saltate (5-3, 5-6, 5-20) venivano scartate da un `continue` muto. Un conteggio che scarta e non lo dice descrive un anno che non esiste;
  - **il difetto che i codici hanno smascherato**: **10 persone avevano due codici** nei cataloghi degli anni, perché la serie dell'anno 1 e quella degli anni 2-5 sono due serie diverse. Mancava un indice unico — lo stesso difetto già visto sulle immagini. `indice_persone` dichiara il canonico e gli alias;
  - **la `premi.md` non è più verificabile solo sui 150 obbligatori**: con i 248 facoltativi codificati la copertura è dell'intera scheda, e quello che resta è la B1, che è una decisione di Pietro e non un lavoro;
  - nuovi `sorgenti/dichiara_mezzo_quinto.py`, `sorgenti/codifica_facoltativi.py` e `sorgenti/verifica_codici.py` (cinque controlli, verde); `dati/videogioco-5-duchi-facoltativi.json` è il nuovo catalogo.
Il conto di §1 passa a **118 voci, 31 chiuse, 87 aperte**: le quattro bloccanti non cambiano, perché nessuna delle due lacune era bloccante.
| 03/10/2026 | 0.13 | **I cataloghi dei personaggi degli anni 2, 3, 4 e 5 esistono: sono i quattro file `dati/videogioco-5-duchi-anno{2,3,4,5}-personaggi.json`, con le 120 schede.** Fino a ieri l'unico anno con un catalogo in `dati/` era il primo (93 schede), e gli altri quattro avevano **centoventi schede scritte a mano dentro i documenti**, mentre `anno2-penisola.md` §6.3 dichiarava da generare un catalogo di **130 voci** che nessun file aveva mai soddisfatto. La `premi.md` §3 pretende che ogni premio abbia una fonte dichiarata: senza i cataloghi la verifica si poteva fare solo sui 150 obbligatori e il progetto non poteva dichiarare di coprire tutta la scheda.
  - **`sorgenti/lingue/catalogo_personaggi.py`** raccoglie quello che è già scritto e **non completa niente**: i campi che i documenti non scrivono (`note_verifica`) restano a `null` **con il motivo accanto**, perché un campo a `null` con la ragione è diverso da un campo assente, e il secondo è un difetto;
  - ogni scheda porta la sua **destinazione** (obbligatoria o facoltativa) con **la prova** che l'ha abbinata — `codice`, `nome_normalizzato`, `nome_senza_articoli`, `nome_parziale` — e le ambiguità (una scheda abbinata a due tappe) sono dichiarate, non risolte scegliendo la prima;
  - **tre difetti reali, tutti trovati mentre si scriveva il generatore.** *Primo*: le righe delle schede hanno **più campi insieme** (`**Periodo:** … **Luogo:** … **Pin:** …`) e la prima versione del parser leggeva una riga come un campo solo: `luogo`, `pin`, `strato` e `attendibilita` risultavano vuoti su **tutte e 120 le schede**, senza che il sintomo dicesse perché. *Secondo*: la `forza` è scritta nelle schede del terzo, quarto e quinto anno ma **nel secondo c'è solo nella tabella §4**, una volta su trenta — leggerla dalle sole schede avrebbe dato trenta forze nulle, cioè un dato falso. *Terzo*: il titolo di `Q92` è scritto con un corsivo che non chiude dopo la parentesi (`*(collettivo): progettisti, …*`) e quella scheda non abbinava niente;
  - **la verifica che conta**: il generatore confronta i **collettivi** del catalogo con la **cifra scritta a mano** nel §4 di ciascun documento (3, 1, 2, 3) ed è verde su tutti e quattro. È il controllo che avrebbe morso il difetto del §3 del registro precedente, ed è quello che va rifatto a ogni rigenerazione: l'anno 5 è già stato corretto una volta perché la frase contava a memoria invece di contare la tabella;
  - **quello che non è risolto, e va detto**: le 120 schede sono i **centoventi** obbligatori dei quattro anni. I **269 facoltativi** sono in parte nomi che il catalogo non contiene, e per quelli la scheda **non esiste e va scritta** — è il catalogo esteso delle 130 voci. La `premi.md` è quindi verificabile sulle 120 schede e **non** sui facoltativi.
**Il conto di §1 è cambiato, e il difetto non era nel numero ma nel controllo che lo doveva confermare.** `conta_questioni.py` cercava la forma di prosa «**N** chiuse», che l'audit non usa: i suoi numeri stanno in una **tabella**, e la ricerca non trovava niente. Il controllo passava da mesi senza aver guardato niente — verde come un controllo che guarda, ma il suo verde non significava niente. Il conto reale è **118 voci, 30 chiuse, 88 aperte** (l'audit ne dichiarava 115/29/86, il README 114/29/85: **tre numeri diversi per la stessa cosa**). La tabella ora è letta, e il controllo confronta anche le due frasi in prosa del §1; con un difetto iniettato morde. È il **quarto** caso in tre giorni della stessa regola — dopo i 99 ambienti, i 57 controlli sulle mappe e le 2 voci collettive — ed è il primo in cui il difetto è nel controllo e non nel testo.
La Q2 di `itinerari.md` passa da aperta a **chiusa al primo gradino**, e resta aperta la parte che riguarda le 130 voci del catalogo esteso.
| 03/10/2026 | 0.12 | **Gli incontri dei centocinquanta livelli erano sparsi in tre documenti, e in uno di quelli il numero era sbagliato.** Nasce `videogioco-5-duchi-itinerari.md`: per ogni tappa, **dove si va, con quale mezzo, chi si incontra**, con la voce obbligatoria e i facoltativi distinti. Il conto è **150 tappe, 141 nomi distinti, 269 facoltativi, 9 voci collettive**, e le cifre sono calcolate, non scritte.
**Il difetto che l'ha fatto nascere**: `anno5-mondo.md` §5 dichiarava **2 voci collettive su 30** e la tabella ne porta **tre** — la macchina (5-13), gli ingegneri delle reti (5-18) e **le mani che hanno approssimato √2** (5-6), tutte e tre marcate `collettivo C`. Il documento le contava a memoria invece di leggerle, ed è il terzo caso in due giorni di un numero in letteratura che invecchia (gli altri due: i 99 ambienti con coordinate e i 57 controlli sulle mappe). Il numero è corretto (anno5 v0.6) e la terza voce è **nominata**, perché un conteggio che non elenca è un conteggio che si rifà a memoria.
  - **`sorgenti/estrai_incontri.py`** legge le tabelle degli anni **per intestazione** — la seconda volta che la lezione viene applicata, dopo che `estrai_luoghi.py` aveva letto per numero e messo il filone del *Furioso* al posto della persona in 29 tappe su 30. Ogni voce porta **la prova** che l'ha fatta classificare (`marcatura_nella_tabella`, `codice`, `catalogo_anno1`, `iniziale_maiuscola`): una voce di cui non si sa come è stata decisa è una voce che il prossimo lettore classificherebbe diversamente;
  - **`sorgenti/verifica_incontri.py`**, cinque controlli: **C5** è quello che vale, perché confronta il dato con **la frase scritta a mano** in quattro documenti diversi, ed è l'unico che avrebbe visto il difetto. Provato con difetto iniettato e morde;
  - le tabelle del documento sono **generate** (`genera_itinerari.py`, `aggiorna_itinerari.py`): 150 righe scritte a mano avrebbero finito con una cifra che il dato non conferma. Il mezzo del **quinto anno è dichiarato `non_dichiarato`** perché in quel mese ne sono possibili ventidue e sceglierne uno sarebbe scegliere al posto di Pietro.
Il conto di §1 non cambia: **115 voci, 29 chiuse, 86 aperte**. Le due questioni nuove sono aperte e non bloccanti: il mezzo del quinto anno (`itinerari.md` Q1) e il catalogo dei nomi degli anni 2-5, senza il quale la scheda di **269 facoltativi** non può essere verificata come la `premi.md` esige (Q2). |
| 03/10/2026 | 0.11 | **La B1 aveva il conto sbagliato, e il numero dei premi che Pietro ha deciso è la risposta.** La scheda diceva **32 livelli per tappa** e **cinquantacinque livelli all'ora**: è un errore, sono **sette** (uno di informatica e uno per ciascuna delle sei lingue) e quindi **7 × 150 = 1050**. Il conto è stato rifatto sui dati, dove ogni tappa linguistica ha già sei righe, una per lingua — cioè i 900 titoli sono costruiti su questa forma da prima che la domanda fosse posta. **La B1 e il numero dei premi sono la stessa domanda**, e i **1050 premi** che Pietro ha deciso equivalgono a *sette livelli per tappa, tutti nella stessa tappa*. Aggiunte **le tre proposte** (A: uno per lingua a scelta del giocatore; B: tutti e sette; C: una principale e le altre a rotazione), con la raccomandazione per **A con la rotazione dichiarata**, perché un ragazzo studia due lingue, non sei, e perché la sfida a mani nude ogni quindici livelli deve restare ogni quindici tappe.
Nello stesso giorno è entrata **Q4bis** in `lingue.md`, che risponde a «che cosa significa che il gioco non sa disegnare la propria lingua dei segni»: significa che **non può produrre il segno**, non che la LIS non possa stare nel gioco. Il numero che mancava è contato e fermo: **55 video in LIS su Commons, tutti con licenza libera (zero non liberi), e 49 con il testo italiano parallelo già nella fonte** — i 49 articoli della Convenzione ONU sui diritti delle persone con disabilità tradotti dal CNR ISTC. Le tre strade che sembravano risolvere il gioco intero sono escluse e per motivi diversi: **SiGIL** (il progetto italiano, traduzione LIS ↔ italiano con avatar che segnano) non è su GitHub e si prende per accordo; **SpreadTheSign**, con oltre 600 000 segni in 23 lingue, dichiara *«It is not allowed to download or use our videos or data without permission»*; **SignAvatars** (ECCV 2024) chiede un modulo e **non contiene la LIS**. Nuovo `cerca_video_lis.py` e `dati/lingue/video_lis_disponibili.json`. Il conto di §1 passa a **115 voci** perché Q4bis è una voce nuova, e resta con **29 chiuse e 86 aperte**: **la B1 resta aperta** perché le proposte sono tre e la scelta è di Pietro. |
| 03/10/2026 | 0.10 | **Un punto di «cosa c'è da fare» era chiuso da due giorni, e insegnava una cosa che nessun controllo sapeva.** In `mappe.md` §11 il punto 8 chiedeva gli ambienti dei centocinquanta livelli: il file c'era, al 150 su 150. Chiudendolo sono tornato alla sezione che l'aveva prodotto e **i numeri scritti non erano più quelli del file**: 99 coordinate contro 100, 69 sagome contro 68, `citta_antica` 11 contro 12, `percorso` 11 contro 10, tre cifre nei vuoti, e la frase che dava alla 1-1 un orientamento che non ha come **nessuno** dei centocinquanta. Le sette verifiche degli ambienti passavano tutte, perché confrontano **i dati fra loro** e nessuna confronta un dato con **le frasi che il documento scrive su di esso**. Il controllo che mancava è **B8** (`verifica_ambienti.py`): legge `fonti-visive.md` §3.6 e confronta ogni numero con il conto, e ne ha trovati sette in una volta sola; è stato poi provato con difetti iniettati su tre vie e morde tutte. Le due frasi che il file scrive su se stesso sono ora **calcolate** in `ambienti_livelli.py`: dicevano «le 51 tappe» quando le ipotesi erano 50. Aggiunta **§3quinquies**. Il conto di §1 non cambia: **le voci sono ancora 114, 29 chiuse, 85 aperte e quattro bloccanti**, perché un difetto di prosa non è una voce. |
| 03/10/2026 | 0.9 | **La parte orale è un documento, e il README aveva un difetto che nessun controllo vedeva.** Nasce `videogioco-5-duchi-parlato.md` (v0.2): la Web Speech API è esclusa perché manda l'audio ai server di Google, il riconoscimento on-device è dichiarato non fatto (non esiste per il ferrarese e riguarda dati di un minore), e il gioco può comunque allenare il parlato misurando **durata, pause, ritmo e riascolto**. Il dato che decide: su Commons ci sono **89 381** registrazioni inglesi, **9 179** italiane e **zero** ferraresi — la lingua di cui il progetto ha più bisogno è l'unica che non ha audio libero, e la risposta è produrlo chiedendo a chi lo parla, come si fa per la LIS con la categoria K. Cinque decisioni restano a Pietro (`parlato.md` §6).

**Il difetto.** Mizando la tabella dei documenti del README, uno script ha scritto la versione nella cella del nome del file: **otto righe su trenta avevano perso il documento che descrivevano**, e la coerenza riportava **zero** perché una riga senza nome non nomina nessun documento e quindi non può contraddirlo. Ricostruite a mano, e il controllo che mancava è scritto: ogni riga numerata nomina un file che finisce in `.md` e finisce con una versione. Provato con un difetto iniettato, e morde.

| 03/10/2026 | 0.8 | **Sei voci chiuse, e una di loro non era una domanda: era un difetto.** Aggiunta **§3ter**. Il **numero dei livelli trasversali** è chiuso — sono **zero**, perché il trasversale è un aggancio dentro i livelli e non un livello (`quadro-trasversale.md` §1.3) — e con esso il conto dei premi, che è **1050 e non i «circa 900»** che il progetto portava da tre giorni: la cifra vecchia contava i soli livelli linguistici e dimenticava i centocinquanta informatici. La **variante dei premi** e il **premio della LIS** erano già chiuse oggi e sono qui raccolte. La **`osservazione e attenzione`** era dichiarata `da_costruire` in due documenti con la frase che «il gioco non ha mai lavorato sull'attenzione come oggetto», ed è un difetto: il dominio esiste in quattro posti che nessuno aveva messi insieme (il nucleo `Q8.2` del livello 3-27, l'osservazione linguistica dei novecento livelli, le tappe 1-23 e 1-29, la 5-11). La lezione che vale è la regola: **una cosa che il gioco fa senza dirlo non è una lacuna, è una riga rimasta indietro**.

La **3-28** è chiusa: era la divergenza dichiarata fra registro e documento (Manchester e Torino) e l'ha chiusa la rigenerazione, che ha portato le divergenze da una a zero. La **4-16** è chiusa *davvero*: era un dato corretto a mano che nessuno poteva rifare, e ora la catena `estrai_luoghi.py` → `coordinate.py` → `classifica.py` lo produce. Eseguendola sono usciti **tre difetti che nessun controllo vedeva**: l'estrattore leggeva le colonne per numero e nell'anno 5 leggeva la stanza al posto della voce (29 tappe su 30 con il filone del *Furioso* al posto della persona); le correzioni di Baghdad e Karakorum vivevano solo in un JSON editato a mano e sparivano alla prima rigenerazione (ora stanno in `dati/luoghi_correzioni.json`); e `classifica.py` aveva due copie divergenti della regola che assegna lo stato della coordinata. Il nuovo `sorgenti/verifica_catena_luoghi.py` ne ha cinque. Il conto di §1 non cambia: le sei voci di oggi non erano voci dell'audit.

|---|---|---|
| 03/10/2026 | 0.7 | **La B1 è spiegata in parole semplici, e due buchi che erano dichiarati aperti sono chiusi.** Pietro ha chiesto di capire la B1 «meglio, con parole più semplici»: sotto la scheda c'è ora **B1 in parole semplici**, che dice che cosa sono i 150 livelli informatici e i 900 linguistici, quale sarà la schermata che il ragazzo vede nella tappa 5-12 (**un compito solo, 32 compiti in fila, o tappe alterne**), che cosa è già costruito e che cosa è bloccato, e che la stima delle schermate — cioè la cosa che servirebbe per decidere — dipende da un prototipo che non esiste. **La domanda è di Pietro e resta aperta.** Intanto sono chiuse tre cose: la **Q6.2** (`furioso.md` §4.12: nessuna stanza ha un disegno proprio, quattro regole, tempo di Pietro **zero**), le **51 ipotesi di coordinata** (`luoghi.md` §4.8: 28 documentate, 21 argomentate con il raggio in metri, 2 immaginate e senza punto; regole **R1-R6** e controllo **B7**) e **l'anno 1**, che non era coperto da nessun controllo dei pin e ora ha cinque controlli suoi, **A1-A5** (`mappe.md` §8ter: **30 tappe su 30 dentro le mura**, e soprattutto **0 tratti fuori sui 29** percorsi fra tappe consecutive, che è l'unico controllo che solo una città dentro le mura può avere). Le 51 ipotesi hanno anche fatto nascere i **mezzi** dell'anno 4 e 5: 22 mezzi, con l'anno di attestazione di ciascuno e un controllo di anacronismo **per tappa** che ne ha trovato uno nella stessa impostazione (`percorsi.md` §1.2). Il conto passa a **29 chiuse** e **85 aperte**; le quattro bloccanti restano quattro e sono le stesse: nessuno dei lavori di oggi le toccava, perché sono lavori che si possono fare senza la risposta. |
| 03/10/2026 | 0.6 | **Quattro importanti chiuse in un giorno, e la quarta ha portato con sé un difetto che le altre tre non avevano trovato.** I colori dei fondi geografici (I19, `fonti-visive.md` Q4) sono in `dati/fonti_visive/colori_cartografici.json`, **19 voci**, con la regola che una categoria con il riempimento ha anche il bordo e i due verificatori che la tengono ferma (`verifica_colori.py`, C1–C7). **Cercandoli è emerso che `dati/mondo_admin1_copertura.json` stava dentro `dati/mappe/`**, dove vale la regola del solo formato a delta, e faceva crashare il lettore delle mappe con un `IndexError` che non diceva niente: il file è stato spostato in `dati/` e il lettore ora solleva un `ValueError` che nomina il percorso. Nello stesso giorno sono entrati i **tre file delle cime** con la loro quota (`mappe.md` §2.5), e la scoperta che vale più dei tre file: la fonte è **mondiale in tutte e tre le scale** e i tre file **non sono annidati**, quindi un motore che li trattasse come risoluzioni diverse dello stesso elenco sbaglierebbe senza che nessun controllo lo vedesse. Chiusa anche la **Q6.1** del *Furioso*: `F11` è dichiarato filone **non assegnato** e la decisione è nei dati (`citazioni.json` v4), tenuta ferma dalla verifica **F16**. Il conto passa a **28 chiuse** e **86 aperte**, e le importanti da sedici a **quindici**. Le quattro bloccanti restano quattro e sono le stesse di prima: nessuno dei quattro lavori le toccava. |
| 03/10/2026 | 0.5 | **Tre importanti chiuse in un giorno, e le tre erano lavori, non domande.** La tavolozza (`fonti-visive.md` Q1), le sagome degli edifici (Q2) e il fondo di Ferrara (Q3) sono prodotti il 03/10/2026: `tavolozza.json` con 18 voci, `edifici_footprint.json` con 5209 sagome su 54 luoghi, `ferrara_fondo.json` con 14 tratti di mura e 4,20 km². Nello stesso giorno è entrato `mondo_admin1.json`, il file amministrativo mondiale che chiude la copertura mancante di `mappe.md` §8bis, e `ambienti_livelli.json`, un ambiente per ciascuno dei 150 livelli. Il conto passa a **26 chiuse** e **88 aperte**, e le importanti da diciannove a **sedici**. La lezione che si vede nel conto è la stessa di B5: **nessuna delle tre aspettava una decisione**, e nessuna delle ventisei chiuse è bloccante. Le quattro bloccanti restano quattro e sono le stesse di prima: nessuno dei tre lavori le toccava. |
| 02/10/2026 | 0.4 | **Il quinto anno passa dagli stessi controlli.** `verifica_pin.py` è stato generalizzato (`--anno N`, `--tutti`) e ha coperto i 30 slot del quinto anno: **15 posti con coordinate, nessun difetto**. Il quinto anno ha però prodotto due errori nella **tabella degli attesi** del verificatore (Rotterdam), secondo caso dopo Castel del Monte. `mappe.md` sale a v0.6 e §8bis porta il conto completo di tutti e cinque gli anni: **120 slot, 71 con coordinate**. Aggiunto in §8bis che l'**anno 1 non è coperto**, perché i suoi pin prendono il confine dal WFS del Comune. Il resto del documento non cambia: il conto è 114 voci, 23 chiuse, 91 aperte, quattro bloccanti. |
| 02/10/2026 | 0.3 | **B5 chiusa.** La verifica dei pin degli anni 2, 3 e 4 è fatta (`sorgenti/gis/verifica_pin.py`, otto controlli, tutti superati): 53 slot di pin con coordinate su 90, e **due difetti reali corretti** — Baghdad a 34 km dal proprio centro, Karakorum in Cina invece che in Mongolia. Il numero 90 era esatto ma era il numero degli **slot**, non dei pin distinti: dietro ci sono 69 posti. Il conto passa a **23 chiuse** e **91 aperte**, e le bloccanti da cinque a **quattro**. Aggiunta **§2bis**, che dice cosa è costato e che cosa resta (nove pin senza unità amministrativa, per copertura del file e non per difetto). Rimando a `mappe.md` aggiornato a v0.5. |
| 02/10/2026 | 0.2 | La **lista operativa**. Il contatore è stato corretto perché vedeva tredici documenti su quindici e sbagliava il conto: ora sono **114 voci**, 22 chiuse e **92 aperte**, con i documenti nuovi (`lingue.md`, `lingue-immagini.md`, `percorsi.md`, `fonti-visive.md`) dentro. Ogni bloccante e ogni importante ha **pro, contro, valutazione e responsabilità**; le altre settantatre sono in sintesi con chi decide. Registrata una doppia domanda (`lingue.md` Q5 = `anno5-mondo.md`) e la catena B1 → B2 → B4. |
| 02/10/2026 | 0.1 | Prima stesura. Le dodici sezioni «Questioni aperte» allora esistenti, **96 voci**, 22 chiuse e 74 aperte, cinque bloccanti, e la catena delle dipendenze. |
