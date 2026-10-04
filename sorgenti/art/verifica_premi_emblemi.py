"""I controlli sugli emblemi dei premi, e i difetti che devono vedere.

Sei controlli, e ognuno guarda una cosa che un altro non guarda:

  Q1  **Il catalogo ha 1050 chiavi distinte**, una per livello. Due record con
      la stessa chiave sono lo stesso premio due volte, ed e' esattamente il
      difetto che i sessanta emblemi delle persone hanno insegnato: sessanta
      emblemi, diciotto file.
  Q2  **Ogni tessera dichiarata nell'indice sta dentro il foglio**, e il
      foglio si decodifica con la misura dichiarata. Un indice che promette
      1050 tessere e ne disegna 1049 e' un indice falso.
  Q3  **Le 1050 tessere sono tutte distinte**: si estrae ciascuna dal foglio e
      se ne confronta lo sha. E' il controllo che ha morso sui ritratti, e qui
      la ragione e' forte: trecento premi hanno la **stessa categoria** e quindi
      la stessa forma, e se la firma non rompesse le collisioni quei trecento
      sarebbero centocinquanta file identici.
  Q4  **Ogni categoria usata ha una forma dichiarata**, e il segno produce
      pixel. Un disegno che non disegna niente e' una forma che non esiste.
  Q5  **Ogni tessera dice perche'** quella forma sta con quella categoria.
  Q6  **Ogni tessera corrisponde a un premio del catalogo**, per chiave.

Uso:  python3 sorgenti/art/verifica_premi_emblemi.py
"""
import hashlib
import json
import os
import sys

RADICE = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(RADICE, "sorgenti", "gis"))
sys.path.insert(0, os.path.join(RADICE, "sorgenti", "art"))
from png_terrarium import decodifica_png, misura_png       # noqa: E402
import emblema                                              # noqa: E402

PREMI = os.path.join(RADICE, "dati", "premi.json")
INDICE = os.path.join(RADICE, "sorgenti", "art", "out", "premi",
                      "premi_indice.json")
CARDINALITA = 1050            # prem.md 4.0: 150 informatici piu' 900 linguistici


def controlla(catalogo=None, indice=None, tessere=None):
    """Tutti i controlli su file in memoria. Ritorna l'elenco dei problemi."""
    problemi = []
    if catalogo is None:
        catalogo = json.load(open(PREMI, encoding="utf-8"))
    if indice is None:
        indice = json.load(open(INDICE, encoding="utf-8"))
    if tessere is None:
        percorso = os.path.join(RADICE, indice["foglio"])
        with open(percorso, "rb") as f:
            blob = f.read()
        w, h = misura_png(blob)
        tessere = decodifica_png(blob)
        if [w, h] != indice["foglio_px"]:
            problemi.append("Q2 il foglio e' %dx%d e l'indice dichiara %dx%d"
                            % (w, h, indice["foglio_px"][0],
                               indice["foglio_px"][1]))
        else:
            tessere = tessere
    voci = indice["tessere"]

    # Q1 — chiavi distinte nel catalogo e una per livello
    chiavi = [p["chiave"] for p in catalogo["premi"]]
    if len(set(chiavi)) != len(chiavi):
        doppi = sorted({k for k in chiavi if chiavi.count(k) > 1})[:3]
        problemi.append("Q1 chiavi duplicate nel catalogo: %s"
                        % ", ".join(doppi))
    if len(catalogo["premi"]) != CARDINALITA:
        problemi.append("Q1 il catalogo ha %d premi e prem.md 4.0 ne dichiara %d"
                        % (len(catalogo["premi"]), CARDINALITA))

    # Q2 — ogni tessera dentro il foglio
    larghezza = len(tessere[0]) if tessere else 0
    altezza = len(tessere)
    for t in voci:
        if t["x"] < 0 or t["y"] < 0 \
                or t["x"] + t["px"][0] > larghezza \
                or t["y"] + t["px"][1] > altezza:
            problemi.append("Q2 %s: la tessera a %d,%d (%dx%d) esce dal foglio "
                            "%dx%d" % (t["chiave"], t["x"], t["y"], t["px"][0],
                                       t["px"][1], larghezza, altezza))
            break

    # Q3 — le tessere sono distinte
    sha = {}
    for t in voci:
        pezzo = [tuple(p) for riga in
                 tessere[t["y"]:t["y"] + t["px"][1]]
                 for p in riga[t["x"]:t["x"] + t["px"][0]]]
        h = hashlib.sha256(repr(pezzo).encode()).hexdigest()
        if h in sha:
            problemi.append("Q3 %s e %s: la stessa tessera, sha uguale"
                            % (sha[h], t["chiave"]))
            break
        sha[h] = t["chiave"]

    # Q4 — ogni categoria usata ha una forma che disegna qualcosa
    for categoria in sorted(indice["categorie_usate"]):
        segno = indice["forme"].get(categoria, {}).get("segno")
        if not segno:
            problemi.append("Q4 la categoria %s non ha forma dichiarata"
                            % categoria)
            continue
        try:
            pixel = emblema.segno(segno, 12, 4, 24)
        except ValueError:
            problemi.append("Q4 la categoria %s dichiara il segno %s che "
                            "nessuno sa disegnare" % (categoria, segno))
            continue
        if not pixel:
            problemi.append("Q4 la categoria %s ha il segno %s che non "
                            "produce nessun pixel" % (categoria, segno))

    # Q5 — ogni tessera dice perche'
    for t in voci:
        if not t.get("forma_perche"):
            problemi.append("Q5 %s: la tessera non dice perche' quella forma"
                            % t["chiave"])
            break

    # Q6 — ogni tessera corrisponde a un premio
    if set(t["chiave"] for t in voci) != set(chiavi):
        solo_i = sorted(set(t["chiave"] for t in voci) - set(chiavi))[:2]
        solo_c = sorted(set(chiavi) - set(t["chiave"] for t in voci))[:2]
        problemi.append("Q6 tessere e premi non combaciano: solo nel foglio %s,"
                        " solo nel catalogo %s" % (solo_i, solo_c))
    return problemi


