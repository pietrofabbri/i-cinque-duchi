# -*- coding: utf-8 -*-
"""I controlli sugli interni degli edifici che l'anno 1 mostra.

**Che cosa badano, e perché questi e non altri.** Il file
`dati/interni_edifici.json` è una raccolta: mette insieme trenta edifici del
gioco, le categorie di Wikimedia Commons che li descrivono, le stanze che
quelle categorie nominano, e le licenze delle fotografie. Ogni passaggio è un
posto dove può succedere una delle tre cose che il progetto chiama tradimento:
un numero che non torna, una fonte che non è la fonte, un'assenza che sembra
uno zero.

| controllo | che cosa guarda |
|---|---|
| **I1** | ogni edificio del gioco c'è nel file, con la sua tappa e il suo argomento, e non ce n'è nessuno in più |
| **I2** | i numeri del riepilogo sono contati sul file, non dichiarati |
| **I3** | ogni stanza è una stanza per la regola dichiarata, e ogni esclusione porta il motivo |
| **I4** | ogni licenza dichiarata è fra quelle accettate, e il numero delle immagini libere è contato |
| **I5** | ogni assenza porta il perché, e nessun edificio è dichiarato assente per non averlo cercato |
| **I6** | le categorie sono di Ferrara, e quelle condivise fra più tappe sono dichiarate |
| **I7** | i numeri che il capitolo §6 dichiara sono quelli che il file ha |

Uso:  python3 sorgenti/verifica_interni.py
      python3 sorgenti/verifica_interni.py --difetti    # prova che i controlli vedano
"""
import io
import json
import os
import re
import sys

RADICE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INTERNI = os.path.join(RADICE, "dati", "interni_edifici.json")
AMBIENTI = os.path.join(RADICE, "dati", "ambienti_livelli.json")
GENERATORE = os.path.join(RADICE, "sorgenti", "interni_edifici.py")
CAPITOLO = os.path.join(RADICE, "docs", "videogioco-5-duchi-luoghi-edifici.md")

# Le etichette che il capitolo scrive, e il numero che ci deve essere dietro.
# **La mappa è dichiarata qui e non nel capitolo**: il capitolo scrive
# «stanze trovate», il file chiama la chiave `stanze`, e se le due cose
# divergono nessuno se ne accorgerebbe finché i numeri non diventano falsi.
NUMERI_IN_PAROLE = {"tre": 3, "quattro": 4, "cinque": 5, "sei": 6,
                   "sette": 7, "otto": 8, "nove": 9, "dieci": 10}

ETICHETTE = {
    "edifici dell\'anno 1": "edifici",
    "con una categoria di Commons": "edifici_con_categoria",
    "con almeno una stanza": "edifici_con_stanze",
    "stanze trovate": "stanze",
    "stanze con almeno una fotografia libera": "stanze_con_immagine_libera",
    "fotografie, tutte con licenza libera dichiarata": "immagini_libere",
    "categorie di Commons condivise da più tappe": "categorie_condivise",
    "edifici dichiarati senza categoria, con il perché": "senza_categoria",
    "edifici con categoria ma senza stanze": "senza_stanze",
}


