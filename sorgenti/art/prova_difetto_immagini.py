"""Prova che `verifica_immagini.py` morda, con difetti iniettati uno alla volta.

Un controllo che non si e' mai visto sbagliare non e' un controllo: e' un
documento che dice «tutto va bene». Qui si rompono le cose apposta, una per una,
e si pretende che il verificatore se ne accorga; poi si rimette tutto com'era e si
richiede che torni verde. I difetti provati sono quelli reali capitati, non quelli
che si immaginano.

**La prova scrive sul file vero e lo rimette.** Una prima versione copiava il
catalogo, gli iniettava il difetto e si fermava li': tre dei cinque difetti non
erano visti, non perche' il verificatore dormisse, ma perche' la prova guardava
un file che nessuno leggeva. Il sintomo — «la prova e' fallita» senza che nulla
fosse rotto — e' il tipo di cosa che questo progetto si permette di trattare come
un difetto del metodo, non della prova: **una prova che non osserva nulla non ha
nessun valore, e il suo fallimento va letto come un difetto della prova**.

Uso:
    python3 sorgenti/art/prova_difetto_immagini.py
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CATALOGO = os.path.join(BASE, "dati", "immagini_gioco.json")
OUT = os.path.join(BASE, "sorgenti", "art", "out")
VERIFICA = os.path.join(BASE, "sorgenti", "art", "verifica_immagini.py")


def gira():
    r = subprocess.run([sys.executable, VERIFICA], capture_output=True, text=True)
    return r.returncode, r.stdout


def leggi():
    return json.load(open(CATALOGO, encoding="utf-8"))


def scrivi(cat):
    with open(CATALOGO, "w", encoding="utf-8") as f:
        json.dump(cat, f, ensure_ascii=False, indent=1)
        f.write("\n")


def persona_di(esito):
    cat = leggi()
    for n, p in cat["persone"].items():
        if p["esito"] == esito:
            return n
    raise SystemExit("nessuna persona con esito %r" % esito)


def main():
    codice, testo = gira()
    if codice != 0:
        raise SystemExit("il verificatore non e' verde prima di cominciare:\n" + testo)
    print("prima della prova: verde")

    # il backup vive fuori dal progetto: se la prova muore, il catalogo resta
    backup = tempfile.mkdtemp(prefix="prova_immagini_")
    copia = os.path.join(backup, "catalogo.json")
    shutil.copy(CATALOGO, copia)
    provati = []

    def inietta(nome, cosa):
        cat = leggi()
        cosa(cat)
        scrivi(cat)
        provati.append((nome, gira()))
        shutil.copy(copia, CATALOGO)      # subito ripristinato

    ritratto = persona_di("ritratto")
    emblema = persona_di("emblema")

    # Il terzo difetto ha bisogno di una persona **aperta**, e il 3 ottobre le
    # aperte sono state chiuse tutte: la prima versione della prova chiedeva
    # `persona_di("da_verificare")` e moriva con «nessuna persona». Una prova
    # che funziona solo finche' esiste un caso, non e' una prova del caso: e' una
    # prova del calendario. Il caso quindi **si costruisce**, partendo da un
    # ritratto e togliendogli la decisione.
    aperto = ritratto

    # difetto 1: il catalogo promette un file che non c'e'. E' successo davvero:
    # il catalogo sceglieva il primo codice in ordine e non quello che aveva
    # ancora la tessera, e prometteva nove file inesistenti.
    def d1(cat):
        cat["persone"][ritratto]["immagine"] = "sorgenti/art/out/ritratto_NON_ESISTE.png"
    inietta("file annunciato e assente", d1)

    # difetto 2: un'immagine respinta lasciata in out/ accanto all'emblema.
    # E' successo davvero, con un francobollo e con una medaglia di bitcoin.
    def d2(cat):
        p = cat["persone"][emblema]
        shutil.copy(os.path.join(BASE, p["immagine"]),
                    os.path.join(OUT, "ritratto_%s.png" % p["usata_in"][0]))
    inietta("immagine respinta lasciata in out/", d2)
    os.remove(os.path.join(OUT, "ritratto_%s.png"
                           % leggi()["persone"][emblema]["usata_in"][0]))

    # difetto 3: un ritratto senza etichetta. Il gioco mostrerebbe un volto senza
    # dire se e' una fotografia o una miniatura, ed e' l'insegnamento sbagliato.
    def d3(cat):
        cat["persone"][ritratto]["etichetta"] = None
    inietta("ritratto senza etichetta", d3)

    # difetto 4: un aperto che porta i dettagli nel campo di un deciso, cioe'
    # sembra approvato a chi legge il dato. Il caso non deve dipendere da una
    # persona reale che sia aperta in questo momento.
    def d4(cat):
        p = cat["persone"][aperto]
        p["esito"] = "da_verificare"
        p["dettagli_non_verificati"] = p.pop("dettagli", None)
        p["dettagli"] = p["dettagli_non_verificati"]
        # anche l'etichetta sparisce: un aperto non e' un ritratto, e lasciare
        # l'etichetta avrebbe fatto mordere il controllo sbagliato, che e' peggio
        # di non far mordere niente: sembra che il difetto sia stato visto
        p["etichetta"] = None
    inietta("aperto con i dettagli di un deciso", d4)

    # difetto 5: una tessera di ritratto che non e' un PNG
    def d5(cat):
        tessera = os.path.join(BASE, cat["persone"][ritratto]["immagine"])
        shutil.copy(tessera, os.path.join(backup, "vera.png"))
        open(tessera, "wb").write(b"non e' un PNG")
    inietta("tessera che non e' un PNG", d5)
    shutil.copy(os.path.join(backup, "vera.png"),
                os.path.join(BASE, leggi()["persone"][ritratto]["immagine"]))

    # difetto 6: una tappa che dal catalogo e' sparita
    def d6(cat):
        cat["persone"][ritratto]["usata_in"] = []
    inietta("tappa sparita dal catalogo", d6)

    shutil.rmtree(backup, ignore_errors=True)

    falliti = []
    for titolo, (codice, testo) in provati:
        primo = ""
        for riga in testo.splitlines():
            if riga.startswith("   "):
                primo = riga.strip()
                break
        if codice == 0:
            falliti.append(titolo)
            print("NON MORDE  %-40s" % titolo)
        else:
            print("morde      %-40s  %s" % (titolo, primo[:66]))

    codice, testo = gira()
    if falliti or codice != 0:
        raise SystemExit("la prova e' fallita")
    print("dopo la prova: verde, e tutti i difetti iniettati erano visti")


if __name__ == "__main__":
    main()