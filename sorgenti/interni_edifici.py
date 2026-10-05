# -*- coding: utf-8 -*-
"""Gli interni degli edifici che il gioco mostra: le stanze, e che cosa c'è dentro.

**Il problema che questo file risolve.** L'anno 1 si gioca dentro Ferrara, in
trenta edifici reali (`dati/ambienti_livelli.json`). Di quegli edifici il
progetto ha la **sagoma** — il poligono da OpenStreetMap, 7322 pezzi su 188
luoghi — e non ha l'interno. Il giocatore vede una facciata e non ci entra.

Il quinto anno ha gia' la nozione di **stanza** (`dati/luoghi_gioco.json`, campo
`tappe[].stanza`: `luogo`, `legame`, `filone`, `canto`, `ottava`). Quella
stanza e' un luogo narrativo — «il bosco dove Orlando perde il senno» — e non
un interno visitabile. **Quindi non e' la stessa cosa, e questo file non
confonde le due**: qui la stanza e' un ambiente fisico di un edificio reale,
con un nome che la fonte scrive.

**La fonte, e perche' questa e non un'altra.** Wikimedia Commons, perche' il
progetto la usa gia' per le sagome, per le immagini degli oggetti e per i
ritratti, e perche' e' l'unica che *distingue una stanza dall'altra con un nome
proprio* dentro una categoria. Un blog di viaggi dice «il castello ha delle
sale», che non si puo' codificare; Commons ha
`Category:Castello Estense (Ferrara) - Salone dei Giochi`, che si puo'.

**Il metodo, e la parte che non funziona.** Il nome del gioco e il nome di
Commons sono due nomi diversi: il gioco scrive «Castello Estense» e Commons
scrive «Castello Estense (Ferrara)». La categoria si cerca quindi per titolo
con tre qualificatori provati in ordine — `(Ferrara)`, il nome solo, e
`nome, Ferrara` — e **il primo che risponde vince**. Un edificio per cui
nessuno dei tre risponde viene registrato come `nessuna_categoria`: e' un
assenza dichiarata, non uno zero.

**Cosa porta ogni stanza.** Il nome come lo scrive la fonte, il numero di
immagini che la stanza ha, e le licenze di quelle immagini. La licenza non si
deduce: si legge dai file, e una stanza con immagini tutte senza licenza
libera dichiarata non entra nella salvadanaio delle fonti.

Uso:  python3 sorgenti/interni_edifici.py            # scrive dati/interni_edifici.json
      python3 sorgenti/interni_edifici.py --sonda    # solo il conto, senza scrivere
"""
import io
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

RADICE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AMBIENTI = os.path.join(RADICE, "dati", "ambienti_livelli.json")
USCITA = os.path.join(RADICE, "dati", "interni_edifici.json")
CACHE = os.path.join(RADICE, "dati", "interni_edifici_cache.json")

API = "https://commons.wikimedia.org/w/api.php"
# **User-Agent dichiarato**: senza, Commons risponde 403. Non e' un muro, e' la
# regola del progetto Wikimedia, e dichiararlo e' anche il modo giusto per farsi
# notare invece di sembrare uno script anonimo.
UA = "i-cinque-duchi/1.0 (progetto didattico; Pietro Fabbri)"

# L'attesa fra una richiesta e l'altra. La prima versione faceva trenta
# richieste di fila e si prese un 429: la lezione e' che una raccolta che non
# raggruppa le richieste non accelera, si fa bloccare.
ATTESA = 1.1

# Le forme di titolo, in ordine di prova. Il nome e' quello che scrive il
# registro dei luoghi del gioco, che non e' quello di Commons.
#
# **Le due prime forme sono quelle che reggono, e le ho messe per prime per una
# ragione che la prima versione del file non aveva capito.** Su Commons gli
# interni di un edificio non stanno nella categoria dell'edificio: stanno in una
# categoria separata che si chiama `... - Interior`, e li stanze sono sue
# sottocategorie. Cercando le stanze dentro `Category:Castello Estense
# (Ferrara)` si trova quasi niente, e la prima esecuzione aveva reso **una sola
# stanza su trenta edifici**: non un edificio senza interni, ma il metodo
# sbagliato. Le due forme dell'edificio restano in coda perche' ci sono
# edifici le cui stanze stanno direttamente sotto la categoria dell'edificio.
QUALIFICATORI = (
    "%(nome)s (Ferrara) - Interior",
    "%(nome)s - Interior",
    "%(nome)s (Ferrara)",
    "%(nome)s",
    "%(nome)s, Ferrara",
)

# Una sottocategoria e' una **stanza** solo se il suo nome lo dice. Su Commons
# la categoria di un edificio contiene quattro cose mescolate: le stanze, le
# parti di una stanza (soffitti, scale, capitelli), e le cose che non sono
# dell'edificio (modelli, eventi, libri in mostra). **Il criterio e' dichiarato
# in due tempi, e l'ordine conta**: prima si esclude, e ogni esclusione porta
# il motivo; poi, su quello che resta, si cerca una parola di ambiente.
#
# **Il primo criterio e' sbagliato, e il secondo ancora di piu'.** La prima
# versione del file accettava solo ` - Sala`, ` - Chapel`, ` - Courtyard`: la
# stanza cioe' sta subito dopo un trattino. Ma su Commons il trattino puo' stare
# anche **dopo**: `Salone dei Giochi - Castello Estense (Ferrara)` e `Sala dei
# Comuni - Castello Estense (Ferrara)` sono due stanze vere che il criterio
# scartava, e `Alfonso I d'Este's Camerino d'Alabastro` non ha trattino
# per niente. Tre stanze su ventisei, tutte scartate. Ora la parola di ambiente
# si cerca **dovunque sia nel nome**, in italiano e in inglese, che sono le due
# lingue con cui la fonte nomina.
#
# Il nome della stanza che si scrive nel catalogo e' quello che la fonte scrive,
# ripulito del nome dell'edificio: la fonte mette l'edificio o prima
# (`Castello Estense (Ferrara) - Sala dell'Aurora`) o dopo (`Salone dei Giochi -
# Castello Estense (Ferrara)`), e senza pulirlo la stanza si chiamerebbe come
# l'edificio.

