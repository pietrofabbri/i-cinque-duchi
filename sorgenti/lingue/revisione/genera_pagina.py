"""Genera la pagina di revisione delle voci degli oggetti (B2): dati/lingue/associazioni.json, cibi_per_tappa.json e segnalazioni_voci.json
dentro pagina.tpl.html, in verifica/revisione-voci.html (non nel ramo). La pagina pubblicata salva le scelte nella collezione `revisione`."""
import json, io, sys
import os
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..") + "/"
S = R + "sorgenti/lingue/revisione/"
a = json.load(open(R + "dati/lingue/associazioni.json"))["associazioni"]
seg = json.load(open(R + "dati/lingue/segnalazioni_voci.json"))
ordine = ["IT", "FE", "LA", "EN", "SI", "EL"]
lingue = []
for sig in ordine:
    x = next(v for v in a if v["lingua"] == sig)
    s = seg.get(sig, {})
    for k in s: assert k in x["voci"], (sig, k)
    if sig == "IT":
        c = json.load(open(R + "dati/lingue/cibi_per_tappa.json"))["tappe"]
        lingue.append({"sig": sig, "nome": x["nome"], "oggetto": "un piatto tipico per ogni luogo", "motivo": x.get("motivo", ""),
                       "voci": [{"n": t["numero"], "anno": t["anno"], "luogo": t["luogo"], "v": t["piatto"] or "(da proporre)", "s": t["segnalazione"]} for t in c]})
        continue
    lingue.append({"sig": sig, "nome": x["nome"], "oggetto": x["oggetto"], "motivo": x.get("motivo", ""),
                   "voci": [{"n": i + 1, "v": v, "s": s.get(v, "")} for i, v in enumerate(x["voci"])]})
os.makedirs(R + "verifica", exist_ok=True)
html = io.open(S + "pagina.tpl.html", encoding="utf-8").read().replace("/*DATI*/", json.dumps(lingue, ensure_ascii=False))
io.open(R + "verifica/revisione-voci.html", "w", encoding="utf-8").write(html)
print(sum(len(l["voci"]) for l in lingue), sum(1 for l in lingue for v in l["voci"] if v["s"]))
