#!/usr/bin/env python3
"""Registra una nuova versione di un documento di `docs/`, in un colpo solo.

Una modifica a un documento richiede quattro gesti, e dimenticarne uno e' il
difetto piu' comune del progetto (`verifica_registri.py` e
`verifica_coerenza.py` esistono per accorgersene):

  1. alzare la versione nell'intestazione YAML e aggiornare la data;
  2. scrivere la riga nel registro delle modifiche, **nel formato che quel
     registro usa gia'** (tabella, elenco o intestazioni) e **nel suo verso**
     (piu' recente in alto o in basso);
  3. aggiornare la versione nella tabella dei documenti del `README.md`;
  4. aggiornare i rimandi «`videogioco-5-duchi-X.md (vN.N)`» in tutti gli altri
     documenti, nel README e in AGENTS.md.

Il quarto gesto **non** alza la versione dei documenti che contengono il
rimando: un rimando aggiornato non cambia quello che il documento dice, e
alzarne la versione produceva una catena di versioni vuote (decisione del
06/10/2026, scritta in `AGENTS.md` §4).

Uso:
    python3 sorgenti/nuova_versione.py docs/videogioco-5-duchi-gioco.md "Che cosa e' cambiato e perche'."
    python3 sorgenti/nuova_versione.py --data 06/10/2026 docs/... "..."
    python3 sorgenti/nuova_versione.py --prova     # esegue le prove sui tre formati e su un registro assente

Un documento senza registro ne riceve uno, in tabella, in fondo.
"""
import datetime
import io
import os
import re
import sys
import tempfile

RADICE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(RADICE, "docs")

RIGA_TAB = re.compile(r"^\| (\d\d/\d\d/\d{4}) \| (\d+\.\d+) \|.*$", re.M)
RIGA_ELENCO = re.compile(r"^- \*\*v(\d+\.\d+) \((\d\d/\d\d/\d{4})\)\*\*.*$", re.M)
RIGA_INTEST = re.compile(r"^(#{2,3}) v(\d+\.\d+) [—-] .*$", re.M)
SEZIONE_REGISTRO = re.compile(r"^## [^\n]*[Rr]egistro[^\n]*$", re.M)


def leggi(p):
    with io.open(p, encoding="utf-8") as f:
        return f.read()


def scrivi(p, testo):
    with io.open(p, "w", encoding="utf-8") as f:
        f.write(testo)


def chiave(v):
    a, b = v.split(".")
    return (int(a), int(b))


def successiva(v):
    a, b = v.split(".")
    return "%s.%d" % (a, int(b) + 1)


def una_riga(messaggio):
    """Una cella di tabella non puo' contenere un a capo o una barra verticale."""
    return " ".join(messaggio.split()).replace("|", "/")


