#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Conta le questioni aperte dichiarate nei documenti di progetto.

Un documento che dichiara un numero di questioni senza che nessuno lo conti
diventa un documento che mente fra tre versioni. Questo script conta, e il
riscontro è con `docs/videogioco-5-duchi-audit.md`.

**Il criterio, dichiarato**, perché un conteggio senza criterio non è un dato:

  voce    un punto della sezione «Questioni aperte», in tre forme possibili,
          tutte riconosciute:
            - un elenco numerato:  `1. **Il buco di S66.** ...`
            - un sottotitolo:      `### Q1 — il titolo`
            - una riga di tabella: `| 1 | la domanda | **chiusa** — ... |`
  chiusa  una voce che porta una marcatura di chiusa **nella sua prima
          riga**: «chiusa», «chiuso», «chiuse», «risolto», «ratificata»,
          «confermata». La prima riga e non tutto il corpo, perché una voce
          aperta spiega dentro il corpo per quale parte è stata chiusa: se si
          contasse tutta la voce, ogni questione parzialmente risolta
          sembrerebbe chiusa

Il confronto finale verifica i numeri che l'audit dichiara: se non tornano, è
l'audit che ha torto, e lo dice.

Uso:
    python3 sorgenti/lingue/conta_questioni.py
"""
import glob
import os
import re
import sys

RADICE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
DOCS = os.path.join(RADICE, "docs")

CHIUSA = re.compile(
    r"chius[aeio]|chiusi|risolt|ratificat|confermata|confermato|confermati", re.I)

FORME = [
    re.compile(r"^\s*\d+\.\s+"),
    re.compile(r"^###+\s*Q\d+\s*[-—:.]?\s*"),
    re.compile(r"^\|\s*\*{0,2}Q?\d+\*{0,2}\s*\|"),
    # I documenti trasversali recenti scrivono le questioni in due forme che
    # il contatore deve vedere, altrimenti l'audit si ferma ai tredici
    # documenti più vecchi e non conta le dodici domande più importanti:
    #   percorsi.md       `### Q1 — la domanda`
    #   fonti-visive.md   `**Q1 — la domanda**`
    re.compile(r"^###+\s+Q\d+\s*[-—:.]"),
    re.compile(r"^\*\*Q\d+\s*[-—:.]"),
]

# I documenti chiamano la sezione in due modi: «Questioni aperte» e «Le
# questioni aperte». La regex accetta entrambi, perché un contatore che vede
# tredici documenti su quindici sbaglia il conto e l'audit dice un numero falso.
SEZIONE = re.compile(r"^##+\s*[\d.]*\s*(?:Le\s+)?[Qq]uestioni aperte(.*?)(?=^##\s|\Z)",
                     re.M | re.S)


def sezione_voci(sezione):
    """Le voci della sezione: (prima riga, numero di riga)."""
    righe = sezione.split("\n")
    fuori = []
    for i, riga in enumerate(righe):
        if riga.startswith("|"):
            # dentro una tabella la prima riga utile è quella dei dati, non la
            # testata: la riga dei trattini si salta
            if re.match(r"^\|\s*-{2,}", riga):
                continue
        for forma in FORME:
            if forma.match(riga):
                fuori.append((riga.strip(), i))
                break
    return fuori


def main():
    righe = []
    aperte = chiuse = 0
    for percorso in sorted(glob.glob(os.path.join(DOCS, "*.md"))):
        testo = open(percorso, encoding="utf-8").read()
        elenco = []
        for m in SEZIONE.finditer(testo):
            elenco += sezione_voci(m.group(1))
        if not elenco:
            continue
        # una stessa voce presa da due forme conta una volta sola
        uniche = []
        for riga, pos in elenco:
            if not uniche or uniche[-1] != riga:
                uniche.append(riga)
        a = sum(1 for r in uniche if not CHIUSA.search(r))
        c = len(uniche) - a
        righe.append((os.path.basename(percorso), a, c))
        aperte += a
        chiuse += c

    print("%-46s %8s %8s" % ("documento", "aperte", "chiuse"))
    for nome, a, c in righe:
        print("%-46s %8d %8d" % (nome, a, c))
    print("-" * 64)
    print("%-46s %8d %8d" % ("TOTALE", aperte, chiuse))
    print("somma: %d" % (aperte + chiuse))

    audit = os.path.join(DOCS, "videogioco-5-duchi-audit.md")
    problemi = []
    if os.path.exists(audit):
        testo = open(audit, encoding="utf-8").read()

        # La tabella del §1, che e' **dove stanno i numeri**. La versione di prima di
        # questo controllo cercava la forma di prosa «**N** chiuse», e in un documento
        # che scrive i numeri in tabella quella forma non compare: la ricerca non
        # trovava niente, il controllo passava, e l'audit dichiarava **115 voci** mentre
        # il conto ne trovava **118**. Il difetto non era nel numero ma nel controllo che
        # doveva confermarlo — e un controllo che non guarda niente e' verde come un
        # controllo che guarda: solo che il verde del primo non significa niente.
        dichiarati = {}
        for riga in testo.split("\n"):
            m = re.match(r"^\|\s*\**(Voci enumerate|Chiuse|Aperte)\**\s*\|\s*\*\*(\d+)\*\*\s*\|",
                         riga)
            if m:
                dichiarati[m.group(1)] = int(m.group(2))
        if not dichiarati:
            problemi.append("non trovo la tabella dei numeri nel §1 dell'audit: "
                            "il controllo non pu' confermare niente")
        # tutte e tre le righe devono essere **leggibili**: una cella che perde il
        # grassetto sparisce dalla ricerca, e una riga che sparisce e' una riga che
        # il controllo non guarda piu'. Meglio un controllo che si rifiuta di tacere
        # che un controllo che tace.
        for chiave in ("Voci enumerate", "Chiuse", "Aperte"):
            if chiave not in dichiarati:
                problemi.append("la riga «%s» del §1 dell'audit non e' leggibile: "
                                "il numero c'e' ma il controllo non lo vede"
                                % chiave.lower())
        for chiave, reale in (("Voci enumerate", aperte + chiuse),
                              ("Chiuse", chiuse), ("Aperte", aperte)):
            if chiave in dichiarati and dichiarati[chiave] != reale:
                problemi.append("l'audit dichiara %s = %d, il conto dà %d"
                                % (chiave.lower(), dichiarati[chiave], reale))

        # E i numeri in prosa della sezione 1, che devono dire la stessa cosa.
        sezione1 = re.search(r"^##\s*1\..*?(?=^##\s)", testo, re.M | re.S)
        if sezione1:
            corpo = sezione1.group(0)
            m = re.search(r"\*\*(\d+) voci non sono \d+ domande\*\*", corpo)
            if m and int(m.group(1)) != aperte + chiuse:
                problemi.append("il §1 scrive «%s voci non sono … domande», "
                                "la somma è %d" % (m.group(1), aperte + chiuse))
            m = re.search(r"nessuna delle (\w+) chiuse", corpo, re.I)
            if m:
                parola = {"ventinove": 29, "trenta": 30, "ventotto": 28,
                          "ventisette": 27, "ventisei": 26}.get(m.group(1).lower())
                if parola is not None and parola != chiuse:
                    problemi.append("il §1 scrive «nessuna delle %s chiuse», "
                                    "il conto ne trova %d" % (m.group(1), chiuse))
    if problemi:
        print("problemi: %d" % len(problemi))
        for p in problemi:
            print("  " + p)
    else:
        print("problemi: 0")
        print("(l'audit dichiara i numeri del §1 e il conto li conferma)")
    return 1 if problemi else 0


if __name__ == "__main__":
    sys.exit(main())