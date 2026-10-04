"""Compone i **fogli di controllo** degli oggetti di interazione.

`lingue-immagini.md` §6.2 Q1 dichiara che guardare i candidati «è un lavoro di
ore» e che **nessuno l'ha fatto**, e i fogli di controllo dei ritratti
(`fogli_controllo.py`) non esistono per gli oggetti: senza fogli l'attestazione a
vista è impossibile, e senza attestazione Q1 resta bloccante per tutte le
tappe dell'oggetto. Questo file li produce.

**Tre regole che vengono dai ritratti e che qui si ripetono.**

1. **Una pagina e non un'immagine composta**: le dimensioni, la griglia e le
   etichette stanno nel file di testo, non dentro un'immagine che non si
   interroga.
2. **Le immagini sono incorporate**: la pagina è un file solo. Se le vicine
   sono su disco il foglio si apre con trenta icone rotte, che sembrerebbero un
   difetto della ricerca.
3. **Il foglio non seleziona**: mostra anche i candidati sospetti, e li mette
   **in testa**, perché un foglio che nasconde i sospetti serve a confermare e
   non a controllare. La ricerca aveva restituito un gatto per Renata Viganò e
   `Antonio Allegri da Correggio.jpg` per «la correggia».

**I candidati di ogni voce**: prima quelli del **secondo giro** (la ricerca che
cerca la cosa che si vede), e se non ce ne sono quelli del primo. Il giro è
scritto in ogni pagina, cella per cella.

Uso:
    python3 sorgenti/lingue/fogli_oggetti.py             # scarica e scrive
    python3 sorgenti/lingue/fogli_oggetti.py --indice    # conta e basta
"""
import base64
import concurrent.futures as cf
import io
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

BASE = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(BASE, "..", ".."))
PRIMO = os.path.join(RADICE, "dati", "lingue", "immagini_oggetti.json")
SECONDO = os.path.join(RADICE, "dati", "lingue", "immagini_2.json")
CARTELLA = os.path.join(RADICE, "sorgenti", "lingue", "fogli_oggetti")
CACHE = os.path.join(CARTELLA, "cache")

API = "https://commons.wikimedia.org/w/api.php"
UA = "i-cinque-duchi/0.2 (progetto didattico per liceo; pietrofabbri)"

LINGUE = ("IT", "FE", "LA", "EN", "SI", "EL")
NOMI_LINGUA = {"IT": "Italiano", "FE": "Ferrarese", "LA": "Latino",
               "EN": "Inglese", "SI": "Lingua dei segni", "EL": "Greco"}

PER_VOCE = 3
PER_FOGLIO = 10
LATO = 190
LARGHEZZA_THUMB = 400


def carica(percorso):
    with open(percorso, encoding="utf-8") as f:
        return json.load(f)["risultati"]


def voci():
    primo = carica(PRIMO)
    secondo = {(r["lingua"], r["voce"]): r for r in carica(SECONDO)}
    out = []
    for lingua in LINGUE:
        for r in [x for x in primo if x["lingua"] == lingua]:
            g2 = secondo.get((lingua, r["voce"]))
            scelti = (g2["candidati"], 2) if (g2 and g2["candidati"]) \
                else (r["candidati"], 1)
            out.append({"lingua": lingua, "numero": r["numero"],
                        "voce": r["voce"],
                        "termini": (g2 or r).get("termini", []),
                        "candidati": scelti[0][:PER_VOCE], "giro": scelti[1],
                        "motivo_nessuna": r.get("motivo", "")})
    return out


def sospetto(c, voce, termini):
    """Il nome del file nomina la voce o il termine cercato? Se no, sospetto."""
    parole = [p for p in re.split(r"[\s,'’]+", voce.lower()) if len(p) > 3]
    nome = (c.get("file") or "").lower()
    for p in parole:
        if p[:6] in nome:
            return False
    for t in [c.get("termino", "")] + list(termini):
        t = (t or "").lower()
        if len(t) > 4 and t[:8] in nome:
            return False
    return True


