#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Il registro dei buchi del progetto, in un file solo: B1-B5.

I buchi conosciuti — le cose che un controllo dichiara di non poter guardare —
vivevano in tre dizionari, in tre file: `TACITI` in `verifica_prove.py`, `SENZA`
e `SENZA_APPOGGIO` in `verifica_numeri.py`. Un registro in tre posti non è un
registro: cercarlo costa tre ricerche, e quando ne nasce uno in uno solo degli
elenchi nessuno lo vede.

Ora l'unico posto dove si scrive è `dati/buchi_aperto.json`, e i tre dizionari
lo leggono. Questo controllo tiene il registro onesto.

  B1  ogni voce ha un motivo, e il motivo non è una scusa: vuoto no, e la
      parola «tempo» non è un motivo
  B2  nessuna chiave può stare in due elenchi: un documento che ha un
      controllo non può essere anche nell'elenco di quelli che non ne hanno
  B3  ogni voce è guardata da qualcuno: lo script che possiede l'elenco esiste
      e lo legge davvero, non lo dichiara e non lo usa
  B4  ogni voce dice a chi appartiene e qual è la sua natura
  B5  il conto dei buchi è quello che il README dichiara, e non cresce da solo

Uso:  python3 sorgenti/verifica_buchi.py
      python3 sorgenti/verifica_buchi.py --difetti