def registra(testo, nuova, data, messaggio):
    """Il testo del documento con la riga nuova nel registro."""
    m = list(SEZIONE_REGISTRO.finditer(testo))
    if not m:
        numeri = [int(x) for x in re.findall(r"^## (\d+)[.\s]", testo, re.M)]
        n = (max(numeri) + 1) if numeri else 1
        return (testo.rstrip("\n") + "\n\n## %d. Registro delle modifiche\n\n"
                "| Data | Versione | Che cosa è cambiato |\n|---|---|---|\n"
                "| %s | %s | %s |\n" % (n, data, nuova, una_riga(messaggio)))
    inizio = m[-1].end()
    corpo = testo[inizio:]

    tab = list(RIGA_TAB.finditer(corpo))
    elenco = list(RIGA_ELENCO.finditer(corpo))
    intest = list(RIGA_INTEST.finditer(corpo))
    # il formato e' quello della prima riga del registro
    candidati = [(r[0].start(), nome, r) for nome, r in
                 (("tab", tab), ("elenco", elenco), ("intest", intest)) if r]
    if not candidati:
        raise SystemExit("il registro c'e' ma non ha righe riconoscibili: "
                         "scrivi la riga a mano")
    candidati.sort(key=lambda t: t[0])
    _, formato, righe = candidati[0]

    def versione_di(r):
        return r.group(2) if formato == "tab" else (
            r.group(1) if formato == "elenco" else r.group(2))

    recente_in_alto = chiave(versione_di(righe[0])) >= chiave(versione_di(righe[-1]))

    if formato == "tab":
        nuova_riga = "| %s | %s | %s |" % (data, nuova, una_riga(messaggio))
        if recente_in_alto:
            pos = righe[0].start()
            corpo = corpo[:pos] + nuova_riga + "\n" + corpo[pos:]
        else:
            pos = righe[-1].end()
            corpo = corpo[:pos] + "\n" + nuova_riga + corpo[pos:]
    elif formato == "elenco":
        nuova_riga = "- **v%s (%s)**: %s" % (nuova, data, " ".join(messaggio.split()))
        if recente_in_alto:
            pos = righe[0].start()
            corpo = corpo[:pos] + nuova_riga + "\n\n" + corpo[pos:]
        else:
            # dopo l'ultima voce: fino alla prossima riga vuota seguita da non-rientro
            coda = corpo[righe[-1].start():]
            fine = re.search(r"\n(?=\n|\Z)", coda)
            pos = righe[-1].start() + (fine.start() if fine else len(coda))
            corpo = corpo[:pos] + "\n\n" + nuova_riga + corpo[pos:]
    else:
        livello = righe[0].group(1)
        blocco = "%s v%s — %s\n\n%s\n" % (livello, nuova, data, messaggio.strip())
        if recente_in_alto:
            pos = righe[0].start()
            corpo = corpo[:pos] + blocco + "\n" + corpo[pos:]
        else:
            corpo = corpo.rstrip("\n") + "\n\n" + blocco
    return testo[:inizio] + corpo


def nuova_versione(percorso, messaggio, data, radice=RADICE):
    nome = os.path.basename(percorso)
    testo = leggi(percorso)
    m = re.search(r"^versione:\s*(\S+)\s*$", testo, re.M)
    if not m:
        raise SystemExit("%s: nessuna versione nell'intestazione" % nome)
    vecchia = m.group(1)
    nuova = successiva(vecchia)
    testo = testo[:m.start(1)] + nuova + testo[m.end(1):]
    iso = "%s-%s-%s" % (data[6:], data[3:5], data[:2])
    testo = re.sub(r"^data:\s*\S+\s*$", "data: " + iso, testo, count=1, flags=re.M)
    testo = registra(testo, nuova, data, messaggio)
    scrivi(percorso, testo)

    # README: la cella della versione nella riga del documento
    readme = os.path.join(radice, "README.md")
    if os.path.exists(readme):
        r = leggi(readme)
        riga = re.compile(r"^(\|[^\n]*`%s`[^\n]*\| *)%s( *\|)$" % (re.escape(nome), re.escape(vecchia)), re.M)
        r2, n = riga.subn(r"\g<1>%s\g<2>" % nuova, r)
        if n:
            scrivi(readme, r2)

    # i rimandi, ovunque, senza alzare la versione di chi li contiene
    citanti = [os.path.join(radice, "docs", f) for f in os.listdir(os.path.join(radice, "docs"))
               if f.endswith(".md")]
    citanti += [os.path.join(radice, f) for f in ("README.md", "AGENTS.md", "FONTI-E-LICENZE.md")]
    rimando = re.compile(r"(%s\s*\()v%s(\))" % (re.escape(nome), re.escape(vecchia)))
    corto = re.compile(r"(`%s`\s*\()v%s(\))" % (re.escape(nome.replace("videogioco-5-duchi-", "")),
                                                re.escape(vecchia)))
    toccati = []
    for c in citanti:
        if not os.path.exists(c):
            continue
        t = leggi(c)
        t2 = rimando.sub(r"\g<1>v%s\g<2>" % nuova, t)
        t2 = corto.sub(r"\g<1>v%s\g<2>" % nuova, t2)
        if t2 != t:
            scrivi(c, t2)
            toccati.append(os.path.relpath(c, radice))
    return vecchia, nuova, toccati


