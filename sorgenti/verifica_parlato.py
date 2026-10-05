"""Verifica che la parte orale del gioco sia dichiarata con i numeri giusti.

Il documento `videogioco-5-duchi-parlato.md` porta un numero per lingua, e quel
numero viene da una ricerca che cambia nel tempo: Commons cresce, e un domani il
ferrarese potrebbe avere trenta registrazioni. Un numero scritto a mano nella
tabella del documento è quindi una fotografia che invecchia, e il controllo che
manca è quello che dice se la fotografia e' ancora quella.

Quattro controlli, e quattro difetti iniettati che devono vedere tutti (morroni):

  A1  il documento porta, per ogni lingua, il numero che il dato conta
  A2  ogni lingua è dichiarata una volta sola: sei righe, sei lingue
  A3  la Web Speech API e' esclusa **per la ragione giusta** (manda l'audio fuori),
      e non per una vaghezza
  A4  nessun livello della parte orale promette il riconoscimento della voce:
      quello che il gioco non sa fare si dichiara, non si simula

Uso:  python3 sorgenti/verifica_parlato.py
      python3 sorgenti/verifica_parlato.py --difetti    # ne inietta quattro, uno per volta
"""
import contextlib
import io
import json
import os
import re
import sys

RADICE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOC = os.path.join(RADICE, "docs", "videogioco-5-duchi-parlato.md")
DATI = os.path.join(RADICE, "dati", "lingue", "audio_disponibili.json")
LINGUE_DOC = os.path.join(RADICE, "docs", "videogioco-5-duchi-lingue.md")

def esito(problemi, etichetta, ok, messaggio):
    """Il verbale di un controllo: dice anche **chi** ha parlato.

    Senza l'etichetta la prova del difetto saprebbe che qualcosa e' andato
    storto e non saprebbe quale dei quattro controlli lo ha visto: una prova
    che non distingue e' una prova che non prova.
    """
    print("  " + ("OK  " if ok else "KO  ") + etichetta + "  " + messaggio)
    if not ok:
        problemi.append("%s  %s" % (etichetta, messaggio))


def numero_italiano(n):
    return "{:,}".format(n).replace(",", " ")


