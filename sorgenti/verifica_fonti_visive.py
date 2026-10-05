#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifica i due file di fonti visive costruiti il 05/10/2026: **M1–M6** sui
mezzi di trasporto ed **E1–E4** sulle epigrafi.

Nati dalla stessa malattia, e per una ragione che vale più dei due buchi che
chiudono: **un numero vero che guarda il numero sbagliato**. La ricerca del
02/10 dichiarava undici mezzi e il gioco ne usa ventuno, e nessuno dei due
numeri era confrontato con l'altro. Un controllo che confronta il file con se
stesso dà verde su quel difetto: per questo `M1` confronta il file con
**`percorsi_mezzi.py`**, cioè con la fonte dei mezzi, e non con se stesso.

  M1  ogni mezzo del gioco ha una riga, e nessun mezzo e' sparito dal file
  M2  ogni immagine scelta e' fra i candidati della ricerca del 02/10
  M3  ogni mezzo ha **una** delle tre forme: immagine, vuoto con ragione,
      oppure segno fantastico — mai due e mai nessuna
  M4  nessun mezzo fantastico ha un'immagine: sono creature
  M5  i numeri scritti in §3.1 del documento sono quelli del file
  M6  ogni immagine ha l'attribuzione calcolata, e la licenza libera
  E1  ogni voce epigrafa ha la sua immagine, scelta fra i candidati
  E2  **nessuna epigrafe entra nel gioco senza trascrizione e traduzione**
  E3  nessun testo e' scritto dal progetto: o c'e' con la sua fonte, o e' null
  E4  i numeri scritti in §3.3 del documento sono quelli del file

Uso:
    python3 sorgenti/verifica_fonti_visive.py
    python3 sorgenti/verifica_fonti_visive.py --difetti   # ne inietta cinque
