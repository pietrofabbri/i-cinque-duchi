#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Conta le questioni aperte dichiarate nei documenti di progetto.

Un documento che dichiara un numero di questioni senza che nessuno lo conti
diventa un documento che mente fra tre versioni. Questo script conta, e il
riscontro è con `docs/videogioco-5-duchi-audit.md` **e con il `README.md`**.

**Il criterio, dichiarato**, perché un conteggio senza criterio non è un dato:

  voce    un punto della sezione «Questioni aperte», in tre forme possibili,
          tutte riconosciute:
            - un elenco numerato:  `1. **Il buco di S66.** ...`
            - un sottotitolo:      `### Q1 — il titolo`
            - una riga di tabella: `| 1 | la domanda | **chiusa** — ... |`
  chiusa  una voce che porta una marcatura di chiusa **nella sua prima
          riga**: «chiusa», «chiuso», «chiuse», «risolto», «ratificata»,
          «confermata». La prima riga e non tutto il corpo, perché una voce
          aperta spiega dentro il corpo per quale parte è stata chiusa: se si
          contasse tutta la voce, ogni questione parzialmente risolta
          sembrerebbe chiusa

I numeri che il confronto guarda, e perché sono quelli:

  §1 dell'audit   la tabella dove stanno i numeri, le due frasi in prosa;
  N1              quante sezioni «Questioni aperte» ci sono: la riga dice 15,
                  il conto ne trova 16. Il numero era scritto a mano e
                  invecchiò quando `itinerari.md` ha aperto la sua;
  N2              i numeri **per documento** nelle intestazioni del §4: sono il
                  conto delle voci aperte di quel documento, e ogni documento
                  con voci aperte deve comparire in un'intestazione. Una voce
                  contata e non elencata è una voce che nessuno legge;
  N3              i numeri che il **README copia** dall'audit: cinque numeri
                  nella riga della tabella dei documenti, cinque nella nota
                  sull'audit, e il numero di documenti di progetto;
  N4/N5/N6        i numeri in **lettere**: le quattro bloccanti (§2), le
                  quindici importanti (§3), e le sezioni contate in §1. Una
                  parola non è un numero che un programma può confrontare, ma è
                  un numero che un lettore prende per esatto: si converte con
                  le regole dell'italiano e si confronta lo stesso.

**Il registro delle modifiche non viene confrontato**, e la ragione è dichiarata
perché è una scelta e non una dimenticanza: le sue righe raccontano **come era**
il documento quando l'avevano scritto, e quei numeri sono quelli di allora.
Confrontarli produrrebbe un falso allarme su ogni versione passata, e un
controllo che urla ogni giorno viene spento per legittima ragione. È la stessa
scelta di `verifica_coerenza.py`, che fa la stessa cosa e lo dichiara.

**Tre forme in cui l'italiano non somma**: `ventuno`, `ventotto`, `trentuno` (e
`trentaotto`). Sono le uniche in cui la decina perde la sua vocale finale, e
sono proprio quelle che un dizionario costruito per concatenazione non
riconosce: il confronto dei numeri in lettere tornava verde **perché non
guardava**, che è la forma peggiore in cui un controllo può mentire.

Uso:
    python3 sorgenti/lingue/conta_questioni.py
    python3 sorgenti/lingue/conta_questioni.py --radice /tmp/copia   # una copia
