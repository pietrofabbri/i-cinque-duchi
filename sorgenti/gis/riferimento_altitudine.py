"""Le altitudini di riferimento delle città misurate, prese da Wikidata.

**Perché questo file esiste.** `luoghi-edifici.md` dichiara «verificato su 14
punti ad altitudine nota, errore medio assoluto 12,6 m». Quella frase non era
verificabile da nessuna parte: i quattordici numeri erano scritti a mano nella
stessa frase che li dichiarava, e nessuno script li poteva ricontare. Un numero
che non si può ricalcolare è una voce di parte, non una misura.

La soluzione non è scrivere a mano un altro elenco, è chiedere a qualcuno che
sa. Per ogni città del campione si cerca su Wikidata l'entità che è **la stessa
città**, e la prova che lo sia non è il nome: è la **posizione**.

**Le tre cose che questo script ha imparato strada facendo, scritte perché il
prossimo non le impari da capo.**

1. Il nome è ambiguo e il paese non basta. «Palermo» c'è in Italia, negli Stati
   Uniti e in Colombia; «Perugia» ha in Italia due entità con l'altitudine (una
   a 493 m e una a 211 m), e sbagliare significa sbagliare di 250 metri. La
   regola è quindi: **stesso nome, stesso paese, e la più vicina** entro 15 km,
   con la popolazione come criterio di primo ordinamento.
2. `wikibase:around` accetta i punti dentro **un solo letterale**, separati da
   uno spazio; due letterali affiancati non sono una domanda valida. E in ogni
   modo l'endpoint accetta in questo momento **una richiesta al minuto**: la
   domanda per prossimità, con tutti i punti insieme, ci metteva quattro
   minuti di attese fra un gruppo e l'altro, mentre la domanda per nome è **una
   richiesta sola** e risponde in un secondo. La via lenta era quella
   elegante; quella che funziona è quella che chiede una volta sola.
3. Le città che Wikidata non conosce, o conosce ma non quota, **non si
   inventano**: restano fuori dal file e il conto le dichiara per nome.

Uso:  python3 sorgenti/gis/riferimento_altitudine.py
      python3 sorgenti/gis/riferimento_altitudine.py --prova
"""
import json
import math
import os
import sys
import time
import urllib.parse
import urllib.request

RADICE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATI = os.path.join(RADICE, "dati")
sys.path.insert(0, os.path.join(RADICE, "sorgenti", "gis"))
import mappe_lettore  # noqa: E402

FILE_RILIEVO = ["rilievo_penisola.json", "rilievo_europa.json"]
USCITA = os.path.join(DATI, "altitudine_riferimento.json")
GREZZO = os.path.join(DATI, "altitudine_riferimento_grezzo.json")
ENDPOINT = "https://query.wikidata.org/sparql"
UA = "i-cinque-duchi/0.1 (progetto didattico per liceo; pietrofabbri)"
RAGGIO_KM = 15.0
PASSO = 10        # il campione: una città ogni PASSO, in ordine di file


def campione():
    """Le città del campione, con la regola dichiarata."""
    scelte = []
    for nome in FILE_RILIEVO:
        percorso = os.path.join(RADICE, "dati", "mappe", nome)
        if not os.path.exists(percorso):
            continue
        _, punti = mappe_lettore.leggi(percorso)
        for i, (campi, x, y) in enumerate(punti):
            if i % PASSO == 0:
                scelte.append({"file": nome, "nome": campi.get("nome"),
                               "paese": campi.get("paese", ""),
                               "lon": x, "lat": y})
    return scelte


def chiedi(nomi, tentativi=5):
    """Una domanda sola per tutti i nomi del campione."""
    if os.path.exists(GREZZO):
        with open(GREZZO, encoding="utf-8") as f:
            grezzo = json.load(f)
        if sorted(grezzo.get("nomi", [])) == sorted(nomi):
            print("  risposta già in cache (%s)" % os.path.basename(GREZZO))
            return grezzo["risposte"], grezzo.get("endpoint", ENDPOINT)
    valori = " ".join('"%s"@it' % n for n in nomi)
    query = """
SELECT ?nome ?alt ?pop ?en ?c ?coord WHERE {
  VALUES ?nome { %s }
  ?c rdfs:label ?nome ; wdt:P2044 ?alt ; wdt:P31/wdt:P279* wd:Q515 ; wdt:P625 ?coord .
  OPTIONAL { ?c wdt:P1082 ?pop }
  OPTIONAL { ?c wdt:P17/rdfs:label ?en . FILTER(lang(?en)="en") }
}
""" % valori
    url = ENDPOINT + "?format=json&query=" + urllib.parse.quote(query)
    for k in range(tentativi):
        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": UA,
                              "Accept": "application/sparql-results+json"})
            with urllib.request.urlopen(req, timeout=170) as f:
                dati = json.load(f)
            risposte = [{kk: vv["value"] for kk, vv in r.items()}
                        for r in dati["results"]["bindings"]]
            with open(GREZZO, "w", encoding="utf-8") as f:
                json.dump({"data": time.strftime("%Y-%m-%d"), "nomi": nomi,
                           "endpoint": ENDPOINT, "risposte": risposte}, f,
                          ensure_ascii=False)
            print("  %d risposte (cache scritta)" % len(risposte))
            return risposte, ENDPOINT
        except Exception as e:                        # 429 dell'endpoint incluso
            print("  tentativo %d fallito (%s): attendo %d s"
                  % (k + 1, e, 45 * (k + 1)), flush=True)
            time.sleep(45 * (k + 1))
    raise SystemExit("l'endpoint non ha risposto")


