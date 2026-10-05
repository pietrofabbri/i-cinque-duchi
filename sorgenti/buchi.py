# -*- coding: utf-8 -*-
"""I buchi conosciuti del progetto, letti da un file solo.

Fino al 5 ottobre 2026 i buchi conosciuti vivevano in tre dizionari, in tre
file: `TACITI` in `verifica_prove.py`, `SENZA` e `SENZA_APPOGGIO` in
`verifica_numeri.py`. Un registro in tre posti non è un registro: cercarlo
costa tre ricerche, e quando ne nasce uno in uno solo degli elenchi nessuno lo
vede.

Ora l'unico posto dove si scrive è `dati/buchi_aperto.json`, e questo modulo è
l'unico modo di leggerlo. I tre dizionari non sono più scritti a mano: sono
costruiti da qui. È la differenza fra un registro e tre elenchi, ed è
verificabile — se un controllo volesse dichiarare un buco fuori dal file,
`verifica_buchi.py` lo direbbe, perché il conto del registro non cambierebbe.

`elenco(nome)` restituisce il dizionario `{chiave: motivo}` di uno dei tre
elenchi, e solleva se l'elenco non esiste: un elenco che sparisce dal registro
non può diventare un elenco che non viene più letto.
"""
import io
import json
import os

RADICE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTRO = os.path.join(RADICE, "dati", "buchi_aperto.json")

# I tre elenchi che il registro può contenere. Un quarto non si può inventare:
# un elenco che esiste solo in uno script è un registro che è tornato a essere
# tre elenchi.
ELENCHI = ("TACITI", "SENZA", "SENZA_APPOGGIO")


def leggi():
    """Il registro, letto da disco."""
    with io.open(REGISTRO, encoding="utf-8") as f:
        return json.load(f)


def elenco(nome):
    """Il dizionario `{chiave: motivo}` di un elenco del registro."""
    if nome not in ELENCHI:
        raise ValueError("%s non è un elenco del registro: %s"
                         % (nome, ", ".join(ELENCHI)))
    dentro = {}
    for b in leggi().get("buchi", []):
        if b.get("elenco") == nome:
            dentro[b["chiave"]] = b.get("motivo", "")
    return dentro
