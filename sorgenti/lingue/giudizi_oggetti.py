"""Registra i giudizi a vista sugli oggetti e li applica all'attestazione.

**Chi guarda e chi scrive sono due persone diverse, ed è dichiarato.** Le
immagini le ha guardate Pietro sui fogli di `fogli_oggetti.py`; questo file
prende i suoi giudizi, li **controlla** e li scrive nell'attestazione. Non
sceglie: mette in fila quello che è stato deciso guardando, e si ferma se un
giudizio non regge.

Il progetto vieta che una scelta entri senza un **motivo di giudizio**
(`lingue-immagini.md` §3): qui il motivo è **obbligatorio** e non può essere una
parola sola. Un `motivo` di due lettere è un file compilato a macchetta, ed è
la stessa forma del difetto del carattere che il font non aveva.

I quattro esiti:
  accettato   il file scelto, con la sua categoria e la sua etichetta
  respinto    il file è guardato e non va bene: il motivo dice perché
  nessuna     la voce non ha immagine, e il motivo dice perché

Uso:
    python3 sorgenti/lingue/giudizi_oggetti.py              # applica
    python3 sorgenti/lingue/giudizi_oggetti.py --controlla  # non scrive
"""
import io
import json
import os
import sys
import time

BASE = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(BASE, "..", ".."))
PRIMO = os.path.join(RADICE, "dati", "lingue", "immagini_oggetti.json")
SECONDO = os.path.join(RADICE, "dati", "lingue", "immagini_2.json")
GIUDIZI = os.path.join(RADICE, "dati", "lingue", "giudizi_oggetti.json")
ATTESTAZIONE = os.path.join(RADICE, "dati", "lingue",
                            "attestazione_oggetti.json")

ETICHETTE = ("fotografia", "immagine_d_archivio", "dipinto", "incisione",
             "miniatura", "rilievo", "partitura", "frammento_antico",
             "immagine_tratteggiata")
CATEGORIE = ("foto", "dipinto", "stampa", "nessuna")
ESITI = ("accettato", "respinto", "nessuna")
LINGUE = ("IT", "FE", "LA", "EN", "SI", "EL")

# Un motivo di due parole non è un motivo di giudizio: è un campo compilato.
MOTIVO_MINIMO = 25


def voci_note():
    note = {}
    for percorso in (PRIMO, SECONDO):
        if not os.path.exists(percorso):
            continue
        with open(percorso, encoding="utf-8") as f:
            for r in json.load(f)["risultati"]:
                note.setdefault((r["lingua"], r["voce"]), []).extend(
                    c["file"] for c in r["candidati"])
    return note


def controlla(giudizi, note, problemi):
    visti = set()
    for g in giudizi:
        chiave = (g.get("lingua"), g.get("voce"))
        dove = "la voce %s %s" % chiave
        if chiave not in note:
            problemi.append("%s: non è una voce del progetto" % dove)
            continue
        if chiave in visti:
            problemi.append("%s: due giudizi sulla stessa voce" % dove)
        visti.add(chiave)
        esito = g.get("esito")
        if esito not in ESITI:
            problemi.append("%s: l'esito è %r, che non è fra %s"
                            % (dove, esito, ", ".join(ESITI)))
        motivo = (g.get("motivo") or "").strip()
        if len(motivo) < MOTIVO_MINIMO:
            problemi.append("%s: il motivo ha %d caratteri e ne servono %d: "
                            "un motivo troppo corto è un campo compilato"
                            % (dove, len(motivo), MOTIVO_MINIMO))
        if esito == "accettato":
            if g.get("file") not in note[chiave]:
                problemi.append("%s: il file %r non è fra i candidati di "
                                "quella voce: la scelta è fatta su un file "
                                "che non si è guardato"
                                % (dove, g.get("file")))
            if g.get("categoria") not in CATEGORIE:
                problemi.append("%s: la categoria è %r, che non è fra %s"
                                % (dove, g.get("categoria"), ", ".join(CATEGORIE)))
            if g.get("etichetta") not in ETICHETTE:
                problemi.append("%s: l'etichetta è %r, che non è fra le nove"
                                % (dove, g.get("etichetta")))
        if esito == "nessuna" and g.get("categoria"):
            problemi.append("%s: esito «nessuna» e categoria %r insieme: "
                            "l'etichetta è di un'immagine che non c'è"
                            % (dove, g.get("categoria")))
    return visti


