"""Costruisce il **catalogo dei personaggi degli anni 2-5**, che i documenti dichiarano e i dati non hanno.

**Il buco, con le sue cifre.** L'anno 1 ha `dati/videogioco-5-duchi-anno1-personaggi.json`
con **93 schede**, ed è l'unico anno con un catalogo in `dati/`. Gli anni 2, 3, 4 e 5
hanno invece **centoventi schede scritte a mano** dentro i documenti (`### Q117 · Josquin
des Prez`), e `anno2-penisola.md` §6.3 dichiara che il «catalogo completo di **130
voci** è da generare in `dati/`» — che è una riga che il file non ha mai soddisfatto.

Perché conta più di una semplice lista. La `premi.md` §3 pretende che **ogni premio ha
una fonte dichiarata**, e la prova si fa sul premio, non sulla persona. I
**centocinquanta obbligatori** hanno le loro schede nei documenti; i **diciannove
facoltativi dell'anno 2 e i 269 in tutto** no. Finché il catalogo non esiste, la
verifica dei premi si può fare solo sui centocinquanta che si sanno, e il progetto
non può dichiarare che la copre tutta. Questo file è il primo passo: porta in `dati/`
quello che è **già scritto**, senza aggiungere niente di nuovo e senza decidere
niente.

**Le tre cose che questo file NON fa**, perché sono le tre tentazioni ovvie:

1. **non completa le schede**: i campi che i documenti non scrivono restano a `null`
   con il motivo accanto. Un campo a `null` con la ragione è diverso da un campo
   assente, e il secondo è un difetto;
2. **non sceglie fra le voci**: dove due nomi possono abbinarsi, l'abbinamento porta
   `prova` (per codice, per nome esatto, per nome normalizzato) e le ambiguità
   vengono dichiarate in `ambigue`, non risolte di nascosto;
3. **non giudica un'immagine**: la `fonte_immagine` viene da
   `sorgenti/art/ritratti_disponibili.json`, che è una **ricerca**, e l'accettazione
   o il rifiuto viene da `sorgenti/art/attestazione_immagini.json`, che è il
   **giudizio a vista**. Il nome del file non è una prova (vedi `AGENTS.md` §5): una
   scheda che ha un'immagine e non è attestata porta `verifica: non_verificata_a_vista`.

**L'ordine di lettura, che è la parte fragile.** Le schede si leggono per
**intestazione di sezione** (`### Q117 ·`), non contando le righe: i documenti hanno
sezioni diverse e una scheda può occupare un numero variabile di righe. Chi conta le
righe finisce con il motto di una scheda dentro il periodo di un'altra.

**Le righe hanno più campi per volta.** La prima riga di ogni scheda porta cinque o sei
campi insieme (`**Periodo:** … **Luogo:** … **Pin:** … **Strato:** …`), e la riga della
fonte ne porta tre. Un parser che «una riga = un campo» legge il primo e butta via il
resto: è il difetto che rendeva vuoti `luogo`, `pin`, `strato` e `attendibilita` su
tutte e 120 le schede senza che il sintomo dicesse perché. Qui la riga si divide sui
grassetti, e ogni campo prende il testo che lo segue fino al grassetto successivo.

Uso:
    python3 sorgenti/lingue/catalogo_personaggi.py           # scrive i quattro file
    python3 sorgenti/lingue/catalogo_personaggi.py --prova   # dice, non scrive
"""
import json
import os
import re
import sys
import unicodedata

RADICE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DOCS = os.path.join(RADICE, "docs")
DATI = os.path.join(RADICE, "dati")
INCONTRI = os.path.join(DATI, "incontri_livelli.json")
RITRATTI = os.path.join(RADICE, "sorgenti", "art", "ritratti_disponibili.json")
ATTESTAZIONE = os.path.join(RADICE, "sorgenti", "art", "attestazione_immagini.json")

# Gli anni 2-5 e il loro documento. L'anno 1 ha gia' il suo catalogo e non si tocca:
# reinventarlo sarebbe perdere 93 schede che hanno piu' campi di queste.
DOCUMENTI = {
    2: "videogioco-5-duchi-anno2-penisola.md",
    3: "videogioco-5-duchi-anno3-europa.md",
    4: "videogioco-5-duchi-anno4-mondo.md",
    5: "videogioco-5-duchi-anno5-mondo.md",
}

# I codici sono proposti nei documenti («I codici `Q` sono proposti (v. §13, Q5)») e
# vanno tenuti distinti dai codici dei dati, che sono gli stessi ma definitivi: il
# campo `codice_stato` dice quale delle due cose sia.
CODICE_STATO = "proposto_nei_documenti"

