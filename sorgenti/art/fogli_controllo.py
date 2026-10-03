"""Compone i **fogli di controllo** dei ritratti che nessuno ha ancora guardato.

`ritratti.md` §5 punto 3 scrive che il taglio del viso è automatico e che i fogli
di controllo sono «**da produrre**»: nessuno li aveva prodotti, e senza fogli
l'attestazione a vista dei 150 ritratti è impossibile. Questo file li produce.

**Perché una pagina e non un'immagine composta.** Il progetto non ha librerie di
immagini, e una pagina dichiara il foglio in testo leggibile: le dimensioni, la
griglia e le etichette sono nel file, non dentro un'imm che non si interroga. La
riduzione la fa `sips`, che è nel sistema.

**Perché il foglio si fa sul grezzo e non sul ritratto finito.** Il ritratto finito
è di 48×54 px: a quella misura non si distingue un volto da un gatto, e il giudizio
che conta è proprio quello. Qui si mostra il file di Commons com'è.

**Perché le immagini sono incorporate nella pagina.** La pagina viene servita con
un solo file: le immagini vicine non si vedono (404) e il foglio si aprirebbe con
venti icone rotte, che sembrerebbero un difetto della ricerca. Incorporarle elimina
il problema alla radice e rende il foglio un file solo, che si può aprire, salvare
e girare.

**Le regole**, dichiarate perché un foglio di controllo è uno strumento di misura:
ogni cella porta **codice, nome e licenza**, perché un giudizio senza il nome della
persona a cui si riferisce non si può applicare a nessuno; il foglio **non
seleziona**, mostra anche le immagini sospette, perché un foglio che nasconde i
sospetti serve a confermare e non a controllare.

Uso:
    python3 sorgenti/art/fogli_controllo.py     # scrive foglio_NN.html
"""
import base64
import json
import os
import subprocess
import tempfile

ART = os.path.dirname(os.path.abspath(__file__))
ELENCO = os.path.join(ART, "ritratti_disponibili.json")
GREZZI = os.path.join(ART, "ritratti_grezzi")

COLS = 3
PER_FOGLIO = 12          # 4 righe da 3: una schermata che si legge tutta
ALTEZZA = 250            # l'altezza della cella immagine, in pixel
LATO = 420               # il lato lungo dell'immagine nel foglio
GRIGLIA = "#d8d2c6"


def da_vedere():
    """I ritratti esistenti e non ancora attestati, in ordine di anno e codice."""
    d = json.load(open(ELENCO, encoding="utf-8"))
    out = []
    for e in sorted(d, key=lambda x: (x["anno"], x["codice"])):
        if e["motivo"] != "ok" or e.get("attestato"):
            continue
        if os.path.exists(os.path.join(GREZZI, e["codice"] + ".img")):
            out.append(e)
    return out


def ridotta(codice, cache):
    """Il grezzo ridotto a `LATO` px, in JPEG, e il suo testo in linea.

    La riduzione la fa `sips`, che c'è nel sistema: il progetto non ha librerie di
    immagini e non si aggiungono dipendenze per comporre un foglio. Il risultato
    entra in memoria come `data:` e non come file, quindi il foglio è autosufficiente.
    """
    if codice in cache:
        return cache[codice]
    src = os.path.join(GREZZI, codice + ".img")
    tmp = os.path.join(tempfile.gettempdir(), "f_%s.jpg" % codice)
    subprocess.run(["sips", "-Z", str(LATO), src, "--out", tmp],
                   capture_output=True, check=False)
    try:
        with open(tmp, "rb") as f:
            dati = f.read()
    except OSError:
        dati = b""
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)
    uri = "data:image/jpeg;base64," + base64.b64encode(dati).decode("ascii") if dati else ""
    cache[codice] = uri
    return uri


def pagina(gruppo, indice, totale, cache):
    """Una pagina di fogli: griglia, codice, nome, licenza, immagine."""
    pezzi = [
        "<!doctype html><meta charset='utf-8'>",
        "<title>foglio %d di %d</title>" % (indice, totale),
        "<style>",
        "body{background:#faf8f4;color:#1e2228;font:13px/1.3 -apple-system,"
        "system-ui,sans-serif;margin:10px}",
        "h1{font-size:16px;margin:0 0 10px}",
        ".g{display:grid;grid-template-columns:repeat(%d,1fr);gap:6px}" % COLS,
        ".c{background:#fff;border:1px solid %s;padding:3px}" % GRIGLIA,
        ".c img{width:100%%;height:%dpx;object-fit:contain;display:block;"
        "background:#eee}" % ALTEZZA,
        ".cod{color:#961e14;font-weight:700;font-size:14px;margin-top:2px}",
        ".lic{color:#6e7076;font-size:11px}",
        "</style>",
        "<h1>foglio %d di %d — %d ritratti da guardare a vista</h1>"
        % (indice, totale, len(gruppo)),
        "<div class='g'>",
    ]
    for e in gruppo:
        codice = e["codice"]
        nome = e["nome"].replace("&", "&amp;").replace("<", "&lt;")
        licenza = (e.get("dettagli") or {}).get("licenza") or "?"
        pezzi.append(
            "<div class='c' id='%s'><img src='%s'>"
            "<div class='cod'>%s</div><div>%s</div><div class='lic'>%s</div></div>"
            % (codice, ridotta(codice, cache), codice, nome, licenza))
    pezzi.append("</div>")
    out = os.path.join(ART, "foglio_%02d.html" % indice)
    open(out, "w", encoding="utf-8").write("\n".join(pezzi))
    return out


if __name__ == "__main__":
    voci = da_vedere()
    totale = (len(voci) + PER_FOGLIO - 1) // PER_FOGLIO
    print("da guardare: %d ritratti, in %d fogli" % (len(voci), totale))
    cache = {}
    for n in range(totale):
        gruppo = voci[n * PER_FOGLIO:(n + 1) * PER_FOGLIO]
        p = pagina(gruppo, n + 1, totale, cache)
        print("  %s  (%s … %s)  %d kB"
              % (os.path.basename(p), gruppo[0]["codice"], gruppo[-1]["codice"],
                 os.path.getsize(p) // 1024))