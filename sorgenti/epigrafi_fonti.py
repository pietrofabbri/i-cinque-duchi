#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Costruisce `dati/fonti_visive/epigrafi.json`: le iscrizioni del gioco.

**Un'epigrafe non e' un'immagine: e' un testo, e il testo manca.** Le
ricerche del 02/10 hanno prodotto **18 immagini** di lapidi, lastre e iscrizioni
e **zero testi**. Il testo e' la parte che il gioco usa davvero — e' la domanda
di ripasso, e' il premio **F** del latino e il **C** del greco
(`premi.md` §2.1), ed e' l'unica cosa che distingue un'epigrafe da una foto di
un sasso. Percio' questo file non si chiude dichiarando che manca: si chiude
dichiarando **la fonte da cui il testo arriva** e **la regola per cui un
testo che non c'e' non entra nel gioco**.

Le tre fonti sono state interrogate il 05/10/2026 e hanno tutte detto di no, in
modi diversi, e ognuna con un conto:

  - **Wikidata**: 63048 voci hanno la proprieta' che rimanda alla scheda
    epigrafica, ma e' un **identificatore numerico**, non il testo; e solo 15
    voci hanno anche una traduzione. Il testo non c'e'. Conto dichiarato, non
    ricordato a memoria: la query e' nel file.
  - **Wikimedia Commons**: la pagina dei file prescelti dà titolo, epoca e
    autore ma il campo `inscriptions` del template e' **vuoto** (verificato su
    tre file). L'immagine c'e', il testo no.
  - **EDH** (Epigraphic Database Heidelberg), che e' la fonte giusta —
    82 000 iscrizioni latine con trascrizione — **risponde con una protezione
    anti-robot** a ogni richiesta, pagina e API. Provato tre volte, due domini.

Il progetto vieta che un testo sia scritto dal progetto: quindi i campi
`trascrizione` e `traduzione` sono `null` con la fonte dichiarata, e
`verifica_fonti_visive.py` vieta che un'epigrafe entri nel gioco senza
entrambi.

Uso:
    python3 sorgenti/epigrafi_fonti.py
