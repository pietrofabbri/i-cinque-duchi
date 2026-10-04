"""Costruisce `dati/immagini_gioco.json`: il catalogo unico che il motore legge.

**Perché un catalogo e non la tabella della ricerca.** `ritratti_disponibili.json`
ha una riga per **tappa**, cioè per codice, e li ci sono cinque personaggi che
compaiono in due anni diversi con lo stesso file: Copernico, Augusto, Alfonso I,
Lucrezia Borgia, l'Ariosto, e per la ricerca sono sei righe e sei immagini da
scaricare, mentre il gioco ne ha bisogno di cinque. Indicizzando per **persona**
quel difetto sparisce da solo, e l'elenco delle tappe in cui la persona compare
diventa un dato (`usata_in`) invece di una copia.

**Perché ogni ritratto porta `esito` e `etichetta`.** Il gioco mostra un volto a
un ragazzo di tredici anni: se non sa che quel volto è una miniatura del Duecento,
l'insegnamento che ne ricava è sbagliato. Per questo l'etichetta non è una nota
di archivio, è parte del dato che il motore legge.

**Perché le respinte diventano emblemi e non spariscono.** Una scheda senza
immagine è un buco a schermo: il gioco deve poter dire «di costui non abbiamo un
volto, e perché». L'emblema è una risposta, non un'assenza.

Uso:
    python3 sorgenti/art/catalogo_immagini.py            # scrive il catalogo
    python3 sorgenti/art/catalogo_immagini.py --solo     # non scrive i file
"""
import json
import os
import shutil
import subprocess
import tempfile

import emblema

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ART = os.path.join(BASE, "sorgenti", "art")
OUT = os.path.join(ART, "out")
ESITO = os.path.join(ART, "ritratti_disponibili.json")
ATTEST = os.path.join(ART, "attestazione_immagini.json")
CATALOGO = os.path.join(BASE, "dati", "immagini_gioco.json")

LATO, ALTEZZA = 48, 54

# Le tre schede che sono la **stessa persona** sotto due nomi. Non e' una
# lista di preferenze: sono tre casi in cui il catalogo aveva due voci e un
# solo file, e lo ha detto il controllo 7 di `verifica_immagini.py` contando gli
# sha256 (138 file distinti su 141 ritratti). Il difetto e' nato da
# `chiave_persona`, che ripulisce il nome ma non sa che «Ottaviano Augusto» e
# «Augusto» sono lo stesso uomo: la normalizzazione e' testuale, e l'identita'
# non e' una questione di testo.
#
# Non si e' cercata una regola che trovasse questi tre da sola: una regola che
# unisce due nomi perche' uno contiene l'altro avrebbe unito anche
# «il territorio del Po» e «i Bersaglieri del Po», che sono due persone diverse.
# Qui si dichiarano i tre, e il controllo 7 continua a sorvegliarli: se un
# quarto doppione compare, il controllo roscola e non lo lascia passare.
ALIAS = {
    "ottaviano augusto": "augusto",
    "niccolò copernico": "copernico",
    "federico ii di svevia": "federico ii",
}


def chiave_persona(e):
    """Il nome ripulito: due schede della stessa persona devono cadere insieme."""
    n = e["nome"].strip().lower()
    for pegg in (" *", "*", " (", "("):
        n = n.split(pegg)[0].strip()
    return ALIAS.get(n, n)


# La tessera dell'emblema **non e' piu' qui**. Fino al 3 ottobre stava qui,
# dentro questa funzione, e produceva un rettangolo con una diagonale il cui
# seme era `sum(ord(codice)) % 22`: i sessanta emblemi erano **diciotto file**,
# e dieci persone ne avevano uno identico. Ora e' in `emblema.py`, che
# classifica il motivo in una delle sette famiglie dichiarate e ci scrive dentro
# il segno della famiglia, le iniziali e la firma.


def ricostruisci(codice):
    """Ricostruisce la tessera 48x54 di un codice dal grezzo, con `sips`.

    Il ritratto finito si faceva con PIL, che non e' installato: la riduzione la
    fa `sips`, che c'e' nel sistema. **Il taglio e' diverso da quello automatico**:
    qui si ritaglia il centro del grezzo in proporzione 48:54 e si riduce, mentre
    il taglio automatico cercava il viso. Per dieci tessere la differenza si
    vede e va dichiarata; per le altre centoquindici resta il taglio giusto.
    """
    src = os.path.join(ART, "ritratti_grezzi", codice + ".img")
    if not os.path.exists(src):
        return False
    con = tempfile.mkdtemp(prefix="tessera_")
    try:
        medio = os.path.join(con, "medio.jpg")
        ritagliato = os.path.join(con, "ritagliato.png")
        piccolo = os.path.join(con, "piccolo.png")
        subprocess.run(["sips", "-Z", "400", src, "--out", medio],
                       capture_output=True, check=False)
        # si ritaglia il centro in 8:9, che e' la proporzione di 48x54
        subprocess.run(["sips", "-c", "450", "400", medio, "--out", ritagliato],
                       capture_output=True, check=False)
        subprocess.run(["sips", "-z", str(ALTEZZA), str(LATO), ritagliato,
                        "-s", "format", "png", "--out",
                        os.path.join(OUT, "ritratto_%s.png" % codice)],
                       capture_output=True, check=False)
        return os.path.exists(os.path.join(OUT, "ritratto_%s.png" % codice))
    finally:
        shutil.rmtree(con, ignore_errors=True)


