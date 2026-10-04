"""Secondo giro di ricerca su Commons per il latino, il greco e il ferrarese.

**Perché un secondo giro.** Il primo ha cercato termini latini transliterati e
ha restituito **coincidenze di lettere**: alla voce «la maledizione» il file
migliore era un ritratto, alla voce «il tabù» una foto delle isole Polinesie.
Il controllo G7 lo dice: **27 voci latine su 28** e **17 greche su 28** hanno
solo proposte scoperte per caso.

**Il principio del secondo giro: si cerca la cosa che si vede, non la parola.**
Una voce non è una parola da tradurre: è **la cosa che il ragazzo guarda**. Per
«gli auspici» la risposta non è un file che si chiama *auspicia* ma **il
lituo dell'augure**, lo strumento che l'augure tiene in mano: è l'oggetto che
fa quella cosa. Dove la cosa non esiste — i proverbi latini non hanno immagine,
il caffè e il tè non sono greci antichi — la risposta giusta non è un file ma
la **dichiarazione che l'immagine non esiste**, che `lingue-immagini.md` §1
chiama `nessuna` e che è una delle quattro categorie, non un buco.

Il file di uscita è `dati/lingue/immagini_2.json`, **separato**: il primo giro
resta com'è, perché è la prova di che cosa aveva trovato una ricerca che cercava
le parole.

Uso:  python3 sorgenti/lingue/cerca_immagini_2.py LA EL FE
      python3 sorgenti/lingue/cerca_immagini_2.py --unisci
"""
import importlib.util
import json
import os
import sys
import time

BASE = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(BASE, "..", ".."))
PRIMO = os.path.join(RADICE, "sorgenti", "lingue", "cerca_immagini_oggetti.py")
ASSOC = os.path.join(RADICE, "dati", "lingue", "associazioni.json")
ESITO = os.path.join(RADICE, "dati", "lingue", "immagini_2.json")

spec = importlib.util.spec_from_file_location("cerca1", PRIMO)
cerca1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cerca1)

