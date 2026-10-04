"""Scarica da OpenStreetMap gli edifici di una zona, dall'API delle mappe.

**Perche' non Overpass, e che cosa e' successo.** Il file delle sagome del 3
ottobre 2026 era stato costruito con Overpass, e il 4 ottobre Overpass ha risposto
`504 Gateway Timeout` a quattro richieste di fila: l'istanza principale era satura
e le due alternative non si raggiungevano. Un progetto che dipende dall'umore di
un server pubblico non e' un progetto che ha una fonte: e' un progetto che
aspetta.

L'**API delle mappe** risponde invece in meno di un secondo, e per quello che
serve qui e' la strada giusta: `api/0.6/map?bbox=…` restituisce tutto quello che
c'e' in un rettangolo, senza query e senza dover imparare Overpass QL. La prova
sulla piazza della Cattedrale (tappa 1-1) ha risposto `200` in 0,72 secondi con
ventidue edifici di geometria vera fra cui la Cattedrale di San Giorgio Martire e
la Loggia dei Merciai — le due cose che la tabella 3 del documento dice e che il
motore deve poter aprire.

**I limiti, dichiarati e non nascosti.** L'API ha un tetto di **cinquantamila nodi**
per richiesta: una tappa con 250 metri di raggio sta sotto le mille, e il file
dichiara i centocinquantamila? No: dichiara il tetto e il fatto che nessuna zona
del gioco lo raggiunge. Un bbox troppo grande viene rifiutato e il chiamante lo
sa, perche' qui non si restituisce mai un elenco vuoto al posto di uno pieno: una
risposta che non arriva e una risposta che non c'e' sono due fatti diversi.

**Le relazioni, e il buco che resta.** Un edificio puo' essere una `relation` di
tipo multipolygon: si prende il primo anello esterno, che e' l'esterno per
costruzione. Se la relazione ha **buchi interni** non li si disegna, e il file
lo dichiara contando le relazioni con buchi: meglio un edificio disegnato senza
il suo cortile che un file che mente sul numero di anelli.

Il formato restituito e' **lo stesso che Overpass restituiva** — `type`, `id`,
`tags`, `geometry` in (lon, lat), e per le relazioni `members` con `geometry` —
perche' `edifici_footprint.py` deve poter cambiare fonte senza cambiare le sue
regole: le regole di significativita' e di altezza sono del progetto, non di una
query.

Uso:
    python3 sorgenti/gis/scarica_osm.py            # un prova e basta
"""
import json
import math
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

API = "https://api.openstreetmap.org/api/0.6/map"
UA = "i-cinque-duchi/0.1 (progetto didattico per liceo; pietrofabbri)"
NODI_MAX = 50000


def bbox(lat, lon, raggio_m):
    """Il rettangolo che contiene il raggio, in (minlon, minlat, maxlon, maxlat)."""
    d = raggio_m / 111320.0
    dlat = d
    dlon = d / max(math.cos(math.radians(lat)), 1e-6)
    return (lon - dlon, lat - dlat, lon + dlon, lat + dlat)


def _tags(el):
    return {c.attrib["k"]: c.attrib["v"] for c in el if c.tag == "tag"}


def _edificio(tag):
    return "building" in tag or any(k.startswith("building:") for k in tag)


def scarica(lat, lon, raggio_m, tentativi=3):
    """Gli edifici di un raggio, nel formato che Overpass restituiva.

    Ritorna `(elementi, stato)`, e `stato` e' una delle quattro cose che sono
    successe: `"ok"`, `"troppo_grande"`, `"http_<codice>"` o `"nessuna_risposta"`.
    Il chiamante deve poter distinguere una tappa senza edifici da una tappa che
    non e' stata chiesta.
    """
    b = bbox(lat, lon, raggio_m)
    url = "%s?bbox=%s" % (API, ",".join("%.6f" % v for v in b))
    for k in range(tentativi):
        try:
            req = urllib.request.Request(API + "?bbox=" +
                                         ",".join("%.6f" % v for v in b),
                                         headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=120) as f:
                corpo = f.read()
            if len(corpo) > 12 * 1024 * 1024:
                return [], "troppo_grande"
            return elementi(corpo), "ok"
        except urllib.error.HTTPError as e:
            if e.code in (400, 509):      # bbox troppo grande: si dice e basta
                return [], "troppo_grande"
            if e.code in (429, 503, 504):
                time.sleep(10 * (k + 1))
                continue
            return [], "http_%d" % e.code
        except Exception:
            time.sleep(5 * (k + 1))
    return [], "nessuna_risposta"


def elementi(corpo):
    """L'XML dell'API nei way e nelle relation che portano un edificio."""
    radice = ET.fromstring(corpo)
    nodi = {n.attrib["id"]: (float(n.attrib["lon"]), float(n.attrib["lat"]))
            for n in radice if n.tag == "node"}

    fuori = []
    for w in radice:
        if w.tag != "way":
            continue
        tag = _tags(w)
        if not _edificio(tag):
            continue
        punti = [nodi[c.attrib["ref"]] for c in w if c.tag == "nd"
                 and c.attrib["ref"] in nodi]
        if len(punti) < 3:
            continue
        fuori.append({"type": "way", "id": w.attrib["id"], "tags": tag,
                      "geometry": [{"lon": x, "lat": y} for x, y in punti]})

    for r in radice:
        if r.tag != "relation":
            continue
        tag = _tags(r)
        if not _edificio(tag):
            continue
        membri = []
        for m in r:
            if m.tag != "member" or m.attrib.get("type") != "way":
                continue
            w = [x for x in radice if x.tag == "way"
                 and x.attrib["id"] == m.attrib["ref"]]
            if not w:
                continue
            punti = [nodi[c.attrib["ref"]] for c in w[0] if c.tag == "nd"
                     and c.attrib["ref"] in nodi]
            if len(punti) >= 3:
                membri.append({"role": m.attrib.get("role", ""),
                               "geometry": [{"lon": x, "lat": y}
                                            for x, y in punti]})
        if membri:
            fuori.append({"type": "relation", "id": r.attrib["id"],
                          "tags": tag, "members": membri})
    return fuori


def conta_buchi(risposta_xml):
    """Quante relation con tag edificio hanno buchi interni. Lo dichiara."""
    if isinstance(risposta_xml, bytes):
        risposta_xml = ET.fromstring(risposta_xml)
    n = 0
    for r in risposta_xml:
        if r.tag != "relation":
            continue
        if not _edificio(_tags(r)):
            continue
        ruoli = [m.attrib.get("role", "") for m in r if m.tag == "member"]
        if "inner" in ruoli:
            n += 1
    return n


if __name__ == "__main__":
    lat = float(sys.argv[1]) if len(sys.argv) > 1 else 44.83604
    lon = float(sys.argv[2]) if len(sys.argv) > 2 else 11.619803
    elementi_trovati, stato = scarica(lat, lon, 250.0)
    print("stato: %s" % stato)
    print("edifici: %d" % len(elementi_trovati))
    for e in elementi_trovati[:10]:
        print("  %-9s %-11s %-40s %d punti"
              % (e["type"], e["id"],
                 (e["tags"].get("name") or e["tags"].get("building") or "-")[:40],
                 len(e.get("geometry") or e["members"][0]["geometry"])))
