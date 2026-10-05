#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""I controlli sui controlli: X1-X6.

Il progetto ha trentatre verificatori e oltre duecento controlli. Fino al 5
ottobre 2026 nessuno di quei numeri era guardato da nessuno: un verificatore
poteva perdere un controllo, o un documento poteva dire «dieci controlli» per
uno script che ne ha venti, e la batteria restava verde lo stesso. Questo
controllo guarda se stessi i guardi.

  X1  le etichette dichiarate sono intere: nessun numero saltato, nessuna
      etichetta due volte, e l'ordine del docstring è quello dei numeri
  X2  ogni controllo dichiarato è guardato dal codice: compare almeno una
      volta, fuori dal docstring, in una riga che riporta un problema
  X3  i numeri che i documenti scrivono sui controlli sono quelli del codice
  X4  ogni verificatore dichiara i suoi controlli, o il motivo per cui non li
      dichiara: nessuno resta fuori dal conto senza essere detto
  X5  la prova del difetto esiste e funziona: `--difetti` viene eseguito e deve
      uscire 0 dicendo di aver visto almeno un difetto
  X6  il conto dei controlli senza prova e' dichiarato nel README, e non cresce
      da solo

**Il conto e' dichiarato, non tollerato.** Un controllo che non ha mai visto
fallire niente e' verde come un controllo che ha visto fallire: finche' la
prova non c'e', il buco e' un buco. Registrarne il numero nel README e' la
differenza fra un debito e una sparizione silenziosa, ed e' quello che X6
controlla: se il numero cresce senza che il documento venga aggiornato, il
controllo e' rosso anche se tutti gli altri sono verdi.

**Il verso che X2 non prende, dichiarato perche' non e' un difetto.** X2
guarda dai controlli dichiarati al codice, non dal codice ai dichiarati. Il
motivo e' che in questo progetto le etichette dei difetti iniettati sono
indistinguibili da quelle dei controlli: in `art/verifica_premi_emblemi.py` i
difetti sono `F1`-`F7` e i controlli sono `Q1`-`Q7`, e chiedere «quale
etichetta non e' stata dichiarata?» risponderebbe `F1`...`F7` ogni volta. Un
controllo che grida sul lupo non e' un controllo.

Uso:  python3 sorgenti/verifica_prove.py
      python3 sorgenti/verifica_prove.py --difetti    # ne inietta sei, uno per volta