SCHEDA = re.compile(r"^###\s+(?P<codice>Q\d+)\s+·\s+(?P<resto>.+?)\s*$")

# Una riga di scheda e' una sequenza di campi in grassetto alternati al loro valore:
#   - **Periodo:** circa 3350 a.C. **Luogo:** Alpi. **Pin:** Bolzano. **Strato:** `S00`.
# Il grassetto puo' stare anche dentro il valore («un **algoritmo** e' un metodo»), e
# allora non e' un campo: si riconosce dal fatto che il testo dentro il grassetto
# somiglia a un nome di campo. Il campo e' scritto come **Luogo:** — il due punti e'
# dentro il grassetto, e questo e' successo perche' una volta la regex lo metteva
# fuori e non riconosceva niente, con il sintomo muto di 120 schede a campi vuoti.
GRASSETTO = re.compile(r"\*\*(?P<chiave>[^*]+?)\*\*")

# Le chiavi che i documenti usano, con il nome del campo che diventa nel JSON. La
# coppia e' (chiave nel documento, campo nel JSON) e non una lista sola, perche' una
# chiave puo' stare in due forme: `Fonte` e `Fonte dell'epoca` sono lo stesso campo.
# La ricerca e' per **inizio** della chiave (`periodo` trova anche `Periodo (fonte)`),
# e l'ordine conta: `fonte` viene prima di `fonte_epoca` solo perche' le due forme
# vanno discriminate dentro la stessa chiave, non per priorita'.
CHIAVI = [
    ("periodo", "periodo"),
    ("luogo", "luogo"),
    ("pin", "pin"),
    ("strato", "strato"),
    ("stato", "stato"),
    ("attendibilit", "attendibilita"),
    ("domanda", "domanda"),
    ("fonte", "fonte_epoca"),
    ("ricostruzione", "ricostruzione"),
    ("memoria", "memoria_successiva"),
    ("aggancio", "aggancio"),
    ("motto", "motto"),
    ("emblema", "emblema"),
    ("forza", "forza"),
]

# Le parole che il documento mette dentro il grassetto ma che NON sono campi. Senza
# questa lista il parser rinuncerebbe a meta' dei valori, perche' il grassetto del
# valore interrompe il campo: `Aggancio 2-2` verrebbe letto come `Aggancio` piu' la
# parola `algoritmo`, e il testo dell'aggancio resterebbe diviso in due.
NON_CAMPI = ("forza", "forte", "medio", "de scena", "fonte dipendente")

# I marcatori del titolo: `*(collettivo)*`, `*(aggiunta — …)*`, `*(in formazione)*`,
# `*(sostituisce X dal …)*`. Non sono parte del nome e vanno tenuti come bandiera.
# Il corsivo del titolo non chiude sempre dopo la parentesi: alla tappa 2-30 e' scritto
# `Il consiglio di corte *(collettivo): progettisti, muratori, proprietari, contadini*`,
# e una regex che pretende `)*` non lo vede — il nome resta con dentro il corsivo e
# quella scheda non abbinava niente. Per questo si prende **tutto** il corsivo, e la
# parentesi iniziale dice da che parte comincia.
MARCATORE = re.compile(r"\*(?P<testo>[^*]+)\*")

# La §12 dei documenti e' la tabella delle verifiche storiche: `| **V3** | Q101 —
# Eratostene | il metodo delle unita' … |`. E' l'unica cosa che assomiglia a
# `note_verifica`, e quindi la si legge, non la si inventa.
VERIFICA_RIGA = re.compile(r"^\|\s*\*?\*?V(?P<num>\d+)\*?\*?\s*\|(?P<voce>[^|]+)\|(?P<testo>[^|]+)\|")


def _pulisci(testo):
    """Togli il grassetto e gli spazi, e tieni il testo."""
    return re.sub(r"\*\*(.+?)\*\*", r"\1", testo).strip()


def _norm(testo):
    """Il nome ridotto a lettere e spazi: `Al-Khwarizmi` = `Al Khwarizmi`.

    Serve all'abbinamento per nome, perche' i documenti scrivono `Al-Khwarizmi` nella
    tabella e `Al-Khwarizmi` nella scheda, e `Ibn Battuta` e `Ibn Battuta`. La
    normalizzazione toglie accenti, punteggiatura e spazi doppi: e' una prova debole
    rispetto al codice, e per questo ogni scheda dichiara **quale prova** l'ha abbinata.
    """
    testo = unicodedata.normalize("NFKD", testo.lower())
    testo = "".join(c for c in testo if not unicodedata.combining(c))
    testo = re.sub(r"[^a-z0-9]+", " ", testo)
    return " ".join(testo.split())