"""
import importlib.util
import io
import json
import os
import re
import sys

RADICE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEZZI = os.path.join(RADICE, "dati", "fonti_visive", "mezzi.json")
EPIGRAFI = os.path.join(RADICE, "dati", "fonti_visive", "epigrafi.json")
CERCA = os.path.join(RADICE, "dati", "fonti_visive", "fonti_visive.json")
DOC = os.path.join(RADICE, "docs", "videogioco-5-duchi-fonti-visive.md")
MEZZI_PY = os.path.join(RADICE, "sorgenti", "percorsi_mezzi.py")

LIBERE = ("CC BY", "CC0", "Public domain", "PD", "No restrictions", "CC BY-SA")


def leggi(p):
    with io.open(p, encoding="utf-8") as f:
        return json.load(f)


def mezzi_del_gioco():
    spec = importlib.util.spec_from_file_location("percorsi_mezzi", MEZZI_PY)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m.MEZZI


def sezione(testo, titolo, prossimo):
    """Il testo di una sezione: dal titolo al titolo seguente."""
    i = testo.index(titolo)
    j = testo.index(prossimo, i)
    return testo[i:j]


def cifra_in_riga(sezione, inizio_cella):
    """La prima cifra in grassetto della **riga di tabella** che comincia con
    una data cella.

    Serve per `M5` ed `E4`: i numeri scritti nel documento sono confrontati col
    conto **del file**, non fra loro, perché un numero che nessuno ricalcola è
    un numero che invecchia. La prima versione di questa funzione cercava la
    prima cifra che segue la frase, e la frase finiva col grassetto che precede
    il numero: leggeva il numero **successivo** e stampava sei difetti tutti
    suoi, dei quali nessuno era un difetto del documento. Un controllo che
    segnala se stesso è peggio di un controllo che non esiste.
    """
    for riga in sezione.splitlines():
        if riga.strip().startswith("| " + inizio_cella):
            m = re.search(r"\*\*(\d+)\*\*", riga)
            return int(m.group(1)) if m else None
    return None


def controlla(problemi, iniettato=None):
    mezzi = leggi(MEZZI)
    epi = leggi(EPIGRAFI)
    del_gioco = mezzi_del_gioco()
    ricerca = leggi(CERCA)["risultati"]
    testo = io.open(DOC, encoding="utf-8").read()

    # M1: una riga per ogni mezzo del gioco, e nessun mezzo in piu'
    righe = {v["mezzo"] for v in mezzi["mezzi"]}
    for nome in sorted(set(del_gioco) - righe):
        problemi.append("M1: il mezzo %s e' in percorsi_mezzi.py e non in "
                        "mezzi.json" % nome)
    for nome in sorted(righe - set(del_gioco)):
        problemi.append("M1: mezzi.json ha %s, che il gioco non usa" % nome)

    # M2: ogni immagine scelta e' fra i candidati della ricerca
    candidati = {c["file"] for v in ricerca["mezzo"] for c in v["candidati"]}
    for v in mezzi["mezzi"]:
        if v["immagine"] and v["immagine"]["file"] not in candidati:
            problemi.append("M2: l'immagine di %s non e' fra i candidati della "
                            "ricerca: %s" % (v["mezzo"], v["immagine"]["file"]))

    # M3: esattamente una delle tre forme, e il vuoto ha la sua ragione
    for v in mezzi["mezzi"]:
        forme = [bool(v["immagine"]), bool(v["vuoto"]), bool(v["segno"])]
        if sum(forme) != 1:
            problemi.append("M3: il mezzo %s ha %d forme (immagine %s, vuoto "
                            "%s, segno %s): deve averne una"
                            % (v["mezzo"], sum(forme), bool(v["immagine"]),
                               bool(v["vuoto"]), bool(v["segno"])))
        elif v["vuoto"] and len(v["vuoto"]) < 25:
            problemi.append("M3: il vuoto di %s non ha la ragione" % v["mezzo"])

    # M4: nessun mezzo fantastico ha un'immagine
    for v in mezzi["mezzi"]:
        if v["tipo"] == "gioco" and v["immagine"]:
            problemi.append("M4: %s e' un mezzo fantastico e ha un'immagine: "
                            "le creature non si fotografano" % v["mezzo"])

    # M6: l'attribuzione calcolata e la licenza libera
    for v in mezzi["mezzi"]:
        if not v["immagine"]:
            continue
        if not v["attribuzione"] or len(v["attribuzione"]) < 10:
            problemi.append("M6: %s ha un'immagine senza attribuzione"
                            % v["mezzo"])
        if not any(l in (v["immagine"]["licenza"] or "") for l in LIBERE):
            problemi.append("M6: la licenza di %s non e' fra quelle libere: %r"
                            % (v["mezzo"], v["immagine"]["licenza"]))

    # M5: i numeri scritti in 3.1 sono quelli del file
    s31 = sezione(testo, "### 3.1 I mezzi di trasporto", "### 3.2 ")
    for cella, chiave in (("Mezzi del gioco", "mezzi"),
                          ("Con immagine proposta", "con_immagine"),
                          ("Storici **senza** immagine", "storici_senza_immagine"),
                          ("Fantastici con segno dedicato", "fantastici_con_segno"),
                          ("Candidati esaminati", "candidati_esaminati")):
        atteso = mezzi["conti"][chiave]
        trovato = cifra_in_riga(s31, cella)
        if trovato is None:
            problemi.append("M5: la sezione 3.1 non dichiara la riga «%s»"
                            % cella)
        elif trovato != atteso:
            problemi.append("M5: la sezione 3.1 dichiara %d per «%s», il file %d"
                            % (trovato, cella, atteso))

    # E1: ogni voce ha la sua immagine, scelta fra i candidati
    cand_epi = {c["file"] for v in ricerca["epigrafe"] for c in v["candidati"]}
    for v in epi["voci"]:
        if not v["immagine"]:
            problemi.append("E1: la voce %s non ha immagine" % v["voce"])
        elif v["immagine"]["file"] not in cand_epi:
            problemi.append("E1: l'immagine di %s non e' fra i candidati: %s"
                            % (v["voce"], v["immagine"]["file"]))

    # E2: nessuna epigrafe entra senza trascrizione e traduzione
    for v in epi["voci"]:
        if v["entra_nel_gioco"] and not (v["trascrizione"] and v["traduzione"]):
            problemi.append("E2: %s entra nel gioco senza la trascrizione e la "
                            "traduzione: una foto di un sasso non e' un testo"
                            % v["voce"])
        if v["entra_nel_gioco"] and not v.get("fonte_del_testo"):
            problemi.append("E2: %s entra nel gioco senza la fonte del testo"
                            % v["voce"])

    # E3: nessun testo scritto dal progetto
    for v in epi["voci"]:
        for campo in ("trascrizione", "traduzione"):
            if v[campo] is not None and "fonte" not in str(v[campo]).lower():
                problemi.append("E3: il/la %s di %s non porta la sua fonte: "
                                "un testo generato dal progetto e' vietato"
                                % (campo, v["voce"]))

    # E4: i numeri scritti in 3.3 sono quelli del file
    s33 = sezione(testo, "### 3.3 Le epigrafi", "### 3.4 ")
    for cella, chiave in (("Voci", "voci"),
                          ("Candidati", "candidati"),
                          ("Con immagine scelta", "con_immagine"),
                          ("Con trascrizione e traduzione",
                           "con_trascrizione_e_traduzione"),
                          ("Che entrano nel gioco", "entrano_nel_gioco")):
        atteso = epi["conti"][chiave]
        trovato = cifra_in_riga(s33, cella)
        if trovato is None:
            problemi.append("E4: la sezione 3.3 non dichiara la riga «%s»"
                            % cella)
        elif trovato != atteso:
            problemi.append("E4: la sezione 3.3 dichiara %d per «%s», il file %d"
                            % (trovato, cella, atteso))
    return problemi


def inietta(quale):
    """Un difetto alla volta, perche' insieme la prova si ferma al primo."""
    if quale == "M1":
        p = MEZZI
        d = leggi(p)
        d["mezzi"] = [v for v in d["mezzi"] if v["mezzo"] != "moto"]
        return p, json.dumps(d, ensure_ascii=False, indent=1) + "\n"
    if quale == "M2":
        p = MEZZI
        d = leggi(p)
        for v in d["mezzi"]:
            if v["immagine"]:
                v["immagine"]["file"] = "File:inventato.jpg"
                break
        return p, json.dumps(d, ensure_ascii=False, indent=1) + "\n"
    if quale == "M4":
        p = MEZZI
        d = leggi(p)
        for v in d["mezzi"]:
            if v["tipo"] == "gioco":
                v["segno"] = None
                v["immagine"] = {"file": "File:drago.jpg", "url": "x",
                                 "licenza": "CC0", "autore": "x",
                                 "data": "1500", "px": [100, 100]}
                v["vuoto"] = "un drago dipinto del Quattrocento"
                break
        return p, json.dumps(d, ensure_ascii=False, indent=1) + "\n"
    if quale == "E2":
        p = EPIGRAFI
        d = leggi(p)
        d["voci"][0]["entra_nel_gioco"] = True
        return p, json.dumps(d, ensure_ascii=False, indent=1) + "\n"
    if quale == "E3":
        p = EPIGRAFI
        d = leggi(p)
        d["voci"][0]["trascrizione"] = "D(is) M(anibus) / POMponio"
        return p, json.dumps(d, ensure_ascii=False, indent=1) + "\n"
    if quale == "M5":
        p = DOC
        t = io.open(p, encoding="utf-8").read()
        return p, t.replace("| Mezzi del gioco | **21**", "| Mezzi del gioco | **11**", 1)
    if quale == "E4":
        p = DOC
        t = io.open(p, encoding="utf-8").read()
        # il difetto va nella **riga che il controllo legge**: la prosa non
        # viene guardata, e la prima versione della prova ci metteva un numero
        # in lettera, cosi' il difetto non c'era nemmeno
        return p, t.replace("| Candidati esaminati | **18**",
                            "| Candidati esaminati | **30**", 1)
    raise ValueError(quale)


