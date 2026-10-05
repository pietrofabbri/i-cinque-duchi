"""Verifica i registri delle modifiche di tutti i documenti: R1-R4.

Quattro numeri e una forma, e sono le cose che il progetto non aveva mai
controllate. Il difetto che le ha motivate e' comparso quattro volte in quattro
giorni, sempre nella stessa forma: **una riga scritta due volte, o non scritta,
non lascia traccia nei controlli dei numeri**, perche' i numeri sono giusti in
entrambi i casi.

  R1  ogni versione fra la piu' remota e la piu' recente ha la sua riga
  R2  nessuna versione ha due righe
  R3  ogni registro e' monotono, in un verso o nell'altro
  R4  ogni tabella di registro ha la riga di separazione sotto l'intestazione
  R5  nessuna intestazione di sezione e' scritta due volte

Uso:  python3 sorgenti/verifica_registri.py            # tutti i documenti
      python3 sorgenti/verifica_registri.py --difetti  # ne inietta quattro, uno per volta
"""
import collections
import io
import os
import re
import sys

RADICE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(RADICE, "docs")

RIGA_TAB = re.compile(r"^\| (\d\d)/(\d\d)/(\d{4}) \| 0\.(\d+) \|", re.M)
RIGA_ELENCO = re.compile(r"^- \*\*v0\.(\d+) \((\d\d)/(\d\d)/(\d{4})\)\*\*", re.M)
INTESTAZIONE = "| Data | Versione | Che cosa è cambiato |"
SEZIONE = re.compile(r"(?m)^(#{2,3} .+)$")
SEPARAZIONE = "|---|---|---|"


def leggi(path):
    with io.open(path, encoding="utf-8") as f:
        return f.read()


def versioni_doc(testo):
    """Le (versione, data) del registro, dalla tabella e dall'elenco."""
    tab = [(int(v), "%s/%s/%s" % (a, m, g))
           for g, m, a, v in RIGA_TAB.findall(testo)]
    elenco = [(int(v), "%s/%s/%s" % (a, m, g))
              for v, g, m, a in RIGA_ELENCO.findall(testo)]
    return tab, elenco


def monotono(blocchi):
    """Il verso del registro: -1 dalla piu' recente, +1 dalla piu' remota.

    `None` quando i blocchi non vanno tutti nello stesso verso, il che non e'
    un difetto: sono due registri paralleli e ognuno ha la sua convenzione.
    """
    versi = set()
    for blocco in blocchi:
        if len(blocco) < 2:
            continue
        versi.add(-1 if blocco == sorted(blocco, reverse=True)
                  else 1 if blocco == sorted(blocco) else None)
    if len(versi) == 1:
        return versi.pop()
    return None


def controlla(testo, nome, problemi):
    tab, elenco = versioni_doc(testo)
    righe = tab + elenco
    if len(righe) < 2:
        return
    presenti = [v for v, _ in righe]

    # R1: nessuna versione salta fra la piu' remota e la piu' recente
    for v in range(min(presenti), max(presenti) + 1):
        if v not in presenti:
            problemi.append("R1 %s: la versione 0.%d non ha riga di registro"
                            % (nome, v))

    # R2: nessuna versione due volte
    for v in sorted(set(presenti)):
        if presenti.count(v) > 1:
            problemi.append("R2 %s: la versione 0.%d ha due righe" % (nome, v))

    # R3: ogni registro e' monotono, in un verso o nell'altro
    for blocco, che_cosa in ((tab, "tabella"), (elenco, "elenco")):
        if len(blocco) < 2:
            continue
        if blocco != sorted(blocco) and blocco != sorted(blocco, reverse=True):
            problemi.append("R3 %s: la %s del registro non e' in ordine, e non "
                            "e' nemmeno al contrario" % (nome, che_cosa))

    # R5: nessuna intestazione di sezione due volte. Il difetto che l'ha
    # motivato era una intestazione di registro scritta due volte di fila:
    # nessuno dei quattro controlli precedenti la vedeva, perche' guardano le
    # righe del registro e non le intestazioni che lo contengono. Una riga in
    # piu' non lascia traccia nei numeri — che e' la regola di questo progetto,
    # detta meglio: *una riga scritta due volte, o non scritta, non lascia
    # traccia nei controlli dei numeri* vale anche per le righe che non sono
    # numeri.
    for titolo, quante in sorted(collections.Counter(
            SEZIONE.findall(testo)).items()):
        if quante > 1:
            problemi.append("R5 %s: l'intestazione %r c'e' %d volte"
                            % (nome, titolo, quante))

    # R4: la tabella ha la riga di separazione sotto l'intestazione
    if INTESTAZIONE in testo:
        i = testo.index(INTESTAZIONE)
        finestra = testo[i:i + len(INTESTAZIONE) + len(SEPARAZIONE) + 2]
        if SEPARAZIONE not in finestra:
            problemi.append("R4 %s: la tabella del registro non ha la riga di "
                            "separazione" % nome)