# Gli articoli che si tolgono prima del confronto. Sono solo quelli che non possono
# stare dentro un nome proprio: `i`, `gli`, `il`, `lo`, `la`, `le`, `di`, `del`,
# `della`, `dei`, `delle`, `che`, `e`. Non si tolgono `a`, `al`, `in`, `per`, `con`,
# `da`: `Al-Khwarizmi` e `Ibn Battuta` cominciano con quelle, e toglierle farebbe
# `Khwarizmi` e `Battuta`, che sono nomi diversi.
ARTICOLI = {"i", "gli", "il", "lo", "la", "le", "di", "del", "della", "dei",
            "delle", "che", "e"}


def _norm2(testo):
    """Il nome senza articoli, per il confronto piu' forte.

    La tabella scrive `Il consiglio di corte: i progettisti, i muratori, i
    proprietari, i contadini` e la scheda `Il consiglio di corte: progettisti,
    muratori, proprietari, contadini`: sono la stessa voce, e la differenza sono
    quattro articoli. Non e' una prova forte come il codice, e resta una prova
    debole come `_norm`: chi legge deve sapere quale delle due ha abbinato.
    """
    return " ".join(w for w in _norm(testo).split() if w not in ARTICOLI)


def _parziale(a, b):
    """Una delle due voci e' l'inizio o la fine dell'altra, a confine di parola.

    Serve per i nomi che la tabella abbrevia: alla tappa 3-17 la tabella scrive
    `Josquin` e la scheda `Josquin des Prez`. Il confronto e' fatto parola per parola
    e non sui caratteri, perche' `Al` non deve essere l'inizio di `Alfonso` e `Boccaccio`
    non deve essere l'inizio di `Bocca`: il confine di parola e' la sola garanzia, ed
    e' anche la prova piu' debole delle tre, e per questo si dichiara con un nome
    proprio: `nome_parziale`.
    """
    if not a or not b:
        return False
    wa, wb = a.split(), b.split()
    if wa == wb:
        return True
    if len(wa) < len(wb):
        return wb[:len(wa)] == wa
    return wa[:len(wb)] == wb


def _titolo(resto):
    """Il nome della scheda, e le sue bandiere.

    `Ötzi — uomo dell'età del Rame` -> nome `Ötzi`, bandiera nessuna.
    `Ashoka *(sostituisce Ibn Khaldun dal 02/10/2026, v. §0.4)*` -> nome `Ashoka`, e
    si sa che sostituisce qualcuno. Il trattino lungo separa il nome dalla didascalia,
    e senza questa regola il nome sarebbe «Ötzi — uomo dell'età del Rame» e non
    abbobinerebbe niente.
    """
    bandiere = {}
    for m in MARCATORE.finditer(resto):
        t = m.group("testo")
        for parola, bandiera in (("collettiv", "collettivo"),
                                 ("aggiunta", "aggiunta"),
                                 ("sostituisce", "sostituisce"),
                                 ("in formazione", "in_formazione")):
            if parola in t.lower():
                bandiere[bandiera] = _pulisci(t)
                break
    pulito = MARCATORE.sub("", resto)
    # il trattino lungo: se c'e' un trattino lungo, il nome e' quello prima
    parti = re.split(r"\s+[—–]\s+", pulito, maxsplit=1)
    nome = parti[0].strip(" ,")
    didascalia = parti[1].strip() if len(parti) > 1 else None
    # il nome della voce collettiva porta la lista dopo i due punti: in tabella e'
    # «Il consiglio di corte: i progettisti, …» e nella scheda «Il consiglio di
    # corte: progettisti, …». Non e' un nome diverso, e' lo stesso nome scritto con
    # quattro articoli in piu'; l'abbinamento lo tratta come tale e lo dichiara.
    return nome, didascalia, bandiere


def _chiave_di(testo):
    """Il campo a cui appartiene un grassetto, o None se non e' un campo."""
    t = testo.strip().rstrip(":").strip().lower()
    if not t or t in NON_CAMPI:
        return None
    for prefisso, campo in CHIAVI:
        if t.startswith(prefisso):
            return campo
    return None


