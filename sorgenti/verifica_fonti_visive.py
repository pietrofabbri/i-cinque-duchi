#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifica i due file di fonti visive costruiti il 05/10/2026: **M1–M6** sui
mezzi di trasporto ed **E1–E4** sulle epigrafi.

Nati dalla stessa malattia, e per una ragione che vale più dei due buchi che
chiudono: **un numero vero che guarda il numero sbagliato**. La ricerca del
02/10 dichiarava undici mezzi e il gioco ne usa ventuno, e nessuno dei due
numeri era confrontato con l'altro. Un controllo che confronta il file con se
stesso dà verde su quel difetto: per questo `M1` confronta il file con
**`percorsi_mezzi.py`**, cioè con la fonte dei mezzi, e non con se stesso.

  M1  ogni mezzo del gioco ha una riga, e nessun mezzo e' sparito dal file
  M2  ogni immagine scelta e' fra i candidati della ricerca del 02/10
  M3  ogni mezzo ha **una** delle tre forme: immagine, vuoto con ragione,
      oppure segno fantastico — mai due e mai nessuna
  M4  nessun mezzo fantastico ha un'immagine: sono creature
  M5  i numeri scritti in §3.1 del documento sono quelli del file
  M7  le voci e i candidati della ricerca sono gli stessi nella tabella delle
      categorie, nel frontespizio e nel riepilogo: tre posti, un numero solo
  M6  ogni immagine ha l'attribuzione calcolata, e la licenza libera
  E1  ogni voce epigrafa ha la sua immagine, scelta fra i candidati
  E2  **nessuna epigrafe entra nel gioco senza trascrizione e traduzione**
  E3  nessun testo e' scritto dal progetto: o c'e' con la sua fonte, o e' null
  E4  i numeri scritti in §3.3 del documento sono quelli del file
  I1  una riga per ogni voce della categoria `incidente`, e nessuna in piu'
  I2  **una** delle tre forme ammesse (immagine, testo, non usata), coerente
      col campo immagine, e la sua raguzione scritta
  I3  ogni immagine e' fra i candidati, con l'attribuzione calcolata e la
      licenza libera
  I4  **una voce che nessuna tappa usa deve dichiararlo, e la dichiarazione
      deve essere vera**: la scansione e' rifatta qui, sul documento, e il conto
      del file deve coincidere con quello che esce
  I5  ogni tappa dichiarata esiste, e l'emblema che il file porta e' quello che
      il documento dell'anno dichiara per quella tappa
  I6  i numeri scritti in §6 del documento sono quelli del file

Uso:
    python3 sorgenti/verifica_fonti_visive.py
    python3 sorgenti/verifica_fonti_visive.py --difetti   # ne inietta quattordici