# Le voci, nell'ordine di `associazioni.json`: una riga per voce, e la riga
# **non puo' mancare**: se manca, il file non e' piu' allineato alle trenta voci
# e il conto torna perche' qualcosa e' stato dimenticato.
TERMINI = {
    "LA": [
        ("gli auspici", ["lit(u)us augur", "augur lituus"]),
        ("i presagi", ["Roman augur divination", "Etruscan augury"]),
        ("il volo degli uccelli", ["Corvus augury", "Roman augur birds"]),
        ("l'ispezione delle interiora", ["Piacenza liver", "extispicy liver divination"]),
        ("i haruspici", ["haruspex relief", "Etruscan diviner relief"]),
        ("i sacerdoti e i riti", ["Roman priest ritual", "capite velato priest relief"]),
        ("il fulmine", ["winged thunderbolt Jupiter", "fulmen Jupiter thunderbolt"]),
        ("la peste", ["plague of Athens", "Plague of Athens vase"]),
        ("i sogni", ["Artemidorus Oneirocritica", "Oneirocritica manuscript"]),
        ("i numeri", ["Roman numerals inscription", "Roman numerals clock"]),
        ("il calendario e i giorni", ["Fasti Antiates", "Fasti Antiates maiores calendar"]),
        ("i mesi", ["Roman calendar Fasti months", "Calendarium Romanum"]),
        ("le feste", ["ludi Romani fresco", "Pompeii ludi amphitheatre"]),
        ("le processioni", ["pompa circensis", "Pompa circensis relief"]),
        ("i voti", ["votive stele", "Votive stele Roman"]),
        ("i giuramenti", ["coniuratio relief", "Roman oath soldiers relief"]),
        ("la maledizione", ["curse tablet defixio", "Defixio tablet"]),
        ("il tabù", ["piaculum", "Roman nefas fas relief"]),
        ("i nomi e la sorte", ["Roman praenomen nomen inscription", "Roman name inscription"]),
        ("il destino", ["Fatum painting", "Moirai Fates painting"]),
        ("i segni premonitori", ["Roman omen prodigy", "prodigy Roman literature"]),
        ("i miracoli", ["miraculum ancient manuscript", "Pliny prodigum"]),
        ("i presagi delle nascite", ["Roman birth omens", "Roman infant omens"]),
        ("i riti funebri", ["Roman funeral procession", "Pompa funeris Roman relief"]),
        ("il fuoco sacro", ["Temple of Vesta fire", "Vestae virgines fire"]),
        ("gli animali divini", ["Lupa Capitolina", "Roman sacred animals relief"]),
        ("i luoghi sacri", ["Roman templum ground plan", "Templum in sky augury"]),
        ("le formule di protezione", ["abraxas gem", "gem gemma magica protective"]),
        ("la vita quotidiana", ["Roman daily life mosaic", "Pompeii daily life mosaic"]),
        ("i proverbi", ["Roman funerary epigram", "Latin proverb manuscript"]),
    ],
    "EL": [
        ("il vino", ["Ancient Greek wine krater", "Greek wine amphora"]),
        ("la produzione del vino", ["Ancient Greek wine press torcularium", "Greek grape press ancient"]),
        ("l'oliva", ["Greek olive oil amphora", "Greek olive branch amphora"]),
        ("l'olio d'oliva", ["Greek olive oil lekythos", "olive oil amphora Greek"]),
        ("l'acqua", ["Greek hydria water", "Ancient Greek water jug"]),
        ("il simposio", ["Greek symposium red figure", "Symposium scene Greek vase"]),
        ("il banchetto", ["banquet scene Greek vase", "Greek banquet reclining"]),
        ("la coppa", ["kylix Greek cup", "Ancient Greek kylix museum"]),
        ("il consumo rituale", ["Greek libation oinochoe", "libation phiale Greek"]),
        ("il vino di Maronea", ["Maroneia amphora", "amphora Maroneia"]),
        ("vini di Creta", ["Cretan amphora", "Crete amphora wine"]),
        ("il kykeon", ["kykeon", "Ancient Greek drink kykeon"]),
        ("la birra", ["ancient beer Egypt", "Beer in ancient Egypt"]),
        ("il caffè", ["coffee cup espresso", "Coffee culture"]),
        ("il tè", ["Greek teapot", "tea history museum"]),
        ("le coppe dipinte", ["Greek black figure kylix", "kylix black figure painting"]),
        ("gli inventari dei simposi", ["Greek pottery shapes", "Greek vase shapes diagram"]),
        ("i nomi dei vasi", ["Greek vase shapes", "amphora types Greek"]),
        ("i vini dirottati", ["Roman wine adulteration law", "Wine law Roman inscription"]),
        ("la sete", ["Greek fountain house", "Ancient Greek fountain nymphaeum"]),
        ("l'ospitalità", ["xenia hospitality Greek", "Greek guest friendship vase"]),
        ("il brindisi", ["Greek drinking scene symposium", "Greek symposium reclining"]),
        ("i precetti di temperanza", ["Greek symposion moderation", "Water clock klepsydra"]),
        ("i vini del Peloponneso", ["Peloponnesian amphora", "Greek amphora wine transport"]),
        ("i vini delle isole", ["Greek island amphora wine", "amphora wine Rhodes"]),
        ("il mosto", ["grape must", "wine must grape juice"]),
        ("la conservazione", ["amphora storage pithos", "pithos storage Greek"]),
        ("il trasporto delle botti", ["Roman wine transport amphora ship", "amphora cargo ship wreck"]),
        ("la tavola", ["Ancient Greek dining table", "Greek symposium table"]),
        ("il brindisi degli atleti", ["Greek athlete victor cup", "Nike victory statue athlete"]),
    ],
    # Il ferrarese non ha oggetti: ha **campi di proverbi**. Pietro ha deciso il
    # 04/10/2026 di associare «qualcosa di evocativo»: la cosa ferrarese di cui
    # il campo parla. Non e' l'immagine del proverbio — un proverbio non ha
    # immagine — e' la cosa che il proverbio riguarda, e che si può fotografare
    # per davvero. Le voci senza una cosa reale restano `nessuna` col motivo.
    "FE": [
        ("i proverbi dell'agricoltura", ["Ferrara campagna paesaggio", "Ferrara countryside"]),
        ("i proverbi dei mestieri", ["Ferrara fabbro forgiatura", "blacksmith forge Italy"]),
        ("i proverbi sul cibo", ["pane ferrarese", "salumi Ferrara"]),
        ("i proverbi sulla famiglia", ["Ferrara famiglia ritratto antico", "Ferrara corte ducale"]),
        ("i proverbi sulla fortuna", ["Ferrara Castello Estense", "Ferrara duomo interno"]),
        ("i proverbi sulla pigrizia", ["gatto dormiente", "Ferrara volto dipinto"]),
        ("i proverbi sul denaro", ["Ferrara moneta antica", "italian old coins"]),
        ("i proverbi sulla fiducia", ["Ferrara Volto Santo", "Ferrara parete dipinta"]),
        ("i proverbi sul tempo", ["Torre dell'Orologio Ferrara", "Ferrara clock tower"]),
        ("i proverbi sull'andare e venire", ["Cammino degli Angeli Ferrara", "Ferrara strada lastricata"]),
        ("i proverbi dei mesi", ["calendario illustrato antico", "Italian calendar old"]),
        ("i proverbi delle stagioni", ["raccolta grano vintage", "harvest wheat field"]),
        ("i modi di dire del corpo", ["anatomia antica tavola", "Old anatomical illustration"]),
        ("i modi di dire del volto", ["maschera carnevale", "Volto dipinto antico"]),
        ("i modi di dire della casa", ["Ferrara Via delle Vigne", "Ferrara casa storica facciata"]),
        ("i modi di dire della strada", ["Ferrara pavimento cordonato", "Ferrara strada piazza"]),
        ("i modi di dire del lavoro", ["Ferrara officina artigiana", "artisan workshop Italy"]),
        ("i modi di dire dell'amore", ["Ferrara Castello Estense fossato", "medieval manuscript illumination lovers"]),
        ("i modi di dire del tacere", ["finger to lips gesture", "silence gesture painting"]),
        ("i modi di dire dell'urlare", ["tamburo Ferrara", "Ferrara maschera urlo"]),
        ("le esclamazioni", ["Ferrara insegna", "Ferrara cartello storico"]),
        ("i saluti rituali", ["Ferrara mano stretta", "Italian greeting old postcard"]),
        ("i soprannomi dei quartieri", ["Ferrara targa via", "Ferrara street sign"]),
        ("i nomi delle porte e delle piazze", ["Porta Paola Ferrara", "Ferrara piazza monument"]),
        ("la parlata dei mercati", ["Piazza delle Erbe Ferrara", "Ferrara mercato coperto"]),
        ("la parlata delle feste", ["Carnevale di Ferrara", "Ferrara addizione carnevale"]),
        ("la parlata dei bambini", ["bambini gioco antico", "children playing old photograph"]),
        ("la parlata degli anziani", ["anziani conversazione", "old men conversation photograph"]),
        ("i proverbi dei viaggiatori", ["Ferrara ponte antico", "viator medieval manuscript"]),
        ("i proverbi di confine", ["mura di Ferrara", "Ferrara mura antiche"]),
    ],
}