STANZA = re.compile(
    r"\b(sala|salone|saletta|saletone|camera|camerino|cameretta|anticamera|"
    r"cappella|cappelle|cucine|cucina|corratoio|correttoio|chiesa|" \
    r"oratorio|sagrestia|"
    r"nave|loggia|logge|cortile|corti|chiostrino|chiostro|libreria|"
    r"aula|aule|galleria|gallerie|pinacoteca|oratorio|prigione|prigioni|"
    r"carcere|museo|archivio|biblioteca|salone|vestibolo|"
    r"room|rooms|hall|chapel|kitchen|kitchens|church|oratory|sacristy|nave|"
    r"theater|theatre|tribune|"
    r"courtyard|cloister|loggia|library|lecture|gallery|galleries|"
    r"dungeon|prison|jail|cellar|refectory|antechamber|cabinet|apartment)\b",
    re.IGNORECASE)

# Ci sono parole che **non** sono una stanza anche se il nome contiene una
# parola di ambiente: «le scale del castello» sono una stanza e una scala. Ogni
# esclusione porta il motivo, perche' una lista scartata senza dire perche'
# sembra una lista arbitraria.
NON_STANZA_PERCHE = (
    ("Ceiling", "i soffitti non sono una stanza: sono una parte di una stanza"),
    ("Capitals", "i capitelli non sono una stanza: sono un elemento architettonico"),
    ("Stair", "le scale collegano due piani: sono il passaggio, non la stanza"),
    ("Model", "il modello in scala non e' un interno: e' un'arma dell'edificio"),
    ("Event", "gli eventi non sono un interno: sono un uso temporaneo"),
    ("Temporary exhibition", "la mostra temporanea non e' un interno stabile"),
    ("exhibition", "la mostra non e' un interno stabile"),
    ("Coats of arms", "gli stemmi sono decorazione, non stanza"),
    ("Fresco", "gli affreschi sono la decorazione di una stanza, non la stanza"),
    ("Sculpture", "le sculture sono opere, non stanze"),
    ("Tomb", "la tomba e' un monumento, non una stanza"),
    ("Collection", "la collezione e' un'opera, non una stanza"),
    ("Historical image", "le immagini storiche non sono un interno"),
    ("Copy of", "la copia di un'opera e' un'opera, non una stanza"),
    ("Terracotta model", "il modello in terracotta e' un'arma, non un interno"),
    ("Interior of", "e' il contenitore degli interni, non una stanza fra le stanze"),
    (" - Interior", "e' il contenitore degli interni, non una stanza fra le stanze"),
    ("Facade", "la facciata e' l'esterno, non un interno"),
    ("Exterior", "l'esterno non e' un interno"),
    ("Garden", "il giardino non e' un interno"),
    ("Moat", "il fossato non e' un interno"),
    ("Portal", "il portale e' sulla facciata, non dentro"),
    ("Portrait", "il ritratto e' un'opera, non una stanza"),
)


def parole_di_ambiente():
    """Le parole che fanno riconoscere una stanza, davvero.

    Il numero si conta **sulle parole**, non sui pezzi del pattern: la prima
    versione contava i gruppi separati dalla barra verticale e diceva
    «66 parole» per un pattern che ne contiene trenta. Un numero contato sul
    posto sbagliato è peggio di un numero scritto a mano, perché sembra
    guardato.

    La lista viene anche usata dal controllo I3, che la confronta con quella
    del pattern: se un domani le parole cambiano e la lista no, il controllo
    lo vede.
    """
    dentro = STANZA.pattern
    dentro = dentro[dentro.index("(") + 1:dentro.rindex(")")]
    parole = set()
    for pezzo in dentro.split("|"):
        pezzo = pezzo.strip().strip("()")
        # una classe di caratteri come `[oi]` non è una parola: si scrive
        # per esteso, così il conto delle parole è il conto delle parole
        if not pezzo or "\x5c" in pezzo or "^" in pezzo or "$" in pezzo \
                or "[" in pezzo or "]" in pezzo:
            continue
        for p in pezzo.split("|"):
            p = p.strip()
            if p and "\x5c" not in p and "[" not in p and "]" not in p:
                parole.add(p.lower())
    return sorted(parole)


def e_stanza(nome, edificio=None):
    """La sottocategoria e' una stanza? Con il motivo quando non lo e'.

    Si guarda il **nome della stanza**, cioe' il nome della categoriaripulito
    dell'edificio: e' la parte che descrive l'ambiente, non quella che dice
    dove si trova. Il ricongiungimento con l'edificio avviene **prima**,
    perche' altrimenti il nome dell'edificio fa da parola di ambiente: in
    «Coats of arms in the Museo Casa Romei (Ferrara)» la parola «Museo» sta
    nel nome del museo e non in quello di nessuna stanza.
    """
    # **Le esclusioni si guardano sul nome intero, e le inclusioni sul nome
    # ripulito.** Il motivo e' che l'esclusione descrive *che cosa e' la
    # categoria* (`Pinacoteca Nazionale (Ferrara) - Interior` e' il
    # contenitore degli interni) e il nome intero e' l'unico posto dove
    # « - Interior» esiste: ripulito dell'edificio, il trattino e' sparito e la
    # categoria passa per una stanza. L'inclusione invece non puo' guardare il
    # nome intero, perche' l'edificio ci mette dentro parole di ambiente
    # («Museo» nel nome del Museo Casa Romei) che non sono quelle di nessuna
    # stanza.
    if edificio and normale(nome) == normale(edificio):
        return False, ("è il nome dell'edificio: la fonte ha aperto una "
                       "categoria dentro la propria, non ha distinto un "
                       "interno")
    if ISTITUZIONE.match(nome):
        return False, ("il nome comincia col nome di un'istituzione: è la "
                       "stessa cosa detta altrimenti, non un ambiente fra gli "
                       "ambienti")
    for frammento, perche in NON_STANZA_PERCHE:
        if frammento.lower() in nome.lower():
            return False, perche
    if " in the " in nome.lower():
        return False, ("la categoria parla di un oggetto che sta nell'edificio, "
                       "non di un ambiente: il nome dice «qualcosa in the "
                       "edificio»")
    pulito = nome_senza_edificio(nome, edificio)
    if STANZA.search(pulito):
        return True, ""
    return False, ("nessuna parola di ambiente nel nome della stanza: "
                   "il nome non dichiara che sia una stanza")


