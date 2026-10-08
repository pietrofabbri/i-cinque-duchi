"""Seconda ricerca delle immagini degli oggetti, dopo la revisione delle voci
dell'08/10/2026 (B2).

Che cosa cambia rispetto a `cerca_immagini_oggetti.py`, che resta com'era:

- **l'italiano ha 150 voci, una per tappa** (`dati/lingue/cibi_per_tappa.json`):
  ogni risultato dell'italiano porta anche `anno`;
- per le altre lingue **si cercano solo le voci cambiate**; le voci confermate
  tengono i candidati della prima ricerca;
- `termini` è la lista vera dei termini usati (la prima versione la scriveva
  lettera per lettera, iterando una stringa);
- lo User-Agent dichiara il progetto e il suo indirizzo, come chiede la
  politica di Wikimedia: con uno generico la risposta è 429.

I termini delle voci nuove sono in `TERMINI_NUOVI` (il primo che dà risultati
liberi vince). L'esito è `dati/lingue/immagini_oggetti.json` versione 2.

Uso:  python3 sorgenti/lingue/cerca_immagini_v2.py              # ricerca completa
      python3 sorgenti/lingue/cerca_immagini_v2.py --solo-vuote  # ripete solo le voci
                                                                 # senza candidati, con i
                                                                 # termini in più
"""
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cerca_immagini_oggetti as base  # noqa: E402

base.UA = ("ICinqueDuchi/0.2 (https://github.com/pietrofabbri/i-cinque-duchi; "
           "progetto didattico) python-urllib")
RADICE = base.RADICE
CIBI = os.path.join(RADICE, "dati", "lingue", "cibi_per_tappa.json")
TERMINI_FILE = os.path.join(RADICE, "dati", "lingue", "termini_ricerca_v2.json")


def senza_articolo(voce):
    for a in ("il ", "lo ", "la ", "i ", "gli ", "le ", "l'", "un ", "una "):
        if voce.startswith(a):
            return voce[len(a):]
    return voce


def solo_vuote():
    """Ripete la ricerca per le voci rimaste senza candidati, con i termini in
    più di `termini_ricerca_v2.json`; le altre non si toccano."""
    with open(base.ESITO, encoding="utf-8") as f:
        esito = json.load(f)
    with open(TERMINI_FILE, encoding="utf-8") as f:
        extra = json.load(f)["termini"]
    for r in esito["risultati"]:
        if r["candidati"] or r["lingua"] == "FE":
            continue
        chiave = ("IT-%d-%02d" % (r["anno"], r["numero"]) if r["lingua"] == "IT"
                  else "%s-%02d" % (r["lingua"], r["numero"]))
        if chiave not in extra:
            continue
        termini = [senza_articolo(r["voce"])] + extra[chiave]
        r["termini"] = termini
        r["candidati"] = base.cerca(extra[chiave])
        r["categoria"] = "da_vedere" if r["candidati"] else "nessuna"
        r["motivo"] = "" if r["candidati"] else "nessun risultato libero per i termini usati"
        print(chiave, r["voce"], len(r["candidati"]), flush=True)
        time.sleep(0.3)
    with open(base.ESITO, "w", encoding="utf-8") as f:
        json.dump(esito, f, ensure_ascii=False, indent=1)
    print("senza candidati:", sum(1 for r in esito["risultati"]
                                  if not r["candidati"] and r["lingua"] != "FE"))


def main():
    if "--solo-vuote" in sys.argv:
        return solo_vuote()
    with open(base.ESITO, encoding="utf-8") as f:
        vecchio = {(r["lingua"], r["numero"]): r for r in json.load(f)["risultati"]}
    with open(base.ASSOC, encoding="utf-8") as f:
        assoc = json.load(f)["associazioni"]
    with open(CIBI, encoding="utf-8") as f:
        cibi = json.load(f)["tappe"]
    with open(TERMINI_FILE, encoding="utf-8") as f:
        termini_extra = json.load(f)["termini"]
    risultati = []

    def cerca_voce(chiave, voce):
        termini = [senza_articolo(voce)] + termini_extra.get(chiave, [])
        cand = base.cerca(termini)
        time.sleep(0.3)
        return termini, cand

    for t in cibi:
        chiave = "IT-%d-%02d" % (t["anno"], t["numero"])
        termini, cand = cerca_voce(chiave, t["piatto"])
        risultati.append({"lingua": "IT", "anno": t["anno"], "numero": t["numero"],
                          "voce": t["piatto"], "termini": termini,
                          "categoria": "da_vedere" if cand else "nessuna",
                          "motivo": "" if cand else "nessun risultato libero per i termini usati",
                          "candidati": cand})
        print(chiave, t["piatto"], len(cand), flush=True)
    for a in assoc:
        if a["lingua"] == "IT":
            continue
        for i, voce in enumerate(a["voci"], 1):
            v = vecchio.get((a["lingua"], i))
            if v and v["voce"] == voce:
                risultati.append(v)
                continue
            if a["lingua"] == "FE":
                risultati.append({"lingua": "FE", "numero": i, "voce": voce, "termini": [],
                                  "categoria": "nessuna",
                                  "motivo": "campo di rilevazione, non oggetto: non esiste immagine che rappresenti un campo di raccolta",
                                  "candidati": []})
                continue
            chiave = "%s-%02d" % (a["lingua"], i)
            termini, cand = cerca_voce(chiave, voce)
            risultati.append({"lingua": a["lingua"], "numero": i, "voce": voce, "termini": termini,
                              "categoria": "da_vedere" if cand else "nessuna",
                              "motivo": "" if cand else "nessun risultato libero per i termini usati",
                              "candidati": cand})
            print(chiave, voce, len(cand), flush=True)
    esito = {"versione": 2, "data": time.strftime("%Y-%m-%d"),
             "nota": "Proposte, non scelte: le sceglie Pietro con lo strumento di scelta "
                     "(sorgenti/lingue/scelta/) e le scelte si registrano in "
                     "dati/lingue/attestazione_oggetti.json. L'italiano ha 150 voci, una per "
                     "tappa, con `anno`; le altre lingue 30. Le voci confermate l'08/10/2026 "
                     "tengono i candidati della prima ricerca (05/10/2026).",
             "risultati": risultati}
    with open(base.ESITO, "w", encoding="utf-8") as f:
        json.dump(esito, f, ensure_ascii=False, indent=1)
    print("voci:", len(risultati), "senza candidati:",
          sum(1 for r in risultati if not r["candidati"] and r["lingua"] != "FE"))


if __name__ == "__main__":
    main()