def main(solo_esecuzione=False):
    esiti = json.load(open(ESITO, encoding="utf-8"))
    att = json.load(open(ATTEST, encoding="utf-8"))

    # le giudicazioni contano piu' del file scaricato: vanno unite qui dentro,
    # altrimenti il catalogo direbbe «ritratto» per un'immagine respinta
    persone = {}
    for e in esiti:
        codice = e["codice"]
        voce = {k: v for k, v in e.items() if k != "codice"}
        giudizio = att.get(codice)
        if giudizio and giudizio.get("esito") == "respinta":
            voce["immagine"] = None
            voce["dettagli"] = None
            voce["etichetta"] = None
            voce["esito"] = "emblema"
            voce["motivo"] = "emblema: " + giudizio["motivo"]
        elif giudizio and giudizio.get("esito") == "da_verificare":
            voce["motivo"] = "da verificare: " + giudizio["motivo"]
            voce["esito"] = "da_verificare"
            # il file c'e' e resta, ma in un campo che dice che non e' stato
            # deciso: se stesse in `dettagli` sembrerebbe un ritratto approvato
            voce["dettagli_non_verificati"] = voce.pop("dettagli", None)
        else:
            voce["esito"] = "ritratto" if e.get("motivo") == "ok" else "emblema"

        nome = chiave_persona(e)
        p = persone.setdefault(nome, {
            "nome": e["nome"], "anni": [], "usata_in": [],
            "file": e.get("immagine"),
            "dettagli": voce.get("dettagli") or None,
            "dettagli_non_verificati": voce.get("dettagli_non_verificati"),
            "etichetta": voce.get("etichetta"),
            "esito": voce["esito"], "motivo": voce["motivo"],
            "tipo": e.get("tipo"), "vivo": bool(e.get("vivo")),
        })
        if codice not in p["usata_in"]:
            p["usata_in"].append(codice)
        if e.get("anno") not in p["anni"]:
            p["anni"].append(e.get("anno"))
        # il ritratto e' della persona: se due schede hanno esiti diversi, la
        # piu' severa vince, e il conflitto si dichiara invece di sciogliersi
        if voce["esito"] == "emblema" and p["esito"] == "ritratto":
            p["esito"] = "emblema"
            p["motivo"] = voce["motivo"]
            p["file"] = None
            p["dettagli"] = None
            p["etichetta"] = None
        elif voce["esito"] == "da_verificare" and p["esito"] == "ritratto":
            p["esito"] = "da_verificare"
            p["motivo"] = voce["motivo"]

    catalogo = {}
    senza_file = []
    ricostruite = []
    for nome in sorted(persone):
        p = persone[nome]
        p["usata_in"] = sorted(p["usata_in"])
        p["anni"] = sorted(p["anni"])
        p.pop("file", None)
        if p["esito"] == "ritratto":
            # Quale dei codici sopravvive? Non si sceglie a mano: si sceglie
            # quello il cui file c'e' davvero. Cinque persone compaiono in due
            # anni, i duplicati sono stati cancellati, e il primo codice in
            # ordine non e' per forza quello che ha ancora la tessera: sceglierlo
            # a caso produceva un catalogo che prometteva un file inesistente.
            vivi = [c for c in p["usata_in"]
                    if os.path.exists(os.path.join(OUT, "ritratto_%s.png" % c))]
            if not vivi and not solo_esecuzione:
                for c in p["usata_in"]:
                    if ricostruisci(c):
                        vivi = [c]
                        ricostruite.append((nome, c))
                        break
            if not vivi:
                senza_file.append(nome)
                p["immagine"] = None
            else:
                p["immagine"] = "sorgenti/art/out/ritratto_%s.png" % vivi[0]
        else:
            p["immagine"] = "sorgenti/art/out/emblema_%s.png" % p["usata_in"][0]
        catalogo[nome] = p

    if solo_esecuzione:
        n = {}
        for p in catalogo.values():
            n[p["esito"]] = n.get(p["esito"], 0) + 1
        print("persone: %d  %s" % (len(catalogo), n))
        return catalogo

    scritti = 0
    cancellati = 0
    for p in catalogo.values():
        if p["esito"] == "ritratto":
            continue
        codice = p["usata_in"][0]
        # La famiglia la calcola `emblema.py` **dal motivo**, e la stessa
        # funzione disegna: non si scrive qui, perche' un catalogo che
        # dichiara una famiglia e un disegno che ne dichiara un'altra e' la
        # stessa bugia del controllo che non guarda.
        png, famiglia, parola = emblema.tessera(p, BASE)
        p["emblema_famiglia"] = famiglia
        p["emblema_famiglia_da"] = parola
        with open(os.path.join(OUT, "emblema_%s.png" % codice), "wb") as f:
            f.write(png)
        scritti += 1
        # Le tessere del ritratto respinto non devono restare in giro, e si
        # cancellano per **tutti** i codici della persona, non solo per il primo:
        # altrimenti la copia dell'anno due resta in `out/` accanto all'emblema,
        # e un'immagine respinta lasciata li' finisce prima o poi a schermo.
        for c in p["usata_in"]:
            vecchio = os.path.join(OUT, "ritratto_%s.png" % c)
            if os.path.exists(vecchio):
                os.remove(vecchio)
                cancellati += 1

    # Il catalogo si scrive **qui, una volta sola, e dopo** che le tessere
    # sono state disegnate: deve dire la famiglia che il disegno porta davvero,
    # e l'unico modo per non sbagliare e' scrivere dopo averla calcolata. Fino
    # al 3 ottobre c'erano tre scritture identiche dello stesso file, con due
    # testi `_nota` diversi (uno dei quali diceva «cinque personaggi», un numero
    # che non era piu' vero da giorni): la terza vinceva e le prime due non
    # servivano a nulla. Non e' un difetto visibile — il risultato era quello
    # giusto — ma un file scritto tre volte con due contraddizioni in mezzo e'
    # un posto dove il prossimo scrive la riga sbagliata e non se ne accorge.
    with open(CATALOGO, "w", encoding="utf-8") as f:
        json.dump({"_nota":
                   "Catalogo unico delle immagini del gioco, indicizzato per "
                   "persona e non per tappa: dodici persone compaiono in due anni "
                   "e hanno un solo file. Ogni voce porta l'esito e l'etichetta, "
                   "cosi' il gioco non mostra un volto senza dire che cos'e'. Le "
                   "voci `da_verificare` non hanno un ritratto: hanno un emblema e "
                   "il file in attesa, finche' non si verifica di chi e'. Ogni "
                   "emblema porta `emblema_famiglia` e `emblema_famiglia_da`: la "
                   "famiglia dice **perche'** qui non c'e' un volto, e `da` dice "
                   "quale parola del motivo l'ha fatta vincere.",
                   "_generato_da": "sorgenti/art/catalogo_immagini.py",
                   "persone": catalogo}, f, ensure_ascii=False, indent=1)
        f.write("\n")

    for p in catalogo.values():
        if p["esito"] != "ritratto" or not p["immagine"]:
            continue
        for c in p["usata_in"]:
            dup = os.path.join(OUT, "ritratto_%s.png" % c)
            if os.path.basename(p["immagine"]) == os.path.basename(dup):
                continue
            if os.path.exists(dup):
                os.remove(dup)
                cancellati += 1

    # Gli orfani si cercano tutti, non solo i `ritratto_`. Una persona che passa
    # da aperta a ritratto conserva la sua vecchia tessera d'emblema, e quella
    # resta in `out/` accanto a quella nuova: sei file che nessuno usa e che il
    # primo che li apre ritrova come se fosse un ritratto respinto ancora valido.
    citate = {os.path.basename(p["immagine"]) for p in catalogo.values()
              if p["immagine"]}
    orfani = 0
    for nome_file in sorted(os.listdir(OUT)):
        if nome_file.endswith(".png") and nome_file not in citate:
            os.remove(os.path.join(OUT, nome_file))
            orfani += 1

    n = {}
    for p in catalogo.values():
        n[p["esito"]] = n.get(p["esito"], 0) + 1
    print("persone nel catalogo: %d  %s" % (len(catalogo), n))
    print("tessere orfane cancellate: %d" % orfani)
    print("tessere d'emblema scritte: %d" % scritti)
    print("tessere duplicate cancellate: %d" % cancellati)
    print("tessere ricostruite dal grezzo: %d %s"
          % (len(ricostruite), [c for _, c in ricostruite]))
    if senza_file:
        print("PERSONE SENZA FILE: %d -> %s" % (len(senza_file), senza_file[:10]))
    print("catalogo: %s" % os.path.relpath(CATALOGO, BASE))


if __name__ == "__main__":
    import sys
    main(solo_esecuzione="--solo" in sys.argv)