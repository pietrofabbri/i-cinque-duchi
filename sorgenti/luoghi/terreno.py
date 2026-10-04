"""Il terreno dei luoghi del gioco, misurato e non scritto a mano.

**Che cosa cambia.** `dati/luoghi_gioco.json` ha un campo `terreno` che fino a
ieri era l'unico campo che nessun comando rifaceva: `aggiorna_registro.py` lo
conserva fra i «campi a mano» perché è stato compilato a mano, e
`verifica_catena_luoghi.py` (L4) conta che sia su almeno cinquanta luoghi. Era
un numero scritto a mano che non invecchiava: era un numero scritto a mano che
invecchiava, e che una volta ha anche mentito.

**Il difetto, e perché l'ho trovato solo adesso.** I valori erano stati misurati
con la prima versione di `rilievo.py`, quella che leggeva il pixel sbagliato del
tassello (l'indice di un tassello a livello superiore al posto di quello di un
pixel). Il sintomo è su Torino: il registro dice **785 m**, che non sono Torino
ma una collina a sette chilometri di distanza; la città sta a **239 m** e il
nuovo file delle città dà 248 m alla sua coordinata. Le altre 53 erano state
misurate bene per caso — la maggior parte delle città è in piano, e su un piano
il pixel sbagliato dà quasi la stessa risposta. È la parte peggiore di un difetto
di coordinate: passa quasi sempre e quando sbaglia sbaglia di cinquecento metri.

Da qui la regola, che è la regola del progetto: **un numero che si può calcolare
non si scrive a mano**. Il campo `terreno` non è più di mano: è questo script.

Uso:  python3 sorgenti/luoghi/terreno.py --prova    (dice, non scrive)
      python3 sorgenti/luoghi/terreno.py            (misura e scrive)
"""
import json
import os
import sys

RADICE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(RADICE, "sorgenti", "gis"))
import rilievo  # noqa: E402

REGISTRO = os.path.join(RADICE, "dati", "luoghi_gioco.json")
CAMPI = ("quota", "pend", "espo", "rel", "scarto")


def main():
    sola_prova = "--prova" in sys.argv
    with open(REGISTRO, encoding="utf-8") as f:
        registro = json.load(f)

    luoghi = registro["luoghi"]
    con_coordinate = [l for l in luoghi
                      if isinstance(l.get("lat"), (int, float))
                      and isinstance(l.get("lon"), (int, float))]
    print("luoghi: %d, con coordinate: %d" % (len(luoghi), len(con_coordinate)))

    cambiati, nuovi, saltati = [], 0, []
    for l in con_coordinate:
        try:
            m = rilievo.misura(l["lat"], l["lon"])
        except SystemExit as e:
            print("  %s: %s" % (l["luogo"], e))
            continue
        if not m:
            saltati.append(l["luogo"])
            continue
        nuovo = {c: m[c] for c in CAMPI}
        nuovo["fonte"] = rilievo.FONTE
        nuovo["stato"] = rilievo.STATO
        vecchio = l.get("terreno") or {}
        if not vecchio:
            nuovi += 1
        elif any(vecchio.get(c) is not None and vecchio[c] != nuovo[c]
                 for c in CAMPI):
            scarto = max(abs(vecchio[c] - nuovo[c]) for c in CAMPI
                         if isinstance(vecchio.get(c), (int, float)))
            cambiati.append((scarto, l["luogo"], vecchio.get("quota"), nuovo["quota"]))
        l["terreno"] = nuovo

    print("misurati %d, nuovi %d, cambiati %d, saltati %d"
          % (len(con_coordinate) - len(saltati), nuovi, len(cambiati), len(saltati)))
    for scarto, nome, prima, dopo in sorted(cambiati, reverse=True)[:12]:
        print("  %-16s %.0f -> %.0f m (scarto massimo %.1f)"
              % (nome, prima or 0, dopo, scarto))
    if saltati:
        print("  saltati: %s" % ", ".join(saltati))
    print("  decodificatore: %s" % rilievo.DECODIFICATORE)

    if sola_prova:
        print("\n--prova: non scrivo nulla")
        return
    with open(REGISTRO, "w", encoding="utf-8") as f:
        json.dump(registro, f, ensure_ascii=False, indent=1)
    print("\nscritto %s" % REGISTRO)


if __name__ == "__main__":
    main()