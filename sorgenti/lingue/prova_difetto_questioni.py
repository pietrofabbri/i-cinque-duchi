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
    difetto("le sezioni dichiarate sono 15 su 16",
            lambda t, r: (sostituisci(t, "| Documenti con una sezione «Questioni aperte» | **16** |",
                                      "| Documenti con una sezione «Questioni aperte» | **15** |"), r),
            "sezioni")

    # 2. il numero delle voci, che nessuno ricalcola a mano
    difetto("le voci enumerate sono 119",
            lambda t, r: (sostituisci(t, "| Voci enumerate | **118** |",
                                      "| Voci enumerate | **119** |"), r),
            "voci")

    # 3. una cella della tabella passa dalla cifra alla parola: il numero c'è
    #    per chi legge, e il controllo non lo vede più. Un controllo che tace
    #    quando non legge è peggio di uno che non esiste, perché sembra che
    #    guardi. Il grassetto che va via non è invece un difetto: il confronto
    #    accetta la cifra sia in grassetto sia no, e la prova lo dichiara
    difetto("la riga «Aperte» scrive il numero in lettere",
            lambda t, r: (sostituisci(t, "| **Aperte** | **87** |",
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
            lambda t, r: (sostituisci(t, "gioco (`gioco.md` 5)", "gioco (`gioco.md` 6)"), r),
            "sommano")

    # 7. il numero in lettere del §2, che è un titolo e non un conteggio libero
    difetto("il §2 si intitola «cinque bloccanti» con quattro schede aperte",
            lambda t, r: (sostituisci(t, "## 2. Le quattro bloccanti",
                                      "## 2. Le cinque bloccanti"), r),
            "cinque bloccanti")

    # 8. il numero di importanti in lettere, senza che nessuna voce I cambi
    difetto("il §1 dichiara sedici importanti con quindici voci I aperte",
            lambda t, r: (sostituisci(t, "| Di cui importanti (cambiano il gioco) | quindici |",
                                      "| Di cui importanti (cambiano il gioco) | sedici |"), r),
            "sedici importanti")

    # 9. il numero di chiuse in prosa, che è la via che il registro non copre
    difetto("l'audit scrive «nessuna delle ventotto chiuse» in §6",
            lambda t, r: (sostituisci(t, "nessuna delle trentuno chiuse le toccava",
                                      "nessuna delle ventotto chiuse le toccava"), r),
            "ventotto chiuse")

    # 10. i numeri che il README copia, che è il buco vero di questa prova.
    #     Il primo tentativo li scriveva nell'ordine sbagliato — `(r, sostituisci(r, …))`
    #     invece di `(t, sostituisci(r, …))` — e finiva per sovrascrivere l'audit con
    #     il README: la prova si annullava da sola e non si accorgeva di non
    #     aver provato niente. Un difetto nella prova è un difetto della prova,
    #     non del verificatore.
    difetto("il README scrive «16 importanti»",
            lambda t, r: (t, sostituisci(r, "31 chiuse, 87 aperte**, 4 bloccanti e 15 importanti",
                                         "31 chiuse, 87 aperte**, 4 bloccanti e 16 importanti")),
            "16 importanti")

    difetto("il README scrive «30 chiuse, 86 aperte»",
            lambda t, r: (t, sostituisci(r, "31 chiuse, 87 aperte**",
                                         "30 chiuse, 86 aperte**")),
            "30 chiuse, 86 aperte")

    difetto("il README scrive «117 voci enumerate»",
            lambda t, r: (t, sostituisci(r, "118 voci enumerate in sedici sezioni",
                                         "117 voci enumerate in sedici sezioni")),
            "117 voci enumerate")

    difetto("il README scrive «quindici sezioni»",
            lambda t, r: (t, sostituisci(r, "in sedici sezioni", "in quindici sezioni")),
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