# ---------------------------------------------------------------- prove
PROVE = {
    "tab_in_alto": ("---\nversione: 0.3\ndata: 2026-10-01\n---\n# T\n\n## 9. Registro delle modifiche\n\n"
                    "| Data | Versione | Che cosa è cambiato |\n|---|---|---|\n"
                    "| 02/10/2026 | 0.3 | c |\n| 01/10/2026 | 0.2 | b |\n| 01/10/2026 | 0.1 | a |\n"),
    "tab_in_basso": ("---\nversione: 0.2\ndata: 2026-10-01\n---\n# T\n\n## 4. Registro modifiche\n\n"
                     "| Data | Versione | Modifica |\n|---|---|---|\n"
                     "| 01/10/2026 | 0.1 | a |\n| 02/10/2026 | 0.2 | b |\n"),
    "elenco_in_alto": ("---\nversione: 0.2\ndata: 2026-10-01\n---\n# T\n\n## 5. Registro modifiche\n\n"
                       "- **v0.2 (02/10/2026)**: b\n\n- **v0.1 (01/10/2026)**: a\n"),
    "elenco_in_basso": ("---\nversione: 0.2\ndata: 2026-10-01\n---\n# T\n\n## 5. Registro modifiche\n\n"
                        "- **v0.1 (01/10/2026)**: a\n  - dettaglio\n- **v0.2 (02/10/2026)**: b\n  - dettaglio\n"),
    "intestazioni": ("---\nversione: 0.5\ndata: 2026-10-01\n---\n# T\n\n## 7. Il registro delle modifiche\n\n"
                     "### v0.5 — 04/10/2026\n\nquinta\n\n### v0.4 — 03/10/2026\n\nquarta\n"),
    "senza_registro": "---\nversione: 0.1\ndata: 2026-09-27\n---\n# T\n\n## 3. Fonti\n\nniente\n",
}


def prova():
    sbagli = 0
    with tempfile.TemporaryDirectory() as d:
        os.makedirs(os.path.join(d, "docs"))
        scrivi(os.path.join(d, "README.md"), "")
        for nome, testo in PROVE.items():
            p = os.path.join(d, "docs", "videogioco-5-duchi-%s.md" % nome)
            scrivi(p, testo)
            nuova_versione(p, "nuova riga", "06/10/2026", radice=d)
            t = leggi(p)
            v = re.search(r"^versione:\s*(\S+)", t, re.M).group(1)
            ok = ("06/10/2026" in t and "nuova riga" in t and "data: 2026-10-06" in t
                  and v in t.split("Registro")[-1] + t.split("registro")[-1])
            # il verso: la riga nuova sta in cima se il registro e' in alto, in fondo se in basso
            reg = t[t.lower().rfind("registro"):]
            pos_nuova = reg.find("nuova riga")
            altre = [reg.find(x) for x in ("| a |", "| b |", "| c |", ": a", ": b", "\nquinta", "\nquarta") if reg.find(x) >= 0]
            if "in_alto" in nome or nome == "intestazioni":
                ok = ok and all(pos_nuova < a for a in altre)
            elif "in_basso" in nome:
                ok = ok and all(pos_nuova > a for a in altre)
            print("  %-16s %s  v%s" % (nome, "ok" if ok else "SBAGLIATO", v))
            sbagli += 0 if ok else 1
    print("prove: %d, sbagliate: %d" % (len(PROVE), sbagli))
    return 1 if sbagli else 0


def main(argv):
    if "--prova" in argv:
        return prova()
    data = datetime.date.today().strftime("%d/%m/%Y")
    if "--data" in argv:
        i = argv.index("--data")
        data = argv[i + 1]
        del argv[i:i + 2]
    if len(argv) != 3:
        print(__doc__)
        return 2
    percorso, messaggio = argv[1], argv[2]
    vecchia, nuova, toccati = nuova_versione(os.path.abspath(percorso), messaggio, data)
    print("%s: v%s -> v%s" % (os.path.basename(percorso), vecchia, nuova))
    for t in toccati:
        print("  rimando aggiornato in %s" % t)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
