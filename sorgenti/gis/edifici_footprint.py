"""Estrae da OpenStreetMap le sagome degli edifici attorno ai luoghi del gioco.

E' il buco piu' grande dei cinque che `fonti-visive.md` 3.2 dichiara: la fonte
(OSM, ODbL) era autorizzata e il file non esisteva. Questo e' quel file.

**Il problema che questo file deve risolvere bene e' l'altezza, non la forma.**
La forma si scarica: il poligono della facciata e' li'. L'altezza no, e OSM la
dichiara raramente. Nella prova sulla piazza della Cattedrale, su 201 edifici
36 hanno `height` e 7 hanno `building:levels`: circa un quinto. Su gli altri
quattro quinti **non si sa quanto sono alti**, e la regola del progetto e' gia'
scritta in `fonti-visive.md` 4.3: «una forma che non e' verificata non si
disegna». Qui la traduzione e' che un edificio senza altezza esce con
`altezza: null` e `fonte_altezza: "assente"`, e il motore ne fa un volume
neutro — non un cubo alto a caso, che sarebbe un'edificio inventato.

Le tre fonti di altezza, in quest'ordine di affidabilita', e ognuna dichiarata:

  osm_height    il tag `height`, in metri: e' la misura, quando c'e'
  osm_levels    `building:levels` moltiplicato per `M_PER_PIANO`, che e' una
                **costante dichiarata** di questo file (3,2 m) e non un fatto:
                un piano di un palazzo di mattoni e' piu' alto di un piano di
                legno, e il file non lo sa. Per questo `fonte_altezza` dice
                `osm_levels` e non `osm_height`: chi legge sa che quel numero
                e' una stima dichiarata
  assente       niente: `altezza: null`, e il motore disegna un volume neutro

**Cosa si tiene e cosa si scarta.** Un intorno di 250 m attorno al pin restituisce
centinaia di edifici, quasi tutti anonimi. Il file ne tiene i **significativi**,
con una regola dichiarata: ha un nome, ha un `wikidata`, ha un'altezza o dei
piani, e' un edificio di una categoria che il gioco sa riconoscere (chiese,
castelli, palazzi, torri), oppure ha un'area maggiore di `AREA_MINIMA`. Il resto
e' volume neutro anonimo e non serve a niente: il file scrive **quanti ne ha
scartati e perche'**, perche' una soglia non dichiarata e' un difetto che nessuno
vede.

La geometria si semplifica con `dp_chiuso` di `mappe_formato.py`, che gia' sa
chiudere gli anelli senza spostarli, e si scrive nel formato delta dello stesso
file: il motore ha gia' un lettore per quel formato e non ne serve un secondo.

La licenza non e' una formalita': OSM e' ODbL, quindi il file porta
`licenza` e `attribuzione` in testa, e `FONTI-E-LICENZE.md` li deve citare.

**La fonte non e' piu' Overpass.** Le tre istanze rispondevano 504, e un'estrazione
di duecento aree non finiva. Ora si interroga l'API standard OSM (`api/0.6/map?bbox=`)
attraverso `scarica_osm.py`, che restituisce lo **stesso formato** di Overpass
perche' a valle non cambiasse niente. Il prezzo dichiarato e' una richiesta per
pin invece di una per gruppo: ogni risposta e' completa o assente, e il file dice
quale, mentre prima una richiesta si spezzava a meta' senza che nessuno lo sapesse.

Uso:  python3 sorgenti/gis/edifici_footprint.py
      python3 sorgenti/gis/edifici_footprint.py --prova          # non scrive
      python3 sorgenti/gis/edifici_footprint.py --luogo Ferrara  # un posto solo
      python3 sorgenti/gis/edifici_footprint.py --livelli       # anche i 150 pin
      python3 sorgenti/gis/edifici_footprint.py --riprendi       # salta i fatti
"""
import json
import math
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mappe_formato import dp_chiuso                               # noqa: E402
import scarica_osm                                                # noqa: E402

RADICE = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))
LUOGHI = os.path.join(RADICE, "dati", "luoghi_gioco.json")
AMBIENTI = os.path.join(RADICE, "dati", "ambienti_livelli.json")
USCITA = os.path.join(RADICE, "dati", "edifici_footprint.json")

UA = "i-cinque-duchi/0.1 (progetto didattico per liceo; pietrofabbri)"
LICENZA = "ODbL 1.0"
ATTRIBUZIONE = "(c) OpenStreetMap contributors"

