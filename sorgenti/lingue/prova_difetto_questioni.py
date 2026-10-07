#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prova che `conta_questioni.py` morda, con difetti iniettati uno alla volta.

Un controllo che non si è mai visto sbagliare non è un controllo: è un
documento che dice «tutto va bene». Qui si rompono le cose apposta, una per una,
e si pretende che il contatore se ne accorga; poi si rimette tutto com'era e si
richiede che torni verde. I difetti provati sono quelli **capitati**, non quelli
che si immaginano: i quattro del 04/10/2026 (le sezioni dichiarate 15 su 16,
`itinerari.md` fuori dal §4, i numeri dei documenti in §4 e il «sedici
documenti» del README) sono qui, e si prova anche che il registro delle
modifiche — che racconta il passato — non venga morso.

**La prova lavora su una copia, non sui file veri.** Una prova che scrive
sull'audit e lo rimette è una prova che, se muore a metà, lascia il documento
sbagliato nel repository: `conta_questioni.py` accetta `--radice` per questo, e
la prova gliela passa. I documenti copiati sono tutti e trentauno, perché un
controllo che ne contasse meno darebbe numeri diversi e la prova passerebbe per
la ragione sbagliata.

Uso:
    python3 sorgenti/lingue/prova_difetto_questioni.py
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CONTA = os.path.join(BASE, "sorgenti", "lingue", "conta_questioni.py")
AUDIT = "videogioco-5-duchi-audit.md"
README = "README.md"


def porzione(testo, schema, che_cosa):
    """La riga del documento che la prova deve alterare, cercata ogni volta.

    **Un numero scritto dentro la prova invecchia come tutti gli altri**, ed e'
    successo: il 05/10/2026 il conto delle questioni chiuse e' passato da 31
    a 34, e i tre difetti che dipendevano da quel numero non hanno piu' trovato
    il testo da alterare. Una prova che non altera niente e non se ne accorge
    passa per la ragione sbagliata, che e' la peggiore: e' verde perche' non
    ha guardato niente. Il numero lo cerca nel documento, non lo sa.
    """
    m = re.search(schema, testo)
    if not m:
        raise SystemExit("la prova cerca %s e non lo trova: il documento e' "
                         "cambiato e la prova va aggiornata" % che_cosa)
    return m.group(0)


def _sposta(testo, schema, che_cosa, posizione, passo):
    """Il numero alla posizione `posizione` (1 = primo) di quella riga, spostato
    di `passo`. Serve a far salire di uno un numero senza sapere quale sia."""
    m = re.search(schema, testo)
    if not m:
        raise SystemExit("la prova cerca %s e non lo trova: il documento e' "
                         "cambiato e la prova va aggiornata" % che_cosa)
    numeri = re.findall(r"\d+", m.group(0))
    if len(numeri) <= posizione:
        raise SystemExit("la riga %s non ha %d numeri: %r"
                         % (che_cosa, posizione + 1, m.group(0)))
    nuovo = str(int(numeri[posizione]) + passo)
    parti = re.split(r"(\d+)", m.group(0))
    volte = 0
    for k, pezzo in enumerate(parti):
        if pezzo.isdigit():
            if volte == posizione:
                parti[k] = nuovo
                break
            volte += 1
    return testo.replace(m.group(0), "".join(parti), 1)


def _piu_uno(testo, schema, che_cosa):
    """Sale di uno il numero che segue `parola` nella riga trovata: serve al
    difetto «il README scrive sedici importanti» senza sapere quanti sono."""
    m = re.search(schema, testo)
    if not m:
        raise SystemExit("la prova cerca %s e non lo trova: il documento e' "
                         "cambiato e la prova va aggiornata" % che_cosa)
    numeri = re.findall(r"\d+", m.group(0))
    ultimo = numeri[-1]
    return testo.replace(m.group(0),
                         m.group(0).replace(ultimo, str(int(ultimo) + 1)), 1)