"""
import ast
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile

RADICE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Il registro dei buchi del progetto sta in un file solo:
# i tre elenchi non si scrivono qui.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import buchi  # noqa: E402

# **Le due forme in cui un verificatore dichiara i propri controlli**, e sono
# due perche' il progetto ne ha due: l'elenco `  X1  testo` nei docstring di
# quasi tutti, e la tabella `| **X1** | testo |` in quello degli interni. Un
# controllo che riconosce una forma sola chiama «nessuna dichiarazione» un
# documento che dichiara: e' la malattia di RIGA_ELENCO in `verifica_registri.py`,
# che non riconosceva il terzo formato del registro e lasciava fuori il
# documento in cui il difetto era nato.
LISTA = re.compile(r"^  ([A-Z]\d+) +\S", re.M)
TABELLA = re.compile(r"^\|\s*\*\*([A-Z]\d+)\*\*\s*\|", re.M)

# Le etichette che il progetto scrive per un'etichetta: i numeri in parole dei
# documenti, fino a «trenta». Le scritte in cifre non hanno bisogno di essere
# riconosciute: sono gia' un numero, e un numero si confronta col numero.
PAROLE = {
    "un": 1, "uno": 1, "una": 1, "due": 2, "tre": 3, "quattro": 4,
    "cinque": 5, "sei": 6, "sette": 7, "otto": 8, "nove": 9, "dieci": 10,
    "undici": 11, "dodici": 12, "tredici": 13, "quattordici": 14,
    "quindici": 15, "sedici": 16, "diciassette": 17, "diciotto": 18,
    "diciannove": 19, "venti": 20, "ventuno": 21, "ventidue": 22,
    "ventitre": 23, "ventiquattro": 24, "venticinque": 25, "ventisei": 26,
    "ventisette": 27, "ventotto": 28, "ventinove": 29, "trenta": 30,
}
# Una riga che riporta un problema: e' la prova che il controllo dichiarato
# arriva davvero a guardare qualcosa. Le forme sono quelle usate dai
# verificatori: l'append al elenco dei problemi, la stampa del titolo del
# controllo (`print("== L1. ...")`) e le due funzioni che ci mettono dentro il
# loro esito.
RIORTA = re.compile(r"print\(|problemi\.append|problemi\.extend|"
                    r"\besito\(|\besiti\.append|raise ")

# Il nome di un verificatore, come lo scrivono il README, AGENTS e i documenti.
NOMINATO = re.compile(r"\b(?:[\w.-]+/)?verifica_[a-z0-9_]+\.py\b")
# «dieci controlli», «**cinque** controlli», «57 controlli»: un numero e la
# parola che lo nomina. La parola viene cercata prima del numero perche' in
# `fonti-visive.md` la forma e' «sei verifiche (A1–A6)» e in `luoghi.md`
# «la riga accanto dichiarava 57 controlli sulle mappe», che non sono
# controlli di nessuno: X3 pretende che il numero e la parola siano nella
# stessa clausola dello script, e se non lo sono non lo guarda.
CONTA = re.compile(r"\b(\d{1,3}|[a-z]+)\s+(?:controlli|verifiche|prove)\b")
# `M1-M6`, `A1–A6`, `R1—R4`: un intervallo di etichette dello stesso prefisso.
INTERVALLO = re.compile(r"(?<![A-Za-z0-9])([A-Z])(\d{1,2})\s*[-–—]\s*\1(\d{1,2})"
                        r"(?![0-9])")
# La sezione del registro delle modifiche: dentro, un numero descrive che cosa
# era vero il giorno in cui la riga e' stata scritta, non che cosa e' vero adesso.
# `fonti-visive.md` §9 dice ancora «dieci controlli M1-M6 ed E1-E4» perche' in
# quel giorno erano dieci: leggerlo come il presente e' il difetto che questo
# controllo doveva trovare, e non lo deve trovare li'.
REGISTRO = re.compile(r"(?m)^#{2,3} .*[Rr]egistro")
INTESTAZIONE = re.compile(r"(?m)^#{2,3} ")

# Il conto che il README deve dichiarare (X6). La chiave e' la riga della
# tabella, senza la colonna finale; il valore e' il numero che quella riga
# promette. Le righe mancanti sono un difetto: una tabella che si accorcia
# quando un difetto viene corretto e' una tabella che non e' un dato.
CONTI = {
    "Verificatori nel ramo": "verificatori",
    "Verificatori che dichiarano i loro controlli": "dichiarano",
    "Verificatori senza dichiarazione": "taciti",
    "Controlli dichiarati in tutto": "controlli",
    "Controlli con la prova del difetto": "provati",
    "Controlli senza prova": "senza_prova",
    "Prove eseguite da questo controllo": "prove_eseguite",
}
SEZIONE_CONTO = "## Il conto dei controlli"

# **I verificatori che non dichiarano i loro controlli, e perche'.** Non e' una
# lista di scuse: e' il posto dove ogni buco dichiarato sta scritto, e X4 e'
# rosso se un verificatore senza dichiarazione non e' qui, o se uno qui adesso
# dichiara. Il secondo caso e' il piu' importante: e' il difetto che lascia la
# lista indietro rispetto alla realta', ed e' successo: `verifica_interni.py`
# dichiara I1-I7 in una tabella e questa lista lo contava fra i taciti.
#
# **I motivi non si scrivono qui**: stanno in `dati/buchi_aperto.json`, che è
# l'unico registro dei buchi del progetto, e si leggono da `sorgenti/buchi.py`.
# Un elenco in tre file non è un registro: quando ne nasce uno in uno solo dei
# tre, nessuno lo vede.
TACITI = buchi.elenco("TACITI")


# --------------------------------------------------------------------------
def leggi(path):
    with io.open(path, encoding="utf-8") as f:
        return f.read()


def scrivi(path, testo):
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(testo)


def docstring(testo):
    """Il docstring del modulo, e il resto del file.

    **Il taglio lo fa `ast`, non una divisione sulle virgolette triple.**
    Questo file ne contiene dentro le stringhe che costruiscono lo stub di X5,
    e la divisione troncava il corpo a meta: X2 e X3 risultavano dichiarati e
    non guardati da nessuna parte, cioe' il controllo che doveva vedere i
    difetti si dichiarava per primo. Il posto giusto del docstring lo sa
    l'albero sintattico, non una ricerca di caratteri.
    """
    righe = testo.splitlines()
    try:
        albero = ast.parse(testo)
    except SyntaxError:
        return "", testo
    if not albero.body:
        return "", testo
    primo = albero.body[0]
    if not (isinstance(primo, ast.Expr)
            and isinstance(primo.value, ast.Constant)
            and isinstance(primo.value.value, str)):
        return "", testo
    valore = primo.value
    fine = valore.end_lineno or valore.lineno
    dentro = righe[valore.lineno - 1:fine]
    fuori = [r for i, r in enumerate(righe, 1)
             if not (valore.lineno <= i <= fine)]
    return "\n".join(dentro), "\n".join(fuori)


def dichiarate(testo):
    """Le etichette che il file dichiara, nell'ordine in cui le dichiara."""
    doc, _ = docstring(testo)
    fuori = []
    for m in LISTA.finditer(doc):
        if m.group(1) not in fuori:
            fuori.append(m.group(1))
    for m in TABELLA.finditer(doc):
        if m.group(1) not in fuori:
            fuori.append(m.group(1))
    return fuori


