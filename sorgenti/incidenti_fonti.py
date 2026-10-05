#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Costruisce `dati/fonti_visive/incidenti.json`: i tre incidenti del gioco.

**I due vuoti che il capitolo dichiarava dal 2 ottobre erano la parte vera di
una domanda che nessuno aveva fatto.** Il capitolo scriveva: «l'incendio e la
carestia non hanno immagine, il vuoto e' reale». Il vuoto e' reale — e non
importa — ma la domanda giusta non era *che immagine ha un incendio*: era
**che cosa mostra il gioco quando un incendio e' in scena**. La risposta e'
scandita dai documenti, non decisa qui, ed e' la stessa per tutte e tre le
voci:

  - **4-3 (Qin Shi Huang)** l'incendio dei libri del 213 a.C. e' la **memoria**
    («l'uomo che bruciò i libri») e l'emblema della tappa e' **un peso di
    bronzo**;
  - **4-10 (Ercole II)** l'incendio dell'archivio del 1534 e' una
    **ricostruzione** e l'emblema e' **uno scaffale vuoto con un cartellino
    scritto a metà**;
  - **4-13 (Ipazia)** l'incendio e' la **memoria**, «un racconto di secoli
    dopo», e l'emblema e' **un frammento di stele**.

Tre tappe, tre oggetti, **nessuna fiamma**. Il gioco non rappresenta
l'incendio: rappresenta **l'oggetto che l'incendio ha lasciato**, ed e' la
forma che `mezzi.json` chiama `segno` e che il progetto chiama «il testo al
posto dell'immagine» fin dall'*Africa* del *Furioso*. Per questo la forma della
voce `incendio` non e' il vuoto: e' **`testo`**, con la scansione che lo
dimostra accanto.

**La voce `carestia` e' un buco di una forma diversa, ed e' il difetto vero di
questa chiusura.** Nessuna delle centocinquanta tappe la nomina: la scansione dei
blocchi di persona dei cinque documenti degli anni non trova la parola, e il
file lo scrive come **numero** (`persone_scansionate`,
`tappe_che_nominano_l_evento`), non come convinzione. Una voce cercata che
nessuna tappa usa e' la malattia di M1 ripetuta nella categoria sbagliata: la
tabella contava le voci cercate, e non le voci che il gioco chiede.

**E la scansione ha trovato un difetto che e' la quarta volta della stessa
lezione.** Cercata con `moria` come sottostringa, la parola sta dentro
**memoria**: la stessa scansione mette la moria in **tutti i 120** blocchi
invece dei tre che sono suoi. Il
progetto lo aveva gia' scritto (§5: «una parola che ha due sensi va cercata con
due parole»), e questa volta la parola ambigua era nel **proprio codice** che
conta le tappe. Il file dichiara i due numeri insieme, `con_confini` e
`senza_confini_di_parola`, cosi' la differenza resta visibile invece di essere
corretta e dimenticata.

Le misure sono del **05/10/2026**, fatte con gli strumenti che avevano rete e
non con `fonti_visive_cerca.py`, che dal processo non ne ha: il file lo dice,
come fanno gli altri due.

Uso:
    python3 sorgenti/incidenti_fonti.py