def controlla(doc, dati, lingue):
    """I quattro controlli sulla parte orale.

    I tre input arrivano dalla chiamata e non sono letti qui: e'
    quello che permette alla prova di far girare gli stessi
    controlli su copie rotte, senza toccare i documenti veri.
    """
    problemi = []
    # ------------------------------------------------------------- A1
    print("== A1. il documento porta il numero che il dato conta ==")
    per_voce = dati["lingue"]
    for r in per_voce:
        n = r["registrazioni"]
        if r["esito"] != "contato":
            esito(problemi, "A1", False, "%s: il dato e' '%s' e il documento non puo' dichiararlo"
                  % (r["nome"], r["esito"]))
            continue
        scritto = numero_italiano(n)
        # il numero del documento porta il separatore delle migliaia o la parola
        # «zero»: i due modi sono entrambi accettati perche' il documento e'
        # scritto per essere letto
        trovato = (scritto in doc) or (n == 0 and re.search(
            r"\|\s*\*\*0\*\*", doc) is not None and re.search(
            r"\*\*" + re.escape(r["nome"].split()[0].lower()) + r"\*\*", doc) is not None)
        esito(problemi, "A1", trovato, "%-26s %s" % (r["nome"], scritto))

    # ------------------------------------------------------------- A2
    print("\n== A2. sei lingue, sei righe, nessuna due volte ==")
    # la tabella di 2.3: sei righe di lingua. Si prendono per il primo campo
    # grassetto, non per il secondo: il secondo porta il numero in forme diverse
    # («89 381», «**0**, e non è un buco») e un formato che cambia è un formato che
    # si rompe.
    sezione = doc[doc.index("### 2.3"):doc.index("## 3.")] if "### 2.3" in doc else ""
    righe = re.findall(r"^\| \*\*([^*]+)\*\* \|", sezione, re.M)
    nomi = righe
    esito(problemi, "A2", len(righe) == 6, "la tabella delle lingue ha %d righe, non 6" % len(righe))
    esito(problemi, "A2", len(set(nomi)) == len(nomi), "nessuna lingua e' dichiarata due volte")
    lingue_codici = {r["lingua"] for r in dati["lingue"]}
    esito(problemi, "A2", len(lingue_codici) == 6, "il dato copre %d lingue" % len(lingue_codici))

    # ------------------------------------------------------------- A3
    print("\n== A3. la Web Speech API e' esclusa per la ragione giusta ==")
    sez = doc[doc.index("### 2.2"):doc.index("### 2.3")] if "### 2.2" in doc else ""
    esito(problemi, "A3", "server di Google" in sez,
          "la sezione 2.2 dice che Chrome manda l'audio ai server di Google")
    esito(problemi, "A3", "non funziona offline" in sez,
          "la sezione 2.2 dice che non funziona offline")
    esito(problemi, "A3", "esclusa" in sez, "la sezione 2.2 dichiara l'esclusione e non la evita")

    # ------------------------------------------------------------- A4
    print("\n== A4. nessun livello promette il riconoscimento della voce ==")
    # i cinque livelli: il quinto e' quello dichiarato non fatto
    livelli = re.findall(r"^### (L\d) ", doc, re.M)
    esito(problemi, "A4", livelli == ["L1", "L2", "L3", "L4", "L5"],
          "i livelli sono %s" % ", ".join(livelli))
    sez5 = doc[doc.index("### L5"):doc.index("## 4.")] if "### L5" in doc else ""
    esito(problemi, "A4", "non fatto" in sez5, "L5 e' dichiarato come non fatto")
    esito(problemi, "A4", "deve poter funzionare **senza** L5" in sez5,
          "il gioco deve funzionare anche se L5 non arriva mai")
    # anche il titolo conta: un livello chiamato «Riconoscimento automatico:
    # funziona» promette il riconoscimento, per quanto sia vago il corpo
    titolo = re.search(r"^### L5 .*$", doc, re.M)
    esito(problemi, "A4", titolo is not None and "non fatto" in titolo.group(0),
          "il titolo di L5 dichiara che non e' fatto")
    # la parte scritta non cambia: nessuna componente nuova, nessuna famiglia nuova
    lingue = open(LINGUE_DOC, encoding="utf-8").read()
    esito(problemi, "A4", "| # | Componente" in lingue and "| 9 |" in lingue,
          "lingue.md resta a nove componenti: la parte orale non ne aggiunge una")
    if "famiglie di esercizi" in doc:
        esito(problemi, "A4", "non è un sistema a sé" in doc,
              "il documento dichiara che la parte orale non e' un sistema separato")

    return problemi


def main():
    sola_prova = "--difetti" in sys.argv
    doc = open(DOC, encoding="utf-8").read()
    dati = json.load(open(DATI, encoding="utf-8"))
    lingue = open(LINGUE_DOC, encoding="utf-8").read()
    if sola_prova:
        return difetti(doc, dati, lingue)
    problemi = controlla(doc, dati, lingue)
    print("\n" + "=" * 62)
    if problemi:
        print("PROBLEMI: %d" % len(problemi))
        for p in problemi:
            print("  - " + p)
        return 1
    print("nessun difetto: la parte orale e' dichiarata con i numeri del dato, e "
          "quello che il gioco non sa fare resta dichiarato")
    return 0



