"""Verifica la tavolozza del gioco: che i colori ci siano ancora, e che la
tavolozza sia coerente con se stessa.

`verifica_coerenza.py` guarda i documenti fra loro. Questo file guarda una cosa
diversa e piu' scomoda: **se i colori dichiarati ci sono ancora**. Una tavolozza
copiata a mano va bene finche' nessuno la tocca; il giorno in cui qualcuno
cambia un esadecimale su Wikidata, il file mente e nessuno se ne accorge. Qui si
va a leggere la fonte di ogni voce e si confronta.

I controlli sono sei, e sono tutti sul file, non sulla fonte:

  A1  ogni voce ha un esadecimale di sei cifre
  A2  le chiavi sono uniche: due voci con lo stesso nome sono due colori che si
      contendono lo stesso nome nel motore
  A3  ogni voce da pigmento porta la sua fonte (Wikidata o infobox) e la sua
      catena, e la catena dice da dove arriva l'esadecimale
  A4  la fonte dichiara ancora quell'esadecimale  (il controllo che va in rete)
  A5  le voci dichiarate e di stato non si presentano come storiche: portano una
      nota che dice che cosa sono
  A6  i colori di stato sono distinguibili fra loro: due colori troppo
      vicini sono due colori che il motore non puo' separare

A6 e' il controllo che serve di piu' ed e' l'unico che guarda due colori insieme:
guardando gli esadecimali uno per uno il file non se ne accorge.

Uso:
    python3 sorgenti/verifica_tavolozza.py
    python3 sorgenti/verifica_tavolozza.py --offline   # salta A4
    python3 sorgenti/verifica_tavolozza.py --difetti   # ne inietta sei
"""
import copy
import json
import os
import re
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tavolozza_campioni as tc                        # noqa: E402

TAV = os.path.join(tc.RADICE, "dati", "fonti_visive", "tavolozza.json")
RE_HEX = re.compile(r"^[0-9A-F]{6}$")
# La soglia di differenza fra due colori di stato. Sotto, l'occhio non
# distingue e il gioco non puo' segnalare nulla: il difetto sarebbe silenzioso.
SOGLIA_STATO = 60.0


def distanza(a, b):
    """La distanza euclidea fra due colori, in 0-441 (massimo: nero e bianco).

    E' la distanza negli spazi RGB, che non e' la distanza che l'occhio
    percepisce: quella e' molto piu' complicata e molto meno riproducibile. Qui
    serve una soglia dichiarata e non un giudizio, e questa si sa spiegare in
    una riga.
    """
    return sum((int(a[i:i + 2], 16) - int(b[i:i + 2], 16)) ** 2
               for i in (0, 2, 4)) ** 0.5


def controlla(doc, offline=False, fonti=None):
    """I sei controlli sul file della tavolozza.

    Restituisce i problemi e il numero delle fonti ricontrollate.
    Il file lo passa chi chiama, non lo legge: e' quello che
    permette alla prova di far girare gli stessi controlli su una
    copia rotta invece che sul file vero.
    """
    voci = doc["voci"]
    problemi = []

    # A1 e A2: la forma del file
    for v in voci:
        if not RE_HEX.match(v.get("hex") or ""):
            problemi.append("A1  %s: esadecimale '%s' non valido"
                           % (v["chiave"], v.get("hex")))
    chiavi = [v["chiave"] for v in voci]
    for k in sorted({c for c in chiavi if chiavi.count(c) > 1}):
        problemi.append("A2  chiave duplicata: %s" % k)

    # A3 e A5: ogni voce dichiara da dove viene
    for v in voci:
        if v["origine"] in ("wikidata_p465", "wikipedia_infobox"):
            if not v.get("catena"):
                problemi.append("A3  %s: voce da pigmento senza catena" % v["chiave"])
            if v["origine"] == "wikidata_p465" and not v.get("wikidata"):
                problemi.append("A3  %s: dice wikidata ma non porta l'oggetto"
                               % v["chiave"])
            if v["origine"] == "wikipedia_infobox" and not v.get("pagina"):
                problemi.append("A3  %s: dice infobox ma non porta la pagina"
                               % v["chiave"])
        else:
            if not (v.get("nota") or "").strip():
                problemi.append("A5  %s: voce '%s' senza nota che dica che "
                               "cosa e'" % (v["chiave"], v["origine"]))

    # A4: la fonte dichiara ancora quell'esadecimale
    a4 = 0
    if not offline:
        # `fonti` sostituisce le due funzioni che leggono la fonte: e' cosi'
        # che A4 ha una prova senza rete, e non un'affermazione.
        da_wikidata = (fonti or {}).get("wikidata", tc.colore_wikidata)
        da_infobox = (fonti or {}).get("infobox", tc.colore_infobox)
        for v in voci:
            if v["origine"] == "wikidata_p465":
                colore, catena, _ = da_wikidata(v["wikidata"])
                a4 += 1
            elif v["origine"] == "wikipedia_infobox":
                colore, _ = da_infobox(v["pagina"])
                a4 += 1
            else:
                continue
            if colore != v["hex"]:
                problemi.append("A4  %s: il file dice %s, la fonte dice %s"
                               % (v["chiave"], v["hex"], colore or "niente"))
            if v["origine"] == "wikidata_p465" and catena != v["catena"]:
                problemi.append("A4  %s: la catena e' cambiata (%s invece di %s)"
                               % (v["chiave"], catena, v["catena"]))
            if fonti is None:
                time.sleep(0.6)

    # A6: i colori di stato devono essere distinguibili fra loro
    stato = [v for v in voci if v["origine"] == "stato"]
    for i, a in enumerate(stato):
        for b in stato[i + 1:]:
            d = distanza(a["hex"], b["hex"])
            if d < SOGLIA_STATO:
                problemi.append(
                    "A6  %s e %s sono troppo vicini (%.0f, sotto %.0f): il "
                    "gioco non li distingue"
                    % (a["chiave"], b["chiave"], d, SOGLIA_STATO))

    return problemi, a4