"""
import io
import json
import os
import re
import sys

RADICE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RADICE, "sorgenti"))
import buchi  # noqa: E402

README = os.path.join(RADICE, "README.md")
SEZIONE = "## Il registro dei buchi aperti"
# Chi possiede ogni elenco: il file che lo legge, e il controllo che lo usa.
PROPRIETARIO = {
    "TACITI": ("sorgenti/verifica_prove.py", "X4"),
    "SENZA": ("sorgenti/verifica_numeri.py", "N2"),
    "SENZA_APPOGGIO": ("sorgenti/verifica_numeri.py", "N4"),
}
# Parole che non sono un motivo: dicono quando manca il tempo, non perché.
# Le frasi si cercano per intero; le parole sole si cercano con i confini di
# parola, perché «poi» dentro «poiché» è una congiunzione e non una scusa.
NON_MOTIVO_FRASE = ("non c'e' tempo", "non c'è tempo", "prima o poi",
                    "non ho tempo", "manca tempo", "tempo che manca")
NON_MOTIVO_PAROLA = ("poi", "tempo")
CONTI = ("Buchi dichiarati", "Verificatori che non dichiarano i controlli",
         "Documenti senza un controllo dei numeri",
         "Dichiarazioni senza riscontro nel codice")


def leggi(path):
    with io.open(path, encoding="utf-8") as f:
        return f.read()


def conta(registro=None):
    registro = buchi.leggi() if registro is None else registro
    voci = registro.get("buchi", [])
    return {
        "Buchi dichiarati": len(voci),
        "Verificatori che non dichiarano i controlli":
            len([b for b in voci if b["elenco"] == "TACITI"]),
        "Documenti senza un controllo dei numeri":
            len([b for b in voci if b["elenco"] == "SENZA"]),
        "Dichiarazioni senza riscontro nel codice":
            len([b for b in voci if b["elenco"] == "SENZA_APPOGGIO"]),
    }


def leggi_conto(testo):
    dentro = False
    letto = {}
    for riga in testo.splitlines():
        if riga.startswith("## "):
            dentro = riga.strip() == SEZIONE
            continue
        if not dentro:
            continue
        m = re.match(r"^\|\s*([^|]+?)\s*\|\s*\*\*(\d+)\*\*\s*\|\s*$", riga)
        if m:
            letto[m.group(1)] = int(m.group(2))
    return letto


def controlla(problemi, registro=None):
    registro = buchi.leggi() if registro is None else registro
    voci = registro.get("buchi", [])
    visti = set()

    for b in voci:
        chiave = b.get("chiave", "")
        motivo = " ".join(str(b.get("motivo", "")).split())

        # ---- B1: il motivo c'è, ed è un motivo
        if not motivo:
            problemi.append(
                "B1 %s (%s): la voce ha un motivo vuoto: un buco senza motivo "
                "non e' un buco dichiarato, e' una casella" % (chiave,
                                                              b["elenco"]))
        else:
            basso = motivo.lower()
            scusa = [f for f in NON_MOTIVO_FRASE if f in basso]
            scusa += [p for p in NON_MOTIVO_PAROLA
                      if re.search(r"\b%s\b" % re.escape(p), basso)]
            if scusa:
                problemi.append(
                    "B1 %s (%s): il motivo dice quando manca il tempo, non "
                    "perche' il buco c'e': «%s»" % (chiave, b["elenco"],
                                                    motivo[:60]))

        # ---- B4: la voce dice a chi appartiene e qual e' la sua natura
        if b.get("elenco") not in PROPRIETARIO:
            problemi.append(
                "B4 %s: l'elenco %r non e' fra quelli che il registro "
                "riconosce (%s): un elenco che esiste solo qui e' un registro "
                "che e' tornato a essere piu' di uno"
                % (chiave, b.get("elenco"), ", ".join(sorted(PROPRIETARIO))))
            continue
        if not b.get("natura", "").strip():
            problemi.append("B4 %s: la voce non dice che natura ha il buco"
                            % chiave)
        if not b.get("guardato_da", "").strip():
            problemi.append(
                "B4 %s: la voce non dice quale controllo la tiene d'occhio"
                % chiave)

        # ---- B2: nessuna chiave in due elenchi
        if (b["elenco"], chiave) in visti:
            problemi.append(
                "B2 %s: la chiave compare due volte nel registro, e un buco "
                "doppio e' un buco che nessuno guarda due volte" % chiave)
        visti.add((b["elenco"], chiave))

        # ---- B3: lo script che possiede l'elenco lo legge davvero
        percorso, controllo = PROPRIETARIO[b["elenco"]]
        sorgente = os.path.join(RADICE, percorso)
        if not os.path.exists(sorgente):
            problemi.append(
                "B3 %s: l'elenco %s dovrebbe stare in %s, che nel ramo non c'e'"
                % (chiave, b["elenco"], percorso))
            continue
        testo = leggi(sorgente)
        # **anche lo script che la voce dichiara deve leggere l'elenco.** Una
        # voce che nomina un proprietario che non legge niente e' una voce che
        # punta a un posto dove nessuno guarda.
        dichiarato = str(b.get("guardato_da", ""))
        m = re.search(r"(sorgenti/[\w./-]+\.py)", dichiarato)
        if m is None:
            problemi.append(
                "B3 %s: la voce non nomina lo script che tiene d'occhio il "
                "buco: «%s»" % (chiave, dichiarato[:50]))
        else:
            altro = os.path.join(RADICE, m.group(1))
            if (not os.path.exists(altro)
                    or ('buchi.elenco("%s")' % b["elenco"])
                    not in leggi(altro)):
                problemi.append(
                    "B3 %s: la voce dice che %s tiene d'occhio il buco, e %s "
                    "non legge l'elenco %s"
                    % (chiave, m.group(1), m.group(1), b["elenco"]))
        if ('buchi.elenco("%s")' % b["elenco"]) not in testo:
            problemi.append(
                "B3 %s: %s non legge l'elenco %s dal registro: un elenco "
                "dichiarato e non letto e' un elenco che qualcuno scrive e "
                "nessuno guarda" % (chiave, percorso, b["elenco"]))
        if controllo not in testo:
            problemi.append(
                "B3 %s: %s non contiene il controllo %s che dovrebbe "
                "guardare l'elenco" % (chiave, percorso, controllo))

    # ---- B2 fra elenchi diversi: un documento non può essere in due posti
    taciti = set(b["chiave"] for b in voci if b["elenco"] == "TACITI")
    senza = set(b["chiave"] for b in voci if b["elenco"] == "SENZA")
    # le chiavi sono percorsi e nomi di documento, quindi non si sovrappongono
    # per costruzione: quello che si controlla è che il registro copra
    # davvero tutto quello che i due controlli pretendono di coprire
    import verifica_numeri  # noqa: E402
    for nome in senza:
        if nome in verifica_numeri.GUARDATO:
            problemi.append(
                "B2 %s: e' nell'elenco dei documenti senza controllo, e "
                "dichiara il controllo %s: un documento non e' senza controllo "
                "e con controllo" % (nome, ",".join(
                    verifica_numeri.GUARDATO[nome])))
    import verifica_prove  # noqa: E402
    for percorso in taciti:
        completo = os.path.join(RADICE, percorso)
        dichiarate = (verifica_prove.dichiarate(leggi(completo))
                      if os.path.exists(completo) else [])
        if dichiarate:
            problemi.append(
                "B2 %s: e' nell'elenco dei verificatori che non dichiarano i "
                "controlli, e il file ne dichiara %d: la voce e' indietro "
                "rispetto alla realta'"
                % (percorso, len(dichiarate)))

    # ---- B5: il conto è quello dichiarato
    letto = leggi_conto(leggi(README))
    atteso = conta(registro)
    for riga, valore in atteso.items():
        if riga not in letto:
            problemi.append(
                "B5 README.md: la tabella dei buchi non ha la riga «%s»" % riga)
        elif letto[riga] != valore:
            problemi.append(
                "B5 README.md: la riga «%s» dichiara %d, il registro ne ha %d"
                % (riga, letto[riga], valore))
    return atteso


def inietta(registro, difetto):
    """Un difetto alla volta, sul registro in memoria."""
    import copy
    r = copy.deepcopy(registro)
    voci = r.get("buchi", [])
    if difetto == "B1":
        if not voci:
            return None
        voci[0]["motivo"] = "  "
        return r
    if difetto == "B2":
        # la stessa voce due volte nello stesso elenco: un buco doppio e' un
        # buco che nessuno guarda due volte
        if not voci:
            return None
        r["buchi"].append(copy.deepcopy(voci[0]))
        return r
    if difetto == "B3":
        # una voce che dichiara un proprietario che non legge quell'elenco
        if not voci:
            return None
        voci[0]["guardato_da"] = "sorgenti/verifica_buchi.py, controllo B1"
        return r
    if difetto == "B4":
        if not voci:
            return None
        voci[0]["natura"] = ""
        return r
    if difetto == "B5":
        r["buchi"] = voci[:-1] if voci else []
        return r
    raise ValueError(difetto)


def main():
    sola_prova = "--difetti" in sys.argv
    registro = buchi.leggi()
    problemi = []
    atteso = controlla(problemi, registro)

    print("== B1-B5. il registro dei buchi aperti")
    print("   buchi dichiarati: %d" % atteso["Buchi dichiarati"])
    for chiave in CONTI[1:]:
        print("   %s: %d" % (chiave.lower(), atteso[chiave]))
    if problemi:
        for p in problemi:
            print("   difetto %s" % p)
    else:
        print("   ogni buco ha un motivo che e' un motivo, nessuno sta in due "
              "elenchi, ogni elenco e' letto dal suo proprietario, e il conto "
              "e' quello dichiarato")

    if sola_prova:
        iniettati = 0
        visti = 0
        for difetto in ("B1", "B2", "B3", "B4", "B5"):
            alterato = inietta(registro, difetto)
            if alterato is None:
                print("   NON INIETTATO  %s" % difetto)
                continue
            iniettati += 1
            p2 = []
            controlla(p2, alterato)
            trovati = [p for p in p2 if p.startswith(difetto + " ")]
            if trovati:
                visti += 1
                for p in trovati[:2]:
                    print("   visto   %s" % p[:110])
            else:
                print("   NON VISTO  %s" % difetto)
        print("\ndifetti iniettati: %d, visti: %d, non visti: %d"
              % (iniettati, visti, iniettati - visti))
        if visti != iniettati:
            return 1

    return 1 if problemi else 0


if __name__ == "__main__":
    sys.exit(main())