def leggi(percorso):
    with io.open(percorso, encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------- I1
def i1_la_lista(dati, ambienti):
    """Un edificio per tappa, con quello che il gioco dice di lui."""
    problemi = []
    per_gioco = {}
    for a in ambienti["ambienti"]:
        if a["anno"] != 1:
            continue
        per_gioco.setdefault(a["livello"], a)
    nel_file = {}
    for e in dati["edifici"]:
        if e["tappa"] in nel_file:
            problemi.append("I1 la tappa %s compare due volte nel file "
                            "degli interni" % e["tappa"])
        nel_file[e["tappa"]] = e
    for tappa, a in sorted(per_gioco.items()):
        e = nel_file.get(tappa)
        if e is None:
            problemi.append("I1 la tappa %s (%s) manca dagli interni: il "
                            "gioco la mostra e il file non la dice"
                            % (tappa, a["luogo"]))
            continue
        if e["luogo"] != a["luogo"]:
            problemi.append("I1 la tappa %s si chiama %s nel gioco e %s negli "
                            "interni" % (tappa, a["luogo"], e["luogo"]))
        if e.get("argomento") != a.get("argomento"):
            problemi.append("I1 la tappa %s ha l'argomento %r negli interni e "
                            "%r nel gioco" % (tappa, e.get("argomento"),
                                              a.get("argomento")))
    for tappa in sorted(set(nel_file) - set(per_gioco)):
        problemi.append("I1 gli interni hanno la tappa %s, che il gioco non "
                        "mostra" % tappa)
    return problemi


# ---------------------------------------------------------------- I2
def i2_i_numeri(dati, ambienti):
    """Il riepilogo è contato sul file, non scritto a mano."""
    problemi = []
    edifici = dati["edifici"]
    tutte = [s for e in edifici for s in e["stanze"]]
    atteso = {
        "edifici": len(edifici),
        "edifici_con_categoria": len([e for e in edifici
                                      if e["categoria_commons"]]),
        "edifici_con_stanze": len([e for e in edifici if e["stanze"]]),
        "stanze": len(tutte),
        "stanze_con_immagine_libera": len([s for s in tutte
                                           if s["immagini_libere"]]),
        "immagini": sum(s["immagini"] for s in tutte),
        "immagini_libere": sum(s["immagini_libere"] for s in tutte),
        "stanze_senza_immagine": len(tutte) - len([s for s in tutte
                                                     if s["immagini_libere"]]),
        "categorie_condivise": len(dati.get("categorie_condivise") or {}),
    }
    for chiave, valore in sorted(atteso.items()):
        dichiarato = dati["riepilogo"].get(chiave)
        if dichiarato != valore:
            problemi.append("I2 il riepilogo dice %s=%r e sul file ci sono %r"
                            % (chiave, dichiarato, valore))
    for chiave in dati["riepilogo"]:
        if chiave == "da":
            continue
        if chiave not in atteso:
            problemi.append("I2 il riepilogo dichiara %s, che nessun "
                            "controllo sa contare" % chiave)
    return problemi


# ---------------------------------------------------------------- I3
def i3_le_stanze(dati, ambienti):
    """Le stanze sono stanze per la regola scritta, e le esclusioni hanno un perché.

    La regola viene **riletta dal generatore**, non ripetuta qui: se le due
    copie divergono, il controllo che le confronta direbbe la stessa frase del
    generatore e non se ne accorgerebbe. Qui si prende il modulo e si gli
    chiede, e gli si chiede anche per un nome che non è nel file — perché una
    regola che si verifica solo sui nomi del file non verifica la regola,
    verifica il file.
    """
    problemi = []
    try:
        sys.path.insert(0, os.path.dirname(GENERATORE))
        import interni_edifici
    except ImportError:
        return ["I3 il generatore non si può importare: il controllo non può "
                "guardare la regola delle stanze"]

    for e in dati["edifici"]:
        edificio = (e.get("nome_cercato") or [None])[0]
        for s in e["stanze"]:
            ok, perche = interni_edifici.e_stanza(s["categoria"], edificio)
            if not ok:
                problemi.append("I3 %s / %s è nel file come stanza ma la "
                                "regola dice che non lo è: %s"
                                % (e["luogo"], s["nome"], perche))
            atteso = interni_edifici.nome_senza_edificio(s["categoria"],
                                                         edificio)
            if s["nome"] != atteso:
                problemi.append("I3 %s: la stanza si chiama %r nel file e %r "
                                "dopo che si toglie l'edificio dal nome che la "
                                "fonte scrive"
                                % (e["luogo"], s["nome"], atteso))
        for n in e["non_stanze"]:
            if not n.get("perche"):
                problemi.append("I3 %s: %s è esclusa e non dice perché"
                                % (e["luogo"], n["categoria"]))
    return problemi


# ---------------------------------------------------------------- I4
def i4_le_licenze(dati, ambienti):
    """Le licenze sono fra quelle accettate, e i numeri delle immagini sono contati."""
    problemi = []
    try:
        sys.path.insert(0, os.path.dirname(GENERATORE))
        import interni_edifici
    except ImportError:
        return ["I4 il generatore non si può importare"]
    # il confronto è sulle **chiavi**, non sui nomi: nel file la licenza si
    # scrive come la chiama `breve()` (l'unica che decide anche se l'immagine
    # è libera), e confrontare la chiave con il nome display scopre un falso
    # problema su tutte le 57 stanze
    accettate = set(interni_edifici.LICENZE_LIBERE)
    for e in dati["edifici"]:
        for s in e["stanze"]:
            if s["immagini_libere"] > s["immagini"]:
                problemi.append("I4 %s / %s: %d immagini libere su %d "
                                "immagini: più libere delle immagini che ci "
                                "sono" % (e["luogo"], s["nome"],
                                          s["immagini_libere"], s["immagini"]))
            if not s["licenze"] and s["immagini"]:
                problemi.append("I4 %s / %s ha %d immagini e nessuna licenza "
                                "riconosciuta" % (e["luogo"], s["nome"],
                                                  s["immagini"]))
            for l in s["licenze"]:
                if l not in accettate:
                    problemi.append("I4 %s / %s: la licenza %r non è fra quelle "
                                    "che il progetto accetta"
                                    % (e["luogo"], s["nome"], l))
            if not s["immagini_libere"] and not s.get("vuoto"):
                problemi.append("I4 %s / %s non ha immagini libere e non "
                                "dichiara il perché"
                                % (e["luogo"], s["nome"]))
    return problemi


# ---------------------------------------------------------------- I5
def i5_le_assenze(dati, ambienti):
    """Ogni assenza dice perché, e nessuna è un non cercato.

    Il secondo punto è quello che rende il primo utile: un edificio senza
    categoria *può* essere un edificio di cui la fonte non parla, e può essere
    un edificio che nessuno ha cercato. La differenza si vede nei campi: un
    buildings cercato e non trovato porta i nomi che sono stati cercati, uno
    non cercato no.
    """
    problemi = []
    for e in dati["edifici"]:
        if not e["categoria_commons"]:
            if not e.get("vuoto"):
                problemi.append("I5 %s non ha categoria e non dice perché"
                                % e["luogo"])
            elif not e["nome_cercato"]:
                problemi.append("I5 %s non ha categoria e non dichiara quale "
                                "nome è stato cercato" % e["luogo"])
            elif "ricerca" not in e and "candidati_ricerca" not in e:
                problemi.append("I5 %s non ha categoria e non dice se la "
                                "ricerca è stata tentata" % e["luogo"])
        elif e["stanze"] and any(v.strip() for v in e.get("vuoto", [])):
            # il vuoto di un edificio si dichiara **quando non ci sono
            # stanze**: è la spiegazione del perché non ce ne sono. Su un
            # edificio che ha stanze, un vuoto dichiarato sarebbe un secondo
            # discorso che contraddice il primo.
            problemi.append("I5 %s ha %d stanze e si dichiara anche vuoto: "
                            "sono due verità che non possono stare insieme"
                            % (e["luogo"], len(e["stanze"])))
    return problemi


# ---------------------------------------------------------------- I6
def i6_la_condivisione(dati, ambienti):
    """Una categoria può stare su più tappe, ma solo se il file lo dichiara.

    Le tre tappe della Certosa sono parti di un complesso solo: la categoria
    è una e le tappe sono tre, e va bene. Il guaio è il diverso: la Cattedrale
    di San Giorgio e il Museo della Cattedrale erano finiti sulla stessa
    categoria senza che nessuno lo dicesse, e chi leggeva il file contava due
    edifici dove ce n'era uno solo. Il controllo non vieta la condivisione:
    chiede che sia **scritta**.
    """
    problemi = []
    try:
        sys.path.insert(0, os.path.dirname(GENERATORE))
        import interni_edifici
    except ImportError:
        return ["I6 il generatore non si può importare: il controllo non può "
                "guardare la città delle categorie"]
    for e in dati["edifici"]:
        cat = e["categoria_commons"]
        if not cat:
            continue
        citta = interni_edifici.citta_di(cat)
        if citta not in (None, "Ferrara"):
            problemi.append("I6 %s ha la categoria di %s: il gioco gioca a "
                            "Ferrara e quella categoria è di un'altra città"
                            % (e["luogo"], citta))
    dichiarate = dati.get("categorie_condivise") or {}
    per_categoria = {}
    for e in dati["edifici"]:
        if e["categoria_commons"]:
            per_categoria.setdefault(e["categoria_commons"], []).append(
                e["tappa"])
    reali = {c: sorted(ts) for c, ts in per_categoria.items() if len(ts) > 1}
    if set(dichiarate) != set(reali):
        problemi.append("I6 le categorie condivise sono %d nel file e %d sono "
                        "dichiarate come tali: %s"
                        % (len(reali), len(dichiarate),
                           ", ".join(sorted(set(reali) ^ set(dichiarate)))))
    for cat, tappe in sorted(dichiarate.items()):
        if sorted(tappe) != reali.get(cat):
            problemi.append("I6 %s è dichiarata condivisa da %s e le tappe che "
                            "la hanno sono %s"
                            % (cat, tappe, reali.get(cat)))
        if sorted(tappe) != sorted(set(tappe)):
            problemi.append("I6 %s dichiara due volte la stessa tappa" % cat)
    return problemi


# ---------------------------------------------------------------- I7
def i7_il_capitolo(dati, ambienti):
    """Il capitolo dichiara i numeri del file, e i numeri sono quelli.

    Il capitolo §6 di `luoghi-edifici.md` scrive una tabella di numeri: sono
    gli stessi del file, ma scritti in un altro posto. Senza un controllo che
    li confronti sono due dichiarazioni indipendenti dello stesso fatto, e la
    prima a muoversi muove la seconda — che è esattamente quello che è
    successo con la riga sul chiostro di Sant'Antonio in Polesine: la frase
    era vera quando fu scritta e falsa quando la regola fu corretta, e nessuno
    l'aveva riletta.

    Il confronto è per **etichetta**, non per posizione: una riga in più nel
    capitolo non deve spostare il resto.
    """
    problemi = []
    if not os.path.exists(CAPITOLO):
        return ["I7 il capitolo %s non c'è: i numeri che dichiara non sono "
                "controllati da nessuno" % CAPITOLO]
    testo = io.open(CAPITOLO, encoding="utf-8").read()
    i = testo.find("## 6. Gli interni")
    if i < 0:
        return ["I7 il capitolo non ha la sezione 6: i numeri che dichiara non "
                "sono controllati da nessuno"]
    sezione = testo[i:]
    r = dati["riepilogo"]
    valori = {
        "edifici": r["edifici"],
        "edifici_con_categoria": r["edifici_con_categoria"],
        "edifici_con_stanze": r["edifici_con_stanze"],
        "stanze": r["stanze"],
        "stanze_con_immagine_libera": r["stanze_con_immagine_libera"],
        "immagini_libere": r["immagini_libere"],
        "categorie_condivise": r["categorie_condivise"],
        "senza_categoria": len([e for e in dati["edifici"]
                                if not e["categoria_commons"]]),
        "senza_stanze": len([e for e in dati["edifici"]
                             if e["categoria_commons"] and not e["stanze"]]),
    }
    visti = 0
    for etichetta, chiave in sorted(ETICHETTE.items()):
        # **la riga di tabella che porta quell'etichetta**, e il primo numero
        # che c'è dentro. La cella del numero può essere la stessa che porta
        # l'etichetta — «| i 12 edifici con categoria ma senza stanze | …» —
        # o quella dopo — «| stanze trovate | 41 |» — e un confronto che
        # cerca il numero solo nella cella successiva chiama «non dichiarato»
        # una riga che lo dichiara.
        riga = None
        for candidato in sezione.splitlines():
            if candidato.startswith("|") and etichetta in candidato:
                riga = candidato
                break
        # l'etichetta si toglie prima: «edifici dell'anno 1» porta un numero
        # dentro il nome, e senza toglierlo il confronto legge l'anno come se
        # fosse il conto degli edifici
        m = re.search(r"(\d+)", riga.replace(etichetta, " ")) if riga else None
        if not m:
            problemi.append("I7 il capitolo non dichiara nessun numero per "
                            "«%s»: l'etichetta è nella mappa dei numeri e "
                            "non è nella sezione" % etichetta)
            continue
        visti += 1
        scritto = int(m.group(1))
        if scritto != valori[chiave]:
            problemi.append("I7 il capitolo dice %s = %d e il file ha %d"
                            % (etichetta, scritto, valori[chiave]))
    # e il numero dei difetti, che il capitolo dichiara e che sta in questo file
    m = re.search(r"inietta \*\*(\d+) difetti\*\*", sezione)
    if m:
        visti += 1
        if int(m.group(1)) != len(DIFETTI):
            problemi.append("I7 il capitolo dice %s difetti iniettati e questo "
                            "file ne ha %d" % (m.group(1), len(DIFETTI)))
    else:
        problemi.append("I7 il capitolo non dichiara quanti difetti inietta: "
                        "il numero c'è e nessuno lo confronta")
    # e il numero dei controlli, che il capitolo scrive in prosa: «Sette
    # controlli in `verifica_interni.py`». È un numero come gli altri, e
    # invecchia come gli altri — quindi anche lui viene guardato, con una mappa
    # di parole dichiarata qui e non nel capitolo.
    m = re.search(r"(?i)\b(tre|quattro|cinque|sei|sette|otto|nove|dieci)"
                  r" controlli in `?sorgenti/verifica_interni\.py", sezione)
    if m:
        visti += 1
        scritto = NUMERI_IN_PAROLE[m.group(1).lower()]
        if scritto != len(CONTROLLI):
            problemi.append("I7 il capitolo dice %s controlli e questo file ne "
                            "ha %d" % (m.group(1).lower(), len(CONTROLLI)))
    else:
        problemi.append("I7 il capitolo non dichiara quanti controlli ha il "
                        "verificatore: il numero c'è e nessuno lo confronta")

    if visti < len(ETICHETTE):
        problemi.append("I7 il capitolo dichiara %d numeri su %d: %d righe non "
                        "hanno nessun controllo che le guardi"
                        % (visti, len(ETICHETTE), len(ETICHETTE) - visti))
    return problemi


CONTROLLI = (
    ("I1", "ogni tappa dell'anno 1 c'è negli interni, una volta sola",
     i1_la_lista),
    ("I2", "i numeri del riepilogo sono contati sul file",
     i2_i_numeri),
    ("I3", "le stanze sono stanze per la regola scritta, e le esclusioni "
           "dicono perché", i3_le_stanze),
    ("I4", "le licenze sono fra quelle accettate e i numeri tornano",
     i4_le_licenze),
    ("I5", "ogni assenza dice perché, e nessuna è un non cercato",
     i5_le_assenze),
    ("I6", "una categoria è di Ferrara, e se sta su più tappe il file lo dice",
     i6_la_condivisione),
    ("I7", "i numeri che il capitolo dichiara sono quelli del file",
     i7_il_capitolo),
)


def problemi(dati, ambienti):
    """Tutti i problemi di tutti i controlli, in ordine.

    **Ogni controllo prende gli stessi due documenti**, anche quelli che ne
    guardano uno solo. Il motivo e' pratico e non elegante: la prima versione
    aveva due firme diverse e sceglieva quale chiamare con un `is`, e un
    controllo aggiunto con la firma diversa non sarebbe stato chiamato senza
    che nulla lo dicesse. Una firma sola non puo' sbagliare cosi'.
    """
    trovati = []
    for nome, _, funzione in CONTROLLI:
        for p in funzione(dati, ambienti):
            trovati.append((nome, p))
    return trovati


# ---------------------------------------------------------------- difetti
DIFETTI = (
    ("I1", "tappa con l'argomento riscritto",
     "si cambia l'argomento di una tappa nel file degli interni"),
    ("I1", "tappa che manca",
     "si toglie un edificio dal file: il gioco lo mostra e il file no"),
    ("I2", "numero del riepilogo gonfiato",
     "si scrive una stanza in più nel riepilogo di quanto ce ne siano"),
    ("I3", "non stanza dichiarata stanza",
     "una sottocategoria che la regola esclude viene spostata fra le stanze"),
    ("I4", "licenza non accettata",
     "si scrive una licenza che il progetto non accetta"),
    ("I4", "immagini libere più delle immagini",
     "si dichiara più immagini libere di quante immagini ci siano"),
    ("I5", "assenza senza perché",
     "si toglie il perché da un edificio dichiarato senza categoria"),
    ("I3", "categoria di un'altra città spacciata per edificio",
     "si mette sotto il nome di un edificio di Ferrara la categoria di un "
     "museo omonimo di un'altra città"),
    ("I3", "categoria di opere spacciata per stanza",
     "si mette fra le stanze una categoria che parla di quadinti e mobili, "
     "non di un ambiente"),
    ("I6", "categoria condivisa non dichiarata",
     "si fa trovare la stessa categoria sotto due tappe senza dichiararlo"),
    ("I7", "numero del capitolo fermo",
     "si scrive nel capitolo un numero che il file non ha: la riga resta "
     "vera finché il dato non si muove, e allora è falsa e nessuno la "
     "rilette"),
)


def inietta(dati, ambienti, difetto):
    """Il difetto, iniettato in una copia del file. Ritorna la copia e il posto."""
    d = json.loads(json.dumps(dati))
    a = json.loads(json.dumps(ambienti))
    if difetto[0] == "I1" and "argomento" in difetto[1]:
        d["edifici"][3]["argomento"] = "un argomento che il gioco non scrive"
        return d, a
    if difetto[0] == "I1" and "manca" in difetto[1]:
        d["edifici"] = d["edifici"][1:]
        return d, a
    if difetto[0] == "I2":
        d["riepilogo"]["stanze"] = d["riepilogo"]["stanze"] + 1
        return d, a
    if difetto[0] == "I3":
        for e in d["edifici"]:
            if e["non_stanze"]:
                scartata = e["non_stanze"].pop(0)
                e["stanze"].append({
                    "nome": scartata["categoria"],
                    "categoria": scartata["categoria"],
                    "immagini": 0, "immagini_libere": 0,
                    "licenze": [], "esemplare": None,
                    "vuoto": ["nessuna immagine con licenza libera dichiarata: "
                              "la stanza c'è ma non entra nelle fonti del "
                              "gioco"],
                })
                return d, a
        raise SystemExit("nessun edificio con una categoria esclusa da spostare")
    if difetto[0] == "I4" and "licenza" in difetto[1]:
        for e in d["edifici"]:
            if e["stanze"]:
                e["stanze"][0]["licenze"] = ["CC BY-NC 4.0"]
                return d, a
        raise SystemExit("nessuna stanza dove scrivere la licenza")
    if difetto[0] == "I4" and "più delle immagini" in difetto[1]:
        for e in d["edifici"]:
            if e["stanze"]:
                e["stanze"][0]["immagini_libere"] = \
                    e["stanze"][0]["immagini"] + 5
                return d, a
        raise SystemExit("nessuna stanza")
    if difetto[0] == "I3" and "città" in difetto[1]:
        for e in d["edifici"]:
            if e["categoria_commons"] and e["stanze"]:
                e["categoria_commons"] = ("Category:Museo del Risorgimento e "
                                          "della Resistenza (Vicenza)")
                break
        return d, a
    if difetto[0] == "I3" and "opere" in difetto[1]:
        for e in d["edifici"]:
            if e["categoria_commons"] and e["stanze"]:
                e["stanze"].append({
                    "nome": "Paintings in the building",
                    "categoria": "Paintings in the building (Ferrara)",
                    "immagini": 4, "immagini_libere": 4,
                    "licenze": ["ccbysa"],
                    "esemplare": "File:un quadro.jpg",
                    "vuoto": [],
                })
                return d, a
        raise SystemExit("nessun edificio con stanze")
    if difetto[0] == "I6":
        for e in d["edifici"]:
            if e["categoria_commons"] and e["stanze"]:
                copia = e["categoria_commons"]
                for altro in d["edifici"]:
                    if altro is e or not altro["categoria_commons"]:
                        continue
                    altro["categoria_commons"] = copia
                    return d, a
        raise SystemExit("nessun edificio con stanze")
    if difetto[0] == "I5":
        for e in d["edifici"]:
            if not e["categoria_commons"]:
                e["vuoto"] = []
                return d, a
        raise SystemExit("nessun edificio dichiarato assente")
    raise SystemExit("difetto non iniettabile: %r" % (difetto,))


def main():
    dati = leggi(INTERNI)
    ambienti = leggi(AMBIENTI)

    if "--difetti" in sys.argv:
        visti = 0
        for controllo, nome, spiegazione in DIFETTI:
            if controllo == "I7":
                # **il difetto è nel capitolo, non nei dati.** Si scrive una
                # copia alterata in un file temporaneo, si fa guardare quella,
                # e si rimette tutto com'era: la prova non tocca mai il
                # documento vero, che è la regola che vale per tutte le prove
                # di questa famiglia.
                import shutil
                import tempfile
                fd, copia_cap = tempfile.mkstemp(suffix=".md")
                os.close(fd)
                shutil.copyfile(CAPITOLO, copia_cap)
                with io.open(copia_cap, encoding="utf-8") as f:
                    testo = f.read()
                numero = dati["riepilogo"]["stanze"]
                alterato = testo.replace("| stanze trovate | %d |" % numero,
                                         "| stanze trovate | %d |"
                                         % (numero + 3), 1)
                if alterato == testo:
                    os.unlink(copia_cap)
                    print("   NON PROVATO %-3s %s" % (controllo, nome))
                    continue
                with io.open(copia_cap, "w", encoding="utf-8") as f:
                    f.write(alterato)
                salvataggio = CAPITOLO
                globals()["CAPITOLO"] = copia_cap
                try:
                    trovati = [p for c, p in problemi(dati, ambienti)
                               if c == controllo]
                finally:
                    globals()["CAPITOLO"] = salvataggio
                    os.unlink(copia_cap)
                if trovati:
                    visti += 1
                    print("   visto   %-3s %s" % (controllo, nome))
                else:
                    print("   NON VISTO %-3s %s" % (controllo, nome))
                continue
            copia, _ = inietta(dati, ambienti, (controllo, nome, spiegazione))
            trovati = [p for c, p in problemi(copia, ambienti)
                       if c == controllo]
            if trovati:
                visti += 1
                print("   visto   %-3s %s" % (controllo, nome))
            else:
                print("   NON VISTO %-3s %s" % (controllo, nome))
        print("\n== i difetti iniettati")
        print("   visti %d su %d" % (visti, len(DIFETTI)))
        return 0 if visti == len(DIFETTI) else 1

    trovati = problemi(dati, ambienti)
    print("== i controlli sugli interni")
    for controllo, descrizione, _ in CONTROLLI:
        numeri = [p for c, p in trovati if c == controllo]
        print("   %-4s %-2d  %s" % (controllo, len(numeri), descrizione))
    r = dati["riepilogo"]
    print("\n   edifici %d, con categoria %d, con stanze %d; stanze %d "
          "(%d con immagine libera)"
          % (r["edifici"], r["edifici_con_categoria"],
             r["edifici_con_stanze"], r["stanze"],
             r["stanze_con_immagine_libera"]))
    if trovati:
        print("\n== i problemi")
        for controllo, p in trovati:
            print("   %-4s %s" % (controllo, p))
    print("\n   PROBLEMI: %d" % len(trovati))
    return 1 if trovati else 0


if __name__ == "__main__":
    sys.exit(main())