def main():
    sola_prova = "--difetti" in sys.argv
    with open(TAV, encoding="utf-8") as f:
        doc = json.load(f)
    if sola_prova:
        return difetti(doc)
    offline = "--offline" in sys.argv
    problemi, a4 = controlla(doc, offline)
    voci = doc["voci"]
    stato = [v for v in voci if v["origine"] == "stato"]
    # il riepilogo, che e' la parte che serve
    per_origine = {}
    for v in voci:
        per_origine[v["origine"]] = per_origine.get(v["origine"], 0) + 1
    print("tavolozza: %s" % os.path.relpath(TAV, tc.RADICE))
    print("  %d voci: %s" % (len(voci), ", ".join(
        "%d %s" % (n, o) for o, n in sorted(per_origine.items()))))
    print("  campioni guardati a vista: %d" % doc.get("campioni_guardati", -1))
    print("  pigmenti visitati senza esadecimale: %d"
          % len(doc.get("pigmenti_senza_colore_macchina", [])))
    if not offline:
        print("  fonti ricontrollate in rete: %d" % a4)
    else:
        print("  fonti ricontrollate in rete: 0 (--offline)")
    print("  coppie di stato verificate: %d" % (len(stato) * (len(stato) - 1) // 2))

    if problemi:
        print("\nPROBLEMI: %d" % len(problemi))
        for p in problemi:
            print("  " + p)
        return 1
    print("\nOK: nessun problema")
    return 0





def inietta(doc, etichetta):
    """Un difetto alla volta, su una copia profonda del file.

    Non si iniettano tutti e sei insieme: fermerebbero la prova al primo
    trovato e gli altri cinque non sarebbero mai guardati. La copia e' profonda
    perche' una copia superficiale lascerebbe il difetto nel file vero, che e'
    l'unico file che non si tocca mai.
    """
    d = copy.deepcopy(doc)
    voci = d["voci"]
    pigmenti = [v for v in voci
                if v["origine"] in ("wikidata_p465", "wikipedia_infobox")]
    altre = [v for v in voci if v not in pigmenti]
    stato = [v for v in voci if v["origine"] == "stato"]
    if etichetta == "A1":
        voci[0]["hex"] = "12345"
    elif etichetta == "A2":
        voci.append(copy.deepcopy(voci[0]))
    elif etichetta == "A3":
        if not pigmenti:
            return None, None
        pigmenti[0].pop("catena", None)
    elif etichetta == "A4":
        # la fonte risponde un colore sbagliato: il file ha ragione e la
        # fonte ha torto, ed e' quello che A4 deve vedere
        def wikidata_sbagliata(_oggetto):
            return ("000000", "catena inventata", None)
        def infobox_sbagliata(_pagina):
            return ("FFFFFF", "")
        return d, {"wikidata": wikidata_sbagliata,
                   "infobox": infobox_sbagliata}
    elif etichetta == "A5":
        if not altre:
            return None, None
        altre[0]["nota"] = "   "
    elif etichetta == "A6":
        if len(stato) < 2:
            return None, None
        stato[1]["hex"] = stato[0]["hex"]
    else:
        raise ValueError(etichetta)
    return d, None


def difetti(doc):
    """Prova che i sei controlli vedano un difetto ciascuno.

    La prova non tocca la rete: quando il difetto e' dentro i controlli che
    stanno sul file, `offline` e' True e la rete non serve; quando il difetto
    e' nella fonte, sono le due funzioni che la leggono ad essere sostituite,
    e anche in quel caso nessuna richiesta esce. Un controllo che si puo'
    provare solo quando c'e' la rete non e' un controllo che si puo' provare.
    """
    print("== i difetti iniettati")
    iniettati = 0
    visti = 0
    for etichetta in ("A1", "A2", "A3", "A4", "A5", "A6"):
        alterato, fonti = inietta(doc, etichetta)
        if alterato is None:
            print("   NON INIETTATO  %s: il file non ha la voce su cui "
                  "intervenire" % etichetta)
            continue
        iniettati += 1
        # `offline` e' True solo quando non ci sono fonti sostitutive: se
        # le fonti ci sono, A4 gira su quelle e non sulla rete
        problemi, _ = controlla(alterato, offline=(fonti is None),
                                fonti=fonti)
        trovati = [p for p in problemi if p.startswith(etichetta + " ")]
        if trovati:
            visti += 1
            for p in trovati:
                print("   visto   %s" % p[:100])
        else:
            print("   NON VISTO  %s" % etichetta)
    print("\ndifetti iniettati: %d, visti: %d, non visti: %d"
          % (iniettati, visti, iniettati - visti))
    return 0 if visti == iniettati else 1

if __name__ == "__main__":
    sys.exit(main())