def _riga_campi(riga):
    """I campi di una riga, nell'ordine in cui il documento li scrive.

    Ogni campo prende il testo che segue il suo grassetto fino al grassetto successivo,
    che sia un campo o no: se il grassetto successivo e' una parola dentro il valore
    («un **algoritmo**»), il valore continua, e il pezzo in grassetto torna col suo
    testo. E' l'unico modo perche' `Periodo`, `Luogo`, `Pin`, `Strato` e
    `Attendibilità` — che stanno tutti sulla stessa riga — escano tutti e cinque.
    """
    pezzi = list(GRASSETTO.finditer(riga))
    campi = []
    for i, m in enumerate(pezzi):
        campo = _chiave_di(m.group("chiave"))
        if campo is None:
            continue
        # il valore arriva fino all'inizio del prossimo grassetto **di un campo**;
        # i grassetti che non sono campi restano dentro il valore, col loro testo
        fine = len(riga)
        for n in pezzi[i + 1:]:
            if _chiave_di(n.group("chiave")) is not None:
                fine = n.start()
                break
        valore = riga[m.end():fine]
        campi.append((campo, valore, m.group("chiave")))
    return campi


def _valore(campo, testo, chiave_grezza):
    """Il valore ripulito, con la forma giusta per il campo.

    Non tutti i campi si puliscono allo stesso modo, e la ragione sta nel documento:
    lo `Strato` e' scritto fra apici inversi (`` `S00` ``) e va tenuto come codice,
    l'`Attendibilita`' ha una lettera (`D`, `L+I`) e spesso una spiegazione fra
    parentesi, il `Periodo` ha dentro un inciso (`circa 3350 a.C. (personaggio
    mitico)`) che **resta**: e' informazione, non sporcoia.

    Il punto e virgola finale si toglie perche' e' il separatore dei tre campi della
    riga della fonte (`**Fonte:** X; **ricostruzione:** Y; **memoria:** Z.`): e' un
    segno di punteggiatura della riga, non parte del testo del campo. Il punto fermo
    invece si lascia quando e' dentro una sigla (`a.C.`), perche' li' fa parte della
    sigla e toglierlo farebbe `a.C` — che non e' piu' nessuna data.
    """
    t = testo.strip()
    if campo == "strato":
        m = re.search(r"`(S\d+)`", t)
        return m.group(1) if m else _pulisci(t).rstrip(". ")
    if campo == "attendibilita":
        m = re.search(r"`([A-Z](?:\+[A-Z])*)`", t)
        if not m:
            m = re.match(r"^([A-Z](?:\+[A-Z])*)\b", t)
        return m.group(1) if m else None
    if campo == "stato":
        # Il documento scrive tre forme: **`def`**, **`in formazione`** e, alla
        # Q303, `def` seguito da un corsetto di nota (*(ritorno: era la voce di
        # 4-7…)*). Gli apici inversi sono del testo del documento, non dello stato,
        # e senza toglierli il valore era "in formazione`", che non e' nessuno stato.
        # **L'ordine conta**: si taglia sul corsivo PRIMA di togliere gli apici, perche'
        # togliendoli prima l'apice di chiusura `in formazione`** diventerebbe una
        # stella e il taglio mangerebbe tutta la parola — il campo risultava nullo
        # su 9 schede su 30 senza che il sintomo dicesse perche'.
        # l'apertura `**` del valore viene dal grassetto del campo stesso e va tolta
        # prima del taglio: senza questo il testo parte da `**` e il taglio sul
        # corsivo non trova niente da tenere
        t = t.lstrip("*`").strip()
        t = re.split(r"\*", t)[0]
        t = t.replace("`", "")
        return t.strip().strip(".").strip().lower() or None
    if campo == "aggancio":
        # l'aggancio porta dentro il testo i rimandi fra apici inversi e le parentesi
        # citate: si tengono, ma il grassetto in eccesso e l'a capo vanno via
        return _pulisci(t).rstrip(". ")
    if campo == "forza":
        # `**Forte.**` e `**Medio,` perché la frase continua: la forza e' la parola,
        # non la frase, e il documento la chiude con un punto che qui e' rumore
        return _pulisci(t).strip(".").strip().lower() or None
    return _chiusura(_pulisci(t).rstrip("; "))


def _chiusura(testo):
    """Togli il punto finale, ma non quello che chiude una sigla.

    `circa 3350 a.C.` finisce in `a.C.`: togliere il punto darebbe `a.C`, che non e'
    piu' nessuna data. La regola e' semplice e si dichiara: si toglie il punto solo se
    il testo **non** finisce con una sigla, cioe' con una lettera preceduta da un
    punto (`a.C.`, `d.C.`, `v.C.`). Il punto e virgola invece si toglie sempre, perche'
    e' il separatore dei tre campi della riga della fonte.
    """
    t = testo.rstrip()
    if t.endswith(".") and not re.search(r"\.[A-Za-z]\.$", t):
        t = t[:-1].rstrip()
    return t


