"""Prepara le miniature per la pubblicazione della pagina di scelta.

Due cose: **ricomprime** ogni miniatura in JPEG (qualità 72, sfondo bianco
sotto la trasparenza), che dimezza il peso senza cambiare quello che si vede a
250 px; e **divide l'italiano per anno** (`IT-1.json` … `IT-5.json`), perché
il suo file intero supera i 16 MB che una pagina pubblicata accetta per file e
perché sul telefono si carica un anno alla volta.

Legge `verifica/miniature/<LINGUA>.json` (`miniature.py`) e scrive
`verifica/pubblica/miniature/`. Uso:
    python3 sorgenti/lingue/scelta/prepara_pubblicazione.py
"""
import base64
import io
import json
import os

from PIL import Image

RADICE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
ENTRA = os.path.join(RADICE, "verifica", "miniature")
ESCE = os.path.join(RADICE, "verifica", "pubblica", "miniature")
ESITO = os.path.join(RADICE, "dati", "lingue", "immagini_oggetti.json")


def ricomprimi(uri):
    dati = base64.b64decode(uri.split(",", 1)[1])
    try:
        im = Image.open(io.BytesIO(dati))
        im.load()
    except Exception:
        return uri
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        fondo = Image.new("RGB", im.size, (255, 255, 255))
        fondo.paste(im, mask=im.split()[-1])
        im = fondo
    else:
        im = im.convert("RGB")
    out = io.BytesIO()
    im.save(out, "JPEG", quality=72, optimize=True, progressive=True)
    return "data:image/jpeg;base64," + base64.b64encode(out.getvalue()).decode()


def main():
    os.makedirs(ESCE, exist_ok=True)
    with open(ESITO, encoding="utf-8") as f:
        risultati = json.load(f)["risultati"]
    for nome in sorted(os.listdir(ENTRA)):
        lingua = nome[:-5]
        with open(os.path.join(ENTRA, nome), encoding="utf-8") as f:
            mini = {k: ricomprimi(v) for k, v in json.load(f).items()}
        if lingua == "IT":
            gruppi = {}
            for r in risultati:
                if r["lingua"] == "IT":
                    for c in r["candidati"]:
                        if c["file"] in mini:
                            gruppi.setdefault("IT-%d" % r["anno"], {})[c["file"]] = mini[c["file"]]
        else:
            gruppi = {lingua: mini}
        for chiave, contenuto in sorted(gruppi.items()):
            p = os.path.join(ESCE, chiave + ".json")
            with open(p, "w", encoding="utf-8") as f:
                json.dump(contenuto, f)
            print(chiave, len(contenuto), "miniature", "%.1f MB" % (os.path.getsize(p) / 1e6))


if __name__ == "__main__":
    main()