def inietta(doc, dati, etichetta):
    """Un difetto alla volta, su copie. Il documento vero non si tocca mai.

    Ogni difetto e' scelto per essere uno che i documenti potrebbero
    davvero avere: un numero che invecchia, una riga che sparisce, una frase
    che qualcuno riformula, un livello che si chiama in un modo diverso.
    """
    d = doc
    if etichetta == "A1":
        # il dato conosce una lingua che il documento non porta: il numero che
        # il dato conta non c'e' nel documento, ed e' esattamente la
        # fotografia che invecchia
        dati = json.loads(json.dumps(dati))
        dati["lingue"].append({"nome": "Klingon", "lingua": "tlh", "esito":
                               "contato", "registrazioni": 123456})
        return d, dati, None
    if etichetta == "A2":
        # una riga della tabella delle lingue sparisce: cinque righe, non sei.
        # **la riga va tolta dalla sezione 2.3**, perche' e' li' che A2 guarda:
        # togliere la prima riga `| **...** |` del documento lascerebbe A2 con
        # sei righe come prima, e il difetto iniettato non cambierebbe niente.
        if "### 2.3" not in d or "## 3." not in d:
            return None, None, None
        sezione = d[d.index("### 2.3"):d.index("## 3.")]
        righe = re.findall(r"(?m)^\| \*\*[^*]+\*\* \|.*$", sezione)
        if not righe:
            return None, None, None
        return d.replace(righe[0] + "\n", "", 1), None, None
    if etichetta == "A3":
        # la sezione 2.2 perde la ragione dell'esclusione e la chiama cosi'
        for frase in ("server di Google", "non funziona offline"):
            if frase in d:
                return d.replace(frase, "una precisione", 1), None, None
        return None, None, None
    if etichetta == "A4":
        # il livello che il gioco non sa fare si chiama come se lo sapesse.
        # **il titolo va riscritto per intero**: quello vero contiene gia'
        # «non fatto», e aggiungere una promessa davanti a quelle parole
        # lascerebbe A4 verde su un titolo che promette il riconoscimento.
        titolo = re.search(r"(?m)^### L5 .*$", d)
        if titolo is None:
            return None, None, None
        nuovo_titolo = "### L5 Riconoscimento automatico della voce: funziona"
        return d[:titolo.start()] + nuovo_titolo + d[titolo.end():], None, None
    if etichetta == "A1":
        # il dato conosce una lingua che il documento non porta: il numero che
        # il dato conta non c'e' nel documento, ed e' esattamente la
        # fotografia che invecchia
        dati = json.loads(json.dumps(dati))
        dati["lingue"].append({"nome": "Klingon", "lingua": "tlh", "esito":
                               "contato", "registrazioni": 123456})
        return d, dati, None
    if etichetta == "A2":
        # una riga della tabella delle lingue sparisce: cinque righe, non sei
        righe = re.findall(r"(?m)^\| \*\*[^*]+\*\* \|.*$", d)
        if not righe:
            return None, None, None
        return d.replace(righe[0] + "\n", "", 1), None, None
    if etichetta == "A3":
        # la sezione 2.2 perde la ragione dell'esclusione e la chiama cosi'
        for frase in ("server di Google", "non funziona offline"):
            if frase in d:
                return d.replace(frase, "una precisione", 1), None, None
        return None, None, None
    if etichetta == "A4":
        # il livello che il gioco non sa fare si chiama come se lo sapesse:
        # il titolo promette il riconoscimento della voce
        if "### L5 " not in d:
            return None, None, None
        return d.replace("### L5 ", "### L5 Riconoscimento automatico: funziona",
                         1), None, None
    raise ValueError(etichetta)


def difetti(doc, dati, lingue):
    """Prova che i quattro controlli vedano un difetto ciascuno."""
    print("== i difetti iniettati")
    iniettati = 0
    visti = 0
    for etichetta in ("A1", "A2", "A3", "A4"):
        alterato, dati_alterati, lingue_alterate = inietta(doc, dati, etichetta)
        if alterato is None:
            print("   NON INIETTATO  %s: il documento non ha la riga su cui "
                  "intervenire" % etichetta)
            continue
        iniettati += 1
        fuori = io.StringIO()
        with contextlib.redirect_stdout(fuori):
            problemi = controlla(alterato,
                                 dati_alterati if dati_alterati else dati,
                                 lingue_alterate if lingue_alterate else lingue)
        trovati = [p for p in problemi if p.startswith(etichetta + " ")]
        if trovati:
            visti += 1
            for p in trovati:
                print("   visto   %s" % p[:100])
        else:
            print("   NON VISTO  %s" % etichetta)
    print("\ndifetti iniettati: %d, visti: %d, non visti: %d"
          % (iniettati, visti, iniettati - visti))
    return 0 if visti == iniettati else 1


if __name__ == "__main__":
    sys.exit(main())