def _verifiche(nome_doc):
    """Le verifiche storiche della §12, per codice `Q`.

    La tabella ha una riga per voce con piu' codici (`Q112 / Q121 — Alcuino, Carlo
    Magno`): la verifica vale per tutti e due, e ogni scheda riceve la sua copia con
    il numero della voce, cosi' il rimando al documento resta leggibile.
    """
    path = os.path.join(DOCS, nome_doc)
    if not os.path.exists(path):
        return {}
    testo = open(path, encoding="utf-8").read()
    m = re.search(r"^##\s*12\.", testo, re.M)
    if not m:
        return {}
    fine = re.search(r"^##\s*13\.", testo[m.end():], re.M)
    sezione = testo[m.end():m.end() + fine.start()] if fine else testo[m.end():]
    out = {}
    for r in sezione.split("\n"):
        mv = VERIFICA_RIGA.match(r)
        if not mv:
            continue
        corpo = _pulisci(mv.group("voce"))
        domanda = _pulisci(mv.group("testo"))
        for codice in re.findall(r"Q\d+", corpo):
            out.setdefault(codice, []).append({
                "voce": "V" + mv.group("num"),
                "domanda": domanda,
                "dove": corpo,
            })
    return out


def _forze(nome_doc):
    """La colonna `Forza` della tabella delle tappe, per livello.

    Il secondo anno scrive la forza **soltanto** li`: la scheda di Q01 chiude con
    «**Forza: forte.**» e le altre ventinove non la hanno, mentre la tabella §4 ha la
    colonna per tutte e trenta. Leggere la forza dalle sole schede avrebbe dato una
    scheda su trenta evento trenta forze nulle — cioe' un dato falso, e il tipo di
    falso peggiore: sembrava che il documento non dicesse niente. La colonna si cerca
    **per intestazione** e non per numero, perche' il quinto anno ne ha una in piu' (la
    stanza) e l'anno 4 ne ha due (la porta): e' la regola che vale da `estrai_incontri`.
    """
    path = os.path.join(DOCS, nome_doc)
    if not os.path.exists(path):
        return {}
    righe = open(path, encoding="utf-8").read().split("\n")
    i = next((k for k, r in enumerate(righe) if r.startswith("| Livello |")), None)
    if i is None:
        return {}
    colonne = [c.strip() for c in righe[i].strip().strip("|").split("|")]
    if "Forza" not in colonne:
        return {}
    j = colonne.index("Forza")
    out = {}
    for r in righe[i + 2:]:
        if not r.startswith("|"):
            break
        celle = [c.strip() for c in r.strip().strip("|").split("|")]
        m = re.match(r"^\**(\d-\d+)\**$", celle[0] if celle else "")
        if not m or len(celle) != len(colonne):
            continue
        out[m.group(1)] = celle[j].strip().lower()
    return out


def _immagini():
    """Le due fonti delle immagini, tenute distinte perché hanno compiti diversi.

    `ritratti_disponibili.json` e' la **ricerca** (il file trovato su Commons con la
    sua licenza); `attestazione_immagini.json` e' il **giudizio a vista** (l'ho
    guardata, è la persona giusta, e con quale etichetta). Una scheda che ha solo la
    ricerca e non il giudizio non è un ritratto: e' un file con un nome che sembra
    giusto. Il file lo dice, e il campo `verifica_immagine` lo ripete per ogni scheda.
    """
    try:
        ricerca = {r["codice"]: r for r in json.load(open(RITRATTI, encoding="utf-8"))}
    except Exception:                                           # noqa: BLE001
        ricerca = {}
    try:
        giudizio = json.load(open(ATTESTAZIONE, encoding="utf-8"))
    except Exception:                                           # noqa: BLE001
        giudizio = {}
    return ricerca, giudizio


