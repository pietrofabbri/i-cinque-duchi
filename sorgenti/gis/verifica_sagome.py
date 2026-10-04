#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Controlla le sagome degli edifici: che siano sagome e non un loro ricordo.

`dati/edifici_footprint.json` è il file che ha chiuso il buco più grande dei
cinque di `fonti-visive.md` §3.2, e il 4 ottobre 2026 si è scoperto che **non
conteneva sagome**. Il generatore scriveva `round(x / Q)` con `Q = 100` su
coordinate già in metri: ogni vertice finiva arrotondato a zero. Il file
risultante aveva 5209 record, tutti con un conteggio, un'area in metri quadri e
un'altezza, e una forma che era un segno di pochi centimetri — la più grande, in
tutti i 52 luoghi, misurava cinque centimetri.

Il difetto è invisibile per costruzione: **il numero è giusto**. Il documento
dichiara «5209 sagome su 54 luoghi», il riepilogo del file dichiara 5209, il
conteggio torna, e la geometria non c'è. Non è recuperabile, perché l'arrotondamento
l'ha distrutta prima che qualcuno la guardasse: nessun controllo del progetto leggeva
un vertice.

Tre controlli, e il secondo è quello che vale.

  S1  **ogni forma dice la stessa area che il record dichiara.** Il record porta
      `area_m2`, che è calcolata dalla geometria prima dell'arrotondamento, e
      porta `forma`, che è la stessa geometria dopo. Se le due non tornano, una
      delle due è falsa, e il file non sa quale: va detto. Il confronto è
      dell'ingombro della forma in metri quadri contro `area_m2`, e tollera il
      fattore due, che è quanto può cambiare un tracciato semplificato.

  S2  **nessuna sagoma è degenere.** Un edificio con area sopra i 100 metri
      quadri non può stare in una sagoma di pochi centimetri. È il controllo che
      avrebbe visto il difetto: non confronta niente con niente, guarda la
      sagoma e chiede che esista.

  S3  **ogni record dice da dove viene la sua altezza**, e l'altezza assente non
      viene stimata: è la regola di `fonti-visive.md` §4.3, e senza di lei il
      motore farebbe un cubo alto a caso.

Uso:  python3 sorgenti/gis/verifica_sagome.py
"""
import json
import os
import sys

RADICE = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))))
SAGOME = os.path.join(RADICE, "dati", "edifici_footprint.json")

# L'ingombro in metri quadri si legge dalla forma in centimeti: il `formato` del
# file dichiara «coordinate locali in metri dal pin, quantizzate a 1/100 m», e i
# valori sono interi. La costante e' dichiarata qui e non presa dal file da
# controllare: se la prendessi da li', il controllo direbbe che il file e' giusto
# perche' il file lo dice.
CM = 100.0
# Fattore due: la semplificazione sposta i vertici e l'area puo' cambiare di un
# po'. Sotto la meta' o sopra il doppio, le due non stanno parlando della stessa
# figura.
TOLLERANZA = (0.5, 2.0)
# Sotto questa area un edificio non viene tenuto dal generatore, quindi non puo'
# avere una sagoma degenere senza che il difetto sia un altro.
AREA_MINIMA = 100.0
# Un ingombro minore di questo e' una sagoma che non si vede: un metro.
INGOMBRO_MINIMO_M = 1.0
ORIGINI_ALTEZZA = {"osm_height", "osm_levels", "assente"}


def ingombro(forma):
    """L'area in metri quadri racchiusa dalla forma, in centimeti."""
    punti = [(x / CM, y / CM) for x, y in forma]
    if len(punti) < 3:
        return 0.0
    s = 0.0
    for i in range(len(punti)):
        x1, y1 = punti[i]
        x2, y2 = punti[(i + 1) % len(punti)]
        s += x1 * y2 - x2 * y1
    return abs(s) / 2.0