def nome_senza_edificio(nome, edificio=None):
    """Il nome della stanza, tolto l'edificio che la fonte ci appiccica.

    La fonte mette l'edificio o davanti (`Castello Estense (Ferrara) - Sala
    dell'Aurora`) o dietro (`Salone dei Giochi - Castello Estense (Ferrara)`),
    e con la stessa formula dentro e fuori: `Palazzo Paradiso (Ferrara) - Sala
    Agnelli`. Percio' si toglie il nome dell'edificio **ovunque sia**, insieme
    al trattino e al qualificatore che gli stanno accanto.

    **La regola non puo' essere "la parte piu' corta e' l'edificio".** L'ho
    scritta cosi' nella prima versione e sbagliava su diciassette nomi su
    trentanove: `Castello Estense (Ferrara) - Chapel` ha l'edificio nella
    parte lunga e la stanza in quella corta, e il risultato era il nome
    dell'edificio al posto della cappella — cioe' il file avrebbe scritto che
    il Castello Estense ha una stanza chiamata «Castello Estense (Ferrara)», e
    non si sarebbe accorto che la cappella non c'era. Serve l'edificio, e il
    chiamante ce l'ha.
    """
    pulito = nome.strip()
    if edificio:
        # via il qualificatore e l'edificio, in ogni ordine e in ogni posizione
        via = re.compile(re.escape(edificio)
                         + r"(?:\s*\([^)]*\))?"
                         + r"|\s*\([^)]*\)(?=[^-]*$)")
        pulito = via.sub(" ", pulito)
    if " - " in pulito:
        a, b = [x.strip() for x in pulito.split(" - ", 1)]
        # **il pezzo giusto e' quello che ha la parola di ambiente.** Il
        # trattino separa l'edificio dalla stanza, e l'edificio non c'e' piu'
        # nella parte giusta perche' e' stato tolto: scegliere «il primo» o
        # «il piu' corto» faceva scartare stanze vere. `San Romano (Ferrara) -
        # Cloister` dentro il Museo della Cattedrale perdeva il chiostro perche'
        # il primo pezzo era pieno e non diceva niente di un ambiente.
        if STANZA.search(a) and not STANZA.search(b):
            pulito = a
        elif STANZA.search(b) and not STANZA.search(a):
            pulito = b
        elif not a:
            pulito = b
        elif not b:
            pulito = a
        else:
            # nessuno dei due ha una parola di ambiente: il nome non lo
            # dichiara e nessuna regoria li sceglie; si tiene il pezzo piu'
            # corto, che di solito e' quello della stanza, e la decisione
            # resta nelle mani del chiamante, che pero' la rifiutera'
            pulito = b if len(b) < len(a) else a
    return re.sub(r"\s+", " ", pulito).strip(" -")


# Le licenze che il progetto accetta: pubblico dominio, CC0, CC BY e CC BY-SA,
# le stesse di `cerca_ritratti.py` e di `verifica_fonti_visive.py`.
#
# **Il confronto non puo' essere una ricerca di sottostringa.** La prima
# versione cercava la chiave `cc-by-sa-4.0` dentro il nome breve `CC BY-SA
# 4.0`: il trattino contro lo spazio, e la chiave non c'e' dentro nessuna delle
# duecentosessantasei licenze che tornano dalla ricerca. Il risultato era che
# **tre sole immagini libere su seicentocinquantatre**, e tutte e tre CC0: le
# 385 CC BY-SA 4.0 erano state scartate per una differenza di un trattino, e
# il conto che il file scriveva era giusto come numero e falso come verdetto.
# Percio' il confronto passa da `normale`, che toglie spazi, trattini,
# punti e underscore e abbassa le maiuscole: `ccbysa40` da una parte e
# dall'altra. Il nome breve che si scrive resta **quello che la fonte
# scrive**, non quello normalizzato.

LICENZE_LIBERE = {
    "cc0": "pubblico dominio (CC0)",
    "publicdomain": "pubblico dominio",
    "pd": "pubblico dominio",
    "norestrictions": "nessun vincolo dichiarato (No restrictions)",
    "ccby": "CC BY",
    "ccbysa": "CC BY-SA",
    "attribution": "attribuzione richiesta",
    "att": "attribuzione richiesta",
    "creativecommons": "Creative Commons",
}


def normale(testo):
    """Il testo senza spazi, trattini, punti e underscore, in minuscolo."""
    t = "".join(c for c in (testo or "").lower()
                if c not in " \t\-_.")
    return t


def breve(nome_licenza):
    """La licenza accettata che questo nome breve e', o `None`.

    La chiave restituita e' quella normalizzata, e serve al documento per
    dire **quale** delle licenze accettate e': `ccbysa40` e `ccbysa25` sono
    entrambe CC BY-SA ma non la stessa licenza, e il gioco deve poter
    scegliere.
    """
    n = normale(nome_licenza)
    if not n:
        return None
    for k in sorted(LICENZE_LIBERE, key=len, reverse=True):
        # `ccbysa` non puo' essere contenuto in `ccbysa40` per caso: si cerca
        # l'inizio della stringa, cosi' la sigla piu' lunga vince e una
        # sigla corta non aggancia una licenza che non e' la sua
        if n.startswith(k) or n == k:
            return k
    # e in fondo, per i nomi che portano la versione dentro la sigla
    for k in ("ccbysa", "ccby", "publicdomain", "pd"):
        if k in n:
            return k
    return None