def leggi_anno(anno, per_tappa, verifiche, forze, ricerca, giudizio):
    """Le schede di un anno, con i campi che i documenti scrivono davvero."""
    nome = DOCUMENTI[anno]
    path = os.path.join(DOCS, nome)
    righe = open(path, encoding="utf-8").read().split("\n")

    schede, corrente = [], None
    for i, r in enumerate(righe):
        m = SCHEDA.match(r)
        if m:
            if corrente:
                schede.append(corrente)
            nome_scheda, didascalia, bandiere = _titolo(m.group("resto"))
            corrente = {
                "codice": m.group("codice"),
                "codice_stato": CODICE_STATO,
                "nome": nome_scheda,
                "didascalia": didascalia,
                "_bandiere": bandiere,
                "anno": anno,
                "scheda": "%s §5 (%s)" % (nome, m.group("codice")),
                "riga_documento": i + 1,
                "periodo": None, "luogo": None, "pin": None, "strato": None,
                "stato": None, "attendibilita": None, "domanda": None,
                "fonte_epoca": None, "ricostruzione": None,
                "memoria_successiva": None, "aggancio": None, "forza": None,
                "motto": None, "emblema": None,
                "aggiunta_dal_progetto": bool(bandiere.get("aggiunta")),
                "collettivo": bool(bandiere.get("collettivo")),
                "_destinazione": [],
            }
            continue
        if corrente is None:
            continue
        if not r.startswith("- "):
            # la scheda finisce alla prima riga che non e' un campo: una riga di testo
            # o un'altra intestazione
            if r.strip() and not r.startswith("#"):
                schede.append(corrente)
                corrente = None
            continue
        for campo, valore, chiave in _riga_campi(r):
            pulito = _valore(campo, valore, chiave)
            if pulito is None or pulito == "":
                continue
            if campo == "fonte_epoca" and corrente["fonte_epoca"] is None:
                corrente["fonte_epoca"] = pulito
            elif campo in ("ricostruzione", "memoria_successiva") \
                    and corrente[campo] is None:
                corrente[campo] = pulito
            elif campo in corrente and corrente[campo] is None:
                corrente[campo] = pulito
    if corrente:
        schede.append(corrente)

    problemi = []
    for s in schede:
        bandiere = s.pop("_bandiere")
        s["bandiere"] = bandiere

        # la destinazione: dove la persona incontra il giocatore. Si legge dagli
        # incontri, che sono il dato, e non dalle frasi della scheda.
        # Le tre prove, in ordine di forza decrescente. Ogni scheda porta **quale**
        # prova l'ha abbinata: un nome che coincide e' una cosa, un codice che
        # coincide e' un'altra, e confonderle e' il modo tipico di trasformare una
        # coincidenza in una scelta.
        def _abbina(altro):
            if not altro:
                return None
            if _norm(altro) == _norm(s["nome"]):
                return "nome_normalizzato"
            if _norm2(altro) == _norm2(s["nome"]):
                return "nome_senza_articoli"
            if _parziale(_norm(altro), _norm(s["nome"])):
                return "nome_parziale"
            return None

        for x in per_tappa:
            v = x["voce_obbligatoria"]
            if v.get("codice") == s["codice"]:
                s["_destinazione"].append({"livello": x["livello"],
                                          "ruolo": "obbligatorio",
                                          "prova": "codice"})
            else:
                prova = _abbina(v.get("nome"))
                if prova:
                    s["_destinazione"].append({"livello": x["livello"],
                                              "ruolo": "obbligatorio",
                                              "prova": prova})
            for f in x.get("facoltativi") or []:
                if f.get("codice") == s["codice"]:
                    s["_destinazione"].append({"livello": x["livello"],
                                              "ruolo": "facoltativo",
                                              "prova": "codice"})
                else:
                    prova = _abbina(f.get("nome"))
                    if prova:
                        s["_destinazione"].append({"livello": x["livello"],
                                                  "ruolo": "facoltativo",
                                                  "prova": prova})
        # la forza: prima dalla scheda, che la scrive solo una volta su trenta nel
        # secondo anno, e poi dalla tabella delle tappe, che la scrive per tutte.
        # Se le due dicono cose diverse e' un difetto del documento e si dichiara.
        forza_scheda = s.get("forza")
        s["forza"] = None
        s["forza_prova"] = None
        for d in s["_destinazione"]:
            if d["ruolo"] != "obbligatorio":
                continue
            dalla_tabella = forze.get(d["livello"])
            if forza_scheda and dalla_tabella and forza_scheda != dalla_tabella:
                problemi.append("%s: la scheda dice forza %s, la tabella %s dice %s"
                                % (s["codice"], forza_scheda, d["livello"], dalla_tabella))
            if forza_scheda:
                s["forza"] = forza_scheda
                s["forza_prova"] = "scheda"
            elif dalla_tabella:
                s["forza"] = dalla_tabella
                s["forza_prova"] = "tabella_tappe"
        # una scheda abbinata a due tappe non e' un abbinamento: e' un'ambiguita' e
        # va detta, non risolta scegliendo la prima
        livelli = [d["livello"] for d in s["_destinazione"] if d["ruolo"] == "obbligatorio"]
        if len(livelli) > 1:
            problemi.append("%s (%s): abbinata a piu' tappe obbligatorie %s"
                            % (s["codice"], s["nome"], ", ".join(livelli)))
        if not s["_destinazione"]:
            problemi.append("%s (%s): nessuna tappa la incontra" % (s["codice"], s["nome"]))

        # le verifiche storiche: vengono dalla §12 del documento, e portano il numero
        # della voce, cosi' chi legge sa dove andare a guardare
        s["verifiche"] = verifiche.get(s["codice"], [])

        # l'immagine: la ricerca e il giudizio sono due cose, e si dichiarano entrambe
        r = ricerca.get(s["codice"]) or {}
        g = giudizio.get(s["codice"]) or {}
        dettagli = r.get("dettagli") or {}
        if g:
            esito = g.get("esito")
            s["fonte_immagine"] = g.get("immagine")
            s["etichetta_immagine"] = g.get("etichetta")
            s["verifica_immagine"] = esito
            s["verifica_immagine_motivo"] = g.get("motivo")
            if esito == "accettata" and dettagli:
                s["licenza"] = dettagli.get("licenza")
                s["licenza_url"] = dettagli.get("url")
                s["autore"] = dettagli.get("autore")
            else:
                s["licenza"] = None
                s["licenza_url"] = None
                s["autore"] = None
        else:
            s["fonte_immagine"] = r.get("immagine")
            s["etichetta_immagine"] = r.get("etichetta")
            s["verifica_immagine"] = ("non_verificata_a_vista" if r.get("immagine")
                                      else "nessuna_immagine")
            s["verifica_immagine_motivo"] = (
                "la ricerca ha trovato il file %s, ma nessuno lo ha guardato: "
                "il nome di un file non e' una prova" % r.get("immagine")
                if r.get("immagine") else
                "la ricerca non ha trovato nessun file: la scheda usa l'emblema, "
                "come vuole la `AGENTS.md` §5")
            s["licenza"] = dettagli.get("licenza")
            s["licenza_url"] = dettagli.get("url")
            s["autore"] = dettagli.get("autore")

        # i campi che i documenti NON scrivono
        s["note_verifica"] = None
        s["note_verifica_motivo"] = (
            "i documenti non scrivono questo campo: la §12 porta le verifiche "
            "storiche nel campo `verifiche`, che e' un'altra cosa — la nota "
            "verifica e' cio' che resta da fare prima che la scheda sia completa")
    return schede, problemi