def main():
    ind = json.load(open(INDICE, encoding="utf-8"))
    percorso = os.path.join(RADICE, ind["foglio"])
    with open(percorso, "rb") as f:
        blob = f.read()
    tessere = decodifica_png(blob)
    w, h = misura_png(blob)
    problemi = controlla(tessere=tessere)
    for p in problemi:
        print("   %s" % p)
    print("PROBLEMI: %d" % len(problemi))
    print("  premi      : %d" % len(json.load(open(PREMI,
                                                   encoding="utf-8"))["premi"]))
    print("  tessere    : %d" % len(ind["tessere"]))
    print("  foglio     : %dx%d, %d byte" % (w, h, len(blob)))
    print("  categorie  : %d usate, %d forme dichiarate"
          % (len(ind["categorie_usate"]), len(ind["forme"])))
    return 1 if problemi else 0


def difetti():
    """Sei difetti iniettati, uno per controllo, su file in memoria.

    Non si rompono i file veri: qui i controlli prendono l'indice e il catalogo
    come dati, e il foglio come griglia di pixel. Un difetto qui e' una copia
    cambiata, che è legittimo perche' **nessun controllo scrive**: il
    generatore scrive, il verificatore guarda. La prova di `prova_difetto_
    disegni.py` invece rompe i file, perché lì il generatore li rifà.
    """
    cat = json.load(open(PREMI, encoding="utf-8"))
    ind = json.load(open(INDICE, encoding="utf-8"))
    con = open(os.path.join(RADICE, ind["foglio"]), "rb").read()
    griglia = decodifica_png(con)
    esiti = []

    def senza_problemi():
        return not controlla(cat, ind, griglia)

    assert senza_problemi(), "il verificatore non e' verde prima di cominciare"
    print("prima della prova: verde")

    # F1: chiave duplicata nel catalogo.
    c = json.loads(json.dumps(cat))
    c["premi"][5]["chiave"] = c["premi"][4]["chiave"]
    esiti.append(("F1 chiave duplicata nel catalogo",
                  controlla(c, ind, griglia), "Q1"))

    # F2: una tessera che esce dal foglio.
    i = json.loads(json.dumps(ind))
    i["tessere"][7]["x"] = len(griglia[0]) + 5
    esiti.append(("F2 tessera fuori dal foglio",
                  controlla(cat, i, griglia), "Q2"))

    # F3: due tessere identiche — la firma smette di rompere le collisioni.
    i = json.loads(json.dumps(ind))
    a, b = i["tessere"][11], i["tessere"][12]
    cx, cy = b["x"], b["y"]
    for y in range(a["px"][1]):
        for x in range(a["px"][0]):
            griglia[cy + y][cx + x] = griglia[a["y"] + y][a["x"] + x]
    esiti.append(("F3 due tessere identiche",
                  controlla(cat, i, griglia), "Q3"))

    # F4: una categoria senza forma dichiarata.
    i = json.loads(json.dumps(ind))
    del i["forme"]["D"]
    esiti.append(("F4 categoria senza forma dichiarata",
                  controlla(cat, i, griglia), "Q4"))

    # F5: una tessera che non dice perche'.
    i = json.loads(json.dumps(ind))
    i["tessere"][3]["forma_perche"] = ""
    esiti.append(("F5 tessera senza il perche' della forma",
                  controlla(cat, i, griglia), "Q5"))

    # F6: una tessera che non corrisponde a nessun premio.
    i = json.loads(json.dumps(ind))
    i["tessere"][9]["chiave"] = "9-99-XX"
    esiti.append(("F6 tessera senza il premio",
                  controlla(cat, i, griglia), "Q6"))

    visti, non = 0, 0
    for nome, problemi, cerca in esiti:
        righe = [p for p in problemi if p.startswith(cerca)]
        if problemi and righe:
            visti += 1
            print("  visto   %-42s %s" % (nome, righe[0][:56]))
        else:
            non += 1
            print("  NON VISTO %-41s %d problemi, nessuno %s"
                  % (nome, len(problemi), cerca))
    print("\ndifetti iniettati: %d, visti: %d, non visti: %d"
          % (len(esiti), visti, non))
    # **Si rilegge il foglio dal disco prima di dichiarare che e' tornato
    # verde.** Il difetto F3 ha cambiato la griglia in memoria, e chiedere a
    # quella griglia se e' a posto significa chiedere a se stessi: la prova
    # dichiarerebbe verde un file che non ha toccato. Il file non e' stato
    # scritto — nessun controllo scrive — ma rileggerlo costa una riga ed e'
    # l’unica verifica che valga.
    del griglia
    griglia = decodifica_png(open(os.path.join(RADICE, ind["foglio"]),
                                  "rb").read())
    assert senza_problemi(), "la prova ha lasciato il file in cattive condizioni"
    print("dopo la prova: verde")
    return 1 if non else 0


if __name__ == "__main__":
    sys.exit(difetti() if "--difetti" in sys.argv else main())
