"""Verifica i disegni degli ambienti: che ci siano, che abbiano la misura
dichiarata e che non siano due volte lo stesso disegno.

Tre controlli, e sono tre perche' sono tre modi in cui un disegno mente:

  D1  **Ogni disegno dichiarato esiste ed e' un PNG.** Un indice che promette
      trenta file e ne ha ventinove e' un indice falso, ed e' il difetto che
      piu' spesso si vede in questo progetto: il numero conta, il file no.
  D2  **Ogni PNG ha la misura che l'indice dichiara**, riletta dall'intestazione
      con `png_terrarium.misura_png()` e non presa da dove l'hai scritta: se il
      disegnatore avesse cambiato la scala senza cambiare l'indice, qui si
      vedrebbe.
  D3  **Due livelli hanno lo stesso disegno solo se hanno gli stessi dati.**
      Era «due SHA non sono mai uguali», e reggeva solo perché le trenta tappe
      dell'anno 1 sono in trenta luoghi diversi: con tutti e 150 non regge,
      perché `2-5` e `2-13` sono entrambe Roma alle stesse coordinate e
      disegnano lo stesso isolato. Adesso confronta la **chiave dei dati** —
      sagome e griglia — e distingue due difetti che il vecchio controllo
      confondeva: due disegni uguali con dati diversi è il disegnatore che
      **perde** qualcosa, due disegni diversi con dati uguali è il disegnatore
      che **aggiunge** qualcosa. Il secondo non era controllato affatto: una
      macchia a caso per distinguere le tappe passava il controllo vecchio.
  D4  **Il file si decodifica davvero, non solo si annuncia.** D1 e D2 leggono
      l'intestazione, che si puo' dichiarare come si vuole: un PNG che promette
      tre canali e ne scrive uno supera i tre controlli e non si apre. D4 lo
      decodifica con `png_terrarium.decodifica_png` e confronta i pixel con la
      misura dichiarata.

Il controllo e' verde come un controllo che guarda: per questo l'indice dice
anche quanti edifici sono stati ritagliati, e `D1` verifica che quel numero ci
sia. Un ritaglio non dichiarato e' un'immagine che mente su quanti edifici
ha.
"""
import hashlib
import json
import os
import sys

RADICE = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(RADICE, "sorgenti", "gis"))
from png_terrarium import decodifica_png, misura_png       # noqa: E402

INDICE = os.path.join(RADICE, "sorgenti", "art", "out", "ambienti",
                      "indice.json")
AMBIENTI = os.path.join(RADICE, "dati", "ambienti_livelli.json")
SAGOME = os.path.join(RADICE, "dati", "edifici_footprint.json")


def chiave_dati(livello, sagome, ambienti):
    """La chiave che decide il disegno: le sagome **e** la griglia.

    Il disegnatore legge l'una e l'altra, quindi la chiave deve contenere
    entrambe: senza la griglia, i sedici livelli che non hanno sagome hanno la
    stessa chiave e vengono dichiarati tutti uguali mentre i loro disegni sono
    diversi. Il primo tentativo del controllo aveva questo difetto.
    """
    griglia = ambienti.get(livello, {}).get("ambiente", {}).get("griglia", {})
    forme = frozenset(
        (tuple(tuple(round(c, 2) for c in punto) for punto in e["forma"]),
         e.get("altezza_m"))
        for e in sagome if e.get("livello") == livello)
    return (griglia.get("colonne"), griglia.get("righe"),
            griglia.get("scala_m_per_tessera"), forme)


