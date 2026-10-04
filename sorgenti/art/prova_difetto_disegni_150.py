"""Prova di D3: due esecuzioni, non quattro.

`verifica_disegni.py` impiega **due minuti e dieci** perche' D4 decodifica tutti
e centocinquanta i PNG in Python puro, e la prova precedente ne faceva quattro:
una prima, due per i difetti, una dopo. Quattro esecuzioni sono otto minuti, e
il tempo della prova e' scaduto con `5-18` **alterato sul disco**: la prova ha
distrutto il file che doveva controllare, che e' il modo peggiore di fallire.

Adesso: due esecuzioni, una per difetto, e il ripristino si verifica con gli sha
invece che con una terza esecuzione — che e' un confronto diretto fra il file e
la copia, non un controllo che puo' fallire per motivi suoi.

Il tempo resta dichiarato, perche' un controllo che impiega due minuti e non lo
dice sembra lento quando funziona e sembra rotto quando e' lento.
"""
import hashlib
import io
import os
import struct
import subprocess
import sys
import zlib

OUT = "sorgenti/art/out/ambienti"
CONTROLLO = "sorgenti/art/verifica_disegni.py"


def sha(p):
    return hashlib.sha1(open(p, "rb").read()).hexdigest()


def gira():
    return subprocess.run([sys.executable, CONTROLLO],
                          capture_output=True, text=True).stdout


def macchia(blob):
    """Un PNG uguale a quello dato con un pixel rosso in piu'."""
    sys.path.insert(0, "sorgenti/gis")
    from png_terrarium import decodifica_png
    g = decodifica_png(blob)
    g[2][3] = (255, 0, 0)

    def lotto(tipo, dati):
        return (struct.pack(">I", len(dati)) + tipo + dati
                + struct.pack(">I", zlib.crc32(tipo + dati) & 0xFFFFFFFF))

    grezzo = b"".join(b"\x00" + bytes(v for px in riga for v in px) for riga in g)
    return (b"\x89PNG\r\n\x1a\n"
            + lotto(b"IHDR", struct.pack(">IIBBBBB", len(g[0]), len(g), 8, 2, 0, 0, 0))
            + lotto(b"IDAT", zlib.compress(grezzo, 9)) + lotto(b"IEND", b""))


def riga(nome, tag):
    for l in nome.split("\n"):
        if tag in l:
            return l.strip()
    return ""


def prova(nome, percorso, nuovo_bytes, tag):
    """Inietta, verifica l'iniezione, gira il controllo, ripristina."""
    prima = open(percorso, "rb").read()
    aperto = hashlib.sha1(prima).hexdigest()
    if nuovo_bytes == prima:
        print("%s NON INIETTATO: il file non cambierebbe" % nome)
        return False
    open(percorso, "wb").write(nuovo_bytes)
    if sha(percorso) == aperto:
        print("%s NON INIETTATO: la scrittura non e' cambiata" % nome)
        open(percorso, "wb").write(prima)
        return False
    try:
        out = gira()
        v = bool(riga(out, tag))
        print("%s %s" % (nome, "VISTO" if v else "NON VISTO"))
        print("   %s" % riga(out, tag))
        return v
    finally:
        open(percorso, "wb").write(prima)
        ripristinato = sha(percorso) == aperto
        print("   ripristinato: %s" % ripristinato)


visti = 0

# F1: il disegnatore perde un edificio. 2-5 ha 22 sagome e 2-8 ne ha 20: dati
# diversi, e il controllo deve dire che lo stesso disegno non e' giustificato.
visti += 1 if prova(
    "F1 il disegnatore perde un edificio    :",
    os.path.join(OUT, "ambiente_2-5.png"),
    open(os.path.join(OUT, "ambiente_2-8.png"), "rb").read(),
    "perde qualcosa") else 0

# F2: il disegnatore aggiunge una macchia. 5-18 e 5-22 hanno gli stessi dati:
# si altera solo 5-18, che e' il file piu' piccolo, e il controllo deve dire
# che la differenza non e' giustificata dai dati.
visti += 1 if prova(
    "F2 il disegnatore aggiunge una macchia :",
    os.path.join(OUT, "ambiente_5-18.png"),
    macchia(open(os.path.join(OUT, "ambiente_5-18.png"), "rb").read()),
    "aggiunge qualcosa") else 0

print("\ndifetti iniettati: 2, visti: %d" % visti)
sys.exit(0 if visti == 2 else 1)