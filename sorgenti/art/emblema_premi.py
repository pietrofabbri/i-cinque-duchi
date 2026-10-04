"""Gli emblemi dei premi: una tessera per livello, dalla categoria dichiarata.

**Che cosa è e che cosa non è questo disegno.** `premi.md` §4 ha deciso che
ogni livello ha un premio, e sono 1050. L'**oggetto** del premio non esiste
ancora: la prova 5 vieta che sia generato, e i campi `premio`, `fonte`,
`licenza` sono `null` con il perché accanto in `dati/premi.json`. Quindi qui
**non si disegna il premio**: si disegna il **simbolo del premio**, cioè la
categoria — `A` figure, `B` pittura, `C` scultura, `D` architettura e così via
fino a `K`. La categoria è **riletta dalla tabella di `premi.md` §2** e non
scelta qui, perché un simbolo che non dice perché quella forma e non dice a chi
appiene è un francobollo.

**Le forme sono dichiarate, una per categoria.** Non un segno generato da un
seme: un seme produce la stessa figura per due categorie diverse quando i nomi
accadono di dare lo stesso numero, ed è il difetto che ha reso i sessanta
emblemi delle persone diciotto file. Qui la forma viene dalla **categoria**,
che è un dato, e la **firma** in basso — cinque caselle, come in `emblema.py` —
rompe le collisioni fra i centocinquanta premi della stessa categoria. Le undici
forme stanno in `emblema.segno()`, accanto ai sette segni delle famiglie e non
al posto loro: quelle dicono *perché qui non c'è il volto*, queste dicono *che
cosa è l'oggetto*, e un dipinto e una legge non possono avere la stessa forma.

**Un foglio solo, e perché.** Centocinquanta tessere in millettocinquanta file
sono millettocinquanta richieste solo per pubblicarle, e il rate limit di
GitHub non le fa passare. Il foglio ne è uno: `premi_foglio.png`, con l'indice
che dice **dove sta ogni tessera** (`x`, `y`), così il motore estrae il pezzo
che gli serve senza che il file sia monolitico. È una scelta dichiarata, non un
risparmio nascosto.

Uso:  python3 sorgenti/art/emblema_premi.py
      python3 sorgenti/art/emblema_premi.py --guarda 1-3-LA    # in caratteri
"""
import json
import os
import re
import sys

RADICE = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import emblema                                              # noqa: E402

PREMI = os.path.join(RADICE, "dati", "premi.json")
TAVOLA = os.path.join(RADICE, "dati", "fonti_visive", "tavolozza.json")
DOC_PREMI = os.path.join(RADICE, "docs", "videogioco-5-duchi-premi.md")
OUT = os.path.join(RADICE, "sorgenti", "art", "out", "premi")
FOGLIO = os.path.join(OUT, "premi_foglio.png")
INDICE = os.path.join(OUT, "premi_indice.json")
FORME_PAGINA = os.path.join(OUT, "forme_prova.png")
FORME_INDICE = os.path.join(OUT, "forme_indice.json")


# La sigla di ogni lingua. **Tre lettere non bastavano**: `IT` e `INFO`
# cominciano per I, `LA` e `LIS` per L, `EN` ed `EL` per E, e due tessere con
# la stessa sigla e lo stesso numero sarebbero lo stesso disegno. La sigla e'
# dichiarata qui e verificata unica dal generatore, che si ferma se due
# lingue ne prendono la stessa.
SIGLE = {"INFO": "IN", "IT": "IT", "FE": "FE", "LA": "LA",
         "EN": "EN", "LIS": "SG", "EL": "EL"}

LATO = emblema.LATO                    # 48
ALTEZZA = emblema.ALTEZZA               # 54
COLONNE = 30                           # trenta tessere per riga
MARGINE = 2                            # pixel fra una tessera e l'altra
# Il foglio delle forme e' **alla scala reale**, non piu' grande. La prima
# versione le disegnava a tre volte per vederle meglio, ed era la cosa
# sbagliata da guardare: `emblema.segno()` e' scritto per una tessera di 24
# pixel e molte sue formule usano scarti assoluti, quindi a scala tre il
# frontone diventava una macchia e il riquadro un pieno. Un foglio di prova
# che non e' come il file vero e' un foglio di prova di un'altra cosa, e il
# difetto che doveva far vedere lo nascondeva invece.
FORMA_LATO = LATO
FORMA_ALTEZZA = ALTEZZA