# La finestra dell'istruzione: `problemi.append(` sta spesso sulla riga prima
# dell'etichetta, e chiedere «l'etichetta e' sulla stessa riga di un append?»
# rispondeva no su quattro controlli che guardano davvero, fra cui due di
# questo file. Il taglio alla riga vuota tiene la finestra dentro
# l'istruzione: dopo un blank line comincia un'altra frase.
FINESTRA_ISTRUZIONE = 260


def riportate(testo, etichetta):
    """Il controllo arriva a guardare qualcosa, o e' una riga di spiegazione?"""
    _, corpo = docstring(testo)
    # lo sguardo guarda anche dentro `G2/G3/G5`, dove tre controlli si
    # riportano nella stessa frase: separarli con la barra e' una scelta di
    # scrittura, non un controllo che non guarda niente
    pat = re.compile(r"(?<![A-Za-z0-9])%s(?![0-9])" % re.escape(etichetta))
    for m in RIORTA.finditer(corpo):
        finestra = corpo[m.start():m.start() + FINESTRA_ISTRUZIONE]
        vuoto = finestra.find("\n\n")
        if vuoto > 0:
            finestra = finestra[:vuoto]
        if pat.search(finestra):
            return True
    return False


def prove_dichiostrate(testo):
    return "--difetti" in testo


def per_prefisso(etichette):
    gruppi = {}
    for e in etichette:
        gruppi.setdefault(e[0], []).append(int(e[1:]))
    return dict((p, v) for p, v in gruppi.items())


# **La finestra del confronto di X3**, in caratteri, davanti e dietro il nome
# dello script. Il numero che riguarda uno script sta accanto al suo nome —
# «`verifica_registri.py` (R1-R5)», «... con nove controlli, B1-B9)»: troppo
# lontano non e' piu' il suo numero, e leggerlo come suo e' il difetto che una
# riga lunga porta dentro se stessa (`luoghi.md` §4.8 nomina il B8 di
# `verifica_ambienti.py` e, nella stessa riga, «57 controlli sulle mappe»).
FINESTRA_PROSA = 120


def intorno(nome, riga):
    """Il pezzo di riga di cui il numero puo' essere, davanti e dietro."""
    i = riga.find(nome)
    return riga[max(0, i - FINESTRA_PROSA):i + len(nome) + FINESTRA_PROSA]


def righe_utili(testo):
    """Le righe che non stanno dentro il registro, con il loro numero vero.

    Il numero e' quello della riga nel file, non quello nella porzione
    tagliata: un difetto segnalato alla riga sbagliata si cerca due volte.
    """
    dentro = REGISTRO.search(testo)
    prima = dentro.start() if dentro else len(testo)
    coppie = []
    posizione = 0
    for numero_riga, riga in enumerate(testo.splitlines(), 1):
        prossima = posizione + len(riga) + 1
        if posizione < prima:
            coppie.append((numero_riga, riga))
        posizione = prossima
    return coppie


def numero(riga):
    m = CONTA.search(riga)
    if not m:
        return None
    parola = m.group(1)
    if parola.isdigit():
        return int(parola)
    return PAROLE.get(parola)