def main(numera=False):
    if not os.path.exists(SAGOME):
        print("non trovo %s" % os.path.relpath(SAGOME, RADICE))
        return 1
    doc = json.load(open(SAGOME, encoding="utf-8"))
    edifici = doc["edifici"]

    problemi = []
    ingombrati, degeneri, falsi = [], [], []

    for e in edifici:
        forma = e.get("forma") or []
        area_dichiarata = e.get("area_m2")
        nome = e.get("nome") or e["id"]

        if not forma:
            degeneri.append(nome)
            problemi.append("S2 %s (%s): la forma e' vuota e il record dichiara "
                           "%.1f m2" % (nome, e["luogo"], area_dichiarata or 0))
            continue
        # S2 viene prima di S1 e, quando una sagoma e' degenere, S1 non parla:
        # il confronto con l'area aggiungerebbe la stessa accusa detta in un
        # altro modo, e un controllo che ripete se stesso non fa leggere meglio
        # un difetto.

        a = ingombro(forma)
        ingombrati.append(a)

        xs = [x / CM for x, _ in forma]
        ys = [y / CM for _, y in forma]
        larghezza = max(xs) - min(xs)
        altezza = max(ys) - min(ys)

        # S2: la sagoma deve esistere. Un edificio da 1728 metri quadri che sta
        # in mezzo metro non e' un edificio piccolo, e' una sagoma perduta.
        if max(larghezza, altezza) < INGOMBRO_MINIMO_M:
            degeneri.append(nome)
            problemi.append(
                "S2 %s (%s): la sagoma e' degenere, %.2f x %.2f m, e il record "
                "dichiara %.1f m2" % (nome, e["luogo"], larghezza, altezza,
                                      area_dichiarata or 0))
            continue

        # S1: la forma e l'area devono parlare della stessa figura.
        if area_dichiarata:
            basso, alto = TOLLERANZA
            if not (basso * area_dichiarata <= a <= alto * area_dichiarata):
                falsi.append(nome)
                problemi.append(
                    "S1 %s (%s): la forma racchiude %.1f m2 e il record dichiara "
                    "%.1f m2: la geometria e' stata persa" % (nome, e["luogo"],
                                                              a, area_dichiarata))

        # S3: l'altezza dichiara la sua fonte, e «assente» resta assente.
        fonte = e.get("fonte_altezza")
        if fonte not in ORIGINI_ALTEZZA:
            problemi.append("S3 %s (%s): `fonte_altezza` e' %r, che non e' una "
                           "delle tre dichiarate" % (nome, e["luogo"], fonte))
        elif fonte == "assente" and e.get("altezza_m") is not None:
            problemi.append("S3 %s (%s): dice che l'altezza e' assente e porta "
                           "%s metri" % (nome, e["luogo"], e.get("altezza_m")))

    if numera:
        print("edifici                : %d su %d luoghi"
              % (len(edifici), len(doc.get("luoghi", []))))
        print("  con sagoma degenere  : %d" % len(degeneri))
        print("  forma contro area    : %d non tornano" % len(falsi))
        if ingombrati:
            print("  ingombro massimo     : %.1f m2" % max(ingombrati))
            print("  ingombro medio       : %.1f m2"
                  % (sum(ingombrati) / len(ingombrati)))
        per_orig = {}
        for e in edifici:
            per_orig[e.get("fonte_altezza")] = per_orig.get(
                e.get("fonte_altezza"), 0) + 1
        for k in sorted(per_orig, key=lambda x: str(x)):
            print("  %-22s: %d" % (k, per_orig[k]))

    if problemi:
        print("PROBLEMI: %d" % len(problemi))
        for p in problemi[:40]:
            print("   " + p)
        if len(problemi) > 40:
            print("   ... e altri %d" % (len(problemi) - 40))
        return 1
    print("sagome: nessun problema")
    return 0


if __name__ == "__main__":
    sys.exit(main(numera="--enumero" in sys.argv))
