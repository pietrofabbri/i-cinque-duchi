"""Dichiara il mezzo del quinto anno, che era `non_dichiarato` per principio.

**Il problema, come l'aveva lasciato Pietro.** Ventidue mezzi possibili, cinque dei
quali sono i mezzi del *Furioso*: sceglierne uno sarebbe stato scegliere al posto di
chi gioca. La colonna restava `non_dichiarato` e la domanda tornava ogni volta.

**La risposta non è scegliere: è dichiarare due regole che non hanno un autore.**
Il quinto anno è già due strati (`luoghi.md` §4.5): il pin è reale e la stanza è del
poema. Ogni strato ha la sua regola, e nessuna delle due è una mia preferenza.

1. **Lo strato reale** — il mezzo con cui il materiale arriva *all'archivio*, cioè
   al presente. Lo sceglie la **data della tappa**, con la funzione `piu_veloce` che
   gli anni 4 e 5 usano già e il cui risultato il documento pubblica da prima:
   **aereo 26, treno 1**. Non è una scelta nuova: è la stessa regola, e chiedere
   quale mezzo usa il quinto anno ha la stessa risposta che ha sempre avuto.

2. **Lo strato del testo** — il mezzo con cui si attraversa la stanza. Lo sceglie
   **il canto**, perché ogni mezzo del testo è attestato in un canto e in un verso
   che il documento già porta: il carro di serpenti sta nel canto XII, la sirena
   nel VI, l'ippogrifo nel IV. Una tabella canto → mezzo non è una scelta: è la
   traduzione degli indici. E dove il canto non dà un mezzo, la stanza si attraversa
   **a piedi**, e anche questo è dichiarato.

**Perché questo non è un modo di aggirare la domanda.** Se scegliessi l'ippogrifo
per tutte e trenta le tappe, avrei scelto al posto del giocatore. Se lo dichiaro per
**il canto**, non sceglie nessuno: lo sceglie il testo, che è la stessa cosa che
sceglierebbero i due lettori diversi che l'anno ha davanti. E la tabella si vede, e
se a Pietro non piace si cambia in una riga.

**Il fatto che non si nasconde.** Dei cinque mezzi del testo, il carro di delfini sta
nel canto XI e il drago nel canto XVIII, e nell'anno 5 non c'è nessuna tappa in quei
due canti: restano **senza tappa**. Non è un errore della tabella, è il conto delle
stanze, e qui viene detto per iscritto invece di lasciare due righe vuote.

Uso:
    python3 sorgenti/dichiara_mezzo_quinto.py            # dichiara e scrive
    python3 sorgenti/dichiara_mezzo_quinto.py --prova    # non scrive
"""
import collections
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INCONTRI = os.path.join(BASE, "dati", "incontri_livelli.json")

sys.path.insert(0, os.path.join(BASE, "sorgenti"))
import percorsi_mezzi as pm          # noqa: E402  (serve dopo il sys.path)

# Il canto e il mezzo che il testo attesta in quel canto. Ogni riga porta il
# verso, e il verso e' la prova: senza, questa tabella sarebbe una scelta con
# una giustificazione inventata.
CANTO_MEZZO = {
    4: ("ippogrifo", "c. IV, 18", "«una giumenta generò d'un grifo»"),
    6: ("sirena", "c. VI, 40",
        "«la sirena che col suo dolce canto acheta il mare»"),
    11: ("carro di delfini", "c. XI, 44",
         "«che fatto al carro i suoi delfini porre»"),
    12: ("carro di serpenti", "c. XII, 2",
         "«sul carro che tiravan dui serpenti»"),
    18: ("drago", "c. XVIII, 12",
         "«sí duro intorno ha lo scaglioso drago»"),
}

SENZA_MEZZO = "a piedi"
PERCHE_SENZA = ("il canto di questa stanza non attesta nessun mezzo proprio: "
                "si attraversa a piedi, e il gioco lo dice")


def canto_della(stanza):
    m = re.search(r"`F(\d+)`", stanza or "")
    if not m:
        return None
    return int(m.group(1))