# --------------------------------------------------------------------------
def controlla(sorgenti, documenti, problemi, esegui=None):
    """I sei controlli su un albero di file in memoria.

    `sorgenti` e `documenti` sono dizionari {percorso: testo}, cosi' che la
    prova `--difetti` possa lavorare su copie e non sui file veri: un difetto
    iniettato che toccasse un documento vero lascerebbe il ramo peggio di come
    l'ha trovato, e il progetto ha una regola su questo.
    """
    # ---- X1: etichette intere, e in ordine
    for rel in sorted(sorgenti):
        testo = sorgenti[rel]
        et = dichiarate(testo)
        for pref, numeri in sorted(per_prefisso(et).items()):
            if sorted(numeri) != list(range(1, len(numeri) + 1)):
                ripetuti = [n for n in set(numeri) if numeri.count(n) > 1]
                mancanti = sorted(set(range(1, max(numeri) + 1)) - set(numeri))
                problemi.append(
                    "X1 %s: le etichette %s non sono 1..%d%s%s" % (
                        rel, pref, len(numeri),
                        ", ripetute: %s" % ",".join("%s%d" % (pref, n)
                                                   for n in sorted(ripetuti))
                        if ripetuti else "",
                        ", mancanti: %s" % ",".join("%s%d" % (pref, n)
                                                    for n in mancanti)
                        if mancanti else ""))
            if numeri != sorted(numeri):
                problemi.append(
                    "X1 %s: le etichette %s sono fuori ordine (%s): l'ordine "
                    "del docstring e' quello dei numeri"
                    % (rel, pref,
                       " ".join("%s%d" % (pref, n) for n in numeri)))

    # ---- X2: ogni controllo dichiarato e' guardato dal codice
    for rel in sorted(sorgenti):
        for et in dichiarate(sorgenti[rel]):
            if not riportate(sorgenti[rel], et):
                problemi.append(
                    "X2 %s: il controllo %s e' dichiarato e non e' guardato "
                    "da nessuna riga che riporta" % (rel, et))

    # ---- X3: i numeri scritti nei documenti sono quelli del codice
    dichiarazioni = {}
    for rel in sorted(sorgenti):
        et = dichiarate(sorgenti[rel])
        if et:
            dichiarazioni[os.path.basename(rel)] = (rel, et)
    guardate = 0
    for rel in sorted(documenti):
        testo = documenti[rel]
        for numero_riga, riga in righe_utili(testo):
            if not riga.strip():
                continue
            citati = sorted(set(
                os.path.basename(m.group(0))
                for m in NOMINATO.finditer(riga)))
            if len(citati) == 1 and citati[0] in dichiarazioni:
                clausola = intorno(citati[0], riga)
                script, et = dichiarazioni[citati[0]]
                gruppi = per_prefisso(et)
                detto = numero(clausola)
                if detto is not None:
                    guardate += 1
                    if detto != len(et):
                        problemi.append(
                            "X3 %s riga %d: scrive %d controlli per %s, "
                            "il file ne dichiara %d (%s)"
                            % (rel, numero_riga, detto, citati[0], len(et),
                               " ".join(et)))
                for pref, a, b in INTERVALLO.findall(clausola):
                    if pref not in gruppi:
                        continue
                    numeri = gruppi[pref]
                    guardate += 1
                    if (int(a), int(b)) != (numeri[0], numeri[-1]):
                        problemi.append(
                            "X3 %s riga %d: %s scrive %s%d-%s%d, il file "
                            "dichiara %s%d-%s%d"
                            % (rel, numero_riga, citati[0], pref, int(a),
                               pref, int(b), pref, numeri[0], pref,
                               numeri[-1]))
    return guardate