"""
import importlib.util
import io
import json
import os
import re
import sys

RADICE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEZZI = os.path.join(RADICE, "dati", "fonti_visive", "mezzi.json")
EPIGRAFI = os.path.join(RADICE, "dati", "fonti_visive", "epigrafi.json")
INCIDENTI = os.path.join(RADICE, "dati", "fonti_visive", "incidenti.json")
AMBIENTI = os.path.join(RADICE, "dati", "ambienti_livelli.json")
CERCA = os.path.join(RADICE, "dati", "fonti_visive", "fonti_visive.json")
DOC = os.path.join(RADICE, "docs", "videogioco-5-duchi-fonti-visive.md")
MEZZI_PY = os.path.join(RADICE, "sorgenti", "percorsi_mezzi.py")

LIBERE = ("CC BY", "CC0", "Public domain", "PD", "No restrictions", "CC BY-SA")

DOCS = os.path.join(RADICE, "docs")
ANNI = ["anno1-ferrara", "anno2-penisola", "anno3-europa", "anno4-mondo",
        "anno5-mondo"]
# le parole con cui una voce nomina il proprio evento: `moria` non e' l'unica
# parola della peste, ed e' dentro `memoria`. I **confini** non sono un dettaglio
INIZIO_Q = re.compile(r"(?m)^#{2,3} (Q\d+)")
QUALSIASI = re.compile(r"(?m)^#{2,3} ")
EMBLEMA = re.compile(r"\*\*Emblema:\*\*\s*(.+?)\s*$", re.M)
RIGA_TAPPA = re.compile(r"(?m)^\| \*\*(\d-\d{1,2})\*\* \|(.*)$")
FORME = ("immagine", "testo", "non_usata")
# le parole con cui una voce nomina il proprio evento: `moria` non e' l'unica
# parola della peste (la tappa 3-22 scrive «la peste», il 4-27 «mortalita», il
# 5-9 «epidemici»), ed e' dentro `memoria`. I **confini di parola** non sono un
# dettaglio: senza, la moria viene fuori in tutti i 120 blocchi di persona
# invece dei tre che sono suoi.
SINONIMI = {
    "incendio": [r"incendi\w*", r"\bbruci\w*"],
    "moria": [r"\bmoria\b", r"\bpeste\b", r"\bepidemi\w*",
              r"\bmortalit\w*", r"\bcolera\b", r"\bvittime\b"],
    "carestia": [r"\bcarest\w*", r"\bfame\b", r"\bfamine\b"],
}


def leggi(p):
    with io.open(p, encoding="utf-8") as f:
        return json.load(f)


def mezzi_del_gioco():
    spec = importlib.util.spec_from_file_location("percorsi_mezzi", MEZZI_PY)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m.MEZZI


def sezione(testo, titolo, prossimo):
    """Il testo di una sezione: dal titolo al titolo seguente."""
    i = testo.index(titolo)
    j = testo.index(prossimo, i)
    return testo[i:j]


def cifra_in_riga(sezione, inizio_cella):
    """La prima cifra in grassetto della **riga di tabella** che comincia con
    una data cella.

    Serve per `M5` ed `E4`: i numeri scritti nel documento sono confrontati col
    conto **del file**, non fra loro, perché un numero che nessuno ricalcola è
    un numero che invecchia. La prima versione di questa funzione cercava la
    prima cifra che segue la frase, e la frase finiva col grassetto che precede
    il numero: leggeva il numero **successivo** e stampava sei difetti tutti
    suoi, dei quali nessuno era un difetto del documento. Un controllo che
    segnala se stesso è peggio di un controllo che non esiste.
    """
    for riga in sezione.splitlines():
        if riga.strip().startswith("| " + inizio_cella):
            m = re.search(r"\*\*(\d+)\*\*", riga)
            return int(m.group(1)) if m else None
    return None


def scansione_independente(parole):
    """Le tappe che nominano l'evento di una voce, rilette qui dal documento.

    **La stessa lettura due volte, scritta due volte, di proposito.** Se questa
    funzione importasse `incidenti_fonti.scansiona`, un difetto di lettura
    sarebbe lo stesso difetto nel file e nel controllo: il verde direbbe che la
    cosa e' stata guardata due volte mentre e' stata guardata una.

    Le due letture sono diverse di metodo: il generatore isola i blocchi di
    persona e li scandisce uno per uno; questa guarda il documento intero e
    assegna ogni occorrenza al blocco in cui cade. Se un numero e' giusto per
    che lo produce, e' giusto anche dall'altra parte.

    Il primo tentativo metteva i confini del blocco **sull'intestazione** e
    chiedeva che la parola cadesse fra l'inizio e la fine di quelli: ma la
    parola viene dopo l'intestazione, quindi la condizione non era mai vera e la
    scansione restituiva zero tappe per tutte e tre le voci. Un controllo che
    non trova niente non e' un controllo, e I4 se n'e' accorto solo perche' il
    numero del file non tornava.
    """
    pattern = "|".join(parole)
    trovare = []
    for nome in ANNI:
        testo = io.open(os.path.join(DOCS, "videogioco-5-duchi-%s.md" % nome),
                        encoding="utf-8").read()
        # i blocchi di persona: da **dopo** l'intestazione fino alla
        # successiva intestazione di qualunque livello, altrimenti l'ultima
        # persona di ogni anno mangia mezzo documento
        confini = []
        for m in INIZIO_Q.finditer(testo):
            n = QUALSIASI.search(testo, m.end())
            confini.append((m.end(), n.start() if n else len(testo),
                            m.group(1)))
        visti = set()
        for m in re.finditer(pattern, testo, re.I):
            for a, b, codice in confini:
                if not a <= m.start() < b or codice in visti:
                    continue
                visti.add(codice)
                # la tappa dalla riga della tabella, non dalla posizione
                tappa = None
                for r in RIGA_TAPPA.finditer(testo):
                    if re.search(r"\(%s[^0-9]" % codice, r.group(2)):
                        tappa = r.group(1)
                        break
                emblema = EMBLEMA.search(testo[a:b])
                trovare.append((nome, codice, tappa,
                                emblema.group(1).strip() if emblema else None))
                break
    return trovare


def controlla(problemi, iniettato=None):
    mezzi = leggi(MEZZI)
    epi = leggi(EPIGRAFI)
    del_gioco = mezzi_del_gioco()
    ricerca = leggi(CERCA)["risultati"]
    testo = io.open(DOC, encoding="utf-8").read()

    # M1: una riga per ogni mezzo del gioco, e nessun mezzo in piu'
    righe = {v["mezzo"] for v in mezzi["mezzi"]}
    for nome in sorted(set(del_gioco) - righe):
        problemi.append("M1: il mezzo %s e' in percorsi_mezzi.py e non in "
                        "mezzi.json" % nome)
    for nome in sorted(righe - set(del_gioco)):
        problemi.append("M1: mezzi.json ha %s, che il gioco non usa" % nome)

    # M2: ogni immagine scelta e' fra i candidati della ricerca
    candidati = {c["file"] for v in ricerca["mezzo"] for c in v["candidati"]}
    for v in mezzi["mezzi"]:
        if v["immagine"] and v["immagine"]["file"] not in candidati:
            problemi.append("M2: l'immagine di %s non e' fra i candidati della "
                            "ricerca: %s" % (v["mezzo"], v["immagine"]["file"]))

    # M3: esattamente una delle tre forme, e il vuoto ha la sua ragione
    for v in mezzi["mezzi"]:
        forme = [bool(v["immagine"]), bool(v["vuoto"]), bool(v["segno"])]
        if sum(forme) != 1:
            problemi.append("M3: il mezzo %s ha %d forme (immagine %s, vuoto "
                            "%s, segno %s): deve averne una"
                            % (v["mezzo"], sum(forme), bool(v["immagine"]),
                               bool(v["vuoto"]), bool(v["segno"])))
        elif v["vuoto"] and len(v["vuoto"]) < 25:
            problemi.append("M3: il vuoto di %s non ha la ragione" % v["mezzo"])

    # M4: nessun mezzo fantastico ha un'immagine
    for v in mezzi["mezzi"]:
        if v["tipo"] == "gioco" and v["immagine"]:
            problemi.append("M4: %s e' un mezzo fantastico e ha un'immagine: "
                            "le creature non si fotografano" % v["mezzo"])

    # M6: l'attribuzione calcolata e la licenza libera
    for v in mezzi["mezzi"]:
        if not v["immagine"]:
            continue
        if not v["attribuzione"] or len(v["attribuzione"]) < 10:
            problemi.append("M6: %s ha un'immagine senza attribuzione"
                            % v["mezzo"])
        if not any(l in (v["immagine"]["licenza"] or "") for l in LIBERE):
            problemi.append("M6: la licenza di %s non e' fra quelle libere: %r"
                            % (v["mezzo"], v["immagine"]["licenza"]))

    # M5: i numeri scritti in 3.1 sono quelli del file
    s31 = sezione(testo, "### 3.1 I mezzi di trasporto", "### 3.2 ")
    for cella, chiave in (("Mezzi del gioco", "mezzi"),
                          ("Con immagine proposta", "con_immagine"),
                          ("Storici **senza** immagine", "storici_senza_immagine"),
                          ("Fantastici con segno dedicato", "fantastici_con_segno"),
                          ("Candidati esaminati", "candidati_esaminati")):
        atteso = mezzi["conti"][chiave]
        trovato = cifra_in_riga(s31, cella)
        if trovato is None:
            problemi.append("M5: la sezione 3.1 non dichiara la riga «%s»"
                            % cella)
        elif trovato != atteso:
            problemi.append("M5: la sezione 3.1 dichiara %d per «%s», il file %d"
                            % (trovato, cella, atteso))

    # E1: ogni voce ha la sua immagine, scelta fra i candidati
    cand_epi = {c["file"] for v in ricerca["epigrafe"] for c in v["candidati"]}
    for v in epi["voci"]:
        if not v["immagine"]:
            problemi.append("E1: la voce %s non ha immagine" % v["voce"])
        elif v["immagine"]["file"] not in cand_epi:
            problemi.append("E1: l'immagine di %s non e' fra i candidati: %s"
                            % (v["voce"], v["immagine"]["file"]))

    # E2: nessuna epigrafe entra senza trascrizione e traduzione
    for v in epi["voci"]:
        if v["entra_nel_gioco"] and not (v["trascrizione"] and v["traduzione"]):
            problemi.append("E2: %s entra nel gioco senza la trascrizione e la "
                            "traduzione: una foto di un sasso non e' un testo"
                            % v["voce"])
        if v["entra_nel_gioco"] and not v.get("fonte_del_testo"):
            problemi.append("E2: %s entra nel gioco senza la fonte del testo"
                            % v["voce"])

    # E3: nessun testo scritto dal progetto
    for v in epi["voci"]:
        for campo in ("trascrizione", "traduzione"):
            if v[campo] is not None and "fonte" not in str(v[campo]).lower():
                problemi.append("E3: il/la %s di %s non porta la sua fonte: "
                                "un testo generato dal progetto e' vietato"
                                % (campo, v["voce"]))

    # M7: i numeri delle voci e dei candidati, che sono il numero piu'
    # invecchiato del capitolo: la tabella delle categorie, il frontespizio e il
    # riepilogo portavano tutti 27 voci e 125 candidati il giorno in cui cinque
    # nuove voci sono entrate nel file di ricerca. Nessuno dei tre si muove da
    # solo, e sono tre posti in cui un numero sbagliato non produce alcun
    # errore: il file era giusto e il documento no.
    voci_ricerca = candidati_ricerca = 0
    for vv in ricerca.values():
        voci_ricerca += len(vv)
        for v in vv:
            candidati_ricerca += len(v["candidati"])
    # la riga del totale ha due numeri: il primo e' il totale delle voci
    riga_tot = [r for r in testo.splitlines()
                if r.strip().startswith("| **Totale** | **")]
    if not riga_tot:
        problemi.append("M7: non c'e' la riga del totale nella tabella delle "
                        "categorie")
    else:
        numeri = [int(x) for x in __import__("re").findall(r"\*\*(\d+)\*\*",
                                                           riga_tot[0])]
        if numeri[:2] != [voci_ricerca, candidati_ricerca]:
            problemi.append("M7: la tabella delle categorie dichiara %s voci e "
                            "%s candidati, il file di ricerca ne ha %d e %d"
                            % (numeri[0], numeri[1], voci_ricerca,
                               candidati_ricerca))
    m = __import__("re").search(r"Candidati cercati su Commons \| \*\*(\d+)\*\*, "
                        r"in (\d+) voci", testo)
    if not m:
        problemi.append("M7: il riepilogo non dichiara i candidati cercati")
    elif (int(m.group(1)), int(m.group(2))) != (candidati_ricerca, voci_ricerca):
        problemi.append("M7: il riepilogo dichiara %s candidati in %s voci, il "
                        "file di ricerca ne ha %d in %d"
                        % (m.group(1), m.group(2), candidati_ricerca,
                           voci_ricerca))
    m = __import__("re").search(r"fonti_visive\.json \(v\d+, (\d+) voci, "
                        r"(\d+) candidati\)", testo)
    if not m:
        problemi.append("M7: il frontespizio non dichiara le voci e i candidati "
                        "del file di ricerca")
    elif (int(m.group(1)), int(m.group(2))) != (voci_ricerca, candidati_ricerca):
        problemi.append("M7: il frontespizio dichiara %s voci e %s candidati, "
                        "il file ne ha %d e %d"
                        % (m.group(1), m.group(2), voci_ricerca,
                           candidati_ricerca))

    # E4: i numeri scritti in 3.3 sono quelli del file
    s33 = sezione(testo, "### 3.3 Le epigrafi", "### 3.4 ")
    for cella, chiave in (("Voci", "voci"),
                          ("Candidati", "candidati"),
                          ("Con immagine scelta", "con_immagine"),
                          ("Con trascrizione e traduzione",
                           "con_trascrizione_e_traduzione"),
                          ("Che entrano nel gioco", "entrano_nel_gioco")):
        atteso = epi["conti"][chiave]
        trovato = cifra_in_riga(s33, cella)
        if trovato is None:
            problemi.append("E4: la sezione 3.3 non dichiara la riga «%s»"
                            % cella)
        elif trovato != atteso:
            problemi.append("E4: la sezione 3.3 dichiara %d per «%s», il file %d"
                            % (trovato, cella, atteso))

    # I1: una riga per ogni voce della categoria, e nessuna in piu'. Il
    # confronto e' con `fonti_visive.json`, che e' la fonte delle voci cercate:
    # un controllo che confronta il file con se stesso darebbe verde anche
    # su un file che ha perso una voce.
    inc = leggi(INCIDENTI)
    voci_cercate = [v["voce"] for v in ricerca["incidente"]]
    righe = [v["voce"] for v in inc["voci"]]
    for nome in sorted(set(voci_cercate) - set(righe)):
        problemi.append("I1: la voce %s e' fra quelle cercate e non ha una "
                        "riga in incidenti.json" % nome)
    for nome in sorted(set(righe) - set(voci_cercate)):
        problemi.append("I1: incidenti.json ha la voce %s, che la ricerca non "
                        "ha mai cercato" % nome)

    # I2: una forma sola fra le tre ammesse, coerente col campo immagine, e la
    # ragione scritta. Il vuoto non e' una forma: un vuoto senza ragione e' un
    # buco travestito da risposta.
    for v in inc["voci"]:
        forma = v["forma"]
        if forma not in FORME:
            problemi.append("I2: la voce %s ha la forma %r, che non e' una "
                            "delle tre: %s" % (v["voce"], forma,
                                               ", ".join(FORME)))
        elif (forma == "immagine") != bool(v["immagine"]):
            problemi.append("I2: la voce %s si dichiara %s ma %s"
                            % (v["voce"], forma,
                               "porta un'immagine" if v["immagine"] else
                               "non ne porta"))
        if len(v.get("perche_questa_forma") or "") < 25:
            problemi.append("I2: la voce %s non ha la ragione della sua forma"
                            % v["voce"])
        if (forma == "non_usata") != bool(v.get("perche_non_usata")):
            problemi.append("I2: la voce %s ha la forma %s e %s"
                            % (v["voce"], forma,
                               "dichiara perche' non e' usata" if
                               v.get("perche_non_usata") else
                               "dichiara perche' non e' usata ma non lo e'"))

    # I3: l'immagine e' fra i candidati, con l'attribuzione calcolata e la
    # licenza libera
    cand_inc = {c["file"] for vv in ricerca["incidente"]
                for c in vv["candidati"]}
    for v in inc["voci"]:
        if not v["immagine"]:
            continue
        if v["immagine"]["file"] not in cand_inc:
            problemi.append("I3: l'immagine di %s non e' fra i candidati: %s"
                            % (v["voce"], v["immagine"]["file"]))
        if not v["attribuzione"] or len(v["attribuzione"]) < 10:
            problemi.append("I3: %s ha un'immagine senza attribuzione"
                            % v["voce"])
        if not any(l in (v["immagine"]["licenza"] or "") for l in LIBERE):
            problemi.append("I3: la licenza di %s non e' fra quelle libere: %r"
                            % (v["voce"], v["immagine"]["licenza"]))

    # I4: la dichiarazione «nessuna tappa la usa» deve essere **vera**, e la
    # scansione la rifà qui. E' il difetto che questa chiusura chiude: la
    # carestia era una voce cercata che nessuna tappa nomina, e nessuno lo
    # aveva detto perche' il numero che si guardava era un altro.
    ambienti = {a["livello"] for a in leggi(AMBIENTI)["ambienti"]}
    for v in inc["voci"]:
        parole = SINONIMI.get(v["voce"])
        if not parole:
            problemi.append("I4: la voce %s non ha le parole con cui cerca "
                            "l'evento: senza, non si puo' dire se una tappa la "
                            "nomina" % v["voce"])
            continue
        trovate = scansione_independente(parole)
        dichiarate = [u["tappa"] for u in v["usata_da"]]
        reali = [t for _, _, t, _ in [(a, b, c, d) for a, b, c, d in trovate]]
        if sorted(reali) != sorted(dichiarate):
            problemi.append("I4: la voce %s dichiara le tappe %s e la scansione "
                            "sui documenti trova %s"
                            % (v["voce"], dichiarate or ["nessuna"],
                               reali or ["nessuna"]))
        if not dichiarate and not v.get("perche_non_usata"):
            problemi.append("I4: la voce %s non e' usata da nessuna tappa e "
                            "non dichiara perche'" % v["voce"])
        if dichiarate and v.get("perche_non_usata"):
            problemi.append("I4: la voce %s dichiara di non essere usata ma %d "
                            "tappe la nominano" % (v["voce"], len(dichiarate)))
        if len(v["usata_da"]) != v["scansione"]["tappe_che_nominano_l_evento"]:
            problemi.append("I4: la voce %s dichiara %d tappe che la nominano "
                            "e ne elenca %d"
                            % (v["voce"],
                               v["scansione"]["tappe_che_nominano_l_evento"],
                               len(v["usata_da"])))

    # I5: ogni tappa dichiarata esiste fra i centocinquanta livelli, e l'emblema
    # che il file porta e' quello che il documento dell'anno dichiara per
    # quella tappa. Il codice `Q` e' in due posti — la riga della tabella delle
    # tappe e l'intestazione della scheda — e i due posti devono dire la stessa
    # persona: senza questo controllo, un emblema sbagliato nel file restava
    # un emblema giusto in due copie.
    for v in inc["voci"]:
        for u in v["usata_da"]:
            if u["tappa"] not in ambienti:
                problemi.append("I5: la voce %s usa la tappa %s, che non e' fra "
                                "i centocinquanta livelli"
                                % (v["voce"], u["tappa"]))
                continue
            percorso = os.path.join(RADICE, u["dove"])
            # **non** `testo`: quello e' il capitolo, che I6 rilegge dopo, e
            # un nome riassegnato dentro una funzione e' la funzione intera
            doc_anno = io.open(percorso, encoding="utf-8").read()
            riga = next((r for r in RIGA_TAPPA.finditer(doc_anno)
                         if r.group(1) == u["tappa"]), None)
            if riga is None or not re.search(r"\(%s[^0-9]" % u["persona"],
                                             riga.group(2)):
                problemi.append("I5: la riga della tappa %s non nomina %s"
                                % (u["tappa"], u["persona"]))
                continue
            # `sezione` e' una funzione di questo modulo (M5 ed E4 la
            # chiamano): qui la variabile si chiama `scheda`, perche' in Python
            # un nome assegnato in un punto della funzione e' locale in tutta
            # la funzione, e le chiamate di prima avrebbero smesso di trovarla
            # la scheda **di quel codice**: `search` sulla prima intestazione
            # dopo la riga prendeva Q201 in ogni anno, e sei emblemi su sei
            # erano quello sbagliato
            scheda = re.search(r"(?m)^#{2,3} %s\b" % u["persona"], doc_anno)
            fine = QUALSIASI.search(doc_anno, scheda.end())
            blocco = doc_anno[scheda.end():fine.start()] if fine \
                else doc_anno[scheda.end():]
            emblema = EMBLEMA.search(blocco)
            if not emblema:
                problemi.append("I5: la scheda di %s non ha l'emblema" % u["persona"])
            elif emblema.group(1).strip() != u["emblema"]:
                problemi.append("I5: l'emblema di %s nel file e' %r, e nel "
                                "documento e' %r"
                                % (u["tappa"], u["emblema"],
                                   emblema.group(1).strip()))

    # I6: i numeri scritti in 6 sono quelli del file
    s6 = sezione(testo, "## 6. I due vuoti dichiarati, e come stanno adesso",
                 "## 6bis.")
    for cella, chiave in (("Voci della categoria", "voci"),
                          ("Candidati esaminati", "candidati"),
                          ("Con immagine scelta", "con_immagine"),
                          ("Col testo al posto", "col_testo_al_posto"),
                          ("Voci che il gioco non usa", "non_usate"),
                          ("Persone scandite", "persone_scansionate"),
                          ("Tappe che nominano", "tappe_che_nominano_un_incidente"),
                          ("Senza i confini di parola", "senza_confini_di_parola")):
        atteso = inc["conti"][chiave]
        trovato = cifra_in_riga(s6, cella)
        if trovato is None:
            problemi.append("I6: la sezione 6 non dichiara la riga «%s»"
                            % cella)
        elif trovato != atteso:
            problemi.append("I6: la sezione 6 dichiara %d per «%s», il "
                            "file %d" % (trovato, cella, atteso))
    return problemi


def inietta(quale):
    """Un difetto alla volta, perche' insieme la prova si ferma al primo."""
    if quale == "M1":
        p = MEZZI
        d = leggi(p)
        d["mezzi"] = [v for v in d["mezzi"] if v["mezzo"] != "moto"]
        return p, json.dumps(d, ensure_ascii=False, indent=1) + "\n"
    if quale == "M2":
        p = MEZZI
        d = leggi(p)
        for v in d["mezzi"]:
            if v["immagine"]:
                v["immagine"]["file"] = "File:inventato.jpg"
                break
        return p, json.dumps(d, ensure_ascii=False, indent=1) + "\n"
    if quale == "M4":
        p = MEZZI
        d = leggi(p)
        for v in d["mezzi"]:
            if v["tipo"] == "gioco":
                v["segno"] = None
                v["immagine"] = {"file": "File:drago.jpg", "url": "x",
                                 "licenza": "CC0", "autore": "x",
                                 "data": "1500", "px": [100, 100]}
                v["vuoto"] = "un drago dipinto del Quattrocento"
                break
        return p, json.dumps(d, ensure_ascii=False, indent=1) + "\n"
    if quale == "M7":
        p = DOC
        t = io.open(p, encoding="utf-8").read()
        return p, t.replace("| **Totale** | **32** | **130**",
                            "| **Totale** | **27** | **125**", 1)
    if quale == "E2":
        p = EPIGRAFI
        d = leggi(p)
        d["voci"][0]["entra_nel_gioco"] = True
        return p, json.dumps(d, ensure_ascii=False, indent=1) + "\n"
    if quale == "E3":
        p = EPIGRAFI
        d = leggi(p)
        d["voci"][0]["trascrizione"] = "D(is) M(anibus) / POMponio"
        return p, json.dumps(d, ensure_ascii=False, indent=1) + "\n"
    if quale == "M5":
        p = DOC
        t = io.open(p, encoding="utf-8").read()
        return p, t.replace("| Mezzi del gioco | **21**", "| Mezzi del gioco | **11**", 1)
    if quale == "E4":
        p = DOC
        t = io.open(p, encoding="utf-8").read()
        # il difetto va nella **riga che il controllo legge**: la prosa non
        # viene guardata, e la prima versione della prova ci metteva un numero
        # in lettera, cosi' il difetto non c'era nemmeno
        return p, t.replace("| Candidati esaminati | **18**",
                            "| Candidati esaminati | **30**", 1)
    if quale == "I1":
        p = INCIDENTI
        d = leggi(p)
        d["voci"] = [v for v in d["voci"] if v["voce"] != "carestia"]
        return p, json.dumps(d, ensure_ascii=False, indent=1) + "\n"
    if quale == "I2":
        p = INCIDENTI
        d = leggi(p)
        for v in d["voci"]:
            if v["voce"] == "incendio":
                # il difetto e' una forma che non e' fra le tre: il vuoto.
                # Sembra la cosa piu' onesta del mondo ed e' il buco che il
                # capitolo aveva dichiarato per due mesi
                v["forma"] = "vuoto"
                break
        return p, json.dumps(d, ensure_ascii=False, indent=1) + "\n"
    if quale == "I3":
        p = INCIDENTI
        d = leggi(p)
        for v in d["voci"]:
            if v["immagine"]:
                v["immagine"]["file"] = "File:inventato.jpg"
                break
        return p, json.dumps(d, ensure_ascii=False, indent=1) + "\n"
    if quale == "I4":
        p = INCIDENTI
        d = leggi(p)
        for v in d["voci"]:
            if v["voce"] == "carestia":
                # la voce che nessuna tappa nomina si dichiara usata dalla
                # 4-15: un numero vero accanto a una lista inventata
                v["usata_da"] = [{
                    "tappa": "4-15", "persona": "Q215",
                    "dove": "docs/videogioco-5-duchi-anno4-mondo.md",
                    "la_parola": "carestia",
                    "la_frase": "frase inventata",
                    "emblema": "un'emblema inventato",
                }]
                v["scansione"]["tappe_che_nominano_l_evento"] = 1
                break
        return p, json.dumps(d, ensure_ascii=False, indent=1) + "\n"
    if quale == "I5":
        p = INCIDENTI
        d = leggi(p)
        for v in d["voci"]:
            for u in v["usata_da"]:
                if u["tappa"] == "4-10":
                    u["emblema"] = "una fiamma che mangia un archivio"
                    return p, json.dumps(d, ensure_ascii=False, indent=1) + "\n"
        raise ValueError("la tappa 4-10 non e' fra le usate")
    if quale == "I6":
        p = DOC
        t = io.open(p, encoding="utf-8").read()
        return p, t.replace("| Tappe che nominano | **6**",
                            "| Tappe che nominano | **5**", 1)
    raise ValueError(quale)