"""
import importlib.util
import io
import json
import os
import re
import sys
import time

RADICE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(RADICE, "dati", "fonti_visive", "incidenti.json")
CERCA = os.path.join(RADICE, "dati", "fonti_visive", "fonti_visive.json")
DOCS = os.path.join(RADICE, "docs")
MEZZI_PY = os.path.join(RADICE, "sorgenti", "mezzi_fonti.py")

# I cinque documenti degli anni: la fonte unica di che cosa una tappa nomina.
ANNI = ["anno1-ferrara", "anno2-penisola", "anno3-europa", "anno4-mondo",
        "anno5-mondo"]

# Le parole con cui una voce nomina il proprio evento. Non e' il nome della voce:
# `moria` e' una voce e l'evento che nomina e' «la peste» o «l'epidemia», e una
# voce che si cerca solo col proprio nome non trova niente. I **confini di
# parola** non sono un dettaglio: senza, «moria» sta dentro «memoria» e la
# scansione trova duecento blocchi invece di tre.
SINONIMI = {
    "incendio": [r"incendi\w*", r"\bbruci\w*"],
    "moria": [r"\bmoria\b", r"\bpeste\b", r"\bepidemi\w*", r"\bmortalit\w*",
              r"\bcolera\b", r"\bvittime\b"],
    "carestia": [r"\bcarest\w*", r"\bfame\b", r"\bfamine\b"],
}

# La forma di ciascuna voce, con la sua ragione e la sua riserva. Le tre forme
# sono le stesse dei mezzi (`mezzi.json`): un'immagine, un segno o un testo al
# posto dell'immagine, e — la quarta, che qui serve — **una voce che il gioco
# non usa**. Il vuoto non e' una forma ammessa: un vuoto senza ragione non e'
# una forma, e' un buco che finge di essere chiuso.
SCELTE = {
    "incendio": (
        "testo",
        "il gioco non rappresenta l'incendio: rappresenta l'oggetto che e' "
        "rimasto dopo. Le tre tappe che lo nominano (4-3, 4-10, 4-13) hanno "
        "per emblema un peso di bronzo, uno scaffale vuoto con un cartellino "
        "scritto a metà e un frammento di stele, e in nessuna delle tre la "
        "fiamma compare; l'incendio ci arriva dentro la domanda, non dentro "
        "l'immagine. E' la forma che il progetto ha gia' deciso per l'Africa "
        "del Furioso: il testo al posto dell'immagine",
        "la scheda della voce resta senza illustrazione, e va detto al "
        "giocatore perche': un'immagine di un incendio d'archivio non esiste, "
        "e quella che esiste su Commons mostra un episodio diverso (i libri "
        "gettati nel fuoco, 14 risultati, nessuno dei quali l'archivio di "
        "Ferrara). Il vuoto e' dichiarato, non ricoperto",
        "la scheda della voce e la domanda della tappa: la scheda porta il "
        "testo della fonte (l'incendio del 1534), la tappa porta il suo "
        "emblema, che e' gia' disegnato dal progetto",
        ),
    "carestia": (
        "non_usata",
        "nessuna delle centocinquanta tappe la nomina. La scansione dei "
        "blocchi di persona dei cinque documenti degli anni non trova la "
        "parola in nessuno, ed e' per questo che la voce e' dichiarata e non "
        "piu' un buco: cercare un'immagine per una tappa che non esiste e' "
        "lavoro che sembra lavoro",
        "una voce cercata e non usata e' la malattia di M1 nella categoria "
        "sbagliata: finche' nessuna tappa la chiede, il numero che conta e' "
        "zero, e il file lo scrive come numero",
        "nessuna: finche' nessuna tappa la nomina, non c'e' dove mostrarla",
        ),
    "moria": (
        "immagine",
        "e' l'unica delle tre che ha sei candidati e tappe che la nominano "
        "(3-22, 4-27 e 5-9), ed e' l'unica che puo' avere un'immagine: le "
        "altre due no, perche' il gioco non le rappresenta",
        "la pagina non dichiara la data e il file porta «senza data»: e' uno "
        "dei tre candidati della stessa serie (H,3.46, H,3.47 e un «After» del "
        "1863), e sceglierne una e' una scelta fra sorelle",
        "la scheda della voce, che la nomina; la scena della tappa e' gia' "
        "l'emblema (l'albero con dieci rami del 3-22, il diagramma a "
        "ragnatela del 4-27, la mappa di strade del 5-9)",
        ),
}

# La scelta fra i sei candidati della moria. Il nome del file e il motivo, e il
# motivo e' la parte difficile: i sei sono tre stampe della stessa serie, una
# processione ottocentesca e una incisione dopo Raffaello.
SCELTO_MORIA = (
    "File:Marcantonio - A plague scene, H,3.46.jpg",
    "la piu' grande delle tre stampe della stessa serie (2500x2005 contro "
    "1600x1254 e 2500x1942) e l'unica che porta una riserva che si puo' "
    "scrivere: e' un'incisione italiana del Cinquecento, che e' l'epoca del "
    "gioco, mentre la processione del Pogliaghi e' del 1890 e quella di "
    "Wellcome e' un'incisione dopo Raffaello con licenza CC BY 4.0, che "
    "obbliga a creare l'attribuzione",
    "la pagina non dichiara la data, e il file porta «senza data», come "
    "sull'aereo: mezzi.json 5 e incidenti.json 1 dicono la stessa cosa",
)

# Le misure del 05/10/2026, con il numero che la fonte ha risposto. Un vuoto
# che non ha un numero accanto e' un buco che aspetta che qualcuno se ne
# accorga: `fonti-visive.md` §5.
MISURE = [
    {"voce": "incendio",
     "interrogazione": "Ferrara 1534 incendio archivio (namespace 6, "
                       "filemime:image/jpeg)",
     "esito": "0 risultati: nessuna immagine libera dell'incendio "
              "dell'archivio ducale",
     "eseguita": "05/10/2026"},
    {"voce": "incendio",
     "interrogazione": "incendio biblioteca antica (namespace 6, "
                       "filemime:image/jpeg)",
     "esito": "0 risultati: nemmeno in italiano, che e' il termine con cui la "
              "voce e' stata cercata il 02/10",
     "eseguita": "05/10/2026"},
    {"voce": "incendio",
     "interrogazione": "burning of books fire engraving (namespace 6, "
                       "filemime:image/jpeg)",
     "esito": "14 risultati, e i due che sono incisioni del Cinquecento "
              "mostrano un episodio leggendario (i libri gettati nel fuoco, il "
              "Romano e il Goto), non un archivio ducale del 1534: nessuno "
              "utilizzabile per l'evento della tappa",
     "eseguita": "05/10/2026"},
    {"voce": "carestia",
     "interrogazione": "carestia 1520 incisione (namespace 6, "
                       "filemime:image/jpeg)",
     "esito": "0 risultati",
     "eseguita": "05/10/2026"},
    {"voce": "carestia",
     "interrogazione": "famine engraving 16th century (namespace 6, "
                       "filemime:image/jpeg)",
     "esito": "3 risultati: Giunone che manda la carestia a Crastore (un "
              "mito del Metropolitan), una pianta di Edimburgo durante "
              "l'assedio del 1573 e un manoscritto di liuto. Nessuna scena di "
              "carestia, che e' quello che il capitolo dichiarava",
     "eseguita": "05/10/2026"},
]

REGOLE = [
    "**Un incidente non si disegna: si mostra l'oggetto che resta.** Le tre "
    "tappe che nominano un incendio hanno per emblema un peso di bronzo, uno "
    "scaffale vuoto e un frammento di stele, e nessuna delle tre ha una "
    "fiamma. Il buco di due mesi fa non era un buco di immagini: era una "
    "domanda che non era stata fatta.",
    "**Il vuoto non e' una forma ammessa.** Le forme sono tre: un'immagine, "
    "il testo al posto dell'immagine, e la voce che il gioco non usa. Un "
    "vuoto senza ragione non e' una forma chiusa: e' un buco travestito da "
    "risposta.",
    "**Una voce che nessuna tappa usa si dichiara, e il conto e' un numero.** "
    "`persone_scansionate` e `tappe_che_nominano_l_evento` sono calcolati, e "
    "`senza_confini_di_parola` dichiara la scansione sbagliata: senza i "
    "confini di parola «moria» sta dentro «memoria» e viene fuori in tutti i "
    "120 blocchi invece dei tre che sono suoi. Il numero e' calcolato, e dove "
    "la scansione sbagliata non trova di piu' il campo vale null: un numero "
    "che non differisce non e' una prova.",
    "**L'immagine di una voce serve alla scheda, non alla scena.** La scheda "
    "e' la riga di carta che nomina l'incidente; la scena della tappa e' "
    "l'emblema, che il progetto disegna. Sono due cose diverse, e confonderle "
    "e' quello che faceva il capitolo: chiedere un'immagine per una scena che "
    "non e' un'immagine.",
    "**Una scelta fra sorelle si dichiara.** Le tre stampe della moria sono la "
    "stessa scena a tre dimensioni diverse: sceglierne una e' una scelta, e il "
    "file dice quale e perche'.",
]

INIZIO_Q = re.compile(r"(?m)^#{2,3} (Q\d+)[^\n]*\n")
QUALSIASI = re.compile(r"(?m)^#{2,3} ")
EMBLEMA = re.compile(r"\*\*Emblema:\*\*\s*(.+?)\s*$", re.M)
RIGA_TAPPA = re.compile(r"(?m)^\| \*\*(\d-\d{1,2})\*\* \|(.*)$")


def leggi(path):
    with io.open(path, encoding="utf-8") as f:
        return f.read()


def cerca():
    with io.open(CERCA, encoding="utf-8") as f:
        return json.load(f)["risultati"]["incidente"]


def mezzi_modulo():
    """L'attribuzione e' calcolata da `mezzi_fonti.py`, una volta sola per tutto
    il progetto: due copie della stessa funzione in due file sono due numeri
    che possono dare due risposte."""
    spec = importlib.util.spec_from_file_location("mezzi_fonti", MEZZI_PY)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def blocchi_persona(testo):
    """{codice Q: testo} dai cinque documenti degli anni.

    Il blocco finisce alla **prima intestazione successiva**, non alla
    successiva intestazione di persona: altrimenti l'ultima persona di ogni
    anno si mangia mezzo documento e la scansione conta paragrafi che non
    sono di nessuno. E' successo, e il conto che ne era uscito era di tre
    persone più di quelle vere.
    """
    out = {}
    for m in INIZIO_Q.finditer(testo):
        n = QUALSIASI.search(testo, m.end())
        out[m.group(1)] = testo[m.end():n.start() if n else len(testo)]
    return out


def tappa_del_persona(testo, codice):
    """Il numero di tappa che la tabella dell'anno assegna a un codice Q.

    Il codice e' in due posti — la riga della tabella delle tappe e
    l'intestazione della scheda — e i due posti devono dire la stessa persona.
    Il numero viene dalla **riga**, non dedotto dalla posizione: dedurlo dal
    numero dell'intestazione sarebbe un numero che guarda se stesso.
    """
    for m in RIGA_TAPPA.finditer(testo):
        if re.search(r"\(%s[^0-9]" % codice, m.group(2)):
            return m.group(1)
    return None


def scansiona(parole, con_confini=True):
    """Le tappe che nominano l'evento, con la frase e l'emblema presi dal
    documento dell'anno.

    Con `con_confini=False` la stessa scansione viene rifatta con le parole
    come sottostringhe: il numero che ne esce e' la prova che il confine serve,
    e va nel file accanto al numero giusto.
    """
    trovare = parole if con_confini else [p.replace(r"\b", "") for p in parole]
    pattern = "|".join(trovare)
    trovate = []
    for anno in ANNI:
        testo = leggi(os.path.join(DOCS, "videogioco-5-duchi-%s.md" % anno))
        for codice, blocco in sorted(blocchi_persona(testo).items()):
            m = re.search(pattern, blocco, re.I)
            if not m:
                continue
            emblema = EMBLEMA.search(blocco)
            trovate.append({
                "tappa": tappa_del_persona(testo, codice),
                "persona": codice,
                "dove": "docs/videogioco-5-duchi-%s.md" % anno,
                "la_parola": m.group(0),
                "la_frase": " ".join(
                    blocco[max(0, m.start() - 40):m.end() + 40].split()),
                "emblema": emblema.group(1).strip() if emblema else None,
            })
    return trovate


def main():
    proposte = {v["voce"]: v["candidati"] for v in cerca()}
    attribuzione = mezzi_modulo().attribuzione
    persone = 0
    for anno in ANNI:
        persone += len(blocchi_persona(
            leggi(os.path.join(DOCS, "videogioco-5-duchi-%s.md" % anno))))

    voci = []
    for nome in sorted(SCELTE):
        forma, perche, riserva, dove = SCELTE[nome]
        if nome not in proposte:
            raise SystemExit("la voce %s non e' nella ricerca" % nome)
        candidati = proposte[nome]
        usata_da = scansiona(SINONIMI[nome])
        senza = scansiona(SINONIMI[nome], con_confini=False)
        riga = {
            "voce": nome,
            "candidati": len(candidati),
            "forma": forma,
            "immagine": None,
            "attribuzione": None,
            "perche_questa_forma": perche,
            "riserva": riserva,
            "dove_andrebbe_mostrata": dove,
            "usata_da": usata_da,
            "perche_non_usata": None,
            "scansione": {
                "persone_scansionate": persone,
                "tappe_che_nominano_l_evento": len(usata_da),
                # None quando la scansione sbagliata trova meno della giusta:
                # un numero che non differisce non e' una prova, e dichiararlo
                # sarebbe un numero che non dice niente
                "senza_confini_di_parola": (len(senza) if len(senza) > len(usata_da)
                                            else None),
            },
            "misure": [m["interrogazione"] for m in MISURE
                       if m["voce"] == nome],
        }
        if forma == "non_usata":
            if usata_da or senza:
                raise SystemExit("%s e' dichiarata non usata ma le due "
                                 "scansioni trovano %d e %d tappe"
                                 % (nome, len(usata_da), len(senza)))
            riga["perche_non_usata"] = (
                "nessuna tappa la nomina: %d persone scandite nei cinque "
                "documenti degli anni, e la parola non compare neppure dentro "
                "un'altra parola (0 tappe con i confini, 0 senza)" % (persone,))
        else:
            if not usata_da:
                raise SystemExit("%s non e' non_usata ma nessuna tappa la "
                                 "nomina" % nome)
            for u in usata_da:
                if not u["tappa"] or not u["emblema"]:
                    raise SystemExit("%s: la persona %s non ha una riga nella "
                                     "tabella delle tappe o non ha emblema"
                                     % (nome, u["persona"]))
        if forma == "immagine":
            scelto, perche_scelta, riserva_scelta = SCELTO_MORIA
            trovato = next((c for c in candidati if c["file"] == scelto), None)
            if trovato is None:
                raise SystemExit("il file scelto per %s non e' fra i candidati "
                                 "della ricerca: %s" % (nome, scelto))
            riga["immagine"] = {
                "file": trovato["file"],
                "url": trovato["url"],
                "licenza": trovato["licenza"],
                "autore": trovato.get("autore"),
                "data": trovato.get("data"),
                "px": [trovato["larghezza"], trovato["altezza"]],
                "termine": trovato.get("termino"),
            }
            riga["attribuzione"] = attribuzione(trovato)
            riga["perche_questa_immagine"] = perche_scelta
            riga["riserva_immagine"] = riserva_scelta
            riga["scelta_da"] = ("ricerca del 02/10/2026, scelta sui metadati; "
                                 "licenza riletta sulla pagina del file il "
                                 "05/10/2026")
        voci.append(riga)

    def conta(predicato, su="forma"):
        return len([v for v in voci if v[su] == predicato])

    file = {
        "versione": 1,
        "data": time.strftime("%Y-%m-%d"),
        "che_cosa": "i tre incidenti del gioco: l'immagine che si puo' avere, "
                    "il testo che la sostituisce quando l'immagine non serve, "
                    "e la voce che il gioco non usa",
        "regole": REGOLE,
        "misure": MISURE,
        "conti": {
            "voci": len(voci),
            "candidati": sum(v["candidati"] for v in voci),
            "con_immagine": len([v for v in voci if v["immagine"]]),
            "col_testo_al_posto": conta("testo"),
            "non_usate": conta("non_usata"),
            "persone_scansionate": persone,
            "tappe_che_nominano_un_incidente": sum(
                len(v["usata_da"]) for v in voci),
            "senza_confini_di_parola": sum(
                v["scansione"]["senza_confini_di_parola"] or 0 for v in voci),
        },
        "voci": voci,
    }
    with io.open(OUT, "w", encoding="utf-8") as f:
        json.dump(file, f, ensure_ascii=False, indent=1, sort_keys=False)
        f.write("\n")
    print("scritto %s" % os.path.relpath(OUT, RADICE))
    c = file["conti"]
    print("  voci %d, candidati %d, con immagine %d, col testo al posto %d, "
          "non usate %d" % (c["voci"], c["candidati"], c["con_immagine"],
                            c["col_testo_al_posto"], c["non_usate"]))
    print("  %d persone scandite, %d tappe che nominano un incidente, e la "
          "scansione senza confini ne troverebbe %d"
          % (c["persone_scansionate"], c["tappe_che_nominano_un_incidente"],
             sum(v["scansione"]["senza_confini_di_parola"] or 0 for v in voci)))
    for v in voci:
        print("  %-9s %-10s %s" % (
            v["voce"], v["forma"],
            ", ".join(u["tappa"] or "?" for u in v["usata_da"]) or "nessuna"))


if __name__ == "__main__":
    sys.exit(main())