def controlla_conto(sorgenti, documenti, problemi, prove_effettive=0):
    """X4 e X6: nessun verificatore resta fuori dal conto, e il conto e' scritto."""
    # ---- X4
    taciti = [rel for rel in sorted(sorgenti) if not dichiarate(sorgenti[rel])]
    for rel in taciti:
        if rel not in TACITI:
            problema_ = True
        else:
            problema_ = not TACITI[rel].strip()
        if problema_:
            problemi.append(
                "X4 %s: non dichiara i suoi controlli e non c'e' un motivo "
                "scritto in TACITI: un buco senza dichiarazione e' una "
                "sparizione silenziosa" % rel)
    for rel, motivo in sorted(TACITI.items()):
        if rel not in sorgenti:
            problemi.append("X4 %s: e' in TACITI ma il file non c'e' piu'"
                            % rel)
        elif motivo.strip() and dichiarate(sorgenti[rel]):
            problemi.append(
                "X4 %s: e' in TACITI con il motivo «%s», ma il file dichiara "
                "adesso %d controlli: la lista e' indietro rispetto alla "
                "realta'" % (rel, motivo[:60], len(dichiarate(sorgenti[rel]))))

    # ---- X6: il conto del debito e' scritto, e non cresce da solo
    conteggi = conta(sorgenti)
    conteggi["prove_eseguite"] = prove_effettive
    letto = leggi_conto(documenti.get("README.md", ""))
    for riga, chiave in CONTI.items():
        if riga not in letto:
            problemi.append(
                "X6 README.md: la tabella del conto non ha la riga «%s»" % riga)
            continue
        if letto[riga] != conteggi[chiave]:
            problemi.append(
                "X6 README.md: la riga «%s» dichiara %d, il conto e' %d"
                % (riga, letto[riga], conteggi[chiave]))
    if "Controlli senza prova" in letto:
        if letto["Controlli dichiarati in tutto"] != (
                letto["Controlli con la prova del difetto"]
                + letto["Controlli senza prova"]):
            problemi.append(
                "X6 README.md: i controlli con la prova e quelli senza non "
                "sommano ai controlli dichiarati")


def conta(sorgenti):
    """I numeri che il README deve dichiarare, contati sui file."""
    dichiarano = [rel for rel in sorgenti if dichiarate(sorgenti[rel])]
    controlli = 0
    provati = 0
    for rel in dichiarano:
        n = len(dichiarate(sorgenti[rel]))
        controlli += n
        if prove_dichiostrate(sorgenti[rel]):
            provati += n
    return {
        "verificatori": len(sorgenti),
        "dichiarano": len(dichiarano),
        "taciti": len(sorgenti) - len(dichiarano),
        "controlli": controlli,
        "provati": provati,
        "senza_prova": controlli - provati,
    }


def leggi_conto(testo):
    """Le righe «| Etichetta | **N** |» della sezione del conto, se c'e'."""
    dentro = False
    letto = {}
    for riga in testo.splitlines():
        if riga.startswith("## "):
            dentro = riga.strip() == SEZIONE_CONTO
            continue
        if not dentro:
            continue
        m = re.match(r"^\|\s*([^|]+?)\s*\|\s*\*\*(\d+)\*\*\s*\|\s*$", riga)
        if m:
            letto[m.group(1)] = int(m.group(2))
    return letto


def esegui_prove(sorgenti, radice, problemi, solo=None):
    """X5: la prova del difetto si esegue davvero, e si esegue bene.

    Non basta che l'opzione ci sia: un `--difetti` che esce 1, o che dice di
    non aver visto niente, e' una prova che non prova niente ed e' verde lo
    stesso. Ogni prova viene eseguita in un processo nuovo, perche' uno stesso
    processo che ha appena controllato il proprio albero non accetterebbe la
    domanda «la tua prova funziona?».
    """
    eseguite = 0
    # **Questo file non e' fra le prove da eseguire**: contiene la parola
    # `--difetti` perche' le costruisce, e senza questa riga ogni processo ne
    # lanciava un altro all'infinito. Un controllo che si esegue da solo non
    # e' un controllo: e' un ciclo.
    se_stesso = os.path.relpath(os.path.abspath(__file__), RADICE)
    for rel in sorted(sorgenti):
        if solo is not None and rel != solo:
            continue
        if rel == se_stesso:
            continue
        if not prove_dichiostrate(sorgenti[rel]):
            continue
        comando = [sys.executable, os.path.join(radice, rel), "--difetti"]
        try:
            fatto = subprocess.Popen(comando, cwd=radice,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.STDOUT)
            uscita, testo = fatto.communicate(timeout=900)
        except Exception as errore:  # noqa: BLE001 - il motivo va detto
            problemi.append("X5 %s: la prova non e' eseguibile (%s)"
                            % (rel, errore))
            continue
        testo = uscita.decode("utf-8", "replace") if uscita else ""
        visti = re.search(r"visti\D{0,3}(\d+)", testo)
        non_visti = re.search(r"non visti\D{0,3}(\d+)", testo)
        if fatto.returncode != 0:
            problemi.append(
                "X5 %s: `--difetti` esce %d: la prova del difetto e' rossa"
                % (rel, fatto.returncode))
            continue
        if visti is None or int(visti.group(1)) < 1:
            problemi.append(
                "X5 %s: `--difetti` esce 0 ma non dice di aver visto alcun "
                "difetto iniettato" % rel)
            continue
        if non_visti and int(non_visti.group(1)) != 0:
            problemi.append(
                "X5 %s: `%d` difetti iniettati e non visti"
                % (rel, int(non_visti.group(1))))
            continue
        eseguite += 1
    return eseguite