def leggi(percorso, default=None):
    if not os.path.exists(percorso):
        return {} if default is None else default
    with io.open(percorso, encoding="utf-8") as f:
        return json.load(f)


def salva_cache(c):
    with io.open(CACHE, "w", encoding="utf-8") as f:
        f.write(json.dumps(c, ensure_ascii=False, sort_keys=True, indent=1))


def chiedi(parametri, cache, attesa=ATTESA):
    """Una domanda a Commons, con la cache su disco.

    **La cache è sul file, non in memoria**, e il motivo è che questa raccolta
    costa trenta richieste: senza cache, il giorno in cui la rete manca la
    raccolta si ferma al primo edificio, e il file resta a metà senza che
    nessuno lo dica. Con la cache, il file su disco è la risposta di ieri e la
    rete serve solo per ciò che è cambiato.
    """
    chiave = json.dumps(parametri, sort_keys=True)
    if chiave in cache:
        return cache[chiave]
    url = API + "?" + urllib.parse.urlencode(parametri, safe="|:")
    # **Cinque tentativi non bastavano.** La raccolta dei trenta edifici fa
    # qualche centinaio di richieste — la categoria, poi ogni stanza, poi le
    # immagini di ogni stanza in blocchi da cinquanta — e Commons risponde 429
    # a raffica. Il backoff è di 10 secondi per il primo tentativo e sale
    #in modo lineare, e la cache su disco fa sì che un'interruzione non perda
    # niente: la ripresa comincia dall'ultima risposta arrivata, non dalla
    # prima.
    for tentativo in range(8):
        try:
            richiesta = urllib.request.Request(
                url, headers={"User-Agent": UA})
            with urllib.request.urlopen(richiesta, timeout=60) as f:
                d = json.load(f)
            cache[chiave] = d
            salva_cache(cache)
            time.sleep(attesa)
            return d
        except urllib.error.HTTPError as e:
            # 429 e 503 sono il rate limit: si aspetta e si riprova. Un altro
            # errore non si aspetta, perché aspettare un 404 non lo fa
            # diventare una risposta.
            if e.code not in (429, 503) or tentativo == 7:
                raise
            attesa_lenta = 10 * (tentativo + 1)
            print("     %d, attendo %d secondi"
                  % (e.code, attesa_lenta))
            time.sleep(attesa_lenta)
    raise SystemExit("mai raggiunto")


def sottocategorie(titolo, cache):
    d = chiedi({"action": "query", "list": "categorymembers",
                "cmtitle": titolo, "cmtype": "subcat",
                "cmlimit": "500", "format": "json"}, cache)
    if "error" in d:
        return None
    return [m["title"][len("Category:"):] for m in
            d["query"]["categorymembers"]]


# Le parole che non distinguono un edificio da un altro: si buttano via
# prima di confrontare i nomi, perche' «di» e «de» sono in tutti.
NON_DISTINTIVE = frozenset((
    "della", "delle", "dei", "degli", "dello", "di", "del", "d",
    "la", "le", "il", "lo", "gli", "un", "una", "e", "ed", "a", "al",
    "ex", "nord", "sud", "est", "ovest", "ferrara", "italia", "the", "of",
    "and", "in", "at", "on",
))


def parole_distintive(nome):
    """Le parole del nome che possono identificare un edificio.

    «Palazzo Turchi di Bagno e Orto Botanico» ha dentro «Palazzo», «di»,
    «Orto» e «Botanico»: solo le ultime due servono, e «Palazzo» serve a
    poco. Percio' si butta via quello che non distingue e si tiene quello che
    e' abbastanza lungo: quattro lettere non sono un indizio.
    """
    parole = re.findall(r"[A-Za-zÀ-ÿ']+", nome.lower())
    return set(p for p in parole
               if p not in NON_DISTINTIVE and len(p) >= 5)


def cerca_categorie(nome, cache):
    """Le categorie che Commons offre per un nome, dalla ricerca.

    Il metodo del titolo esatto funziona solo quando il nome del gioco e'
    identico a quello di Commons, e non lo e' mai per tutti: il gioco
    scrive «Palazzo Turchi di Bagno e Orto Botanico» e Commons scrive
    «Palazzo Turchi di Bagno (Ferrara)». La ricerca e' il secondo tentativo,
    e restituisce **tutti** i candidati: scegliere il primo sarebbe una
    decisione senza regola, e il progetto non ne prende.
    """
    d = chiedi({"action": "query", "list": "search", "srsearch": nome,
                "srnamespace": "14", "srlimit": "20",
                "format": "json"}, cache)
    if "error" in d:
        return []
    return [m["title"] for m in d.get("query", {}).get("search", [])]


# Le parole con cui la fonte dice che una categoria parla di oggetti e non
# dell'edificio. Vale per la categoria dell'edificio come per le sue stanze:
# «Collections of the Museo Palazzina di Marfisa d'Este (Ferrara)» è una
# categoria vera, piena di immagini, e non è l'edificio che il gioco mostra.
NON_EDIFICIO = (
    ("Collections of", "la collezione è un'accolta di opere, non l'edificio"),
    ("Paintings in", "i dipinti sono opere, non l'edificio"),
    ("Paintings from", "i dipinti sono opere, non l'edificio"),
    ("Sculptures in", "le sculture sono opere, non l'edificio"),
    ("Furniture in", "i mobili sono opere, non l'edificio"),
    ("Medals in", "le medaglie sono opere, non l'edificio"),
    ("Pottery in", "la ceramica è un'opera, non l'edificio"),
    ("Frescos in", "gli affreschi sono opere, non l'edificio"),
    ("Frescoes in", "gli affreschi sono opere, non l'edificio"),
    ("Grotesque decoration", "la decorazione non è l'edificio"),
    ("Decoration in", "la decorazione non è l'edificio"),
    ("Models of", "i modelli non sono l'edificio, sono la sua rappresentazione"),
    ("Historical images", "le immagini storiche non sono l'edificio"),
    ("Exterior", "l'esterno non è l'edificio"),
)

