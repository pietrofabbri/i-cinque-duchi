"""Controlla i file del rilievo: che cosa dicono e quanto valgono.

`rilievo.py` produce due file — il rilievo delle città della penisola e
dell'Europa — e il documento che li prometteva li aveva sempre descritti senza
che nessuno li producesse. Produrli non basta: un file prodotto può essere
sbagliato in tre modi, e sono tre modi che non si vedono guardando i numeri del
file.

V1  ogni riga porta i sette campi che il documento promette, e i numeri sono
    numeri: un campo assente non è uno zero
V2  ogni file ha **tante righe quante sono le città di partenza**, e nessuna
    coordinata è ripetuta. È il controllo che avrebbe visto il difetto dei
    duplicati (408 righe su 212 città) e quello delle città perse (212 città
    diventate 210, perché due si chiamano uguale)
V3  i numeri sono plausibili — la pendenza non è negativa, l'esposizione sta fra
    0 e 360, la quota sta nel mondo — e il file contiene **un punto sotto il
    livello del mare e uno sopra i mille metri**: se un domani spariscono i due
    estremi, non è che il mondo si sia appiattito, è che il file è stato tagliato
V4  le città che si somigliano sono **dette**: quante righe hanno un'altra riga
    dello stesso nome entro cento metri, e quante hanno lo stesso nome in paesi
    diversi. Non è un difetto, è la fonte; un difetto è non saperlo
V5  **l'errore medio assoluto** contro le altitudini di riferimento di Wikidata,
    ricalcolato, e confrontato con la cifra che il documento scrive. È il
    controllo che rende verificabile la frase «verificato su 14 punti»: senza,
    la frase è una voce di parte
V6  la stessa città misurata due volte dà lo stesso numero: le 54 quote già nel
    registro dei luoghi del gioco e le quote dei nuovi file devono coincidere
    entro la tolleranza dichiarata (le due misure usano coordinate diverse,
    prese da due fonti diverse)

Uso:  python3 sorgenti/gis/verifica_rilievo.py
"""
import json
import os
import re
import sys

RADICE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATI = os.path.join(RADICE, "dati", "mappe")
sys.path.insert(0, os.path.join(RADICE, "sorgenti", "gis"))
import mappe_lettore  # noqa: E402

FILE = [("rilievo_penisola.json", "penisola_10_citta.json"),
        ("rilievo_europa.json", "europa_50_citta.json")]
RIFERIMENTO = os.path.join(RADICE, "dati", "altitudine_riferimento.json")
GIOCO = os.path.join(RADICE, "dati", "luoghi_gioco.json")
DOC = os.path.join(RADICE, "docs", "videogioco-5-duchi-luoghi-edifici.md")
README = os.path.join(RADICE, "README.md")
CAMPI = ["nome", "paese", "quota", "pend", "espo", "rel", "fonte", "stato"]
TOLLERANZA_GIOCO = 100.0     # metri, fra due misure con coordinate diverse


def leggi(nome):
    percorso = os.path.join(DATI, nome)
    if not os.path.exists(percorso):
        return None
    _, punti = mappe_lettore.leggi(percorso)
    return punti