LINGUE = ("IT", "FE", "LA", "EN", "SI", "EL")


def nomi_voci():
    with open(os.path.join(RADICE, "dati", "lingue", "immagini_oggetti.json"),
              encoding="utf-8") as f:
        primo = json.load(f)
    out = {}
    for r in primo["risultati"]:
        out.setdefault(r["lingua"], []).append(r["voce"])
    return out


def controlla_allineamento():
    """Le voci cercate devono essere **esattamente** le trenta del primo giro.

    Una tabella di termini con una voce in piu' o in meno' sposta tutte le
    righe: il primo giro l'ha gia' fatto e il suo file lo dichiara
    (`termini` allineati all'ordine delle trenta voci). Il controllo sta qui
    perche' il costo di sbagliarlo e' tutto il lavoro.
    """
    per = nomi_voci()
    problemi = []
    for lingua in sorted(TERMINI):
        cercate = [v for v, _ in TERMINI[lingua]]
        vere = per.get(lingua, [])
        if cercate != vere:
            mancanti = [v for v in vere if v not in cercate]
            inpiu = [v for v in cercate if v not in vere]
            problemi.append("%s: le voci cercate sono %d e le voci sono %d; "
                            "mancano %s, in piu' %s"
                            % (lingua, len(cercate), len(vere), mancanti, inpiu))
    for p in problemi:
        print("   difetto %s" % p)
    return not problemi


