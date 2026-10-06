#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""I numeri scritti in prosa e chi li confronta col dato: N1-N5.

I7 confronta i numeri che **una** sezione dichiara con il file. La regola che
lo ha motivato — *un numero giusto e una frase sbagliata* — e' generale: vale
per ogni numero scritto in prosa in ogni documento. Questo controllo la porta
a tutti i documenti, e chiede la domanda che I7 si faceva per gli interni:
**questa frase e' un numero, e qualcuno lo confronta col dato?**

La misura prima è questa: i documenti del progetto portano, fuori dai
registri e dalle tabelle, **3634 numeri scritti in prosa**. Non si possono
guardare uno a uno, e un controllo che ne guarda qualcuno e dice «la regola è
generale» mente per la parte che non guarda. Perciò la domanda è posta alla
granaia giusta, che è il **documento**: un documento o ha un controllo che
legge i suoi numeri, o non ne ha nessuno, e in quel caso lo dice.

  N1  l'inventario dei numeri in prosa è generato, e rigenerarlo dà lo stesso
      sha: un inventario scritto a mano invecchia come tutti gli altri numeri
  N2  ogni documento dichiara il controllo che guarda i suoi numeri, o il
      motivo per cui non ne ha uno: nessun documento resta senza risposta
  N3  il controllo dichiarato esiste davvero nel ramo
  N4  il controllo dichiarato si appoggia a qualche riferimento vero: il suo
      codice nomina il documento o il suo dato. Una dichiarazione che non ha
      dietro niente è una promessa, e una promessa non è un controllo
  N5  il conto è dichiarato nel README e non cresce da solo

**Il conto di N4 è un numero che può essere diverso da zero, e va letto.** Un
documento può dichiarare un controllo che non lo guarda per intero: il
controllo guarda una sezione, e il documento ne ha dodici. Il numero dice
quante dichiarazioni reggono solo in parte, che è la misura onesta di quanto il
progetto crede di controllare e quanto non crede.

Uso:  python3 sorgenti/verifica_numeri.py
      python3 sorgenti/verifica_numeri.py --rigenera   # riscrive l'inventario
      python3 sorgenti/verifica_numeri.py --difetti    # ne inietta cinque
