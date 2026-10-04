"""Il foglio di controllo degli **emblemi**, in caratteri.

`sorgenti/art/fogli_controllo.py` compone i fogli dei **ritratti** da guardare a
vista, e li fa in HTML perche' un volto si guarda in un browser. Gli emblemi sono
un'altra cosa: sono **disegni**, e fino al 4 ottobre 2026 non avevano un foglio
che fosse un file del progetto — quello che girava era uno script ad hoc, finito
in `_foglio_emblemi.html` e poi cancellato. Un foglio che sparisce quando finisce
la sessione che l'ha prodotto non e' un foglio di controllo: e' una fotografia
di una sessione.

**Perche' in caratteri e non in HTML.** Perche' la finestra del browser del
progetto non si e' piu' composta e uno schermo non si guarda: il foglio deve
poter essere letto **nel terminale**, con `grep`, e confrontato riga per riga
con un altro. Un'immagine composta e' bella e non si interroga; qui ogni
riga del file e' un fatto e ogni difetto si cerca con una parola.

**Cosa porta ogni cella.** Il **codice**, il **nome della persona** e la
**famiglia** che l'ha fatta vincere: un foglio senza il nome non si puo' applicare
a nessuno, e i sessanta emblemi hanno nomi che sembrano di persone e non lo
sono sempre. La tessera e' ridotta di un terzo con il **medio** dei pixel di ogni
3 × 3, e resta 16 per 18 caratteri: la prova ha cominciato con un quarto (12 per
13) e le iniziali non si distinguevano piu' — un foglio di controllo che non fa
vedere il difetto che deve far vedere e' un foglio che non controlla niente.
Il carattere dice la luminosita in dieci livelli, e ogni livello conta.

**Il conto e' calcolato.** Quanti emblemi ci sono, quante famiglie e quante
persone per famiglia vengono letti dal catalogo e ricalcolati da
`emblema.classifica()`: nessun numero di questo foglio e' scritto a mano, quindi
il foglio non puo' dire che ci sono sessanta emblemi il giorno che ne sono
cinquantanove.

Uso:
    python3 sorgenti/art/foglio_emblemi.py            # scrive e riporta
    python3 sorgenti/art/foglio_emblemi.py --a-video  # non scrive, guarda
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import emblema

BASE = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(BASE, "sorgenti", "gis"))
import png_terrarium

OUT = os.path.join(BASE, "sorgenti", "art", "out")
FOGLIO = os.path.join(BASE, "sorgenti", "art", "foglio_emblemi.txt")

# Quattro caratteri per quattro livelli di luminosita, dal piu' scuro al piu'
# chiaro. Lo spazio non e' un colore: e' «qui non c'e' niente», ed e' diverso da
# un punto scuro, che si vede a schermo.
LIVELLI = "@%#*+=-:. "

# Ogni tessera e' larga 48 px: a un quarto sono 12 caratteri, e tre tessere
# stanno in 41 colonne. La riduzione e' la media dei pixel, non un campione:
# una media perde i dettagli, un campione li perde e rende il giudizio una
# moneta.
RIDUCI = 3
PER_RIGA = 2


def luminosita(griglia, x0, y0, lato, passo):
    """Il livello medio di un blocco `passo` per `passo` pixel."""
    tot, quante = 0, 0
    for y in range(y0, min(y0 + passo, len(griglia))):
        riga = griglia[y]
        for x in range(x0, min(x0 + passo, len(riga))):
            r, v, b = riga[x]
            tot += (r * 3 + v * 6 + b) // 10      # la percezione pesa il verde
            quante += 1
    if not quante:
        return 0
    media = tot / quante
    return min(len(LIVELLI) - 1, int(media * len(LIVELLI) / 256))


def tessera_in_caratteri(griglia, colonne, righe):
    """La tessera come `righe` righe di testo, ridotta di `RIDUCI`."""
    out = []
    for y in range(0, righe, RIDUCI):
        riga = ""
        for x in range(0, colonne, RIDUCI):
            riga += LIVELLI[luminosita(griglia, x, y, colonne, RIDUCI)]
        out.append(riga)
    return out


def main():
    cat = json.load(open(os.path.join(BASE, "dati", "immagini_gioco.json"),
                         encoding="utf-8"))
    persone = {n: p for n, p in cat["persone"].items()
               if p["esito"] == "emblema"}

    # La famiglia viene **ricalcolata** dal motivo, non letta dal catalogo: il
    # controllo 8 confronta le due, e un foglio che copiasse il catalogo
    # mostrerebbe la stessa risposta del difetto che il controllo cerca.
    voci = []
    for nome, p in sorted(persone.items()):
        famiglia, parola = emblema.classifica(p["motivo"])
        percorso = os.path.join(BASE, p["immagine"])
        if not os.path.exists(percorso):
            raise SystemExit("manca %s: il foglio deve guardare il file vero" %
                             percorso)
        griglia = png_terrarium.decodifica_png(open(percorso, "rb").read())
        voci.append({"nome": nome, "codice": p["usata_in"][0],
                     "famiglia": famiglia, "parola": parola,
                     "px": (len(griglia[0]), len(griglia)),
                     "disegno": tessera_in_caratteri(griglia, len(griglia[0]),
                                                     len(griglia))})

    per_famiglia = {}
    for v in voci:
        per_famiglia[v["famiglia"]] = per_famiglia.get(v["famiglia"], 0) + 1

    larghezza = max(len(d) for d in voci[0]["disegno"]) + 3
    righe = max(len(d) for d in voci[0]["disegno"])
    testo = []
    testo.append("FOGLIO DEGLI EMBLEMI")
    testo.append("")
    testo.append("Generato da sorgenti/art/foglio_emblemi.py. Ogni cella porta "
                 "il codice della tappa, il nome della persona e la famiglia che "
                 "l'ha fatta vincere, ricalcolata dal motivo.")
    testo.append("")
    testo.append("emblemi: %d   famiglie: %d" % (len(voci),
                                                  len(per_famiglia)))
    for f, n in sorted(per_famiglia.items(), key=lambda kv: (-kv[1], kv[0])):
        testo.append("  %-22s %d" % (f, n))
    testo.append("")
    for inizio in range(0, len(voci), PER_RIGA):
        blocco = voci[inizio:inizio + PER_RIGA]
        for i in range(righe):
            testo.append("  ".join(v["disegno"][i].ljust(larghezza)
                                   for v in blocco).rstrip())
        for v in blocco:
            testo.append("  " + "%s %s  %s  «%s»"
                         % (v["codice"], v["nome"][:22], v["famiglia"],
                            v["parola"]))
        testo.append("")

    corpo = "\n".join(testo) + "\n"
    if "--a-video" in sys.argv:
        sys.stdout.write(corpo)
        return 0
    with open(FOGLIO, "w", encoding="utf-8") as f:
        f.write(corpo)
    print("scritto %s (%d righe, %d emblemi)"
          % (os.path.relpath(FOGLIO, BASE), len(testo), len(voci)))
    print("guardalo con:  less sorgenti/art/foglio_emblemi.txt")
    return 0


if __name__ == "__main__":
    sys.exit(main())