# --------------------------------------------------------------------------
def inietta(sorgenti, documenti, difetto):
    """Un difetto alla volta, su una copia dell'albero.

    Nessun difetto viene iniettato nei file veri: `--difetti` riscrive i file
    solo se glielo si chiede esplicitamente, e qui non glielo si chiede. Il
    difetto X5 ha bisogno di un file su disco, e quel file sta in una directory
    temporanea che muore con la prova.
    """
    s = dict(sorgenti)
    d = dict(documenti)
    if difetto == "X1":
        rel = "sorgenti/verifica_registri.py"
        # una versione che salta: R6 dichiarata, R5 non piu' li'
        s[rel] = s[rel].replace("\n  R5  nessuna intestazione",
                                "\n  R6  nessuna intestazione")
    elif difetto == "X2":
        rel = "sorgenti/verifica_sequenza.py"
        # un'etichetta dichiarata che nessun codice usa: il docstring promette
        # S0 e il file non ne parla. Togliere la riga che riporta S7 non
        # bastava, perche' la finestra del controllo la ritrovarebbe nella
        # riga dopo: il difetto vero e' l'etichetta, non la riga
        if "  S7  " not in s[rel]:
            return None, None, None
        s[rel] = s[rel].replace("  S7  ", "  S0  ", 1)
    elif difetto == "X3":
        rel = "docs/videogioco-5-duchi-sequenza.md"
        # un numero scritto a mano che invecchia: il documento chiama «nove
        # controlli» uno script che ne dichiara sette
        righe = [r for r in d[rel].splitlines()
                 if "verifica_sequenza.py" in r and "controlli" in r]
        if not righe:
            return None, None, None
        scelta = righe[0]
        nuovo_testo = re.sub(r"\b(dieci|nove|otto|sette|sei|cinque|quattro)\b",
                             lambda m: {"dieci": "dodici", "nove": "undici",
                                        "otto": "dieci", "sette": "nove",
                                        "sei": "otto", "cinque": "sette",
                                        "quattro": "sei"}[m.group(1)],
                             scelta, count=1)
        if nuovo_testo == scelta:
            return None, None, None
        d[rel] = d[rel].replace(scelta, nuovo_testo, 1)
    elif difetto == "X4":
        rel = "sorgenti/verifica_colori.py"
        # un verificatore che smette di dichiarare i suoi controlli e resta
        # fuori dalla lista dei motivi
        coppia = TACITI.pop(rel, None)
        if coppia is None:
            return None, None, None
        s[rel] = re.sub(r"^  [A-Z]\d+ +\S.*$", "", s[rel], flags=re.M)
    elif difetto == "X5":
        # l'albero vuoto e' quello che serve: lo stub sta nel terzo valore, e
        # il chiamante lo distingue dal «non iniettato» guardando proprio li'
        return {}, {}, ("sorgenti/verifica_finta.py",
                            "#!/usr/bin/env python3\n"
                            "\"\"\"Una prova che dichiara `--difetti` e non vede nessun difetto.\"\"\"\n"
                            "import sys\n"
                            "print(\"   NON VISTO  X1: difetto non guardato\")\n"
                            "print(\"difetti iniettati: 1, visti: 0, non "
                            "visti: 1\")\n"
                            "sys.exit(0)\n")
    elif difetto == "X6":
        rel = "README.md"
        # il debito cresce e nessuno aggiorna la riga che lo dichiara
        righe = [r for r in d[rel].splitlines()
                 if "| Controlli senza prova |" in r]
        if not righe:
            return None, None, None
        attuale = int(re.search(r"\*\*(\d+)\*\*", righe[0]).group(1))
        d[rel] = d[rel].replace(righe[0], righe[0].replace(
            "**%d**" % attuale, "**%d**" % (attuale + 7)))
    else:
        raise ValueError(difetto)
    return s, d, None