def controlla():
    problemi = []

    # V1 e V2, file per file
    dati = {}
    for prodotto, partenza in FILE:
        punti = leggi(prodotto)
        if punti is None:
            problemi.append("V1 %s non esiste" % prodotto)
            continue
        dati[prodotto] = punti
        for campi, x, y in punti:
            if not isinstance(campi, dict):
                problemi.append("V1 %s: una riga non ha campi con nome" % prodotto)
                continue
            mancanti = [c for c in CAMPI if c not in campi]
            if mancanti:
                problemi.append("V1 %s %s: mancano %s"
                                % (prodotto, campi.get("nome", "?"),
                                   ", ".join(mancanti)))
            for c in ("quota", "pend", "espo", "rel"):
                if c in campi and not isinstance(campi[c], (int, float)):
                    problemi.append("V1 %s %s: %s non è un numero"
                                    % (prodotto, campi.get("nome", "?"), c))
            if campi.get("fonte") != "terrarium/SRTM":
                problemi.append("V1 %s %s: fonte %r"
                                % (prodotto, campi.get("nome", "?"),
                                   campi.get("fonte")))
        origini = leggi(partenza)
        if origini is None:
            problemi.append("V2 %s non esiste" % partenza)
        else:
            if len(punti) != len(origini):
                problemi.append("V2 %s ha %d righe su %d città di partenza"
                                % (prodotto, len(punti), len(origini)))
        visti = {}
        for campi, x, y in punti:
            k = (round(x, 5), round(y, 5))
            if k in visti:
                problemi.append("V2 %s: le coordinate %.5f, %.5f ci sono due volte"
                                % (prodotto, x, y))
            visti[k] = campi.get("nome")

    if not dati:
        return problemi, {}

    # V3
    tutte = [p for punti in dati.values() for p in punti]
    quote = [c["quota"] for c, _, _ in tutte if isinstance(c.get("quota"), (int, float))]
    if quote and not any(q < 0 for q in quote):
        problemi.append("V3 nessun punto sotto il livello del mare")
    if quote and not any(q > 1000 for q in quote):
        problemi.append("V3 nessun punto sopra i mille metri")
    for campi, x, y in tutte:
        if campi.get("pend") is not None and campi["pend"] < 0:
            problemi.append("V3 %s: pendenza negativa" % campi.get("nome"))
        if campi.get("espo") is not None and not 0 <= campi["espo"] < 360:
            problemi.append("V3 %s: esposizione %s fuori da 0-360"
                            % (campi.get("nome"), campi.get("espo")))
        if campi.get("quota") is not None and not -500 <= campi["quota"] <= 9000:
            problemi.append("V3 %s: quota %s fuori dal mondo"
                            % (campi.get("nome"), campi.get("quota")))

    # V4: quante righe somigliano a un'altra
    somigliani, omonimi = 0, []
    for i, (a, ax, ay) in enumerate(tutte):
        for b, bx, by in tutte[i + 1:]:
            if a.get("nome") != b.get("nome"):
                continue
            d = ((ax - bx) ** 2 + (ay - by) ** 2) ** 0.5
            if d <= 0.01:                       # circa 700 m
                somigliani += 1
            elif a.get("paese") != b.get("paese"):
                omonimi.append("%s (%s / %s)" % (a.get("nome"), a.get("paese"),
                                                 b.get("paese")))

    # V5: errore contro il riferimento, e confronto con la cifra del documento
    errore = {}
    if not os.path.exists(RIFERIMENTO):
        problemi.append("V5 manca %s" % os.path.basename(RIFERIMENTO))
    else:
        with open(RIFERIMENTO, encoding="utf-8") as f:
            riferimento = json.load(f)
        per_punto = {}
        for punti in dati.values():
            for campi, x, y in punti:
                per_punto[(campi.get("nome"), round(x, 4), round(y, 4))] = campi
        errori, peggiori = [], []
        for r in riferimento.get("punti", []):
            k = (r["nome"], round(r["lon"], 4), round(r["lat"], 4))
            campi = per_punto.get(k)
            if campi is None:
                problemi.append("V5 il punto di riferimento %s non è nei file"
                                % r["nome"])
                continue
            d = abs(campi["quota"] - r["altitudine"])
            errori.append(d)
            peggiori.append((d, r["nome"], campi["quota"], r["altitudine"]))
        if errori:
            errore["n"] = len(errori)
            errore["medio"] = sum(errori) / len(errori)
            errore["massimo"] = max(errori)
            errore["sopra_50"] = sum(1 for d in errori if d > 50)
            peggiori.sort(reverse=True)
            errore["peggiori"] = peggiori[:5]
        # le cifre che i documenti scrivono. Non solo quello che promette il
        # file: anche il README, che ne copia il numero nella sua nota, e che
        # nessun controllo guardava. È lo stesso difetto della volta che
        # l'audit confrontava se stesso e non il README che lo riassume.
        for percorso, espressione in ((DOC, r"errore medio assoluto \*\*([\d,]+) m\*\*"),
                                      (README, r"errore medio \*\*([\d,]+) m\*\* su (\d+) punti")):
            if not os.path.exists(percorso):
                continue
            testo = open(percorso, encoding="utf-8").read()
            trovato = re.search(espressione, testo)
            if not trovato:
                continue
            dichiarato = float(trovato.group(1).replace(",", "."))
            nome_doc = os.path.basename(percorso)
            if "medio" in errore and abs(dichiarato - errore["medio"]) > 0.05:
                problemi.append(
                    "V5 %s dichiara un errore medio di %s m, il conto dà %.1f m su %d punti"
                    % (nome_doc, trovato.group(1), errore["medio"], errore["n"]))
            elif len(trovato.groups()) > 1 and int(trovato.group(2)) != errore["n"]:
                problemi.append(
                    "V5 %s dichiara %s punti di riferimento, il campione ne ha %d"
                    % (nome_doc, trovato.group(2), errore["n"]))
            else:
                errore.setdefault("documenti", []).append("%s: %.1f m" % (nome_doc, dichiarato))

    # V6: le quote già nel registro dei luoghi del gioco
    if os.path.exists(GIOCO):
        with open(GIOCO, encoding="utf-8") as f:
            luoghi = json.load(f)["luoghi"]
        per_nome = {}
        for campi, x, y in tutte:
            per_nome.setdefault(campi.get("nome"), []).append(campi)
        confronti, sbagli = 0, []
        for l in luoghi:
            terreno = l.get("terreno")
            if not terreno:
                continue
            trovati = per_nome.get(l.get("luogo"))
            if not trovati:
                continue
            d = min(abs(t["quota"] - terreno["quota"]) for t in trovati)
            confronti += 1
            if d > TOLLERANZA_GIOCO:
                sbagli.append("%s: %.1f m contro %.1f m"
                              % (l.get("luogo"), terreno["quota"], d))
        errore["confronti_gioco"] = confronti
        errore["fuori_tolleranza"] = len(sbagli)
        if sbagli:
            problemi.append("V6 %d luoghi del gioco differiscono più di %.0f m: %s"
                            % (len(sbagli), TOLLERANZA_GIOCO, "; ".join(sbagli[:6])))

    errore["righe"] = len(tutte)
    errore["somigliani"] = somigliani
    errore["omonimi"] = omonimi
    return problemi, errore


