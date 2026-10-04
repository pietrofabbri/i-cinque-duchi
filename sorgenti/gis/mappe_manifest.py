#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Produce `dati/mappe_manifest.json`: da dove viene ogni file di `dati/mappe/`.

**Il difetto che questo file risolve, e perché è un difetto vero.** Il
generatore `mappe_formato.py` sa da dove viene ogni file — la fonte Natural
Earth è nella sua lista `LAVORI`, con lo shapefile e la scala — ma quella lista
sta **in un sorgente Python**, e il file di dati non la porta con sé. Un file
di `dati/mappe/` letto da solo, oggi, non dice nulla di sé: `mondo_110_paesi.json`
potrebbe essere Natural Earth, potrebbe essere un rilievo, potrebbe essere
qualsiasi cosa. Il 04/10/2026 la conseguenza è stata concreta: per contare i
file di quella cartella nessuno poteva farlo dai dati, e i documenti hanno dato
**quattro numeri diversi** — 19, 21, 23, 25 — perché ognuno li aveva copiati a
mano da un momento diverso della storia del progetto.

**La regola è quella del progetto**, detta in `AGENTS.md`: *un dato non si
corregge a mano; e un numero scritto a mano invecchia, un numero calcolato no*.
Qui il numero viene calcolato e la fonte **dichiara** è messa dove la legge
dell'inventario la vuole.

**Perché un manifest e non un campo dentro il file.** Il formato a delta è
`{"q":…, "f":[…], "p":[…]}`, e aggiungere un quarto campo cambierebbe la forma
di venticinque file per farci dire qualcosa che un file accanto già dice. Il
progetto ha già la convenzione: `dati/altitudine_manifest.json` sta in `dati/`
e **non** in `dati/mappe/`, perché lì dentro vale la regola del solo formato a
delta e un JSON ordinario fa crashare `mappe_lettore.leggi()`. Il manifest
obbedisce alla stessa regola, e il controllo `C6` di `verifica_colori.py` —
che già impedisce a un file fuori formato di finire in quella cartella — lo
prende in carico anche per i futuri.

I tre campi che il manifest porta e che prima non esistevano da nessuna parte
come dato:

  `file`     ogni nome, con la **fonte**, la scala, il riquadro e il numero di
             geometrie e punti — letti dai file veri, non dichiarati qui;
  `categorie` il conto per categoria, che è il numero che i documenti citano e
             che nessuno poteva controllare;
  `totale`   il numero di file e il loro peso in byte.

Uso:
    python3 sorgenti/gis/mappe_manifest.py            # riscrive il manifest
    python3 sorgenti/gis/mappe_manifest.py --leggi    # lo stampa e non scrive
