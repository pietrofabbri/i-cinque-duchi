#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prova che `verifica_inventario_mappe.py` morda, con difetti iniettati.

Un controllo che non si è mai visto sbagliare non è un controllo: è un
documento che dice «tutto va bene». Qui si rompono le cose apposta, una per una,
e si pretende che il verificatore se ne accorga; poi si rimette tutto com'era e si
richiede che torni verde.

**I difetti provati sono quelli capitati il 04/10/2026**, non quelli che si
immaginano: i quattro documenti che parlano di `dati/mappe/` avevano dato quattro
numeri diversi (19, 21, 23, 25), `AGENTS.md` elencava dentro la cartella il file
che il giorno prima l'aveva fatta crashare, e nessun file di dati diceva da dove
viene. Qui si iniettano tutti e quattro più i casi che il controllo deve coprire
e che non sono ancora capitati.

**La prova lavora su una copia.** Il manifest e i documenti sono letti da
percorsi reali, e scriverci sopra per provare il verificatore significherebbe
lasciare il repository in uno stato inventato se la prova morisse a metà. La copia
è di `dati/mappe/` (i file sono 1,5 MB: sono piccoli), del manifest e dei quattro
documenti. Il controllo accetta `--radice`.

Uso:
    python3 sorgenti/gis/prova_difetto_mappe_manifest.py
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

BASE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    "..", ".."))
VERIFICA = os.path.join(BASE, "sorgenti", "gis", "verifica_inventario_mappe.py")

DOCUMENTI = ("AGENTS.md", "README.md",
             "docs/videogioco-5-duchi-mappe.md",
             "docs/videogioco-5-duchi-fonti-visive.md")


def gira(radice):
    r = subprocess.run([sys.executable, VERIFICA, "--radice", radice],
                       capture_output=True, text=True)
    return r.returncode, r.stdout


def copia_progetto():
    """La copia: `dati/mappe/`, il manifest e i quattro documenti che citano i
    numeri. Anche `dati/mondo_admin1_copertura.json`, perché il controllo I8 lo
    legge: senza, la copia non sarebbe fedele e ogni difetto sotto passerebbe
    per la ragione sbagliata."""
    radice = tempfile.mkdtemp(prefix="prova_mappe_")
    shutil.copytree(os.path.join(BASE, "dati", "mappe"),
                    os.path.join(radice, "dati", "mappe"))
    shutil.copy(os.path.join(BASE, "dati", "mappe_manifest.json"),
                os.path.join(radice, "dati", "mappe_manifest.json"))
    shutil.copy(os.path.join(BASE, "dati", "mondo_admin1_copertura.json"),
                os.path.join(radice, "dati", "mondo_admin1_copertura.json"))
    shutil.copytree(os.path.join(BASE, "docs"), os.path.join(radice, "docs"))
    shutil.copy(os.path.join(BASE, "AGENTS.md"), os.path.join(radice, "AGENTS.md"))
    shutil.copy(os.path.join(BASE, "README.md"), os.path.join(radice, "README.md"))
    return radice


def percorso(radice, nome):
    return os.path.join(radice, nome)


def leggi(radice, nome):
    return open(percorso(radice, nome), encoding="utf-8").read()


def scrivi(radice, nome, testo):
    with open(percorso(radice, nome), "w", encoding="utf-8") as f:
        f.write(testo)


def sostituisci(testo, vecchio, nuovo):
    if testo.count(vecchio) != 1:
        raise SystemExit("la prova cerca «%s» e lo trova %d volte: il difetto che "
                         "doveva iniettare non è più nel documento, e la prova "
                         "passerebbe per la ragione sbagliata"
                         % (vecchio[:60], testo.count(vecchio)))
    return testo.replace(vecchio, nuovo)


