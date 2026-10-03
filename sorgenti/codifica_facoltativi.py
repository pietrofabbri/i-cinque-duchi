"""Codifica i facoltativi che non hanno ancora un codice, e dichiara i casidubbi.

**La domanda era**: un codice `Q` a ciascuno dei 269 facoltativi, così la regola dei
premi si verifica su tutti e non solo sui centocinquanta obbligatori. La misura dice
che i 269 sono **occorrenze**, non persone: dietro ci sono **248 persone distinte**,
di cui **49 hanno già un codice** (le 93 schede dell'anno 1 e le 120 degli anni 2-5).
Da codificare sono dunque **199**, e non 269.

**Il pericolo che la codifica meccanica avrebbe creato, e che questo file evita.**
Nei facoltativi ci sono nomi che sono un **cognome solo** — «Alberti», «Alfonso I»,
«Archita», «Alboino», «Appio Claudio» — accanto a un nome con macron
(`Al-Khwārizmī` accanto a `al-Khwarizmi`). Un codice nuovo per «Alberti» avrebbe
creato **una seconda persona** diversa da Leon Battista Alberti, che ha già `P20`, e
un codice nuovo per una variante con l'accento avrebbe creato un terzo
Al-Khwarizmi. In un catalogo le duplicazioni sono peggio che le assenze: un'assenza
si vede, una duplicazione si no, e la verifica dei premi passerebbe due volte sullo
 stesso volto contando due premi.

Per questo il confronto è **normalizzato** (diacritici, apici, spazi, maiuscole) e
inoltre ci sono tre esiti, non due:

- `codice` — la persona è già in un catalogo, o è nuova e il codice le è stato
  assegnato qui;
- `da_verificare` — il nome **sembra** una forma breve di qualcuno che ha già un
  codice (un cognome che è l'ultima parola del nome di una persona nota). Non si
  duplica e non si collega: si dichiara, e resta scritto il nome lungo che
  sospetterebbe;
- le varianti normalizzate che combaciano con una persona nota prendono **il suo**
  codice, senza crearne uno.

**Il numero che esce non viene scritto a mano**: tutto ciò che il file stampa è
calcolato da `dati/incontri_livelli.json` e dai cataloghi.

Uso:
    python3 sorgenti/codifica_facoltativi.py --prova
    python3 sorgenti/codifica_facoltativi.py
"""
import collections
import json
import os
import re
import unicodedata
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INC = os.path.join(BASE, "dati", "incontri_livelli.json")
USCITA = os.path.join(BASE, "dati", "videogioco-5-duchi-facoltativi.json")


def normalizza(nome):
    """Il nome come chiave di confronto: minuscolo, senza diacritici, senza apici.

    I diacritici si toccano perche' `Al-Khwārizmī` e `al-Khwarizmi` sono la stessa
    persona e due codici diversi sarebbero un difetto, non una precisione. La
    chiave non finisce in nessun file: serve solo a confrontare.
    """
    n = unicodedata.normalize("NFKD", nome.strip().lower())
    n = "".join(c for c in n if not unicodedata.combining(c))
    n = n.replace("’", "'").replace("`", "")
    n = re.sub(r"\s+", " ", n)
    return n.strip()


def senza_marcature(nome):
    """Il nome senza le marche fra parentesi e gli asterischi del testo."""
    n = re.sub(r"\([^)]*\)", " ", nome)
    n = n.replace("*", " ")
    return re.sub(r"\s+", " ", n).strip()


def persone_della(nome):
    """Il nome di una cella diventa l'elenco delle persone che contiene.

    Si divide solo sulla **virgola seguita da spazio**, e solo se ogni pezzo
    sembra un nome proprio. Una divisione sbagliata crea due codici per una
    persona sola, che è il difetto peggiore di questo lavoro; quindi la regola è
    stretta e quando non è sicura non divide.
    """
    parti = [p.strip() for p in nome.split(", ") if p.strip()]
    if len(parti) == 1:
        return [nome.strip()]

    def sembra_nome(p):
        if p.startswith("(") or p.endswith(")") or " e " in p:
            return False
        return p[:1].isupper()

    if all(sembra_nome(p) for p in parti):
        return parti
    return [nome.strip()]


