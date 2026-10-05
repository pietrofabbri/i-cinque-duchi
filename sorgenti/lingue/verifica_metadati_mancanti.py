#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""I candidati respinti perché manca l'autore: li dichiara la fonte? M1-M4.

Cinque candidati su 1120 vengono respinti perché non hanno l'autore, e la
domanda giusta non è «manca?» — manca, e si vede — ma **chi non lo mette**.
Sono due risposte opposte:

- **la fonte non lo dichiara**: su Commons la chiave c'è ed è vuota. Nessun
  codice può cambiare la risposta, e il rifiuto è giusto.
- **noi non lo leggiamo**: su Commons la chiave c'è e ha un valore, e il
  nostro estrattore guarda solo `Artist` e `Credit`. Il rifiuto è nostro, e si
  chiude scrivendo.

È successo: quattro file sono di pubblico dominio e non dichiarano nessun
autore, e il quinto — `File:Red wine cap.jpg`, **CC BY 2.0**, dove
l'attribuzione è obbligatoria per legge — dichiara `Attribution: Wollombi` e
veniva respinto lo stesso. Non si risponde a memoria: ogni risposta qui
arriva dalla fonte, e le richieste sono in una cache su disco perché la
ricontrollo non sia una decisione che si prende due volte.

  M1  ogni candidato respinto per l'autore ha una risposta, e la risposta è
      una delle tre classi: la fonte non lo dichiara, noi non lo leggiamo, o
      non verificato
  M2  nessun candidato resta **non verificato** quando la fonte è raggiungibile:
      una classe che non risponde è una risposta mancante
  M3  il file dei risultati è quello che la fonte dice: rigenerarlo cambia
      l'inventario delle chiavi, e l'inventario è nel file
  M4  il conto delle tre classi è quello che il capitolo dichiara

Uso:  python3 sorgenti/lingue/verifica_metadati_mancanti.py
      python3 sorgenti/lingue/verifica_metadati_mancanti.py --ricontrolla
"""
import io
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

RADICE = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))
DATI = os.path.join(RADICE, "dati", "lingue", "immagini_oggetti.json")
ESITO = os.path.join(RADICE, "dati", "lingue", "metadati_mancanti.json")
CACHE = os.path.join(RADICE, "dati", "lingue", "metadati_mancanti_cache.json")
CAPITOLO = os.path.join(RADICE, "docs",
                        "videogioco-5-duchi-lingue-immagini.md")
API = "https://commons.wikimedia.org/w/api.php"
USER_AGENT = ("VerificaOggettiProgetto/1.0 (uso didattico del progetto "
              "«I cinque duchi»)")
# Le tre chiavi in cui un autore può stare. Le prime due sono quelle che il
# generatore leggeva: `Attribution` è la terza, ed è quella che mancava.
CHIAVI = ("Artist", "Credit", "Attribution")
NON_VERIFICATO = "non verificato"
DICHIARATO = (re.compile(r"\*\*(\d+) candidati con l'autore mancante\*\*.*?"
                        r"la fonte non lo dichiara \*\*(\d+)\*\*.*?"
                        r"noi non lo leggevamo \*\*(\d+)\*\*", re.S))


def leggi(path, default=None):
    if not os.path.exists(path):
        return default
    with io.open(path, encoding="utf-8") as f:
        return json.load(f)


def scrivi(path, cosa):
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(json.dumps(cosa, ensure_ascii=False, indent=1, sort_keys=True))
        f.write("\n")


def candidati_senza_autore():
    """I candidati che il generatore ha lasciato senza autore."""
    dati = leggi(DATI)
    if dati is None:
        return []
    senza = []
    for a in dati.get("risultati", []):
        for c in a.get("candidati", []):
            if not c.get("autore"):
                senza.append(c["file"])
    return sorted(senza)


def chiedi(titolo):
    """Che cosa dice la fonte, su questo file. Una richiesta, e la verita'.

    Non si usa un formato comodo: la fonte risponde come risponde, e quello
    che non c'è si vede che non c'è. `Artist` e `Credit` ci sono ma vuoti su
    tutti e cinque i file, ed è la prova che non è un nostro difetto di
    lettura.
    """
    qs = urllib.parse.urlencode({
        "action": "query", "format": "json", "titles": titolo,
        "prop": "imageinfo", "iiprop": "extmetadata|url|size"})
    richiesta = urllib.request.Request(API + "?" + qs, headers={
        "User-Agent": USER_AGENT, "Accept": "application/json"})
    with urllib.request.urlopen(richiesta, timeout=30) as f:
        risposta = json.loads(f.read().decode("utf-8"))
    pagine = risposta.get("query", {}).get("pages", {}) or {}
    if not pagine:
        return {"errore": "la fonte non conosce il file"}
    ii = ((list(pagine.values())[0].get("imageinfo") or [{}])[0])
    meta = ii.get("extmetadata", {}) or {}

    def val(k):
        testo = str((meta.get(k) or {}).get("value", "") or "")
        return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", testo)).strip()

    valori = dict((k, val(k)) for k in CHIAVI)
    con_valore = [k for k in CHIAVI if valori[k]]
    if con_valore:
        classe = "noi non lo leggevamo"
    elif any(k in meta for k in CHIAVI):
        classe = "la fonte non lo dichiara"
    else:
        classe = "la fonte non dichiara la chiave"
    return {
        "classe": classe,
        "chiavi_lette": list(meta),
        "chiavi_con_valore": con_valore,
        "valori": valori,
        "licenza": val("LicenseShortName") or val("License"),
        "dominio_pubblico": val("Copyrighted").strip().lower() != "true",
    }


def ricontrolla():
    """Interroga la fonte per ogni candidato senza autore e scrive l'esito."""
    cache = leggi(CACHE, {}) or {}
    senza = candidati_senza_autore()
    risultati = []
    for titolo in senza:
        if titolo in cache:
            esito = cache[titolo]
        else:
            try:
                esito = chiedi(titolo)
            except Exception as errore:  # noqa: BLE001 - il motivo va scritto
                esito = {"classe": NON_VERIFICATO, "errore": str(errore)}
            cache[titolo] = esito
            time.sleep(0.7)
        risultati.append({"file": titolo, "esito": esito})
    scrivi(CACHE, cache)
    scrivi(ESITO, {"versione": 1,
                   "data": "2026-10-05",
                   "chiavi_legte": list(CHIAVI),
                   "risultati": risultati})
    return risultati


