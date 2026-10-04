"""Verifica le immagini del gioco: esito, etichetta, licenza, misura, copertura.

Il progetto ha la regola che **un numero scritto a mano invecchia, un numero
calcolato no**, e questa e' la sesta volta che la regola serve. I numeri qui non
sono scritti: sono letti da `dati/immagini_gioco.json` e ricalcolati su quello che
c'e' davvero in `sorgenti/art/out/`.

**I cinque controlli, e perche' ognuno esiste.**

1. **Il file che il catalogo indica deve esistere.** Il motore legge il catalogo e
   apre un file: se il catalogo promette un ritratto e il file non c'e', a
   schermo c'e' un riquadro vuoto e nessuno lo sa. Questo e' il difetto che si
   e' gia' visto nascere: il catalogo e' stato scritto prima che i duplicati
   venissero cancellati, e il conto e' tornato senza che nessuno guardasse.

2. **Il file in `out/` non citato da nessuno e' spazio morto.** Se un'immagine
   respinta resta in `out/` accanto al suo emblema, prima o poi qualcuno la
   riapre e la usa: e' il modo piu' semplice di rimettere in gioco un volto che
   si era giudicato sbagliato.

3. **Ogni ritratto deve avere un'etichetta fra quelle dichiarate.** Il gioco mostra
   il volto a un ragazzo: senza sapere che cos'e' (una miniatura, un'incisione,
   una fotografia) l'insegnamento che ne ricava e' sbagliato. Un'etichetta fuori
   elenco non e' un dettaglio: e' un bug che nessuno vedra' a schermo.

4. **Ogni ritratto deve avere una licenza libera**, riletta dalla tabella, e ogni
   `da_verificare` deve restare **aperto**: sette immagini non ancora decise non
   possono comparire fra i ritratti, perche' un'immagine non verificata a schermo
   e' una bugia che il gioco racconta con il volto di una persona vera.

5. **Ogni codice di tappa deve comparire nel catalogo**, una volta sola per
   persona: e' la copertura. Se un codice sparisce, sparisce una tappa.

6. **Una scheda respinta a vista non puo' comparire come ritratto.**

7. **I file distinti devono essere tanti quanti le persone.** Questo e' il
   controllo che mancava fino al 3 ottobre 2026, e la sua assenza e' la ragione
   per cui sessanta emblemi erano **diciotto file**: tutti e sessanta i PNG
   esistevano, avevano la misura giusta e passavano i controlli, e dieci persone
   avevano lo stesso identico file. Il conto che gli altri controlli facevano
   era sui file, e sessanta file identici a gruppi sono, per un contatore,
   sessanta file giusti. Qui si conta lo **sha256** e si pretende che ogni
   persona abbia un'immagine sua.

   Il difetto si dichiara con i **nomi** delle persone coinvolte: un difetto che
   non si lascia guardare e' un difetto che non si lascia correggere. Ed e' cosi'
   che questo controllo ha trovato, da solo, i tre doppioni fra i ritratti
   (Augusto/Ottaviano Augusto, Copernico/Niccolò Copernico, Federico
   II/Federico II di Svevia): sei voci di catalogo per tre persone.

8. **Ogni emblema dichiara la famiglia e la parola che l'ha fatta vincere**, e
   la famiglia viene **ricalcolata dal motivo**: se il catalogo dicesse una
   famiglia e il motivo un'altra, il gioco mostrerebbe un segno che non spiega
   la frase scritta accanto. E se la parola non sta piu' nel motivo, il
   controllo lo dice invece di passare: una parola sparita e' un controllo che
   non guarda.

Uso:
    python3 sorgenti/art/verifica_immagini.py            # riporta i difetti
    python3 sorgenti/art/verifica_immagini.py --enumero  # stampa i numeri
"""
import glob
import hashlib
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import emblema

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ESITO = os.path.join(BASE, "sorgenti", "art", "ritratti_disponibili.json")
ATTEST = os.path.join(BASE, "sorgenti", "art", "attestazione_immagini.json")
OUT = os.path.join(BASE, "sorgenti", "art", "out")


def trova_catalogo():
    """Il catalogo si cerca, non si scrive: e' l'unico nome che si scrive a mano.

    Qui c'era scritto a mano, e la parola «gioco» era diventata «giogo» in un
    file su due. Il sintomo non era un errore di sintassi ne' un file mancante:
    era un `Errno 2` su un percorso che sembrava giusto, perche' la differenza
    fra `gioco` e `giogo` non si vede. **Un nome scritto a due posti diverge, per
   che' a un posto verra' corretto e all'altro no.** Per questo il catalogo si
    cerca fra i file, e se non se ne trova uno solo il controllo si ferma e lo
    dice invece di andare avanti con un percorso sbagliato.
    """
    candidati = sorted(glob.glob(os.path.join(BASE, "dati", "immagini_gioc*.json")))
    if len(candidati) != 1:
        raise SystemExit(
            "Interrotto: nella cartella dati ci sono %d file che cominciano per "
            "'immagini_gioc', e ne serve uno solo: %s"
            % (len(candidati), [os.path.basename(c) for c in candidati]))
    return candidati[0]