def main():
    codice, testo = gira(BASE)
    if codice != 0:
        raise SystemExit("il verificatore non è verde prima di cominciare:\n" + testo)
    print("prima della prova: verde")

    radice = copia_progetto()
    # la copia deve essere fedele: se i file copiati fossero meno, il conto
    # sarebbe un altro e ogni difetto sotto passerebbe senza essere visto
    originali = len(os.listdir(os.path.join(BASE, "dati", "mappe")))
    copiati = len(os.listdir(os.path.join(radice, "dati", "mappe")))
    if originali != copiati:
        raise SystemExit("la copia ha %d file e la cartella %d"
                         % (copiati, originali))

    provati = []

    def difetto(nome, cosa, atteso):
        """Iniettare, pretendere che il verificatore lo dica, rimettere."""
        stato = salva(radice)
        cosa(radice)
        codice, uscita = gira(radice)
        provati.append((nome, codice, atteso, uscita))
        ripristina(radice, stato)

    # 1. il numero copiato a mano che invecchia: il difetto del 04/10, in README
    difetto("il README torna a dichiarare 23 file",
            lambda r: sostituisci_in(r, "README.md", "i 25 file di mappe in",
                                     "i 23 file di mappe in"),
            "README.md dichiara 23")

    # 2. e in AGENTS.md, che era il 21
    difetto("AGENTS.md torna a dichiarare 21 file",
            lambda r: sostituisci_in(r, "AGENTS.md", "`dati/mappe/`**: **25 file**",
                                     "`dati/mappe/`**: **21 file**"),
            "AGENTS.md dichiara 21")

    # 3. il file di copertura torna dentro la cartella: il difetto del 03/10,
    #    pubblicato da un documento invece che vissuto da un crash
    difetto("AGENTS.md rielenca il file di copertura dentro `dati/mappe/`",
            lambda r: sostituisci_in(
                r, "AGENTS.md",
                "il suo conto di copertura è `dati/mondo_admin1_copertura.json`, "
                "che sta in **`dati/` e non in `dati/mappe/`**",
                "più `mondo_admin1_copertura.json`"),
            "elenca `mondo_admin1_copertura.json` dentro")

    # 4. un file nella cartella che il manifest non conosce: il manifest che
    #    enumera 24 file su 25 e resta verde è un manifesto che non coprie
    def file_fantasma(r):
        with open(os.path.join(r, "dati", "mappe", "probe.json"), "w",
                  encoding="utf-8") as f:
            f.write('{"q":100,"f":[],"p":[]}')
    difetto("un file nella cartella che il manifest non elenca", file_fantasma,
            "il manifest e la cartella non elencano gli stessi file")

    # 5. un file che non dichiara la fonte: il difetto che il manifest è nato
    #    per chiudere, e che nessuno poteva vedere perché la fonte stava in un
    #    sorgente Python
    def senza_fonte(r):
        p = os.path.join(r, "dati", "mappe_manifest.json")
        m = json.load(open(p, encoding="utf-8"))
        for riga in m["file"]:
            if riga["categoria"] == "natural_earth":
                riga["fonte"] = "NON DICHIARATA"
                break
        json.dump(m, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    difetto("un file senza fonte dichiarata", senza_fonte,
            "non dichiara da dove viene")

    # 6. e un file la cui categoria non ha un produttore: un file di cui
    #    nessuno risponde
    def senza_produttore(r):
        p = os.path.join(r, "dati", "mappe_manifest.json")
        m = json.load(open(p, encoding="utf-8"))
        del m["produttori"]["rilievo"]
        json.dump(m, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    difetto("una categoria senza produttore dichiarato", senza_produttore,
            "non ha un produttore dichiarato")

    # 7. il peso dichiarato che non è il peso calcolato: «1,5 MB» è un numero
    #    scritto a mano che invecchierà al primo file nuovo
    def peso_falso(r):
        p = os.path.join(r, "dati", "mappe_manifest.json")
        m = json.load(open(p, encoding="utf-8"))
        m["totale"]["byte"] = 1400000
        json.dump(m, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    difetto("il manifest dichiara un peso che i file non hanno", peso_falso,
            "il manifest dichiara 1400000 byte")

    # 8. il conto delle città di un rilievo, che il manifest riconta e il file
    #    dichiara: i due devono dire la stessa cosa
    def citta_smentite(r):
        # Il difetto colpisce il **manifest**, non il file: un manifesto che
        # porta un numero sbagliato è il caso per cui I5 esiste, e la prima
        # stesione della prova cambiava `citta` sul primo rilievo che
        # incontrava — che era quello con il conto giusto, e quindi la prova
        # non rompeva niente. Una prova che colpisce il pezzo sbagliato è verde
        # per la ragione sbagliata.
        p = os.path.join(r, "dati", "mappe_manifest.json")
        m = json.load(open(p, encoding="utf-8"))
        for riga in m["file"]:
            if riga["categoria"] == "rilievo" and riga["file"] == "rilievo_europa.json":
                riga["citta"] = riga["citta"] + 1
                json.dump(m, open(p, "w", encoding="utf-8"), ensure_ascii=False,
                          indent=1)
                return
        raise SystemExit("la prova cerca rilievo_europa.json nel manifest e non "
                         "lo trova: non può iniettare il difetto")
    difetto("il manifest conta più città di quante ne abbia il rilievo",
            citta_smentite, "il manifest conta")

    # 9. e i pin coperti, che sono un dato e non una frase: il documento ne
    #    dichiara un numero diverso da quello del file di copertura
    difetto("AGENTS.md dichiara 53 pin coperti su 54",
            lambda r: sostituisci_in(r, "AGENTS.md", "che coprono **54 pin su 54**",
                                     "che coprono **53 pin su 54**"),
            "AGENTS.md dichiara")

    # 10. il manifest che manca del tutto: senza, nessun file dichiara da dove
    #     viene e i documenti tornano a portare numeri copiati a mano
    difetto("il manifest non c'è più", lambda r: os.remove(
        os.path.join(r, "dati", "mappe_manifest.json")), "manca")

    codice, uscita = gira(radice)
    if codice != 0:
        raise SystemExit("la copia è rimasta sporca dopo dieci difetti:\n" + uscita)
    print("la copia è tornata verde: ogni difetto è stato rimesso")

    falliti = 0
    print("\n%-58s %-6s %s" % ("difetto", "morso", "detto"))
    print("-" * 100)
    for nome, codice, atteso, uscita in provati:
        morso = codice != 0 and atteso in uscita
        print("%-58s %-6s %s" % (nome[:58], "sì" if morso else "NO", atteso))
        if not morso:
            falliti += 1
            print("   il verificatore ha detto:")
            for riga in uscita.splitlines():
                if riga.startswith("  "):
                    print("     " + riga.strip())
    print("-" * 100)
    if falliti:
        print("difetti non visti: %d su %d" % (falliti, len(provati)))
        shutil.rmtree(radice, ignore_errors=True)
        return 1
    print("difetti visti: %d su %d" % (len(provati), len(provati)))
    shutil.rmtree(radice, ignore_errors=True)
    return 0


def salva(radice):
    """Lo stato della copia, per rimetterlo dopo ogni difetto."""
    stato = {}
    for nome in ("dati/mappe_manifest.json", "AGENTS.md", "README.md"):
        stato[nome] = leggi(radice, nome)
    for nome in DOCUMENTI[2:]:
        stato[nome] = leggi(radice, nome)
    stato["_mappe"] = sorted(os.listdir(os.path.join(radice, "dati", "mappe")))
    return stato


def ripristina(radice, stato):
    for nome, testo in stato.items():
        if nome == "_mappe":
            continue
        scrivi(radice, nome, testo)
    cartella = os.path.join(radice, "dati", "mappe")
    for nome in os.listdir(cartella):
        if nome not in stato["_mappe"]:
            os.remove(os.path.join(cartella, nome))


def sostituisci_in(radice, documento, vecchio, nuovo):
    scrivi(radice, documento,
           sostituisci(leggi(radice, documento), vecchio, nuovo))


if __name__ == "__main__":
    sys.exit(main())