# La forma di ogni categoria e **perché sta con quella categoria**. La forma
# e' il segno in `emblema.segno()`; il perché sta nell'indice e nel documento,
# perché `AGENTS.md` vieta un colore o un segno che viva in un posto solo.
FORME = {
    "A": ("volto_riquadrato", "una persona: il riquadro dove un volto "
         "starebbe, ma non un volto"),
    "B": ("pennello_e_tela", "un dipinto: la tela e il pennello"),
    "C": ("figura_su_piedistallo", "una statua: la figura sul suo basamento"),
    "D": ("edificio_a_frontone", "un edificio: il frontone e le due colonne"),
    "E": ("foglio_stampato", "una pagina: il foglio con le righe e il piega"),
    "F": ("lastra_iscritta", "una lastra: il cippo con l'iscrizione"),
    "G": ("chiave_e_onda", "una musica: la chiave e le due onde"),
    "H": ("sipario", "un teatro: il sipario raccolto e i due riflettori"),
    "I": ("pagina_con_suggello", "una legge: la pagina col sigillo"),
    "J": ("scudo", "uno stemma: lo scudo, che ha un bordo e un fondo"),
    "K": ("quaderno_del_giocatore", "la scheda del giocatore: il quaderno "
         "aperto, una pagina scritta e una vuota"),
}