# Le parole con cui un nome comincia a dire un'istituzione e non un ambiente.
# Una stanza il cui nome è il nome del museo che la contiene non è una stanza:
# e' la stessa cosa detta due volte, e il file la conterebbe due volte.
ISTITUZIONE = re.compile(
    r"^(museo|museum|pinacoteca|galleria|gallery|biblioteca|library|"
    r"theatre|theater|teatro|musei|museums)\b", re.IGNORECASE)


def ed_e_oggetti(titolo):
    """Il titolo non è l'edificio ma una raccolta di opere? Con il perché."""
    for frammento, perche in NON_EDIFICIO:
        if frammento.lower() in titolo.lower():
            return False, perche
    return True, ""


def citta_di(titolo):
    """La città che il titolo dichiara fra parentesi, o `None`.

    Su Commons la città sta fra parentesi: `Palazzo Schifanoia (Ferrara)` e
    `Museo del Risorgimento e della Resistenza (Vicenza)`. Il gioco gioca a
    Ferrara, e il progetto lo dichiara: un edificio che porta il nome di
    un'altra città non è quello che il gioco mostra, per quanto il nome
    sia identico.
    """
    for parentesi in re.findall(r"\(([^)]*)\)", titolo):
        p = parentesi.strip().lower()
        if p and p not in ("italia", "italy"):
            return parentesi.strip()
    return None


def scegli_categoria(candidati, edificio, cache):
    """Il candidato che parla dell'edificio del gioco, o `None`.

    **La regola e' dichiarata, e il motivo e' che l'alternativa e' peggiore.**
    Un candidato passa se condivide col nome del gioco almeno una parola
    distintiva. Senza questa regola, la ricerca per «Cattedrale di San
    Giorgio» o per «Museo del Risorgimento e della Resistenza» restituirebbe
    categorie vere di altri edifici, con stanze vere, e non sarebbero
    l'edificio che il gioco mostra: il file prenderebbe le stanze di un altro
    palazzo e le scriverebbe sotto il nome di quello giusto. Un numero
    giusto e un edificio falso e' la forma peggiore di errore che ci sia.

    Fra i candidati che passano vince **quello che ha sottocategorie**: un
    edificio senza stanze dichiarate vale meno di un edificio con, e se ce
    n'e' uno con stanze non si deve scegliere il primo per ordine alfabetico.
    """
    distintive = parole_distintive(edificio)
    if not distintive:
        return None, [], ("nessuna parola distintiva nel nome «%s»: senza, "
                          "la ricerca puo' restituire qualunque edificio del "
                          "mondo e non si distingue l'uno dall'altro" % edificio)
    # **La città si guarda prima di tutto il resto.** Il confronto delle
    # parole distintive accetta che «Museo del Risorgimento e della
    # Resistenza» di Vicenza passi per quello di Ferrara: le parole sono le
    # stesse, e senza questa regola il file avrebbe scritto le stanze di un
    # museo che il gioco non mostra, sotto il nome di quello che mostra. Il
    # numero era giusto e l'edificio falso.
    di_ferrara = [c for c in candidati if citta_di(c) in (None, "Ferrara")]
    altrove = [c for c in candidati if c not in di_ferrara]
    if candidati and not di_ferrara:
        return None, [], ("i %d candidati della ricerca sono tutti di un'altra "
                          "città (%s): il gioco gioca a Ferrara e quelle "
                          "categorie non sono l'edificio che mostra"
                          % (len(altrove), ", ".join(sorted(set(
                              citta_di(c) or "?" for c in altrove)))))
    # **Due parole, non una.** Il gioco scrive «Cattedrale di San Giorgio» e
    # la sua categoria si chiama «Museo della Cattedrale (Ferrara)»: una parola
    # su due, e il file prendeva le stanze di un museo che non è la cattedrale.
    # Quando il nome ha almeno due parole distintive, il candidato ne
    # condivide almeno due: una parola sola è un indizio, e un indizio non
    # basta per mettere un edificio al posto di un altro.
    soglia = 2 if len(distintive) >= 2 else 1
    condividono = [(c, len(distintive & parole_distintive(c)))
                   for c in di_ferrara]
    # **Una categoria che non dice dove si trova può essere accettata solo se
    # nessun'altra categoria con quel nome dice un posto diverso.** Il Museo
    # del Risorgimento e della Resistenza esiste a Vicenza e quello di Roma
    # non porta la città nel nome; il gioco mostra quello di Ferrara. Senza
    # questa regola il file prende il Vittoriano, che è il più conosciuto dei
    # tre, e lo scrive sotto il nome di quello che il gioco mostra.
    senza_citta = [c for c in di_ferrara if citta_di(c) is None]
    if altrove and senza_citta:
        di_ferrara = [c for c in di_ferrara if citta_di(c) is not None]
        if not di_ferrara:
            return None, [], ("i candidati che parlano dell'edificio non "
                              "dicono di che città sono, e altri candidati con "
                              "lo stesso nome sono di %s: il gioco gioca a "
                              "Ferrara e la fonte non permette di sapere se "
                              "quello sia qui"
                              % ", ".join(sorted(set(citta_di(c) or "?"
                                                      for c in altrove))))
    superano = [c for c, n in condividono if n >= soglia and c in di_ferrara]
    if not superano:
        return None, [], ("nessuno dei %d candidati della ricerca condivide "
                          "con il nome del gioco %d parole distinctive su %s "
                          "(%s): sono categorie vere, ma di altri edifici"
                          % (len(di_ferrara), soglia,
                             ", ".join(sorted(distintive)),
                             ", ".join(c[len("Category:"):] for c in di_ferrara[:4])
                             or "nessun candidato"))
    # e il candidato scelto non può essere una categoria di opere
    per_oggetti = []
    rimasti = []
    for c in superano:
        ok, perche = ed_e_oggetti(c)
        if not ok:
            per_oggetti.append(c)
            continue
        rimasti.append(c)
    if not rimasti:
        return None, [], ("i candidati che parlano dell'edificio sono "
                          "categorie di opere, non l'edificio: %s"
                          % ", ".join(sorted(set(per_oggetti))))

    for c in sorted(rimasti):
        sotto = sottocategorie(c, cache)
        if not sotto:
            continue
        # **la città si guarda anche nelle sottocategorie.** Il Teatro Comunale
        # di Ferrara su Commons si chiama come quello di Treviso, e la categoria
        # non porta la città: la porta una delle sue sottocategorie, e senza
        # questo controllo il file avrebbe preso le stanze del teatro giusto
        # al posto di quello mostrato.
        altrove = [x for x in sotto if citta_di(x) not in (None, "Ferrara")]
        if altrove:
            continue
        return c, superano, ""
    return None, rimasti, ("i candidati che parlano dell'edificio non hanno "
                            "sottocategorie di interni a Ferrara: o non hanno "
                            "stanze, o le stanze che hanno sono di un altro "
                            "edificio")