def _collettivi_dichiarati(anno):
    """Quanti collettivi il documento dell'anno dichiara, e dove lo dichiara.

    La regola del progetto e' che **un numero scritto a mano invecchia**: i documenti
    degli anni 3, 4 e 5 scrivono «In questo anno sono **N su 30**» e il secondo scrive
    «Sono 3 su 30» senza la formula. Il quinto anno e' quello che e' gia' stato corretto
    una volta perche' la frase contava a memoria invece di contare la tabella, ed e'
    esattamente il numero che va ricontrollato a ogni rigenerazione.
    """
    path = os.path.join(DOCS, DOCUMENTI[anno])
    testo = open(path, encoding="utf-8").read()
    m = (re.search(r"sono \*\*(\d+) su 30\*\*", testo)
         or re.search(r"[Ss]ono (\d+) su 30", testo))
    if not m:
        return None
    return int(m.group(1))


def main():
    prova = "--prova" in sys.argv
    if not os.path.exists(INCONTRI):
        raise SystemExit("esegui prima estrai_incontri.py")
    inc = json.load(open(INCONTRI, encoding="utf-8"))
    per_anno = {}
    for x in inc["incontri"]:
        per_anno.setdefault(x["anno"], []).append(x)
    ricerca, giudizio = _immagini()

    scritte = []
    for anno in sorted(DOCUMENTI):
        schede, problemi = leggi_anno(anno, per_anno.get(anno, []),
                                      _verifiche(DOCUMENTI[anno]),
                                      _forze(DOCUMENTI[anno]), ricerca, giudizio)
        obbl = sum(1 for s in schede
                   if any(d["ruolo"] == "obbligatorio" for d in s["_destinazione"]))
        faco = sum(1 for s in schede
                   if any(d["ruolo"] == "facoltativo" for d in s["_destinazione"]))
        # i campi vuoti: si contano e si dichiarano, perche' una scheda con un campo
        # vuoto e' una scheda incompleta e non una scheda senza quel campo
        vuoti = []
        for s in schede:
            mancanti = [k for k in ("periodo", "luogo", "pin", "strato",
                                    "attendibilita", "domanda", "fonte_epoca",
                                    "ricostruzione", "memoria_successiva",
                                    "aggancio", "motto", "emblema")
                        if not s.get(k)]
            s["campi_vuoti"] = mancanti
            if mancanti:
                vuoti.append("%s: %s" % (s["codice"], ", ".join(mancanti)))
        # l'anno 5 dichiara due campi in piu' (`stato` e `aggiunta`, §5): non sono
        # un campo mancante negli altri anni, e non si contano come vuoti
        for s in schede:
            if anno == 5 and not s.get("stato"):
                problemi.append("%s: stato mancante (l'anno 5 lo dichiara obbligatorio)"
                                % s["codice"])
        # il confronto con la cifra scritta nel documento: se il catalogo dice tre
        # collettivi e il testo ne dichiara due, il testo ha la ragione perche' e' stato
        # scritto prima che la terza voce diventasse collettiva — ma allora il testo va
        # corretto, e il difetto si vede subito invece di aspettare la prossima riga
        collettivi = sum(1 for s in schede if s["attendibilita"] == "C")
        dichiarati = _collettivi_dichiarati(anno)
        if dichiarati is not None and dichiarati != collettivi:
            problemi.append("il documento dichiara %d collettivi su 30, il catalogo ne "
                            "ha %d: la frase e la tabella non dicono la stessa cosa"
                            % (dichiarati, collettivi))
        out = {
            "versione": 1,
            "data": "2026-10-03",
            "anno": anno,
            "documento": DOCUMENTI[anno],
            "scopo": "le schede dei personaggi dell'anno %d, portate dai documenti "
                     "in dati/ senza aggiungere nulla" % anno,
            "come_si_legge": "per intestazione di sezione (`### Q117 ·`), non "
                             "contando le righe; e ogni riga si divide sui grassetti, "
                             "perche' i campi del primogruppo stanno tutti sulla stessa "
                             "riga",
            "avvertenza": "questo file **non completa** le schede, le raccoglie. Il "
                          "campo `note_verifica` resta a null con il motivo accanto, e "
                          "ogni scheda dichiara in `campi_vuoti` che cosa manca. Un "
                          "catalogo con campi vuoti dichiarati e' usabile; un "
                          "catalogo che non li dichiara mente",
            "avvertenza_immagine": "`fonte_immagine` viene da "
                                   "`sorgenti/art/ritratti_disponibili.json`, che e' "
                                   "una ricerca; il giudizio e' in "
                                   "`sorgenti/art/attestazione_immagini.json`. Una "
                                   "scheda con immagine e `verifica_immagine: "
                                   "non_verificata_a_vista` **non ha un ritratto "
                                   "certificato**: ha un file che sembra giusto",
            "codici": "%s: i codici Q sono proposti nei documenti, non confermati" %
                      CODICE_STATO,
            "schede": len(schede),
            "obbligatori": obbl,
            "facoltativi": faco,
            "senza_tappa": [s["codice"] for s in schede if not s["_destinazione"]],
            "collettivi": collettivi,
            "collettivi_dichiarati": _collettivi_dichiarati(anno),
            "campi_vuoti_totali": sum(len(s["campi_vuoti"]) for s in schede),
            "con_immagine": sum(1 for s in schede if s["fonte_immagine"]),
            "immagine_verificata": sum(1 for s in schede
                                       if s["verifica_immagine"] == "accettata"),
            "con_verifiche_storiche": sum(1 for s in schede if s["verifiche"]),
            "problemi": problemi + vuoti,
            "persone": [{k: v for k, v in s.items() if k != "_destinazione"} |
                        {"destinazione": s["_destinazione"]} for s in schede],
        }
        path = os.path.join(DATI, "videogioco-5-duchi-anno%d-personaggi.json" % anno)
        if not prova:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(out, f, ensure_ascii=False, indent=2)
                f.write("\n")
            scritte.append(path)
        print("anno %d: %d schede (%d obbligatorie, %d facoltative), %d campi vuoti, "
              "%d con immagine (%d verificate), %d con verifiche storiche, %d problemi"
              % (anno, out["schede"], out["obbligatori"], out["facoltativi"],
                 out["campi_vuoti_totali"], out["con_immagine"],
                 out["immagine_verificata"], out["con_verifiche_storiche"],
                 len(problemi) + len(vuoti)))
        for s in (problemi + vuoti)[:5]:
            print("    " + s)
        if len(problemi) + len(vuoti) > 5:
            print("    ... e altre %d" % (len(problemi) + len(vuoti) - 5))
    if prova:
        print("--prova: non scrivo")
        return 0
    for p in scritte:
        print("scritto %s" % os.path.relpath(p, RADICE))
    return 0


if __name__ == "__main__":
    sys.exit(main())