"""
import hashlib
import io
import json
import os
import re
import sys

RADICE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Il registro dei buchi del progetto sta in un file solo:
# i tre elenchi non si scrivono qui.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import buchi  # noqa: E402
DOCS = os.path.join(RADICE, "docs")
INVENTARIO = os.path.join(RADICE, "dati", "numeri_prosa.json")
README = os.path.join(RADICE, "README.md")

# Il numero in prosa: una cifra o una parola, seguite da un nome. `| **7** |`
# dentro una tabella non è prosa, e le righe di tabella sono escluse: un
# numero in tabella è un dato con la sua colonna, un numero in prosa è una
# frase che invecchia.
PAROLE = ("zero|uno|due|tre|quattro|cinque|sei|sette|otto|nove|dieci|undici|"
          "dodici|tredici|quattordici|quindici|sedici|diciassette|diciotto|"
          "diciannove|venti|ventuno|ventidue|ventitré|ventiquattro|venticinque|"
          "ventisei|ventisette|ventotto|ventinove|trenta|quaranta|cinquanta|"
          "sessanta|settanta|ottanta|novanta|cento|duecento|trecento|quattrocento"
          "|cinquecento|seicento|settecento|ottocento|novecento|mille")
NUMERO = re.compile(r"(?<![A-Za-z0-9/§.-])(\d{1,4}|%s)\s+"
                    r"([a-zA-Zà-ù][\wà-ù'-]{2,})" % PAROLE)
# Il registro delle modifiche racconta il passato: i suoi numeri sono quelli
# che erano veri il giorno in cui la riga è stata scritta.
REGISTRO = re.compile(r"(?m)^#{2,3} .*[Rr]egistro")
NUMERI_DICHIARATI = {"tre": 3, "quattro": 4, "cinque": 5, "sei": 6,
                     "sette": 7, "otto": 8, "nove": 9, "dieci": 10,
                     "undici": 11, "dodici": 12, "tredici": 13,
                     "quattordici": 14, "quindici": 15, "sedici": 16,
                     "diciassette": 17, "diciotto": 18, "diciannove": 19,
                     "venti": 20, "trenta": 30, "quaranta": 40, "cento": 100,
                     "duecento": 200, "trecento": 300, "quattrocento": 400,
                     "cinquecento": 500, "seicento": 600, "settecento": 700,
                     "ottocento": 800, "novecento": 900, "mille": 1000}

# **Il documento e il controllo che guarda i suoi numeri.** Ogni riga è una
# dichiarazione, e N4 la mette alla prova: il codice del controllo deve
# nominare il documento o il suo dato.
GUARDATO = {
    "videogioco-5-duchi-fonti-visive.md": [
        "sorgenti/verifica_fonti_visive.py", "sorgenti/verifica_tavolozza.py",
        "sorgenti/verifica_ambienti.py", "sorgenti/verifica_colori.py"],
    "videogioco-5-duchi-luoghi-edifici.md": ["sorgenti/verifica_interni.py"],
    "videogioco-5-duchi-luoghi.md": [
        "sorgenti/verifica_catena_luoghi.py"],
    "videogioco-5-duchi-furioso.md": [
        "sorgenti/furioso/verifica_citazioni.py"],
    "videogioco-5-duchi-mappe.md": [
        "sorgenti/gis/verifica_pin.py", "sorgenti/gis/verifica_altitudine.py",
        "sorgenti/gis/verifica_sagome.py", "sorgenti/verifica_coerenza.py"],
    "videogioco-5-duchi-sequenza.md": ["sorgenti/verifica_sequenza.py"],
    "videogioco-5-duchi-parlato.md": ["sorgenti/verifica_parlato.py"],
    "videogioco-5-duchi-premi.md": [
        "sorgenti/verifica_premi.py", "sorgenti/art/verifica_premi_emblemi.py"],
    "videogioco-5-duchi-inventario.md": ["sorgenti/verifica_inventario.py"],
    "videogioco-5-duchi-pedagogia.md": ["sorgenti/verifica_pedagogia.py"],
    "videogioco-5-duchi-ripassi.md": ["sorgenti/verifica_ripassi.py"],
    "videogioco-5-duchi-audit.md": ["sorgenti/lingue/conta_questioni.py"],
    "videogioco-5-duchi-lingue-immagini.md": [
        "sorgenti/lingue/verifica_immagini_oggetti.py"],
    "videogioco-5-duchi-ritratti.md": ["sorgenti/art/verifica_immagini.py"],
    "videogioco-5-duchi-modello-di-livello.md": ["sorgenti/verifica_modello.py"],
}

# I documenti senza un controllo dei loro numeri, e i motivi.
#
# **Non si scrivono qui**: stanno in `dati/buchi_aperto.json`, che è l'unico
# registro dei buchi del progetto, e si leggono da `sorgenti/buchi.py`. Un
# elenco in tre file non è un registro. N2 è rosso se un documento non è
# dichiarato in nessuno dei due posti.
SENZA = buchi.elenco("SENZA")

# **Le dichiarazioni che N4 non puo' reggere**, e perche'. Sono controlli che
# guardano il dato di un documento senza nominarlo: il documento descrive il
# gioco, il controllo guarda il file. Il numero resta nel conto di N5, e non e'
# una scusa: e' la misura di quanti documenti credono di essere guardati e non
# lo sono nel senso stretto della parola.
SENZA_APPOGGIO = buchi.elenco("SENZA_APPOGGIO")

SEZIONE_CONTO = "## I numeri scritti in prosa"
CONTI = ("Documenti con un controllo dichiarato", "Documenti senza controllo",
         "Numeri in prosa contati", "Documenti interamente guardati",
         "Dichiarazioni senza riscontro nel codice")


def leggi(path):
    with io.open(path, encoding="utf-8") as f:
        return f.read()


def numeri_prosa(testo):
    """I numeri scritti in prosa, con la riga e il nome che seguono.

    Le righe di tabella sono escluse: `| **6** |` è un dato con la sua colonna,
    e dentro una tabella il numero ha un posto dove essere confrontato. Quello
    che invecchia è il numero che sta in una frase.
    """
    dentro = REGISTRO.search(testo)
    fuori = testo[:dentro.start()] if dentro else testo
    trovati = []
    for numero_riga, riga in enumerate(fuori.splitlines(), 1):
        secca = riga.strip()
        if not secca or secca.startswith(("|", ">", "#", "```")):
            continue
        for m in NUMERO.finditer(riga):
            parola = m.group(1)
            valore = (int(parola) if parola.isdigit()
                      else NUMERI_DICHIARATI.get(parola))
            trovati.append({"numero": valore, "scritto": parola,
                            "soggetto": m.group(2), "riga": numero_riga})
    return trovati


def documenti():
    for n in sorted(os.listdir(DOCS)):
        if n.endswith(".md"):
            yield n, leggi(os.path.join(DOCS, n))


def codice(percorso):
    completo = os.path.join(RADICE, percorso)
    if not os.path.exists(completo):
        return None
    return leggi(completo)


def appoggi(percorso, nome_doc, testo_doc):
    """Il controllo guarda davvero questo documento? Cita il documento o il
    suo dato? Le due cose che un controllo guarda sono il testo del documento
    e il file che il documento descrive."""
    sorgente = codice(percorso)
    if sorgente is None:
        return None
    if nome_doc in sorgente or nome_doc[:-3] in sorgente:
        return True
    dati = re.findall(r"`(dati/[\w./-]+\.json)`", testo_doc)
    for d in dati:
        if os.path.basename(d) in sorgente:
            return True
    return False


def inventario():
    """L'inventario dei numeri in prosa, per documento."""
    out = {}
    for nome, testo in documenti():
        out[nome] = numeri_prosa(testo)
    return out