def inietta(testo, difetto):
    """Un difetto alla volta, perche' iniettarli insieme fa fermare la prova al
    primo trovato e gli altri due non vengono mai guardati."""
    if difetto == "R1":
        # una versione che salta: la piu' recente sale di due
        tab = [(int(v), "%s/%s/%s" % (a, m, g))
               for g, m, a, v in RIGA_TAB.findall(testo)]
        if not tab:
            return None
        i = testo.index("| Data | Versione | Che cosa è cambiato |\n"
                        + SEPARAZIONE + "\n") + len(
            "| Data | Versione | Che cosa è cambiato |\n" + SEPARAZIONE + "\n")
        salto = max(v for v, _ in tab) + 2
        return (testo[:i] + "| 04/10/2026 | 0.%d | riga iniettata |\n" % salto
                + testo[i:])
    if difetto == "R2":
        # la stessa versione due volte
        m = RIGA_TAB.search(testo)
        if not m:
            return None
        return testo[:m.start()] + m.group(0) + "\n" + testo[m.start():]
    if difetto == "R4":
        # la tabella del registro senza la riga di separazione: va tolta
        # **quella**, non la prima del file, che puo' essere di un'altra
        # tabella — ed e' successo: la rimozioneAVA colpito l'altra e R4
        # non vedeva niente
        if INTESTAZIONE not in testo:
            return None
        i = testo.index(INTESTAZIONE)
        j = testo.find(SEPARAZIONE + "\n", i)
        if j < 0 or j - i > len(INTESTAZIONE) + 2:
            return None
        return testo[:j] + testo[j + len(SEPARAZIONE) + 1:]
    if difetto == "R5":
        # l'intestazione della sezione del registro scritta due volte
        m = re.search(r"(?m)^#{2,3} .+$", testo)
        if not m:
            return None
        return testo[:m.end()] + "\n\n" + m.group(0) + "\n" + testo[m.end():]
    raise ValueError(difetto)


def main():
    sola_prova = "--difetti" in sys.argv
    problemi = []
    con_registro = 0
    documenti = [n for n in sorted(os.listdir(DOCS)) if n.endswith(".md")]

    for nome in documenti:
        testo = leggi(os.path.join(DOCS, nome))
        tab, elenco = versioni_doc(testo)
        if len(tab) + len(elenco) < 2:
            continue
        con_registro += 1
        controlla(testo, nome, problemi)

    print("== R1-R5. i registri delle modifiche")
    print("   documenti con registro: %d su %d" % (con_registro, len(documenti)))
    if problemi:
        for p in problemi:
            print("   difetto %s" % p)
    else:
        print("   nessuna versione salta, nessuna riga e' doppia, nessun "
              "registro e' fuori ordine, nessuna tabella senza separazione, "
              "nessuna intestazione ripetuta")

    if sola_prova:
        candidati = []
        per_r5 = []
        for nome in documenti:
            testo = leggi(os.path.join(DOCS, nome))
            tab, _ = versioni_doc(testo)
            if len(tab) >= 3:
                candidati.append((nome, testo))
            # R5 cerca un'intestazione di sezione e non una riga di registro:
            # chiedergli lo stesso candidato degli altri lo lasciava senza
            # nessuno da guardare, e la prova finiva «NON INIETTATO» — che e'
            # un difetto che si dichiara e non si fa notare. I quattro difetti
            # hanno bisogno di quattro documenti diversi per non accumularsi.
            if SEZIONE.search(testo):
                per_r5.append((nome, testo))
        iniettati = 0
        visti = 0
        # un difetto alla volta, ciascuno su un documento diverso: iniettarli
        # insieme fa fermare la prova al primo trovato e gli altri non vengono
        # guardati, che e' il difetto che questa sezione dell'audit descrive
        for numero, difetto in enumerate(("R1", "R2", "R4", "R5")):
            if difetto == "R5":
                if numero >= len(per_r5):
                    print("   NON INIETTATO  %s: nessun documento con "
                          "un'intestazione di sezione" % difetto)
                    continue
                nome, testo = per_r5[numero]
            else:
                if numero >= len(candidati):
                    print("   NON INIETTATO  %s: nessun documento con una "
                          "tabella di registro" % difetto)
                    continue
                nome, testo = candidati[numero]
            alterato = inietta(testo, difetto)
            if alterato is None:
                print("   NON INIETTATO  %s su %s" % (difetto, nome))
                continue
            iniettati += 1
            problemi2 = []
            controlla(alterato, nome + " (difetto)", problemi2)
            trovati = [p for p in problemi2 if p.startswith(difetto + " ")]
            if trovati:
                visti += 1
                for p in trovati:
                    print("   visto   %s" % p[:110])
            else:
                print("   NON VISTO  %s su %s" % (difetto, nome))
        print("\ndifetti iniettati: %d, visti: %d, non visti: %d"
              % (iniettati, visti, iniettati - visti))
        if visti != iniettati:
            return 1

    return 1 if problemi else 0


if __name__ == "__main__":
    sys.exit(main())