"""
import glob
import os
import re
import sys
import unicodedata

RADICE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
DOCS = os.path.join(RADICE, "docs")
README = os.path.join(RADICE, "README.md")

# I documenti si chiamano `videogioco-5-duchi-<nome>.md`, ma nei documenti si
# citano come `<nome>.md`: il confronto delle intestazioni del §4 usa la forma
# corta e la riporta a quella lunga una volta sola, qui.
PREFISSO = "videogioco-5-duchi-"

CHIUSA = re.compile(
    r"chius[aeio]|chiusi|risolt|ratificat|confermata|confermato|confermati", re.I)

FORME = [
    re.compile(r"^\s*\d+\.\s+"),
    re.compile(r"^###+\s*Q\d+\s*[-—:.]?\s*"),
    re.compile(r"^\|\s*\*{0,2}Q?\d+\*{0,2}\s*\|"),
    # I documenti trasversali recenti scrivono le questioni in due forme che
    # il contatore deve vedere, altrimenti l'audit si ferma ai tredici
    # documenti più vecchi e non conta le dodici domande più importanti:
    #   percorsi.md       `### Q1 — la domanda`
    #   fonti-visive.md   `**Q1 — la domanda**`
    re.compile(r"^###+\s+Q\d+\s*[-—:.]"),
    re.compile(r"^\*\*Q\d+\s*[-—:.]"),
]

# I documenti chiamano la sezione in due modi: «Questioni aperte» e «Le
# questioni aperte». La regex accetta entrambi, perché un contatore che vede
# tredici documenti su quindici sbaglia il conto e l'audit dice un numero falso.
SEZIONE = re.compile(r"^##+\s*[\d.]*\s*(?:Le\s+)?[Qq]uestioni aperte(.*?)(?=^##\s|\Z)",
                     re.M | re.S)


# --------------------------------------------------------------------------
# numeri in lettere
# --------------------------------------------------------------------------
def _parole():
    """1..99 in italiano, con le due elisioni («ventuno», «ventotto»)."""
    unità = ["", "uno", "due", "tre", "quattro", "cinque", "sei", "sette",
             "otto", "nove"]
    teen = {10: "dieci", 11: "undici", 12: "dodici", 13: "tredici",
            14: "quattordici", 15: "quindici", 16: "sedici", 17: "diciassette",
            18: "diciotto", 19: "diciannove"}
    decine = ["", "", "venti", "trenta", "quaranta", "cinquanta", "sessanta",
              "settanta", "ottanta", "novanta"]
    out = {}
    for n in range(1, 100):
        if n < 10:
            parola = unità[n]
        elif n < 20:
            parola = teen[n]
        else:
            # «venti» + «uno» fa «ventuno» e «venti» + «otto» fa «ventotto»:
            # sono le due forme in cui una parola non si somma, e sono le
            # uniche. Senza queste due righe il dizionario contiene
            # «trentauno» e «trentaotto», che nessuno scrive, e **il confronto
            # delle parole che il documento usa ignorava in silenzio proprio i
            # numeri che il documento scrive in lettere**: un controllo che
            # non riconosce la parola che cerca è un controllo che non guarda.
            if n % 10 == 0:
                parola = decine[n // 10]
            elif n % 10 == 1:
                # la decina finale in vocale cade: «venti» + «uno» = «ventuno»,
                # «trenta» + «uno» = «trentuno». Su «venti» basta togliere la
                # i; su «trenta» bisogna togliere la a finale, e una regola che
                # taglia l'ultima lettera qualunque farebbe «trentaauno».
                parola = decine[n // 10].rstrip("ia") + "uno"
            elif n % 10 == 8:
                # stessa caduta: «venti» + «otto» = «ventotto», e senza
                # togliere la i verrebbe «ventiotto», che non è una parola
                parola = decine[n // 10].rstrip("ia") + "otto"
            else:
                parola = decine[n // 10] + unità[n % 10]
        out[parola] = n
        # senza accento: «ventitré» e «ventitre» sono la stessa parola
        out[parola.replace("é", "e")] = n
    return out


PAROLE = _parole()


# Le righe del registro delle modifiche raccontano **come era** il documento, e i
# loro numeri sono quelli di allora: «26 chiuse» è vero per il 03/10 alle 18:00
# e falso per adesso, e controllarlo come se fosse di adesso produrrebbe un
# falso allarme su ogni versione passata. Come in `verifica_coerenza.py`, il
# registro si legge a mano e non si confronta.
RIGA_REGISTRO = re.compile(r"^\|\s*\d{2}/\d{2}/\d{4}\s*\|")


def senza_registro(testo):
    """Le sole righe di prosa: il registro fuori, tutto il resto dentro."""
    return "\n".join(r for r in testo.split("\n") if not RIGA_REGISTRO.match(r))


def parola_numero(s):
    """Il valore di un numero in lettere, o None se non è un numero."""
    s = unicodedata.normalize("NFKD", s.lower().strip())
    s = "".join(c for c in s if not unicodedata.combining(c))
    # «una bloccante», «una sola»: il femminile di «uno», dal 07/10/2026
    if s == "una":
        s = "uno"
    return PAROLE.get(s)


# --------------------------------------------------------------------------
# il conto
# --------------------------------------------------------------------------
def sezione_voci(sezione):
    """Le voci della sezione: (prima riga, numero di riga)."""
    righe = sezione.split("\n")
    fuori = []
    for i, riga in enumerate(righe):
        if riga.startswith("|"):
            # dentro una tabella la prima riga utile è quella dei dati, non la
            # testata: la riga dei trattini si salta
            if re.match(r"^\|\s*-{2,}", riga):
                continue
        for forma in FORME:
            if forma.match(riga):
                fuori.append((riga.strip(), i))
                break
    return fuori


def conta(solo=None):
    """Il conto: {documento: (aperte, chiuse)} e i due totali."""
    per_documento = {}
    for percorso in sorted(glob.glob(os.path.join(solo or DOCS, "*.md"))):
        testo = open(percorso, encoding="utf-8").read()
        elenco = []
        for m in SEZIONE.finditer(testo):
            elenco += sezione_voci(m.group(1))
        if not elenco:
            continue
        # una stessa voce presa da due forme conta una volta sola
        uniche = []
        for riga, pos in elenco:
            if not uniche or uniche[-1] != riga:
                uniche.append(riga)
        a = sum(1 for riga in uniche if not CHIUSA.search(riga))
        per_documento[os.path.basename(percorso)] = (a, len(uniche) - a)
    aperte = sum(a for a, _ in per_documento.values())
    chiuse = sum(c for _, c in per_documento.values())
    return per_documento, aperte, chiuse


# --------------------------------------------------------------------------
# le parti dell'audit che portano numeri
# --------------------------------------------------------------------------
def corto(nome):
    """`videogioco-5-duchi-luoghi.md` → `luoghi.md`: nei messaggi si parla dei
    documenti come li chiama il documento che li contiene."""
    return nome[len(PREFISSO):] if nome.startswith(PREFISSO) else nome


def sezione_del(testo, titolo):
    """Il corpo di una sezione `## N.`, dalla sua intestazione alla successiva."""
    m = re.search(r"^##\s*" + re.escape(titolo) + r".*?(?=^##\s|\Z)", testo, re.M | re.S)
    return m.group(0) if m else ""


def numeri_del_gioco(gioco, coppia, taglia_grassetto=True):
    """Le righe `| I<n> |` della tabella delle importanti: quante sono aperte."""
    righe = [r for r in gioco.split("\n") if re.match(r"^\|\s*I\d+\s*\|", r)]
    if taglia_grassetto:
        righe = [r for r in righe if "chiusa il" not in r]
    return len(righe)


def schede_bloccanti(sezione2):
    """Le schede `### B<n> ·` e quante sono aperte."""
    righe = [r for r in sezione2.split("\n") if re.match(r"^###\s*B\d+\s*·", r)]
    aperte = [r for r in righe if not CHIUSA.search(r)]
    return len(righe), len(aperte)


def importanti_per_documento(sezione3):
    """Quante importanti aperte citano ciascun documento.

    Una importante che cita due documenti (I18, `meccaniche.md` e
    `curricolo.md`) **conta una volta sola**, attribuita al primo che cita: due
    attribuzioni farebbero sparire una voce dalla sintesi del §4 senza che
    nessuno l'avesse chiusa, ed è il difetto che un numero diviso a metà
    produce.
    """
    fuori = {}
    for riga in sezione3.split("\n"):
        if not re.match(r"^\|\s*I\d+\s*\|", riga) or "chiusa il" in riga:
            continue
        citati = re.findall(r"`([a-z0-9-]+\.md)`", riga)
        if not citati:
            continue
        nome = PREFISSO + citati[0]
        fuori[nome] = fuori.get(nome, 0) + 1
    return fuori


def intestazioni_sintesi(sezione4):
    """Le coppie (documento, numero) delle intestazioni del §4.

    La forma dichiarata è una sola: **ogni numero dentro parentesi è preceduto
    dal nome del suo documento fra apici inversi** —
    `### Anno 1 (`anno1-ferrara.md` 7) e curricolo (`curricolo.md` 5)`. Il
    controllo toglie le coppie e poi pretende che dentro le parentesi non resti
    **nessuna cifra**: un numero che può stare anche senza il nome del
    documento è un numero che nessuno conta, e un controllo che passa su un
    numero che non legge è verde come un controllo che guarda.

    Fuori dalle parentesi le cifre non sono conteggi ma nomi — «Anno 3», «*Furioso*
    (2)» è dentro, ma il 3 di «Anno 3» è un titolo — e non sono confrontate.
    """
    coppie = []
    illeggibili = []
    for riga in sezione4.split("\n"):
        if not riga.startswith("### "):
            continue
        titolo = riga[4:].strip()
        dentro = re.findall(r"\(([^)]*)\)", titolo)
        if not dentro:
            continue
        for testo in dentro:
            coppie += [(PREFISSO + nome, int(numero), titolo)
                       for nome, numero in
                       re.findall(r"`?([a-z0-9-]+\.md)`?\s+(\d+)", testo)]
            residuo = re.sub(r"`?[a-z0-9-]+\.md`?\s+\d+", "", testo)
            if re.search(r"\d", residuo):
                illeggibili.append(titolo)
    return coppie, illeggibili


def confronta_audit(testo, per_documento, aperte, chiuse, problemi):
    """Tutti i numeri dell'audit, e nessuno dei due conti riservato a lui."""
    # --- la tabella del §1, che e' **dove stanno i numeri**. La versione di
    # prima di questo controllo cercava la forma di prosa «**N** chiuse», e in
    # un documento che scrive i numeri in tabella quella forma non compare: la
    # ricerca non trovava niente, il controllo passava, e l'audit dichiarava
    # **115 voci** mentre il conto ne trovava **118**. Il difetto non era nel
    # numero ma nel controllo che doveva confermarlo — e un controllo che non
    # guarda niente e' verde come un controllo che guarda: solo che il verde del
    # primo non significa niente.
    dichiarati = {}
    in_lettere = {}
    for riga in testo.split("\n"):
        m = re.match(r"^\|\s*\**([^|*]+?)\**\s*\|\s*\**(\d+)\**\s*\|", riga)
        if m:
            chiave = m.group(1).strip().strip("*")
            valore = int(m.group(2))
            if chiave.startswith("Documenti con una sezione"):
                dichiarati["sezioni"] = valore
            elif chiave == "Voci enumerate":
                dichiarati["voci"] = valore
            elif chiave == "Chiuse":
                dichiarati["chiuse"] = valore
            elif chiave == "Aperte":
                dichiarati["aperte"] = valore
            continue
        m = re.match(r"^\|\s*\**(Di cui bloccanti|Di cui importanti[^*]*)\**\s*\|\s*([A-Za-z]+)\s*\|",
                     riga)
        if m:
            in_lettere[m.group(1).strip().strip("*")] = m.group(2).lower()
    if "sezioni" not in dichiarati:
        problemi.append("non trovo la riga «Documenti con una sezione» del §1: "
                        "il numero delle sezioni non e' controllato")
    for chiave in ("sezioni", "voci", "chiuse", "aperte"):
        if chiave not in dichiarati:
            problemi.append("la riga «%s» del §1 dell'audit non e' leggibile: "
                            "il numero c'e' ma il controllo non lo vede" % chiave)
    reale = {"sezioni": len(per_documento), "voci": aperte + chiuse,
             "chiuse": chiuse, "aperte": aperte}
    for chiave, valore in reale.items():
        if chiave in dichiarati and dichiarati[chiave] != valore:
            problemi.append("l'audit dichiara %s = %d, il conto dà %d"
                            % (chiave, dichiarati[chiave], valore))

    # --- le due frasi in prosa del §1
    sezione1 = sezione_del(testo, "1.")
    m = re.search(r"\*\*(\d+) voci non sono \d+ domande\*\*", sezione1)
    if m and int(m.group(1)) != aperte + chiuse:
        problemi.append("il §1 scrive «%s voci non sono … domande», la somma è %d"
                        % (m.group(1), aperte + chiuse))
    # Due forme: «nessuna delle N chiuse» e, dal 07/10/2026 quando B1 e' stata
    # la prima bloccante chiusa, «una sola delle N chiuse». Il numero in lettere
    # si confronta in tutte e due.
    for m in re.finditer(r"(?:nessuna|una sola) delle (\w+) chiuse", senza_registro(testo), re.I):
        n = parola_numero(m.group(1))
        if n is not None and n != chiuse:
            problemi.append("l'audit scrive «nessuna delle %s chiuse», "
                            "il conto ne trova %d" % (m.group(1), chiuse))

    # --- N4/N5: i numeri in lettere delle due sezioni che li portano
    sezione2 = sezione_del(testo, "2.")
    sezione3 = sezione_del(testo, "3.")
    titolo2 = re.search(r"^##\s*2\.\s*(.*)$", sezione2, re.M)
    schede, bloccanti = schede_bloccanti(sezione2)
    if titolo2:
        m = re.search(r"(\w+)\s+bloccant[ei]", titolo2.group(1), re.I)
        n = parola_numero(m.group(1)) if m else None
        if n is not None and n != bloccanti:
            problemi.append("il §2 si intitola «%s bloccanti», le schede B aperte "
                            "sono %d" % (m.group(1), bloccanti))
    if "Di cui bloccanti" in in_lettere:
        n = parola_numero(in_lettere["Di cui bloccanti"])
        if n is None:
            problemi.append("il §1 scrive «Di cui bloccanti: %s», che non è un numero"
                            % in_lettere["Di cui bloccanti"])
        elif n != bloccanti:
            problemi.append("il §1 scrive «di cui %s bloccanti», le schede B aperte "
                            "sono %d" % (in_lettere["Di cui bloccanti"], bloccanti))
    titolo3 = re.search(r"^##\s*3\.\s*(.*)$", sezione3, re.M)
    importanti = numeri_del_gioco(sezione3, "I")
    if titolo3:
        m = re.search(r"(\w+)\s+importanti", titolo3.group(1), re.I)
        n = parola_numero(m.group(1)) if m else None
        if n is not None and n != importanti:
            problemi.append("il §3 si intitola «%s importanti», le voci I aperte "
                            "sono %d" % (m.group(1), importanti))
    for chiave, valore in in_lettere.items():
        if chiave.startswith("Di cui importanti"):
            n = parola_numero(valore)
            if n is None:
                problemi.append("il §1 scrive «%s: %s», che non è un numero"
                                % (chiave, valore))
            elif n != importanti:
                problemi.append("il §1 scrive «di cui %s importanti», le voci I "
                                "aperte sono %d" % (valore, importanti))

    # --- N1: le sezioni contate anche in prosa. Nell'audit la frase è nel
    # frontespizio e vale per i documenti che portano una sezione: se ne nasce
    # uno, la frase invecchia — che è successo il 03/10 con `itinerari.md`.
    for m in re.finditer(r"(\w+) sezioni(?=[:,.]| e )", senza_registro(testo)):
        n = parola_numero(m.group(1))
        if n is not None and n != len(per_documento):
            problemi.append("l'audit scrive «%s sezioni», i documenti con una sezione "
                            "sono %d" % (m.group(1), len(per_documento)))

    # --- N2: i numeri per documento della sintesi del §4. Il numero dichiarato
    # è **il conto delle voci aperte di quel documento meno le importanti che il
    # §3 elenca già**: il §4 si intitola «Le altre, in sintesi», e un numero che
    # contasse anche le importanti sarebbe doppio. Ogni documento con voci
    # aperte deve comparire in un'intestazione: una voce contata e non elencata
    # è una voce che nessuno legge.
    sezione4 = sezione_del(testo, "4.")
    imp = importanti_per_documento(sezione3)
    coppie, illeggibili = intestazioni_sintesi(sezione4)
    for titolo in illeggibili:
        problemi.append("l'intestazione «%s» del §4 porta un numero senza il nome "
                        "del documento: quel numero non è controllato" % titolo)
    citati = set()
    for nome, dichiarato, titolo in coppie:
        citati.add(nome)
        if nome not in per_documento:
            problemi.append("il §4 dichiara un numero per %s, che non è un "
                            "documento di progetto" % corto(nome))
            continue
        atteso = per_documento[nome][0] - imp.get(nome, 0)
        if dichiarato != atteso:
            problemi.append("il §4 dichiara %d per %s, il conto delle altre è %d "
                            "(%d aperte meno %d importanti già nel §3)"
                            % (dichiarato, corto(nome), atteso, per_documento[nome][0],
                               imp.get(nome, 0)))
    mancanti = sorted(n for n, (a, _) in per_documento.items()
                      if a - imp.get(n, 0) > 0 and n not in citati)
    for nome in mancanti:
        problemi.append("%s ha %d voci aperte e non compare in nessuna "
                        "intestazione del §4: sono contate e non elencate"
                        % (corto(nome), per_documento[nome][0] - imp.get(nome, 0)))
    # e la somma delle intestazioni deve essere il totale delle aperte meno le
    # importanti: due vie di contare la stessa cosa che non tornano è il difetto
    # che questo controllo esiste per trovare
    somma = sum(n for _, n, _ in coppie)
    atteso = aperte - sum(imp.values())
    if somma != atteso:
        problemi.append("i numeri del §4 sommano %d, le aperte meno le importanti "
                        "sono %d" % (somma, atteso))
    return reale, in_lettere