def catalogo_anni_2_5():
    noti = {}
    for a in (2, 3, 4, 5):
        f = os.path.join(BASE, "dati",
                         "videogioco-5-duchi-anno%d-personaggi.json" % a)
        for p in json.load(open(f, encoding="utf-8"))["persone"]:
            noti[normalizza(p["nome"])] = p["codice"]
    return noti


def catalogo_anno_1():
    a1 = json.load(open(os.path.join(
        BASE, "dati", "videogioco-5-duchi-anno1-personaggi.json"),
        encoding="utf-8"))
    return {normalizza(p["nome"]): p["id"] for p in a1["personaggi"]}


def cognomi_noti():
    """L'ultima parola di ogni persona già codificata, con **tutti** i candidati.

    Serve a riconoscere un cognome solo: se «Alberti» compare da solo e una sola
    persona già codificata si chiama «Leon Battista Alberti», allora «Alberti» non
    è un'altra persona: non c'e' nessun altro a cui poter essere. Lo si collega, e
    la prova si scrive accanto.

    Se invece i candidati sono **due o piu'** — «Alfonso» potrebbe essere Alfonso I
    o Alfonso II — la scelta non la fa nessun file: la voce resta
    `da_verificare` con tutti i candidati elencati, perche' scegliere sarebbe
    inventare. E' la differenza fra un controllo che compie il lavoro e uno che
    finge di compierlo: il primo distingue il caso deciso dal caso aperto, il
    secondo dice «da verificare» a tutti e non distingue niente.
    """
    # I candidati sono **persone**, non codici: una persona che porta due codici
    # (succede a dodici nomi, uno per anno) resta una persona sola, e contarla due
    # volte faceva di «Alberti» un omonimo che non e' un omonimo. Si raggruppa per
    # nome normalizzato e si tiene il codice canonico.
    canonici, alias, _ = indice_persone()
    out = collections.defaultdict(list)
    for k, c in canonici.items():
        out[k.split()[-1]].append((c, k))
    return out


def indice_persone():
    """Una persona, un codice: l'indice che i cataloghi degli anni non hanno.

    Nei cataloghi **%d persone hanno due codici**: compaiono in due anni e hanno
    una scheda per anno, e nessuno dei due file si accorge che sono la stessa
    persona. Non e' un difetto degli anni, che sono fatti per anno: e' un difetto
    di nessun indice unico, ed e' lo stesso difetto che si era gia' visto sulle
    immagini, dove la stessa persona aveva due file.

    La regola dichiarata: **il codice canonico e' quello dell'anno 1** quando la
    persona c'e' anche li', perche' e' il primo in cui il gioco la incontra; se non
    c'e', e' il codice piu' basso della serie `Q`. Gli altri codici diventano
    **alias** e non spariscono: restano scritti, perche' i documenti degli anni li
    nominano, ma il motore e la verifica dei premi usano solo il canonico.

    Il risultato e' quello che chiude il buco: una verifica fatta sul codice
    canonico vale per tutte le occorrenze della persona, in tutti gli anni.
    """
    occorrenze = collections.defaultdict(list)
    for nome, codice in catalogo_anno_1().items():
        occorrenze[nome].append(codice)
    for nome, codice in catalogo_anni_2_5().items():
        occorrenze[nome].append(codice)
    canonici = {}
    alias = {}
    doppie = {}
    for nome, codici in occorrenze.items():
        if len(codici) == 1:
            canonici[nome] = codici[0]
            continue
        p = [c for c in codici if c.startswith("P")]
        if p:
            can = p[0]
        else:
            can = min(codici, key=lambda c: int(c[1:]))
        canonici[nome] = can
        alias[nome] = sorted(c for c in codici if c != can)
        doppie[nome] = sorted(codici)
    return canonici, alias, doppie