def _meno_uno(testo, schema, che_cosa, quanti):
    """Scende di uno gli ultimi `quanti` numeri della riga: il difetto e'
    «il conto e' sbagliato», non «il conto e' questo numero»."""
    m = re.search(schema, testo)
    if not m:
        raise SystemExit("la prova cerca %s e non lo trova: il documento e' "
                         "cambiato e la prova va aggiornata" % che_cosa)
    numeri = re.findall(r"\d+", m.group(0))
    if len(numeri) < quanti:
        raise SystemExit("la riga %s non ha %d numeri" % (che_cosa, quanti))
    nuovo = m.group(0)
    for n in reversed(numeri[-quanti:]):
        nuovo = nuovo.replace(n, str(int(n) - 1), 1)
    return testo.replace(m.group(0), nuovo, 1)


def gira(radice):
    r = subprocess.run([sys.executable, CONTA, "--radice", radice],
                       capture_output=True, text=True)
    return r.returncode, r.stdout


def copia_progetto():
    """Una copia intera di `docs/` e del README: il confronto ha bisogno di
    tutti i documenti, perché il conto parte da loro."""
    radice = tempfile.mkdtemp(prefix="prova_questioni_")
    shutil.copytree(os.path.join(BASE, "docs"), os.path.join(radice, "docs"))
    shutil.copy(os.path.join(BASE, README), os.path.join(radice, README))
    return radice


def percorso(radice, nome):
    """Dove sta un file della copia: il README sta in radice, l'audit in `docs/`."""
    if os.path.dirname(nome):
        return os.path.join(radice, nome)
    return os.path.join(radice, nome if nome == README else "docs/" + nome)


def leggi(radice, nome):
    return open(percorso(radice, nome), encoding="utf-8").read()


def scrivi(radice, nome, testo):
    with open(percorso(radice, nome), "w", encoding="utf-8") as f:
        f.write(testo)


def sostituisci(testo, vecchio, nuovo):
    """Una sostituzione che fallisce rumorosamente se il testo non è quello."""
    if testo.count(vecchio) != 1:
        raise SystemExit("la prova cerca «%s» e lo trova %d volte: il difetto "
                         "che doveva iniettare non è più nel documento, e la "
                         "prova passerebbe per la ragione sbagliata"
                         % (vecchio[:60], testo.count(vecchio)))
    return testo.replace(vecchio, nuovo)


