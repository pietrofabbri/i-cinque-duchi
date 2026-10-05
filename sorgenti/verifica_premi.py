"""Verifica il catalogo dei premi: P1-P8.

Undici categorie, undici discipline e quattro prove di ammissione sono numeri e
nomi che si possono confrontare fra loro e con gli altri documenti. Qui si
controlla che la lista sia chiusa e senza buchi, che ogni disciplina abbia una
categoria primaria, che i sei ambiti della sfida a mani nude abbiano ciascuno un
premio possibile, che nessuna disciplina sia inventata, e che nessun premio possa
essere un'opera generata o un'immagine senza licenza.

  P1  le undici categorie sono A..K, senza buchi e senza duplicati
  P2  ogni disciplina ha almeno una categoria primaria, e sono le undici del progetto
  P3  i sei domini della sfida a mani nude hanno ciascuno almeno una categoria
  P4  nessuna disciplina abbinata e' una disciplina che il progetto non ha
  P5  nessun premio puo' essere generato o senza licenza: il divieto e' scritto
  P6  ogni record porta l'elemento interattivo da cui viene e l'argomento che
      `lingue.md` dà per quel livello; l'informatica non ne ha e lo dichiara;
      ogni voce e' usata cinque volte, una per anno
  P7  le trenta voci sono dichiarate in due file e le due dichiarazioni dicono
      la stessa cosa
  P8  nessun rimando porta a una prova che `premi.md` §3 non dichiara: le prove
      sono quattro, e un «prova 5» che gira in quattro file e' un numero vero
      che guarda il numero sbagliato

Uso:  python3 sorgenti/verifica_premi.py
      python3 sorgenti/verifica_premi.py --difetti   # ne inietta due
"""
import io
import json
import os
import re
import sys

RADICE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOC = os.path.join(RADICE, "docs", "videogioco-5-duchi-premi.md")
LINGUE = os.path.join(RADICE, "docs", "videogioco-5-duchi-lingue.md")
QUADRO = os.path.join(RADICE, "docs", "videogioco-5-duchi-quadro-trasversale.md")
PREMI = os.path.join(RADICE, "dati", "premi.json")
LINGUE_MD = os.path.join(RADICE, "docs", "videogioco-5-duchi-lingue.md")
ASSOCIAZIONI = os.path.join(RADICE, "dati", "lingue", "associazioni.json")
IMMAGINI_OGGETTI = os.path.join(RADICE, "dati", "lingue",
                                "immagini_oggetti.json")

# L'ordine delle sezioni di `lingue.md` §6 e l'oggetto che ognuna dichiara: qui
# la sezione si prende **per posizione** e l'oggetto si verifica, che è il
# contrario del generatore. Se i due non coincidono, i due controlli non
# possono sbagliare insieme.
SEZIONI_LINGUE = [("IT", "cibi"), ("FE", "detti popolari"),
                  ("LA", "superstizioni"), ("EN", "musiche"),
                  ("LIS", "artigianato tipico"), ("EL", "bevande")]
# `associazioni.json` e `immagini_oggetti.json` dicono SI, il catalogo dice LIS.
SIGLA_DALLA_PARTE = {"SI": "LIS"}


def normalizza(testo):
    """La regola di pulizia della cella, non il codice del generatore: la regola
    e' che il segno del facoltativo non fa parte dell'argomento."""
    return " ".join(testo.replace("\u2020", "").split())

CATEGORIE = list("ABCDEFGHIJK")

# Le discipline del gioco, dove l'informatica e' esclusa per decisione di Pietro.
DISCIPLINE = ("Italiano", "Ferrarese", "Latino", "Inglese", "Lingua dei segni",
              "Greco", "Diritto", "Etica", "Filosofia", "Psicologia",
              "Osservazione e attenzione")

STATI = ("dichiarato", "possibile", "chiuso")
# `da_costruire` e' sparito dalla lista il 03/10/2026: era la riga di
# `osservazione e attenzione`, che il gioco gia' praticava in quattro posti e che
# nessuno aveva cercato. Un dominio che il progetto non ha non si dichiara, si
# cerca: quindi se `da_costruire` torna in una tabella dei premi, questo controllo
# deve dire che il lavoro di cercarlo non e' stato fatto.

DOMINI_SFIDA = ("logica", "calcolo mentale e stime", "informatica",
                "linguistica e testo", "Costituzione e cittadinanza",
                "osservazione e attenzione")