CATALOGO = trova_catalogo()

LATO, ALTEZZA = 48, 54
LIB_OK = re.compile(r"public domain|pubblico dominio|\bpd\b|cc0|no restrictions"
                    r"|attribution|cc[- ]?by(?![a-z])|creative commons", re.I)
LIB_NO = re.compile(r"non[- ]?commercial|fair use|\bcc by[- ]nc|no deriv", re.I)


def dimensione_png(percorso):
    """L'altezza e la larghezza lette dagli 8 byte dell'intestazione PNG.

    Si leggono e non si assumono: un file che non e' un PNG, o che ha una misura
    diversa, non puo' passare per un ritratto solo perche' si chiama cosi'.
    """
    with open(percorso, "rb") as f:
        testa = f.read(24)
    if len(testa) < 24 or testa[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    larghezza = int.from_bytes(testa[16:20], "big")
    altezza = int.from_bytes(testa[20:24], "big")
    return larghezza, altezza


def main(numera=False):
    cat = json.load(open(CATALOGO, encoding="utf-8"))
    persone = cat["persone"]
    esiti = json.load(open(ESITO, encoding="utf-8"))
    att = json.load(open(ATTEST, encoding="utf-8"))
    etichette_dichiarate = set(att.get("_etichette", {})) | {"mummia"}

    difetti = []

    # 1. il file che il catalogo indica deve esistere
    citati = set()
    for nome, p in persone.items():
        rel = p["immagine"]
        citati.add(os.path.basename(rel))
        percorso = os.path.join(BASE, rel)
        if not os.path.exists(percorso):
            difetti.append("1 %s: il catalogo indica %s e il file non c'e'"
                           % (nome, rel))
            continue
        mis = dimensione_png(percorso)
        if mis is None:
            difetti.append("1 %s: %s non e' un PNG" % (nome, rel))
        elif mis != (LATO, ALTEZZA):
            difetti.append("1 %s: %s e' %dx%d e il motore aspetta %dx%d"
                           % (nome, rel, mis[0], mis[1], LATO, ALTEZZA))

    # 2. niente file in out/ che il catalogo non cita
    if os.path.isdir(OUT):
        for nome_file in sorted(os.listdir(OUT)):
            if nome_file.endswith(".img"):
                continue
            if nome_file not in citati:
                difetti.append("2 %s sta in out/ e nessuna persona lo usa"
                               % nome_file)

    # 3. ogni ritratto ha un'etichetta dell'elenco
    for nome, p in persone.items():
        if p["esito"] == "ritratto":
            if not p.get("etichetta"):
                difetti.append("3 %s: ritratto senza etichetta" % nome)
            elif p["etichetta"] not in etichette_dichiarate:
                difetti.append("3 %s: etichetta fuori elenco, %r"
                               % (nome, p["etichetta"]))
        elif p.get("etichetta"):
            difetti.append("3 %s: e' %s e porta l'etichetta %r: un emblema "
                           "non e' un ritratto e non si etichetta come uno"
                           % (nome, p["esito"], p["etichetta"]))

    # 4. licenza libera sui ritratti; gli aperti restano aperti
    for nome, p in persone.items():
        if p["esito"] == "ritratto":
            det = p.get("dettagli") or {}
            lic = det.get("licenza", "")
            if not lic:
                difetti.append("4 %s: ritratto senza licenza registrata" % nome)
            elif LIB_NO.search(lic) or not LIB_OK.search(lic):
                difetti.append("4 %s: licenza non libera: %s" % (nome, lic))
        elif p["esito"] == "da_verificare":
            if p.get("dettagli"):
                difetti.append("4 %s: aperto, ma i dettagli stanno dove stanno "
                               "quelli di un ritratto deciso: sembra approvato"
                               % nome)
            elif not p.get("dettagli_non_verificati"):
                difetti.append("4 %s: aperto e senza nessuna traccia del file: "
                               "si e' perso anche il materiale da verificare"
                               % nome)

    # 5. copertura: ogni codice di tappa deve comparire, una volta sola
    visti = []
    for nome, p in persone.items():
        visti.extend(p["usata_in"])
    attesi = [e["codice"] for e in esiti]
    mancanti = sorted(set(attesi) - set(visti))
    ripetuti = sorted(c for c in set(visti) if visti.count(c) > 1)
    if mancanti:
        difetti.append("5 %d codici di tappa non compaiono in nessuna persona: %s"
                       % (len(mancanti), mancanti[:12]))
    if ripetuti:
        difetti.append("5 %d codici compaiono in due persone: %s"
                       % (len(ripetuti), ripetuti[:12]))

    # nessuna scheda respinta puo' essere finita nel catalogo come ritratto
    for codice, giudizio in att.items():
        if codice.startswith("_") or giudizio.get("esito") != "respinta":
            continue
        for nome, p in persone.items():
            if codice in p["usata_in"] and p["esito"] == "ritratto":
                difetti.append("6 %s e' stata respinta a vista e %scompare "
                               "come ritratto" % (codice, nome))

    # 7. i file distinti devono essere tanti quanti le persone
    for esito in ("ritratto", "emblema"):
        del_file = {}
        for nome, p in persone.items():
            if p["esito"] != esito or not p.get("immagine"):
                continue
            percorso = os.path.join(BASE, p["immagine"])
            if not os.path.exists(percorso):
                continue
            impronta = hashlib.sha256(open(percorso, "rb").read()).hexdigest()
            del_file.setdefault(impronta, []).append(nome)
        attese = sum(1 for p in persone.values() if p["esito"] == esito)
        distinti = len(del_file)
        if distinti != attese:
            raggruppati = sorted((v for v in del_file.values() if len(v) > 1),
                                 key=lambda v: -len(v))
            difetti.append(
                "7 %d %s su %d hanno un'immagine tutta loro: %d file distinti "
                "per %d persone. I doppioni sono %s"
                % (distinti, esito, attese, distinti, attese,
                   "; ".join("= ".join(v) for v in raggruppati[:6])))

    # 8. ogni emblema dichiara la famiglia, e la famiglia viene dal motivo
    for nome, p in persone.items():
        if p["esito"] != "emblema":
            if p.get("emblema_famiglia"):
                difetti.append("8 %s e' un ritratto e porta una famiglia di "
                               "emblema: il dato mente sul esito" % nome)
            continue
        if not p.get("emblema_famiglia") or not p.get("emblema_famiglia_da"):
            difetti.append("8 %s e' un emblema senza `emblema_famiglia`: il "
                           "gioco non sa che cosa dire" % nome)
            continue
        try:
            ricalcolata, parola = emblema.classifica(p["motivo"])
        except emblema.FamigliaNonRiconosciuta:
            difetti.append("8 %s: il motivo non sta in nessuna famiglia "
                           "dichiarata, e il catalogo dice %r"
                           % (nome, p["emblema_famiglia"]))
            continue
        if ricalcolata != p["emblema_famiglia"]:
            difetti.append("8 %s: il catalogo dice %r, il motivo dice %r"
                           % (nome, p["emblema_famiglia"], ricalcolata))
        # La parola da confrontare e' **quella dichiarata**, non quella appena
        # ricalcolata: confrontando la ricalcolata con se stessa il controllo
        # passava qualunque cosa dicesse `emblema_famiglia_da`, ed e' un difetto
        # che la prova dei difetti ha trovato iniettando proprio una parola
        # inesistente. Un campo che nessuno guarda e' un campo che non esiste.
        dichiarata = p["emblema_famiglia_da"]
        if dichiarata not in p["motivo"]:
            difetti.append("8 %s: `emblema_famiglia_da` dice %r e quella parola "
                           "nel motivo non c'e': il controllo sta guardando una "
                           "parola che non c'e'" % (nome, dichiarata))
        elif dichiarata != parola:
            difetti.append("8 %s: il motivo ha fatto vincere %r e il catalogo "
                           "dichiara %r: due parole diverse per la stessa "
                           "famiglia" % (nome, parola, dichiarata))

    if numera:
        per_esito = {}
        for p in persone.values():
            per_esito[p["esito"]] = per_esito.get(p["esito"], 0) + 1
        print("persone          : %d" % len(persone))
        for k in sorted(per_esito):
            print("  %-14s: %d" % (k, per_esito[k]))
        print("tappe coperte    : %d su %d" % (len(set(visti)), len(attesi)))
        print("file in out/     : %d" % len([f for f in os.listdir(OUT)
                                            if f.endswith(".png")]))
        for esito in sorted({p["esito"] for p in persone.values()}):
            impronte = {hashlib.sha256(open(os.path.join(BASE, p["immagine"]),
                                            "rb").read()).hexdigest()
                        for p in persone.values()
                        if p["esito"] == esito and p.get("immagine")
                        and os.path.exists(os.path.join(BASE, p["immagine"]))}
            print("  file distinti %-9s: %d su %d"
                  % (esito, len(impronte),
                     sum(1 for p in persone.values() if p["esito"] == esito)))
        famiglie = {}
        for p in persone.values():
            if p["esito"] == "emblema":
                famiglie[p["emblema_famiglia"]] = \
                    famiglie.get(p["emblema_famiglia"], 0) + 1
        for k in sorted(famiglie):
            print("  %-22s: %d" % (k, famiglie[k]))

    if difetti:
        print("PROBLEMI: %d" % len(difetti))
        for d in difetti:
            print("   " + d)
        return 1
    print("immagini: nessun problema")
    return 0


if __name__ == "__main__":
    sys.exit(main(numera="--enumero" in sys.argv))