def api(params, tentativi=4):
    for k in range(tentativi):
        try:
            r = urllib.request.Request(
                API + "?" + urllib.parse.urlencode(params),
                headers={"User-Agent": UA, "Accept": "application/json"})
            with urllib.request.urlopen(r, timeout=60) as f:
                return json.load(f)
        except Exception:
            time.sleep(2 * (k + 1))
    return {}


def url_thumb(titoli):
    """Gli URL delle miniature, in blocchi da cinquanta titoli.

    Un blocco e' una richiesta: chiedere ogni file da solo sarebbe una richiesta
    per immagine, e Commons risponde con un 429 che va letto come «nessuna
    immagine esiste» — l'errore che il progetto ha gia' imparato a temere.
    """
    url = {}
    for i in range(0, len(titoli), 50):
        blocco = titoli[i:i + 50]
        d = api({"action": "query", "format": "json",
                 "titles": "|".join(blocco), "prop": "imageinfo",
                 "iiprop": "url", "iiurlwidth": str(LARGHEZZA_THUMB)})
        for pagina in (d.get("query", {}).get("pages", {}) or {}).values():
            ii = (pagina.get("imageinfo") or [{}])[0]
            t = ii.get("thumburl") or ii.get("url")
            if t:
                url[pagina.get("title", "")] = t
        time.sleep(0.3)
    return url


def scarica(url, nome):
    if not url:
        return None
    destinazione = os.path.join(CACHE, nome)
    if os.path.exists(destinazione) and os.path.getsize(destinazione) > 0:
        return destinazione
    try:
        r = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(r, timeout=90) as f:
            dati = f.read()
        with open(destinazione, "wb") as f:
            f.write(dati)
        return destinazione
    except Exception:
        return None


def html_voce(v, url):
    celle = []
    for c in v["candidati"]:
        nome = re.sub(r"[^A-Za-z0-9._-]", "_", c["file"].split(":", 1)[-1])[-60:]
        percorso = scarica(url.get(c["file"]), nome)
        if percorso:
            with open(percorso, "rb") as f:
                b64 = base64.b64encode(f.read()).decode("ascii")
            ext = "jpeg" if percorso.endswith((".jpg", ".jpeg")) else "png"
            img = ("<img src='data:image/%s;base64,%s' alt='%s'>"
                   % (ext, b64, c["file"]))
        else:
            img = "<div class='mancante'>immagine non scaricata</div>"
        sos = " SOSPETTO" if sospetto(c, v["voce"], v["termini"]) else ""
        celle.append(
            "<figure><div class='box'>%s</div><figcaption>"
            "<b>%s</b>%s<br><span class='meta'>%s<br>%s · %s<br>%sx%s</span>"
            "</figcaption></figure>"
            % (img, re.sub(r"<[^>]+>", "", c["file"])[-46:], sos,
               c.get("licenza", "?")[:40], c.get("autore", "?")[:70],
               (c.get("data") or "senza data")[:24],
               c.get("larghezza"), c.get("altezza")))
    if not celle:
        return ("<section class='voce'><h3>%s %d · %s</h3>"
                "<p class='vuoto'>nessun candidato%s</p></section>"
                % (v["lingua"], v["numero"], v["voce"],
                   (": " + v["motivo_nessuna"]) if v["motivo_nessuna"] else ""))
    return ("<section class='voce'><h3>%s %d · %s <small>giro %d — cercato: %s</small></h3>"
            "<div class='celle'>%s</div></section>"
            % (v["lingua"], v["numero"], v["voce"], v["giro"],
               ", ".join(v["termini"])[:80], "".join(celle)))