VIETATI = ("immagine generata", "immagine sintetica", "senza licenza libera")

# Il registro delle modifiche, che in ogni documento ha un numero di sezione
# diverso («## 9. Registro delle modifiche», «## 7. Registro…») e a volte un
# livello di titolo diverso. Il pattern e' un posto solo perche' la regola sia
# scritta una volta: i due punti di sezione che esistono sono storici e non si
# toccano, e il numero della sezione non e' un numero che si scrive a mano.
REGISTRO = re.compile(r"(?m)^#{2,3} [0-9]*\.? ?Registro delle modifiche\s*$")

# La prima intestazione di un file, che sia un .md o un .py: e' il punto in cui
# la riga malata va messa, e cioe' **dentro il corpo**. Nei .py la docstring del
# modulo sta prima di qualunque intestazione, e quindi finisce anch'essa nel
# corpo: e' giusto, perche' la riga malata deve stare dove un lettore la puo'
# trovare, non in coda dove nessuno la legge.
TITOLO = re.compile(r"(?m)^#{1,3} ")

# I quattro file che c**itavano** il rimando pendente «la prova 5», oltre al
# documento dei premi e ai due generatori: sono quelli che, se il numero delle
# prove cambiasse, avrebbero continuato a dire una prova inesistente.
FONTI_VISIVE = os.path.join(RADICE, "docs",
                            "videogioco-5-duchi-fonti-visive.md")
LINGUE_IMMAGINI = os.path.join(RADICE, "docs",
                               "videogioco-5-duchi-lingue-immagini.md")


def leggi(percorso):
    """Il testo di un file, qualunque cosa sia: .md, .py, e un domani. Un
    rimando pendente puo' stare in un generatorore quanto in un documento, e il
    posto peggiore in cui lasciarlo e' quello che nessuno riapre."""
    with io.open(percorso, encoding="utf-8") as f:
        return f.read()


def sezione(doc, inizio, fine):
    """Il testo fra due marcatori: i documenti hanno piu' tabelle e ogni controllo
    deve leggere la sua, non la prima che capita."""
    i = doc.index(inizio)
    j = doc.index(fine, i + len(inizio))
    return doc[i:j]


def leggi(path):
    with io.open(path, encoding="utf-8") as f:
        return f.read()


def sezione_per_posizione(documento, numero):
    """La sezione §6.**numero** di `lingue.md`, per la sua posizione."""
    m = re.search(r"(?m)^### 6\.%d [^\n]*\n" % numero, documento)
    if not m:
        return None
    j = documento.find("\n### ", m.end())
    return documento[m.end():j if j > 0 else len(documento)]


def argomenti_della_sezione(corpo):
    """{anno, numero): argomento} dalla tabella della sezione."""
    fuori = {}
    for riga in corpo.splitlines():
        m = re.match(r"^\| (\d{1,2}) \|(.*)\|\s*$", riga)
        if not m:
            continue
        numero = int(m.group(1))
        celle = [normalizza(c) for c in m.group(2).split("|")]
        for anno, testo in enumerate(celle[:5], 1):
            fuori[(anno, numero)] = testo
    return fuori


def inietta_riga_malata(testo):
    """Il difetto di P8 dentro il **corpo** del testo, non in coda.

    In coda cadrebbe dentro il registro delle modifiche, che il controllo
    esclude per scelta: la prova passerebbe — o fallirebbe — per un motivo che
    non ha niente a che fare col difetto che dichiara di provare. La riga va
    messa **dentro** il corpo, e qui la parola «dentro» è la parola giusta.
    """
    m = TITOLO.search(testo)
    if not m:
        raise SystemExit("il testo non ha un titolo: dove metterei il difetto?")
    return "%s\nla prova 5 vieta che sia generato\n%s" % (
        testo[:m.start()], testo[m.start():])


