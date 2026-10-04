"""Disegna gli ambienti dei livelli in PNG, dalla sagoma e dalla griglia.

**Che cosa fa.** Ogni tappa diventa un'immagine: le sagome degli edifici del
suo livello, prese da `dati/edifici_footprint.json` per chiave di livello, e
la sua griglia da `dati/ambienti_livelli.json`. Nessun nome viene abbinato a
mano: se un livello non ha record, l'immagine esce vuota e il file lo dichiara.

**Perche' un disegno e non una fotografia.** Le foto esistono gia' per i luoghi
(`immagini_gioco.json`), ma la foto non si puo' mettere in una zona di
vento metri per quindici: ingrandita diventa una macchia. Qui la scala e' di
`PXL_PER_M` pixel per metro ed e' la stessa che il documento della tappa 1-1
usa per i suoi sprite; il riquadro non e' scritto, e' l'inviluppo delle sagome
del livello con la griglia come minimo.

**L'altezza non si inventa.** Un edificio con `altezza_m` viene estruso a
quell'altezza. Un edificio con `altezza_m: null` esce come **volume neutro**,
alto `NEUTRO_M` metri: la regola e' `fonti-visive.md` 4.3, «una forma che non
e' verificata non si disegna», e qui la cosa non verificata e' esattamente
l'altezza. Il disegno non distingue i due casi a occhio, e non deve: quello
che li distingue e' il dato.

**Come e' fatto il disegno, e che cosa non sa fare.** Ogni edificio e' il
**rettangolo che occupa** visto dalla zona, ritagliato ai bordi, con l'altezza
che il dato dichiara; e non la sua facciata. La facciata c'e' nel file, ma a
questa scala e' piu' grande della zona e ritagliarla lascia un bordo obliquo,
non un edificio. Il disegno e' dunque **schematico**: dice quanti edifici ci
sono, quanto sono alti e dove stanno, non com'e' fatto il tetto. Chi vuole la
facciata la rilegge in `edifici_footprint.json`, che e' il dato e non
l'immagine.

L'ordine di disegno e' dal pin in fuori, cosi' il tetto di uno non mangia la
facciata di un altro. Non e' una prospettiva e non c'e' il cielo: non
pretende di essere un rilievo, e non viene descritto come se lo fosse.

Uso:  python3 sorgenti/art/disegna_ambienti.py                  # l'anno 1
      python3 sorgenti/art/disegna_ambienti.py --anno 3
      python3 sorgenti/art/disegna_ambienti.py --tutte           # 150
      python3 sorgenti/art/disegna_ambienti.py --guarda 1-1      # in caratteri
"""
import json
import math
import os
import struct
import sys
import zlib

RADICE = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))
AMBIENTI = os.path.join(RADICE, "dati", "ambienti_livelli.json")
SAGOME = os.path.join(RADICE, "dati", "edifici_footprint.json")
OUT = os.path.join(RADICE, "sorgenti", "art", "out", "ambienti")

# Quanti pixel copre un metro: il divisore con cui la griglia diventa
# immagine. Dichiarato perche' chi legge sappia rifare la figura a mano.
PXL_PER_M = 4
# L'altezza del volume neutro, in metri. Un edificio di altezza sconosciuta non
# si disegna alto e non si disegna piatto: si disegna con un'altezza dichiarata
# che non pretende di essere quella giusta.
NEUTRO_M = 4.0
# Pixel d'aria sopra l'edificio piu' alto, perche' il tetto si veda.
MARGINE_ALTO_PX = 8

SFONDO, INCHIOSTRO, TERRA, ORO = 0, 1, 2, 3
SEGNI = {SFONDO: ".", INCHIOSTRO: "#", TERRA: "-", ORO: "O"}

# Che cosa si disegna di un edificio, e di che colore. Le chiavi sono i valori
# che `fonte_altezza` puo' avere: se ne nasce una quarta, `disegna` lo dice e
# non indovina.
DA_FONTE = {
    "osm_height": ("altezza misurata in OSM", ORO),
    "osm_levels": ("altezza stimata dai piani, non misurata", TERRA),
    "assente": ("volume neutro: altezza non dichiarata", TERRA),
}