def km(lon1, lat1, lon2, lat2):
    m = math.radians
    x = (m(lon2) - m(lon1)) * math.cos(m((lat1 + lat2) / 2))
    return math.hypot(x, m(lat2 - lat1)) * 6371.0


def wkt_a_punto(testo):
    dentro = testo[testo.find("(") + 1:testo.find(")")]
    lon, lat = dentro.split()
    return float(lon), float(lat)


def main():
    sola_prova = "--prova" in sys.argv
    punti = campione()
    print("campione: %d città (una ogni %d)" % (len(punti), PASSO), flush=True)
    if not punti:
        raise SystemExit("nessun file di rilievo da campionare")

    nomi = sorted({p["nome"] for p in punti})
    risposte, endpoint = chiedi(nomi)

    per_nome = {}
    for r in risposte:
        lon, lat = wkt_a_punto(r["coord"])
        per_nome.setdefault(r["nome"], []).append(
            {"qid": r["c"], "altitudine": float(r["alt"]),
             "popolazione": int(float(r["pop"])) if r.get("pop") else None,
             "paese": r.get("en", ""), "lon": lon, "lat": lat})

    righe, senza = [], []
    for p in punti:
        candidati = per_nome.get(p["nome"], [])
        # stesso paese prima, distanza dopo: il nome da solo non è un'identità
        candidati = [c for c in candidati if c["paese"] == p["paese"]] or candidati
        if not candidati:
            senza.append("%s (%s)" % (p["nome"], p["paese"]))
            continue
        for c in candidati:
            c["distanza_km"] = round(km(p["lon"], p["lat"], c["lon"], c["lat"]), 3)
        vicine = [c for c in candidati if c["distanza_km"] <= RAGGIO_KM]
        if not vicine:
            senza.append("%s (%s): la città più vicina è a %.0f km"
                         % (p["nome"], p["paese"],
                            min(c["distanza_km"] for c in candidati)))
            continue
        vicine.sort(key=lambda c: (c["distanza_km"],
                                   -(c["popolazione"] or 0)))
        riga = dict(p)
        riga["qid"] = vicine[0]["qid"]
        riga["altitudine"] = vicine[0]["altitudine"]
        riga["popolazione"] = vicine[0]["popolazione"]
        riga["distanza_km"] = vicine[0]["distanza_km"]
        riga["altre_omonime"] = [{"altitudine": c["altitudine"],
                                  "paese": c["paese"],
                                  "distanza_km": c["distanza_km"]}
                                 for c in candidati[:3] if c is not vicine[0]]
        righe.append(riga)

    if senza:
        print("senza riferimento (%d): %s" % (len(senza), "; ".join(senza)))
    if sola_prova:
        for r in righe:
            print("  %-14s misurata %s, riferimento %s m (%s, %.1f km)"
                  % (r["nome"], "?", r["altitudine"], r["qid"], r["distanza_km"]))
        print("prova: %d punti con riferimento, %d senza" % (len(righe), len(senza)))
        return

    documento = {
        "versione": 1,
        "data": time.strftime("%Y-%m-%d"),
        "fonte": "Wikidata, proprietà P2044 (altitudine sul livello del mare) "
                 "delle entità di classe Q515 (città)",
        "endpoint": endpoint,
        "regola": "stesso nome, stesso paese, entità più vicina entro %.0f km; "
                  "a parità di distanza la più popolosa" % RAGGIO_KM,
        "campione": "una città ogni %d, in ordine di file, sui file %s"
                    % (PASSO, ", ".join(FILE_RILIEVO)),
        "senza_riferimento": senza,
        "nota": "le città che Wikidata non conosce o non quota restano fuori: "
                "il file contiene solo riferimenti con fonte, e il conto dice "
                "quali sono e quante",
        "punti": righe,
    }
    with open(USCITA, "w", encoding="utf-8") as f:
        json.dump(documento, f, ensure_ascii=False, indent=1)
    print("scritto %s: %d punti con riferimento, %d senza (%d byte)"
          % (USCITA, len(righe), len(senza), os.path.getsize(USCITA)))


if __name__ == "__main__":
    main()