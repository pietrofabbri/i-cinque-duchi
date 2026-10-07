#!/usr/bin/env python3
"""Verifica il modello di livello contro il codice e i dati: K1-K4.

`docs/videogioco-5-duchi-modello-di-livello.md` riporta numeri che vengono da
altrove: la soglia e la pool della bottega vengono dal codice degli esercizi,
i tipi di livello dal file dei livelli. Un numero riportato invecchia quando
cambia la sua fonte (`metodo.md` §1.4), quindi qui si confronta.

  K1  NEED e POOL scritti nella tabella del §3 sono le costanti di
      `sorgenti/esercizi1.js`
  K2  i livelli per tipo scritti nella tabella del §6 sono quelli di
      `dati/videogioco-5-duchi-livelli.json`
  K3  le parti del livello (§1) sono numerate senza buchi, e ogni documento
      che la colonna «Dove si specifica» nomina esiste in `docs/`
  K4  il numero di domande che il §8 annuncia in lettere è il numero di voci
      del §9 prima del §9.1

Uso:  python3 sorgenti/verifica_modello.py
      python3 sorgenti/verifica_modello.py --difetti   # ne inietta quattro, uno per volta
"""
import collections
import io
import json
import os
import re
import sys

RADICE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOC = os.path.join(RADICE, "docs", "videogioco-5-duchi-modello-di-livello.md")
ESERCIZI = os.path.join(RADICE, "sorgenti", "esercizi1.js")
LIVELLI = os.path.join(RADICE, "dati", "videogioco-5-duchi-livelli.json")
PREFISSO = "videogioco-5-duchi-"

PAROLE = {"una": 1, "uno": 1, "due": 2, "tre": 3, "quattro": 4, "cinque": 5, "sei": 6,
          "sette": 7, "otto": 8, "nove": 9, "dieci": 10, "undici": 11, "dodici": 12}


def leggi(p):
    with io.open(p, encoding="utf-8") as f:
        return f.read()


def sezione(testo, numero):
    m = re.search(r"(?ms)^## %d\. .*?(?=^## |\Z)" % numero, testo)
    return m.group(0) if m else ""


