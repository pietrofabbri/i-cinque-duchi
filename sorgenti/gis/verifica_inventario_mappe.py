#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Confronta l'inventario di `dati/mappe/` con quello che i documenti dichiarano.

**Il perché, che è la regola del progetto**: un numero scritto a mano invecchia,
un numero calcolato no. `dati/mappe/` è la cartella che cresce di un file ogni
volta che una fonte nuova entra — e il 04/10/2026 ne sono entrati due, i due
`rilievo_*.json`. Al posto di aggiornare i documenti uno per uno, il conteggio si
**calcola** da `dati/mappe_manifest.json` e si confronta con quello che i
documenti dichiarano: un documento che non viene aggiornato smette di essere
verde, e non è più un documento che mente in silenzio.

**I quattro numeri che il 04/10/2026 si contraddicevano**, e che nessuno
controllava:

  `mappe.md`        25   giusto, e dice perché: 19 del 01/10 più `mondo_admin1.json`,
                         i tre `*_altitudine.json` del 03/10 e i due `rilievo_*.json`
                         del 04/10
  `README.md`       23   il conto di prima dei due rilievo, in due posti diversi
  `AGENTS.md`       21   il conto di prima delle altitudini, e dice che
                         `mondo_admin1_copertura.json` sta **in `dati/mappe/`** —
                         che è proprio il file che il 03/10 ha fatto crashare il
                         lettore, spostato in `dati/` e mai tolto da qui
  `fonti-visive.md` 19   giusto **se dice «di Natural Earth»**, che è quello che
                         dice: il numero dei 19 non è il totale della cartella

Uso:
    python3 sorgenti/gis/verifica_inventario_mappe.py
    python3 sorgenti/gis/verifica_inventario_mappe.py --radice /tmp/copia
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mappe_lettore                                     # noqa: E402

RADICE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                      "..", ".."))
if "--radice" in sys.argv:
    # `--radice` serve a `prova_difetto_mappe_manifest.py`, che lavora su una
    # copia: scrivere sui file veri per provare il verificatore lascerebbe il
    # repository in uno stato inventato se la prova morisse a metà.
    RADICE = os.path.abspath(sys.argv[sys.argv.index("--radice") + 1])
MAPPE = os.path.join(RADICE, "dati", "mappe")
MANIFEST = os.path.join(RADICE, "dati", "mappe_manifest.json")

# I documenti che dichiarano un numero, e **la frase** in cui lo dichiarano.
# Ogni voce è (file, espressione, indice del gruppo, che cosa confronta). Le
# espressioni sono volutamente strette: un controllo che legge un numero «per
# caso» in una pagina lunga finisce per confrontare il numero sbagliato e a dare
# un falso allarme, che è il modo più rapido per far spegnere un controllo.
DICHIARANO = [
    ("docs/videogioco-5-duchi-mappe.md",
     r"\*\*(\d+) file di mappe\*\* in formato proprio in `dati/mappe/`", 1, "totale"),
    ("docs/videogioco-5-duchi-mappe.md",
     r"nessun vertice fuori dal mondo, in tutti i (\d+) file", 1, "totale"),
    # nel frontespizio di `mappe.md` il percorso è in testo semplice, non fra
    # backtick: il backtick richiesto faceva fallire la ricerca, e una ricerca
    # che fallisce non e' una ricerca che non trova niente — e' una ricerca che
    # non guarda niente, che è la peggiore delle due
    ("docs/videogioco-5-duchi-mappe.md",
     r"dati/mappe/\*\.json`? \((\d+) file:", 1, "totale"),
    ("docs/videogioco-5-duchi-fonti-visive.md",
     r"I \*\*(\d+) file\*\* di `dati/mappe/` vengono da Natural Earth", 1, "ne"),
    ("docs/videogioco-5-duchi-fonti-visive.md",
     r"\| Fondi geografici già pronti \| \*\*(\d+) file\*\*", 1, "ne"),
    ("docs/videogioco-5-duchi-fonti-visive.md",
     r"\| \*\*Fondi geografici\*\* \| fatto, (\d+) file\b", 1, "ne"),
    ("docs/videogioco-5-duchi-fonti-visive.md",
     r"fondi geografici \((\d+) file Natural Earth", 1, "ne"),
    ("docs/videogioco-5-duchi-fonti-visive.md",
     r"I (\d+) file Natural Earth hanno propriet", 1, "ne"),
    ("README.md", r"i (\d+) file di mappe in `dati/mappe/`", 1, "totale"),
    ("README.md", r"\*\*(\d+) file\*\* in `dati/mappe/` \(1,5 MB\)", 1, "totale"),
# `AGENTS.md` ha due asterischi di troppo dopo il backtick («\`dati/mappe/\`**:
    # **25 file**»): la regex è scritta sul testo **attuale**, non su quello che
    # il testo era quando l'ho scritta per la prima volta. Una regex che
    # smette di corrispondere a una riscrittura non è un controllo che segnala
    # un difetto: è un controllo che tace, e il numero che doveva guardare
    # diventa proprio quello che nessuno guarda. Per questo ogni voce della
    # lista è **provata** da `prova_difetto_mappe_manifest.py`.
    ("AGENTS.md", r"è in `dati/mappe/`\*\*?: \*\*(\d+) file\*\*", 1, "totale"),
]

