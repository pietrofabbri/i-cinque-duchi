#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Costruisce `dati/fonti_visive/mezzi.json`: la veste grafica dei mezzi di
trasporto, uno per mezzo del gioco.

**Il buco era più grande di quanto il documento dicesse.** La ricerca del
02/10/2026 aveva coperto **undici** mezzi; il gioco ne usa **ventuno**, e
nessuno dei due numeri era confrontato con l'altro. Dieci mezzi storici non
hanno mai avuto una ricerca, e i cinque mezzi fantastici del *Furioso*
—ippogrifo, drago, sirena, carro di delfini, carro di serpenti— non hanno
immagine **e non la devono avere**: sono creature, e la regola dei luoghi
fantastici è già scritta in `AGENTS.md`, «vanno disegnati a mano sulla carta
del gioco, con un segno dedicato».

**Le scelte sono fatte sui metadati, non a vista.** L'agente non può vedere
un'immagine, e il progetto vieta che una scelta sia inventata: qui ogni scelta
porta il motivo per cui il candidato è adatto a *quello che il gioco descrive*
in `percorsi_mezzi.py`, e il file dice che la scelta è sui metadati. La
verifica a vista resta a Pietro, ed è la stessa regola dei 180 oggetti
linguistici.

I vuoti non sono un fallimento nascosto: sono messi, uno per mezzo, con la
ragione. Dieci storici su sedici e nessun magico su cinque.

Uso:
    python3 sorgenti/mezzi_fonti.py            # scrive il file e riassume