def foglio_forme(tav):
    """Un foglio con **tutte** le forme dichiarate, grandi tre volte.

    Sei delle undici categorie non hanno nessun livello e quindi nessuna
    tessera nel foglio dei premi: le loro forme sono state scritte e non
    sono mai state **guardate**. Un controllo che verifica che una forma
    produca pixel verifica che produca qualcosa, non che produca una
    figura riconoscibile — e una figura non riconoscibile è un difetto che
    resta invisibile finché nessuno la guarda. Questo foglio esiste per
    poterla guardare, e per guardarle tutte e undici insieme, che è il
    modo in cui si vedono anche le due che somigliano.
    """
    categorie = sorted(FORME)
    colonne = 6
    righe = (len(categorie) + colonne - 1) // colonne
    passo_x = FORMA_LATO + MARGINE * 3
    passo_y = FORMA_ALTEZZA + MARGINE * 4
    fondo = emblema._hex(tav["bianco_calce"]["hex"])
    larghezza = colonne * passo_x + MARGINE
    altezza = righe * passo_y + MARGINE
    tela = [[fondo] * larghezza for _ in range(altezza)]
    inchiostro = emblema._hex(tav["inchiostro"]["hex"])[:3]
    colore = emblema._hex(
        tav[emblema.FAMIGLIE["opera_non_persona"]["colore"]]["hex"])[:3]

    voci = []
    for i, categoria in enumerate(categorie):
        segno, perche = FORME[categoria]
        cx = MARGINE + (i % colonne) * passo_x
        cy = MARGINE + (i // colonne) * passo_y
        # `emblema.segno` e' pensata per una tessera piccola e restituisce
        # coordinate intere, ma a tre volte il foglio le arrotla e restano
        # dei float: `tela[y][x]` con un float e' un TypeError. La conversione
        # e' qui e non dentro `segno`, perche' li' gli indici sono gia' interi
        # per costruzione e la conversione sarebbe silenziosa.
        for x, y in emblema.segno(segno, cx + (FORMA_LATO - 24) // 2,
                                  cy + emblema.SEGNO_Y, emblema.SEGNO_ALTEZZA):
            xi, yi = int(round(x)), int(round(y))
            if 0 <= xi < larghezza and 0 <= yi < altezza:
                tela[yi][xi] = colore
        # la lettera della categoria in basso, con il font di sempre
        x0 = cx + (FORMA_LATO - 5) // 2
        for righe_lettera, punti in enumerate(
                emblema.FONT.get(categoria, [])):
            for c, pieno in enumerate(punti):
                if pieno == "#" and 0 <= cy + FORMA_ALTEZZA + 4 + righe_lettera \
                        < altezza and 0 <= x0 + c < larghezza:
                    tela[cy + FORMA_ALTEZZA + 4 + righe_lettera][x0 + c] = \
                        inchiostro
        voci.append({"categoria": categoria, "segno": segno, "perche": perche,
                     "x": cx, "y": cy, "px": [FORMA_LATO, FORMA_ALTEZZA],
                     "scala": 1})
    return tela, larghezza, altezza, voci, colonne


def categorie_del_documento():
    """Le lettere chiuse da `premi.md` §1, lette dal documento."""
    testo = open(DOC_PREMI, encoding="utf-8").read()
    return set(re.findall(r"^\| \*\*([A-Z])\*\* \| ", testo, re.M))


def tessera_premio(record, tav):
    """I pixel di un emblema di premio, e la categoria che l'ha disegnato.

    La struttura è quella di `emblema.tessera`: bordo in inchiostro, segno
    della categoria in alto, il **numero della tappa** al centro e la firma in
    basso. Il numero, e non le iniziali della lingua: `1-3-LA` non ha
    iniziali sensate, e scrivere `L` e `A` direbbe che il premio è di una
    categoria `L` che non esiste. Quello che il giocatore vede sulla mappa è
    il numero della tappa.
    """
    categoria = record["categoria"]
    if categoria not in FORME:
        raise SystemExit("categoria %s senza forma dichiarata" % categoria)
    segno, perche = FORME[categoria]

    inchiostro = emblema._hex(tav["inchiostro"]["hex"])
    fondo = emblema._hex(tav["bianco_calce"]["hex"])
    colore = emblema._hex(tav[emblema.FAMIGLIE["opera_non_persona"]["colore"]]
                          ["hex"])

    righe = [[fondo] * LATO for _ in range(ALTEZZA)]
    for x in range(LATO):
        righe[0][x] = righe[ALTEZZA - 1][x] = inchiostro
    for y in range(ALTEZZA):
        righe[y][0] = righe[y][LATO - 1] = inchiostro

    def metti(x, y, c):
        if 2 <= x < LATO - 2 and 2 <= y < ALTEZZA - 2:
            righe[y][x] = c

    x0 = (LATO - emblema.SEGNO_ALTEZZA) // 2
    for x, y in emblema.segno(segno, x0, emblema.SEGNO_Y,
                              emblema.SEGNO_ALTEZZA):
        metti(x, y, colore)

    # **Numero della tappa e sigla della lingua**: i due caratteri che
    # dicono *quale* livello. Le iniziali del nome del premio non ci sono
    # ancora — l'oggetto non e' deciso, e `dati/premi.json` lo dichiara.
    # **Anno, tappa con due cifre, sigla.** Il numero della tappa da solo non
    # basta: `1-2` e `2-2` hanno entrambi il numero 2 e producevano la stessa
    # tessera — il secondo giro di Q3. Con l'anno davanti e la tappa
    # sempre su due cifre, `1-2` dice «102SG» e `2-2` dice «202SG»: cinque
    # caratteri, che a 48 pixel ci stono e non si toccano fra loro.
    anno, numero = record["livello"].split("-")
    lettere = anno + numero.zfill(2) + SIGLE[record["lingua"]]
    passo = 6
    x0 = (LATO - (len(lettere) * passo - 1)) // 2
    if x0 < 2:
        raise SystemExit("la sigla %s non ci sta in %d px"
                         % (lettere, LATO))
    for i, lettera in enumerate(lettere):
        for riga, punti in enumerate(emblema.FONT.get(lettera, [])):
            for c, pieno in enumerate(punti):
                if pieno == "#":
                    metti(x0 + i * passo + c, emblema.INIZIALI_Y + riga,
                          inchiostro)

    bit = emblema.firma(record["chiave"])
    x0 = (LATO - (5 * 4 + 4)) // 2
    for i in range(5):
        pieno = (bit >> i) & 1
        for dx in range(4):
            for dy in range(3):
                metti(x0 + i * 5 + dx, emblema.FIRMA_Y + dy,
                      colore if pieno else fondo)
    return righe, categoria, perche


def scrivi_png(tela, percorso):
    """PNG RGB, tre byte per pixel. I pixel sono gia' triplette: qui non si
    deve trasformare niente, e una versione precedente scriveva l'indice del
    colore al posto del canale."""
    import struct
    import zlib

    def lotto(tipo, dati):
        return (struct.pack(">I", len(dati)) + tipo + dati
                + struct.pack(">I", zlib.crc32(tipo + dati) & 0xFFFFFFFF))

    grezzo = b"".join(b"\x00" + bytes(v for px in r for v in px)
                      for r in tela)
    png = (b"\x89PNG\r\n\x1a\n"
           + lotto(b"IHDR", struct.pack(">IIBBBBB", len(tela[0]), len(tela),
                                         8, 2, 0, 0, 0))
           + lotto(b"IDAT", zlib.compress(grezzo, 9))
           + lotto(b"IEND", b""))
    with open(percorso, "wb") as f:
        f.write(png)
    return len(png)


def in_caratteri(tela, tessera, tav):
    """La tessera in caratteri, per guardarla senza un visualizzatore."""
    inchiostro = emblema._hex(tav["inchiostro"]["hex"])[:3]
    fondo = emblema._hex(tav["bianco_calce"]["hex"])[:3]
    x0, y0 = tessera["x"], tessera["y"]
    for y in range(y0, y0 + tessera["px"][1]):
        riga = ""
        for x in range(x0, x0 + tessera["px"][0]):
            p = tela[y][x][:3]
            # l'inchiostro e' un '#' e non uno spazio: con lo spazio il
            # bordo della tessera spariva e la forma sembrava galleggiare.
            riga += "#" if p == inchiostro else ("." if p == fondo else "o")
        print(riga)


def principale():
    guarda = (sys.argv[sys.argv.index("--guarda") + 1]
              if "--guarda" in sys.argv else None)
    with open(PREMI, encoding="utf-8") as f:
        cat = json.load(f)
    premiate = cat["premi"]
    tav = emblema.tavolozza(RADICE)
    dichiarate = categorie_del_documento()

    if len(set(SIGLE.values())) != len(SIGLE):
        doppie = sorted({v for v in SIGLE.values()
                         if list(SIGLE.values()).count(v) > 1})
        raise SystemExit("due lingue prendono la stessa sigla: %s"
                         % ", ".join(doppie))
    sconosciute = sorted({p["lingua"] for p in premiate} - set(SIGLE))
    if sconosciute:
        raise SystemExit("lingue senza sigla dichiarata: %s"
                         % ", ".join(sconosciute))

    usate = {p["categoria"] for p in premiate}
    senza = sorted(usate - set(FORME))
    if senza:
        raise SystemExit("categorie usate senza forma dichiarata: %s"
                         % ", ".join(senza))
    nuove = sorted(set(FORME) - dichiarate)
    if nuove:
        raise SystemExit("forme dichiarate per categorie che il documento non "
                         "chiude: %s" % ", ".join(nuove))

    righe_foglio = (len(premiate) + COLONNE - 1) // COLONNE
    larghezza = COLONNE * (LATO + MARGINE) + MARGINE
    altezza = righe_foglio * (ALTEZZA + MARGINE) + MARGINE
    fondo = emblema._hex(tav["bianco_calce"]["hex"])
    tela = [[fondo] * larghezza for _ in range(altezza)]

    indice, per_categoria = [], {}
    for i, p in enumerate(premiate):
        righe, categoria, perche = tessera_premio(p, tav)
        cx = MARGINE + (i % COLONNE) * (LATO + MARGINE)
        cy = MARGINE + (i // COLONNE) * (ALTEZZA + MARGINE)
        for y, riga in enumerate(righe):
            for x, px in enumerate(riga):
                tela[cy + y][cx + x] = px
        indice.append({"chiave": p["chiave"], "livello": p["livello"],
                       "lingua": p["lingua"], "categoria": categoria,
                       "forma": FORME[categoria][0], "forma_perche": perche,
                       "x": cx, "y": cy, "px": [LATO, ALTEZZA]})
        per_categoria[categoria] = per_categoria.get(categoria, 0) + 1

    os.makedirs(OUT, exist_ok=True)
    byte = scrivi_png(tela, FOGLIO)

    tela_f, larghezza_f, altezza_f, voci_forme, colonne_f = foglio_forme(tav)
    byte_f = scrivi_png(tela_f, FORME_PAGINA)
    with open(FORME_INDICE, "w", encoding="utf-8") as f:
        json.dump({"versione": 1, "data": "2026-10-04",
                   "foglio": os.path.relpath(FORME_PAGINA, RADICE),
                   "foglio_px": [larghezza_f, altezza_f],
                   "colonne": colonne_f, "scala": 1,
                   "scala_perche": "alla scala reale della tessera: "
                                   "emblema.segno e' scritto per 24 pixel e "
                                   "a scala maggiore le formule sbagliano",
                   "che_cosa_e": "tutte le undici forme dichiarate, grandi "
                                 "tre volte, per poterle guardare: sei di "
                                 "queste non hanno nessun livello e quindi "
                                 "nessuna tessera nel foglio dei premi",
                   "forme": voci_forme}, f,
                  ensure_ascii=False, separators=(",", ":"))

    with open(INDICE, "w", encoding="utf-8") as f:
        json.dump({"versione": 1, "data": "2026-10-04",
                   "foglio": os.path.relpath(FOGLIO, RADICE),
                   "foglio_px": [larghezza, altezza],
                   "tessera_px": [LATO, ALTEZZA],
                   "colonne": COLONNE, "margine": MARGINE,
                   "che_cosa_e": "il simbolo della **categoria** del premio, "
                                 "non l'oggetto: l'oggetto non esiste ancora e "
                                 "la prova 5 vieta che sia generato "
                                 "(dati/premi.json, campo vuoto)",
                   "come": "segno della categoria in alto, numero della tappa "
                           "al centro, firma di cinque caselle in basso. "
                           "Come in emblema.py, e per la stessa ragione",
                   "foglio_unico_perche": "1050 file da 48x54 sono 1050 "
                                          "richieste solo per pubblicarli, e "
                                          "il rate limit di GitHub non le fa "
                                          "passare: l'indice dice dove sta "
                                          "ogni tessera",
                   "forme": {k: {"segno": v[0], "perche": v[1]}
                             for k, v in FORME.items()},
                   "categorie_usate": dict(sorted(per_categoria.items())),
                   "premi": len(premiate),
                   "tessere": indice}, f,
                  ensure_ascii=False, separators=(",", ":"))

    print("emblemi dei premi: %d in un foglio %dx%d (%d byte)"
          % (len(premiate), larghezza, altezza, byte))
    print("  per categoria: %s" % dict(sorted(per_categoria.items())))
    print("  categorie chiuse dal documento: %d, forme dichiarate: %d"
          % (len(dichiarate), len(FORME)))
    print("scritti %s e %s"
          % (os.path.relpath(FOGLIO, RADICE), os.path.relpath(INDICE, RADICE)))
    print("  foglio delle %d forme: %dx%d (%d byte), in %s"
          % (len(FORME), larghezza_f, altezza_f, byte_f,
             os.path.relpath(FORME_PAGINA, RADICE)))

    if guarda is not None:
        trovato = [t for t in indice if t["chiave"] == guarda]
        if not trovato:
            raise SystemExit("nessun premio con la chiave %s" % guarda)
        print("=== %s, categoria %s (%s) ==="
              % (guarda, trovato[0]["categoria"], trovato[0]["forma"]))
        in_caratteri(tela, trovato[0], tav)
    return 0


if __name__ == "__main__":
    sys.exit(principale())