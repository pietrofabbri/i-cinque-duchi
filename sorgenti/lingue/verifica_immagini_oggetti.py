#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifica le immagini degli oggetti di interazione.

Fa sei controlli sui dati di `dati/lingue/immagini_oggetti.json`, che sono
**proposte** e non scelte: il verificatore guarda i numeri, non le immagini.
Le scelte le fa una persona e si registrano in
`dati/lingue/attestazione_oggetti.json` con etichetta e motivo, come per i
ritratti.

I controlli:

  G1  copertura    ogni voce ha candidati, e le trenta ferraresi dichiarano
                  perché non ne possono avere
  G2  licenze      ogni candidato ha una licenza libera riconosciuta
  G3  misura      ogni candidato è abbastanza grande per la scheda del gioco
  G4  proporzione **per voce**: esiste almeno un candidato con la forma giusta
                  per entrare nella scheda senza essere straziato dal ritaglio
  G5  completezza  l'indirizzo c'è in ogni candidato, e l'autore c'è quando la
                  licenza lo richiede: in pubblico dominio non lo richiede
  G6  pertinenza   dichiarata, non automatica: quante voci restano da guardare
                  a vista e quante rischiano di avere un'immagine sbagliata
  G7  scivolamento  **avviso, non problema**: nessun candidato della voce nomina
                  l'oggetto né i termini cercati, il che vuol dire che la
                  ricerca ha scoperto una coincidenza di lettere. Non dice che
                  l'immagine sia sbagliata: dice che va guardata per prima
  G8  due classi   i candidati respinti si contano separati: per merito
                  (il candidato è stato guardato e non entra) e per
                  metadati mancanti (la fonte non li dichiara e nessun
                  codice li può far comparire). I due numeri sono
                  quelli che il documento dichiara
  G9  l'estrattore **eseguito**, non letto: gli altri otto controlli guardano
                  il file che l'estrattore ha scritto, e un estrattore rotto
                  produce un file coerente e falso. Qui l'estrattore vero
                  gira senza rete su una risposta di Commons finta, e ogni
                  candidato deve portare il proprio autore