def main():
    problemi, errore = controlla()
    print("== i numeri ==")
    print("  righe misurate              : %s" % errore.get("righe", 0))
    print("  coppie a meno di 700 m      : %s" % errore.get("somigliani", 0))
    if errore.get("omonimi"):
        print("  nomi uguali in paesi diversi: %s" % ", ".join(errore["omonimi"]))
    if "medio" in errore:
        print("  punti con riferimento        : %d" % errore["n"])
        print("  errore medio assoluto       : %.1f m" % errore["medio"])
        print("  errore massimo              : %.1f m" % errore["massimo"])
        print("  errori sopra 50 m           : %d" % errore["sopra_50"])
        for riga in errore.get("documenti", []):
            print("  dichiarato in %s" % riga)
        for d, nome, misurata, riferimento in errore.get("peggiori", []):
            print("    peggiore: %-14s %.1f m misurata, %.0f m di riferimento "
                  "(scarto %.0f m)" % (nome, misurata, riferimento, d))
    if "confronti_gioco" in errore:
        print("  confronti col registro luoghi: %d, fuori tolleranza %d"
              % (errore["confronti_gioco"], errore["fuori_tolleranza"]))
    print()
    if problemi:
        for p in problemi:
            print("difetto: %s" % p)
    print("rilievo: %s" % ("nessun problema" if not problemi
                          else "%d difetti" % len(problemi)))
    return 1 if problemi else 0


if __name__ == "__main__":
    sys.exit(main())