RAGGIO_M = 250.0        # quanto intorno al pin si guarda
M_PER_PIANO = 3.2       # costante dichiarata, non un fatto storico
AREA_MINIMA = 120.0     # m^2: sotto, e' un edificio accessorio
# Un ingombro sotto il metro quadro non e' una forma, e' un punto: la
# soglia e' separata da AREA_MINIMA perche' la prima guarda il metro
# cubo disegnato e la seconda la grandezza dell'edificio.
INGOMBRO_MINIMO_M = 1.0
TOLLERANZA = 1.5        # m: semplificazione della facciata
MAX_PER_LUOGO = 140     # oltre, il posto si riempie di cubi anonimi
# Quanti edifici si tengono per area interrogata, e perche' sono due numeri e
# non uno. Un **luogo** del registro e' una citta': il motore ci disegna sopra e
# gli edifici lontani dal centro servono. Un **livello** e' una zona percorribile
# di ottanta metri per sessanta al massimo, e tenerne trecento vuol dire portare
# in giro cose che nessuno vedra': i piu' vicini al centro della zona, e il resto
# dichiarato come scarto. Sono scelte di progetto, non regole di una fonte.
TETTO_LUOGO = 140
TETTO_LIVELLO = 40
# Margine oltre la diagonale della griglia, per non tagliare un edificio che
# entra dalla parte opposta del bordo.
MARGINE_M = 20
# Pausa fra due aree: l'API OSM chiede di non martellarla. Un secondo basta,
# e il file lo dichiara invece di farlo di nascosto.
PAUSA_S = 1.0

# Il raggio di un livello e' **calcolato dalla sua griglia**, non scritto: la
# diagonale della zona piu' un margine. Con le nove griglie dichiarate in
# `ambienti_livelli.py` il raggio va da 51 metri (una porta) a 121 metri (un
# paesaggio), e chiederne 250 per tutte voleva dire tre quarti degli edifici
# fuori dalla zona: dati veri che il motore non puo' mostrare, che e' la stessa
# cosa di nessun dato, solo piu' pesante.
GRIGLIE = {
    "piazza": (22, 14, 1.25), "citta": (30, 22, 1.5),
    "edificio": (16, 12, 1.25), "porta": (18, 14, 1.25),
    "percorso": (34, 10, 1.5), "area": (34, 26, 2.0),
    "citta_antica": (30, 22, 1.5), "situazione": (24, 18, 1.5),
    "paesaggio": (40, 30, 2.0),
}


def raggio_del_livello(ambiente):
    """Il raggio in metri della zona percorribile, dalla diagonale della griglia."""
    tipo = (ambiente.get("ambiente") or {}).get("tipo", "paesaggio")
    colonne, righe, scala = GRIGLIE.get(tipo, GRIGLIE["paesaggio"])
    return int(math.hypot(colonne * scala, righe * scala) + MARGINE_M)
# Quanti centimetri vale un metro nel file: 100. La forma si scrive in
# centimetri interi, come `mappe_formato.scrivi` fa con `int(round(x * q))`.
# **Qui era il difetto.** La prima versione scriveva `round(x / Q)` invece di
# `round(x * Q)`: divideva per cento un numero che era gia' in metri, quindi
# ogni vertice finiva a zero e tutte le 5209 sagome del file erano un punto.
# Il conteggio era vero e la geometria distrutta, e nessuno lo vedeva perche'
# non c'era un controllo che guardasse: e' quello che `verifica_sagome.py` fa
# adesso, controllando che l'ingombro della forma torni con `area_m2`.
Q = 100.0


def metri(lat0, lon0, pts):
    """Dall'equidistanza al piano, in metri, con l'origine nel pin.

    Il piano e' tangente alla sfera: a Ferrara la differenza e' di qualche
    centesimo di millimetro, ma il file lo dichiara perche' il motore usa le
    stesse coordinate per i fondi e le due cose devono combaciare.
    """
    mlat = 111132.92 - 559.82 * math.cos(2 * math.radians(lat0)) \
        + 1.175 * math.cos(4 * math.radians(lat0))
    mlon = 111412.84 * math.cos(math.radians(lat0)) \
        - 93.5 * math.cos(3 * math.radians(lat0))
    return [(round((lon - lon0) * mlon, 2), round((lat - lat0) * mlat, 2))
            for lon, lat in pts]


def area(pts):
    a = 0.0
    for i in range(len(pts)):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % len(pts)]
        a += x1 * y2 - x2 * y1
    return abs(a) / 2.0