def nome_categoria_di(titolo):
    """Il nome dell'edificio dentro il titolo della categoria.

    Serve al riconoscimento delle stanze, che ha bisogno di sapere quale
    pezzo del nome della sottocategoria e' l'edificio e quale e' la stanza.
    Si toglie il qualificatore fra parentesi e il trattino che Commons usa per
    i sottoinsiemi. Se il titolo non ha un pezzo che sembri un edificio si
    restituisce il titolo intero: la funzione sbaglia dove non puo' fare
    diversamente, e sbagliare dicendolo e' diverso da sbagliare tacendo.
    """
    t = titolo[len("Category:"):] if titolo.startswith("Category:") else titolo
    via = re.sub(r"\s*\([^)]*\)", "", t).strip()
    via = via.split(" - ")[0].strip()
    return via or t


def immagini_e_licenze(titolo, cache):
    """Le immagini di una categoria, con la licenza di ciascuna.

    La licenza si legge dai file, in due passate: prima i nomi, poi le
    `extmetadata` dei file. Il nome della licenza viene da `LicenseShortName`
    o da `License`, e **non si deduce dalla presenza della fotografia**: una
    foto senza licenza non è un bene libero, e il progetto lo sa già per gli
    oggetti (dodici candidati respinti per metadati mancanti).
    """
    d = chiedi({"action": "query", "list": "categorymembers",
                "cmtitle": titolo, "cmtype": "file",
                "cmlimit": "500", "format": "json"}, cache)
    if "error" in d:
        return []
    titoli = [m["title"] for m in d["query"]["categorymembers"]]
    if not titoli:
        return []
    # la API accetta al massimo cinquanta titoli per domanda
    fuori = []
    for i in range(0, len(titoli), 50):
        blocco = titoli[i:i + 50]
        dd = chiedi({"action": "query", "titles": "|".join(blocco),
                     "prop": "imageinfo",
                     "iiprop": "extmetadata|url",
                     "format": "json"}, cache)
        for p in dd.get("query", {}).get("pages", {}).values():
            if "missing" in p:
                continue
            meta = (p.get("imageinfo") or [{}])[0].get("extmetadata", {})
            nome = (meta.get("LicenseShortName", {}) or {}).get("value") or \
                   (meta.get("License", {}) or {}).get("value") or ""
            autore = (meta.get("Artist", {}) or {}).get("value") or ""
            # l'artista è HTML: si tiene il testo e si buttano i tag
            autore = re.sub(r"<[^>]+>", "", autore).strip()
            fuori.append({"file": p["title"], "licenza": nome.strip(),
                          "autore": autore[:120], "libera": False})
    for f in fuori:
        # **un solo criterio**: quello che decide se l'immagine e' libera e'
        # quello che scrive il nome breve della licenza. Due funzioni che
        # rispondono alla stessa domanda possono rispondere cose diverse, e
        # il file non se ne accorgerebbe.
        f["licenza_accettata"] = breve(f["licenza"])
        f["libera"] = f["licenza_accettata"] is not None
    return fuori


def edifici_anno_uno():
    """I trenta edifici che l'anno 1 mostra, in ordine di tappa."""
    ambienti = leggi(AMBIENTI)["ambienti"]
    visti = []
    for a in ambienti:
        if a["anno"] != 1:
            continue
        if any(v["tappa"] == a["livello"] for v in visti):
            continue
        visti.append({"tappa": a["livello"], "luogo": a["luogo"],
                      "argomento": a["argomento"], "voce": a["voce"]})
    visti.sort(key=lambda v: int(v["tappa"].split("-")[1]))
    return visti


