"""Prova che `verifica_disegni.py` morda, con difetti iniettati uno alla volta.

Un controllo che non si e' mai visto sbagliare non e' un controllo: e' un
documento che dice «tutto va bene». Qui si rompono le cose apposta, una per una,
si pretende che il verificatore se ne accorga e poi si rimette tutto com'era.

**La prova scrive sul file vero e lo rimette subito**, come
`prova_difetto_immagini.py`: una prova che rompesse una copia starebbe
provando un file che nessuno legge. Il backup vive fuori dal progetto.

`cerca` e' il numero del controllo che **deve** comparire fra le righe che il
difetto produce: senza, la prova guarderebbe la prima riga dell'output, che
puo' essere quella di un controllo diverso, e una prova che guarda la riga
sbagliata verde e non sa niente.

I difetti sono sei e coprono i quattro controlli:

  E1  un file promesso e non scritto            -> D1
  E2  un file che c'e' ma non e' un PNG        -> D1
  E3  una misura dichiarata diversa dalla vera  -> D2
  E4  due livelli con lo stesso disegno         -> D3
  E6  il file si annuncia come un PNG e non lo e' -> D4
  E5  una tappa dell'anno 1 senza disegno       -> D1

L'ordine e' quello in cui il codice li inietta, e non quello dei numeri perche'
**E6 ed E5 sono gia' etichette del progetro**: in `anno1-ferrara.md` segnano le
epoche di Ferrara (E5 Studio, E6 pontificia). Rinumerarli qui non romperebbe
nessun riferimento — nessuno cita queste lettere della prova — ma due E5 che
volgono dire cose diverse nello stesso progetto costano piu' di una numerazione
disordinata. La prova li inietta nell'ordine del codice, e li dichiara tutti e sei:
una prova che ne dichiara cinque e ne inietta sei e' una prova che mente sul
proprio conto, ed e' la prima cosa che va letta quando si cerca di capire se ha
guardato tutto.

Uso:  python3 sorgenti/art/prova_difetto_disegni.py
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(BASE, "sorgenti", "art", "out", "ambienti")
INDICE = os.path.join(OUT, "indice.json")
VERIFICA = os.path.join(BASE, "sorgenti", "art", "verifica_disegni.py")


def gira():
    r = subprocess.run([sys.executable, VERIFICA], capture_output=True,
                       text=True)
    return r.returncode, r.stdout


def leggi():
    return json.load(open(INDICE, encoding="utf-8"))


def scrivi(ind):
    with open(INDICE, "w", encoding="utf-8") as f:
        json.dump(ind, f, ensure_ascii=False, indent=1)


def main():
    codice, testo = gira()
    if codice != 0:
        raise SystemExit("il verificatore non e' verde prima di cominciare:\n"
                         + testo)
    print("prima della prova: verde")

    backup = tempfile.mkdtemp(prefix="prova_disegni_")
    copia_indice = os.path.join(backup, "indice.json")
    shutil.copy(INDICE, copia_indice)
    # Le copie dei PNG che E4 tocca: senza, la prova romperebbe il file vero e
    # non lo rimetterebbe, e un difetto che lascia il progetto rotto non e' una
    # prova di niente.
    copie, creati = {}, []
    provati = []

    def rimetti():
        shutil.copy(copia_indice, INDICE)
        for nome, percorso in copie.items():
            shutil.copy(percorso, os.path.join(OUT, nome))
        for percorso in creati:
            if os.path.exists(percorso):
                os.remove(percorso)

    def inietta(nome, cosa, cerca):
        ind = leggi()
        cosa(ind)
        scrivi(ind)
        provati.append((nome, gira(), cerca))
        rimetti()

    def inietta_su(nome, che_cosa, cerca):
        """Un difetto che sta sui PNG e non sull'indice."""
        che_cosa()
        provati.append((nome, gira(), cerca))
        rimetti()

    # E1: promesso e non scritto.
    def e1(ind):
        ind["disegnati"][3]["file"] = \
            "sorgenti/art/out/ambienti/non_esiste_mai.png"
    inietta("E1 il file promesso non c'e'", e1, "D1")

    # E2: il file c'e' ma non e' un PNG.
    def e2(ind):
        fasullo = os.path.join(OUT, "non_un_png.png")
        with open(fasullo, "wb") as f:
            f.write(b"questo file ha un nome che sembra un PNG e non lo e'")
        ind["disegnati"][5]["file"] = \
            "sorgenti/art/out/ambienti/non_un_png.png"
        # il file e' **stato creato** dalla prova: va cancellato, non rimesso
        creati.append(fasullo)
    inietta("E2 il file non e' un PNG", e2, "D1")

    # E3: la misura dichiarata non e' quella del PNG.
    def e3(ind):
        larghezza, altezza = ind["disegnati"][7]["px"]
        ind["disegnati"][7]["px"] = [larghezza + 2, altezza]
    inietta("E3 la misura dichiarata non e' quella del PNG", e3, "D2")

    # E4: due livelli con lo stesso disegno. Si copia davvero il primo PNG sul
    # nome del secondo: il difetto vero e' che il generatore produce due
    # immagini uguali e non se ne accorge, non che l'indice sbaglia una riga.
    def e4(ind):
        from png_terrarium import misura_png
        a, b = ind["disegnati"][10], ind["disegnati"][11]
        src = os.path.join(BASE, a["file"])
        dst = os.path.join(BASE, b["file"])
        # La copia di sicurezza e' del file che verrà **sovrascritto**, non di
        # quello da cui si copia: rimettere il primo sul secondo lascia due
        # file identici, cioe' il difetto che si voleva provare.
        sicuro = os.path.join(backup, os.path.basename(b["file"]))
        shutil.copy(dst, sicuro)
        shutil.copy(src, dst)
        with open(src, "rb") as f:
            w, h = misura_png(f.read())
        b["px"] = [w, h]
        copie[os.path.basename(b["file"])] = sicuro
    sys.path.insert(0, os.path.join(BASE, "sorgenti", "gis"))
    inietta("E4 due livelli con lo stesso disegno", e4, "D3")

    # E6: il file si annuncia come un'immagine e non lo e'. Il PNG di prima
    # versione aveva l'intestazione RGB e un byte per pixel: D1 e D2 lo
    # accettavano, perche' guardano l'intestazione, e solo la decodifica lo
    # smaschera. Il difetto che questo controllo e' nato per morire.
    def e6(ind):
        fasullo = os.path.join(OUT, "annunciato_solo.png")
        import struct as _s, zlib as _z
        w, h = 8, 4
        righe = b"".join(b"\x00" + b"\x07" * w for _ in range(h))
        def blocco(tipo, dati):
            return (_s.pack(">I", len(dati)) + tipo + dati
                    + _s.pack(">I", __import__("zlib").crc32(tipo + dati)
                              & 0xffffffff))
        con = (b"\x89PNG\r\n\x1a\n"
               + blocco(b"IHDR", _s.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
               + blocco(b"IDAT", _z.compress(righe, 9)) + blocco(b"IEND", b""))
        with open(fasullo, "wb") as f:
            f.write(con)
        ind["disegnati"][9]["file"] = \
            "sorgenti/art/out/ambienti/annunciato_solo.png"
        ind["disegnati"][9]["px"] = [w, h]
        creati.append(fasullo)
    inietta("E6 il file si annuncia come un PNG e non lo e'", e6, "D4")

    # E5: una tappa dell'anno 1 non ha piu' il suo disegno.
    def e5(ind):
        tolto = ind["disegnati"][2]["livello"]
        ind["disegnati"] = [x for x in ind["disegnati"]
                            if x["livello"] != tolto]
    inietta("E5 una tappa dell'anno 1 senza disegno", e5, "D1")

    # e adesso deve tornare verde
    rimetti()
    codice, testo = gira()
    if codice != 0:
        raise SystemExit("dopo la prova il verificatore non e' tornato verde:\n"
                         + testo)
    print("dopo la prova: verde\n")

    visti, non = 0, 0
    for nome, (codice, testo), cerca in provati:
        righe = [r for r in testo.splitlines() if r.strip().startswith(cerca)]
        if codice != 0 and righe:
            visti += 1
            print("  visto   %-40s %s" % (nome, righe[0].strip()[:60]))
        else:
            non += 1
            print("  NON VISTO %-39s codice %d, righe %s: %d"
                  % (nome, codice, cerca, len(righe)))

    print("\ndifetti iniettati: %d, visti: %d, non visti: %d"
          % (len(provati), visti, non))
    return 1 if non else 0


if __name__ == "__main__":
    sys.exit(main())