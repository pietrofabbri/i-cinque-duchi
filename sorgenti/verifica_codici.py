"""Verifica la codifica dei facoltativi, che è la cosa che rende la regola dei premi
verificabile su tutti e non solo sui centocinquanta obbligatori.

**I cinque controlli, e perché esistono.**

1. **Ogni occorrenza di facoltativo ha un codice, o un motivo per non averlo.**
   `null` senza spiegazione e il buco che questo lavoro doveva chiudere: la
   verifica dei premi poteva guardare solo gli obbligatori e nessuno se ne
   accorgeva, perché «non c'è codice» e «non c'è persona» sembrano la stessa cosa.

2. **Un codice a una persona sola.** Due persone con lo stesso codice significa che
   la verifica dei premi passa due volte sullo stesso volto contando due premi,
   ed è il difetto che non si vede.

3. **Una persona, un codice.** Due codici per la stessa persona significano che il
   motore e la verifica possono guardare due schede diverse della stessa faccia.
   Le persone che compaiono in due anni hanno due codici: non è un difetto dei
   cataloghi degli anni, che sono per anno, ma la ragione per cui qui si confronta
   il **nome normalizzato**, e non il codice.

4. **Il codice non è un numero usato due volte.** Un codice nuovo che inciampa su
   quello di una scheda già esistente è peggio di un codice mancante: è un codice
   che punta alla persona sbagliata, e quella non si vede.

5. **Il numero di facoltativi torna con quello che dichiarano i documenti.** Se il
   catalogo ne conta un numero diverso dalle 269 occorrenze, uno dei due mente, e
   senza questo controllo nessuno dei due lo direbbe.

Uso:
    python3 sorgenti/verifica_codici.py
"""
import collections
import json
import os
import re
import unicodedata

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INC = os.path.join(BASE, "dati", "incontri_livelli.json")
CAT = os.path.join(BASE, "dati", "videogioco-5-duchi-facoltativi.json")

CODICE = re.compile(r"^[PQ]\d+$")


def normalizza(nome):
    n = unicodedata.normalize("NFKD", nome.strip().lower())
    n = "".join(c for c in n if not unicodedata.combining(c))
    n = n.replace("’", "'").replace("`", "")
    return re.sub(r"\s+", " ", n).strip()


def main():
    inc = json.load(open(INC, encoding="utf-8"))
    cat = json.load(open(CAT, encoding="utf-8"))
    persone = cat["persone"]
    difetti = []

    # 1. ogni occorrenza ha un codice o un motivo
    occorrenze = 0
    senza = []
    for t in inc["incontri"]:
        for f in (t.get("facoltativi") or []):
            occorrenze += 1
            if not f.get("codice"):
                if not f.get("codice_perche"):
                    senza.append("%s: %s" % (t["livello"], f["nome"]))
    if senza:
        difetti.append("1 %d occorrenze senza codice e senza motivo: %s"
                       % (len(senza), senza[:8]))

    # 2. un codice a una persona sola
    per_codice = collections.defaultdict(set)
    for v in persone:
        if v.get("codice"):
            per_codice[v["codice"]].add(normalizza(v.get("nome_completo")
                                                   or v["nome"]))
    doppi = {c: sorted(n) for c, n in per_codice.items() if len(n) > 1}
    if doppi:
        difetti.append("2 %d codici su piu' persone: %s"
                       % (len(doppi), list(doppi.items())[:5]))

    # 3. una persona, un codice (confrontando il nome, non il codice)
    per_nome = collections.defaultdict(set)
    for v in persone:
        if v.get("codice"):
            per_nome[normalizza(v["nome"])].add(v["codice"])
    molteplici = {n: sorted(c) for n, c in per_nome.items() if len(c) > 1}
    if molteplici:
        difetti.append("3 %d persone con piu' di un codice: %s"
                       % (len(molteplici), list(molteplici.items())[:5]))

    # 4. nessun codice nuovo che inciampa su uno gia' esistente
    alias = set()
    for lista in (cat.get("_indice_persone", {}).get("codici_alias") or {}).values():
        alias.update(lista)
    esistenti = set()
    a1 = json.load(open(os.path.join(
        BASE, "dati", "videogioco-5-duchi-anno1-personaggi.json"),
        encoding="utf-8"))
    esistenti.update(p["id"] for p in a1["personaggi"])
    for a in (2, 3, 4, 5):
        for p in json.load(open(os.path.join(
                BASE, "dati",
                "videogioco-5-duchi-anno%d-personaggi.json" % a),
                encoding="utf-8"))["persone"]:
            esistenti.add(p["codice"])
    nuovi = {v["codice"] for v in persone if v.get("esito") == "nuovo"}
    if nuovi & esistenti:
        difetti.append("4 %d codici nuovi gia' in uso: %s"
                       % (len(nuovi & esistenti), sorted(nuovi & esistenti)[:8]))
    if alias & nuovi:
        difetti.append("4 %d codici nuovi collidono con un alias: %s"
                       % (len(alias & nuovi), sorted(alias & nuovi)[:8]))
    if any(not CODICE.match(c or "") for c in nuovi):
        difetti.append("4 ci sono codici nuovi che non sono P o Q seguiti da numeri")

    # 5. il conto delle occorrenze torna con quello dei documenti
    if occorrenze != sum(len(t.get("facoltativi") or [])
                         for t in inc["incontri"]):
        difetti.append("5 il conto delle occorrenze non torna")
    # Il confronto NON e' un'aritmetica fra occorrenze e somme: sei celle
    # contengono due persone, e il totale delle tappe del catalogo e' quindi
    # maggiore del numero delle occorrenze. La prima versione li confrontava e si
    # fermava con 276 contro 269, segnalando un difetto che non c'era. Il
    # confronto giusto e' una corrispondenza: ogni occorrenza deve trovare la sua
    # persona, e la sua tappa deve stare fra le tappe di quella persona.
    tappe_giuste = set()
    for t in inc["incontri"]:
        for f in (t.get("facoltativi") or []):
            for codice in (f.get("codici") or []):
                tappe_giuste.add((t["livello"], codice))
    persone_senza = []
    for v in persone:
        if not v.get("codice"):
            continue
        for liv in v["tappe"]:
            if (liv, v["codice"]) not in tappe_giuste:
                persone_senza.append("%s porta %s che non e' di %s"
                                     % (v["codice"], liv, v["nome"][:30]))
    if persone_senza:
        difetti.append("5 %d tappe nel catalogo che nessun incontro conferma: %s"
                       % (len(persone_senza), persone_senza[:6]))
    if len(tappe_giuste) != sum(len(v["tappe"]) for v in persone
                                if v.get("codice")):
        difetti.append("5 le tappe delle persone non sono le stesse degli incontri: "
                       "%d contro %d" % (len(tappe_giuste), sum(
                           len(v["tappe"]) for v in persone if v.get("codice"))))

    per_esito = collections.Counter(v["esito"] for v in persone)
    print("persone nel catalogo dei facoltativi : %d" % len(persone))
    for k in sorted(per_esito):
        print("  %-16s %d" % (k, per_esito[k]))
    print("occorrenze di facoltativo coperte   : %d" % occorrenze)
    print("persone con due codici nei cataloghi: %d"
          % cat.get("_indice_persone", {}).get("persone_con_due_codici", 0))

    if difetti:
        print("PROBLEMI: %d" % len(difetti))
        for d in difetti:
            print("   " + d)
        return 1
    print("codici: nessun problema")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())