def conta(risultati):
    c = {"noi non lo leggevamo": 0, "la fonte non lo dichiara": 0,
         "la fonte non dichiara la chiave": 0, NON_VERIFICATO: 0}
    for r in risultati:
        classe = r["esito"].get("classe", NON_VERIFICATO)
        c[classe] = c.get(classe, 0) + 1
    return c


def controlla(problemi, risultati=None):
    if risultati is None:
        risultati = leggi(ESITO) or {}
        risultati = risultati.get("risultati", [])
    senza = candidati_senza_autore()
    if len(senza) != len(risultati):
        problemi.append(
            "M1 i candidati senza autore sono %d e gli esiti registrati %d: "
            "ogni candidato respinto ha una risposta, e sono %d/%d"
            % (len(senza), len(risultati), len(risultati), len(senza)))
    c = conta(risultati)

    # ---- M2: nessuna risposta mancasa
    if c.get(NON_VERIFICATO):
        problemi.append(
            "M2 %d candidati non sono verificati: senza rete la classe "
            "giusta non si sa, e un rifiuto che non sa chi lo ha fatto è un "
            "rifiuto che non si può discutere" % c[NON_VERIFICATO])

    # ---- M3: il file è quello che la fonte dice
    salvato = leggi(ESITO)
    if salvato is not None:
        if salvato.get("chiavi_legte") != list(CHIAVI):
            problemi.append(
                "M3 il file registra le chiavi %s e il controllo ne legge %s"
                % (salvato.get("chiavi_legte"), list(CHIAVI)))

    # ---- M4: il conto è quello dichiarato dal capitolo
    capitolo = io.open(CAPITOLO, encoding="utf-8").read()
    m = DICHIARATO.search(capitolo)
    if m is None:
        problemi.append(
            "M4 il capitolo non dichiara la riga dei candidati con l'autore "
            "mancante: i tre conti non hanno con cosa essere confrontati")
    else:
        totale = int(m.group(1))
        fonte = int(m.group(2))
        nostro = int(m.group(3))
        if fonte + nostro != totale:
            problemi.append(
                "M4 il capitolo dichiara %d candidati, %d per la fonte e %d "
                "per noi: %d non fa %d"
                % (totale, fonte, nostro, fonte + nostro, totale))
        if nostro != c.get("noi non lo leggevamo", 0):
            problemi.append(
                "M4 il capitolo dichiara %d rifiuti nostri, la fonte ne "
                "conferma %d" % (nostro, c.get("noi non lo leggevamo", 0)))
        if fonte != (c.get("la fonte non lo dichiara", 0)
                     + c.get("la fonte non dichiara la chiave", 0)):
            problemi.append(
                "M4 il capitolo dichiara %d rifiuti della fonte, la fonte ne "
                "conferma %d"
                % (fonte, c.get("la fonte non lo dichiara", 0)
                   + c.get("la fonte non dichiara la chiave", 0)))
    return c


def main():
    if "--ricontrolla" in sys.argv:
        risultati = ricontrolla()
        c = conta(risultati)
        print("ricontrollati %d candidati su Commons" % len(risultati))
        for r in risultati:
            print("  %-46s %s" % (r["file"][:46], r["esito"].get("classe")))
        print("noi non lo leggevamo: %d, la fonte: %d, non verificati: %d"
              % (c.get("noi non lo leggevamo", 0),
                 c.get("la fonte non lo dichiara", 0)
                 + c.get("la fonte non dichiara la chiave", 0),
                 c.get(NON_VERIFICATO, 0)))
        return 0

    risultati = (leggi(ESITO) or {}).get("risultati", [])
    problemi = []
    c = controlla(problemi, risultati)
    print("== M1-M4. i candidati respinti per l'autore, e chi non lo mette")
    print("   candidati senza autore: %d" % len(candidati_senza_autore()))
    print("   noi non lo leggevamo: %d, la fonte non lo dichiara: %d, "
          "non verificati: %d"
          % (c.get("noi non lo leggevamo", 0),
             c.get("la fonte non lo dichiara", 0)
             + c.get("la fonte non dichiara la chiave", 0),
             c.get(NON_VERIFICATO, 0)))
    for r in risultati:
        e = r["esito"]
        print("   %-46s %s%s" % (r["file"][:46], e.get("classe"),
                                 (" [%s]" % ",".join(e.get("valori_k", []) or
                                                     e.get("chiavi_con_valore",
                                                           [])))
                                 if e.get("chiavi_con_valore") else ""))
    if problemi:
        for p in problemi:
            print("   difetto %s" % p)
    else:
        print("   ogni candidato respinto ha una risposta dalla fonte, e i "
              "tre conti sono quelli che il capitolo dichiara")
    return 1 if problemi else 0


if __name__ == "__main__":
    sys.exit(main())
