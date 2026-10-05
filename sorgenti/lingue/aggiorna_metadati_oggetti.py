#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rilegge gli autori che Commons dichiara, senza ripetere le ricerche.

Il 2 ottobre 2026 il file `dati/lingue/immagini_oggetti.json` era stato scritto
da un estrattore che leggeva due chiavi di metadati. Il 5 ottobre l'estrattore
ha imparato a leggerne tre — `Attribution` è quella che mancava — e subito
dopo è stato trovato che leggeva `autore` prima di assegnarlo, morendo di
`UnboundLocalError` a ogni candidato. Il file non è mai stato rigenerato: non
per una scelta di rimandare, ma perché l'estrattore non girava.

Questo script è la via stretta per rimetterlo in pari senza rifare le 180
ricerche: **non cerca niente**, interroga Commons solo sui titoli che il file
già contiene e ne aggiorna il campo `autore`. La ricerca è un'altra cosa: se si
rifacesse, i candidati cambierebbero tutti insieme, e i diciotto fogli di
controllo — che sono la parte guardata a vista — parlerebbero di un file che
non esiste più. Un aggiornamento dei metadati non tocca le scelte, e quelle le
fa una persona.

La regola di quale chiave leggere non è qui dentro: è `autore_di()` nell'estrattore,
lo stesso posto che usa la ricerca. Una regola copiata in due script è una
regola che un giorno i due script racconteranno diversamente.

Uso:  python3 sorgenti/lingue/aggiorna_metadati_oggetti.py
      python3 sorgenti/lingue/aggiorna_metadati_oggetti.py --secco
"""
import io
import json
import os
import sys
import time

BASE = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(BASE, "..", ".."))
sys.path.insert(0, BASE)

from cerca_immagini_oggetti import autore_di, get  # noqa: E402

DATI = os.path.join(RADICE, "dati", "lingue", "immagini_oggetti.json")

# Commons accetta fino a cinquanta titoli per richiesta; oltre, risponde con un
# avviso e i titoli eccedenti verrebbero silenziosamente persi. Un titolo perso
# in mezzo a mille è un'autore che sparisce senza che nessuno lo dica, quindi il
# limite si tiene basso e ogni blocco viene contato.
PER_RICHIESTA = 50
PAUSA = 0.4


def titoli_che_citano(risultati):
    """Tutti i titoli distinti che il file contiene, in ordine."""
    visti = []
    gia = set()
    for voce in risultati:
        for cand in voce.get("candidati", []):
            titolo = cand.get("file")
            if titolo and titolo not in gia:
                gia.add(titolo)
                visti.append(titolo)
    return visti


def metadati(titoli):
    """I metadati di tutti quei titoli, chiesti a blocchi di cinquanta."""
    trovati = {}
    for inizio in range(0, len(titoli), PER_RICHIESTA):
        blocco = titoli[inizio:inizio + PER_RICHIESTA]
        d = get({
            "action": "query", "format": "json",
            "titles": "|".join(blocco),
            "prop": "imageinfo", "iiprop": "extmetadata",
        })
        if "_errore" in d:
            print("  blocco %d: la fonte non ha risposto (%s), lasciati come "
                  "erano" % (inizio // PER_RICHIESTA + 1, d["_errore"]),
                  file=sys.stderr)
            continue
        # `-1` sta per "titolo assente": non e' un errore, e va distinto dal
        # blocco che non e' arrivato, altrimenti un file cancellato su Commons
        # sembrerebbe una risposta andata bene.
        for pagina in (d.get("query", {}).get("pages", {}) or {}).values():
            if pagina.get("missing"):
                continue
            ii = (pagina.get("imageinfo") or [{}])[0]
            titolo = pagina.get("title")
            if titolo:
                trovati[titolo] = ii.get("extmetadata", {}) or {}
        if inizio + PER_RICHIESTA < len(titoli):
            time.sleep(PAUSA)
    return trovati


def main():
    with io.open(DATI, encoding="utf-8") as f:
        documento = json.load(f)
    risultati = documento.get("risultati", [])
    titoli = titoli_che_citano(risultati)
    print("candidati distinti nel file: %d, in %d richieste"
          % (len(titoli), (len(titoli) + PER_RICHIESTA - 1) // PER_RICHIESTA))

    if "--secco" in sys.argv:
        print("secco: nessuna richiesta fatta, nessun file scritto")
        return 0

    trovati = metadati(titoli)
    print("titoli di cui la fonte ha risposto: %d su %d"
          % (len(trovati), len(titoli)))

    corretti = 0
    aggiunti = 0
    persi = 0
    per_voce = {}
    for voce in risultati:
        for cand in voce.get("candidati", []):
            titolo = cand.get("file")
            if titolo not in trovati:
                persi += 1
                continue
            nuovo = autore_di(trovati[titolo])
            vecchio = cand.get("autore") or ""
            if nuovo == vecchio:
                continue
            corretti += 1
            if not vecchio and nuovo:
                aggiunti += 1
            if vecchio and not nuovo:
                print("  ATTENZIONE %s: la fonte non dichiara piu' un autore "
                      "che il file aveva (%r)" % (titolo, vecchio),
                      file=sys.stderr)
            cand["autore"] = nuovo
            per_voce.setdefault(voce.get("lingua"), []).append(titolo)

    print("autori corretti: %d, di cui comparsi dal nulla: %d"
          % (corretti, aggiunti))
    print("titoli senza risposta (lasciati come erano): %d" % persi)
    if "--scrivi" in sys.argv:
        documento["versione"] = documento.get("versione", 1)
        documento["data"] = time.strftime("%Y-%m-%d")
        documento["nota"] = ("%s Metadati riletti da Commons il %s senza "
                             "ripetere le ricerche: le scelte a vista non "
                             "cambiano, gli autori si."
                             % (documento.get("nota", ""),
                                time.strftime("%Y-%m-%d"))).strip()
        with io.open(DATI, "w", encoding="utf-8") as f:
            json.dump(documento, f, ensure_ascii=False, indent=1)
        print("scritto: %s" % DATI)
    else:
        print("nessuna scrittura: manca --scrivi")
    return 0


if __name__ == "__main__":
    sys.exit(main())