def ingombro_cm(f):
    """L'area in metri quadri racchiusa dalla forma scritta in centimetri."""
    return area([(x / Q, y / Q) for x, y in f])


def tolleranza_per(mp):
    """La tolleranza di semplificazione di un anello, dalla sua dimensione.

    TOLLERANZA va bene per un palazzo e cancella una stalla: la banda dentro
    cui si scarta un vertice e' piu' larga dell'edificio, quindi la sagoma
    finisce per dire un quarto dell'area reale. Qui la tolleranza non scende
    sotto un ventesimo della dimensione maggiore, e non sale sopra il
    dichiarato. Il rapporto e' una soglia di progetto, non una legge.
    """
    dx = max(p[0] for p in mp) - min(p[0] for p in mp)
    dy = max(p[1] for p in mp) - min(p[1] for p in mp)
    return max(min(TOLLERANZA, max(dx, dy) / 20.0), 0.01)


def forma(sempl, area_dichiarata):
    """La facciata semplificata in centimetri interi, e se si e' persa.

    Restituisce `(forma, perdita)`. La perdita e' `True` quando l'ingombro
    della forma non sta nella stessa scala dell'area che il record dichiara:
    allora la sagoma non descrive piu' l'edificio e va scartata, non scritta.
    Il confronto e' contro `area_dichiarata`, non contro l'area della figura
    semplificata: se si facesse il contrario, il controllo misurerebbe la
    perdita della quantizzazione contro la perdita della semplificazione, e le
    due si coprirebbero a vicenda.
    Il fattore due per lato e' la banda dichiarata entro cui la
    semplificazione sposta i vertici senza cambiare figura.
    """
    f = [[int(round(x * Q)), int(round(y * Q))] for x, y in sempl]
    banda = (0.5 * area_dichiarata, 2.0 * area_dichiarata)
    return f, not (banda[0] <= ingombro_cm(f) <= banda[1])


def altezza(tag):
    """L'altezza di un edificio, e **da dove viene**.

    Restituisce `(metri, fonte, livelli)`. I tre valori possono essere
    `(None, "assente", None)`: non e' un fallimento, e' la dichiarazione che
    quell'edificio non si sa quanto e' alto. La regola e' quella di
    `fonti-visive.md` 4.3.
    """
    h = (tag.get("height") or "").strip().split(";")[0].strip()
    if h:
        try:
            return float(h.rstrip("m").strip()), "osm_height", None
        except ValueError:
            pass
    lv = (tag.get("building:levels") or "").strip()
    if lv:
        try:
            n = float(lv)
            return round(n * M_PER_PIANO, 1), "osm_levels", n
        except ValueError:
            pass
    return None, "assente", None

# Le categorie che il gioco sa nominare. Non e' una scelta estetica: sono quelle
# per cui `dettagli_ferrara.json` e le schede degli edifici hanno una cronologia,
# e quindi un edificio senza nome ma di questa categoria ha comunque qualcosa da
# dire. Un `building=yes` anonimo non lo sa.
CATEGORIE = {
    "church": "chiesa", "cathedral": "cattedrale", "chapel": "cappella",
    "castle": "castello", "palace": "palazzo", "monastery": "monastero",
    "tower": "torre", "townhall": "palazzo_comunale", "museum": "museo",
    "theatre": "teatro", "library": "biblioteca", "university": "universita",
    "fortification": "fortificazione", "ruins": "rovina",
}


def anello(el):
    """Il primo anello esterno di un elemento Overpass, in (lon, lat).

    Su una relazione multi-poligono Overpass con `out geom` mette i membri con
    `role: outer` in `geometry` e gli altri in nessun posto: si prende il primo
    anello con almeno tre vertici, che e' l'esterno per costruzione.
    """
    geo = el.get("geometry")
    if geo:
        return [(p["lon"], p["lat"]) for p in geo if "lon" in p]
    membri = el.get("members") or []
    for m in membri:
        g = m.get("geometry")
        if m.get("role") in ("outer", "") and g and len(g) >= 3:
            return [(p["lon"], p["lat"]) for p in g if "lon" in p]
    return []


def scegli(tag, sup):
    """Un edificio e' significativo? Tre ragioni, e si sa quale."""
    if tag.get("name") or tag.get("wikidata"):
        return "nominato"
    if sup["altezza"] is not None:
        return "altezza_dichiarata"
    cat = CATEGORIE.get((tag.get("building") or "").lower())
    if cat:
        return "categoria_" + cat
    if tag.get("heritage") or tag.get("historic"):
        return "patrimonio"
    if sup["area"] >= AREA_MINIMA:
        return "grande"
    return ""