def raccogli(cache):
    """Un edificio per volta: la categoria, le stanze, e quello che non c'è."""
    edifici = edifici_anno_uno()
    out = []
    for i, e in enumerate(edifici, 1):
        nome = e["luogo"]
        # il nome del gioco può portare una parte fra parentesi che su Commons
        # è altrove: «Museo della Cattedrale (ex San Romano)» sta su Commons
        # come «Museo della Cattedrale (Ferrara)». Si prova il nome intero e
        # poi quello dentro le parentesi, che è il nome dell'edificio.
        candidati = [nome]
        m = re.match(r"^(.*?)\s*\((?:ex\s+)?[^)]*\)$", nome)
        if m and m.group(1).strip() != nome:
            candidati.append(m.group(1).strip())
        # e la parte dopo i due punti, che è come il gioco distingue
        # «Certosa: chiostro» e «Certosa: cimitero monumentale»
        if ":" in nome:
            prima = nome.split(":")[0].strip()
            if prima and prima not in candidati:
                candidati.append(prima)
        # **e la parte prima di una congiunzione.** Il gioco mette due cose
        # in un nome solo quando sono lo stesso posto: «Palazzo Turchi di
        # Bagno e Orto Botanico» è un palazzo e un orto, e la ricerca di
        # quel nome non trova niente perché non è il nome di nessuna
        # categoria. «Palazzo Turchi di Bagno» è. La regola prova anche i
        # pezzi dopo «e», «ed», «/» e «–», perché sono le congiunzioni con cui
        # il registro dei luoghi tiene insieme due nomi.
        for congiunzione in (" e ", " ed ", " / ", " – "):
            if congiunzione in nome:
                prima = nome.split(congiunzione)[0].strip()
                if len(prima) >= 4 and prima not in candidati:
                    candidati.append(prima)

        cat = None
        per = None
        for base in candidati:
            for q in QUALIFICATORI:
                titolo = "Category:" + q % {"nome": base}
                sott = sottocategorie(titolo, cache)
                if sott:
                    cat, per = titolo, base
                    break
            if cat:
                break

        cerca, superano, perche_cerca = [], [], ""
        prove, prove_riuscita = [], ""
        if not cat:
            # secondo tentativo: la ricerca. Il nome del gioco e' quasi
            # sempre diverso da quello di Commons, e il titolo esatto lasciava
            # diciassette edifici su trenta senza categoria.
            #
            # **Si prova ogni nome candidato, non solo il primo.** Il gioco
            # scrive «Palazzo Turchi di Bagno e Orto Botanico»: un edificio e
            # un orto botanico nella stessa voce, e la ricerca di quel nome non
            # trova niente. «Palazzo Turchi di Bagno» trova. La ricerca prova
            # allora i candidati in ordine e si ferma al primo che regge, e il
            # nome con cui ha cercato resta scritto.
            prove = []
            for base in candidati:
                cerca = cerca_categorie(base, cache)
                prove.append({"nome": base, "candidati": len(cerca)})
                cat, superano, perche_cerca = scegli_categoria(
                    cerca, nome, cache)
                if cat:
                    per = nome_categoria_di(cat)
                    cerca = [c for c in cerca if c in superano]
                    prove_riuscita = base
                    break
            if not cat:
                cerca = [c for c in cerca if c in superano]

        if not cat:
            out.append({
                "tappa": e["tappa"], "luogo": nome, "argomento": e["argomento"],
                "voce": e["voce"],
                "categoria_commons": None, "nome_cercato": candidati,
                "candidati_ricerca": len(cerca),
                "ricerca": prove,
                "stanze": [], "non_stanze": [],
                "vuoto": ["nessuna categoria di Commons regge per questo "
                          "edificio, ne' per titolo esatto ne' per ricerca: "
                          + (perche_cerca or "gli interni non sono dichiarati "
                             "da una fonte che il progetto possa citare, e "
                             "senza fonte non si scrivono")],
            })
            print("  %2d/%d %-52s nessuna categoria (%d candidati)"
                  % (i, len(edifici), nome[:52], len(cerca)))
            continue

        tutte = sottocategorie(cat, cache)
        stanze, non_stanze = [], []
        immagini_grezze = {}
        for s in tutte:
            # l'edificio serve: senza, il riconoscimento della stanza legge
            # il nome dell'edificio e ci vede dentro parole di ambiente che
            # non sono quelle di nessuna stanza
            ok, perche = e_stanza(s, per)
            if not ok:
                non_stanze.append({"categoria": s, "perche": perche})
                continue
            immagini = immagini_e_licenze("Category:" + s, cache)
            immagini_grezze[s] = immagini
            libere = [f for f in immagini if f["libera"]]
            stanze.append({
                "nome": nome_senza_edificio(s, per),
                "categoria": s,
                "immagini": len(immagini),
                "immagini_libere": len(libere),
                "licenze": sorted(set(f["licenza_accettata"] for f in immagini
                                      if f["licenza_accettata"])),
                "esemplare": (libere or immagini or [{}])[0].get("file"),
                "vuoto": ([] if libere else
                          ["nessuna immagine con licenza libera dichiarata: "
                           "la stanza c'è ma non entra nelle fonti del gioco"]),
            })
        stanze.sort(key=lambda s: s["nome"])
        out.append({
            "_licenze": [f for st in stanze
                         for f in immagini_grezze[st["categoria"]]],
            "tappa": e["tappa"], "luogo": nome, "argomento": e["argomento"],
            "voce": e["voce"],
            "categoria_commons": cat, "nome_cercato": [per],
            "come": ("titolo esatto" if not cerca else
                     "ricerca su «%s»: %d candidati, scelto quello che parla "
                     "dell'edificio" % (prove_riuscita, len(cerca))),
            "stanze": stanze, "non_stanze": non_stanze,
            "vuoto": ([] if stanze else
                      ["la categoria di Commons esiste ma non ha sottocategorie "
                       "che siano stanze: gli interni non sono separati uno per "
                       "uno nella fonte"]),
        })
        print("  %2d/%d %-52s %2d stanze su %d sottocategorie"
              % (i, len(edifici), nome[:52], len(stanze), len(tutte)))
    return out


def categorie_condivise(edifici):
    """Le categorie che stanno su più di una tappa, e con quali tappe.

    Le tre tappe della Certosa sono parti di un complesso solo e su Commons
    finiscono sulla categoria unica del complesso: è giusto. Ma senza questa
    dichiarazione il file lo dice in tre punti senza dirlo in nessuno, e chi
    lo legge conta tre edifici dove ce n'è uno. **Il controllo I6 chiede che
    la condivisione sia scritta**, e non che non accada: un tappa senza
    categoria propria è un'assenza, e va trattata come tale.
    """
    per_categoria = {}
    for e in edifici:
        if e["categoria_commons"]:
            per_categoria.setdefault(e["categoria_commons"], []).append(
                e["tappa"])
    return {c: ts for c, ts in per_categoria.items() if len(ts) > 1}


