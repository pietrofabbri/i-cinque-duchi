"""Va a leggere i metadati di Commons delle immagini rimaste `da_verificare`.

Il giudizio a vista può stabilire **che cos'e'** l'immagine (un ritratto, uno
stemma, una scena), ma non **di chi e'**: due profili di dame del Cinquecento sono
identici a occhio, e i ritratti dei duchi estensi sono i piu' scambiati fra loro di
tutta la raccolta. Il metadato e' il pezzo che manca: la descrizione che
l'uploader ha scritto, le categorie, il titolo dell'opera.

**Perche' pero' il metadato non e' una prova e va letto con caution.** Il
metadato dice *che cosa dichiara il file*, non se il file ha ragione: su Commons
la descrizione la scrive chi ha caricato il file. Percio' qui non si accetta
niente: si mette a confronto **tre** cose e si giudica solo se concordano —
il nome del file, la descrizione, le categorie. Se due delle tre dicono una cosa
e la terza un'altra, l'immagine resta aperta e il conflitto si scrive per iscritto,
perche' un conflitto nascosto diventa una scelta sbagliata a schermo.

Uso:
    python3 sorgenti/art/verifica_metadati.py          # cosa dichiara Commons
    python3 sorgenti/art/verifica_metadati.py --grep X # filtra per una parola
"""
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

ART = os.path.dirname(os.path.abspath(__file__))
ESITO = os.path.join(ART, "ritratti_disponibili.json")
ATTEST = os.path.join(ART, "attestazione_immagini.json")
API = "https://commons.wikimedia.org/w/api.php"
UA = "i-cinque-duchi/0.4 (progetto didattico per liceo; pietrofabbri)"
LOTTO = 20


def chiedi(parametri):
    corpo = urllib.parse.urlencode(dict(parametri, format="json")).encode()
    for k in range(5):
        try:
            r = urllib.request.Request(API, data=corpo, headers={
                "User-Agent": UA, "Accept": "application/json",
                "Content-Type": "application/x-www-form-urlencoded"})
            with urllib.request.urlopen(r, timeout=60) as f:
                d = json.load(f)
            if d.get("error"):
                return None
            return d
        except urllib.error.HTTPError as e:
            if e.code in (429, 503):
                attesa = float(e.headers.get("Retry-After") or 0) or 10 * (k + 1)
                print("   %d, attendo %.0f s" % (e.code, attesa), flush=True)
                time.sleep(attesa)
                continue
            return None
        except Exception:
            time.sleep(3 * (k + 1))
    return None


def pulisci(testo):
    testo = re.sub(r"<[^>]+>", " ", testo or "")
    testo = re.sub(r"&[a-z]+;", " ", testo)
    return re.sub(r"\s+", " ", testo).strip()


def main(filtro=None):
    att = json.load(open(ATTEST, encoding="utf-8"))
    esiti = json.load(open(ESITO, encoding="utf-8"))
    per = {e["codice"]: e for e in esiti}
    aperti = [k for k in sorted(att)
              if not k.startswith("_") and att[k].get("esito") == "da_verificare"]
    if filtro:
        aperti = [k for k in aperti
                  if filtro.lower() in json.dumps(att[k], ensure_ascii=False).lower()
                  or filtro.lower() in per.get(k, {}).get("nome", "").lower()]
    print("da verificare: %d\n" % len(aperti))

    for i in range(0, len(aperti), LOTTO):
        gruppo = aperti[i:i + LOTTO]
        titoli = [per[k]["immagine"] for k in gruppo]
        d = chiedi({
            "action": "query", "prop": "imageinfo",
            "iiprop": "extmetadata|canonicaltitle|size",
            "titles": "|".join("File:" + t.replace("_", " ") for t in titoli)})
        if not d:
            raise SystemExit("Interrotto: Commons non ha risposto bene.")
        cat = chiedi({"action": "query", "prop": "categories",
                      "cllimit": "200",
                      "titles": "|".join("File:" + t.replace("_", " ")
                                         for t in titoli)})
        categorie = {}
        if cat:
            for _, p in (cat.get("query", {}).get("pages") or {}).items():
                categorie[p.get("title", "")] = [c["title"] for c in
                                                p.get("categories", [])]
        per_titolo = {}
        for _, p in (d.get("query", {}).get("pages") or {}).items():
            ii = (p.get("imageinfo") or [None])[0]
            if not ii:
                continue
            em = ii.get("extmetadata", {})
            per_titolo[p["title"]] = {
                "descrizione": pulisci((em.get("ImageDescription", {}) or {})
                                       .get("value", ""))[:400],
                "credito": pulisci((em.get("Credit", {}) or {}).get("value", ""))[:160],
                "categorie": categorie.get(p.get("title", ""), []),
            }

        for k in gruppo:
            e = per[k]
            titolo = "File:" + e["immagine"].replace("_", " ")
            info = per_titolo.get(titolo)
            print("=== %s · %s" % (k, e["nome"]))
            print("   file        : %s" % e["immagine"])
            if not info:
                print("   METADATO    : assente — il file non esiste più o "
                      "l'albero non l'ha trovato\n")
                continue
            print("   descrizione : %s" % (info["descrizione"] or "(nessuna)"))
            if info["credito"]:
                print("   credito     : %s" % info["credito"])
            if info["categorie"]:
                print("   categorie   : %s" % "; ".join(info["categorie"][:14]))
            print("   misura      : %sx%s" % (e.get("dettagli", {})
                                             .get("larghezza"),
                                             (e.get("dettagli") or {})
                                             .get("altezza")))
            print()


if __name__ == "__main__":
    main(sys.argv[sys.argv.index("--grep") + 1]
         if "--grep" in sys.argv else None)