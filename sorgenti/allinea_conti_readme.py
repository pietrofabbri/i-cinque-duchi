#!/usr/bin/env python3
"""Riporta nel README i conti che i verificatori hanno calcolato.

Tre tabelle del `README.md` scrivono numeri che un programma conta: «Il conto
dei controlli» (`verifica_prove.py`, X6), «I numeri scritti in prosa»
(`verifica_numeri.py`, N5) e «Il registro dei buchi aperti»
(`verifica_buchi.py`, B5). I tre verificatori confrontano la riga con il conto
e, quando non tornano, lo dicono con una frase di forma fissa:

    la riga «<etichetta>» dichiara <X>, il conto e' <Y>
    la riga «<etichetta>» dichiara <X>, il registro ne ha <Y>

Ogni documento aggiunto o tolto fa cambiare quattro o cinque di quei numeri, e
correggerli a mano e' esattamente la forma di lavoro che il progetto vuole
evitare: un numero scritto a mano invecchia, uno calcolato no. Questo script
esegue i tre verificatori, legge le frasi e scrive il conto nella riga.

**Che cosa non fa.** Non cambia la frase intorno ai numeri e non tocca i
numeri scritti in lettere nella prosa: quelli li legge una persona, e se il
conto cambia la frase va riletta (i verificatori li segnalano a parte). Non
scrive niente se un verificatore e' rosso per un motivo diverso da un conto
della sua tabella: in quel caso si ferma e lo dice.

Uso:
    python3 sorgenti/allinea_conti_readme.py          # scrive
    python3 sorgenti/allinea_conti_readme.py --prova  # dice che cosa scriverebbe
"""
import io
import os
import re
import subprocess
import sys

RADICE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
README = os.path.join(RADICE, "README.md")
VERIFICATORI = ["verifica_numeri.py", "verifica_buchi.py", "verifica_prove.py"]
FRASE = re.compile(r"README\.md: la riga «([^»]+)» dichiara (\d+), "
                   r"(?:il conto e'|il registro ne ha) (\d+)")


def conti():
    """(etichetta, dichiarato, contato) da tutti e tre i verificatori, e gli
    altri difetti che non sono conti del README."""
    trovati, altri = {}, []
    for v in VERIFICATORI:
        uscita = subprocess.run([sys.executable, os.path.join(RADICE, "sorgenti", v)],
                                capture_output=True, text=True, cwd=RADICE)
        for riga in uscita.stdout.splitlines():
            if not riga.strip().startswith("difetto"):
                continue
            m = FRASE.search(riga)
            if m:
                trovati[m.group(1)] = (int(m.group(2)), int(m.group(3)))
            elif "prova del difetto e' rossa" not in riga and "inventario" not in riga:
                # una prova del difetto e' rossa finche' il README non torna:
                # e' l'effetto, non la causa
                altri.append("%s: %s" % (v, riga.strip()))
    return trovati, altri


def main(argv):
    """Si ripete finche' i conti sono stabili, al piu' quattro volte.

    Una riga dipende dalle altre: «Prove eseguite da questo controllo» conta le
    prove del difetto che passano, e una prova non passa finche' il README ha
    un altro conto sbagliato. Al primo giro quella riga scende, al secondo
    torna su: il giro buono e' l'ultimo, quello che non cambia piu' niente.
    """
    if "--prova" in argv:
        return giro(True)
    for _ in range(4):
        esito = giro(False)
        if esito != "scritto":
            return esito
    print("i conti non si stabilizzano dopo quattro giri: guardali a mano")
    return 1


def giro(solo_dire):
    trovati, altri = conti()
    if altri:
        print("non scrivo: ci sono difetti che non sono conti del README")
        for a in altri:
            print("  " + a)
        return 1
    with io.open(README, encoding="utf-8") as f:
        testo = f.read()
    nuovo = testo
    for etichetta, (era, giusto) in sorted(trovati.items()):
        riga = re.compile(r"^(\| %s \| \*\*)%d(\*\* \|)$" % (re.escape(etichetta), era), re.M)
        nuovo, n = riga.subn(r"\g<1>%d\g<2>" % giusto, nuovo)
        print("  %-52s %5d -> %-5d %s" % (etichetta, era, giusto,
                                          "scritto" if n and not solo_dire else
                                          ("da scrivere" if n else "RIGA NON TROVATA")))
    if not trovati:
        print("i conti del README tornano")
    if nuovo != testo and not solo_dire:
        with io.open(README, "w", encoding="utf-8") as f:
            f.write(nuovo)
        return "scritto"
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