def riepilogo(edifici):
    con_stanze = [e for e in edifici if e["stanze"]]
    tutte_stanze = [s for e in con_stanze for s in e["stanze"]]
    con_immagini = [s for s in tutte_stanze if s["immagini_libere"]]
    return {
        "edifici": len(edifici),
        "edifici_con_categoria": len([e for e in edifici
                                      if e["categoria_commons"]]),
        "edifici_con_stanze": len(con_stanze),
        "stanze": len(tutte_stanze),
        "stanze_con_immagine_libera": len(con_immagini),
        "immagini": sum(s["immagini"] for s in tutte_stanze),
        "immagini_libere": sum(s["immagini_libere"] for s in tutte_stanze),
        "stanze_senza_immagine": len(tutte_stanze) - len(con_immagini),
        "categorie_condivise": len(categorie_condivise(edifici)),
        "da": "le sottocategorie di Commons che il nome dice essere stanze; "
              "il numero è contato, non dichiarato",
    }


def licenze_viste(edifici):
    """Le licenze dei file, contate: quello che la fonte ha davvero detto.

    Il conto e' fatto sui dati raccolti, non su una lista scritta a mano: se
    domani Commons dicesse un'altra licenza, il numero la mostrerebbe e il
    documento mentirebbe.
    """
    conto = {}
    for e in edifici:
        for f in e.get("_licenze", []):
            n = f["licenza"].strip() or "(nessuna dichiarata)"
            conto[n] = conto.get(n, 0) + 1
    return sorted(conto.items(), key=lambda kv: (-kv[1], kv[0]))


def metodo(parole):
    """Il metodo, **generato dalle regole e non scritto**.

    Le parole di ambiente gliele passa `main`, che le usa anche nel file: due
    copie della stessa lista in due funzioni, e il giorno che una cambia
    l'altra resta indietro.

    La prima versione scriveva qui «tre qualificatori provati in ordine»,
    mentre i qualificatori erano cinque: la frase invecchiava da sola e
    nessuno se ne accorgeva, perché era la stessa a scriverla e a leggerla. Ora
    il numero dei qualificatori, il numero delle esclusioni e il numero delle
    parole di ambiente sono letti da dove stanno, e la regola della città è
    quella del codice.
    """
    return {
        "categoria": "prima per titolo esatto: il nome dell'edificio con %d "
                     "qualificatori provati in ordine (%s); poi per ricerca, "
                     "sui nomi che il registro ricava dal nome dell'edificio. "
                     "Vince il primo che risponde e parla dell'edificio"
                     % (len(QUALIFICATORI),
                        ", ".join(q % {"nome": "NOME"} for q in QUALIFICATORI)),
        "citta": "una categoria è accettata solo se dichiara Ferrara o nessuna "
                 "città, e se dichiararne una, le sue sottocategorie non ne "
                 "dichiarano un'altra: il gioco gioca a Ferrara",
        "stanza": "prima si esclude, e ogni esclusione porta il motivo (%d "
                  "motivi); poi, sul nome ripulito dell'edificio, si cerca una "
                  "parola di ambiente fra le %d parole elencate in "
                  "`parole_di_ambiento`"
                  % (len(NON_STANZA_PERCHE), len(parole)),
        "licenza": "letta dai metadati di ciascun file e confrontata dopo aver "
                   "tolto spazi, trattini e punti: il nome breve della fonte è "
                   "`CC BY-SA 4.0` e la chiave del progetto è `ccbysa`, e un "
                   "trattino di differenza scartava 385 immagini",
        "attesa": "%.1f secondi fra una richiesta e l'altra: senza, Commons "
                  "risponde 429 e la raccolta si ferma" % ATTESA,
    }


def main():
    cache = leggi(CACHE, {})
    edifici = raccogli(cache)
    r = riepilogo(edifici)
    parole = parole_di_ambiente()

    if "--sonda" in sys.argv:
        print("\n== la sonda ==")
        for chiave, valore in sorted(r.items()):
            print("   %-34s %s" % (chiave, valore))
        return 0

    documento = {
        "versione": 1,
        "data": time.strftime("%Y-%m-%d"),
        "fonte": "Wikimedia Commons, via API standard 0.6",
        "licenza_fonte": "CC BY-SA 4.0 e CC0 per le immagini; le categorie sono "
                         "di Wikimedia Commons",
        "attribuzione": "(c) Wikimedia Commons contributors",
        "user_agent": UA,
        "scopo": "gli interni degli edifici che l'anno 1 mostra: le stanze che "
                 "la fonte nomina una per una, con quante immagini libere ha. "
                 "Non e' il catalogo delle stanze: e' quello che la fonte "
                 "dichiara, e quello che non dichiara resta dichiarato vuoto",
        "che_cosa_non_e": "NON e' un inventario di interni. NON e' il campo "
                          "`stanza` di `luoghi_gioco.json`, che e' un luogo "
                          "narrativo del Furioso e non un ambiente visitabile: "
                          "le due cose non si sommano e non si confondono. E "
                          "non e' una pianta: nessuna fonte libera del progetto "
                          "dà le dimensioni delle stanze",
        "metodo": metodo(parole),
        "licenze_accettate": sorted(set(LICENZE_LIBERE.values())),
        "licenze_viste_sulle_immagini": licenze_viste(edifici),
        "parole_di_ambiente": parole,
        "riepilogo": r,
        "categorie_condivise": {c: ts for c, ts
                                in sorted(categorie_condivise(edifici).items())},
        "edifici": [{k: v for k, v in e.items() if not k.startswith("_")}
                    for e in edifici],
    }
    with io.open(USCITA, "w", encoding="utf-8") as f:
        f.write(json.dumps(documento, ensure_ascii=False, separators=(",", ":")))
    print("\nscritto dati/interni_edifici.json (%d kB)"
          % (os.path.getsize(USCITA) // 1024))
    for chiave in ("edifici", "edifici_con_categoria", "edifici_con_stanze",
                   "stanze", "stanze_con_immagine_libera", "immagini",
                   "immagini_libere"):
        print("   %-34s %s" % (chiave, r[chiave]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
