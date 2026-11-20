---
tipo: piano
---
# Bozze delle 150 voci per lingua: istruzioni

*Scritte il 10/10/2026, riscritte il 20/11/2026. Servono a chi (persona o AI) scrive le bozze di `dati/lingue/bozze_150/<SIGLA>.json`.*

**Progetto.** «I cinque duchi», videogioco didattico per un liceo (ragazzi 14–19 anni). Cinque anni × trenta tappe = 150 tappe; ogni tappa è un luogo reale (Ferrara nell'anno 1, la penisola nell'anno 2, l'Europa nell'anno 3, il mondo negli anni 4 e 5). In ogni tappa c'è un livello per ciascuna di sei lingue, e ogni lingua ha un **oggetto di interazione**: italiano → cibi, ferrarese → detti popolari, latino → superstizioni, inglese → musiche, lingua dei segni italiana → artigianato tipico, greco → bevande.

**Decisione di Pietro (il docente, 10/10/2026).** Ogni lingua ha **una voce per tappa, 150, legata al luogo della tappa** (e alla sua epoca, se il luogo è antico). Il modello è la lista dei cibi, già fatta e validata: `dati/lingue/cibi_per_tappa.json`. Le tappe, con luogo, titolo del livello di informatica, duca e piatto, sono in `dati/lingue/bozze_150/tappe.json`. Per i tre luoghi vaghi dell'anno 5 (5-18, 5-22, 5-24) si usa il luogo proposto nella segnalazione del piatto (San Francisco e Palo Alto; il Giappone; Cheltenham).

## Regole

1. **Legata al luogo**, con un legame vero spiegabile in una frase.
2. **Nessuna ripetizione** fra le 150 voci di una lingua. Ferrara compare in 48 tappe: varia molto (quartieri, epoche, persone, istituzioni; la corte estense è ben documentata).
3. **Nome italiano**, con l'articolo, 2–6 parole. Niente nomi dialettali, tranne nel ferrarese.
4. **Mai inventare.** Ogni voce deve esistere ed essere legata al luogo. Meglio una voce più generica ma vera che una specifica inventata.
5. **Validata su testi di riferimento del campo** (richiesta di Pietro del 10/10/2026): enciclopedie (Treccani, Britannica, Grove/Oxford per la musica), registri ufficiali (UNESCO patrimonio immateriale, registri dei mestieri d'arte, DOP/IGP), musei e istituzioni, fonti antiche con il passo preciso (Perseus, LacusCurtius, The Latin Library). Wikipedia serve a orientarsi; il fatto si conferma altrove quando si può. Blog e pagine commerciali no.
6. **`verificata`**: `true` solo se la fonte è stata davvero aperta e conferma voce e legame; altrimenti `false`. Non costruire indirizzi a memoria: un link non aperto va nel campo `fonti_da_controllare`.
7. **Curiosità**: un fatto interessante e verificato, una o due frasi, per un quattordicenne. Facoltativa. Le persone citate verranno presentate nel gioco con una scheda.
8. **Segnalazione**: solo un dubbio aperto. Altrimenti stringa vuota.
9. **Termini immagine**: due o tre termini (inglese o lingua locale) per trovare un'immagine su Wikimedia Commons.
10. Adatto ai ragazzi; l'alcol mai presentato come attraente.

## Formato

```json
{"lingua": "<SIGLA>", "oggetto": "...", "voci": [
  {"tappa": "1-1", "voce": "...", "legame": "...", "curiosita": "...", "segnalazione": "...",
   "fonti": ["url aperti"], "fonti_da_controllare": ["..."], "verificata": true,
   "termini_immagine": ["...", "..."]}
]}
```

Più i campi propri di ogni lingua (`parola_greca`, `latino`, `aggancio_inglese`, `gesto`, `esempio_noto`). 150 elementi nell'ordine delle tappe; un controllo con Python prima di finire (150, tutte le tappe, nessuna voce ripetuta).