def albero():
    """I file di cui il controllo ha bisogno, letti dal disco."""
    sorgenti = {}
    for base, cartelle, nomi in os.walk(os.path.join(RADICE, "sorgenti")):
        cartelle[:] = [c for c in cartelle if c != "__pycache__"]
        for n in sorted(nomi):
            if n.startswith("verifica") and n.endswith(".py"):
                percorso = os.path.join(base, n)
                rel = os.path.relpath(percorso, RADICE)
                sorgenti[rel] = leggi(percorso)
    documenti = {"README.md": leggi(os.path.join(RADICE, "README.md"))}
    cartella = os.path.join(RADICE, "docs")
    for n in sorted(os.listdir(cartella)):
        if n.endswith(".md"):
            documenti["docs/" + n] = leggi(os.path.join(cartella, n))
    return sorgenti, documenti


def main():
    sola_prova = "--difetti" in sys.argv
    sorgenti, documenti = albero()

    problemi = []
    guardate = controlla(sorgenti, documenti, problemi)
    eseguite = esegui_prove(sorgenti, RADICE, problemi)
    controlla_conto(sorgenti, documenti, problemi, eseguite)

    numeri = conta(sorgenti)
    print("== X1-X6. i controlli sui controlli")
    print("   verificatori: %d, che dichiarano i loro controlli: %d, "
          "senza dichiarazione: %d"
          % (numeri["verificatori"], numeri["dichiarano"], numeri["taciti"]))
    print("   controlli dichiarati: %d, con la prova del difetto: %d, "
          "senza prova: %d" % (numeri["controlli"], numeri["provati"],
                               numeri["senza_prova"]))
    print("   numeri scritti nei documenti confrontati con il codice: %d"
          % guardate)
    print("   prove `--difetti` eseguite davvero: %d" % eseguite)
    if problemi:
        for p in problemi:
            print("   difetto %s" % p)
    else:
        print("   nessuna etichetta saltata, nessun controllo dichiarato e "
              "non guardato, nessun numero in prosa che non sia quello del "
              "codice, nessun verificatore fuori dal conto, ogni prova "
              "eseguita e' verde, il conto del debito e' quello dichiarato")

    if sola_prova:
        iniettati = 0
        visti = 0
        for difetto in ("X1", "X2", "X3", "X4", "X5", "X6"):
            s, d, finto = inietta(dict(sorgenti), dict(documenti), difetto)
            if s is None or (not s and not d and finto is None):
                print("   NON INIETTATO  %s: nessun file su cui intervenire"
                      % difetto)
                continue
            iniettati += 1
            if difetto == "X5":
                # X5 guarda un file su disco: il difetto sta in una directory
                # temporanea, e l'albero vero non viene toccato
                temporanea = tempfile.mkdtemp(prefix="prove_")
                try:
                    destinazione = os.path.join(temporanea, finto[0])
                    cartella = os.path.dirname(destinazione)
                    if not os.path.isdir(cartella):
                        os.makedirs(cartella)
                    scrivi(destinazione, finto[1])
                    problemi2 = []
                    esegui_prove({finto[0]: finto[1]}, temporanea, problemi2)
                    trovati = [p for p in problemi2 if p.startswith("X5 ")]
                finally:
                    shutil.rmtree(temporanea, ignore_errors=True)
            else:
                problemi2 = []
                controlla(s, d, problemi2)
                controlla_conto(s, d, problemi2, eseguite)
                trovati = [p for p in problemi2 if p.startswith(difetto + " ")]
            if trovati:
                visti += 1
                for p in trovati:
                    print("   visto   %s" % p[:120])
            else:
                print("   NON VISTO  %s" % difetto)
        print("\ndifetti iniettati: %d, visti: %d, non visti: %d"
              % (iniettati, visti, iniettati - visti))
        if visti != iniettati:
            return 1

    return 1 if problemi else 0


if __name__ == "__main__":
    sys.exit(main())