def main():
    difetti_prova = [a for a in sys.argv if a.startswith("--difetti")]
    problemi = controlla([])
    print("== M1-M7, E1-E4 e I1-I6. i mezzi, le epigrafi e gli incidenti")
    if problemi:
        for p in problemi:
            print("   difetto %s" % p)
    else:
        print("   ogni mezzo ha una forma, i numeri delle due sezioni e del "
              "frontespizio sono\n   quelli del file, nessuna epigrafe entra "
              "nel gioco senza testo, e ogni incidente ha\n   una forma, una "
              "ragione e una scansione che torna sui documenti")

    if not difetti_prova:
        return 1 if problemi else 0

    print("\nprova: un difetto alla volta, coi file rimessi a posto")
    iniettati = visti = 0
    for quale in ("M1", "M2", "M4", "M5", "M7", "E2", "E3", "E4",
                  "I1", "I2", "I3", "I4", "I5", "I6"):
        percorso, nuovo = inietta(quale)
        prima = io.open(percorso, encoding="utf-8").read()
        if nuovo == prima:
            print("   NON INIETTATO  %s: il difetto non cambierebbe il file"
                  % quale)
            continue
        try:
            io.open(percorso, "w", encoding="utf-8").write(nuovo)
            trovati = controlla([])
            # **Visto vuol dire visto da quel controllo.** Accettare che un
            # difetto sia notato da un controllo diverso nasconde i controlli
            # che non guardano: l'M4 iniettava un'immagine a un mezzo
            # fantastico e la segnalava M2, perche' l'immagine non era fra i
            # candidati. Il difetto era visto, il controllo no.
            visto = any(p.startswith(quale + ":") for p in trovati)
            altri = [p[:60] for p in trovati if not p.startswith(quale + ":")]
            iniettati += 1
            visti += 1 if visto else 0
            print("   %-4s %s%s" % (quale, "VISTO" if visto else "NON VISTO",
                                   (": %s" % trovati[0][:80]) if trovati else
                                   " (nessun difetto: la prova non ha provato)"))
            if altri and visto:
                print("        altri controlli che l'hanno visto: %s" % altri)
        finally:
            io.open(percorso, "w", encoding="utf-8").write(prima)
    print("\ndifetti iniettati: %d, visti: %d" % (iniettati, visti))
    return 0 if (iniettati == visti and not problemi) else 1


if __name__ == "__main__":
    sys.exit(main())