Il punto di G6 e G7 è la lezione già imparata con i ritratti, dove una ricerca
automatica ha restituito un gatto per Renata Viganò e una ceramica iraniana per
i mercanti di Ferrara. Una ricerca che trova il file «giusto» non ha ancora
trovato l'oggetto giusto, e G7 lo rende visibile senza guardare le immagini.
"""
import collections
import io
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(BASE, "..", ".."))
DATI = os.path.join(RADICE, "dati", "lingue", "immagini_oggetti.json")
ATTESTAZIONE = os.path.join(RADICE, "dati", "lingue", "attestazione_oggetti.json")

# La scheda dell'oggetto nel gioco. I ritratti sono 48×54; l'oggetto ha poco
# più di spazio, perché si vede meglio, ma non il doppio.
LARGHEZZA_SCHEDA = 96
ALTEZZA_SCHEDA = 72

# Sotto questa misura l'immagine nel gioco verrebbe ingrandita, e il gioco non
# ingrandisce: non entra.
LARGHEZZA_MINIMA = 160
ALTEZZA_MINIMA = 120

# La scheda è 4:3. Si accetta una fascia attorno: ritagliare una foto in 4:3
# spesso toglie l'oggetto, e obbligare al ritaglio peggiorerebbe proprio la
# rappresentazione che il progetto vuole fedele.
PROPORZIONE = LARGHEZZA_SCHEDA / ALTEZZA_SCHEDA
TOLLERANZA = 0.45

LIB_OK = re.compile(
    r"public domain|pubblico dominio|\bpd\b|cc0|no restrictions"
    r"|cc[- ]?by(?![a-ns])|cc[- ]?by[- ]sa|attribution", re.I)
LIB_NO = re.compile(r"non[- ]?commercial|fair use|\bcc by[- ]nc|no deriv", re.I)
# **Le licenze che obbligano a nominare l'autore.** Solo le Creative Commons con
# attribuzione: in pubblico dominio e in CC0 l'opera si puo' usare senza dire di
# chi e', e chiedere un autore che la legge non chiede respinse quattro
# immagini che si potevano usare legittimamente.
LICENZA_ATTRIBUZIONE = re.compile(r"cc[- ]?by", re.I)


def candito_buono(c):
    """Un candidato che si può usare: licenza libera, abbastanza grande, con
    l'indirizzo, e con l'autore solo se la licenza lo richiede.

    Non dice che sia l'oggetto giusto: quello lo dice una persona.
    """
    licenza = c.get("licenza", "")
    if LIB_NO.search(licenza):
        return False, "licenza non libera"
    if not LIB_OK.search(licenza):
        return False, "licenza non riconosciuta"
    # **L'indirizzo serve sempre**: e' la via per ritrovare il file e da' la
    # provenienza. Senza indirizzo non si sa da dove venga un'immagine, e
    # quello e' un difetto nostro, non della fonte.
    if not c.get("url"):
        return False, "manca l'indirizzo"
    if LICENZA_ATTRIBUZIONE.search(licenza) and not c.get("autore"):
        return False, "manca l'autore che la licenza richiede"
    larghezza = c.get("larghezza") or 0
    altezza = c.get("altezza") or 0
    if not larghezza or not altezza:
        return False, "mancano le dimensioni"
    if larghezza < LARGHEZZA_MINIMA or altezza < ALTEZZA_MINIMA:
        return False, "troppo piccola"
    return True, ""


# **La classe di ogni motivo di rifiuto.** `merito` è un giudizio: il
# candidato è stato guardato e non entra. `fonte` è un'assenza: la fonte non
# dichiara il metadato, e nessun codice lo può far comparire. «licenza non
# riconosciuta» sta nella seconda, ed è la scelta che conta: non riconoscere
# una licenza non è un giudizio, è la stessa forma del difetto che respinse 385
# fotografie CC BY-SA perché la chiave del progetto era `cc-by-sa-4.0` e la
# fonte scrive `CC BY-SA 4.0`. Un trattino non è una sentenza.
CLASSE = {
    "licenza non libera": ("G2", "merito"),
    "licenza non riconosciuta": ("G2", "fonte"),
    "troppo piccola": ("G3", "merito"),
    "manca l'indirizzo": ("G5", "fonte"),
    "manca l'autore che la licenza richiede": ("G5", "fonte"),
    "mancano le dimensioni": ("G5", "fonte"),
}
DICHIARATO = re.compile(
    r"\*\*(\d+) candidati respinti\*\*.*?per merito \*\*(\d+)\*\*.*?"
    r"per metadati mancanti[^0-9]*\*\*(\d+)\*\*", re.S)


def proporzione_buona(c):
    larghezza = c.get("larghezza") or 0
    altezza = c.get("altezza") or 0
    if not larghezza or not altezza:
        return False
    p = larghezza / altezza
    return abs(p - PROPORZIONE) / PROPORZIONE <= TOLLERANZA


def scivolato(voce, termini, nome_file):
    """Il file è stato trovato per una coincidenza di lettere?

    Il metodo: dal nome del file si tolgono i termini cercati e le parole della
    voce. Se rimane un nome proprio che non compare da nessuna parte, il file
    c'entra per caso. È successo davvero: alla voce «la correggia» è stato
    proposto il file di un pittore che si chiama Correggio, e alla voce «gli
    occhiali» una moschea di Istanbul.

    Non è un controllo che «sa» se l'immagine è giusta: è un controllo che
    dice che il nome del file non parla dell'oggetto, e quindi che la scelta va
    guardata per prima.
    """
    testo = nome_file.replace("File:", "")
    testo = re.sub(r"[\d\(\)\[\]&,.\-—_%+']", " ", testo)
    noto = (voce + " " + " ".join(termini)).lower()
    residui = []
    for p in re.findall(r"[A-Za-zÀ-ÿ]{4,}", testo):
        if p.lower() in noto:
            continue
        residui.append(p)
    if not residui:
        return ""
    return ", ".join(residui[:3])


COMUNE = {
    # parole che compaiono in millemila nomi di file e non dicono niente
    "file", "image", "photo", "wikipedia", "commons", "jpg", "jpeg", "png",
    "gis", "svg", "italian", "italy", "italiano", "italiana", "greek",
    "greek", "ancient", "roman", "greece", "italia", "italian", "deutsch",
    "english", "france", "french", "germany", "spain", "greece", "turkey",
    "und", "der", "die", "das", "des", "von", "les", "des", "pour", "avec",
    "photo", "white", "black", "red", "green", "blue", "old", "new", "the",
    "chr", "st", "di", "da", "de", "del", "la", "le", "el", "los", "das",
    "cropped", "detail", "close", "view", "logo", "map", "chart", "cover",
}


def tutto_a_rischio(voce, termini, candidati):
    """Nessun candidato della voce nomina l'oggetto.

    Il confronto è con la voce **e con i termini cercati**: il file di un'anfora
    greca non contiene la parola «coppa» ma contiene «kylix», che è il termine
    giusto, e va tenuto. Il caso peggiore è quando non contiene né l'uno né
    l'altro: alla voce «la correggia» il file migliore era
    «Antonio Allegri da Correggio.jpg».
    """
    noto = {p.lower() for p in re.findall(r"[A-Za-zÀ-ÿ]{4,}", voce + " " + " ".join(termini))}
    for c in candidati:
        testo = re.sub(r"[\d\(\)\[\]&,.\-—_%+']", " ", c["file"].replace("File:", ""))
        parole = {p.lower() for p in re.findall(r"[A-Za-zÀ-ÿ]{4,}", testo)} - COMUNE
        if parole & noto:
            return False
    return True


# **La risposta finta con cui si esercita l'estrattore.** Tre candidati che
# dicono cose diverse: uno ha l'autore in `Artist`, uno solo in `Attribution`,
# uno non dichiara niente. Il terzo e' quello che distingue un estrattore
# corretto da uno che porta l'autore del primo candidato su tutti gli altri:
# senza di lui, «il primo autore finisce su tutti» passerebbe.
RISPOSTA_FINTA = {
    "query": {"pages": {
        "1": {"title": "File:Primo.jpg", "imageinfo": [{
            "width": 800, "height": 600, "descriptionurl": "u/1",
            "extmetadata": {"LicenseShortName": {"value": "CC BY 2.0"},
                            "Artist": {"value": "AUTORE-PRIMO"}}}]},
        "2": {"title": "File:Secondo.jpg", "imageinfo": [{
            "width": 900, "height": 700, "descriptionurl": "u/2",
            "extmetadata": {"LicenseShortName": {"value": "CC BY-SA 4.0"},
                            "Artist": {"value": "AUTORE-SECONDO"}}}]},
        "3": {"title": "File:Terzo.jpg", "imageinfo": [{
            "width": 900, "height": 700, "descriptionurl": "u/3",
            "extmetadata": {"LicenseShortName": {"value": "CC0"},
                            "Attribution": {"value": "Wollombi"}}}]},
        "4": {"title": "File:Quarto.jpg", "imageinfo": [{
            "width": 900, "height": 700, "descriptionurl": "u/4",
            "extmetadata": {"LicenseShortName": {"value": "CC0"}}}]},
    }},
}
# Cosa ci si aspetta da quei quattro candidati, nell'ordine in cui li restituisce
# l'estrattore: il primo autore, il secondo, quello che sta solo in
# `Attribution`, e nessuno. L'ultimo e' il caso che distingue tutto.
ATTESI_FINTI = ["AUTORE-PRIMO", "AUTORE-SECONDO", "Wollombi", ""]


def carica_estrattore(percorso=None):
    """L'estrattore, importato da un percorso dato o dal suo posto solito."""
    import importlib.util
    if percorso is None:
        percorso = os.path.join(BASE, "cerca_immagini_oggetti.py")
    spec = importlib.util.spec_from_file_location("cerca_immagini_oggetti",
                                                  percorso)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def controlla_estrattore(problemi, percorso=None):
    """G9: l'estrattore gira davvero e ogni candidato porta il suo autore."""
    try:
        estrattore = carica_estrattore(percorso)
    except Exception as errore:  # noqa: BLE001 - il motivo va detto
        problemi.append("G9 l'estrattore non si puo' caricare: %s" % errore)
        return
    estrattore.get = lambda q: RISPOSTA_FINTA
    estrattore.time.sleep = lambda *a, **k: None
    try:
        candidati = estrattore.cerca(["un termine qualsiasi"])
    except Exception as errore:  # noqa: BLE001 - il motivo va detto
        problemi.append(
            "G9 l'estrattore muore su una risposta finta: %s: %s "
            "(e' il difetto che aveva reso impossibile rigenerare i dati)"
            % (type(errore).__name__, errore))
        return
    if len(candidati) != len(ATTESI_FINTI):
        problemi.append(
            "G9 l'estrattore ha restituito %d candidati su %d: la risposta "
            "finita ne contiene %d"
            % (len(candidati), len(ATTESI_FINTI), len(ATTESI_FINTI)))
        return
    for ottenuto, atteso, nome in zip([c.get("autore", "") for c in candidati],
                                      ATTESI_FINTI,
                                      [c.get("file", "?") for c in candidati]):
        if ottenuto != atteso:
            problema = "G9 %s: autore %r, la fonte dichiara %r" % (
                nome, ottenuto, atteso)
            if ottenuto == ATTESI_FINTI[0] and atteso != ATTESI_FINTI[0]:
                problema += (" — l'estrattore sta portando l'autore del primo "
                             "candidato su tutti gli altri")
            problemi.append(problema)