def principale():
    solo_prova = "--prova" in sys.argv
    solo_luogo = None
    if "--luogo" in sys.argv:
        solo_luogo = sys.argv[sys.argv.index("--luogo") + 1]

    with open(LUOGHI, encoding="utf-8") as f:
        luoghi = json.load(f)["luoghi"]
    scelti = [l for l in luoghi
              if l.get("coord_stato") == "verificata" and l.get("lat") is not None
              and (solo_luogo is None or solo_luogo in l["luogo"])]

    # La ripresa esiste per una ragione concreta: Overpass risponde 504 e un
    # estrazione di 54 luoghi non finisce in un colpo. Senza ripresa si
    # ricomincerebbe da capo ogni volta che il server si stanca, e si perderebbero
    # anche i gruppi gia' fatti. Con la ripresa il file di uscita e' il punto di
    # partenza, e `--riprendi` salta i luoghi che ci sono gia'.
    gia = None
    if "--riprendi" in sys.argv and os.path.exists(USCITA):
        with open(USCITA, encoding="utf-8") as f:
            vecchio = json.load(f)
        gia = set(vecchio.get("luoghi", []))
        print("ripresa: %d luoghi gia' nel file" % len(gia))
    if gia:
        scelti = [l for l in scelti if l["luogo"] not in gia]
    # **I pin dei centocinquanta livelli, non solo quelli delle città.** Il
    # primo giro interrogava Overpass attorno ai pin del registro dei luoghi, e i
    # pin del registro sono città intere: i ventotto punti dell'anno 1 stanno
    # fra 204 e 1422 metri dal pin di Ferrara, e solo uno dei ventotto e' entro
    # i 250 metri che il generatore guarda. In pratica il file diceva «Ferrara ha
    # centoquattro edifici» e le tappe non ne avevano nessuno: le sagome c'erano,
    # e non erano di nessuno.
    #
    # Qui si interroga anche ogni livello, per **relazione esplicita**: la chiave
    # del record e' il livello, come nel file degli ambienti. Nessun confronto di
    # nomi, che e' la tecnica che ha fatto cadere Karakorum sulla catena.
    by_livello = {}
    if "--livelli" in sys.argv:
        with open(AMBIENTI, encoding="utf-8") as f:
            for a_ in json.load(f)["ambienti"]:
                pin = a_.get("pin_da_disegnare") or {}
                if pin.get("lat") is None:
                    continue
                if solo_luogo is not None and solo_luogo not in a_["livello"]:
                    continue
                if gia and a_["livello"] in gia:
                    continue
                by_livello[a_["livello"]] = a_
                scelti.append({"luogo": a_["livello"], "lat": pin["lat"],
                               "lon": pin["lon"], "livello": a_["livello"],
                               "tappa_di": a_.get("luogo")})
    # L'ordine conta piu' del numero: due aree che si sovrappongono costano a
    # Overpass come una sola, e i ventotto pin di Ferrara sono tutti dentro un
    # chilometro e mezzo. Ordinati per posizione, viaggiano insieme; mescolati a
    # città lontane, la stessa richiesta diventa piu' grande di qualsiasi server.
    scelti.sort(key=lambda l: (round(l["lat"], 1), round(l["lon"], 1)))
    print("aree da interrogare: %d (%d luoghi, %d livelli)"
          % (len(scelti), len([l for l in scelti if not l.get("livello")]),
             len([l for l in scelti if l.get("livello")])))

    edifici, scartati, per_luogo = [], {}, {}
    perduti, spezzati = [], {}
    if gia:
        edifici = vecchio.get("edifici", [])
        per_luogo = {k: v for k, v in
                     vecchio.get("riepilogo", {}).get("per_luogo", {}).items()}
        scartati = dict(vecchio.get("riepilogo", {}).get("scartati", {}))
        perduti = list(vecchio.get("luoghi_senza_edifici", []))
        spezzati = {"gruppo": vecchio.get("gruppi_spezzati", 0)}
    # **Un pin alla volta.** L'API delle mappe risponde a un rettangolo alla
    # volta, e non a un'unione di aree come Overpass: non c'e' piu' nessun gruppo,
    # nessuna richiesta che si rompe a meta' e nessuna risposta che arriva a
    # pezzi. Il prezzo e' una richiesta per pin — centonovanta — e il guadagno e'
    # che ciascuna risposta e' completa o assente, e il file dice quale.
    for i, l in enumerate(scelti):
        raggio = (raggio_del_livello(by_livello.get(l["luogo"], {}))
                  if l.get("livello") else RAGGIO_M)
        risposta, stato = scarica_osm.scarica(l["lat"], l["lon"], raggio)
        if stato != "ok":
            perduti.append([l["luogo"], stato])
            print("  %s: %s (raggio %d m)" % (l["luogo"], stato, raggio),
                  flush=True)
            continue
        elementi = risposta
        if not elementi:
            perduti.append([l["luogo"], "nessun_edificio"])
            print("  %s: nessun edificio entro %d m"
                  % (l["luogo"], raggio), flush=True)
            continue
        print("  %s: %d edifici entro %d m" % (l["luogo"], len(elementi), raggio),
              flush=True)
        per_luogo[l["luogo"]] = 0
        # Gli edifici si ordinano **per distanza dal centro della zona** e si
        # tiene il tetto: i piu' vicini sono quelli che la zona mostra, e gli
        # altri vengono dichiarati come scarto invece di sparire.
        ordinati = []
        for el in elementi:
            pts = anello(el)
            if len(pts) < 3:
                scartati["anello_troppo_corto"] = scartati.get(
                    "anello_troppo_corto", 0) + 1
                continue
            d = math.hypot((pts[0][0] - l["lon"]) * math.cos(
                math.radians(pts[0][1])), pts[0][1] - l["lat"])
            ordinati.append((d, pts, el))
        ordinati.sort(key=lambda t: t[0])
        tetto = TETTO_LIVELLO if l.get("livello") else TETTO_LUOGO
        if len(ordinati) > tetto:
            scartati["oltre_tetto_area"] = scartati.get(
                "oltre_tetto_area", 0) + len(ordinati) - tetto
            ordinati = ordinati[:tetto]

        for _d, pts, el in ordinati:
            tag = el.get("tags") or {}
            # il piano e' locale al pin dell'area: l'API ha gia' detto da dove
            # viene, e non c'e' nessun gruppo a cui attribuirlo
            mp = metri(l["lat"], l["lon"], pts)
            sup = {"area": area(mp)}
            h, fonte, liv = altezza(tag)
            sup["altezza"] = h
            motivo = scegli(tag, sup)
            if not motivo:
                scartati["anonimo_e_piccolo"] = scartati.get(
                    "anonimo_e_piccolo", 0) + 1
                continue
            if sup["area"] > (math.pi * raggio ** 2):
                scartati["fuori_raggio"] = scartati.get("fuori_raggio", 0) + 1
                continue
            sempl = dp_chiuso(mp, tolleranza_per(mp))
            if len(sempl) < 3:
                scartati["semplificato_troppo"] = scartati.get(
                    "semplificato_troppo", 0) + 1
                continue
            # La forma si costruisce **prima** di entrare nel file, e si
            # controlla che dica la stessa area del record: e' il difetto che
            # questa versione corregge, e il controllo sta qui perche' il
            # difetto nasce qui.
            f, perdita = forma(sempl, sup["area"])
            if perdita:
                scartati["forma_perdita_nell_arrotondamento"] = scartati.get(
                    "forma_perdita_nell_arrotondamento", 0) + 1
                continue
            if ingombro_cm(f) < INGOMBRO_MINIMO_M:
                scartati["troppo_piccolo_per_disegnare"] = scartati.get(
                    "troppo_piccolo_per_disegnare", 0) + 1
                continue
            per_luogo[l["luogo"]] = per_luogo.get(l["luogo"], 0) + 1
            edifici.append({
                "luogo": l["luogo"],
                "livello": l.get("livello"),
                "tappa_di": l.get("tappa_di"),
                "id": "%s/%s" % (el["type"], el["id"]),
                "nome": tag.get("name"),
                "categoria": CATEGORIE.get((tag.get("building") or "").lower()),
                "wikidata": tag.get("wikidata"),
                "forma": f,
                "area_m2": round(sup["area"], 1),
                "altezza_m": sup["altezza"],
                "fonte_altezza": fonte,
                "livelli": liv,
                "perche": motivo,
                "start_date": tag.get("start_date"),
                "fonte": "openstreetmap",
            })
        print("  aree %d/%d: %d edifici tenuti"
              % (i + 1, len(scelti), len(edifici)), flush=True)
        time.sleep(PAUSA_S)

    # il tetto per luogo: un centro storico con 400 edifici non e' piu' un
    # ambiente, e' un muro. Il file tiene i piu' grandi e dichiara quanti sono
    # spariti, perche' il tetto e' una soglia e le soglie vanno dichiarate.
    per_id = {}
    for e in edifici:
        per_id.setdefault(e["luogo"], []).append(e)
    tenuti = []
    for luogo, lista in per_id.items():
        lista.sort(key=lambda e: -e["area_m2"])
        tenuti.extend(lista[:MAX_PER_LUOGO])
        if len(lista) > MAX_PER_LUOGO:
            scartati["oltre_tetto_luogo"] = scartati.get(
                "oltre_tetto_luogo", 0) + len(lista) - MAX_PER_LUOGO
    tenuti.sort(key=lambda e: (e["luogo"], e["id"]))

    per_origine = {"con_altezza": 0, "da_piani": 0, "senza_altezza": 0}
    for e in tenuti:
        if e["fonte_altezza"] == "osm_height":
            per_origine["con_altezza"] += 1
        elif e["fonte_altezza"] == "osm_levels":
            per_origine["da_piani"] += 1
        else:
            per_origine["senza_altezza"] += 1

    print("\nedifici tenuti: %d su %d luoghi" % (len(tenuti), len(per_luogo)))
    if perduti:
        print("  luoghi perduti (dichiarati): %s"
              % ", ".join(x for g in perduti for x in g))
    print("  altezza: %d con height, %d da levels (stima dichiarata), "
          "%d senza altezza (volume neutro)"
          % (per_origine["con_altezza"], per_origine["da_piani"],
             per_origine["senza_altezza"]))
    print("  scartati: %s" % (", ".join("%s %d" % kv for kv in
                                       sorted(scartati.items())) or "nessuno"))
    if solo_prova:
        return 0

    doc = {
        "versione": 1,
        "data": "2026-10-03",
        "fonte": "OpenStreetMap, via API standard OSM 0.6",
        "licenza": LICENZA,
        "attribuzione": ATTRIBUZIONE,
        "nota_licenza": "ODbL e' copyleft: se il gioco riusa queste sagome "
                        "l'attribuzione va tenuta anche nei materiali derivati. "
                        "FONTI-E-LICENZE.md la cita",
        "formato": "coordinate locali in metri dal pin, in centimetri interi "
                   "(un metro = 100 unita'), semplificate con tolleranza fino a "
                   "%.1f m e comunque non oltre un ventesimo della dimensione "
                   "maggiore dell'anello, perche' a tolleranza fissa una stalla "
                   "di due metri veniva cancellata. Il formato e' quello di "
                   "mappe_formato.py, che il motore gia' sa leggere"
                   % TOLLERANZA,
        "regole": {
            "raggio_m": RAGGIO_M,
            "m_per_piano": M_PER_PIANO,
            "area_minima_m2": AREA_MINIMA,
            "tetto_per_luogo": MAX_PER_LUOGO,
            "significativo": "ha un nome, ha un wikidata, ha un'altezza o dei "
                             "piani, e' di una categoria che il gioco sa "
                             "nomiare, e' patrimonio, oppure ha un'area "
                             "maggiore di area_minima_m2",
        },
        "altezza": {
            "principio": "un'altezza non dichiarata non si stima: l'edificio "
                         "esce con altezza_m null e il motore ne fa un volume "
                         "neutro, che e' la regola di fonti-visive.md 4.3",
            "fonti": {"osm_height": "il tag height: e' la misura",
                      "osm_levels": "building:levels per m_per_piano: e' una "
                                    "stima dichiarata, non una misura",
                      "assente": "nessuna delle due: volume neutro"},
        },
        "luoghi": sorted(per_luogo),
        "luoghi_senza_edifici": perduti,
        "gruppi_spezzati": spezzati.get("gruppo", 0),
        "edifici": tenuti,
        "riepilogo": {
            "edifici": len(tenuti),
            "luoghi": len(per_luogo),
            "per_luogo": per_luogo,
            "altezza": per_origine,
            "scartati": scartati,
        },
    }
    with open(USCITA, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, separators=(",", ":"))
    print("scritto %s (%.0f kB)"
          % (os.path.relpath(USCITA, RADICE), os.path.getsize(USCITA) / 1024.0))
    return 0


if __name__ == "__main__":
    sys.exit(principale())