def sha_dell_inventario(inv):
    return hashlib.sha256(
        json.dumps(inv, ensure_ascii=False, sort_keys=True,
                   indent=1).encode("utf-8")).hexdigest()


def scrivi_inventario(inv):
    con = io.open(INVENTARIO, "w", encoding="utf-8")
    con.write(json.dumps(inv, ensure_ascii=False, sort_keys=True, indent=1))
    con.write("\n")
    con.close()


def leggi_conto(testo):
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


def controlla(problemi, inv=None, guardato=None, senza=None, conto=None):
    """I cinque controlli.

    L'inventario, le due mappe e il conto arrivano dalla chiamata: la prova
    del difetto ne passa di alterati e nessun file vero viene toccato.
    """
    inv = inventario() if inv is None else inv
    guardato = GUARDATO if guardato is None else guardato
    senza = SENZA if senza is None else senza
    testi = dict(documenti())

    # ---- N1: l'inventario e' quello del file
    if os.path.exists(INVENTARIO):
        salvato = json.loads(leggi(INVENTARIO))
        if sha_dell_inventario(salvato) != sha_dell_inventario(inv):
            problemi.append(
                "N1 dati/numeri_prosa.json non e' quello che i documenti "
                "danno: l'inventario e' un file generato e va rigenerato "
                "(python3 sorgenti/verifica_numeri.py --rigenera)")
    else:
        problemi.append(
            "N1 dati/numeri_prosa.json non esiste: l'inventario si genera "
            "con --rigenera")

    # ---- N2 e N3: ogni documento dichiara, e la dichiarazione esiste
    numeri = 0
    guardati = 0
    interi = 0
    senza_appoggio = []
    for nome in sorted(testi):
        numeri += len(inv.get(nome, []))
        if nome in guardato:
            guardati += 1
            if len(inv.get(nome, [])) == 0:
                interi += 1
            for percorso in guardato[nome]:
                if codice(percorso) is None:
                    problemi.append(
                        "N3 %s dichiara %s, che nel ramo non c'e'" % (nome, percorso))
                    continue
                if appoggi(percorso, nome, testi[nome]) is False:
                    senza_appoggio.append("%s -> %s" % (nome, percorso))
        elif nome in senza and senza[nome].strip():
            continue
        else:
            problemi.append(
                "N2 %s non dichiara il controllo che guarda i suoi numeri, e "
                "non e' nella lista di quelli che non ne hanno: un documento "
                "senza controllo che non lo dice e' un documento che nessuno "
                "guarda" % nome)

    # ---- N4: la dichiarazione si appoggia a un riferimento vero
    for coppia in sorted(senza_appoggio):
        if not SENZA_APPOGGIO.get(coppia, "").strip():
            problemi.append(
                "N4 %s: il codice del controllore non nomina ne' il documento "
                "ne' il suo dato, e non c'e' un motivo scritto che lo dichiari"
                % coppia)

    # ---- N5: il conto e' quello dichiarato
    letto = leggi_conto(leggi(README)) if conto is None else conto
    atteso = {"Documenti con un controllo dichiarato": guardati,
              "Documenti senza controllo": len(testi) - guardati,
              "Numeri in prosa contati": numeri,
              "Documenti interamente guardati": interi,
              "Dichiarazioni senza riscontro nel codice": len(senza_appoggio)}
    for riga, valore in atteso.items():
        if riga not in letto:
            problemi.append(
                "N5 README.md: la tabella dei numeri non ha la riga «%s»" % riga)
        elif letto[riga] != valore:
            problemi.append(
                "N5 README.md: la riga «%s» dichiara %d, il conto e' %d"
                % (riga, letto[riga], valore))
    return atteso