# **Il difetto iniettato, scritto una volta sola e usato come si usa.** Non e'
# togliere una riga: e' l'autore del primo candidato che resta appeso alla
# funzione e viene riusato per tutti gli altri. Non e' neppure il difetto di
# una lista che non riparte da vuoto — e' quello che nasce scrivendo «se non
# ce n'e' uno, tienilo» invece di «leggilo ogni volta». Le tre righe sostituiscono
# una riga sola, e la riga che sostituiscono e' l'unica che legge l'autore.
DIFETTO_AUTORE = (
    '            autore = getattr(cerca, "_primo", "") or autore_di(meta)\n'
    '            cerca._primo = autore'
)
RIGA_DA_CORROMPERE = "            autore = autore_di(meta)"


def prova_difetti():
    """Il difetto vero, iniettato su una copia dell'estrattore.

    L'estrattore copiato che porta l'autore del primo candidato su tutti gli
    altri deve essere rosso. Se la prova non morde vuol dire che G9 non sta
    guardando il codice ma qualcosa d'altro.
    """
    import shutil
    import tempfile
    vero = os.path.join(BASE, "cerca_immagini_oggetti.py")
    with io.open(vero, encoding="utf-8") as f:
        testo = f.read()
    rotto = testo.replace(RIGA_DA_CORROMPERE, DIFETTO_AUTORE, 1)
    if rotto == testo:
        print("   NON INIETTATO G9: l'estrattore non chiama piu' autore_di")
        print("\ndifetti iniettati: 0, visti: 0, non visti: 1")
        return 1
    temporanea = tempfile.mkdtemp(prefix="g9_")
    try:
        copia = os.path.join(temporanea, "cerca_immagini_oggetti.py")
        with io.open(copia, "w", encoding="utf-8") as f:
            f.write(rotto)
        problemi = []
        controlla_estrattore(problemi, copia)
        visti = [p for p in problemi if p.startswith("G9 ")]
    finally:
        shutil.rmtree(temporanea, ignore_errors=True)
    for p in visti:
        print("   visto   %s" % p)
    if not visti:
        print("   NON VISTO  G9")
    print("\ndifetti iniettati: 1, visti: %d, non visti: %d"
          % (len(visti), 0 if visti else 1))
    return 0 if visti else 1