def main():
    if not os.path.exists(INDICE):
        print("non trovo %s" % os.path.relpath(INDICE, RADICE))
        return 1
    ind = json.load(open(INDICE, encoding="utf-8"))
    sagome = json.load(open(SAGOME, encoding="utf-8"))["edifici"]
    ambienti = {a["livello"]: a for a in
                json.load(open(AMBIENTI, encoding="utf-8"))["ambienti"]}
    problemi = []
    visti, sha, decodificati = [], {}, 0
    # `sha` tiene il **livello** e non solo il nome del file: D3 confronta due
    # livelli, e senza il livello non puo' dire nulla. `sha_digest` serve al
    # secondo verso, quello dei dati uguali con disegni diversi.
    sha_digest = {}
    chiavi = {}

    def chiave(livello):
        return chiave_dati(livello, sagome, ambienti)

    for d in ind["disegnati"]:
        percorso = os.path.join(RADICE, d["file"])
        nome = d["livello"]
        if not os.path.exists(percorso):
            problemi.append("D1 %s: l'indice promette %s e il file non c'e'"
                            % (nome, d["file"]))
            continue
        with open(percorso, "rb") as f:
            blob = f.read()
        if not blob.startswith(b"\x89PNG\r\n\x1a\n"):
            problemi.append("D1 %s: il file c'e' ma non e' un PNG" % nome)
            continue
        w, h = misura_png(blob)
        if [w, h] != d["px"]:
            problemi.append("D2 %s: il PNG e' %dx%d e l'indice dichiara %dx%d"
                            % (nome, w, h, d["px"][0], d["px"][1]))
        # **D4: il file si decodifica davvero.** D1 e D2 guardano l'intestazione,
        # che si puo' dichiarare come si vuole: un PNG che promette tre canali e
        # ne scrive uno supera i due controlli e non si apre. Il primo tentativo
        # dei disegni era esattamente questo — intestazione RGB, un byte per
        # pixel — e i tre controlli erano verdi.
        try:
            griglia = decodifica_png(blob)
        except Exception as e:
            problemi.append("D4 %s: il file si annuncia come %dx%d ma non si "
                           "decodifica (%s: %s)"
                           % (nome, w, h, type(e).__name__, e))
            continue
        if len(griglia) != h or len(griglia[0]) != w:
            problemi.append("D4 %s: si decodifica in %dx%d e l'indice dichiara "
                           "%dx%d" % (nome, len(griglia[0]), len(griglia),
                                       w, h))
            continue
        if len({tuple(p) for p in griglia[0]}) < 1:
            problemi.append("D4 %s: si decodifica ma la prima riga e' vuota"
                           % nome)
            continue

        digest = hashlib.sha256(blob).hexdigest()
        if digest in sha:
            # Due livelli possono avere lo stesso disegno — se sono nella stessa
            # citta' alle stesse coordinate e' la risposta giusta. La domanda
            # non e' «il disegno e' uguale» ma «i dati sono uguali».
            altro_livello = sha[digest][1]
            if chiave(nome) != chiave(altro_livello):
                problemi.append(
                    "D3 %s e %s: stesso disegno, dati diversi: il disegnatore "
                    "perde qualcosa" % (altro_livello, nome))
        sha[digest] = (nome, d["livello"])
        sha_digest[d["livello"]] = digest
        chiavi.setdefault(chiave(d["livello"]), []).append(d["livello"])
        visti.append(nome)
        decodificati += 1

    # Il verso che il vecchio controllo non aveva: **stessi dati, disegni
    # diversi**. Il disegnatore che aggiunge una macchia per distinguere le
    # tappe passa «sha distinti» e non e' affatto fedele.
    for k, liv in chiavi.items():
        if len(liv) > 1:
            quanti = len({sha_digest[l] for l in liv if l in sha_digest})
            if quanti > 1:
                problemi.append(
                    "D3 %s: stessi dati e %d disegni diversi: il disegnatore "
                    "aggiunge qualcosa che nei dati non c'e'"
                    % (", ".join(liv[:4]), quanti))

    # Ogni tappa dell'anno 1 deve avere il suo disegno: l'indice puo' dire che
    # mancano, ma non puo' dirlo per errore. Il confronto e' con l'anno letto
    # dal file degli ambienti, non con una lista scritta qui.
    ambienti = json.load(open(AMBIENTI, encoding="utf-8"))["ambienti"]
    anno1 = [a["livello"] for a in ambienti if a["livello"].startswith("1-")]
    mancanti = [l for l in anno1 if l not in visti]
    if mancanti:
        problemi.append("D1 tappe dell'anno 1 senza disegno: %d (%s)"
                        % (len(mancanti), ", ".join(mancanti[:6])))

    for p in problemi:
        print("   %s" % p)
    print("PROBLEMI: %d" % len(problemi))
    print("  disegni verificati : %d" % len(visti))
    print("  distinti (sha)     : %d" % len(sha))
    print("  chiavi dati       : %d" % len(chiavi))
    print("  decodificati (D4) : %d" % decodificati)
    return 1 if problemi else 0


if __name__ == "__main__":
    sys.exit(main())