# Il peso dichiarato nei documenti, in MB con la virgola italiana. Le frasi sono
# strette come le altre, e il confronto ammette ±0,15 MB perche' un documento
# che arrotonda «1,52» a «1,5» o a «1,6» ha detto la verita' approssimata: il
# peso e' l'unico numero
# che cresce a ogni file, ed e' il primo a invecchiare e l'ultimo a essere
# notato, perche' «1,6 MB» resta un numero che sembra giusto.
PESO = [
    ("docs/videogioco-5-duchi-mappe.md", r"per un totale di \*\*([\d,]+) MB\*\*"),
    ("docs/videogioco-5-duchi-fonti-visive.md",
     r"\| Fondi geografici già pronti \| \*\*\d+ file\*\*, ([\d,]+) MB"),
    ("README.md", r"\*\*\d+ file\*\* in `dati/mappe/` \(([\d,]+) MB\)"),
]



def leggi(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def manifest():
    if not os.path.exists(MANIFEST):
        # questo e' un caso speciale, non un problema fra gli altri: senza
        # manifest il file non esiste e il messaggio di `SystemExit` finisce
        # fuori dal canone «problemi: N» che chi chiama lo script si aspetta.
        # Lo si conta lo stesso, perche' il conto dei problemi deve voler dire
        # «questa copia non e' verificabile» e non «non c'e' niente da dire».
        print("problemi: 1")
        print("  manca dati/mappe_manifest.json: rigeneralo con `python3 "
              "sorgenti/gis/mappe_manifest.py`. Senza il manifest nessun file di "
              "dati dichiara da dove viene, e i documenti tornano a portare "
              "numeri copiati a mano")
        raise SystemExit(1)
    return json.load(open(MANIFEST, encoding="utf-8"))


def main():
    m = manifest()
    categorie = m["categorie"]
    totale = m["totale"]["file"]
    ne = categorie["natural_earth"]["file"]

    # I1  il manifest deve parlare di **tutti** i file che ci sono, e non di
    #     qualcuno che non c'è più. Un manifest che enumera 24 file su 25 e
    #     verde è un manifest che non copre la cartella che dichiara di coprire.
    print("== I. il manifest contro la cartella ==")
    su_disco = sorted(os.path.basename(p) for p in
                      os.listdir(MAPPE) if p.endswith(".json"))
    nel_manifest = sorted(r["file"] for r in m["file"])
    problemi = []
    if su_disco != nel_manifest:
        mancanti = sorted(set(su_disco) - set(nel_manifest))
        invecchiati = sorted(set(nel_manifest) - set(su_disco))
        for n in mancanti:
            print("   %s è nella cartella e non nel manifest" % n)
        for n in invecchiati:
            print("   %s è nel manifest e non più nella cartella" % n)

    # I2  ogni file deve dichiarare la sua fonte: un file che non la dichiara
    #     non è «di Natural Earth per default», è un file di provenienza ignota
    senza = [r["file"] for r in m["file"] if r["fonte"] == "NON DICHIARATA"]
    ignoti = [r["file"] for r in m["file"] if r["categoria"] == "non_dichiarata"]

    # I3  e il produttore: un file senza produttore è un file di cui nessuno
    #     risponde. Il produttore si legge dal manifest per categoria.
    senza_produttore = [r["file"] for r in m["file"]
                        if r["categoria"] not in m["produttori"]]

    # I4  il peso dichiarato deve essere il peso calcolato: i byte sono l'unico
    #     numero che il motore deve scaricare, e «1,4 MB» è un numero scritto a
    #     mano che invecchierà al primo file nuovo
    byte_reale = sum(r["byte"] for r in m["file"])
    if m["totale"]["byte"] != byte_reale:
        problemi.append("I4  il manifest dichiara %d byte, i file ne pesano %d"
                        % (m["totale"]["byte"], byte_reale))

    # I5  e i due rilievi: ogni punto **e'** una citta', e il conto deve
    #     tornare con quello che il file contiene davvero. Il numero si rilegge
    #     dal file con il lettore del progetto, non da una chiava del manifest:
    #     un manifesto che porta un numero copiato da sé solo è un manifesto che
    #     può portare un numero sbagliato e non accorgersene.
    for r in m["file"]:
        if r["categoria"] == "rilievo":
            _g, punti = mappe_lettore.leggi(os.path.join(MAPPE, r["file"]))
            if len(punti) != r.get("citta"):
                problemi.append("I5  %s: il manifest conta %s città, il file ne ha %d"
                                % (r["file"], r.get("citta"), len(punti)))

    print("%-16s %5s  %s" % ("categoria", "file", "produttore"))
    for cat in sorted(categorie):
        v = categorie[cat]
        prod = m["produttori"].get(cat, "NESSUNO")
        print("%-16s %5d  %s" % (cat, v["file"], prod.split(" -> ")[-1]))
    print("%-16s %5d  %.2f MB" % ("TOTALE", totale, m["totale"]["megabyte"]))

    # II  i numeri che i documenti dichiarano
    print("\n== II. i numeri che i documenti dichiarano ==")
    print("%-40s %-12s %8s %8s" % ("documento", "che cosa", "dice", "reale"))
    # Il difetto vero di questa prima stesione, e il più subdolo dei tre che
    # questo controllo aveva: **`problemi` veniva riassegnata** qui, a metà del
    # corpo, e l'assegnazione svuotava la lista. I4 e I5 potevano solo
    # scrivervi sopra: nessuno dei due poteva produrre un problema, e nessuno
    # dei due poteva accorgersene, perché il codice che li faceva fallire era
    # esattamente il codice che ne cancellava la traccia. Il sintomo era una
    # prova che iniettava un peso falso e un conteggio di città falso e **non
    # vedeva niente**: la prova che non mordeva indicava il difetto giusto, ma
    # il difetto non era lì. Un controllo che scrive in una lista che qualcuno
    # riassegna è un controllo che scrive nella spazzatura: la lista si
    # dichiara **una volta sola**, in cima.
    if su_disco != nel_manifest:
        problemi.append("I1  il manifest e la cartella non elencano gli stessi file")
    for n in senza:
        problemi.append("I2  %s non dichiara da dove viene" % n)
    for n in ignoti:
        problemi.append("I2  %s è nella categoria «non dichiarata»" % n)
    for n in senza_produttore:
        problemi.append("I3  %s non ha un produttore dichiarato" % n)

    print()
    if m["totale"]["byte"] != byte_reale:
        problemi.append("I4  il manifest dichiara %d byte, i file ne pesano %d"
                        % (m["totale"]["byte"], byte_reale))

    # I4b  e il **peso in MB** dichiarato nei documenti: «1,6 MB» in uno e
    #     «1,4 MB» nell'altro erano due numeri copiati a mano che non coincidevano
    #     fra loro, e il conto dà 1,52. Il peso è il numero che il motore deve
    #     scaricare ed è l'unico che cresce a ogni file: è il primo a invecchiare
    #     e l'ultimo a essere notato, perché «1,6 MB» resta un numero che sembra
    #     giusto. La soglia è ±0,15 MB: sotto quella, il documento ha arrotondato
    #     e non ha sbagliato.
    for percorso, expr in PESO:
        testo = leggi(os.path.join(RADICE, percorso))
        for m2 in re.finditer(expr, testo):
            dichiarato = m2.group(1).replace(",", ".")
            if abs(float(dichiarato) - m["totale"]["megabyte"]) > 0.15:
                problemi.append("I4b %s dichiara %s MB di mappe, i file pesano %.2f MB"
                                % (os.path.basename(percorso), dichiarato,
                                   m["totale"]["megabyte"]))

    for percorso, expr, gruppo, che in DICHIARANO:
        testo = leggi(os.path.join(RADICE, percorso))
        reale = totale if che == "totale" else ne
        for m2 in re.finditer(expr, testo):
            dichiarato = int(m2.group(gruppo))
            nome = os.path.basename(percorso)
            flag = "" if dichiarato == reale else "   <-- non torna"
            print("%-40s %-12s %8d %8d%s"
                  % (nome[:40], che, dichiarato, reale, flag))
            if dichiarato != reale:
                problemi.append("I6  %s dichiara %d (%s), il conto dà %d"
                                % (nome, dichiarato, che, reale))
        # «non contiene più la frase» si confronta con le **trovate**, non con
        # `re.search`: una riga che contiene la frase non è una riga che non la
        # contiene. La prima stesione chiedeva `not re.search(...)` e mordeva i
        # documenti che dichiarano il numero **più volte** — che sono tre su
        # quattro, e sono i documenti più curati. Un controllo che si arrabbia
        # con la precisione viene spento, e la precisione era il difetto.
        if not re.findall(expr, testo):
            # Una voce della lista che non trova piu' il suo numero non e' una
            # voce innocua: e' **un numero che il controllo non guarda piu'**, e
            # il documento che lo scrive puo' dire quello che vuole senza che
            # nessuno se ne accorga. Meglio un controllo che si rifiuta di tacere
            # che un controllo che tace.
            problemi.append("I6  %s non contiene piu' la frase che dichiara il "
                            "numero dei file: quel numero non e' controllato"
                            % os.path.basename(percorso))

    # I7  la regola della cartella, guardata nei documenti e non solo nei file:
    #     `mondo_admin1_copertura.json` è un JSON ordinario, sta in `dati/` e ci
    #     è finito il 03/10 per errore dentro `dati/mappe/`, dove faceva
    #     crashare il lettore. Un documento che lo nomina **senza dire che è
    #     fuori** ripubblica l'errore, e `AGENTS.md` — il file che tutti leggono
    #     — lo ripubblicava.
    for percorso in ("AGENTS.md", "README.md", "docs/videogioco-5-duchi-mappe.md",
                     "docs/videogioco-5-duchi-fonti-visive.md"):
        testo = leggi(os.path.join(RADICE, percorso))
        # Il difetto e' uno solo e ha una forma sola: **il file elencato dentro
        # `dati/mappe/`**. Una riga che lo nomina dicendo che sta in `dati/` e
        # non li' e' la correzione, non il difetto, e va lasciata stare: un
        # controllo che morde anche la correzione viene spento, e la prossima
        # volta che serve smetterebbe di dire la verita' su tutto il resto.
        for m2 in re.finditer(r"[^\n]*mondo_admin1_copertura\.json[^\n]*", testo):
            riga = m2.group(0)
            dentro = re.search(r"`?dati/mappe/`?[^\n]*mondo_admin1_copertura", riga)
            if not dentro:
                continue
            # elencato fra i file di `dati/mappe/`: e' il difetto, salvo che la
            # stessa riga dichiari lo spostamento
            if re.search(r"spostat|fuori da|non in `dati/mappe/`|non ci sta|"
                         r"tolto da|sta in `dati/`|perche' li", riga):
                continue
            problemi.append("I7  %s elenca `mondo_admin1_copertura.json` dentro "
                            "`dati/mappe/`: quel file ci e' stato il 03/10 e ha "
                            "fatto crashare il lettore, ed e' in `dati/`"
                            % os.path.basename(percorso))

    # I8  e i pin coperti dal file amministrativo, che è un dato e non una frase
    cop = json.load(open(os.path.join(RADICE, "dati", "mondo_admin1_copertura.json"),
                         encoding="utf-8"))
    testo = leggi(os.path.join(RADICE, "AGENTS.md"))
    for m2 in re.finditer(r"che coprono \*\*(\d+) pin su (\d+)\*\*", testo):
        if int(m2.group(1)) != cop["pin_coperti"] or int(m2.group(2)) != cop["pin_totali"]:
            problemi.append("I8  AGENTS.md dichiara %s pin coperti, il file di "
                            "copertura dice %d su %d"
                            % (m2.group(0), cop["pin_coperti"], cop["pin_totali"]))

    print()
    if problemi:
        print("problemi: %d" % len(problemi))
        for p in problemi:
            print("  " + p)
    else:
        print("problemi: 0")
        print("(il manifest copre la cartella, ogni file dichiara fonte e "
              "produttore, e ogni numero che i documenti riportano combacia)")
    return 1 if problemi else 0


if __name__ == "__main__":
    sys.exit(main())