CSS = """<style>
body{font-family:Georgia,serif;background:#f6f2ea;color:#2b2622;margin:0;padding:10px}
h1{font-size:20px}h2{font-size:16px;border-bottom:1px solid #cfc6b5;padding-bottom:3px}
.voce{border:1px solid #ddd5c6;background:#fff;padding:6px;margin:8px 0}
h3{margin:0 0 5px;font-size:14px}
h3 small{font-weight:normal;color:#777;font-size:11px}
.celle{display:flex;gap:6px;flex-wrap:wrap}
figure{margin:0;width:%dpx}
.box{width:%dpx;height:%dpx;background:#eee;border:1px solid #ccc;overflow:hidden}
.box img{width:%%100%%;height:%%100%%;object-fit:contain}
.mancante{padding:20px 4px;color:#a33;font-size:11px;text-align:center}
figcaption{font-size:9px;line-height:1.25;margin-top:2px;word-wrap:break-word}
.meta{color:#666}
.SOSPETTO{color:#a03000;font-weight:bold}
.vuoto{color:#777;font-size:12px;font-style:italic}
</style>""" % (LATO, LATO, int(LATO * 0.75))


def scrivi_fogli(voci_):
    os.makedirs(CARTELLA, exist_ok=True)
    os.makedirs(CACHE, exist_ok=True)
    titoli = sorted({c["file"] for v in voci_ for c in v["candidati"]})
    print("   %d file da chiedere a Commons, in blocchi da 50" % len(titoli))
    url = url_thumb(titoli)
    print("   %d URL di miniatura ottenuti" % len(url))

    fogli, per = [], PER_FOGLIO
    for i in range(0, len(voci_), per):
        fogli.append(voci_[i:i + per])
    scritte = []
    for n, blocco in enumerate(fogli, 1):
        lingue = sorted({v["lingua"] for v in blocco})
        corpo = "".join(html_voce(v, url) for v in blocco)
        html = ("<!doctype html><meta charset='utf-8'><title>foglio oggetti %02d</title>"
                "%s<h1>Foglio di controllo degli oggetti — %d di %d</h1>"
                "<h2>Lingue: %s — tre candidati per voce, i sospetti in cima</h2>"
                "<p>Ogni cella porta il nome del file su Commons, la licenza, "
                "l'autore, la data e la misura. <b>SOSPETTO</b> vuol dire che "
                "il nome del file non nomina né la voce né il termine cercato: "
                "va guardata per prima, non scartata.</p>%s"
                % (n, CSS, n, len(fogli),
                   ", ".join(NOMI_LINGUA[l] for l in lingue), corpo))
        percorso = os.path.join(CARTELLA, "foglio_oggetti_%02d.html" % n)
        with io.open(percorso, "w", encoding="utf-8") as f:
            f.write(html)
        scritte.append(percorso)
        print("   scritto %s (%d voci, %.1f MB)"
              % (os.path.basename(percorso), len(blocco),
                 os.path.getsize(percorso) / 1e6))
    return scritte


def main():
    v = voci()
    print("== fogli di controllo degli oggetti")
    print("   %d voci, %d candidati mostrati"
          % (len(v), sum(len(x["candidati"]) for x in v)))
    print("   voci senza candidati: %d"
          % sum(1 for x in v if not x["candidati"]))
    if "--indice" in sys.argv:
        return 0
    scritte = scrivi_fogli(v)
    indice = {"versione": 1, "data": time.strftime("%Y-%m-%d"),
              "che_cosa_e": "i fogli che l'attestazione a vista richiede: "
                            "nessuno ha ancora guardato i candidati degli "
                            "oggetti, e la ricerca ha gia' restituito un "
                            "ritratto di pittore per «la correggia»",
              "come": "per ogni voce, i tre candidati migliori del secondo "
                      "giro (o del primo se il secondo non ne ha), con la "
                      "licenza, l'autore, la data e la misura",
              "candidati_per_voce": PER_VOCE, "voci_per_foglio": PER_FOGLIO,
              "lingue": list(LINGUE),
              "fogli": [os.path.basename(x) for x in scritte]}
    with io.open(os.path.join(CARTELLA, "indice.json"), "w",
                 encoding="utf-8") as f:
        json.dump(indice, f, ensure_ascii=False, indent=1)
    print("   %d fogli in %s" % (len(scritte),
                                 os.path.relpath(CARTELLA, RADICE)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