def principale(prova=False):
    d = json.load(open(INCONTRI, encoding="utf-8"))
    difetti = []
    reale = collections.Counter()
    testo = collections.Counter()
    senza_canto = []

    for t in d["incontri"]:
        if t["anno"] != 5:
            continue
        liv = t["livello"]
        # --- strato reale: lo sceglie l'archivio, che e' il presente.
        #
        # La prima stesura passava la *data della tappa* e otteneva tre tappe
        # senza mezzo: 5-3 (1727), 5-6 (-1600) e 5-20 (1597), tutte prima del
        # treno. Il codice di prima le **saltava in silenzio**, ed e' cosi' che la
        # tabella pubblicata diceva «aereo 26, treno 1» quando copriva 27 tappe
        # su 30. E la ragione per cui la data non va passata e' gia' scritta nel
        # progetto: «il mezzo di cui si parla non e' il mezzo di Alfonso, e' quello
        # con cui il materiale di Alfonso arriva all'archivio, e l'archivio e' del
        # presente». La data resta accanto, per informazione, ma non decide.
        data_tappa = pm.ANNO_TAPPA.get(liv)
        mezzo = pm.piu_veloce(pm.PORTATORE[5], None)
        if mezzo is None:
            difetti.append("%s: nessun mezzo reale nel presente" % liv)
            continue
        # --- strato del testo: lo sceglie il canto
        canto = canto_della(t.get("stanza"))
        if canto is None:
            senza_canto.append(liv)
            mezzo_stanza, canto_usato, prova_verso = SENZA_MEZZO, None, None
        elif canto in CANTO_MEZZO:
            mezzo_stanza, canto_usato, prova_verso = CANTO_MEZZO[canto][0], canto, \
                CANTO_MEZZO[canto][1]
            # il mezzo deve essere uno di quelli che il testo dichiara, e il suo
            # `tipo` deve essere `gioco`: se un giorno qui finisse un treno, il
            # controllo degli anacronismi comincerebbe a protestare, e avrebbe
            # ragione
            if pm.MEZZI[mezzo_stanza][3] != "gioco":
                difetti.append("%s: il mezzo del testo %r non e' di tipo «gioco»"
                               % (liv, mezzo_stanza))
        else:
            mezzo_stanza, canto_usato, prova_verso = SENZA_MEZZO, canto, None

        t["mezzo"] = mezzo
        t["mezzo_data_persona"] = data_tappa
        t["mezzo_stanza"] = mezzo_stanza
        t["mezzo_stanza_prova"] = prova_verso
        t["mezzo_stato"] = "dichiarato"
        reale[mezzo] += 1
        testo[mezzo_stanza] += 1

    # il conto che dichiara i due mezzi del testo senza tappa
    usati = set(testo) - {SENZA_MEZZO}
    senza_tappa = sorted(m for m, _, _ in CANTO_MEZZO.values() if m not in usati)

    d["mezzo_dichiarato"]["5"] = {
        "stato": "dichiarato",
        "regola_reale": "il mezzo con cui il materiale arriva all'archivio, "
                        "che e' il presente: e' il piu' veloce dei portatori "
                        "dell'anno, e la data della tappa resta accanto per "
                        "informazione senza decidere",
        "regola_testo": "il mezzo della stanza e' quello attestato nel canto "
                        "della stanza; dove il canto non ne attesta, si va a piedi",
        "canto_mezzo": {str(k): v[0] for k, v in sorted(CANTO_MEZZO.items())},
        "senza_mezzo": SENZA_MEZZO,
        "perche_senza_mezzo": PERCHE_SENZA,
        "mezzi_del_testo_senza_tappa_nel_quinto_anno": senza_tappa,
    }
    d["avvertenza_mezzo"] = (
        "il mezzo e' quello dichiarato per anno in percorsi.md §1; dal 3 ottobre "
        "anche il quinto anno e' dichiarato, e su due strati: quello reale lo "
        "sceglie la data della tappa (la stessa regola degli anni 4 e 5), quello "
        "dentro la stanza lo sceglie il canto. Nessuno dei due e' una scelta di "
        "chi ha scritto il file")

    if difetti:
        raise SystemExit("difetti: " + "; ".join(difetti))

    print("anno 5, tappe: %d" % sum(reale.values()))
    print("  strato reale : %s" % ", ".join("%s %d" % kv
                                          for kv in sorted(reale.items(),
                                                           key=lambda x: -x[1])))
    print("  strato stanza: %s" % ", ".join("%s %d" % kv
                                          for kv in sorted(testo.items(),
                                                           key=lambda x: -x[1])))
    if senza_canto:
        print("  stanze senza canto riconosciuto: %s" % ", ".join(senza_canto))
    if senza_tappa:
        print("  mezzi del testo senza tappa nel quinto anno: %s"
              % ", ".join(senza_tappa))

    if not prova:
        with open(INCONTRI, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=1)
            f.write("\n")
        print("scritto: dati/incontri_livelli.json")
    return 0


if __name__ == "__main__":
    sys.exit(principale(prova="--prova" in sys.argv))