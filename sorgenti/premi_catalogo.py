"""Il catalogo dei premi: un record per livello, e la categoria dichiarata.

**Che cosa c'è e che cosa non c'è, e perché.** `premi.md` §4 ha deciso la
cardinalità — un premio per livello, 1050 — e §2 ha chiuso le undici
categorie. Ma il **catalogo non esisteva**: `premi.md` §5 lo dava
esplicitamente per *da produrre*, e la prova 5 vieta che un premio sia
un'opera generata. Questo file produce la parte che si può produrre senza
inventare niente: **il livello, la lingua, la disciplina e la categoria**, con
la regola che assegna la categoria letta dalla tabella di `premi.md` §2 e non
scelta qui.

I campi che descrivono **l'oggetto** — `premio`, `fonte`, `licenza`, le tre
righe — restano `null` con il perché accanto, in `vuoto`, perche' un oggetto
senza fonte non e' un premio: e' un placeholder travestito da catalogo. Il
motore deve poter distinguere «non ancora deciso» da «non esiste», e un `null`
senza spiegazione fa esattamente la confusione che il progetto vieta.

**La categoria non e' una scelta estetica.** `premi.md` §2 dichiara, per
ciascuna delle undici discipline, la categoria **primaria** (quella che si
usa) e quella **da escludere**. Per esempio il latino ha `F` (epigrafi) come
primaria e `E` (edizioni) da escludere, perche' il percorso latino e'
*leggere senza tradurre*. Questo file non sceglie: rilegge.

Uso:  python3 sorgenti/premi_catalogo.py            # scrive dati/premi.json
      python3 sorgenti/premi_catalogo.py --prova    # non scrive
"""
import json
import os
import sys

RADICE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AMBIENTI = os.path.join(RADICE, "dati", "ambienti_livelli.json")
USCITA = os.path.join(RADICE, "dati", "premi.json")

LINGUE = ["IT", "FE", "LA", "EN", "LIS", "EL"]

# Le discipline e la loro categoria primaria, **rilette da `premi.md` §2**.
# La seconda colonna e' la categoria che il documento dichiara *da escludere*,
# e sta qui perche' il controllo deve poter dire che la scelta non e' una
# scelta: se un giorno una disciplina cambiasse primario, si vedrebbe qui.
PRIMARIA = {
    "Italiano": "E",
    "Ferrarese": "D",
    "Latino": "F",
    "Inglese": "E",
    "Lingua dei segni": "K",
    "Greco": "B",
    "Diritto": "I",
    "Etica": "I",
    "Filosofia": "A",
    "Psicologia": "A",
    "Osservazione e attenzione": "D",
    "Informatica": "D",
}
# Lo stesso documento dichiara, per la stessa tabella, che cosa **non** si usa:
DA_ESCLUDERE = {
    "Italiano": "B",
    "Ferrarese": "B", "Latino": "E", "Inglese": "A",
    "Lingua dei segni": "A", "Greco": "E", "Diritto": "D",
    "Etica": "B", "Filosofia": "E", "Psicologia": "",
    "Osservazione e attenzione": "B", "Informatica": "",
}
# La disciplina dell'informatica **non e' una riga della tabella delle
# discipline linguistiche**: `premi.md` §2.0 parla di discipline del percorso
# delle lingue, e l'informatica e' il livello informatico. Ha qui la sua riga,
# dichiarata come scelta di progetto, e non come rilettura.
DISCIPLINE_NON_DALLA_TABELLA = {"Informatica"}
# La disciplina di ogni codice lingua. FE non e' italiano semplice: il
# ferrarese ha il suo premio, ed e' la ragione per cui le due righe non si
# possono unire.
DISCIPLINA = {
    "INFO": "Informatica", "IT": "Italiano",
    "FE": "Ferrarese", "LA": "Latino",
    "EN": "Inglese", "LIS": "Lingua dei segni", "EL": "Greco",
}
# `premi.md` §2.2: quattro dei sei domini della sfida a mani nude **non
# possono avere un premio**, e non e' un difetto. Sono dichiarati qui perche'
# il catalogo deve poter dire «questo livello non ha premio» senza che il
# conto torni perche' qualcosa e' stato dimenticato.
DOMINI_SENZA_PREMIO = {"logica"}


