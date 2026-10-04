"""Le dieci cifre del font, disegnate come le lettere: cinque per sette.

Il font di `emblema.py` aveva **solo le ventisei lettere**, e i premi hanno
bisogno del **numero della tappa**: senza le cifre `FONT.get("2", [])`
restituisce una lista vuota e la tessera non disegna niente. Duecento tessere
su mille e cinquanta erano quindi identiche alle rispettive vicine, e il
controllo Q3 lo ha visto subito — che è il suo lavoro.

Il perché sta nella griglia come nelle lettere: cinque pixel di larghezza e
sette di altezza, il pennello in alto a sinistra, perche' una cifra disegnata
con un altro passo da quella delle lettere sembrerebbe un altro carattere.
"""

CIFRE = {
    "0": (" ### ", "#   #", "#  ##", "# # #", "##  #", "#   #", " ### "),
    "1": ("  #  ", " ##  ", "  #  ", "  #  ", "  #  ", "  #  ", " ### "),
    "2": (" ### ", "#   #", "    #", "   # ", "  #  ", " #   ", "#####"),
    "3": ("#####", "   # ", "  #  ", "   # ", "    #", "#   #", " ### "),
    "4": ("   # ", "  ## ", " # # ", "#  # ", "#####", "   # ", "   # "),
    "5": ("#####", "#    ", "#### ", "    #", "    #", "#   #", " ### "),
    "6": ("  ## ", " #   ", "#    ", "#### ", "#   #", "#   #", " ### "),
    "7": ("#####", "    #", "   # ", "  #  ", " #   ", " #   ", " #   "),
    "8": (" ### ", "#   #", "#   #", " ### ", "#   #", "#   #", " ### "),
    "9": (" ### ", "#   #", "#   #", " ####", "    #", "   # ", " ##  "),
}


def come_font():
    """Le cifre nel formato del font: una riga per riga, con `#` e spazi.

    Le lettere di `emblema.FONT` sono liste di stringhe con `#` e `.`, e non
    con spazi: vengono convertite qui perche' il confronto pixel per pixel dei
    due formati fa fallire ogni controllo che li confronti.
    """
    return {c: [r.replace("#", "#").replace(" ", ".")
                for r in righe] for c, righe in CIFRE.items()}


if __name__ == "__main__":
    for c, righe in sorted(CIFRE.items()):
        print(c)
        for r in righe:
            print("   " + r)