def controlla(doc, codice, livelli, documenti):
    """Tutti i controlli su testi e dati passati dalla chiamata: la prova del
    difetto li fa girare su copie rotte (`metodo.md` §1.1)."""
    problemi = []

    # K1
    need = re.search(r"\bconst NEED\s*=\s*(\d+)", codice)
    pool = re.search(r"\bPOOL\s*=\s*NEED\s*\*\s*(\d+)", codice)
    s3 = sezione(doc, 3)
    d_need = re.search(r"Esercizi giusti per superare un gradino \(`NEED`\) \| \*\*(\d+)\*\*", s3)
    d_pool = re.search(r"\*\*(\d+) × NEED = (\d+)\*\*", s3)
    if not (need and pool):
        problemi.append("K1 esercizi1.js non dichiara NEED e POOL nella forma attesa")
    elif not (d_need and d_pool):
        problemi.append("K1 il §3 del modello non scrive NEED e POOL nella forma attesa")
    else:
        n, k = int(need.group(1)), int(pool.group(1))
        if int(d_need.group(1)) != n:
            problemi.append("K1 il modello scrive NEED = %s, il codice %d" % (d_need.group(1), n))
        if int(d_pool.group(1)) != k or int(d_pool.group(2)) != n * k:
            problemi.append("K1 il modello scrive POOL = %s × NEED = %s, il codice %d × %d = %d"
                            % (d_pool.group(1), d_pool.group(2), k, n, n * k))

    # K2
    conto = collections.Counter(l["tipo"] for l in livelli)
    s6 = sezione(doc, 6)
    for chiave, dato in (("normale", "normale"), ("prova", "prova")):
        m = re.search(r"^\| `%s`[^|]*\| (\d+)" % chiave, s6, re.M)
        if not m:
            problemi.append("K2 il §6 non ha la riga del tipo `%s`" % chiave)
        elif int(m.group(1)) != conto.get(dato, 0):
            problemi.append("K2 il §6 scrive %s livelli `%s`, i dati ne hanno %d"
                            % (m.group(1), chiave, conto.get(dato, 0)))
    altri = set(conto) - {"normale", "prova"}
    if altri:
        problemi.append("K2 i dati hanno tipi che il §6 non nomina: %s" % sorted(altri))

    # K3
    s1 = sezione(doc, 1)
    righe = re.findall(r"^\| (\d+) \| \*\*([^*]+)\*\* \|[^\n]*\| ([^|\n]*) \|$", s1, re.M)
    numeri = [int(r[0]) for r in righe]
    if not numeri or numeri != list(range(1, len(numeri) + 1)):
        problemi.append("K3 le parti del §1 non sono numerate da 1 senza buchi: %s" % numeri)
    for _, nome, dove in righe:
        for citato in re.findall(r"`([a-z0-9-]+\.md)`", dove):
            if PREFISSO + citato not in documenti:
                problemi.append("K3 la parte «%s» rimanda a `%s`, che non è in docs/" % (nome, citato))

    # K4
    s8, s9 = sezione(doc, 8), sezione(doc, 9)
    m = re.search(r"Gli altri (\w+) sono domande per Pietro", s8)
    # Solo la parte del §9 prima del §9.1: dal 07/10/2026 il §9.1 raccoglie le
    # domande nate dopo l'allineamento, nella forma «### Q6», e il loro testo
    # ha elenchi numerati che non sono domande.
    s9 = s9.split("### 9.1")[0]
    voci = re.findall(r"^\d+\. \*\*", s9, re.M)
    if not m:
        problemi.append("K4 il §8 non annuncia quante sono le domande")
    else:
        attese = PAROLE.get(m.group(1).lower(), -1)
        if attese != len(voci):
            problemi.append("K4 il §8 annuncia «%s» domande e il §9 ne ha %d" % (m.group(1), len(voci)))
    return problemi


def carica():
    return (leggi(DOC), leggi(ESERCIZI), json.load(io.open(LIVELLI, encoding="utf-8")),
            set(os.listdir(os.path.join(RADICE, "docs"))))


DIFETTI = {
    "K1": lambda d, c, l, x: (d.replace("(`NEED`) | **4**", "(`NEED`) | **5**"), c, l, x),
    "K2": lambda d, c, l, x: (d, c, l[:-1], x),
    "K3": lambda d, c, l, x: (d.replace("`ripassi.md`", "`ripasso.md`", 1), c, l, x),
    "K4": lambda d, c, l, x: (d.replace("Gli altri cinque sono domande", "Gli altri sei sono domande"), c, l, x),
}


def difetti():
    vero = carica()
    if controlla(*vero):
        print("il modello e' gia' rosso: la prova non ha senso")
        return 1
    visti = 0
    for etichetta, rompi in DIFETTI.items():
        rotto = rompi(*vero)
        trovati = [p for p in controlla(*rotto) if p.startswith(etichetta + " ")]
        print("   %-6s %s" % ("visto" if trovati else "NON VISTO", etichetta))
        visti += 1 if trovati else 0
    print("\ndifetti iniettati: %d, visti: %d, non visti: %d"
          % (len(DIFETTI), visti, len(DIFETTI) - visti))
    return 0 if visti == len(DIFETTI) else 1


def main():
    if "--difetti" in sys.argv:
        return difetti()
    problemi = controlla(*carica())
    print("== K1-K4. il modello di livello contro il codice e i dati")
    for p in problemi:
        print("   difetto %s" % p)
    if not problemi:
        print("   NEED, POOL, i tipi di livello, le parti e le domande tornano")
    return 1 if problemi else 0


if __name__ == "__main__":
    sys.exit(main())