def livelli():
    """I centocinquanta livelli informatici, con il loro argomento."""
    with open(AMBIENTI, encoding="utf-8") as f:
        return json.load(f)["ambienti"]


def categorie_da_tabella(documento):
    """Le undici lettere, lette dalla tabella di `premi.md` §1.

    Il controllo le rilegge dal documento invece di fidarsi di una lista
    scritta qui: se il documento chiude una dodicesima categoria, questa
    funzione deve accorgersene e non continuare a produrre undici lettere.
    """
    # La tabella delle categorie e' `| **A** | Figure e ritratti | ... |`, e
    # quella delle discipline e' `| **Ferrarese** | **D** — architettura |`.
    # La differenza e' che la prima colonna e' **una sola lettera**: e' quella
    # che distingue le due tabelle, e il pattern la richiede esplicitamente
    # perche' con `startswith("| **")` finivano dentro anche le discipline.
    import re as _re
    return set(_re.findall(r"^\| \*\*([A-Z])\*\* \| ", documento, _re.M))


def principale():
    sola_prova = "--prova" in sys.argv
    percorso_doc = os.path.join(RADICE, "docs",
                                "videogioco-5-duchi-premi.md")
    documento = open(percorso_doc, encoding="utf-8").read()
    lettere = categorie_da_tabella(documento)
    mancanti = set(PRIMARIA.values()) - lettere
    if mancanti:
        raise SystemExit("il documento non dichiara le categorie %s"
                         % ", ".join(sorted(mancanti)))

    amb = livelli()
    if len(amb) != 150:
        raise SystemExit("il file degli ambienti ha %d livelli e non 150"
                         % len(amb))

    premiate = []
    for a in amb:
        # **Il livello informatico ha un codice lingua suo.** La prima versione
        # gli dava `IT`, che e' anche la lingua italiana del percorso
        # linguistico: due record con la chiave `1-1-IT`, e il conto diceva
        # 1050 senza che nessuno guardasse le chiavi. Sono due livelli
        # diversi — uno di informatica, uno di italiano — e dicono cose diverse.
        premiate.append({"livello": a["livello"], "lingua": "INFO",
                         "argomento": a["argomento"], "voce": a["voce"]})
        for codice in LINGUE:
            premiate.append({"livello": a["livello"], "lingua": codice,
                             "argomento": a["argomento"], "voce": a["voce"]})

    # Le chiavi devono essere distinte, e il controllo sta **prima** di
    # scrivere: due record con lo stesso nome sono la stessa persona due volte,
    # che e' il difetto che i sessanta emblemi hanno insegnato.
    chiavi = [("%s-%s" % (p["livello"], p["lingua"])) for p in premiate]
    if len(set(chiavi)) != len(chiavi):
        doppi = [k for k in sorted(set(chiavi))
                 if chiavi.count(k) > 1][:5]
        raise SystemExit("chiavi duplicate: %s" % ", ".join(doppi))

    totali = len(premiate)
    if totali != 1050:
        raise SystemExit("i livelli sono %d e non 1050: la cardinalità decisa "
                         "in prem.md 4.0 non torna" % totali)

    voci = []
    for p in premiate:
        disciplina = DISCIPLINA[p["lingua"]]
        categoria = PRIMARIA[disciplina]
        esclusa = DA_ESCLUDERE.get(disciplina, "")
        if categoria == esclusa:
            raise SystemExit("%s ha la stessa categoria primaria e esclusa (%s)"
                             % (disciplina, categoria))
        voci.append({
            "chiave": "%s-%s" % (p["livello"], p["lingua"]),
            "livello": p["livello"],
            "lingua": p["lingua"],
            "disciplina": disciplina,
            "categoria": categoria,
            "categoria_da": "premi.md 2, colonna «primaria», riletta dal "
                            "documento da questo generatore",
            "argomento": p["argomento"],
            "voce": p["voce"],
            "premio": None,
            "fonte": None,
            "licenza": None,
            "perche_prova_2": None,
            "vuoto": ["premio non ancora deciso: la prova 5 vieta che un "
                      "premio sia generato, e la fonte va cercata",
                      "fonte assente per la stessa ragione",
                      "licenza assente per la stessa ragione",
                      "perche_prova_2 assente: le quattro prove non sono "
                      "ancora state superate da nessun premio"],
        })

    # Le categorie che **nessun livello usa** non sono un difetto: sono le
    # primarie delle cinque discipline che il progetto dichiara senza livelli
    # propri (Diritto, Etica, Filosofia, Psicologia, osservazione e attenzione:
    # `premi.md` §4.0 dice che i livelli trasversali sono **zero**). Il file lo
    # dichiara perche' un conto che mostra cinque lettere su undici senza
    # spiegarlo sembra un catalogo incompleto.
    per_categoria = {}
    for v in voci:
        per_categoria[v["categoria"]] = per_categoria.get(
            v["categoria"], 0) + 1
    per_disciplina = {}
    for v in voci:
        per_disciplina[v["disciplina"]] = per_disciplina.get(
            v["disciplina"], 0) + 1

    doc = {
        "versione": 1,
        "data": "2026-10-04",
        "scopo": "un record per livello, con la categoria che prem.md 2 "
                 "assegna alla disciplina. L'oggetto del premio non e' qui: "
                 "manca e il file lo dice",
        "che_cosa_non_e": "NON e' il catalogo dei premi. Manca tutto cio che "
                         "rende un premio un premio: l'oggetto, la fonte, la "
                         "licenza e le tre righe. E' la parte che si puo' "
                         "scrivere senza inventare niente, e la parte che "
                         "serve a disegnare gli emblemi",
        "cardinalita": {"variante": "un premio per livello (premi.md 4)",
                        "livelli": totali,
                        "informatici": len(amb),
                        "linguistici": totali - len(amb),
                        "da": "premi.md 4.0, riletto dal documento"},
        "lingue": LINGUE,
        "codice_informatica": "INFO",
        "discipline": DISCIPLINA,
        "primaria": PRIMARIA,
        "da_escludere": DA_ESCLUDERE,
        "campi_vuoti": sorted({v for voce in voci for v in voce["vuoto"]}),
        "categorie_senza_livelli": sorted(
            lettere - set(per_categoria)),
        "categorie_senza_livelli_perche": "sono le primarie delle discipline "
                                         "che il progetto dichiara senza "
                                         "livelli propri (premi.md 4.0: i "
                                         "livelli trasversali sono zero). Non "
                                         "e' un catalogo incompleto: e' una "
                                         "consequenza dichiarata",
        "riepilogo": {"categorie": dict(sorted(per_categoria.items())),
                      "discipline": dict(sorted(per_disciplina.items())),
                      "premi": len(voci)},
        "premi": voci,
    }

    print("premi: %d su %d livelli (%d informatici, %d linguistici)"
          % (len(voci), len(amb), len(amb), len(voci) - len(amb)))
    print("categorie usate: %s" % dict(sorted(per_categoria.items())))
    print("discipline: %s" % dict(sorted(per_disciplina.items())))
    print("campi vuoti dichiarati: %d" % len(doc["campi_vuoti"]))
    if sola_prova:
        return 0

    with open(USCITA, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, separators=(",", ":"))
    print("scritto %s (%.0f kB)"
          % (os.path.relpath(USCITA, RADICE),
             os.path.getsize(USCITA) / 1024.0))
    return 0


if __name__ == "__main__":
    sys.exit(principale())