"""
import io
import json
import os
import sys
import time

RADICE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(RADICE, "dati", "fonti_visive", "epigrafi.json")
CERCA = os.path.join(RADICE, "dati", "fonti_visive", "fonti_visive.json")

# La scelta fra i candidati: il nome del file e il motivo. Tutte e tre sono
# **immagini senza testo**, e il motivo dice perche' quella e' la meno peggio.
SCELTE = {
    "lapide": (
        "File:Funerary stele of Sosibia (Boston MFA 1971.209).jpg",
        "una stele funeraria di persona nota, che e' la forma che il gioco "
        "usa per la lapide; 3460x5352 px e la piu' alta del lotto",
        "senza testo: il campo inscriptions della pagina Commons e' vuoto"),
    "lastra": (
        "File:Marble funerary relief MET DP337516.jpg",
        "un rilievo funerario marmoreo del Metropolitan, di grandezza maggiore "
        "dei cinque simili che la ricerca ha portato",
        "senza testo, e le sei lastre candidate sono tutte lo stesso tipo: "
        "l'antiguità non ha lastre con iscrizioni diverse"),
    "iscrizione": (
        "File:Greek inscription, Eleutherna, 600-450 BC, AM Rethymno, "
        "076104.jpg",
        "un'iscrizione greca di Creta che **proibisce l'eccesso di vino**, che "
        "e' un testo che si può tradurre e usare: e' la scelta perche' e' "
        "l'unica che promette qualcosa",
        "senza testo nella pagina Commons; il testo (le tre righe greche) si "
        "potrebbe prendere da EDH, che pero' risponde anti-robot"),
}

REGOLE = [
    "**Un'epigrafe entra nel gioco solo con la sua trascrizione e la sua "
    "traduzione.** Una foto di un sasso non e' un testo: e' un'illustrazione, "
    "e l'illustrazione la fa il progetto con le sue sagome, non con la fonte.",
    "**Il testo non lo scrive il progetto.** Una trascrizione o una traduzione "
    "redatte qui sarebbero un testo generato, che e' la stessa cosa che il "
    "progetto vieta per le immagini degli oggetti. Se il testo non c'e' nella "
    "fonte, l'epigrafe non entra: si dichiara e basta.",
    "**La fonte del testo e' EDH** (Epigraphic Database Heidelberg, 82 000 "
    "iscrizioni latine, CC BY-SA), con EDR ed EAGLE come alternative per "
    "italiano e greco. Il rimando all'iscrizione e' l'id che Wikidata porta "
    "nella proprieta' P1415, ed e' cid che rende l'epigrafe recuperabile quando "
    "la fonte si lascia interrogare.",
    "**Un'epigrafe senza testo non e' un premio.** I premi F del latino e C "
    "del greco sono «premio da guardare e non da leggere»: se l'epigrafe non "
    "ha testo, il premio che e' la domanda di ripasso non si puo' costruire, e "
    "la tappa resta senza premio finche' il testo non c'e'.",
]

MISURE = [
    {"fonte": "Wikidata Query Service",
     "interrogazione": "SELECT (COUNT(?item) AS ?n) WHERE { ?item wdt:P1415 ?insc }",
     "esito": "63048 voci con la scheda epigrafica, che e' un identificatore e "
              "non il testo; con la traduzione soltanto 15",
     "eseguita": "05/10/2026"},
    {"fonte": "Wikimedia Commons",
     "interrogazione": "action=query&prop=revisions&rvprop=content sui file "
                        "prescelti",
     "esito": "il campo `inscriptions` del template Artwork e' vuoto: "
              "l'immagine c'e', il testo no",
     "eseguita": "05/10/2026"},
    {"fonte": "EDH, due domini e l'API",
     "interrogazione": "pagina dell'iscrizione e API JSON",
     "esito": "risposta anti-robot a tutte e tre le richieste: la fonte giusta "
              "non e' interrogabile da qui",
     "eseguita": "05/10/2026"},
]


def cerca():
    with io.open(CERCA, encoding="utf-8") as f:
        return json.load(f)["risultati"]["epigrafe"]


def main():
    proposte = {v["voce"]: v["candidati"] for v in cerca()}
    voci = []
    for nome, candidati in proposte.items():
        scelto, perche, riserva = SCELTE[nome]
        trovato = next((c for c in candidati if c["file"] == scelto), None)
        if trovato is None:
            raise SystemExit("il file scelto per %s non e' fra i candidati: %s"
                             % (nome, scelto))
        voci.append({
            "voce": nome,
            "candidati": len(candidati),
            "immagine": {
                "file": trovato["file"],
                "url": trovato["url"],
                "licenza": trovato["licenza"],
                "autore": trovato.get("autore"),
                "data": trovato.get("data"),
                "px": [trovato["larghezza"], trovato["altezza"]],
            },
            "perche_questa": perche,
            "riserva": riserva,
            "trascrizione": None,
            "traduzione": None,
            "fonte_del_testo": "EDH (Epigraphic Database Heidelberg), via "
                               "l'identificatore in Wikidata P1415; EDR ed "
                               "EAGLE per italiano e greco",
            "testo_mancante_perche": "la fonte non e' interrogabile da questa "
                                     "sessione: EDH risponde anti-robot e "
                                     "Wikidata non porta il testo",
            "entra_nel_gioco": False,
            "usa_per": {"lapide": "premio F del latino: la domanda di ripasso",
                        "lastra": "premio F del latino: la domanda di ripasso",
                        "iscrizione": "premio C del greco: la domanda di ripasso"},
        })
    file = {
        "versione": 1,
        "data": time.strftime("%Y-%m-%d"),
        "che_cosa": "le tre voci epigrafiche del gioco: l'immagine proposta e "
                    "il testo che manca, con la fonte da cui arriva",
        "regole": REGOLE,
        "misure": MISURE,
        "conti": {
            "voci": len(voci),
            "candidati": sum(v["candidati"] for v in voci),
            "con_immagine": len([v for v in voci if v["immagine"]]),
            "con_trascrizione": len([v for v in voci if v["trascrizione"]]),
            "con_trascrizione_e_traduzione": len(
                [v for v in voci if v["trascrizione"] and v["traduzione"]]),
            "entrano_nel_gioco": len([v for v in voci if v["entra_nel_gioco"]]),
        },
        "voci": voci,
    }
    with io.open(OUT, "w", encoding="utf-8") as f:
        json.dump(file, f, ensure_ascii=False, indent=1, sort_keys=False)
        f.write("\n")
    print("scritto %s" % os.path.relpath(OUT, RADICE))
    print("  voci %d, candidati %d, con immagine %d, con testo %d, che entrano "
          "nel gioco %d" % (file["conti"]["voci"], file["conti"]["candidati"],
                            file["conti"]["con_immagine"],
                            file["conti"]["con_trascrizione_e_traduzione"],
                            file["conti"]["entrano_nel_gioco"]))


if __name__ == "__main__":
    sys.exit(main())