"""Scarica da Wikimedia Commons le miniature dei candidati di
`dati/lingue/immagini_oggetti.json`, per lo strumento di scelta delle immagini.

Le miniature (250 px di larghezza) diventano un file JSON per lingua,
`verifica/miniature/<LINGUA>.json`, con `{file: "data:image/jpeg;base64,..."}`:
la pagina pubblicata non può caricare immagini da Commons (la sua politica di
sicurezza lo vieta), quindi le immagini viaggiano con la pagina. I file non
sono nel ramo (`verifica/` è ignorata) e si rigenerano con questo comando.

Uso:  python3 sorgenti/lingue/scelta/miniature.py            # tutte le lingue
      python3 sorgenti/lingue/scelta/miniature.py LA EN    # solo alcune
"""
import base64
import json
import os
import sys
import time
import urllib.parse
import urllib.request

RADICE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
ESITO = os.path.join(RADICE, "dati", "lingue", "immagini_oggetti.json")
USCITA = os.path.join(RADICE, "verifica", "miniature")
UA = ("ICinqueDuchi/0.2 (https://github.com/pietrofabbri/i-cinque-duchi; "
      "progetto didattico) python-urllib")
API = "https://commons.wikimedia.org/w/api.php"
LARGHEZZA = 250  # Commons ammette solo misure a gradini: 240 dà errore 400


def richiesta(url, tentativi=5):
    for k in range(tentativi):
        try:
            r = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(r, timeout=60) as f:
                return f.read(), f.headers.get("Content-Type", "")
        except urllib.error.HTTPError as e:
            if e.code in (429, 503):
                time.sleep(float(e.headers.get("Retry-After") or 0) or 5 * (k + 1))
                continue
            return None, ""
        except Exception:
            time.sleep(2 * (k + 1))
    return None, ""


def indirizzi(titoli):
    """L'indirizzo della miniatura di ogni file, cinquanta titoli per volta."""
    fuori = {}
    for i in range(0, len(titoli), 50):
        q = urllib.parse.urlencode({
            "action": "query", "format": "json", "prop": "imageinfo",
            "iiprop": "url", "iiurlwidth": str(LARGHEZZA),
            "titles": "|".join(titoli[i:i + 50])})
        corpo, _ = richiesta(API + "?" + q)
        if not corpo:
            continue
        d = json.loads(corpo)
        norm = {n["to"]: n["from"] for n in d.get("query", {}).get("normalized", [])}
        for p in d.get("query", {}).get("pages", {}).values():
            ii = (p.get("imageinfo") or [{}])[0]
            if ii.get("thumburl"):
                # Commons risponde con thumb.wikimedia.org, che la rete del
                # progetto non raggiunge; lo stesso file sta su
                # upload.wikimedia.org, e i parametri di tracciamento si tolgono
                u = ii["thumburl"].split("?")[0].replace(
                    "//thumb.wikimedia.org/", "//upload.wikimedia.org/")
                fuori[norm.get(p["title"], p["title"])] = u
        time.sleep(0.5)
    return fuori


def main():
    with open(ESITO, encoding="utf-8") as f:
        risultati = json.load(f)["risultati"]
    os.makedirs(USCITA, exist_ok=True)
    per_lingua = {}
    for r in risultati:
        for c in r["candidati"]:
            per_lingua.setdefault(r["lingua"], set()).add(c["file"])
    scelte = [a for a in sys.argv[1:] if not a.startswith("-")]
    for lingua, titoli in sorted(per_lingua.items()):
        if scelte and lingua not in scelte:
            continue
        percorso = os.path.join(USCITA, lingua + ".json")
        fatte = {}
        if os.path.exists(percorso):
            with open(percorso, encoding="utf-8") as f:
                fatte = json.load(f)
        mancano = sorted(t for t in titoli if t not in fatte)
        url = indirizzi(mancano)
        for n, t in enumerate(mancano, 1):
            if t not in url:
                continue
            corpo, tipo = richiesta(url[t])
            if corpo:
                tipo = tipo.split(";")[0] or "image/jpeg"
                fatte[t] = "data:%s;base64,%s" % (tipo, base64.b64encode(corpo).decode())
            if n % 10 == 0:
                print(lingua, n, "/", len(mancano), flush=True)
                with open(percorso, "w", encoding="utf-8") as f:
                    json.dump(fatte, f)
            time.sleep(2.5)  # piu' in fretta upload.wikimedia.org risponde 429
        with open(percorso, "w", encoding="utf-8") as f:
            json.dump(fatte, f)
        print(lingua, len(fatte), "miniature su", len(titoli),
              "%.1f MB" % (os.path.getsize(percorso) / 1e6), flush=True)


if __name__ == "__main__":
    sys.exit(main())