def principale(prova=False):
    d = json.load(open(INC, encoding="utf-8"))
    canonici, alias, doppie = indice_persone()
    noti = dict(canonici)

    # anche le voci obbligatorie hanno un codice: un facoltativo che è la stessa
    # persona dell'obbligatorio di un'altra tappa non deve crearne una nuova. Il
    # codice dell'obbligatorio passa dall'indice, cosi' anche lui ha il canonico.
    for t in d["incontri"]:
        v = t.get("voce_obbligatoria") or {}
        if v.get("codice"):
            k = normalizza(senza_marcature(v["nome"]))
            if k in canonici:
                v["codice_canonico"] = canonici[k]
            else:
                noti.setdefault(k, v["codice"])

    prossimo = 1 + max(int(c[1:]) for c in noti.values() if c.startswith("Q"))
    cognomi = cognomi_noti()

    persone = collections.OrderedDict()
    for t in d["incontri"]:
        for f in (t.get("facoltativi") or []):
            for p in persone_della(f["nome"]):
                pulito = senza_marcature(p)
                k = normalizza(pulito)
                v = persone.setdefault(k, {
                    "nome": pulito, "anni": [], "tappe": [], "codice": None,
                    "esito": None, "perche": None, "nome_cellula": f["nome"]})
                if t["anno"] not in v["anni"]:
                    v["anni"].append(t["anno"])
                if t["livello"] not in v["tappe"]:
                    v["tappe"].append(t["livello"])

    nuovi = 0
    verificare = 0
    collegati = 0
    for k, v in persone.items():
        if k in noti:
            v["codice"] = noti[k]
            v["esito"] = "gia_codificato"
            v["perche"] = "il nome combacia con una scheda che ha gia' il codice"
            continue
        parole = k.split()
        if len(parole) == 1 and k in cognomi:
            candidati = cognomi[k]
            if len(candidati) == 1:
                codice, nome_lungo = candidati[0]
                v["esito"] = "collegato"
                v["codice"] = codice
                v["nome_completo"] = nome_lungo
                v["perche"] = ("cognome solo, e %s e' l'unica persona gia' codificata "
                               "che lo porta: il codice e' il suo, non un codice "
                               "nuovo" % nome_lungo)
                collegati += 1
            else:
                v["esito"] = "da_verificare"
                v["codice"] = None
                v["candidati"] = sorted("%s (%s)" % (n, c) for c, n in candidati)
                v["perche"] = ("cognome solo, e %d persone gia' codificate lo portano: "
                               "%s. Non si duplica e non si sceglie, perche' scegliere "
                               "sarebbe inventare una persona"
                               % (len(candidati), "; ".join(sorted(n for _, n in candidati))))
                verificare += 1
            continue
        prossimo += 1
        v["codice"] = "Q%d" % prossimo
        v["esito"] = "nuovo"
        v["perche"] = "non e' in nessun catalogo: codice assegnato qui"
        nuovi += 1

    # La verifica: **una persona, un codice, e un codice a una persona sola**.
    # Il confronto non e' fra le stringhe che si vedono, perche' «Tasso» e
    # «Torquato Tasso» sono la stessa persona e la guardia si fermava su due false
    # accuse. Si confronta la **persona**: chi e' stato collegato porta con se' il
    # nome lungo, e li' si confronta. Un codice che resta su due nomi lunghi
    # diversi e' una duplicazione vera, ed e' quello che si cerca.
    per_codice = collections.defaultdict(set)
    for k, v in persone.items():
        if not v["codice"]:
            continue
        # normalizzato, perche' «Torquato Tasso» e «torquato tasso» sono la
        # stessa persona e il confronto ne'Due faceva due
        identita = normalizza(v.get("nome_completo") or v["nome"])
        per_codice[v["codice"]].add(identita)
    doppi = {c: sorted(n) for c, n in per_codice.items() if len(n) > 1}
    if doppi:
        raise SystemExit("codici attribuiti a piu' persone: %s" % doppi)

    # I codici **nuovi** non possono cozzare con quelli dei cataloghi. La guardia
    # non guarda tutti i codici usati, perche' quelli che una persona gia' aveva
    # vengono ripresi apposta e occupano un posto che e' proprio il loro: la
    # prima versione li contava come conflitto e si fermava su 52 codici, tutti
    # legittimi. Un controllo che non distingue «rubato» da «ripreso» non serve
    # a niente e impedisce di vedere i conflitti veri.
    occupati = set(noti.values())
    nuovi_usati = {v["codice"] for v in persone.values() if v["esito"] == "nuovo"}
    clash = sorted(nuovi_usati & occupati)
    if clash:
        raise SystemExit("codici nuovi gia' in uso nei cataloghi: %s" % clash)
    ripresi = sum(1 for v in persone.values() if v["esito"] == "gia_codificato")
    if len(per_codice) != len(set(
            normalizza(v.get("nome_completo") or v["nome"])
            for v in persone.values() if v["codice"])):
        raise SystemExit("il conto dei codici non torna: %d codici per %d persone"
                         % (len(per_codice), sum(1 for v in persone.values()
                                                  if v["codice"])))

    # il JSON degli incontri riceve il codice di ogni facoltativo
    for t in d["incontri"]:
        for f in (t.get("facoltativi") or []):
            parti = persone_della(f["nome"])
            codici = []
            for p in parti:
                v = persone[normalizza(senza_marcature(p))]
                f["codice"] = v["codice"]
                f["codice_esito"] = v["esito"]
                f["codice_perche"] = v["perche"]
                codici.append(v["codice"] or "(da verificare)")
            f["codici"] = codici

    schede = sorted(persone.values(), key=lambda v: v["codice"] or "ZZZ")
    out = {
        "_nota": ("Catalogo dei facoltativi: le %d occorrenze di facoltativo "
                  "dei 150 incontri sono %d persone distinte, di cui %d avevano "
                  "gia' un codice. Il confronto fra nomi e' normalizzato sui "
                  "diacritici, perche' due grafie della stessa persona non "
                  "possono diventare due codici. Le voci `da_verificare` sono "
                  "quelle in cui il nome e' un cognome solo che qualcun altro gia' "
                  "porta: non si duplicano e non si collegano, perche' scegliere "
                  "qui sarebbe inventare una persona." % (
                      sum(len(t.get("facoltativi") or []) for t in d["incontri"]),
                      len(persone), len(persone) - nuovi - verificare
                      - collegati)),
        "_indice_persone": {
            "regola": "il codice canonico e' quello dell'anno 1 quando la persona "
                      "c'e' anche li', altrimenti il piu' basso della serie Q; gli "
                      "altri codici sono alias e restano scritti",
            "persone_con_due_codici": len(doppie),
            "codici_alias": {k: v for k, v in sorted(alias.items())},
        },
        "_collegati": ("%d facoltativi comparivano col solo cognome; sono stati "
                       "collegati al codice della persona, non con uno nuovo, "
                       "perche' il cognome non poteva essere di nessun altro" % collegati),
        "_generato_da": "sorgenti/codifica_facoltativi.py",
        "persone": schede,
    }

    print("persone con due codici nei cataloghi degli anni : %d" % len(doppie))
    print("  (il codice canonico e' quello dell'anno 1; gli altri sono alias)")
    print()
    print("persone distinte dietro i facoltativi : %d" % len(persone))
    print("  con codice gia' nei cataloghi         : %d"
          % (len(persone) - nuovi - verificare - collegati))
    print("  cognome solo, collegato al suo codice : %d" % collegati)
    print("  codici nuovi assegnati qui           : %d" % nuovi)
    print("  da verificare (omonimi)               : %d" % verificare)
    print("  ultimo codice Q usato                 : Q%d" % prossimo)
    if verificare:
        print()
        print("da verificare:")
        for v in schede:
            if v["esito"] == "da_verificare":
                print("   %-22s %s" % (v["nome"], v["perche"][:88]))

    if not prova:
        with open(INC, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=1)
            f.write("\n")
        with open(USCITA, "w", encoding="utf-8") as f:
            json.dump(out, f, ensure_ascii=False, indent=1)
            f.write("\n")
        print("\nscritti: %s e %s" % (os.path.relpath(INC, BASE),
                                      os.path.relpath(USCITA, BASE)))
    return 0


if __name__ == "__main__":
    sys.exit(principale(prova="--prova" in sys.argv))