def main():
    codice, testo = gira(BASE)
    if codice != 0:
        raise SystemExit("il contatore non è verde prima di cominciare:\n" + testo)
    print("prima della prova: verde")

    radice = copia_progetto()
    # la copia deve essere fedele: se i documenti copiati fossero meno, il conto
    # sarebbe un altro e ogni difetto sotto passerebbe senza essere visto
    originali = len([f for f in os.listdir(os.path.join(BASE, "docs"))
                     if f.endswith(".md")])
    copiati = len(os.listdir(os.path.join(radice, "docs")))
    if originali != copiati:
        raise SystemExit("la copia ha %d documenti e il progetto ne ha %d"
                         % (copiati, originali))

    provati = []

    def difetto(nome, cosa, atteso):
        """Iniettare il difetto, pretendere che il contatore lo dica, rimettere."""
        t = leggi(radice, AUDIT)
        r = leggi(radice, README)
        t, r = cosa(t, r)
        # la prova scrive **t** sull'audit e **r** sul README: se le due cose
        # tornassero scambiate, l'audit prenderebbe il testo del README e la
        # prova passerebbe senza aver guardato il posto giusto
        assert t.startswith("---"), \
            "il primo valore restituito dalla prova non è l'audit"
        assert r.lstrip().startswith("# I cinque duchi"), \
            "il secondo valore restituito dalla prova non è il README"
        scrivi(radice, AUDIT, t)
        scrivi(radice, README, r)
        codice, uscita = gira(radice)
        provati.append((nome, codice, atteso, uscita))
        # si rimette subito: la prova successiva parte dal documento vero
        scrivi(radice, AUDIT, leggi(BASE, "docs/" + AUDIT))
        shutil.copy(os.path.join(BASE, README), os.path.join(radice, README))

    # 1. il numero delle sezioni, indietro di uno: il difetto del 04/10
    #    Il numero si legge dal documento (`_meno_uno`): fino al 07/10/2026 era
    #    scritto qui, e ogni nuova sezione di questioni rompeva la prova.
    difetto("le sezioni dichiarate sono una di meno",
            lambda t, r: (_meno_uno(t, r"\| Documenti con una sezione «Questioni aperte» \| \*\*\d+\*\* \|",
                                    "la riga delle sezioni", 1), r),
            "sezioni")

    # 2. il numero delle voci, che nessuno ricalcola a mano
    difetto("le voci enumerate sono una di meno",
            lambda t, r: (_meno_uno(t, r"\| Voci enumerate \| \*\*\d+\*\* \|",
                                    "la riga delle voci", 1), r),
            "voci")

    # 3. una cella della tabella passa dalla cifra alla parola: il numero c'è
    #    per chi legge, e il controllo non lo vede più. Un controllo che tace
    #    quando non legge è peggio di uno che non esiste, perché sembra che
    #    guardi. Il grassetto che va via non è invece un difetto: il confronto
    #    accetta la cifra sia in grassetto sia no, e la prova lo dichiara
    difetto("la riga «Aperte» scrive il numero in lettere",
            lambda t, r: (sostituisci(t,
                                      porzione(t, r"\| \*\*Aperte\*\* \| "
                                              r"\*\*\d+\*\* \|", "la riga «Aperte»"),
                                      "| **Aperte** | ottantasette |"), r),
            "non e' leggibile")

    # 4. l'itinerari torna fuori dal §4: era contato e non elencato
    difetto("`itinerari.md` non compare più in nessuna intestazione del §4",
            lambda t, r: (sostituisci(t, "### Itinerari (`itinerari.md` 1)\n\n"
                                           "| Domanda | Chi decide |\n|---|---|\n"
                                           "| Le cinque tappe del primo anno senza facoltativi: "
                                           "sono un dato o una dimenticanza? Se sono un dato, "
                                           "va scritto perché sono cinque e non tre | Pietro |\n",
                                           ""), r),
            "non compare in nessuna intestazione")

    # 5. un numero del §4 senza il nome del documento: nessuno lo conta
    difetto("una cifra del §4 senza il nome del suo documento",
            lambda t, r: (sostituisci(t, "### Percorsi (`percorsi.md` 5)",
                                      "### Percorsi (restano 5)"), r),
            "senza il nome del documento")

    # 6. il numero di un documento sbagliato nel §4, di uno
    difetto("il §4 dichiara 4 altre per `luoghi.md` invece di 2",
            lambda t, r: (sostituisci(t, "### Luoghi (`luoghi.md` 2)", "### Luoghi (`luoghi.md` 4)"), r),
            "il §4 dichiara 4 per luoghi.md")
    difetto("il §4 dichiara 5 altre per `gioco.md` invece di 5 (somma rotta)",
            lambda t, r: (_sposta(t, r"gioco \(`gioco\.md` \d+\)", "il numero di gioco.md nel §4", 0, 1), r),
            "sommano")

    # 7. il numero in lettere del §2, che è un titolo e non un conteggio libero
    difetto("il §2 si intitola «cinque bloccanti» con una scheda aperta",
            lambda t, r: (sostituisci(t, "## 2. Una bloccante",
                                      "## 2. Le cinque bloccanti"), r),
            "cinque bloccanti")

    # 8. il numero di importanti in lettere, senza che nessuna voce I cambi
    #    La riga si cerca, non si sa: dal 07/10/2026 le importanti sono
    #    diciotto, e la parola iniettata («sette») e' scelta lontana dal conto.
    difetto("il §1 dichiara sette importanti con piu' voci I aperte",
            lambda t, r: (sostituisci(t, porzione(t, r"\| Di cui importanti \(cambiano il gioco\) \| \w+ \|",
                                                  "la riga delle importanti"),
                                      "| Di cui importanti (cambiano il gioco) | sette |"), r),
            "sette importanti")

    # 9. il numero di chiuse in prosa, che è la via che il registro non copre.
    #    Fino al 06/10/2026 la frase stava anche nel §6; il §6 ora la dice
    #    senza numero, e la frase che resta e' quella del §1.
    difetto("l'audit scrive «nessuna delle ventotto chiuse» in §1",
            lambda t, r: (sostituisci(t,
                                      porzione(t, r"Una sola delle \w+ chiuse è bloccante",
                                              "la frase sulle chiuse del §1"),
                                      "Una sola delle ventotto chiuse è bloccante"), r),
            "ventotto chiuse")

    # 10. i numeri che il README copia, che è il buco vero di questa prova.
    #     Il primo tentativo li scriveva nell'ordine sbagliato — `(r, sostituisci(r, …))`
    #     invece di `(t, sostituisci(r, …))` — e finiva per sovrascrivere l'audit con
    #     il README: la prova si annullava da sola e non si accorgeva di non
    #     aver provato niente. Un difetto nella prova è un difetto della prova,
    #     non del verificatore.
    #     L'atteso e' la **forma** della frase («importanti», «l'audit dice») e
    #     non la cifra: la cifra la decide il documento, e un'atteso con la
    #     cifra dentro si rompe da sola alla prima chiusura — che e' gia'
    #     successo una volta su questi due difetti.
    difetto("il README scrive un numero di importanti diverso dall'audit",
            lambda t, r: (t, _piu_uno(r, r"\d+ chiuse, \d+ aperte\*\*, \d+ bloccant[ei] e "
                                      r"\d+ importanti",
                                      "i numeri che il README copia")),
            "importanti")

    difetto("il README scrive un conto di chiuse e aperte diverso dall'audit",
            lambda t, r: (t, _meno_uno(r, r"\d+ chiuse, \d+ aperte\*\*",
                                       "i numeri che il README copia", 2)),
            "l'audit dice")

    difetto("il README scrive una voce enumerata di meno",
            lambda t, r: (t, _meno_uno(r, r"\d+ voci enumerate in \w+ sezioni",
                                       "le voci che il README copia", 1)),
            "voci enumerate")

    difetto("il README scrive «quindici sezioni»",
            lambda t, r: (t, sostituisci(r, porzione(r, r"in \w+ sezioni, \*\*\d+ chiuse",
                                                     "le sezioni in lettere del README"),
                                         "in quindici sezioni, **%s chiuse" % porzione(
                                             r, r"(?<=sezioni, \*\*)\d+(?= chiuse)",
                                             "le chiuse del README"))),
            "quindici sezioni")

    difetto("il README scrive «il progetto ha sedici documenti»",
            lambda t, r: (t, sostituisci(r, "il progetto ha **trentauno documenti**",
                                         "il progetto ha sedici documenti")),
            "sedici documenti")

    # 11. e il contrario, che è la parte difficile: il **registro** racconta il
    #     passato e non deve essere morso. Se il registro fosse confrontato, ogni
    #     versione passata che avesse contato meno voci darebbe un falso allarme,
    #     e un controllo che urlava ogni giorno verrebbe spento per legittima ragione
    codice, uscita = gira(radice)
    if codice != 0:
        raise SystemExit("la copia è rimasta sporca dopo undici difetti:\n" + uscita)
    print("la copia è tornata verde: ogni difetto è stato rimesso")

    falliti = 0
    print("\n%-58s %-8s %s" % ("difetto", "morso", "detto"))
    print("-" * 100)
    for nome, codice, atteso, uscita in provati:
        morso = codice != 0 and atteso in uscita
        print("%-58s %-8s %s" % (nome[:58], "sì" if morso else "NO", atteso))
        if not morso:
            falliti += 1
            print("   il contatore ha detto:")
            for riga in uscita.splitlines():
                if riga.startswith("  "):
                    print("     " + riga.strip())
    print("-" * 100)
    if falliti:
        print("difetti non visti: %d su %d" % (falliti, len(provati)))
        return 1

    # e la prova del registro: una riga di registro con un numero vecchio
    # non deve produrre problemi
    t = leggi(radice, AUDIT)
    t = sostituisci(t, "| 03/10/2026 | 0.5 |", "| 03/10/2026 | 0.5 | il conto passa a "
                    "**26 chiuse** e **88 aperte**, e le importanti da diciannove a "
                    "**sedici**. |")
    scrivi(radice, AUDIT, t)
    codice, uscita = gira(radice)
    if codice != 0:
        print("\nIl registro delle modifiche viene confrontato, e non deve: i suoi "
              "numeri sono quelli di allora.\n" + uscita)
        return 1
    print("\nIl registro non viene confrontato: i suoi numeri sono quelli di "
          "quando sono scritti.")
    print("difetti visti: %d su %d, più il registro lasciato in pace"
          % (len(provati), len(provati)))
    shutil.rmtree(radice, ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())