def confronta_readme(testo, per_documento, reale, in_lettere, radice_docs, problemi):
    """I numeri che il README copia dall'audit: cinque per riga, cinque in nota."""
    # la riga della tabella dei documenti: «118 voci in **16 sezioni**, **31
    # chiuse, 87 aperte**, 4 bloccanti e 15 importanti». I grassetti cambiano
    # quando la riga viene riscritta e non sono parte del dato: la regex li
    # tollera, perché un controllo che smette di guardare una riga perché il
    # grassetto è cambiato è un controllo che non guarda.
    for m in re.finditer(r"(\d+) voci\b.{0,40}?\**(\d+) chiuse, (\d+) aperte\**, "
                         r"(\d+) bloccant[ei] e (\d+) importanti", testo):
        voci, chiuse_r, aperte_r, blocchi, importanti = (int(g) for g in m.groups())
        if (voci, chiuse_r, aperte_r) != (reale["voci"], reale["chiuse"], reale["aperte"]):
            problemi.append("il README scrive «%d voci, %d chiuse, %d aperte», "
                            "l'audit dice %d, %d, %d"
                            % (voci, chiuse_r, aperte_r, reale["voci"],
                               reale["chiuse"], reale["aperte"]))
        for scritto, chiave in ((blocchi, "Di cui bloccanti"),):
            if chiave in in_lettere:
                atteso = parola_numero(in_lettere[chiave])
                if atteso is not None and scritto != atteso:
                    problemi.append("il README scrive «%d bloccanti», l'audit dice %d"
                                    % (scritto, atteso))
        if "Di cui importanti (cambiano il gioco)" in in_lettere:
            atteso = parola_numero(in_lettere["Di cui importanti (cambiano il gioco)"])
            if atteso is not None and importanti != atteso:
                problemi.append("il README scrive «%d importanti», l'audit dice %d"
                                % (importanti, atteso))

    # la nota sull'audit: «118 voci enumerate in sedici sezioni, **31 chiuse** e
    # **87 aperte**, delle quali **4 bloccanti**», e «il progetto ha … documenti»
    for m in re.finditer(r"(\d+) voci enumerate in (\w+) sezioni, \**(\d+) chiuse\** "
                         r"e \**(\d+) aperte\**, delle quali \**(\d+) bloccant[ei]\**", testo):
        voci = int(m.group(1))
        sezioni = parola_numero(m.group(2))
        chiuse_r, aperte_r, blocchi = (int(g) for g in m.groups()[2:])
        if voci != reale["voci"]:
            problemi.append("il README scrive «%d voci enumerate», l'audit dice %d"
                            % (voci, reale["voci"]))
        if sezioni is not None and sezioni != len(per_documento):
            problemi.append("il README scrive «%s sezioni», i documenti con una "
                            "sezione sono %d" % (m.group(2), len(per_documento)))
        if (chiuse_r, aperte_r) != (reale["chiuse"], reale["aperte"]):
            problemi.append("il README scrive «%d chiuse e %d aperte», l'audit dice "
                            "%d e %d" % (chiuse_r, aperte_r, reale["chiuse"],
                                         reale["aperte"]))
        if "Di cui bloccanti" in in_lettere:
            atteso = parola_numero(in_lettere["Di cui bloccanti"])
            if atteso is not None and blocchi != atteso:
                problemi.append("il README scrive «%d bloccanti», l'audit dice %d"
                                % (blocchi, atteso))
    for m in re.finditer(r"nessuna delle (\w+) chiuse", testo, re.I):
        n = parola_numero(m.group(1))
        if n is not None and n != reale["chiuse"]:
            problemi.append("il README scrive «nessuna delle %s chiuse», "
                            "l'audit ne conta %d" % (m.group(1), reale["chiuse"]))
    documenti = len(glob.glob(os.path.join(radice_docs, "*.md")))
    for m in re.finditer(r"il progetto ha (\w+) documenti", testo):
        n = parola_numero(m.group(1))
        if n is not None and n != documenti:
            problemi.append("il README scrive «il progetto ha %s documenti», "
                            "in `docs/` ci sono %d" % (m.group(1), documenti))