def inietta(difetto, inv):
    """Un difetto alla volta, tutto in memoria: nessun file vero si tocca."""
    import copy
    if difetto == "N1":
        # l'inventario non e' piu' quello dei documenti: manca un numero
        alterato = copy.deepcopy(inv)
        for nome, voci in alterato.items():
            if voci:
                alterato[nome] = voci[:-1]
                break
        return {"inv": alterato}
    if difetto == "N2":
        # un documento sparisce da entrambe le liste: nessuna risposta
        guardato = dict(GUARDATO)
        senza = dict(SENZA)
        for nome in sorted(senza):
            if nome.endswith(".tacito"):
                continue
            senza.pop(nome)
            return {"inv": inv, "guardato": guardato, "senza": senza}
        return None
    if difetto == "N3":
        # un documento dichiara un controllore che nel ramo non c'e'
        guardato = dict(GUARDATO)
        nome = sorted(guardato)[0]
        guardato[nome] = guardato[nome] + ["sorgenti/verifica_che_non_esiste.py"]
        return {"inv": inv, "guardato": guardato}
    if difetto == "N4":
        # una dichiarazione senza nessun riferimento nel codice
        guardato = dict(GUARDATO)
        nome = sorted(guardato)[0]
        guardato[nome] = guardato[nome] + ["sorgenti/verifica_coerenza.py"]
        return {"inv": inv, "guardato": guardato}
    if difetto == "N5":
        # il conto del README non torna: il numero piu' vicino e' spostato
        letto = leggi_conto(leggi(README))
        riga = "Documenti con un controllo dichiarato"
        if riga not in letto:
            return None
        letto[riga] = letto[riga] + 3
        return {"inv": inv, "conto": letto}
    raise ValueError(difetto)


def main():
    sola_prova = "--difetti" in sys.argv
    inv = inventario()

    if "--rigenera" in sys.argv:
        scrivi_inventario(inv)
        print("inventario scritto: %s (%d numeri)"
              % (os.path.relpath(INVENTARIO, RADICE),
                 sum(len(v) for v in inv.values())))
        return 0

    problemi = []
    atteso = controlla(problemi, inv)

    print("== N1-N5. i numeri scritti in prosa, e chi li guarda")
    print("   documenti: %d, con un controllo dichiarato: %d, senza: %d"
          % (atteso["Documenti con un controllo dichiarato"]
             + atteso["Documenti senza controllo"],
             atteso["Documenti con un controllo dichiarato"],
             atteso["Documenti senza controllo"]))
    print("   numeri in prosa contati: %d" % atteso["Numeri in prosa contati"])
    print("   dichiarazioni senza riscontro nel codice: %d"
          % atteso["Dichiarazioni senza riscontro nel codice"])
    if problemi:
        for p in problemi:
            print("   difetto %s" % p)
    else:
        print("   ogni documento dichiara il controllo che guarda i suoi "
              "numeri o il motivo per cui non ne ha uno, ogni controllo "
              "dichiarato esiste, l'inventario e' quello dei documenti, e il "
              "conto e' quello dichiarato")

    if sola_prova:
        iniettati = 0
        visti = 0
        for difetto in ("N1", "N2", "N3", "N4", "N5"):
            alterato = inietta(difetto, inv)
            if alterato is None:
                print("   NON INIETTATO  %s" % difetto)
                continue
            iniettati += 1
            problemi2 = []
            controlla(problemi2, **alterato)
            trovati = [p for p in problemi2 if p.startswith(difetto + " ")]
            if trovati:
                visti += 1
                for p in trovati:
                    print("   visto   %s" % p[:110])
            else:
                print("   NON VISTO  %s" % difetto)
        print("\ndifetti iniettati: %d, visti: %d, non visti: %d"
              % (iniettati, visti, iniettati - visti))
        if visti != iniettati:
            return 1

    return 1 if problemi else 0


if __name__ == "__main__":
    sys.exit(main())