"""
import importlib.util
import io
import json
import os
import re
import sys
import time

RADICE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(RADICE, "dati", "fonti_visive", "mezzi.json")
CERCA = os.path.join(RADICE, "dati", "fonti_visive", "fonti_visive.json")
MEZZI_PY = os.path.join(RADICE, "sorgenti", "percorsi_mezzi.py")

# La scelta per ogni mezzo: il **nome del file** fra i candidati, il motivo, e
# la riserva quando c'e'. La motivazione e' un testo e va scritta a mano: il
# numero accanto e' un numero e va calcolato dal candidato.
SCELTE = {
    "mulo": (
        "File:Peter Birmann - The Devil's Bridge in the Schöllenen Gorge on "
        "the Way across the St. Gotthard Pass with a Mule Train, before 1805 "
        "- Google Art Project.jpg",
        "una mulattiera del San Gottardo: la strada delle mule che e' il modo "
        "di trasporto dell'Europa preferita dai merciai, ed e' italiana",
        "1805 e non Quattrocento; il gioco descrive «la bestia da soma delle "
        "vie postali» e questa e' l'immagine che lo dice senza mentire"),
    "galera": (
        "File:Galea veneziana del Provveditore d'Armata imbandierata.jpg",
        "l'unica immagine di galera veneziana fra i candidati, e la Venezia e' "
        "il porto del gioco",
        "autore ignoto nel file e 735x516 px: e' la piu' piccola del lotto, e "
        "l'attribuzione porta «autore non dichiarato»"),
    "nave": (
        "File:Portuguese Carracks off a Rocky Coast.jpg",
        "la rotta costiera dei velieri portoghesi, che e' il viaggio del gioco",
        "circa 1540, e il gioco descrive un veliero latino: la somiglianza e' "
        "dichiarata, non nascosta"),
    "carovana": (
        "File:Photo A camel caravan transports salt in the Mauritanian Adrar "
        "region 1965 - Touring Club Italiano BBC 40.jpg",
        "carovana del sale con le guide, che e' la carovana delle strade delle "
        "carovane",
        "**una fotografia del 1965**, non un dipinto: il gioco non promette "
        "immagini d'epoca per la carovana e questo va detto"),
    "diligenza": (
        "File:Vincent van Gogh - Tarascon Stagecoach - L.1988.62.11 - "
        "Princeton University Art Museum.jpg",
        "una diligenza di strada intera, non un dettaglio: 1888, e la diligenza "
        "del gioco e' delle poste",
        "l'attribuzione porta «Vincent van Gogh,1888»; fra i candidati c'era "
        "anche una stampa di Abel Hold, che si e' scelto di non usare"),
    "treno": (
        "File:Ferrovia Marmifera Carrara -1890.jpg",
        "una ferrovia italiana del 1890, che e' la prima ferrovia del gioco",
        "641x393 px e una foto di giornale: misura piccola dichiarata, "
        "l'immagine puo' stare solo come icona"),
}

# I vuoti, e **la ragione** di ciascuno: un vuoto senza ragione è un buco che
# si dimentica, e il progetto vieta il default che sostituisce un dato mancante.
VUOTI = {
    "a piedi": ("i due candidati non mostrano «un uomo solo, con la bisaccia»: "
                "uno e' un sentiero di pellegrini di oggi, l'altro e' un "
                "conchiglio",
                "cercata"),
    "cavallo": ("**tre dei quattro candidati sono la Cappella dei Magi**, che e' "
                "un corteo di trecento persone, e il quarto e' una batteria "
                "d'artiglieria: nessuno dei quattro e' un cavallo",
                "cercata"),
    "aereo": ("**i due candidati sono il volo turistico sugli aerei da "
              "giardinaggio** del §5: nessuno dei due e' un aereo di linea",
              "cercata"),
    "carrozza": ("la carrozza americana del 1922 e le tre immagini di guida "
                 "turistica del Novecento: nessuna carrozza di corte",
                 "cercata"),
    "pipa": ("l'unico candidato e' **il rospo del genere *Pipa*** del §5, cioe' "
             "l'animale e non la pianta",
             "cercata"),
    "crociera": ("nessuna ricerca: la ricerca del 02/10 ha coperto undici "
                 "mezzi su ventuno e questa voce non e' fra quelle",
                 "non cercata"),
    "moto": ("nessuna ricerca, come la crociera", "non cercata"),
    "sci": ("nessuna ricerca, come la crociera", "non cercata"),
    "elicottero": ("nessuna ricerca, come la crociera", "non cercata"),
    "monopattino": ("nessuna ricerca, come la crociera", "non cercata"),
}

REGOLE = [
    "**Il mezzo e' quello che `percorsi_mezzi.py` descrive**, non quello che il "
    "termine di ricerca richiama: il gioco scrive «un uomo solo, con la "
    "bisaccia» e un sentiero di pellegrini non lo soddisfa.",
    "**Il nome del file non e' una prova e il corteo non e' il cavallo**: la "
    "Cappella dei Magi resta la fonte piu' bella e sbagliata del 02/10, e "
    "questa sezione la dichiara perche' qualcuno la ritroverà.",
    "**Un mezzo fantastico non ha immagine e non la vuole**: si disegna con il "
    "segno dedicato sulla carta del gioco, come i luoghi fantastici di "
    "`AGENTS.md`. Nessun mezzo di gioco ha un'immagine in questo file, ed e' "
    "un controllo.",
    "**La scelta e' sui metadati, non a vista**, e resta una proposta: il "
    "file lo dichiara e `verifica_fonti_visive.py` lo verifica.",
    "**Il vuoto si dichiara con la sua ragione**, mai si sostituisce con "
    "quello che c'e'.",
]


def mezzi_del_gioco():
    spec = importlib.util.spec_from_file_location("percorsi_mezzi", MEZZI_PY)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m.MEZZI


def cerca():
    with io.open(CERCA, encoding="utf-8") as f:
        return json.load(f)["risultati"]["mezzo"]


def attribuzione(c):
    """La riga di attribuzione, calcolata dai metadati della fonte.

    Il progetto non ne scrive una a mano per ogni immagine: le calcola, perche'
    un'attribuzione scritta a mano sbaglia e sbaglia in silenzio. E la calcola
    **pulita**, perche' la fonte porta pezzi che non sono un nome e non sono
    un anno: «before 1805», «1965 date 15», e ilclassico «Unkown» con la K
    in piu' che si trova anche in Commons. Un nome che non c'e' si dichiara
    «autore non dichiarato», che e' informazione; «Unkown» e' spazzatura che
    passa per un nome.
    """
    autore = (c.get("autore") or "").strip()
    if not autore or autore.lower().startswith(("unknown author", "unkown")):
        autore = "autore non dichiarato"
    else:
        autore = autore.split("(")[0].strip()
        if len(autore) > 40:
            autore = autore[:37] + "..."
    anno = re.search(r"\b(\d{4})\b", str(c.get("data") or ""))
    data = anno.group(1) if anno else "senza data"
    return "%s, %s, %s" % (c["file"].replace("File:", ""), autore, data)


def costruisci():
    mezzi = mezzi_del_gioco()
    proposte = {v["voce"]: v["candidati"] for v in cerca()}
    voci = []
    for nome, (km, persone, nota, tipo, dal) in mezzi.items():
        riga = {
            "mezzo": nome,
            "tipo": tipo,
            "dal": dal,
            "km_giorno": km,
            "persone": persone,
            "descrizione": nota,
            "immagine": None,
            "vuoto": None,
            "segno": None,
            "scelta_da": None,
            "perche": None,
            "riserva": None,
            "attribuzione": None,
        }
        if tipo == "gioco":
            riga["segno"] = ("segno dedicato sulla carta del gioco; nessuna "
                             "immagine, e non ne serve una")
            riga["scelta_da"] = "non cercata: il mezzo non esiste"
        elif nome in SCELTE:
            scelto, perche, riserva = SCELTE[nome]
            candidati = proposte.get(nome, [])
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
            riga["scelta_da"] = "ricerca del 02/10/2026, scelta sui metadati"
            riga["perche"] = perche
            riga["riserva"] = riserva
        else:
            motivo, stato = VUOTI[nome]
            riga["vuoto"] = motivo
            riga["scelta_da"] = ("ricerca del 02/10/2026" if stato == "cercata"
                                 else "nessuna ricerca")
        voci.append(riga)
    return voci


def main():
    voci = costruisci()
    con_immagine = [v for v in voci if v["immagine"]]
    con_vuoto = [v for v in voci if v["vuoto"]]
    con_segno = [v for v in voci if v["segno"]]
    storici = [v for v in voci if v["tipo"] == "storico"]
    file = {
        "versione": 1,
        "data": time.strftime("%Y-%m-%d"),
        "che_cosa": "la veste grafica dei mezzi di trasporto, uno per mezzo "
                    "del gioco: immagine proposta, vuoto dichiarato o segno "
                    "fantastico",
        "regole": REGOLE,
        "fonte_da_cui": "i candidati della ricerca del 02/10/2026 in "
                        "dati/fonti_visive/fonti_visive.json; nessuna "
                        "ricerca nuova, perche' la sessione non ha rete",
        "scelta": "sui metadati, non a vista; l'attestazione e' di Pietro",
        "conti": {
            "mezzi": len(voci),
            "storici": len(storici),
            "con_immagine": len(con_immagine),
            "storici_senza_immagine": len([v for v in storici if not v["immagine"]]),
            "storici_senza_ricerca": len([v for v in storici
                                          if v["scelta_da"] == "nessuna ricerca"]),
            "fantastici_con_segno": len(con_segno),
            "candidati_esaminati": sum(len(c) for c in
                                      (v["candidati"] for v in cerca())),
        },
        "mezzi": voci,
    }
    with io.open(OUT, "w", encoding="utf-8") as f:
        json.dump(file, f, ensure_ascii=False, indent=1, sort_keys=False)
        f.write("\n")
    print("scritto %s" % os.path.relpath(OUT, RADICE))
    print("  mezzi %d: con immagine %d, storici senza immagine %d, "
          "fantastici con segno %d"
          % (len(voci), len(con_immagine),
             len([v for v in storici if not v["immagine"]]), len(con_segno)))
    for v in voci:
        stato = ("immagine %s" % v["immagine"]["file"][5:40]) if v["immagine"] else (
            "segno" if v["segno"] else "VUOTO")
        print("  %-20s %s" % (v["mezzo"], stato))


if __name__ == "__main__":
    sys.exit(main())