def applica(giudizi):
    note = voci_note()
    with open(PRIMO, encoding="utf-8") as f:
        primo = json.load(f)["risultati"]
    secondi = {}
    if os.path.exists(SECONDO):
        with open(SECONDO, encoding="utf-8") as f:
            for r in json.load(f)["risultati"]:
                secondi[(r["lingua"], r["voce"])] = r

    scelte = []
    for g in giudizi:
        chiave = (g["lingua"], g["voce"])
        r2 = secondi.get(chiave)
        r1 = next((r for r in primo
                   if (r["lingua"], r["voce"]) == chiave), {})
        scelte.append({
            "lingua": g["lingua"], "numero": g.get("numero"),
            "voce": g["voce"],
            "esito": g["esito"],
            "file": g.get("file"),
            "categoria": g.get("categoria"),
            "etichetta": g.get("etichetta"),
            "motivo": (g.get("motivo") or "").strip(),
            "guardato_a_vista": True,
            "guardato_il": g.get("guardato_il", "04/10/2026"),
            "giro_candidati": 2 if (r2 and r2["candidati"]) else 1,
        })

    attestazione = {
        "versione": 2,
        "data": time.strftime("%Y-%m-%d"),
        "stato": "%d voci su 180 attestate a vista" % len(scelte),
        "nota": "Ogni riga e' un giudizio di una persona che ha guardato "
                "l'immagine sul foglio di controllo. Il motivo e' obbligatorio "
                "e non vuoto: una riga senza motivo di giudizio non entra.",
        "campi": {
            "lingua": ", ".join(LINGUE),
            "numero": "da 1 a 30, il numero della voce in associazioni.json",
            "esito": "accettato, respinto, nessuna",
            "file": "il nome del file su Commons, con il prefisso File:, e "
                    "solo se e' fra i candidati della voce",
            "categoria": ", ".join(CATEGORIE),
            "etichetta": ", ".join(ETICHETTE),
            "motivo": "perché questa immagine e non un'altra, o perché non ce "
                      "n'è: almeno %d caratteri" % MOTIVO_MINIMO,
        },
        "scelte": scelte,
    }
    with open(ATTESTAZIONE, "w", encoding="utf-8") as f:
        json.dump(attestazione, f, ensure_ascii=False, indent=1)
    conta = {}
    for s in scelte:
        conta[s["esito"]] = conta.get(s["esito"], 0) + 1
    return conta, len(note)


def main():
    solo = "--controlla" in sys.argv
    if not os.path.exists(GIUDIZI):
        print("manca %s: nessun giudizio da registrare" % os.path.relpath(
            GIUDIZI, RADICE))
        return 2
    with open(GIUDIZI, encoding="utf-8") as f:
        giudizi = json.load(f)["giudizi"]
    note = voci_note()
    problemi = []
    visti = controlla(giudizi, note, problemi)
    print("== giudizi a vista sugli oggetti")
    print("   giudizi: %d su %d voci del progetto" % (len(giudizi), len(note)))
    if problemi:
        for p in problemi:
            print("   difetto %s" % p)
        print("   %d difetti: niente e' stato scritto" % len(problemi))
        return 1
    print("   tutti i giudizi reggono: voce del progetto, esito dichiarato, "
          "motivo di almeno %d caratteri, file fra i candidati" % MOTIVO_MINIMO)
    if solo:
        return 0
    conta, tot = applica(giudizi)
    print("   scritta l'attestazione: %s" % conta)
    print("   voci ancora senza giudizio: %d" % (len(note) - len(visti)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