def cerca_una(lingua):
    # **Non** `zip(nomi, TERMINI[lingua])`: il secondo elemento della tabella e'
    # gia' la coppia (voce, termini), e lo zip produceva un termine che era il
    # **nome italiano della voce**. Il primo giro aveva lo stesso difetto, ed e'
    # la ragione delle 67 voci a rischio di G7: cercava «gli auspici» su
    # Commons invece del lituo dell'augure.
    out = []
    for voce, termini in TERMINI[lingua]:
        print("   %s %-42s %s" % (lingua, voce, termini[0]), flush=True)
        candidati = cerca1.cerca(termini)
        out.append({
            "lingua": lingua, "numero": len(out) + 1, "voce": voce,
            "termini": termini, "giro": 2,
            "candidati": candidati,
        })
        time.sleep(0.3)
    return out


def unisci():
    with open(ESITO, encoding="utf-8") as f:
        vecchio = json.load(f)
    per_voce = {(r["lingua"], r["voce"]): r for r in vecchio.get("risultati", [])}
    nuovi = 0
    for r in vecchio.get("risultati", []):
        key = (r["lingua"], r["voce"])
        if key in per_voce and r.get("giro") == 2:
            nuovi += 1
    esito = {
        "versione": 2,
        "data": time.strftime("%Y-%m-%d"),
        "nota": "Secondo giro di ricerca, e solo per il latino, il greco e il "
                "ferrarese. Il primo giro sta in immagini_oggetti.json e non "
                "e' stato toccato: e' la prova di che cosa aveva trovato una "
                "ricerca che cercava le **parole** invece delle **cose**.",
        "principio": "si cerca la cosa che si vede: alla voce «gli auspici» "
                     "il lituo dell'augure, non un file che si chiama "
                     "auspicia. Dove la cosa non esiste si dichiara che "
                     "l'immagine non esiste.",
        "risultati": vecchio.get("risultati", []),
    }
    with open(ESITO, "w", encoding="utf-8") as f:
        json.dump(esito, f, ensure_ascii=False, indent=1)
    print("scritte %d voci del secondo giro" % nuovi)


def main():
    if "--unisci" in sys.argv:
        return unisci()
    lingue = [a for a in sys.argv[1:] if not a.startswith("--")] or list(TERMINI)
    print("== allineamento delle voci")
    if not controlla_allineamento():
        return 1
    esistenti = {}
    if os.path.exists(ESITO):
        with open(ESITO, encoding="utf-8") as f:
            esistenti = {(r["lingua"], r["voce"]): r
                         for r in json.load(f)["risultati"]}
    for lingua in lingue:
        if lingua not in TERMINI:
            print("   nessuna tabella dei termini per %s" % lingua)
            continue
        print("== %s" % lingua)
        for r in cerca_una(lingua):
            esistenti[(r["lingua"], r["voce"])] = r
            with open(ESITO, "w", encoding="utf-8") as f:
                json.dump({"versione": 2, "data": time.strftime("%Y-%m-%d"),
                           "nota": "Secondo giro: latino, greco e ferrarese. "
                                   "Il primo giro sta in immagini_oggetti.json.",
                           "principio": "si cerca la cosa che si vede, non la "
                                        "parola.",
                           "risultati": list(esistenti.values())},
                          f, ensure_ascii=False, indent=1)
    print("fuori: %s" % os.path.relpath(ESITO, RADICE))
    return 0


if __name__ == "__main__":
    sys.exit(main())