def problemi_delle_prove(doc, documenti):
    """P8: i rimandi «prova n» devono esistere nella tabella di §3.

    **Il numero delle prove è letto dalla tabella**, non scritto qui: se il
    documento un giorno dichiarasse cinque prove, questo controllo accetterebbe
    «prova 5» senza che nessuno lo tocchi. I documenti da controllare sono quelli
    che citano le prove dei premi, e il catalogo: un rimando in un file di dati
    è un rimando che il giocatore non legge ma che il programma sì, e quindi
    invecchia peggio.

    Il difetto che questo controllo è nato per trovare è **cinque righe in
    quattro file** che dicevano «la prova 5», e §3 ne dichiara quattro: la
    quinta prova non esiste e nessuno se n'era accorto, perché un rimando a una
    cosa inesistente è una frase che si legge come le altre.

    **Il registro delle modifici è escluso, e per una ragione che è una scelta e
    non una scappatoia**: un registro riporta quello che il documento diceva
    allora, e quindi *deve* poter citare il rimando sbagliato che c'era — è
    l'unico posto in cui quella frase è vera. Controllare anche il registro
    obbligherebbe a riscrivere la cronologia per far passare un controllo, che è
    il modo migliore per far smettere a un registro di essere un registro. Il
    corpo del documento, quello che il lettore legge, è controllato per intero.
    """
    tabella = sezione(doc, "## 3.", "## 4.")
    dichiarate = set(re.findall(r"^\| \*\*(\d+)\. ", tabella, re.M))
    if not dichiarate:
        problemi = ["P8: la tabella delle prove di §3 non ha nessuna riga"]
        return problemi, dichiarate
    if dichiarate != {str(n) for n in range(1, len(dichiarate) + 1)}:
        problemi = ["P8: le prove dichiarate sono %s e non 1..%d"
                    % (", ".join(sorted(dichiarate, key=int)),
                       len(dichiarate))]
        return problemi, dichiarate
    problemi = []
    for nome, testo in documenti:
        corpo = REGISTRO.split(testo)[0]
        for m in re.finditer(r"prova (\d+)", corpo):
            if m.group(1) not in dichiarate:
                riga = corpo.count("\n", 0, m.start()) + 1
                problemi.append("P8: %s riga %d rimanda alla prova %s e §3 "
                                "dichiara %s" % (nome, riga, m.group(1),
                                                 ", ".join(sorted(
                                                     dichiarate, key=int))))
                return problemi, dichiarate
    return problemi, dichiarate


