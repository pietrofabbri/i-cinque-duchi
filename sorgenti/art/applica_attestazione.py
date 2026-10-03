"""Applica `attestazione_immagini.json` a `ritratti_disponibili.json`.

Il principio: **l'attestazione decide, ma non si fida di se stessa.** Ogni nome di
file scritto a mano nella tabella viene riverificato su Commons, e controllata la
licenza. Se un nome non esiste o la licenza non e' libera, la scheda non viene
accettata in silenzio: passa a emblema e lo scrive, cosi' che l'errore resti
visibile invece di diventare un'immagine sbagliata a schermo.

Le schede senza attestazione non vengono toccate, ma perdono la parola `ok` e
diventano `non verificate a vista`: e' la differenza fra un ritratto guardato e
uno soltanto scaricato.
"""
import json
import os
import re
import time
import urllib.parse
import urllib.request
import urllib.error

ART = os.path.dirname(os.path.abspath(__file__))
ESITO = os.path.join(ART, "ritratti_disponibili.json")
ATTESTAZIONE = os.path.join(ART, "attestazione_immagini.json")
UA = "i-cinque-duchi/0.3 (progetto didattico per liceo; pietrofabbri)"

LIB_OK = re.compile(
    r"public domain|pubblico dominio|\bpd\b|cc0|no restrictions|attribution"
    r"|cc[- ]?by(?![a-z])|creative commons", re.I)
LIB_NO = re.compile(r"non[- ]?commercial|fair use|\bcc by[- ]nc|no deriv", re.I)
PREFISSO = re.compile(r"^\d+px-")


LOTTO = 45            # la API ne accetta 50 per richiesta; 45 lascia il margine


def _un_lotto(titoli):
    """Una richiesta a Commons. Restituisce None se la API ha risposto male."""
    corpo = urllib.parse.urlencode({
        "action": "query", "format": "json", "prop": "imageinfo",
        "iiprop": "extmetadata|url|size",
        "titles": "|".join("File:" + t for t in titoli)}).encode()
    for k in range(4):
        try:
            r = urllib.request.Request("https://commons.wikimedia.org/w/api.php",
                                       data=corpo, headers={
                                           "User-Agent": UA,
                                           "Accept": "application/json",
                                           "Content-Type":
                                               "application/x-www-form-urlencoded"})
            with urllib.request.urlopen(r, timeout=60) as f:
                d = json.load(f)
            break
        except urllib.error.HTTPError as e:
            if e.code in (429, 503):
                att = float(e.headers.get("Retry-After") or 0) or 10 * (k + 1)
                print("   %d, attendo %.0f s" % (e.code, att), flush=True)
                time.sleep(att)
                continue
            return None
        except Exception:
            time.sleep(3 * (k + 1))
    else:
        return None
    # Una risposta con `error` o senza `query` **non** significa che i file non
    # esistono. Significa che non abbiamo chiesto bene, e la differenza è
    # enorme: la prima volta che questa funzione ha ricevuto 195 titoli in una
    # sola richiesta, Commons ha risposto `toomanyvalues` con zero pagine, e il
    # codice ha letto quello zero come «il file non esiste»: 127 ritratti giusti
    # sono diventati emblemi senza una sola riga di errore. Per questo qui si
    # interrompe invece di rispondere, e per questo i titoli viaggiano a lotti.
    if d.get("error") or not (d.get("query") or {}).get("pages"):
        return None
    return d


def licenze(titoli):
    """titoli -> dettaglio del file. Attenzione: su Commons i file stanno nello
    spazio `File`, e senza quel prefisso la API cerca pagine e non trova
    `imageinfo`: la risposta arriva, vuota, e sembra che il file non esista."""
    su = {}
    for i in range(0, len(titoli), LOTTO):
        d = _un_lotto(titoli[i:i + LOTTO])
        if d is None:
            return None
        for _, p in d["query"]["pages"].items():
            if "missing" in p:
                continue
            ii = (p.get("imageinfo") or [None])[0]
            if not ii:
                continue
            em = ii.get("extmetadata", {})
            su[p["title"].split(":", 1)[-1].replace("_", " ")] = {
                "licenza": (em.get("LicenseShortName", {}) or {}).get("value", ""),
                "autore": re.sub(r"<[^>]+>", "",
                                 (em.get("Artist", {}) or {}).get("value", ""))[:120],
                "url": ii.get("url"),
                "larghezza": ii.get("width"), "altezza": ii.get("height")}
    return su


