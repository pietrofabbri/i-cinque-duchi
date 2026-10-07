---
titolo: Videogioco "I cinque duchi" — Metodo: come si lavora ai dati, ai controlli e ai documenti
tipo: normativo
versione: 0.1
data: 2026-10-06
autore: Pietro Fabbri (con Claude)
documenti collegati: videogioco-5-duchi-storico.md (v0.8)
---

# Metodo

Queste sono le regole con cui si lavora al progetto, per chiunque lo riprenda: una persona o un'IA, con o senza il contesto delle conversazioni in cui il progetto è nato. Valgono come `AGENTS.md`, che le richiama.

Ogni regola è scritta al presente e dice **come si fa rispettare**: quale controllo la guarda, o quale strumento la applica. Il difetto da cui è nata è nello storico (`storico.md`), e non serve conoscerlo per applicarla.

## 1. I controlli

### 1.1 Un controllo che non è mai stato visto fallire non è un controllo

Ogni verificatore ha una prova del difetto: un'opzione `--difetti` che inietta i difetti che deve vedere, uno alla volta, su una copia, e pretende di vederli tutti. `python3 sorgenti/verifica_prove.py` (**X1-X6**) esegue davvero le prove in processi nuovi, invece di accettare che l'opzione esista, e tiene il conto dei controlli che una prova non ce l'hanno ancora: quel numero è scritto nel `README.md` ed è un debito dichiarato.

Un controllo che legge il proprio file dentro `main()` non si può provare. I controlli prendono i loro input dalla chiamata — `controlla(doc)`, `controlla(doc, dati)` — e la prova fa girare gli stessi controlli su una copia rotta.

### 1.2 Una prova che non rimette a posto il progetto è un danno

Una prova che rompe un file vero lo rimette subito, con una copia di sicurezza **del file sovrascritto** (non del sorgente), tenuta fuori dal progetto. Il ripristino avviene prima della prova successiva, e alla fine la prova pretende che il verificatore torni verde: una prova che non chiede il verde finale non dice se ha lasciato il progetto com'era.

### 1.3 Un controllo che verifica la forma non verifica la premessa

Un record ben costruito può poggiare su un dato sbagliato. Quando un controllo dice che un record è coerente, la domanda successiva è **da dove viene il dato su cui il record è costruito**, e se quella fonte è a sua volta controllata.

### 1.4 Un numero scritto a mano invecchia, un numero calcolato no

1. **Un numero in un documento viene dal conto, non dalla memoria.** Dove si può, la frase che riporta il numero è costruita sul valore calcolato (per esempio, `ambienti_livelli.py` scrive le frasi sui propri conti).
2. **Se un documento riporta i numeri di un file, un controllo li confronta col file.** Quando si aggiunge una sezione con dei numeri, si aggiunge anche il confronto, come fa **B8** in `verifica_ambienti.py`.
3. **Lo stesso vale per i comandi e per i conteggi dei controlli**: una riga che dichiara un numero di controlli sbagliato, o uno script nella cartella sbagliata, è un difetto della stessa natura.
4. **I numeri in lettere sono numeri.** «Le quattro bloccanti» si converte e si confronta come «4».
5. **Un numero che descrive il passato non si confronta con il presente.** Le righe dei registri delle modifiche e lo storico sono esclusi dai confronti, ed è dichiarato.

`python3 sorgenti/verifica_numeri.py` (**N1-N5**) tiene l'inventario di tutti i numeri scritti in prosa e pretende che ogni documento o abbia un controllo che legge i suoi numeri, o dichiari in `dati/buchi_aperto.json` perché non ce l'ha. Le righe del `README.md` che riportano i conti dei verificatori si aggiornano con `python3 sorgenti/allinea_conti_readme.py`, non a mano.

### 1.5 Un controllo guarda che cosa conta, non solo quanto

Un file che dichiara un conteggio ha anche un controllo che guarda **che cosa** ha contato: un conteggio vero può stare accanto a una geometria vuota, a un'immagine illeggibile, a un carattere che il font non disegna. Un difetto che entra in un file si propaga a ogni lettore, quindi si ferma **alla fonte**, e il fermo si scrive come uno scarto contato, non come un valore che non viene scritto.

### 1.6 Un valore di default che sostituisce un dato mancante è una sparizione silenziosa

`dizionario.get(chiave, [])` su un dato che deve esserci, o `get(chiave, 0)` su un conteggio, fanno sparire il dato mancante senza dirlo. Dove un dato deve esserci, la sua assenza è un errore che si dichiara, non un valore vuoto.

### 1.7 Un controllo scritto per un campione non copre l'insieme