def main():
    radice = RADICE
    if "--radice" in sys.argv:
        radice = os.path.abspath(sys.argv[sys.argv.index("--radice") + 1])
    docs = os.path.join(radice, "docs")
    readme = os.path.join(radice, "README.md")
    audit = os.path.join(docs, "videogioco-5-duchi-audit.md")

    per_documento, aperte, chiuse = conta(docs)

    print("%-46s %8s %8s" % ("documento", "aperte", "chiuse"))
    for nome in sorted(per_documento):
        a, c = per_documento[nome]
        print("%-46s %8d %8d" % (nome, a, c))
    print("-" * 64)
    print("%-46s %8d %8d" % ("TOTALE", aperte, chiuse))
    print("somma: %d" % (aperte + chiuse))
    print("documenti con una sezione: %d" % len(per_documento))

    problemi = []
    reale = {}
    if os.path.exists(audit):
        testo = open(audit, encoding="utf-8").read()
        reale, in_lettere = confronta_audit(testo, per_documento, aperte, chiuse, problemi)
        if os.path.exists(readme):
            confronta_readme(open(readme, encoding="utf-8").read(), per_documento,
                             reale, in_lettere, docs, problemi)
    else:
        problemi.append("non trovo l'audit: nessun numero è confrontato")

    if problemi:
        print("problemi: %d" % len(problemi))
        for p in problemi:
            print("  " + p)
    else:
        print("problemi: 0")
        print("(l'audit e il README dichiarano i numeri del §1, le intestazioni "
              "del §4 e i numeri in lettere, e il conto li conferma tutti)")
    return 1 if problemi else 0


if __name__ == "__main__":
    sys.exit(main())