"""
import glob
import json
import os
import sys

RADICE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                      "..", ".."))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
MAPPE = os.path.join(RADICE, "dati", "mappe")
MANIFEST = os.path.join(RADICE, "dati", "mappe_manifest.json")

import mappe_lettore                                     # noqa: E402

# Le scale, dalla prima cifra del nome. Il nome del file **non** è la fonte: è
# l'indice con cui trovare la fonte nella lista del generatore, e se un nome non
# ci sta la fonte non si inventa.
SCALA = {"110": "110m (mondo intero)", "50": "50m (Europa)", "10": "10m (penisola)"}

# Le categorie, con il loro produttore. Una categoria nuova non si aggiunge qui
# senza dichiarare **chi** la produce: un file senza produttore è un file di
# cui nessuno risponde.
PRODUTTORI = {
    "natural_earth": "sorgenti/gis/scarica_ne.py -> sorgenti/gis/mappe_formato.py",
    "admin1": "sorgenti/gis/mondo_admin1.py",
    "altitudine": "sorgenti/gis/scarica_ne.py -> sorgenti/gis/altitudine.py",
    "rilievo": "sorgenti/gis/riferimento_altitudine.py -> sorgenti/gis/rilievo.py",
}


def lavori_di_mappe_formato():
    """{nome: shapefile} dalla lista del generatore, se importabile.

    `mappe_formato.py` importa `pyshp` **dentro** `le()` e non è installato su
    questa macchina: si importa il modulo per la lista, che non lo richiede, ma
    se un giorno l'import fallisce il manifest non si ferma — dice che la fonte
    non è disponibile e lascia che sia il controllo a dirlo.
    """
    try:
        import mappe_formato
        return {nome: shp for nome, shp, _tol, _q, _k, _box in mappe_formato.LAVORI}
    except Exception as e:                                # pragma: no cover
        sys.stderr.write("avviso: non riesco a leggere LAVORI (%s); le fonti "
                         "Natural Earth resteranno «non disponibile»\n" % e)
        return {}


def scala_di(nome):
    if nome.startswith("mondo_110"):
        return SCALA["110"]
    if nome.startswith("europa_50"):
        return SCALA["50"]
    if nome.startswith("penisola_10"):
        return SCALA["10"]
    return "mondiale (tutta la cartella)"


def categoria_di(nome, fonti):
    """La categoria del file, e **la fonte**.

    L'ordine è quello della compilazione: `rilievo_` e `_altitudine` hanno nomi
    propri, `mondo_admin1` ha un nome proprio, e tutto il resto deve trovare la
    sua fonte nella lista del generatore. Un file che non la trova non è «di
    Natural Earth» per default: è un file di provenienza ignota, ed è il
    controllo a dirlo.
    """
    if nome.startswith("rilievo_"):
        cat = "rilievo"
    elif nome.endswith("_altitudine"):
        cat = "altitudine"
    elif nome == "mondo_admin1":
        cat = "admin1"
    elif nome in fonti:
        cat = "natural_earth"
    else:
        cat = None
    fonte = None
    if cat == "natural_earth":
        fonte = "Natural Earth %s (pubblico dominio)" % fonti[nome]
    elif cat == "admin1":
        fonte = ("Natural Earth 10m admin_1_states_provinces (pubblico dominio), "
                 "tagliato sul riquadro della penisola")
    elif cat == "altitudine":
        fonte = "Natural Earth geography_regions_elevation_points (pubblico dominio)"
    elif cat == "rilievo":
        fonte = "Wikidata P2044, campione su 41 città"
    return cat, fonte


def leggi_file(nome, cat, fonte, fonti):
    """Il conto del file, letto dal file vero con il lettore del progetto."""
    path = os.path.join(MAPPE, nome + ".json")
    geom, punti = mappe_lettore.leggi(path)
    riga = {
        "file": nome + ".json",
        "categoria": cat,
        "fonte": fonte or "NON DICHIARATA",
        "scala": scala_di(nome),
        "geometrie": len(geom),
        "punti": len(punti),
        "byte": os.path.getsize(path),
        "formato": "delta con quantizzazione, q = %g" % quantizzazione(nome),
    }
    if cat == "rilievo":
        # I due rilievi hanno una proprieta' che le altre non hanno: ogni punto
        # **e'** una citta' con la sua altitudine. Il conteggio e' il numero dei
        # punti, non quello di una chiave `citta` che nei file non esiste: la
        # prima stesione del manifest la cercava, non la trovava, e scriveva un
        # conto **0** che il controllo ha letto come un numero vero. Un dato
        # letto dalla chiave sbagliata e' peggio di un dato assente, perche' il
        # dato assente almeno fa domanda.
        riga["citta"] = len(punti)
        riga["campo"] = "altitudine del terreno, da `dati/altitudine_riferimento.json`"
    return riga


def quantizzazione(nome):
    testo = open(os.path.join(MAPPE, nome + ".json"), encoding="utf-8").read()
    return float(testo.split('"q":', 1)[1].split(",", 1)[0])


def costruisci():
    fonti = lavori_di_mappe_formato()
    righe = []
    categorie = {}
    byte = 0
    for path in sorted(glob.glob(os.path.join(MAPPE, "*.json"))):
        nome = os.path.basename(path)[:-len(".json")]
        cat, fonte = categoria_di(nome, fonti)
        riga = leggi_file(nome, cat, fonte, fonti)
        righe.append(riga)
        categorie.setdefault(cat or "non_dichiarata", []).append(nome + ".json")
        byte += riga["byte"]

    categorie = {k: {"file": len(v), "nomi": v} for k, v in sorted(categorie.items())}
    return {
        "versione": 1,
        "data": "2026-10-04",
        "cosa_e": "l'inventario di `dati/mappe/`: **da dove viene ogni file**, "
                  "quando e con quale produttore. Sta in `dati/` e non in "
                  "`dati/mappe/` perche' li vale la regola del solo formato a "
                  "delta, e un JSON ordinario li fa crashare "
                  "`mappe_lettore.leggi()`",
        "perche_esiste": "il generatore conosce la fonte di ogni file ma la "
                         "teneva in una lista Python: **il file di dati non la "
                         "portava con se**. Il 04/10/2026 ne e' venuto fuori che "
                         "per contare i file di quella cartella nessuno poteva "
                         "farlo dai dati, e i documenti avevano dato quattro "
                         "numeri diversi — 19, 21, 23, 25 — copiati a mano in "
                         "momenti diversi della storia del progetto",
        "come_si_legge": "sorgenti/gis/mappe_lettore.py per i dati, "
                         "sorgenti/gis/verifica_inventario_mappe.py per i conti",
        "come_si_rigenera": "python3 sorgenti/gis/mappe_manifest.py — i conteggi "
                            "sono **calcolati** sui file veri con il lettore, e "
                            "non copiati qui: se un file cambia, il manifest "
                            " cambia con lui",
        "la_regola": "un file che non trova la sua fonte nella lista del "
                     "generatore **non e' di Natural Earth per default**: e' un "
                     "file di provenienza ignota, e va detto",
        "totale": {"file": len(righe), "byte": byte,
                   "megabyte": round(byte / 1048576.0, 2)},
        "categorie": categorie,
        "produttori": PRODUTTORI,
        "file": righe,
    }


def main():
    if "--leggi" in sys.argv:
        print(json.dumps(construisci(), ensure_ascii=False, indent=1))
        return 0
    m = costruisci()
    with open(MANIFEST, "w", encoding="utf-8") as f:
        json.dump(m, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("scritto dati/mappe_manifest.json")
    print("  %d file, %d categorie, %.2f MB"
          % (m["totale"]["file"], len(m["categorie"]), m["totale"]["megabyte"]))
    for cat, v in m["categorie"].items():
        print("  %-16s %3d  %s" % (cat, v["file"], ", ".join(
            n[:-len(".json")] for n in v["nomi"][:4]) + ("…" if v["file"] > 4 else "")))
    return 0


if __name__ == "__main__":
    sys.exit(main())