def main():
    if "--difetti" in sys.argv:
        return prova_difetti()
    if not os.path.exists(DATI):
        print("manca", DATI)
        return 1
    with open(DATI, encoding="utf-8") as f:
        risultati = json.load(f)["risultati"]

    problemi = []
    copertura = collections.defaultdict(lambda: {"voci": 0, "con": 0, "senza": 0,
                                                "senza_proporzione": 0, "candidati": 0})
    licenze = collections.Counter()
    rischi = set()
    da_vedere = 0
    scarti = {"merito": 0, "fonte": 0}
    scarti_per_motivo = collections.Counter()
    respinti = []

    for a in risultati:
        lingua = a["lingua"]
        v = copertura[lingua]
        v["voci"] += 1
        etichetta = "%s %d (%s)" % (lingua, a["numero"], a["voce"])

        # G1 — copertura
        if not a["candidati"]:
            v["senza"] += 1
            if not a.get("motivo"):
                problemi.append("G1 %s: nessun candidato e nessun motivo dichiarato" % etichetta)
            continue
        v["con"] += 1
        da_vedere += 1
        if a["categoria"] != "da_vedere":
            problemi.append("G1 %s: ha candidati ma la categoria è %r" % (etichetta, a["categoria"]))

        usabili = 0
        per_proporzione = 0
        for c in a["candidati"]:
            v["candidati"] += 1
            licenze[c.get("licenza", "")[:30] or "(nessuna)"] += 1
            buono, motivo = candito_buono(c)
            if not buono:
                # l'etichetta e' quella del controllo che ha respinto, e non un
                # fascio di tre: sapere che G5 e' quello che ha scartato dice
                # anche da dove si comincia a rimediare
                chi, classe = CLASSE.get(motivo, ("G2", "fonte"))
                scarti[classe] += 1
                scarti_per_motivo[motivo] += 1
                # l'etichetta sta in letterale e non in un `%s`: un'etichetta
                # costruita a runtime è invisibile a un controllo che la cerca
                # nel codice, e un'etichetta invisibile è un'etichetta che non
                # si può citare. La tabella dei tre formati sta qui accanto,
                # non in fondo al file, perché sia dove si riporta.
                # l'etichetta sta **dopo** la sua riga che riporta, in
                # letterale: un controllo che cerca l'etichetta nel codice la
                # cerca in avanti rispetto a chi riporta, e una tabella di
                # formati scritta prima dell'append non la trova. Tre righe in
                # piu', e ognuna dice da chi viene il rifiuto.
                # Uno scarto **per merito** e' il controllo che ha fatto il suo
                # lavoro: il candidato e' stato misurato e non entra, e il
                # documento lo conta (G8). Non e' un difetto del progetto, e
                # metterlo fra i problemi rende il verificatore rosso per
                # sempre: fra il 5 e il 6 ottobre 2026 lo era per sette
                # immagini troppo piccole che il capitolo dichiara respinte.
                # Uno scarto **per fonte** resta un problema: e' un metadato
                # che nessuno ha deciso, e qualcuno deve rimediare.
                if chi == "G3" and classe == "merito":
                    respinti.append("G3 %s: %s — %s (%s)"
                                    % (etichetta, c["file"], motivo, classe))
                elif chi == "G2" and classe == "merito":
                    respinti.append("G2 %s: %s — %s (%s)"
                                    % (etichetta, c["file"], motivo, classe))
                elif chi == "G3":
                    problemi.append("G3 %s: %s — %s (%s)"
                                    % (etichetta, c["file"], motivo, classe))
                elif chi == "G5":
                    problemi.append("G5 %s: %s — %s (%s)"
                                    % (etichetta, c["file"], motivo, classe))
                else:
                    problemi.append("G2 %s: %s — %s (%s)"
                                    % (etichetta, c["file"], motivo, classe))
                continue
            usabili += 1
            if proporzione_buona(c):
                per_proporzione += 1

        # G7 — la voce è a rischio quando nessun candidato nomina l'oggetto
        if usabili and tutto_a_rischio(a["voce"], a.get("termini", []), a["candidati"]):
            esempi = ", ".join(c["file"][:34] for c in a["candidati"][:2])
            rischi.add((etichetta, esempi, "nessun candidato nomina l'oggetto"))

        # G4 — la voce è coperta solo se almeno un candidato è-usabile ha la
        # forma giusta. Se tutti gli usabili sono strisce o strani, la voce
        # non è coperta e va cercata meglio.
        if usabili == 0:
            v["senza"] += 1
            problemi.append("G4 %s: nessun candidato usabile fra %d proposti"
                            % (etichetta, len(a["candidati"])))
        elif per_proporzione == 0:
            v["senza_proporzione"] += 1
            problemi.append("G4 %s: i %d candidati usabili sono tutti lontani "
                            "dalla proporzione della scheda (%.2f): vanno cercati "
                            "meglio, non ritagliati a forza"
                            % (etichetta, usabili, PROPORZIONE))

    ferraresi = [a for a in risultati if a["lingua"] == "FE"]
    for a in ferraresi:
        if a["candidati"]:
            problemi.append("G1 FE %d: un campo di rilevazione non ha immagine, ma ne ha una"
                            % a["numero"])

    scelte = 0
    if os.path.exists(ATTESTAZIONE):
        with open(ATTESTAZIONE, encoding="utf-8") as f:
            scelte = len(json.load(f).get("scelte", []))

    print("voci: %d" % len(risultati))
    for lingua in sorted(copertura):
        v = copertura[lingua]
        print("  %s: %2d voci, %2d con immagini libere, %2d senza, %d da cercare meglio"
              % (lingua, v["voci"], v["con"], v["senza"], v["senza_proporzione"]))
    print("candidati proposti: %d" % sum(v["candidati"] for v in copertura.values()))
    print("licenze dei candidati: %d diverse" % len(licenze))
    for k, n in licenze.most_common(8):
        print("    %4d  %s" % (n, k))
    # G8 — i due rifiuti non sono la stessa cosa, e il documento lo dice
    documento = open(os.path.join(RADICE, "docs",
                                  "videogioco-5-duchi-lingue-immagini.md"),
                     encoding="utf-8").read()
    m = DICHIARATO.search(documento)
    if m is None:
        problemi.append(
            "G8 il documento non dichiara la riga dei candidati respinti: "
            "senza quella riga i due conti non hanno con cosa essere "
            "confrontati, e sono solo due numeri qui")
    else:
        totale, merito, metadati = (int(m.group(1)), int(m.group(2)),
                                    int(m.group(3)))
        if totale != merito + metadati:
            problemi.append(
                "G8 il documento dichiara %d candidati respinti, %d per merito "
                "e %d per metadati mancanti: %d non fa %d"
                % (totale, merito, metadati, merito + metadati, totale))
        if merito != scarti["merito"] or metadati != scarti["fonte"]:
            problemi.append(
                "G8 il documento dichiara %d respinti per merito e %d per "
                "metadati mancanti, i candidati sono %d e %d"
                % (merito, metadati, scarti["merito"], scarti["fonte"]))

    # G9 — l'estrattore, eseguito
    controlla_estrattore(problemi)

    print("candidati respinti: %d in tutto" % (scarti["merito"]
                                              + scarti["fonte"]))
    print("  per merito (il candidato e' stato guardato e non entra): %d"
          % scarti["merito"])
    print("  per metadati mancanti (la fonte non li dichiara, nessun codice "
          "li puo' far comparire): %d" % scarti["fonte"])
    for motivo, n in scarti_per_motivo.most_common():
        chi, classe = CLASSE.get(motivo, ("G2", "fonte"))
        print("    %2d  %-6s %-28s %s" % (n, chi, classe, motivo))
    for r in respinti:
        print("    respinto  " + r)
    print("G6 voci da guardare a vista: %d (il controllo automatico non può "
          "sapere se l'immagine è dell'oggetto giusto)" % da_vedere)
    voci_a_rischio = sorted({r[0] for r in rischi})
    print("G7 AVVISI, non problemi: %d voci in cui nessun candidato nomina "
          "l'oggetto, e che vanno quindi guardate per prime" % len(voci_a_rischio))
    for etichetta, esempi, scivolo in sorted(rischi)[:10]:
        print("    %-30s %s" % (etichetta, esempi))
    if len(rischi) > 10:
        print("    ... e altre %d voci" % (len(rischi) - 10))
    print("    G7 non dice che l'immagine sia sbagliata: dice che il suo nome")
    print("    non parla dell'oggetto, e quindi che guardarla è la prima cosa.")
    print("immagini già scelte a vista: %d" % scelte)
    print("G9 l'estrattore e' stato eseguito su una risposta finta, senza rete")
    print("problemi: %d" % len(problemi))
    for p in problemi:
        print("  " + p)
    return 1 if problemi else 0


if __name__ == "__main__":
    sys.exit(main())