def problemi_del_legame(catalogo):
    """P6 e P7: che cosa ogni livello deve portare, e che cosa i due file delle
    trenta voci devono dire insieme.

    **Una sola funzione per il controllo e per la prova.** La prima versione
    aveva la prova riscritta per conto suo: due implementazioni dello stesso
    controllo, e una dentro la prova — il difetto che questo progetto si e' preso
    tre volte, con la particella che a un certo punto era il difetto invece
    della prova. Qui la prova inietta il difetto e chiama questa funzione, come
    fa `verifica_fonti_visive.py`.
    """
    fuori = []
    lingue_md = leggi(LINGUE_MD)
    attesi = {}
    for posizione, (sigla, oggetto) in enumerate(SEZIONI_LINGUE, 1):
        corpo = sezione_per_posizione(lingue_md, posizione)
        if corpo is None:
            fuori.append("P6: lingue.md non ha la sezione 6.%d" % posizione)
            continue
        dichiarato = re.search(r"Oggetto di interazione: \*\*(.+?)\*\*", corpo)
        if not dichiarato or dichiarato.group(1).strip() != oggetto:
            fuori.append("P6: la sezione 6.%d dichiara l'oggetto %r e non %r: "
                         "le sezioni e le lingue non sono piu' nello stesso "
                         "ordine, e il catalogo va riletto"
                         % (posizione,
                            dichiarato.group(1).strip() if dichiarato else "?",
                            oggetto))
            continue
        for (anno, numero), testo in argomenti_della_sezione(corpo).items():
            attesi[(sigla, anno, numero)] = testo
    if attesi and len(attesi) != 900:
        fuori.append("P6: le sei tabelle danno %d argomenti e non 900"
                     % len(attesi))

    usi = {}
    for record in catalogo:
        anno, numero = (int(x) for x in record["livello"].split("-"))
        if record["lingua"] == "INFO":
            if record["elemento_interattivo"] is not None or \
                    record["elemento_numero"] is not None:
                fuori.append("P6: %s e' un livello informatico e ha l'elemento "
                             "%r: le trenta voci sono delle lingue"
                             % (record["chiave"],
                                record["elemento_interattivo"]))
            elif not any("elemento interattivo assente" in v
                         for v in record["vuoto"]):
                fuori.append("P6: %s non ha elemento e non dichiara perche'"
                             % record["chiave"])
            continue
        if record["elemento_numero"] != numero:
            fuori.append("P6: %s porta l'elemento n.%s e il suo livello e' il "
                         "%d" % (record["chiave"], record["elemento_numero"],
                                 numero))
        atteso = attesi.get((record["lingua"], anno, numero))
        if atteso is None:
            fuori.append("P6: nessun argomento per %s in lingue.md"
                         % (record["lingua"], anno, numero))
        elif record["argomento_del_livello"] != atteso:
            fuori.append("P6: %s dichiara l'argomento %r e lingue.md scrive %r"
                         % (record["chiave"], record["argomento_del_livello"],
                            atteso))
        if not record["elemento_interattivo"]:
            fuori.append("P6: %s non ha l'elemento interattivo"
                         % record["chiave"])
        k = (record["lingua"], record["elemento_numero"])
        usi[k] = usi.get(k, 0) + 1
    if usi and sorted(set(usi.values())) != [5]:
        fuori.append("P6: le voci sono usate %s volte: ogni voce deve stare in "
                     "cinque livelli, uno per anno" % sorted(set(usi.values())))
    if len(usi) != 180:
        fuori.append("P6: gli elementi legati sono %d e non 180" % len(usi))

    with io.open(ASSOCIAZIONI, encoding="utf-8") as f:
        proposte = json.load(f)["associazioni"]
    with io.open(IMMAGINI_OGGETTI, encoding="utf-8") as f:
        ricercate = json.load(f)["risultati"]
    dalle_ricerche = {}
    for v in ricercate:
        dalle_ricerche[(SIGLA_DALLA_PARTE.get(v["lingua"], v["lingua"]),
                        int(v["numero"]))] = v["voce"]
    if len(dalle_ricerche) != 180:
        fuori.append("P7: immagini_oggetti.json ha %d voci e non 180"
                     % len(dalle_ricerche))
    # le due dichiarazioni delle trenta voci devono dire la stessa cosa
    per_associazioni = {}
    for a in proposte:
        sigla = SIGLA_DALLA_PARTE.get(a["lingua"], a["lingua"])
        for numero, voce in enumerate(a["voci"], 1):
            per_associazioni[(sigla, numero)] = voce
            if dalle_ricerche.get((sigla, numero)) != voce:
                fuori.append("P7: la voce %s n.%d e' %r nelle associazioni e %r "
                             "nelle immagini cercate"
                             % (sigla, numero, voce,
                                dalle_ricerche.get((sigla, numero))))
    # **per record, non per dizionario**: un record sbagliato che condivide la
    # chiave `(lingua, numero)` con altri quattro finisce coperto da quelli, e
    # la prova lo mostrava spostando `2-14-IT` sul numero quindici senza che
    # nessuno se ne accorgesse
    for record in catalogo:
        if not record["elemento_interattivo"]:
            continue
        k = (record["lingua"], record["elemento_numero"])
        if per_associazioni.get(k) != record["elemento_interattivo"]:
            fuori.append("P7: il record %s porta l'elemento %r e le "
                         "associazioni dicono %r per la voce n.%d"
                         % (record["chiave"],
                            record["elemento_interattivo"],
                            per_associazioni.get(k), record["elemento_numero"]))
    return fuori


