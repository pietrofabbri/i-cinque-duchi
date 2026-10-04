"""I sessanta emblemi: forme dichiarate, non tessere anonime.

**Perché questo modulo esiste.** Fino al 3 ottobre 2026 l'emblema era un
rettangolo con una diagonale e il seme era `sum(ord(codice)) % 22`: i
sessanta emblemi erano **diciotto file diversi**, e dieci persone ne
condividevano uno identico. La funzione diceva, nel suo docstring, che «il
seme decide la diagonale, così due emblemi diversi non sembrano lo stesso
file»: era falso, e nessun controllo lo guardava, perché i controlli contavano
i file e non i file *distinti*.

**Che cosa è un emblema, in questo progetto.** `AGENTS.md` §3 vieta i volti
inventati per le persone reali. Un emblema non è un volto: è **la risposta
dichiarata** al fatto che qui il volto non c'è. Il documento sui ritratti lo
chiedeva esplicitamente («ogni emblema deve dire *perché* la persona non ha un
volto qui»), e il perché sta in una frase lunga che nessuno legge a schermo.
Quindi l'emblema porta tre cose, tutte leggibili a 48×54:

1. **il segno della famiglia** — *perché* non c'è il volto, in una forma
   geometrica. Le sette famiglie non sono state scelte a caso e non stanno
   scritte persona per persona: sono **classificate dalla frase del motivo**,
   con una regola dichiarata in `REGOLE` e riportata nel catalogo
   (`emblema_famiglia`, `emblema_famiglia_da`). Una classificazione che
   cambia quando il motivo cambia è una classificazione; scritta a mano sarebbe
   una lista di preferenze travestita da regola.
2. **le iniziali** — chi è. Un emblema senza nome è lo stesso inganno del
   francobollo: dice che c'è qualcosa senza dire chi.
3. **la firma** — cinque caselle che rompono le collisioni. Le iniziali da
   sole non bastano: `Cincinnato` e `i censori` danno entrambe `C`, e
   `Azzo VII d'Este` e `Azzo VIII d'Este` danno entrambe `AZZ`. La firma è
   un hash del nome della voce di catalogo: non significa niente, e serve
   esattamente a rendere i sessanta file distinti.

**Ogni colore viene dalla tavolozza.** Non un esadecimale scritto qui: le
sette chiavi sono lette da `dati/fonti_visive/tavolozza.json`, che è il file
che dichiara da dove viene ogni colore del gioco. Un colore nuovo scritto in
questo modulo sarebbe un colore che nessun documento conosce.

**Nessuna libreria.** Come i fondi di Terrarium (`gis/png_terrarium.py`) e
come gli shapefile (`gis/shapefile_lettore.py`): PNG e forme si scrivono con
`zlib` e qualche riga di `struct`. Il progetto non installa pacchetti per
un rettangolo.
"""
import hashlib
import json
import math
import os
import struct
import unicodedata
import zlib

LATO, ALTEZZA = 48, 54

# Dove stanno le tre parti dentro la tessera, dichiarato perché un numero
# scritto in due posti è un numero che un giorno è diverso.
SEGNO_Y, SEGNO_ALTEZZA = 4, 24
INIZIALI_Y, INIZIALI_ALTEZZA = 31, 7
FIRMA_Y = 45

# Le sette famiglie. `chiave_tavolozza` è il nome della voce in
# `dati/fonti_visive/tavolozza.json`: se la voce non c'è il modulo si ferma,
# perché un colore che non dichiara la sua fonte è un colore inventato.
FAMIGLIE = {
    "vivo": {
        "segno": "anello_interrotto",
        "colore": "azzurro_oltremare",
        "leggibile": "persona viva: il volto non si disegna finché è vivo",
    },
    "collettivo": {
        "segno": "tre_cerchi",
        "colore": "verde_rame",
        "leggibile": "collettivo: più persone, un volto solo non è di nessuno",
    },
    "numero_discorde": {
        "segno": "due_quadrati",
        "colore": "terra_gialla",
        "leggibile": "la numerazione delle fonti non concorda: non si sa quale",
    },
    "identita_conflitto": {
        "segno": "cerchi_sovrapposti",
        "colore": "rosso_minio",
        "leggibile": "due nomi per due persone diverse: l'immagine è dell'altra",
    },
    "opera_non_persona": {
        "segno": "riquadro_opera",
        "colore": "bruno",
        "leggibile": "quello che si è trovato è un'opera o un oggetto, non un volto",
    },
    "nessun_ritratto_libero": {
        "segno": "riquadro_vuoto",
        "colore": "azzurro",
        "leggibile": "nessun ritratto con licenza libera esiste",
    },
    "tradizione": {
        "segno": "volta",
        "colore": "oro",
        "leggibile": "figura della tradizione: nessun ritratto storico lo riprende",
    },
}