def main():
    difetti_prova = [a for a in sys.argv if a.startswith("--difetti")]
    problemi = controlla([])
    print("== M1-M6 ed E1-E4. i mezzi e le epigrafi")
    if problemi:
        for p in problemi:
            print("   difetto %s" % p)
    else:
        print("   ogni mezzo ha una forma, i numeri della sezione sono quelli "
              "del file,\n   e nessuna epigrafe entra nel gioco senza testo")

    if not difetti_prova:
        return 1 if problemi else 0

    print("\nprova: un difetto alla volta, coi file rimessi a posto")
    iniettati = visti = 0
    for quale in ("M1", "M2", "M4", "M5", "E2", "E3", "E4"):
        percorso, nuovo = inietta(quale)
        prima = io.open(percorso, encoding="utf-8").read()
        if nuovo == prima:
            print("   NON INIETTATO  %s: il difetto non cambierebbe il file"
                  % quale)
            continue
        try:
            io.open(percorso, "w", encoding="utf-8").write(nuovo)
            trovati = controlla([])
            # **Visto vuol dire visto da quel controllo.** Accettare che un
            # difetto sia notato da un controllo diverso nasconde i controlli
            # che non guardano: l'M4 iniettava un'immagine a un mezzo
            # fantastico e la segnalava M2, perche' l'immagine non era fra i
            # candidati. Il difetto era visto, il controllo no.
            visto = any(p.startswith(quale + ":") for p in trovati)
            altri = [p[:60] for p in trovati if not p.startswith(quale + ":")]
            iniettati += 1
            visti += 1 if visto else 0
            print("   %-4s %s%s" % (quale, "VISTO" if visto else "NON VISTO",
                                   (": %s" % trovati[0][:80]) if trovati else
                                   " (nessun difetto: la prova non ha provato)"))
            if altri and visto:
                print("        altri controlli che l'hanno visto: %s" % altri)
        finally:
            io.open(percorso, "w", encoding="utf-8").write(prima)
    print("\ndifetti iniettati: %d, visti: %d" % (iniettati, visti))
    return 0 if (iniettati == visti and not problemi) else 1


if __name__ == "__main__":
    sys.exit(main())