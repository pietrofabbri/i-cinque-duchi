"""Genera la pagina per scegliere le immagini degli oggetti (B4).

Legge `dati/lingue/immagini_oggetti.json` (i candidati), `cibi_per_tappa.json`
(luogo e curiosità dei piatti) e `associazioni.json` (le curiosità delle altre
lingue), e scrive `verifica/scelta-immagini.html`. Le miniature sono file a
parte: `miniature.py` le scarica in `verifica/miniature/`, `prepara_pubblicazione.py`
le ricomprime in `verifica/pubblica/miniature/` (l'italiano in `IT-1` … `IT-5`),
e si pubblicano accanto alla pagina come `miniature/<nome>.json`.

La pagina salva le scelte nella collezione `scelte` dell'archivio della
pagina: un documento per voce, con chiave `IT-<anno>-<NN>` per l'italiano e
`<LINGUA>-<NN>` per le altre, e i campi `file` (il file scelto, o null) e
`nessuna` (vero se nessun candidato va bene). `registra_scelte.py` le riporta
in `dati/lingue/attestazione_oggetti.json`.

Uso:  python3 sorgenti/lingue/scelta/genera_pagina.py
"""
import json
import os

RADICE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
D = os.path.join(RADICE, "dati", "lingue")


def chiave(r):
    if r["lingua"] == "IT":
        return "IT-%d-%02d" % (r["anno"], r["numero"])
    return "%s-%02d" % (r["lingua"], r["numero"])


def main():
    with open(os.path.join(D, "immagini_oggetti.json"), encoding="utf-8") as f:
        risultati = json.load(f)["risultati"]
    with open(os.path.join(D, "cibi_per_tappa.json"), encoding="utf-8") as f:
        cibi = {(t["anno"], t["numero"]): t for t in json.load(f)["tappe"]}
    with open(os.path.join(D, "associazioni.json"), encoding="utf-8") as f:
        curio = {a["lingua"]: a.get("curiosita", {}) for a in json.load(f)["associazioni"]}
    voci = []
    for r in risultati:
        if r["lingua"] == "FE":
            continue
        v = {"k": chiave(r), "lingua": r["lingua"], "numero": r["numero"], "voce": r["voce"],
             "candidati": [{k: c.get(k, "") for k in ("file", "licenza", "autore", "data", "url")}
                           for c in r["candidati"]]}
        if r["lingua"] == "IT":
            t = cibi[(r["anno"], r["numero"])]
            v.update(anno=r["anno"], luogo=t["luogo"].replace("`", ""), curiosita=t.get("curiosita", ""))
        else:
            v["curiosita"] = curio.get(r["lingua"], {}).get(r["voce"], "")
        voci.append(v)
    ordine = {"IT": 0, "LA": 1, "EN": 2, "SI": 3, "EL": 4}
    voci.sort(key=lambda v: (ordine[v["lingua"]], v.get("anno", 0), v["numero"]))
    with open(os.path.join(os.path.dirname(__file__), "pagina.tpl.html"), encoding="utf-8") as f:
        html = f.read().replace("/*DATI*/", json.dumps(voci, ensure_ascii=False))
    os.makedirs(os.path.join(RADICE, "verifica"), exist_ok=True)
    with open(os.path.join(RADICE, "verifica", "scelta-immagini.html"), "w", encoding="utf-8") as f:
        f.write(html)
    print(len(voci), "voci,", sum(len(v["candidati"]) for v in voci), "candidati")


if __name__ == "__main__":
    main()