def poligono(forma):
    """La sagoma in metri. Le unita' del file sono i centimeti che dichiara."""
    return [(x / 100.0, y / 100.0) for x, y in forma]


def ritaglia(punti, x0, y0, x1, y1):
    """Sutherland-Hodgman: il poligono dentro al rettangolo, e' lui.

    Serve perche' un edificio largo duecento metri non entra in una zona di
    venti, e non si puo' semplicemente ignorare i pixel fuori: il disegno
    mostrerebbe la facciata intera, spostata, e direbbe che l'edificio e' dove
    non e'. Ritagliando il poligono si vede il pezzo che il giocatore vede
    camminando, che e' l'unica cosa giusta da disegnare.
    """
    def taglia(punti, dentro, interseca):
        if not punti:
            return []
        fuori = []
        prec = punti[-1]
        prec_d = dentro(prec)
        for cur in punti:
            cur_d = dentro(cur)
            if cur_d != prec_d:
                fuori.append(interseca(prec, cur))
            if cur_d:
                fuori.append(cur)
            prec, prec_d = cur, cur_d
        return fuori

    def ix(a, b, i, limite):
        """Il punto in cui il segmento a-b taglia la retta i = limite."""
        if b[i] == a[i]:
            return b
        t = (limite - a[i]) / (b[i] - a[i])
        return (a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1]))

    # I quattro lati, nell'ordine in cui si ritaglia: ogni lato puo' cambiare
    # il poligono di una faccia, quindi si applicano in sequenza. La epsilon
    # tiene il bordo dentro: senza, un vertice sul bordo puo' entrare e uscire
    # due volte e la faccia si sdoppia.
    p = list(punti)
    EPS = 1e-9
    for i, limite, segno in ((0, x0, +1), (0, x1, -1),
                             (1, y0, +1), (1, y1, -1)):
        p = taglia(p,
                   lambda q, i=i, v=limite - segno * EPS: segno * (q[i] - v) >= 0,
                   lambda a, b, i=i, v=limite: ix(a, b, i, v))
    return p


def dentro(x, y, punti):
    """Il punto e' dentro al poligono? Conta i lati attraversati."""
    interno = False
    n = len(punti)
    for i in range(n):
        x1, y1 = punti[i]
        x2, y2 = punti[(i + 1) % n]
        if (y1 > y) != (y2 > y):
            if x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
                interno = not interno
    return interno


def riquadro(tela, x, y, w, h, colore):
    """Un rettangolo pieno, ritagliato alla tela: niente resta fuori."""
    for yy in range(max(0, y), min(len(tela), y + h)):
        riga = tela[yy]
        for xx in range(max(0, x), min(len(riga), x + w)):
            riga[xx] = colore


def scrivi_png(tela, percorso):
    """Il PNG piu' semplice che esista: RGB, tre byte per pixel."""
    righe = b"".join(b"\x00" + bytes(pixel) for pixel in tela)
    grezzo = zlib.compress(righe, 9)

    def blocco(tipo, dati):
        return (struct.pack(">I", len(dati)) + tipo + dati
                + struct.pack(">I", zlib.crc32(tipo + dati) & 0xffffffff))

    con = (b"\x89PNG\r\n\x1a\n"
           + blocco(b"IHDR", struct.pack(">IIBBBBB", len(tela[0]), len(tela),
                                         8, 2, 0, 0, 0))
           + blocco(b"IDAT", grezzo)
           + blocco(b"IEND", b""))
    with open(percorso, "wb") as f:
        f.write(con)
    return len(con)