def main():
    if not os.path.exists(DOC):
        print("manca %s" % DOC)
        return 2
    doc = leggi(DOC)
    lingue = leggi(LINGUE)
    quadro = leggi(QUADRO)
    problemi = []

    print("== P1. le undici categorie sono A..K, senza buchi ==")
    tabelle = re.findall(r"^\| \*\*([A-K])\*\* \| ([^|]+) \|", doc, re.M)
    trovate = [c for c, _ in tabelle]
    print("   categorie trovate: %s" % ", ".join(trovate))
    if trovate != CATEGORIE:
        mancanti = [c for c in CATEGORIE if c not in trovate]
        problemi.append("P1: le categorie sono %s, mancano %s" % (trovate, mancanti))
    for c, nome in tabelle:
        if len(nome.strip()) < 3:
            problemi.append("P1: la categoria %s non ha nome" % c)
    if "elenco è **chiuso**" not in doc and "elenco e' **chiuso**" not in doc:
        problemi.append("P1: il documento non dichiara l'elenco chiuso")

    print("\n== P2. ogni disciplina ha una categoria primaria, o un'eccezione dichiarata ==")
    tab = sezione(doc, "## 2.", "### 2.1")
    righe = re.findall(r"^\| \*\*([^*]+)\*\* \| ([^|]+) \| ([^|]+) \| ([^|]*) \|", tab, re.M)
    # la terza colonna e' il secondario e la quarta e' «da escludere»: la
    # dichiarazione di eccezione puo' stare in una qualunque delle tre, e in
    # questa tabella sta nella quarta, percio' si cerca nella riga intera
    primarie = {nome.strip(): (r[0], " ".join(r)) for nome, *r in righe}
    eccezioni = ("Osservazione e attenzione",)
    for d in DISCIPLINE:
        if d not in primarie:
            problemi.append("P2: la disciplina «%s» non ha riga" % d)
        elif d in eccezioni:
            # le due righe che la sezione 2.1 dichiara eccezione o da costruire:
            # devono dirlo anche nella riga, altrimenti l'eccezione e' invisibile
            if not re.search(r"nessuna delle dieci|da[_ ]costruire|non esiste ancora", primarie[d][1]):
                problemi.append("P2: «%s» e' eccezione ma la sua riga non lo dice" % d)
        elif not re.search(r"\*\*[A-K]\*\*", primarie[d][0]):
            problemi.append("P2: «%s» non ha una categoria primaria dichiarata" % d)
    print("   discipline con riga: %d su %d (eccezioni dichiarate: %s)"
          % (len(primarie), len(DISCIPLINE), ", ".join(eccezioni)))

    print("\n== P3. i sei domini della sfida hanno un premio o una dichiarazione di vuoto ==")
    tabella = sezione(doc, "### 2.1", "## 3.")
    righe = re.findall(r"^\| `([^`]+)` \| ([^|]+) \| ([^|]+) \|", tabella, re.M)
    premia = {d: (prem.strip(), stato.strip()) for d, prem, stato in righe}
    for dominio in DOMINI_SFIDA:
        if dominio not in premia:
            problemi.append("P3: il dominio `%s` non ha riga: nessun premio e nessuna dichiarazione" % dominio)
            print("   %-30s %s" % (dominio, "ASSENTE"))
            continue
        prem, stato = premia[dominio]
        vuoto = "nessuno" in prem or "nessuna" in prem
        print("   %-30s %s (%s)" % (dominio, "senza premio" if vuoto else "con premio", stato))
        if not vuoto and not re.search(r"\*\*[A-K]\*\*", prem):
            problemi.append("P3: `%s` ha un premio ma nessuna categoria" % dominio)
        if stato not in STATI:
            problemi.append("P3: `%s` ha lo stato «%s», che non e' fra %s"
                            % (dominio, stato, ", ".join(sorted(STATI))))
    if len(DOMINI_SFIDA) != 6:
        problemi.append("P3: i domini sono %d, non 6" % len(DOMINI_SFIDA))

    print("\n== P4. nessuna disciplina abbinata e' inventata ==")
    tab2 = sezione(doc, "## 2.", "### 2.1")
    lingue_nel_doc = set(re.findall(r"^\| \*\*([^*]+)\*\* \|", tab2, re.M))
    ambiti = set(re.findall(r"^\| \*\*(Diritto|Etica|Filosofia|Psicologia)\*\*", quadro, re.M))
    # tutte e undici sono discipline ammesse: `osservazione e attenzione` e'
    # chiusa il 03/10/2026 (`quadro-trasversale.md` §1.3), non un abbinamento
    # inventato
    ammesse = set(DISCIPLINE)
    extra = lingue_nel_doc - ammesse
    print("   discipline citate: %d; ambiti in quadro-trasversale: %d" % (len(lingue_nel_doc), len(ambiti)))
    for nome in sorted(extra):
        problemi.append("P4: la disciplina «%s» non e' fra quelle del progetto" % nome)
    if len(ambiti) != 4:
        problemi.append("P4: quadro-trasversale.md non dichiara piu' quattro ambiti")
    for nome in ("Italiano", "Ferrarese", "Latino", "Inglese", "Lingua dei segni", "Greco"):
        if ("**%s**" % nome) not in lingue:
            problemi.append("P4: lingue.md non dichiara piu' la lingua «%s»" % nome)

    print("\n== P5. nessun premio puo' essere generato o senza licenza ==")
    for v in VIETATI:
        # il divieto deve comparire nel documento come divieto, non come descrizione
        if v in doc.lower():
            problemi.append("P5: il documento contiene «%s» senza dichiararlo vietato" % v)
    if "l'elenco è **chiuso**" not in doc and "l'elenco e' **chiuso**" not in doc:
        pass
    for frase in ("vieta le immagini", "libera di diritti"):
        if frase not in doc:
            problemi.append("P5: il documento non dice che il premio dev'essere «%s»" % frase)
    print("   il divieto di generare e' dichiarato e il campo licenza e' fra le prove")

    print("\n== P8. nessun rimando a una prova che §3 non dichiara ==")
    citati = [(os.path.relpath(p, RADICE), leggi(p))
              for p in (DOC, FONTI_VISIVE, LINGUE_IMMAGINI,
                        os.path.join(RADICE, "sorgenti", "premi_catalogo.py"),
                        os.path.join(RADICE, "sorgenti", "art",
                                     "emblema_premi.py"))]
    problemi_8, dichiarate = problemi_delle_prove(doc, citati)
    problemi += problemi_8
    print("   %d prove dichiarate in §3, %d file citano rimandi, %s"
          % (len(dichiarate), len(citati),
             "nessun rimando pendente" if not problemi_8 else "difetti"))

    with io.open(PREMI, encoding="utf-8") as f:
        catalogo = json.load(f)["premi"]
    problemi += problemi_del_legame(catalogo)
    print("\n== P6 e P7. il legame fra livello ed elemento interattivo ==")
    print("   %d record, %d con elemento legato, e le trenta voci confrontate "
          "fra i due file che le dichiarano"
          % (len(catalogo),
             len([r for r in catalogo if r["elemento_interattivo"]])))

    print("\n== sintesi ==")
    if problemi:
        for p in problemi:
            print("   difetto: " + p)
        print("\nproblemi: %d" % len(problemi))
        return 1
    print("   nessun difetto: le undici categorie sono chiuse, le discipline hanno un premio, i sei domini sono dichiarati")
    print("\n==== controlli superati: 8/8 ====")

    if "--difetti" not in sys.argv:
        return 0

    print("\nprova: un difetto alla volta, col file rimesso a posto")

    # P8 e' l'unico dei tre che non guarda il catalogo: guarda i **testi**, e
    # quindi non puo' passare dalla stessa coppia (file, difetto) degli altri
    # due. Il suo difetto si inietta in memoria e si passa alla stessa funzione
    # che il controllo usa, ed e' la funzione a dover accorgersene.
    con_8, _dichiarate = problemi_delle_prove(
        doc, [(nome, inietta_riga_malata(testo)) for nome, testo in citati])
    visti8 = any(m.startswith("P8:") for m in con_8)
    iniettati, visti = 1, 1 if visti8 else 0
    print("   %-4s %s%s" % ("P8", "VISTO" if visti8 else "NON VISTO",
                            ": %s" % con_8[0][:70] if con_8 else
                            " (nessun difetto: la prova non ha provato)"))

    with io.open(PREMI, encoding="utf-8") as f:
        prima = f.read()
    for quale, _descrizione in (
            ("P6", "l'argomento del livello riscritto: `2-14-IT` porta un "
                   "argomento che `lingue.md` non scrive per quel livello"),
            ("P7", "l'elemento dichiarato sbagliato: `2-14-IT` porta «il mulo» "
                   "al posto della voce che i due file dicono. Il numero resta "
                   "giusto, quindi il conto non si muove")):
        copia = json.loads(prima)
        for r in copia["premi"]:
            if r["chiave"] == "2-14-IT":
                if quale == "P6":
                    r["argomento_del_livello"] = "14. Una riga inventata"
                else:
                    r["elemento_interattivo"] = "il mulo"
                break
        with io.open(PREMI, "w", encoding="utf-8") as f:
            f.write(json.dumps(copia, ensure_ascii=False,
                               separators=(",", ":")))
        try:
            with io.open(PREMI, encoding="utf-8") as f:
                rotto = json.load(f)["premi"]
            trovati = problemi_del_legame(rotto)
            visto = any(m.startswith(quale + ":") for m in trovati)
            altri = sorted({m[:3] for m in trovati
                            if not m.startswith(quale + ":")})
            iniettati += 1
            visti += 1 if visto else 0
            print("   %-4s %s%s" % (quale, "VISTO" if visto else "NON VISTO",
                                    ": %s" % trovati[0][:70] if trovati else
                                    " (nessun difetto: la prova non ha "
                                    "provato)"))
            if altri and visto:
                print("        altri controlli che l'hanno visto: %s"
                      % ", ".join(altri))
        finally:
            with io.open(PREMI, "w", encoding="utf-8") as f:
                f.write(prima)
    print("\ndifetti iniettati: %d, visti: %d" % (iniettati, visti))
    return 0 if (iniettati == visti and not problemi) else 1


if __name__ == "__main__":
    sys.exit(main())