# La regola di classificazione, nell'ordine in cui viene applicata. La prima
# famiglia che trova la sua parola vince, e il catalogo dice **quale** parola
# ha fatto vincere: `emblema_famiglia_da` è la prova che la classificazione è
# avvenuta e non è stata indovinata.
REGOLE = [
    ("vivo", ["persona viva"]),
    ("collettivo", ["collettivo", "non ha un volto unico"]),
    ("numero_discorde", ["numerazione discordante", "numerati in modo diverso"]),
    ("identita_conflitto", ["categorie dicono", "gatto"]),
    ("opera_non_persona", [
        "francobollo", "scena", "statua", "tavoletta", "stele", "gioiello",
        "moneta", "stemma", "xilografia", "frontespizio", "ceramica",
        "monumento", "didascalia", "pannello", "inventario", "interno dipinto",
        "convento", "sfilano", "oggetti di culto",
    ]),
    ("nessun_ritratto_libero", [
        "nessun ritratto", "non ha ritratto", "nessun file", "non ha un volto",
        "nessuna immagine",
    ]),
    ("tradizione", ["tradizione"]),
]

# Parole che non portano un nome: dentro una voce di catalogo sono il
# rivestimento grammaticale, non la persona.
MUTE = {"il", "i", "e", "la", "le", "che", "non", "hanno", "del", "della",
        "di", "da", "un", "una", "sono", "stesso"}