Quando il dato si allarga, un controllo **si riscrive, non si tara**: la domanda non è «come faccio perché passi?» ma «che cosa deve essere vero quando il dato è più grande?». Per esempio, **D3** in `sorgenti/art/verifica_disegni.py` non chiede che tutti i disegni siano diversi (sull'insieme non è vero), ma che dati uguali diano disegni uguali e dati diversi disegni diversi.

Un generatore che scrive un manifesto unico può cancellarne metà senza dirlo, se lo si lancia su una parte: si usa l'opzione che lavora sull'insieme (per i disegni, `--tutte`).

### 1.8 Un elenco si confronta con la fonte che lo genera, non con se stesso

Un file che confronta solo se stesso è verde anche quando manca metà del mondo. Un elenco di voci si confronta con la fonte da cui le voci vengono (per esempio **M1** in `verifica_fonti_visive.py` legge `percorsi_mezzi.py` e pretende una riga per ogni mezzo), e ogni voce ha una delle forme ammesse — un dato, o un vuoto con la sua ragione — mai una terza forma che è «non ci ho pensato».

## 2. I dati

### 2.1 Un dato corretto a mano è un dato che nessuno può ricostruire

Un file generato non si corregge a mano: la correzione sparisce alla prima rigenerazione. Una correzione trovata da un controllo va in un file di correzioni che il generatore riapplica, con la fonte e il controllo che l'hanno trovata (per i luoghi, `dati/luoghi_correzioni.json`), e i campi compilati a mano si portano dietro unendo, non sovrascrivendo.

### 2.2 Le tabelle si leggono per intestazione

Una tabella di un documento si legge per nome di colonna, mai contando le barre: le tabelle degli anni non hanno tutte le stesse colonne. Una riga di tabella si riscrive dalle sue celle, non si taglia.

### 2.3 Una regola sta in un posto solo

Se due script applicano la stessa regola, la regola sta in una funzione sola che entrambi chiamano. Due copie della stessa regola divergono.

### 2.4 Una richiesta che non arriva non è una risposta negativa

Ogni script che parla con un servizio in rete aspetta un tempo minimo fra le richieste, ascolta il `Retry-After` su `HTTP 429`, e distingue `non_trovato` (risposta avuta, niente) da `richiesta_fallita` (nessuna risposta). Una richiesta fallita non chiude mai una scheda: la lascia da rifare. Un verificatore che non può raggiungere la sua fonte lo dice subito e non si dichiara verde (per esempio `verifica_tavolozza.py` esce con il codice 2).

### 2.5 Una ricerca automatica propone, una persona decide

Un nome di file non è una prova, e un file che arriva non è la risposta giusta: una ricerca trova parole, non oggetti. Ogni immagine entra nel gioco solo dopo un giudizio a vista registrato con il suo motivo (`attestazione*.json`). Una parola ambigua si cerca con due parole che non possono confondersi.

### 2.6 Un vuoto si dichiara, non si riempie

Quando un dato non c'è, il campo dice che non c'è e perché: un volume neutro invece di un'altezza stimata, un emblema invece di un volto inventato, un'ipotesi con il suo grado invece di una coordinata scelta in silenzio. Un vuoto non dichiarato è un dato falso.

### 2.7 Prima di dichiarare una lacuna, si cerca

Una riga «da costruire» è la cosa più economica da scrivere, e spesso nasconde un difetto. La domanda da porre prima è **«dove lo abbiamo già costruito senza accorgercene?»**: una cosa che il gioco fa senza dirlo non è una lacuna, è una riga rimasta indietro.

## 3. I documenti

### 3.1 I tipi

Ogni documento dichiara il suo tipo nell'intestazione: `normativo` (che cosa è deciso, al presente), `catalogo` (tabelle generate dai dati), `audit` (le domande aperte e le chiuse), `storico` (come ci si è arrivati), `piano` (il lavoro in corso). Un documento normativo non racconta come si è arrivati a una decisione: la dice, e il racconto va nello storico, alla lettera, con l'indicazione di dove stava. Lo controlla `verifica_coerenza.py` («tipi dei documenti»).

### 3.2 Le versioni e i registri

Ogni modifica al contenuto alza la versione e scrive una riga nel registro delle modifiche, e si fa con `python3 sorgenti/nuova_versione.py docs/<file>.md "che cosa è cambiato e perché"`, che aggiorna anche la tabella del `README.md` e i rimandi negli altri documenti. Aggiornare un rimando di versione o un campo dell'intestazione non è una modifica del contenuto e non alza la versione di chi lo contiene.

Un registro che perde una riga è un documento che mente sul proprio lavoro: `python3 sorgenti/verifica_registri.py` (**R1–R5**) pretende che nessuna versione salti, che nessuna abbia due righe, che il registro sia in ordine, che ogni tabella di registro abbia la riga di separazione e che nessuna intestazione sia scritta due volte.

### 3.3 Le domande aperte

Una domanda nuova va nell'audit, non lasciata in fondo a un documento. Quando si chiude, il suo esito va nella tabella delle chiuse dell'audit e il racconto della chiusura nello storico.

## 4. Prima di dichiarare finito

1. Fai girare **tutti** i verificatori (`sorgenti/verifica*.py` e `sorgenti/*/verifica*.py`): devono essere verdi, o dire perché non possono esserlo.
2. Se hai aggiunto o tolto un documento o un controllo, `python3 sorgenti/allinea_conti_readme.py`.
3. `python3 sorgenti/verifica_coerenza.py` per ultimo.
4. Nel messaggio di commit: **che cosa** è cambiato e **perché**.

## 5. Registro delle modifiche

| Data | Versione | Che cosa è cambiato |
|---|---|---|
| 06/10/2026 | 0.1 | Prima stesura (fase 1 della roadmap). Le regole di metodo che stavano in `AGENTS.md` §4, raccontate ciascuna con il difetto da cui era nata, sono scritte qui al presente con il controllo che le fa rispettare; i racconti sono in `storico.md` §3. Entrano anche regole che erano solo nell'audit o nei documenti: il valore di default che fa sparire un dato, la regola in un posto solo, il verificatore che non raggiunge la fonte. |