def disegna(record, sagome):
    """L'immagine di un livello: ritorna (tela, alto_px, statistiche).

    Il record arriva da `ambienti_livelli.json` e la griglia e' sotto la chiave
    `ambiente`, non in testa: leggere `record["griglia"]` e' un KeyError che
    dice solo che il file non ha quella chiave in quel posto.
    """
    ambiente_liv = record["livello"]
    griglia = record["ambiente"]["griglia"]
    miei = [e for e in sagome if e.get("livello") == ambiente_liv]

    # **Il riquadro e' l'inviluppo delle sagome, non un numero scritto.** La
    # griglia dice la zona percorribile, che e' piu' piccola dell'area da cui
    # vengono gli edifici: ritagliare a quella griglia vuol dire buttare via
    # tutto. Si prende l'inviluppo di quello che c'e' e si tiene la griglia
    # come minimo, cosi' un livello senza edifici disegna lo stesso la sua
    # zona. L'inviluppo si prende intero, perche' un riquadro a metri e mezzo
    # non si sa quale sia.
    griglia_m = max(griglia["colonne"] * griglia["scala_m_per_tessera"],
                    griglia["righe"] * griglia["scala_m_per_tessera"])
    semi = griglia_m / 2.0
    for e in miei:
        for x, y in poligono(e["forma"]):
            semi = max(semi, abs(x) + 2.0, abs(y) + 2.0)
    semi = math.ceil(semi)
    larghezza_m = altezza_m = semi * 2.0

    # Dal pin in fuori: il tetto di un edificio non copre la facciata di uno
    # piu' vicino, che e' quello che si vede per primo.
    miei.sort(key=lambda e: -max(abs(x) for x, _ in poligono(e["forma"])))

    piu_alto = max([e["altezza_m"] or NEUTRO_M for e in miei] or [0.0])
    w = int(larghezza_m * PXL_PER_M)
    h = int(altezza_m * PXL_PER_M)
    alto_px = h + int(piu_alto * PXL_PER_M) + MARGINE_ALTO_PX

    # Il pin e' al centro della zona: le coordinate del file sono locali al
    # pin, e la griglia e' la zona che il giocatore attraversa.
    cx, cy = w / 2.0, h / 2.0
    x0, x1 = -larghezza_m / 2.0, larghezza_m / 2.0
    y0, y1 = -altezza_m / 2.0, altezza_m / 2.0
    tela = [[SFONDO] * w for _ in range(alto_px)]

    disegnati, tagliati = 0, 0
    for e in miei:
        grezzi = poligono(e["forma"])
        fonte = e.get("fonte_altezza")
        if fonte not in DA_FONTE:
            raise SystemExit("%s: fonte_altezza sconosciuta %r"
                             % (ambiente_liv, fonte))
        _, colore = DA_FONTE[fonte]
        su = int(round((e["altezza_m"] or NEUTRO_M) * PXL_PER_M))

        # **Il ritaglio e' una scelta, e viene contata.** Un edificio esteso
        # come il chiostro di una cattedrale e' piu' largo della zona
        # percorribile, e in un'immagine di venti metri esce dal bordo. Due
        # strade: allargare l'immagine, che allora non e' piu' la zona che il
        # documento dichiara; oppure ritagliare, e dire quanti edifici sono
        # fuori. Si ritaglia e si conta, perche' un ritaglio non dichiarato
        # e' un'immagine che mente su quanti edifici ha.
        xs = [p[0] for p in grezzi]
        ys = [p[1] for p in grezzi]
        ax0, ax1 = max(x0, min(xs)), min(x1, max(xs))
        ay0, ay1 = max(y0, min(ys)), min(y1, max(ys))
        if ax1 - ax0 <= 0 or ay1 - ay0 <= 0:
            tagliati += 1
            continue
        disegnati += 1
        # l'ingombro ritagliato alla zona, in pixel
        px_a, px_b = int(cx + ax0 * PXL_PER_M), int(cx + ax1 * PXL_PER_M)
        py_alto = int(cy - ay1 * PXL_PER_M) - su
        py_basso = int(cy - ay0 * PXL_PER_M)
        riquadro(tela, px_a, py_alto, px_b - px_a, py_basso - py_alto, colore)
        # il contorno scuro sul tetto: dice dove finisce l'edificio
        if 0 <= py_alto < alto_px:
            for px in range(max(0, px_a), min(w, px_b)):
                tela[py_alto][px] = INCHIOSTRO

    stat = {"edifici": len(miei), "disegnati": disegnati,
            "tagliati": tagliati,
            "riquadro_m": larghezza_m,
            "riquadro_da": "inviluppo delle sagome del livello, minimo la "
                           "griglia; calcolato, non scritto",
            "larghezza_m": larghezza_m, "altezza_m": altezza_m,
            "piu_alto_m": piu_alto,
            "con_altezza": sum(1 for e in miei if e.get("altezza_m"))}
    return tela, alto_px, stat