# Il font: sette righe di cinque pixel per lettera. Cinque e non tre perché a
# tre `M`, `N` e `H` si leggono uguali, e un emblema con la lettera sbagliata
# è peggio di un emblema senza lettere. La prima versione di questo modulo
# aveva il font 3×5 ed è stata scartata guardando il foglio: `DOM` si leggeva
# `DOH`.
FONT = {
    "A": (".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "B": ("####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."),
    "C": (".###.", "#...#", "#....", "#....", "#....", "#...#", ".###."),
    "D": ("####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."),
    "E": ("#####", "#....", "#....", "####.", "#....", "#....", "#####"),
    "F": ("#####", "#....", "#....", "####.", "#....", "#....", "#...."),
    "G": (".###.", "#...#", "#....", "#.###", "#...#", "#...#", ".###."),
    "H": ("#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "I": ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "#####"),
    "J": ("..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."),
    "K": ("#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"),
    "L": ("#....", "#....", "#....", "#....", "#....", "#....", "#####"),
    "M": ("#...#", "##.##", "#.#.#", "#...#", "#...#", "#...#", "#...#"),
    "N": ("#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#", "#...#"),
    "O": (".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "P": ("####.", "#...#", "#...#", "####.", "#....", "#....", "#...."),
    "Q": (".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"),
    "R": ("####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"),
    "S": (".####", "#....", "#....", ".###.", "....#", "....#", "####."),
    "T": ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."),
    "U": ("#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "V": ("#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."),
    "W": ("#...#", "#...#", "#...#", "#...#", "#.#.#", "##.##", "#...#"),
    "X": ("#...#", "#...#", ".#.#.", "..#..", ".#.#.", "#...#", "#...#"),
    "Y": ("#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."),
    "Z": ("#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"),
    " ": (".....", ".....", ".....", ".....", ".....", ".....", "....."),
}


class FamigliaNonRiconosciuta(ValueError):
    """Il motivo di un emblema non sta in nessuna famiglia dichiarata.

    Non si lascia passare: un emblema senza famiglia sarebbe una forma senza
    significato, cioè esattamente la tessera anonima che questo modulo
    sostituisce.
    """


def classifica(motivo):
    """La famiglia del motivo, e la parola che l'ha fatta vincere."""
    for famiglia, parole in REGOLE:
        for parola in parole:
            if parola in motivo:
                return famiglia, parola
    raise FamigliaNonRiconosciuta(motivo)


def iniziali(nome):
    """Le prime tre lettere del nome, senza accenti e senza le parole mute.

    Tre lettere e non una: una sola non distingue niente, e per un ragazzo di
    tredici anni `AZZ` dice «gli Azzo» molto meglio di `A`.
    """
    n = unicodedata.normalize("NFD", nome)
    n = "".join(c for c in n if unicodedata.category(c) != "Mn")
    parole = [w for w in n.replace('"', " ").replace("-", " ").split()
              if w.lower() not in MUTE]
    lettere = [c.upper() for w in parole for c in w if c.isascii() and c.isalpha()]
    if not lettere:
        raise ValueError("nessuna lettera nel nome %r" % nome)
    return "".join(lettere[:3])


def firma(nome_voce):
    """Cinque bit dall'hash del nome della voce: rompono le iniziali uguali.

    Non significa niente e non è un'etichetta: è la promessa che sessanta
    voci producono sessanta file. Il controllo 7 di `verifica_immagini.py`
    verifica la promessa sui file, non su questa funzione.
    """
    return int(hashlib.sha256(nome_voce.encode("utf-8")).hexdigest(), 16) % 32


def tavolozza(base):
    """I colori letti dal file che li dichiara, e non scritti qui."""
    percorso = os.path.join(base, "dati", "fonti_visive", "tavolozza.json")
    with open(percorso, encoding="utf-8") as f:
        voci = {v["chiave"]: v for v in json.load(f)["voci"]}
    mancanti = sorted({f_["colore"] for f_ in FAMIGLIE.values()} - set(voci))
    if mancanti:
        raise SystemExit("la tavolozza non dichiara %s: un colore che non "
                         "dichiara la sua fonte non si usa" % mancanti)
    return voci


def _hex(s):
    return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


def _cerchio(px, cx, cy, r, spessore=1.6, vuoto=True):
    """L'anello di un cerchio: il cerchio intero del progetto, fatto a mano."""
    for y in range(int(cy - r - 2), int(cy + r + 3)):
        for x in range(int(cx - r - 2), int(cx + r + 3)):
            d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
            if abs(d - r) <= spessore / 2.0 + 0.35:
                px.add((x, y))
            elif not vuoto and d <= spessore:
                px.add((x, y))


def _quadrato(px, x0, y0, x1, y1, spessore=2):
    for x in range(x0, x1 + 1):
        for dy in range(spessore):
            px.add((x, y0 + dy))
            px.add((x, y1 - dy))
    for y in range(y0, y1 + 1):
        for dx in range(spessore):
            px.add((x0 + dx, y))
            px.add((x1 - dx, y))


def segno(nome_segno, x0, y0, lato):
    """I pixel del segno geometrico della famiglia, in un quadrato `lato`.

    Nessuna di queste forme è un volto, e nessuna è un ritratto: sono forme di
    pittura, che è il limite che il progetto ha messo a tutta la grafica. I
    sette segni sono disegnati perché si distinguano **a colpo d'occhio e senza
    leggere**: una cornice vuota e una cornice con una riga dentro sono due
    segni diversi solo se la cornice è abbastanza grossa da distinguerli.
    """
    px = set()
    m = lato / 2.0
    cx, cy = x0 + m, y0 + m
    x1, y1 = x0 + lato, y0 + lato
    r = m - 1.0

    if nome_segno == "anello_interrotto":
        # un anello con una fessura stretta in alto a destra: il volto c'è e
        # non si può disegnare. La fessura è **stretta** apposta: un varco
        # largo toglie metà dell'anello e il segno si legge come una C, che non
        # vuol dire niente.
        for y in range(int(cy - r - 3), int(cy + r + 4)):
            for x in range(int(cx - r - 3), int(cx + r + 4)):
                d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
                if abs(d - r) > 1.2:
                    continue
                angolo = math.degrees(math.atan2(-(y - cy), x - cx))
                if 28.0 <= angolo <= 41.0:      # la fessura: 13 gradi
                    continue
                px.add((x, y))
    elif nome_segno == "tre_cerchi":
        # tre cerchi uguali in triangolo: sono tre persone, non una
        _cerchio(px, cx - m * 0.58, cy - m * 0.42, m * 0.30)
        _cerchio(px, cx + m * 0.58, cy - m * 0.42, m * 0.30)
        _cerchio(px, cx, cy + m * 0.58, m * 0.30)
    elif nome_segno == "due_quadrati":
        # due cornici spostate: due numerazioni che non coincidono
        _quadrato(px, int(x0 + 1), int(y0 + 1), int(x0 + m + 3), int(y0 + m + 3))
        _quadrato(px, int(x0 + m - 3), int(y0 + m - 3), int(x1 - 1), int(y1 - 1))
    elif nome_segno == "cerchi_sovrapposti":
        # due anelli che si incrociano: due persone diverse per un nome solo
        _cerchio(px, cx - m * 0.35, cy, m * 0.62)
        _cerchio(px, cx + m * 0.35, cy, m * 0.62)
    elif nome_segno == "riquadro_opera":
        # una cornice con due righe dentro: un'opera stampata, non un volto
        _quadrato(px, int(x0 + 1), int(y0 + 1), int(x1 - 1), int(y1 - 1))
        for y in (int(cy - m * 0.28), int(cy + m * 0.28)):
            for x in range(int(x0 + 4), int(x1 - 3)):
                px.add((x, y))
    elif nome_segno == "riquadro_vuoto":
        # una cornice e nient'altro: qui il ritratto non c'è
        _quadrato(px, int(x0 + 1), int(y0 + 1), int(x1 - 1), int(y1 - 1))
    elif nome_segno == "volta":
        # una nicchia: due colonne, un arco e il piano. Si disegna come si
        # misura — colonna, arco, soglia — e non riempiendola: la prima
        # versione riempiva l'arco e diventava una macchia che non somigliava
        # a niente.
        base = int(y0 + lato - 2)
        spalla = int(base - r * 0.55)          # dove la colonna incontra l'arco
        piedi = (int(round(cx - r)), int(round(cx + r)))
        for x in range(piedi[0], piedi[1] + 1):
            px.add((x, base))                  # il piano
        for x in piedi:
            for y in range(spalla, base + 1):   # le due colonne
                px.add((x, y))
        # l'arco sta **sopra** la spalla e si traccia per **angolo**, non per
        # soglia su un numero reale: la soglia produceva un arco con un
        # fianco di tre pixel e l'altro di uno, cioè una nicchia storta.
        for grado in range(0, 181, 2):
            ang = math.radians(grado)
            px.add((int(round(cx + r * math.cos(ang))),
                    int(round(spalla - r * math.sin(ang)))))
    else:
        raise ValueError("nessun segno dichiarato si chiama %r" % nome_segno)
    return px


def tessera(voce_catalogo, base):
    """La PNG 48×54 dell'emblema di una voce, con la famiglia del disegno.

    La funzione **ritorna anche la famiglia e la parola che l'ha fatta
    vincere**: il generatore non deve scrivere nel catalogo una famiglia che non
    è quella del disegno, e l'unico modo per non sbagliare è farla calcolare
    una volta sola.
    """
    motivo = voce_catalogo["motivo"]
    famiglia, parola = classifica(motivo)
    tav = tavolozza(base)
    inchiostro = _hex(tav["inchiostro"]["hex"])
    fondo = _hex(tav["bianco_calce"]["hex"])
    colore = _hex(tav[FAMIGLIE[famiglia]["colore"]]["hex"])

    righe = [[fondo] * LATO for _ in range(ALTEZZA)]

    # il bordo, in inchiostro: dice al ragazzo che il riquadro è vuoto di volto
    for x in range(LATO):
        righe[0][x] = righe[ALTEZZA - 1][x] = inchiostro
    for y in range(ALTEZZA):
        righe[y][0] = righe[y][LATO - 1] = inchiostro

    def metti(x, y, colore_pixel):
        if 2 <= x < LATO - 2 and 2 <= y < ALTEZZA - 2:
            righe[y][x] = colore_pixel

    # 1. il segno della famiglia, in alto al centro
    x0 = (LATO - SEGNO_ALTEZZA) // 2
    for x, y in segno(FAMIGLIE[famiglia]["segno"], x0, SEGNO_Y, SEGNO_ALTEZZA):
        metti(x, y, colore)

    # 2. le iniziali, al centro, alla misura del font
    lettere = iniziali(voce_catalogo["nome"])
    passo = 6            # cinque pixel di lettera più uno di distanza
    x0 = (LATO - (len(lettere) * passo - 1)) // 2
    for i, lettera in enumerate(lettere):
        for riga, punti in enumerate(FONT[lettera]):
            for c, pieno in enumerate(punti):
                if pieno == "#":
                    metti(x0 + i * passo + c, INIZIALI_Y + riga, inchiostro)

    # 3. la firma: cinque caselle, le piene secondo i bit del nome della voce
    bit = firma(voce_catalogo["nome"])
    larghezza = 5 * 4 + 4
    x0 = (LATO - larghezza) // 2
    for i in range(5):
        pieno = (bit >> i) & 1
        for dx in range(4):
            for dy in range(3):
                metti(x0 + i * 5 + dx, FIRMA_Y + dy,
                      colore if pieno else fondo)

    def lotto(tipo, dati):
        return (struct.pack(">I", len(dati)) + tipo + dati
                + struct.pack(">I", zlib.crc32(tipo + dati) & 0xFFFFFFFF))

    grezzo = b"".join(b"\x00" + bytes(v for px in r for v in px) for r in righe)
    png = (b"\x89PNG\r\n\x1a\n"
           + lotto(b"IHDR", struct.pack(">IIBBBBB", LATO, ALTEZZA, 8, 2, 0, 0, 0))
           + lotto(b"IDAT", zlib.compress(grezzo, 9))
           + lotto(b"IEND", b""))
    return png, famiglia, parola