if __name__ == "__main__":
    esiti = json.load(open(ESITO, encoding="utf-8"))
    att = json.load(open(ATTESTAZIONE, encoding="utf-8"))
    per_codice = {e["codice"]: e for e in esiti}

    ignora = {k for k in att if k.startswith("_")}
    codici = [k for k in att if k not in ignora]
    ignora_sconosciuti = [k for k in codici if k not in per_codice]
    if ignora_sconosciuti:
        print("ATTENZIONE: codici inesistenti nell'elenco: %s" % ignora_sconosciuti)

    # riverifica tutti i file citati nella tabella, in un'unica richiesta
    citati = []
    for k in codici:
        nome = att[k].get("immagine") or per_codice[k].get("immagine")
        # il REST dei riassunti restituisce il nome della miniatura, con il
        # prefisso di dimensione: quel nome non e' una scheda su Commons
        for prova in (nome, PREFISSO.sub("", nome or "")):
            if prova and prova.replace("_", " ") not in citati:
                citati.append(prova.replace("_", " "))
    print("da riverificare su Commons: %d file" % len(citati))
    su = licenze(citati)
    if su is None:
        raise SystemExit("Interrotto: Commons non ha risposto, o ha risposto male. "
                         "Senza risposta non si decide niente, e decidere 'non "
                         "esiste' sarebbe un falso.")

    accettate = respinte = da_verificare = 0
    problemi = []
    for k in codici:
        a = att[k]
        e = per_codice.get(k)
        if not e:
            continue
        nome = a.get("immagine") or e.get("immagine")
        det = None
        for prova in (nome, PREFISSO.sub("", nome or "")):
            det = su.get((prova or "").replace("_", " "))
            if det:
                nome = prova
                break

        if a["esito"] == "respinta":
            e["immagine"] = None
            e["dettagli"] = None
            e["pagina"] = None
            e["etichetta"] = None
            e["attestato"] = True
            e["motivo"] = "emblema: " + a["motivo"]
            respinte += 1
            continue

        # Il terzo esito: si vede un ritratto, ma non si puo' accertare di chi e'.
        # Non viene accettata in silenzio, perche' un'immagine non verificata
        # diventerebbe a schermo un volto che il gioco non puo' difendere. Resta
        # in elenco con il file e la ragione, e va chiusa prima della consegna.
        if a["esito"] == "da_verificare":
            e["attestato"] = False
            e["verifica"] = "da verificare sui metadati"
            e["motivo"] = "da_verificare: " + a["motivo"]
            if det:
                e["immagine"] = nome
                e["dettagli"] = det
            da_verificare += 1
            continue

        if not det:
            e["attestato"] = True
            e["motivo"] = ("emblema: attestata come accettata, ma il file non e' "
                           "stato trovato su Commons, quindi niente e' stato "
                           "verificato")
            problemi.append((k, a.get("immagine") or e.get("immagine"), "assente"))
            respinte += 1
            continue
        if LIB_NO.search(det["licenza"]) or not LIB_OK.search(det["licenza"]):
            e["motivo"] = "emblema: licenza non libera: " + det["licenza"]
            e["attestato"] = True
            problemi.append((k, nome, det["licenza"]))
            respinte += 1
            continue

        e["immagine"] = nome
        e["dettagli"] = det
        e["etichetta"] = a.get("etichetta")
        e["attestato"] = True
        e["motivo"] = "ok"
        accettate += 1

    # le schede rimaste senza attestazione: non sono sbagliate, ma non sono
    # state guardate, e vanno dichiarate per quello che sono
    non_viste = 0
    for e in esiti:
        if "attestato" in e:
            continue
        e["attestato"] = False
        e["verifica"] = "non verificata a vista"
        if e["motivo"].startswith("ok"):
            non_viste += 1

    with open(ESITO, "w", encoding="utf-8") as f:
        json.dump(esiti, f, ensure_ascii=False, indent=1)

    ritratti = [e for e in esiti if e["motivo"] == "ok"]
    emblemi = [e for e in esiti if e["motivo"].startswith("emblema")
               or "collettivo" in e["motivo"] or "solo emblema" in e["motivo"]]
    visti = [e for e in ritratti if e.get("attestato")]

    print("\naccettate dall'attestazione : %d" % accettate)
    print("respinte a emblema          : %d" % respinte)
    print("da verificare (aperte)      : %d" % da_verificare)
    print("problemi (file assenti o licenza non libera): %d" % len(problemi))
    for k, n, m in problemi:
        print("   %-6s %-52s %s" % (k, str(n)[:52], m))
    print("\ntotale schede                : %d" % len(esiti))
    print("  ritratti autentici         : %d" % len(ritratti))
    print("    di cui guardati a vista  : %d" % len(visti))
    print("    di cui non ancora guardati: %d" % (len(ritratti) - len(visti)))
    print("  ritratti aperti da verificare: %d"
          % sum(1 for e in esiti if str(e.get("motivo", "")).startswith("da_verificare")))
    print("  emblemi                    : %d" % len(emblemi))
    print("  ancora da rivedere         : %d"
          % sum(1 for e in esiti if e["motivo"].startswith("richiesta_fallita")))