def in_caratteri(tela, w, h):
    """Il disegno in caratteri, per guardarlo senza un visualizzatore.

    E' lo stesso trucco dei sprite: una riga ogni `passo` pixel, e un carattere
    ogni tanto in larghezza. Un controllo che non guarda e' verde come un
    controllo che guarda, e questo e' il modo di guardare.
    """
    passo = max(1, h // 34)
    col = max(1, w // 78)
    for y in range(0, h, passo):
        print("".join(SEGNI.get(tela[y][x], "?") for x in range(0, w, col)))


def principale():
    anno = None
    if "--anno" in sys.argv:
        anno = int(sys.argv[sys.argv.index("--anno") + 1])
    tutte = "--tutte" in sys.argv
    guarda = (sys.argv[sys.argv.index("--guarda") + 1]
              if "--guarda" in sys.argv else None)

    with open(AMBIENTI, encoding="utf-8") as f:
        ambienti = json.load(f)["ambienti"]
    with open(SAGOME, encoding="utf-8") as f:
        sagome = json.load(f)["edifici"]

    scelti = [a for a in ambienti
              if tutte or guarda == a["livello"]
              or (anno is None and a["livello"].startswith("1-"))
              or (anno is not None and int(a["livello"].split("-")[0]) == anno)]
    os.makedirs(OUT, exist_ok=True)

    disegnati, vuoti, tagliati = [], [], 0
    for a in scelti:
        tela, alto_px, stat = disegna(a, sagome)
        nome = os.path.join(OUT, "ambiente_%s.png" % a["livello"])
        scrivi_png(tela, nome)
        disegnati.append({"livello": a["livello"],
                          "file": os.path.relpath(nome, RADICE),
                          "px": [len(tela[0]), alto_px],
                          "statistiche": stat})
        if stat["edifici"] == 0:
            vuoti.append(a["livello"])
        tagliati += stat["tagliati"]
        if guarda == a["livello"]:
            print("=== %s: %d x %d px, %d edifici, %d con altezza ==="
                  % (a["livello"], len(tela[0]), alto_px, stat["edifici"],
                     stat["con_altezza"]))
            in_caratteri(tela, len(tela[0]), alto_px)

    indice = os.path.join(OUT, "indice.json")
    with open(indice, "w", encoding="utf-8") as f:
        json.dump({"versione": 1, "data": "2026-10-04",
                   "tipo_disegno": "schematico: l'ingombro di ogni edificio "
                                   "ritagliato alla zona, non la facciata",
                   "px_per_m": PXL_PER_M, "neutro_m": NEUTRO_M,
                   "passaggi": len(disegnati),
                   "senza_sagome": vuoti,
                   "edifici_ritagliati": tagliati,
                   "disegnati": disegnati},
                  f, ensure_ascii=False, separators=(",", ":"))

    print("disegnati %d in %s" % (len(disegnati), os.path.relpath(OUT, RADICE)))
    print("  con edifici %d, senza %d%s"
          % (len(disegnati) - len(vuoti), len(vuoti),
             (": " + ", ".join(vuoti)) if vuoti else ""))
    print("  edifici fuori dalla zona, ritagliati: %d" % tagliati)
    print("scritto %s" % os.path.relpath(indice, RADICE))
    return 0


if __name__ == "__main__":
    sys.exit(principale())