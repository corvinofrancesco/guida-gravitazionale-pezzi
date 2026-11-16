#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Controlla i file CSV di dati/ e riassume i valori utili alla guida gravitazionale.

- Errori STRUTTURALI (colonne mancanti, numeri non validi, stato sconosciuto):
  exit code 1.
- Anomalie rispetto alla norma FIDE (ordine delle altezze, tolleranza del 10%,
  rapporto base/altezza 40-50%): solo segnalate, NON fanno fallire. Sono un
  risultato dei dati, non un errore del file.

Solo libreria standard. Esecuzione:  python3 dati/verifica_dati.py [-v]
"""

import csv
import os
import sys
from collections import defaultdict

AQUI = os.path.dirname(os.path.abspath(__file__))

STATI = {"norma", "dichiarato", "stimato_foto", "misurato"}
PEZZI = ["re", "regina", "alfiere", "cavallo", "torre", "pedone"]
FIDE_NOMINALE = {"re": 95, "regina": 85, "alfiere": 70, "cavallo": 60, "torre": 55, "pedone": 50}
TOLLERANZA = 0.10
RAPPORTO_BASE = (0.40, 0.50)

COL_TORNEO = ["modello", "pezzo", "colore", "altezza_mm", "base_mm", "collo_mm", "collare_mm",
              "testa_mm", "peso_g", "baricentro_mm", "stato", "incertezza_mm", "fonte", "data", "note"]
COL_NUMERICHE = ["altezza_mm", "base_mm", "collo_mm", "collare_mm", "testa_mm", "peso_g",
                 "baricentro_mm", "incertezza_mm"]
COL_GIGANTI = ["modello", "pezzo", "altezza_cm", "base_cm", "casa_scacchiera_cm", "stato", "fonte", "data", "note"]
COL_IMBALLI = ["modello", "colli", "dimensioni_cm_per_collo", "peso_kg_totale", "fonte", "data", "note"]

errori = []
note = []


def leggi(nome, colonne):
    path = os.path.join(AQUI, nome)
    with open(path, newline="", encoding="utf-8") as f:
        r = csv.DictReader(f)
        if r.fieldnames != colonne:
            errori.append("%s: colonne attese %s, trovate %s" % (nome, colonne, r.fieldnames))
            return []
        righe = []
        for n, riga in enumerate(r, start=2):
            if None in riga or None in riga.values():
                errori.append("%s riga %d: numero di campi errato" % (nome, n))
                continue
            riga["_n"] = n
            righe.append(riga)
        return righe


def numero(riga, col, nome):
    v = riga[col].strip()
    if v == "":
        return None
    try:
        return float(v)
    except ValueError:
        errori.append("%s riga %d: %s non numerico: %r" % (nome, riga["_n"], col, v))
        return None


def controlla_torneo():
    nome = "misure_pezzi_torneo.csv"
    righe = leggi(nome, COL_TORNEO)
    sets = defaultdict(dict)
    for r in righe:
        if r["pezzo"] not in PEZZI:
            errori.append("%s riga %d: pezzo sconosciuto %r" % (nome, r["_n"], r["pezzo"]))
            continue
        if r["stato"] not in STATI:
            errori.append("%s riga %d: stato sconosciuto %r" % (nome, r["_n"], r["stato"]))
        vals = {c: numero(r, c, nome) for c in COL_NUMERICHE}
        r["_v"] = vals
        if r["stato"] != "norma":
            sets[(r["modello"], r["colore"])][r["pezzo"]] = vals

    anomalie = []
    for (modello, colore), pezzi in sets.items():
        etichetta = modello + (" [%s]" % colore if colore else "")
        # ordine delle altezze
        alt = [(p, pezzi[p]["altezza_mm"]) for p in PEZZI if p in pezzi and pezzi[p]["altezza_mm"]]
        for (p1, h1), (p2, h2) in zip(alt, alt[1:]):
            if h1 <= h2:
                anomalie.append("%s: ordine FIDE violato (%s %g <= %s %g)" % (etichetta, p1, h1, p2, h2))
        for p, v in pezzi.items():
            h, b = v["altezza_mm"], v["base_mm"]
            if h is not None:
                nom = FIDE_NOMINALE[p]
                if abs(h - nom) / nom > TOLLERANZA + 1e-9:
                    anomalie.append("%s: %s %g mm fuori dal +-10%% del nominale (%d)" % (etichetta, p, h, nom))
            if h and b:
                rap = b / h
                if not (RAPPORTO_BASE[0] <= rap <= RAPPORTO_BASE[1]):
                    note.append("%s: %s base/altezza = %.0f%% (FIDE 40-50%%)" % (etichetta, p, rap * 100))
    return righe, anomalie


def riassunto(righe):
    print("\nIntervalli nei set 'dichiarato' (mm):")
    print("%-9s %-14s %-14s" % ("pezzo", "altezza", "base"))
    for p in PEZZI:
        h = [r["_v"]["altezza_mm"] for r in righe
             if r["pezzo"] == p and r["stato"] == "dichiarato" and r["_v"]["altezza_mm"]]
        b = [r["_v"]["base_mm"] for r in righe
             if r["pezzo"] == p and r["stato"] == "dichiarato" and r["_v"]["base_mm"]]
        fh = "%g-%g (n=%d)" % (min(h), max(h), len(h)) if h else "-"
        fb = "%g-%g (n=%d)" % (min(b), max(b), len(b)) if b else "-"
        print("%-9s %-14s %-14s" % (p, fh, fb))
    print("\nStime da foto (set utente):")
    for r in righe:
        if r["stato"] == "stimato_foto":
            v = r["_v"]
            campi = ["%s=%g" % (c.replace("_mm", ""), v[c]) for c in
                     ["altezza_mm", "base_mm", "collo_mm", "collare_mm", "testa_mm"] if v[c] is not None]
            print("  %-8s %s (+-%s mm)" % (r["pezzo"], ", ".join(campi) if campi else "nessun valore affidabile",
                                          r["incertezza_mm"] or "?"))


def controlla_giganti():
    nome = "misure_pezzi_giganti.csv"
    for r in leggi(nome, COL_GIGANTI):
        if r["pezzo"] not in PEZZI:
            errori.append("%s riga %d: pezzo sconosciuto %r" % (nome, r["_n"], r["pezzo"]))
        if r["stato"] not in STATI:
            errori.append("%s riga %d: stato sconosciuto %r" % (nome, r["_n"], r["stato"]))
        for c in ("altezza_cm", "base_cm"):
            numero(r, c, nome)
    nome = "imballi_giganti.csv"
    for r in leggi(nome, COL_IMBALLI):
        numero(r, "colli", nome)
        numero(r, "peso_kg_totale", nome)


def main():
    righe, anomalie = controlla_torneo()
    controlla_giganti()
    if errori:
        print("ERRORI STRUTTURALI:")
        for e in errori:
            print("  -", e)
        return 1
    riassunto(righe)
    print("\nAnomalie rispetto alla norma FIDE (informative):")
    for a in anomalie or ["nessuna"]:
        print("  -", a)
    print("\nRapporto base/altezza fuori da 40-50%% (informativo, %d casi; dettagli con -v)" % len(note))
    if "-v" in sys.argv:
        for n in note:
            print("  -", n)
    print("\nOK: struttura dei file valida.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
