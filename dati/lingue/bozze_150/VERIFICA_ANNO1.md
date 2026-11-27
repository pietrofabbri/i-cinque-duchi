---
tipo: piano
---
# Verifica delle voci dell'anno 1 (27/11/2026)

*Decisione: le 750 voci delle bozze si verificano un anno alla volta, cominciando dall'anno 1 (tappe 1-1 … 1-30, tutte a Ferrara e nel Ferrarese), che è il primo da costruire.*

Per la lingua assegnata, e **solo per le tappe 1-1 … 1-30** del suo file in `dati/lingue/bozze_150/<SIGLA>.json`:

1. Per ogni voce cerca una **fonte di riferimento** che confermi la voce e il suo legame con il luogo (regola 5 di `ISTRUZIONI.md`). Fonti utili per Ferrara: Treccani (Enciclopedia e Dizionario Biografico), Lewis Lockwood «Music in Renaissance Ferrara» (accesso aperto), Musei di Arte Antica e Musei civici di Ferrara, MEIS, Biblioteca Ariostea, Fondazione Estense, Regione Emilia-Romagna (elenco PAT, patrimonio culturale), UNESCO (Ferrara città del Rinascimento e il suo Delta del Po), Comune di Ferrara e Ferrara Terra e Acqua (sito turistico ufficiale), Delta del Po (parco).
2. Se la fonte conferma: `verificata: true`, indirizzo **aperto** in `fonti`, togli la segnalazione se il dubbio è chiuso.
3. Se la fonte smentisce o il legame è debole: **sostituisci la voce** con una verificata dello stesso oggetto, legata davvero al luogo, non già usata altrove nel file (controlla tutte le 150), e scrivi la vecchia voce nel campo `sostituita` con il perché.
4. Se non riesci a verificare: lascia `verificata: false` e scrivi nella segnalazione che cosa manca.
5. Mai inventare; mai costruire indirizzi a memoria.

**Budget: al massimo 30 ricerche web**, condivise con altri cinque lavori in parallelo. Salva il file dopo ogni 10 tappe. A fine lavoro un controllo Python: 150 voci, ordine delle tappe, nessuna voce ripetuta.
