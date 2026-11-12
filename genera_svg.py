#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generatore sagome SVG 1:1 per il prototipo in cartone:
"Guida gravitazionale per pezzi degli scacchi".

- Output in scala reale 1:1 (1 unita utente SVG = 1 mm).
- Un file multi-pagina compatibile Inkscape (pagine affiancate) + un file
  per ogni foglio A4 (stampa universale a 100%).
- Legenda linee:
    continuo           -> taglio
    tratteggiato       -> piega
    tratto-punto       -> riferimento di allineamento / registro
    retino arancio     -> zona da incollare (linguetta)

Nessuna dipendenza esterna: solo libreria standard.
Esecuzione:  python3 genera_svg.py
"""

import os
import math
import xml.dom.minidom as minidom

# ---------------------------------------------------------------- costanti
A4_W, A4_H = 210.0, 297.0
MARGIN = 8.0
CONTENT_X0 = MARGIN
CONTENT_Y0 = 32.0                      # sotto l'intestazione (titolo + scala)
CONTENT_W = A4_W - 2 * MARGIN          # 194
CONTENT_H = (A4_H - MARGIN) - CONTENT_Y0  # 257
GAP = 7.0                             # spazio fra le parti nel packing

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "svg")

# ---------------------------------------------------------------- CONFIG (misure in mm)
# Tutte le misure chiave del prototipo stanno qui: per sperimentare si cambia SOLO
# questo blocco e si rilancia il generatore (python3 genera_svg.py).
# Unita': millimetri, salvo dove indicato (gradi). I builder leggono da CONFIG.
CONFIG = {
    # --- Modulo A: imbuto -------------------------------------------------
    "imbuto": {
        "bocca_lunga": 140.0,      # apertura superiore, lato lungo (pareti A1)
        "bocca_corta": 110.0,      # apertura superiore, lato corto (pareti A3)
        "uscita": 60.0,            # uscita a paratia aperta (quadrata)
        "altezza": 90.0,           # altezza dell'imbuto
    },
    "paratia_A5": {
        "larghezza": 64.0,         # larghezza del corpo della paratia
        "altezza": 92.0,           # altezza del corpo (senza maniglia)
        "maniglia_larghezza": 28.0,
        "maniglia_altezza": 14.0,
        # Aperture libere marcate sulla sagoma (tacche). La paratia entra dall'asola
        # di A6: la tacca allineata al bordo dell'uscita (lato inserimento) da' l'apertura.
        "aperture": (30.0, 40.0, 50.0, 55.0),
        "apertura_iniziale": 35.0,  # taratura di partenza suggerita (README §8), fra le tacche 30 e 40
    },
    # Pezzo piu' ingombrante da non bloccare: il re (base) -- vedi verifica a calcolo.
    "re": {
        "base_diametro": 50.0,
        "gioco_minimo": 2.0,       # luce minima ammessa fra re e bordo dell'apertura
    },
    "guida_paratia_A6": {
        "lunghezza": 70.0,
        "altezza": 14.0,
        "linguetta": 10.0,
    },
    # --- Modulo B: rampa + raddrizzatore -----------------------------------
    "rampa": {
        "larghezza": 120.0,        # piano B1
        "lunghezza": 180.0,        # piano B1 (e lunghezza utile di B2/B3)
        "parete_altezza": 45.0,    # pareti laterali B2
        "parete_linguetta": 12.0,
        "guida_base_altezza": 16.0,   # guide inferiori B3
        "guida_base_linguetta": 10.0,
        "canale": (30.0, 34.0, 38.0),  # larghezze di canale previste (B3 e C2)
        "combi_distanza_da_asse": 26.0,  # posizione dei combi B4 sul piano
    },
    "combo_B4": {
        "lunghezza": 140.0,
        "altezza_ingresso": 60.0,  # altezza guida curva all'ingresso
        "altezza_uscita": 22.0,    # altezza guida curva all'uscita
        "linguetta": 12.0,
    },
    "striscia_B5": {
        "lunghezza": 150.0,
        "altezza": 42.0,
    },
    "gamba_B6": {
        "altezze": (48.0, 65.0, 84.0),   # gradini per 15 / 20 / 25 gradi
        "gradino": 24.0,                 # larghezza di ogni gradino
        "linguetta": 12.0,
    },
    "base_BP1": {
        "larghezza": 140.0,
        "lunghezza": 190.0,
    },
    # --- Modulo C: uscita ---------------------------------------------------
    "uscita_C": {
        "larghezza": 60.0,         # piano C1
        "lunghezza": 110.0,        # piano C1
        "guida_lunghezza": 110.0,  # guide C2
        "guida_altezza": 22.0,
        "guida_linguetta": 10.0,
    },
}

# ---------------------------------------------------------------- stili
S_CUT   = "fill:none;stroke:#111111;stroke-width:0.4;stroke-linejoin:round;stroke-linecap:round"
S_FOLD  = "fill:none;stroke:#1565c0;stroke-width:0.3;stroke-dasharray:3,2"
S_ALIGN = "fill:none;stroke:#c62828;stroke-width:0.28;stroke-dasharray:4,1.2,0.8,1.2"
S_GLUEF = "fill:url(#hatch);stroke:none"
S_FRAME = "fill:none;stroke:#bbbbbb;stroke-width:0.2"
S_DIM   = "fill:none;stroke:#444444;stroke-width:0.25"
T_CODE  = "font-family:Helvetica,Arial,sans-serif;font-weight:bold;fill:#111111"
T_TXT   = "font-family:Helvetica,Arial,sans-serif;fill:#111111"
T_RED   = "font-family:Helvetica,Arial,sans-serif;fill:#c62828"
T_BLUE  = "font-family:Helvetica,Arial,sans-serif;fill:#1565c0"
T_GREY  = "font-family:Helvetica,Arial,sans-serif;fill:#666666"


# ---------------------------------------------------------------- primitive SVG (stringhe)
def _f(v):
    return ("%.2f" % v).rstrip("0").rstrip(".") if isinstance(v, float) else str(v)


def line(x1, y1, x2, y2, style=S_CUT):
    return '<line x1="%s" y1="%s" x2="%s" y2="%s" style="%s"/>' % (_f(x1), _f(y1), _f(x2), _f(y2), style)


def rect(x, y, w, h, style=S_CUT, rx=0):
    r = ' rx="%s"' % _f(rx) if rx else ""
    return '<rect x="%s" y="%s" width="%s" height="%s"%s style="%s"/>' % (_f(x), _f(y), _f(w), _f(h), r, style)


def poly(points, style=S_CUT, closed=True):
    pts = " ".join("%s,%s" % (_f(p[0]), _f(p[1])) for p in points)
    tag = "polygon" if closed else "polyline"
    return '<%s points="%s" style="%s"/>' % (tag, pts, style)


def path(d, style=S_CUT):
    return '<path d="%s" style="%s"/>' % (d, style)


def text(x, y, s, size=3.0, anchor="start", style=T_TXT):
    s = (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
    return '<text x="%s" y="%s" style="%s;font-size:%spx" text-anchor="%s">%s</text>' % (
        _f(x), _f(y), style, _f(size), anchor, s)


def arrow(x, y, dx, dy, label="", style=S_CUT, tsize=2.6):
    """Freccia corta da (x,y) lunga (dx,dy) con eventuale etichetta a fine."""
    x2, y2 = x + dx, y + dy
    ang = math.atan2(dy, dx)
    a = 2.2
    left = (x2 - a * math.cos(ang - 0.4), y2 - a * math.sin(ang - 0.4))
    right = (x2 - a * math.cos(ang + 0.4), y2 - a * math.sin(ang + 0.4))
    out = [line(x, y, x2, y2, style),
           poly([(x2, y2), left, right], style="fill:#111;stroke:none")]
    if label:
        out.append(text(x2 + 1.5 * math.cos(ang), y2 + 1.5 * math.sin(ang) + 1.0, label, tsize, style=T_TXT))
    return out


def glue_tab(x, y, w, h, side="bottom"):
    """Linguetta da incollare: retino + bordi di taglio su 3 lati, piega sul lato 'side'."""
    out = [rect(x, y, w, h, S_GLUEF)]  # retino
    # bordi di taglio (tutti tranne il lato di piega) + piega tratteggiata
    edges = {
        "top":    [("fold", x, y, x + w, y), ("cut", x, y, x, y + h), ("cut", x + w, y, x + w, y + h), ("cut", x, y + h, x + w, y + h)],
        "bottom": [("fold", x, y + h, x + w, y + h), ("cut", x, y, x + w, y), ("cut", x, y, x, y + h), ("cut", x + w, y, x + w, y + h)],
        "left":   [("fold", x, y, x, y + h), ("cut", x, y, x + w, y), ("cut", x + w, y, x + w, y + h), ("cut", x, y + h, x + w, y + h)],
        "right":  [("fold", x + w, y, x + w, y + h), ("cut", x, y, x + w, y), ("cut", x, y, x, y + h), ("cut", x, y + h, x + w, y + h)],
    }[side]
    for kind, x1, y1, x2, y2 in edges:
        out.append(line(x1, y1, x2, y2, S_FOLD if kind == "fold" else S_CUT))
    return out


def dim_h(x1, x2, y, label, above=True):
    """Quota orizzontale con frecce e testo."""
    out = [line(x1, y, x2, y, S_DIM),
           line(x1, y - 1.5, x1, y + 1.5, S_DIM),
           line(x2, y - 1.5, x2, y + 1.5, S_DIM)]
    ty = y - 1.4 if above else y + 3.2
    out.append(text((x1 + x2) / 2, ty, label, 2.6, "middle", T_GREY))
    return out


def dim_v(x, y1, y2, label, right=True):
    out = [line(x, y1, x, y2, S_DIM),
           line(x - 1.5, y1, x + 1.5, y1, S_DIM),
           line(x - 1.5, y2, x + 1.5, y2, S_DIM)]
    tx = x + 1.6 if right else x - 1.6
    anc = "start" if right else "end"
    out.append(text(tx, (y1 + y2) / 2, label, 2.6, anc, T_GREY))
    return out


# ---------------------------------------------------------------- struttura "parte"
class Part:
    def __init__(self, code, name, qty, material, w, h):
        self.code = code
        self.name = name
        self.qty = qty
        self.material = material
        self.w = w
        self.h = h
        self.elems = []

    def add(self, *els):
        for e in els:
            if isinstance(e, list):
                self.elems.extend(e)
            else:
                self.elems.append(e)

    def label(self, extra=""):
        """Blocco etichetta in alto a sinistra (occupa i primi 11 mm della bbox)."""
        self.add(text(0, 3.4, self.code, 4.4, style=T_CODE))
        self.add(text(0, 6.8, self.name, 2.8, style=T_TXT))
        if self.qty > 1:
            self.add(text(len(self.name) * 1.55 + 3, 6.8, "(RITAGLIARNE %d)" % self.qty, 2.8,
                          style="font-family:Helvetica,Arial,sans-serif;font-weight:bold;fill:#c62828"))
        else:
            self.add(text(len(self.name) * 1.55 + 3, 6.8, "(1 pezzo)", 2.6, style=T_GREY))
        self.add(text(0, 9.6, "Materiale: %s%s" % (self.material, ("  -  " + extra if extra else "")), 2.5, style=T_GREY))


LBL = 11.0  # altezza riservata all'etichetta in cima a ogni parte


# ---------------------------------------------------------------- builder parti
def wall_rect(code, name, qty, material, W, H, tab=12.0, verso="", refs=None, notes=None):
    """Parete/strip rettangolare con linguetta di incollaggio in basso."""
    p = Part(code, name, qty, material, W, LBL + H + tab)
    top = LBL
    p.add(rect(0, top, W, H, S_CUT))
    p.label()
    if verso:
        p.add(arrow(W * 0.5 - 12, top + H * 0.5, 24, 0, verso, S_ALIGN))
    # linee di riferimento verticali (per posizionare altre parti su un piano)
    if refs:
        for rx, lab in refs:
            p.add(line(rx, top, rx, top + H, S_ALIGN))
            p.add(text(rx, top - 0.8, lab, 2.3, "middle", T_RED))
    if notes:
        for (nx, ny, s) in notes:
            p.add(text(nx, top + ny, s, 2.4, style=T_TXT))
    # linguetta
    p.add(glue_tab(0, top + H, W, tab, "top"))
    p.add(text(W / 2, top + H + tab - 2.0, "INCOLLARE / NASTRO", 2.3, "middle", T_GREY))
    return p


def trapezoid_wall(code, name, qty, material, T, B, slant, note=""):
    """Parete trapezoidale dell'imbuto (si uniscono con nastro)."""
    W = max(T, B)
    p = Part(code, name, qty, material, W, LBL + slant)
    top = LBL
    xTL = (W - T) / 2.0
    xBL = (W - B) / 2.0
    pts = [(xTL, top), (xTL + T, top), (xBL + B, top + slant), (xBL, top + slant)]
    p.add(poly(pts, S_CUT))
    p.label()
    # tacche di allineamento sulla mezzeria (per incollare dritto)
    p.add(line(W / 2, top, W / 2, top + 5, S_ALIGN))
    p.add(line(W / 2, top + slant - 5, W / 2, top + slant, S_ALIGN))
    p.add(text(W / 2, top + 4.0, "ALTO (bordo superiore largo)", 2.4, "middle", T_TXT))
    p.add(text(W / 2, top + slant - 1.6, "uscita " + _f(B) + " mm", 2.4, "middle", T_TXT))
    # zone nastro sui lati obliqui
    if note:
        p.add(text(W / 2, top + slant / 2, note, 2.4, "middle", T_GREY))
    return p


def gate_part():
    """Paratia regolabile dell'imbuto, con maniglia."""
    g = CONFIG["paratia_A5"]
    W, H, hand_w, hand_h = g["larghezza"], g["altezza"], g["maniglia_larghezza"], g["maniglia_altezza"]
    p = Part("A5", "Paratia regolabile", 1, "cartone ondulato", W, LBL + H + hand_h)
    top = LBL
    # maniglia + corpo come un unico profilo chiuso
    hx = (W - hand_w) / 2
    pts = [(hx, top), (hx, top), (hx + hand_w, top),
           (hx + hand_w, top + hand_h), (W, top + hand_h),
           (W, top + hand_h + H), (0, top + hand_h + H), (0, top + hand_h), (hx, top + hand_h)]
    p.add(poly(pts, S_CUT))
    p.label()
    p.add(text(W / 2, top + hand_h / 2 + 1, "presa", 2.4, "middle", T_GREY))
    p.add(text(W / 2, top + hand_h + H / 2, "si sfila per", 2.6, "middle", T_TXT))
    p.add(text(W / 2, top + hand_h + H / 2 + 4, "regolare l'uscita", 2.6, "middle", T_TXT))
    # tacche di apertura: distanza dalla punta = uscita imbuto - apertura libera
    bottom = top + hand_h + H
    uscita = CONFIG["imbuto"]["uscita"]
    p.add(text(W / 2, bottom - 58, "TACCHE = apertura libera (mm)", 2.4, "middle", T_RED))
    p.add(text(W / 2, bottom - 54.6, "allinea la tacca al bordo A6", 2.2, "middle", T_GREY))
    for ap in CONFIG["paratia_A5"]["aperture"]:
        y = bottom - (uscita - ap)
        p.add(line(0, y, W, y, S_ALIGN))
        etichetta = "%s mm" % _f(ap)
        if ap >= CONFIG["re"]["base_diametro"] + CONFIG["re"]["gioco_minimo"]:
            etichetta += "  (passa il re)"
        p.add(text(W - 2, y - 1.0, etichetta, 2.4, "end", T_RED))
    return p


def comb_part():
    """Sostegno (combo) della guida curva: trapezio rettangolo alto all'ingresso,
    basso all'uscita; linguetta di base; linea di ritaglio alternativa per cambiare la curva."""
    c = CONFIG["combo_B4"]
    L = c["lunghezza"]
    HE, HX = c["altezza_ingresso"], c["altezza_uscita"]
    tab = c["linguetta"]
    p = Part("B4", "Combo guida curva", 2, "cartone ondulato", L, LBL + HE + tab)
    top = LBL
    bottom = top + HE
    pts = [(0, top), (L, top + (HE - HX)), (L, bottom), (0, bottom)]
    p.add(poly(pts, S_CUT))
    p.label()
    # linea di ritaglio alternativa (curva piu dolce) tratto-punto
    d = "M 0 %s C %s %s, %s %s, %s %s" % (_f(top + 8), _f(L * 0.4), _f(top + 10),
                                          _f(L * 0.7), _f(top + (HE - HX) - 6), _f(L), _f(top + (HE - HX) + 2))
    p.add(path(d, S_ALIGN))
    p.add(text(4, top + 6, "ingresso (alto)", 2.4, style=T_TXT))
    p.add(text(L - 4, top + (HE - HX) + 5, "uscita (basso)", 2.4, "end", style=T_TXT))
    p.add(text(L * 0.5, top + 20, "- - -  profilo alternativo: ritaglia qui per curva piu dolce", 2.3, "middle", T_RED))
    p.add(arrow(10, bottom - 4, 26, 0, "verso valle", S_ALIGN))
    p.add(glue_tab(0, bottom, L, tab, "top"))
    p.add(text(L / 2, bottom + tab - 2, "piega + incolla sul fianco della rampa", 2.3, "middle", T_GREY))
    return p


def strip_part():
    """Striscia della guida curva in cartoncino sottile (si curva ad arco)."""
    W, H = CONFIG["striscia_B5"]["lunghezza"], CONFIG["striscia_B5"]["altezza"]
    p = Part("B5", "Striscia guida curva", 1, "cartoncino sottile", W, LBL + H)
    top = LBL
    p.add(rect(0, top, W, H, S_CUT))
    p.label()
    p.add(line(0, top + H / 2, W, top + H / 2, S_ALIGN))
    p.add(text(W / 2, top + H / 2 - 1.2, "linea di flessione - curvare ad arco (concavita in basso)", 2.4, "middle", T_RED))
    p.add(text(W / 2, top + H - 2.5, "appoggia e fissa sul bordo superiore dei due combi B4", 2.4, "middle", T_GREY))
    return p


def prop_part():
    """Gamba d'inclinazione a gradini (15/20/25 gradi) con piede."""
    g = CONFIG["gamba_B6"]
    H1, H2, H3 = g["altezze"]
    d = g["gradino"]
    tab = g["linguetta"]
    W = 3 * d
    p = Part("B6", "Gamba inclinazione", 2, "cartone ondulato (2-3 strati)", W, LBL + H3 + tab)
    top = LBL
    bottom = top + H3
    pts = [(0, bottom - H1), (d, bottom - H1), (d, bottom - H2),
           (2 * d, bottom - H2), (2 * d, bottom - H3), (3 * d, bottom - H3),
           (3 * d, bottom), (0, bottom)]
    p.add(poly(pts, S_CUT))
    p.label()
    p.add(text(d / 2, bottom - H1 + 4, "15", 3.0, "middle", T_TXT))
    p.add(text(d / 2, bottom - H1 + 7, "gradi", 2.1, "middle", T_GREY))
    p.add(text(d + d / 2, bottom - H2 + 4, "20", 3.0, "middle", T_TXT))
    p.add(text(d + d / 2, bottom - H2 + 7, "gradi", 2.1, "middle", T_GREY))
    p.add(text(2 * d + d / 2, bottom - H3 + 4, "25", 3.0, "middle", T_TXT))
    p.add(text(2 * d + d / 2, bottom - H3 + 7, "gradi", 2.1, "middle", T_GREY))
    p.add(text(W / 2, bottom - 3, "la rampa appoggia su un gradino", 2.3, "middle", T_GREY))
    p.add(glue_tab(0, bottom, W, tab, "top"))
    return p


def ramp_floor():
    """Piano della rampa con linee di riferimento per canale, combi, pareti, soglia."""
    r = CONFIG["rampa"]
    W, H = r["larghezza"], r["lunghezza"]
    p = Part("B1", "Piano rampa", 1, "cartone ondulato rigido", W, LBL + H)
    top = LBL
    cx = W / 2
    p.add(rect(0, top, W, H, S_CUT))
    p.label()
    # pareti laterali
    for x, lab in [(4, "parete B2"), (W - 4, "parete B2")]:
        p.add(line(x, top, x, top + H, S_ALIGN))
    p.add(text(4, top - 0.8, "parete B2", 2.2, "start", T_RED))
    p.add(text(W - 4, top - 0.8, "parete B2", 2.2, "end", T_RED))
    # guide inferiori (canale base) a 30/34/38 mm -> semilarghezze 15/17/19
    for cw in r["canale"]:
        hw = int(cw / 2) if cw % 2 == 0 else cw / 2
        p.add(line(cx - hw, top + 8, cx - hw, top + H - 30, S_ALIGN))
        p.add(line(cx + hw, top + 8, cx + hw, top + H - 30, S_ALIGN))
    p.add(text(cx, top + 14, "canale base B3: 30 / 34 / 38 mm", 2.4, "middle", T_RED))
    p.add(text(cx, top + 17.2, "(parti dall'esterno = 38, poi stringi)", 2.2, "middle", T_GREY))
    # posizione combi B4
    dc = r["combi_distanza_da_asse"]
    for x in (cx - dc, cx + dc):
        p.add(line(x, top + 10, x, top + 150, S_ALIGN))
    p.add(text(cx - dc, top + 155, "combo B4", 2.2, "middle", T_RED))
    p.add(text(cx + dc, top + 155, "combo B4", 2.2, "middle", T_RED))
    # soglia removibile
    p.add(line(10, top + H - 22, W - 10, top + H - 22, S_ALIGN))
    p.add(text(cx, top + H - 23.5, "soglia / gradino removibile (pivot)", 2.4, "middle", T_RED))
    # verso del moto
    p.add(text(cx, top + 5.5, "INGRESSO (da imbuto A)", 2.6, "middle", T_TXT))
    p.add(arrow(cx - 14, top + H - 8, 0, -22, "", S_ALIGN))
    p.add(text(cx, top + H - 5, "USCITA -> modulo C", 2.6, "middle", T_TXT))
    return p


def base_plate():
    """Base d'appoggio con riferimenti di cerniera, gambe e impronte moduli."""
    W, H = CONFIG["base_BP1"]["larghezza"], CONFIG["base_BP1"]["lunghezza"]
    p = Part("BP1", "Base d'appoggio", 1, "cartone ondulato rigido", W, LBL + H)
    top = LBL
    p.add(rect(0, top, W, H, S_CUT))
    p.label()
    # cerniera rampa (nastro) in alto
    p.add(line(10, top + 18, W - 10, top + 18, S_ALIGN))
    p.add(text(W / 2, top + 16.5, "cerniera rampa B1 (nastro) - lato INGRESSO in alto", 2.4, "middle", T_RED))
    # appoggio gambe
    p.add(line(10, top + 150, W - 10, top + 150, S_ALIGN))
    p.add(text(W / 2, top + 148.5, "appoggio gambe B6 (sposta per cambiare inclinazione)", 2.3, "middle", T_RED))
    # impronta modulo C
    p.add(rect(30, top + 158, 80, 26, S_ALIGN))
    p.add(text(W / 2, top + 172, "impronta modulo C (uscita)", 2.4, "middle", T_RED))
    p.add(text(W / 2, top + 8, "BASE - tutto si fissa qui con nastro", 2.6, "middle", T_TXT))
    return p


def exit_floor():
    W, H = CONFIG["uscita_C"]["larghezza"], CONFIG["uscita_C"]["lunghezza"]
    p = Part("C1", "Piano uscita", 1, "cartone ondulato rigido", W, LBL + H)
    top = LBL
    cx = W / 2
    p.add(rect(0, top, W, H, S_CUT))
    p.label()
    for x in (3, W - 3):
        p.add(line(x, top, x, top + H, S_ALIGN))
    p.add(text(3, top - 0.8, "guida C2", 2.1, "start", T_RED))
    p.add(text(W - 3, top - 0.8, "guida C2", 2.1, "end", T_RED))
    for cw in CONFIG["rampa"]["canale"]:
        hw = int(cw / 2) if cw % 2 == 0 else cw / 2
        p.add(line(cx - hw, top + 6, cx - hw, top + H - 6, S_ALIGN))
        p.add(line(cx + hw, top + 6, cx + hw, top + H - 6, S_ALIGN))
    p.add(text(cx, top + H / 2, "canale 30/34/38", 2.3, "middle", T_RED))
    p.add(text(cx, top + 4.5, "da rampa", 2.3, "middle", T_TXT))
    p.add(text(cx, top + H - 2.5, "uscita pezzi", 2.3, "middle", T_TXT))
    return p


def build_parts():
    parts = []
    im, a6, r = CONFIG["imbuto"], CONFIG["guida_paratia_A6"], CONFIG["rampa"]
    # Modulo A - imbuto
    parts.append(trapezoid_wall("A1", "Imbuto parete fronte/retro", 2, "cartone ondulato",
                                T=im["bocca_lunga"], B=im["uscita"],
                                slant=math.hypot(im["altezza"], (im["bocca_lunga"] - im["uscita"]) / 2),
                                note="unire con nastro ai lati"))
    parts.append(trapezoid_wall("A3", "Imbuto parete laterale", 2, "cartone ondulato",
                                T=im["bocca_corta"], B=im["uscita"],
                                slant=math.hypot(im["altezza"], (im["bocca_corta"] - im["uscita"]) / 2),
                                note="unire con nastro ai lati"))
    parts.append(gate_part())                                   # A5
    parts.append(wall_rect("A6", "Guida paratia", 2, "cartone ondulato", a6["lunghezza"], a6["altezza"],
                           tab=a6["linguetta"], notes=[(2, 8, "crea l'asola per A5")]))
    # Modulo B - rampa
    parts.append(ramp_floor())                                  # B1
    parts.append(wall_rect("B2", "Parete laterale rampa", 2, "cartone ondulato",
                           r["lunghezza"], r["parete_altezza"],
                           tab=r["parete_linguetta"], verso="verso valle ->"))
    parts.append(wall_rect("B3", "Guida inferiore base", 2, "cartone ondulato",
                           r["lunghezza"], r["guida_base_altezza"],
                           tab=r["guida_base_linguetta"], verso="verso valle ->"))
    parts.append(comb_part())                                   # B4
    parts.append(strip_part())                                  # B5
    parts.append(prop_part())                                   # B6
    parts.append(base_plate())                                  # BP1
    # Modulo C - uscita
    parts.append(exit_floor())                                  # C1
    u = CONFIG["uscita_C"]
    parts.append(wall_rect("C2", "Guida laterale uscita", 2, "cartone ondulato",
                           u["guida_lunghezza"], u["guida_altezza"],
                           tab=u["guida_linguetta"], verso="uscita ->"))
    return parts


# ---------------------------------------------------------------- packing (shelf FFDH)
def pack(parts):
    # un solo disegno per parte (la quantita e' indicata sull'etichetta: "RITAGLIARNE N")
    insts = [(p, 1) for p in parts]
    insts.sort(key=lambda t: t[0].h, reverse=True)

    pages = []            # ogni pagina: lista di (part, copy, x, y)
    cur = []
    x = 0.0
    y = 0.0
    shelf_h = 0.0
    for p, k in insts:
        if p.w > CONTENT_W or p.h > CONTENT_H:
            raise ValueError("Parte %s troppo grande per A4: %.1fx%.1f" % (p.code, p.w, p.h))
        if x + p.w > CONTENT_W + 1e-6:          # nuova mensola
            y += shelf_h + GAP
            x = 0.0
            shelf_h = 0.0
        if y + p.h > CONTENT_H + 1e-6:          # nuova pagina
            pages.append(cur)
            cur = []
            x = 0.0
            y = 0.0
            shelf_h = 0.0
        cur.append((p, k, x, y))
        x += p.w + GAP
        shelf_h = max(shelf_h, p.h)
    if cur:
        pages.append(cur)
    return pages


def check_overlaps(pages):
    for pi, pg in enumerate(pages):
        boxes = [(p.code, x, y, x + p.w, y + p.h) for (p, k, x, y) in pg]
        for i in range(len(boxes)):
            for j in range(i + 1, len(boxes)):
                a = boxes[i]; b = boxes[j]
                if not (a[3] <= b[1] or b[3] <= a[1] or a[4] <= b[2] or b[4] <= a[2]):
                    raise ValueError("SOVRAPPOSIZIONE pagina %d: %s con %s" % (pi, a[0], b[0]))


def verifica_passaggio_re():
    """Verifica a calcolo: il re (base diametro 50) passa dall'imbuto a paratia aperta.

    Controlla (1) l'uscita dell'imbuto, (2) la massima apertura marcata su A5,
    (3) che le tacche stiano dentro il corpo della paratia. Solleva ValueError se no.
    Restituisce le righe di report.
    """
    re_d = CONFIG["re"]["base_diametro"]
    gioco = CONFIG["re"]["gioco_minimo"]
    uscita = CONFIG["imbuto"]["uscita"]
    aperture = CONFIG["paratia_A5"]["aperture"]
    corpo = CONFIG["paratia_A5"]["altezza"]
    ap_max = max(aperture)
    if uscita < re_d + gioco:
        raise ValueError("Uscita imbuto %.1f mm < re %.1f + gioco %.1f" % (uscita, re_d, gioco))
    if ap_max < re_d + gioco:
        raise ValueError("Apertura massima A5 %.1f mm < re %.1f + gioco %.1f" % (ap_max, re_d, gioco))
    if uscita - min(aperture) > corpo:
        raise ValueError("Tacca piu' stretta fuori dal corpo di A5")
    return [
        "Passaggio re (base diam. %s): uscita imbuto a paratia aperta %s mm -> gioco %s mm  OK" % (
            _f(re_d), _f(uscita), _f(uscita - re_d)),
        "Passaggio re: apertura massima A5 %s mm -> gioco %s mm (minimo richiesto %s)  OK" % (
            _f(ap_max), _f(ap_max - re_d), _f(gioco)),
        "Tacche A5 (mm): %s  |  taratura iniziale: %s" % (
            " / ".join(_f(a) for a in aperture), _f(CONFIG["paratia_A5"]["apertura_iniziale"])),
    ]


# ---------------------------------------------------------------- pagine speciali
def cover_page():
    e = []
    e.append(text(MARGIN, 44, "Guida gravitazionale per pezzi degli scacchi", 7.0, style=T_CODE))
    e.append(text(MARGIN, 51, "Prototipo in cartone - sagome di taglio in scala 1:1 - foglio A4", 3.4, style=T_GREY))
    # legenda
    y = 62
    e.append(text(MARGIN, y, "LEGENDA", 4.2, style=T_CODE)); y += 7
    leg = [
        (S_CUT, "linea continua = TAGLIO"),
        (S_FOLD, "linea tratteggiata = PIEGA"),
        (S_ALIGN, "linea tratto-punto = riferimento di allineamento / registro"),
    ]
    for st, lab in leg:
        e.append(line(MARGIN, y - 1.2, MARGIN + 24, y - 1.2, st))
        e.append(text(MARGIN + 28, y, lab, 3.0, style=T_TXT)); y += 6.5
    e.append(rect(MARGIN, y - 4, 24, 5, S_GLUEF))
    e.append(text(MARGIN + 28, y, "retino arancio = ZONA DA INCOLLARE (linguetta)", 3.0, style=T_TXT)); y += 6.5
    e.append(line(MARGIN, y - 1.2, MARGIN + 24, y - 1.2, S_FRAME))
    e.append(text(MARGIN + 28, y, "cornice grigia = margine di stampa (NON tagliare)", 3.0, style=T_GREY)); y += 10

    # indice parti
    e.append(text(MARGIN, y, "INDICE DELLE PARTI", 4.2, style=T_CODE)); y += 6
    rows = [
        ("A1", "Imbuto parete fronte/retro", "2", "cartone ondulato"),
        ("A3", "Imbuto parete laterale", "2", "cartone ondulato"),
        ("A5", "Paratia regolabile", "1", "cartone ondulato"),
        ("A6", "Guida paratia", "2", "cartone ondulato"),
        ("B1", "Piano rampa", "1", "cartone ondulato rigido"),
        ("B2", "Parete laterale rampa", "2", "cartone ondulato"),
        ("B3", "Guida inferiore base", "2", "cartone ondulato"),
        ("B4", "Combo guida curva", "2", "cartone ondulato"),
        ("B5", "Striscia guida curva", "1", "cartoncino sottile"),
        ("B6", "Gamba inclinazione", "2", "cartone ondulato spesso"),
        ("BP1", "Base d'appoggio", "1", "cartone ondulato rigido"),
        ("C1", "Piano uscita", "1", "cartone ondulato rigido"),
        ("C2", "Guida laterale uscita", "2", "cartone ondulato"),
    ]
    e.append(text(MARGIN, y, "Cod.", 2.8, style=T_GREY))
    e.append(text(MARGIN + 16, y, "Componente", 2.8, style=T_GREY))
    e.append(text(MARGIN + 95, y, "Q.ta", 2.8, style=T_GREY))
    e.append(text(MARGIN + 112, y, "Materiale", 2.8, style=T_GREY))
    y += 4.5
    for c, n, q, m in rows:
        e.append(text(MARGIN, y, c, 2.9, style=T_CODE))
        e.append(text(MARGIN + 16, y, n, 2.9, style=T_TXT))
        e.append(text(MARGIN + 95, y, q, 2.9, style=T_TXT))
        e.append(text(MARGIN + 112, y, m, 2.9, style=T_TXT))
        y += 4.6
    y += 4
    e.append(text(MARGIN, y, "NOTA: progetto sperimentale. La geometria del raddrizzatore (B4/B5) e' una PRIMA ipotesi,", 2.7, style=T_RED)); y += 4
    e.append(text(MARGIN, y, "da regolare o ritagliare di nuovo dopo le prime prove. Non e' garantito che funzioni al primo tentativo.", 2.7, style=T_RED))
    return e


# --- richiami dei codici (callout) ------------------------------------------
def tag_box(x, y, code, w=11.0, h=5.2):
    return [rect(x, y, w, h, "fill:#fff8e1;stroke:#111111;stroke-width:0.3", rx=1.2),
            text(x + w / 2, y + h - 1.6, code, 3.0, "middle", T_CODE)]


def callout(tx, ty, lx, ly, code, desc="", w=11.0):
    """Pallino sul target + linea guida + riquadro codice a (lx,ly) + descrizione a destra."""
    out = [line(tx, ty, lx + w / 2, ly + 2.6, S_DIM),
           '<circle cx="%s" cy="%s" r="0.9" style="fill:#111111;stroke:none"/>' % (_f(tx), _f(ty))]
    out += tag_box(lx, ly, code, w)
    if desc:
        out.append(text(lx + w + 2, ly + 4, desc, 2.4, "start", T_TXT))
    return out


def green_piece(px, py, rot, scale=1.0):
    s = scale
    return ['<g transform="translate(%s,%s) rotate(%s)">' % (_f(px), _f(py), _f(rot)) +
            rect(-1.8 * s, -8 * s, 3.6 * s, 10 * s, "fill:none;stroke:#1b7a3d;stroke-width:0.5") +
            '<circle cx="0" cy="%s" r="%s" style="fill:none;stroke:#1b7a3d;stroke-width:0.5"/>' % (_f(-10 * s), _f(2.2 * s)) +
            rect(-4.5 * s, -2 * s, 9 * s, 3 * s, "fill:none;stroke:#1b7a3d;stroke-width:0.5") + '</g>']


def assembly_page():
    e = []
    e.append(text(MARGIN, 40, "VISTA D'ASSIEME (con i codici dei componenti)", 5.0, style=T_CODE))
    e.append(text(MARGIN, 46, "Come funziona: i pezzi versati nell'IMBUTO (A) scendono sulla RAMPA inclinata (B); le guide inferiori tengono la", 2.6, style=T_TXT))
    e.append(text(MARGIN, 49.4, "base mentre la guida curva prova a raddrizzare il pezzo; dal canale di USCITA (C) escono in piedi, in fila.", 2.6, style=T_TXT))
    e.append(text(MARGIN, 52.8, "Ogni codice qui sotto corrisponde a una sagoma da ritagliare (vedi fogli successivi).", 2.6, style=T_GREY))

    # ---------------- (1) vista laterale
    e.append(text(14, 61, "1) Vista laterale (il pezzo scende da sinistra verso destra)", 3.0, style=T_CODE))
    baseY = 116
    e.append(line(22, baseY, 175, baseY, S_CUT))                    # base
    e += callout(150, baseY, 150, baseY + 4, "BP1", "base d'appoggio")
    # rampa inclinata (alta a sx, bassa a dx)
    e.append(line(40, 72, 150, 112, S_CUT))
    e += callout(96, 92, 100, 66, "B1", "piano rampa")
    # gamba
    e.append(poly([(36, 72), (46, 72), (46, baseY), (36, baseY)], S_ALIGN))
    e += callout(41, 100, 14, 96, "B6", "inclinazione 15-25")
    # guida curva
    e.append(path("M 46 62 Q 96 56 150 104", S_FOLD))
    e += callout(96, 57, 118, 46, "B5", "guida curva (arco)")
    # soglia
    e.append(line(138, 112, 138, 105, S_CUT))
    e += callout(138, 108, 150, 98, "sog", "soglia/perno removibile", w=12)
    # imbuto sopra l'ingresso
    e.append(poly([(26, 40), (58, 40), (48, 58), (36, 58)], S_CUT))
    e.append(arrow(42, 59, 0, 10, "", S_CUT))
    e += callout(42, 49, 14, 42, "A", "imbuto (dettaglio sotto)")
    # uscita
    e.append(line(150, 112, 172, 112, S_CUT))
    e += callout(164, 112, 160, 120, "C1", "piano uscita")
    # pezzo in 3 fasi
    for (px, rot, lab) in [(60, -70, "coricato"), (100, -35, "in rotazione"), (146, 0, "verticale")]:
        yy = 72 + (112 - 72) * ((px - 40) / (150 - 40)) - 7
        e += green_piece(px, yy, rot, 0.9)
        e.append(text(px, yy + 11, lab, 2.2, "middle", "font-family:Helvetica;fill:#1b7a3d"))

    # ---------------- (2) sezione A-A
    e.append(text(14, 131, "2) Sezione A-A sul raddrizzatore", 3.0, style=T_CODE))
    fy = 192
    e.append(line(24, fy, 96, fy, S_CUT))                           # piano
    e.append(rect(40, fy - 16, 3, 16, S_CUT))                       # guida B3 sx
    e.append(rect(69, fy - 16, 3, 16, S_CUT))                       # guida B3 dx
    e.append(rect(34, fy - 24, 2.5, 24, S_CUT))                     # parete B2 sx
    e.append(rect(77.5, fy - 24, 2.5, 24, S_CUT))                   # parete B2 dx
    e.append(line(33, fy, 35, fy - 36, S_CUT))                      # combo B4 sx
    e.append(line(80, fy, 78, fy - 36, S_CUT))                      # combo B4 dx
    e.append(path("M 34 %s Q 56 %s 78 %s" % (_f(fy - 34), _f(fy - 40), _f(fy - 34)), S_FOLD))  # B5
    # pezzo in piedi dentro al canale
    e.append(rect(41, fy - 6, 30, 6, "fill:none;stroke:#1b7a3d;stroke-width:0.5"))
    e.append(rect(50, fy - 28, 12, 22, "fill:none;stroke:#1b7a3d;stroke-width:0.5"))
    e.append('<circle cx="56" cy="%s" r="5" style="fill:none;stroke:#1b7a3d;stroke-width:0.5"/>' % _f(fy - 33))
    e += callout(35, fy - 20, 12, 150, "B2", "pareti rampa")
    e += callout(41, fy - 8, 12, 162, "B3", "canale base 30-38")
    e += callout(34, fy - 24, 12, 174, "B4", "sostegni guida curva")
    e += callout(78, fy - 37, 84, 146, "B5", "striscia curva")

    # ---------------- (3) vista dall'alto
    e.append(text(108, 131, "3) Vista dall'alto (canale + imbuto)", 3.0, style=T_CODE))
    e.append(rect(126, 150, 70, 30, S_FRAME))
    e.append(line(126, 158, 196, 158, S_CUT))
    e.append(line(126, 172, 196, 172, S_CUT))
    # imbuto (bocca) a sx
    e.append(poly([(110, 148), (126, 156), (126, 174), (110, 182)], S_CUT))
    e.append(rect(124, 156, 3, 18, S_CUT))                          # paratia
    e.append(arrow(182, 154, 12, 0, "pezzi", S_CUT))
    e += callout(116, 152, 108, 138, "A1", "parete fronte/retro")
    e += callout(120, 178, 150, 138, "A3", "parete laterale")
    e += callout(125, 165, 108, 186, "A5", "paratia regolab.")
    e += callout(126, 156, 150, 186, "A6", "guide paratia")
    e += callout(196, 165, 170, 150, "C2", "guide uscita")
    return e


def _steps(x, y, title, steps, wrap=52):
    out = [text(x, y, title, 3.4, style=T_CODE)]
    yy = y + 6
    for i, s in enumerate(steps, 1):
        line1 = "%d. %s" % (i, s)
        out.append(text(x, yy, line1, 2.5, style=T_TXT))
        yy += 4.4
    return out, yy


def montaggio_ab():
    e = []
    e.append(text(MARGIN, 40, "MONTAGGIO - moduli A (imbuto) e B (rampa)", 5.0, style=T_CODE))

    # ====== MODULO A - esploso
    e.append(text(14, 50, "Modulo A - imbuto (esploso)", 3.0, style=T_CODE))
    ox, oy = 48, 80                           # centro uscita
    s = 16
    e.append(rect(ox - s / 2, oy - s / 2, s, s, S_ALIGN))          # uscita 60x60
    e.append(text(ox, oy + 1, "uscita", 2.1, "middle", T_GREY))
    # parete sopra (A1), sotto (A1), sx (A3), dx (A3)
    e.append(poly([(ox - 14, oy - 26), (ox + 14, oy - 26), (ox + s / 2, oy - s / 2), (ox - s / 2, oy - s / 2)], S_CUT))
    e.append(line(ox - s / 2, oy - s / 2, ox + s / 2, oy - s / 2, S_FOLD))
    e.append(poly([(ox - s / 2, oy + s / 2), (ox + s / 2, oy + s / 2), (ox + 14, oy + 26), (ox - 14, oy + 26)], S_CUT))
    e.append(line(ox - s / 2, oy + s / 2, ox + s / 2, oy + s / 2, S_FOLD))
    e.append(poly([(ox - 24, oy - 12), (ox - s / 2, oy - s / 2), (ox - s / 2, oy + s / 2), (ox - 24, oy + 12)], S_CUT))
    e.append(line(ox - s / 2, oy - s / 2, ox - s / 2, oy + s / 2, S_FOLD))
    e.append(poly([(ox + s / 2, oy - s / 2), (ox + 24, oy - 12), (ox + 24, oy + 12), (ox + s / 2, oy + s / 2)], S_CUT))
    e.append(line(ox + s / 2, oy - s / 2, ox + s / 2, oy + s / 2, S_FOLD))
    for (ax, ay, dx, dy) in [(ox, oy - 27, 0, -4), (ox, oy + 27, 0, 4), (ox - 25, oy, -4, 0), (ox + 25, oy, 4, 0)]:
        e.append(arrow(ax, ay, dx, dy, "", S_FOLD))
    e += callout(ox, oy - 24, 70, 54, "A1", "fronte/retro (x2)")
    e += callout(ox - 22, oy, 12, 92, "A3", "lati (x2)")
    # paratia a lato
    e.append(rect(84, oy - 10, 6, 24, S_CUT))
    e.append(arrow(83, oy, -6, 0, "", S_FOLD))
    e += callout(87, oy + 14, 78, 100, "A5", "paratia regolabile")
    e += callout(ox + s / 2, oy - s / 2, 70, 100, "A6", "guide paratia (x2)")

    st, _ = _steps(104, 50, "Passi - modulo A", [
        "Unisci le 4 pareti (A1 x2 + A3 x2) con nastro",
        "   sugli spigoli: tronco di piramide, bocca in alto.",
        "Uscita in basso ~60x60 mm.",
        "Incolla A6 x2 ai bordi dell'uscita: crei 2 asole.",
        "Infila la paratia A5 nelle asole: alzala o",
        "   abbassala per regolare l'apertura (max ~55 per il re).",
    ])
    e += st

    # ====== MODULO B - esploso (vista laterale)
    e.append(text(14, 132, "Modulo B - rampa (esploso, vista laterale)", 3.0, style=T_CODE))
    bY = 205
    e.append(line(20, bY, 116, bY, S_CUT))
    e += tag_box(100, bY + 2, "BP1")
    # rampa sollevata
    e.append(line(30, 158, 114, 196, S_CUT))
    e += tag_box(70, 150, "B1")
    e.append(line(114, 196, 114, bY, S_DIM)); e.append(text(116, bY - 4, "cerniera (nastro)", 2.2, style=T_GREY))
    # gamba
    e.append(poly([(26, 158), (34, 158), (34, bY), (26, bY)], S_ALIGN))
    e += tag_box(12, 170, "B6")
    # pareti/guide/combi (indicate con tacche + tag)
    e.append(path("M 36 150 Q 75 146 112 184", S_FOLD)); e += tag_box(74, 138, "B5")
    e.append(line(44, 171, 44, 162, S_CUT)); e.append(line(90, 189, 90, 180, S_CUT))
    e += tag_box(44, 158, "B4")
    e += tag_box(55, 176, "B3")
    e += tag_box(55, 184, "B2")
    e.append(text(20, bY + 9, "B2 pareti, B3 canale, B4 sostegni curva: vedi sezione nel foglio d'assieme.", 2.3, style=T_GREY))

    st2, _ = _steps(124, 132, "Passi - modulo B", [
        "Su B1 trovi le linee-guida (canale, pareti,",
        "   combi, soglia): servono a posizionare le parti.",
        "Piega e fissa le pareti B2 x2 ai lati.",
        "Fissa le guide B3 x2 nel canale (parti da 38 mm).",
        "Incolla i combi B4 x2 in piedi, lato alto",
        "   verso l'ingresso.",
        "Curva la striscia B5 e appoggiala sui combi.",
        "Metti la soglia removibile vicino all'uscita.",
        "Fissa B1 a BP1 con nastro (cerniera) e solleva",
        "   il lato alto con le gambe B6 x2.",
    ])
    e += st2
    return e


def montaggio_c_union():
    e = []
    e.append(text(MARGIN, 40, "MONTAGGIO - modulo C (uscita) e unione dei moduli", 5.0, style=T_CODE))

    # ===== modulo C esploso
    e.append(text(14, 50, "Modulo C - uscita (esploso, vista dall'alto)", 3.0, style=T_CODE))
    e.append(rect(34, 58, 40, 46, S_CUT))                 # piano C1
    e += callout(54, 80, 12, 64, "C1", "piano uscita")
    e.append(rect(34, 58, 4, 46, S_ALIGN))               # guida sx
    e.append(rect(70, 58, 4, 46, S_ALIGN))               # guida dx
    e.append(arrow(30, 70, 6, 0, "", S_FOLD)); e.append(arrow(78, 70, -6, 0, "", S_FOLD))
    e += callout(72, 100, 80, 96, "C2", "guide (x2) piegate in su")
    e.append(text(54, 110, "canale 30-38 mm", 2.2, "middle", T_GREY))

    st, _ = _steps(104, 50, "Passi - modulo C", [
        "Su C1 piega e fissa le guide C2 x2 lungo",
        "   le linee del canale.",
        "Stessa larghezza del canale della rampa.",
        "Tieni le guide un po' basse per vedere i pezzi.",
    ])
    e += st

    # ===== unione dei moduli
    e.append(text(14, 132, "Unione dei moduli (vista laterale d'insieme)", 3.0, style=T_CODE))
    bY = 196
    e.append(line(20, bY, 190, bY, S_CUT))
    e += callout(170, bY, 168, bY + 4, "BP1", "base: tutto si fissa qui")
    # rampa B
    e.append(line(50, 150, 150, 190, S_CUT)); e += callout(100, 171, 96, 150, "B", "rampa")
    e.append(poly([(46, 150), (56, 150), (56, bY), (46, bY)], S_ALIGN)); e += tag_box(30, 156, "B6")
    e.append(line(150, 190, 150, bY, S_DIM)); e.append(text(152, bY - 3, "cerniera nastro", 2.2, style=T_GREY))
    # imbuto A
    e.append(poly([(36, 112), (72, 112), (60, 136), (48, 136)], S_CUT)); e += callout(54, 124, 14, 110, "A", "imbuto sopra l'ingresso")
    e.append(arrow(54, 137, 0, 10, "", S_CUT))
    # uscita C
    e.append(line(150, 190, 178, 190, S_CUT)); e += callout(166, 190, 160, 172, "C", "uscita a filo")
    # pezzi
    e += green_piece(70, 162, -40, 0.8)
    e += green_piece(140, 186, 0, 0.8)

    st2, _ = _steps(14, 212, "Passi - unione", [
        "Fissa B1 a BP1 con nastro (cerniera), lato ingresso in alto; solleva con B6.",
        "Metti il modulo C nell'impronta, a filo sotto l'uscita della rampa.",
        "Sostieni l'imbuto A sopra l'ingresso (montanti di scarto) cosi' l'uscita cade nel canale.",
        "Regola: inclinazione (B6), larghezza canale (B3 e C2), apertura imbuto (A5). Poi fai le prove.",
    ])
    e += st2
    return e


def quote_page():
    e = []
    e.append(text(MARGIN, 40, "TAVOLA QUOTATA (quote in mm)", 5.0, style=T_CODE))

    # --- sezione trasversale del canale
    ox, oy = 30, 75
    e.append(text(ox, oy - 6, "Sezione trasversale A-A (sul raddrizzatore)", 3.2, style=T_TXT))
    floor_y = oy + 70
    e.append(line(ox, floor_y, ox + 120, floor_y, S_CUT))     # piano rampa
    # guide inferiori (B3) a 34 mm
    gi_l = ox + 43
    gi_r = ox + 77
    e.append(rect(gi_l - 3, floor_y - 18, 3, 18, S_CUT))
    e.append(rect(gi_r, floor_y - 18, 3, 18, S_CUT))
    # pezzo in piedi (base 30, corpo)
    cx = (gi_l + gi_r) / 2
    e.append(rect(cx - 15, floor_y - 6, 30, 6, "fill:none;stroke:#1b7a3d;stroke-width:0.5"))     # base 30
    e.append(rect(cx - 6, floor_y - 44, 12, 38, "fill:none;stroke:#1b7a3d;stroke-width:0.5"))    # collo/corpo
    e.append('<circle cx="%s" cy="%s" r="8" style="fill:none;stroke:#1b7a3d;stroke-width:0.5"/>' % (_f(cx), _f(floor_y - 50)))
    # guida curva sopra
    e.append(path("M %s %s Q %s %s %s %s" % (_f(gi_l - 8), _f(floor_y - 60), _f(cx), _f(floor_y - 66), _f(gi_r + 8), _f(floor_y - 60)), S_FOLD))
    e.append(text(cx, floor_y - 68, "guida curva B5", 2.6, "middle", T_BLUE))
    # quote
    e.extend(dim_h(gi_l, gi_r, floor_y + 8, "canale 34 (reg. 30-38)"))
    e.extend(dim_v(ox - 6, floor_y - 44, floor_y, "corpo ~44"))
    e.extend(dim_h(cx - 15, cx + 15, floor_y + 16, "base 30"))
    e.extend(dim_v(ox + 128, floor_y - 60, floor_y, "H curva ~60 (reg.)"))
    e.append(text(ox, floor_y + 24, "Luce guida-corpo: mantieni >= 2 mm per non schiacciare il collo (collo ~12).", 2.6, style=T_RED))

    # --- profilo laterale zona raddrizzatore
    px, py = 30, 185
    e.append(text(px, py - 6, "Profilo laterale B (incl. 15-25 gradi) - quote principali", 3.2, style=T_TXT))
    fy = py + 60
    e.append(line(px, fy, px + 150, fy, S_CUT))
    e.append(text(px, fy + 5, "piano rampa (lungh. 180)", 2.6, style=T_GREY))
    e.extend(dim_h(px, px + 150, fy + 12, "180 (lunghezza utile rampa)"))
    # combo curva entry/exit
    e.append(line(px + 20, fy, px + 20, fy - 60, S_ALIGN))
    e.append(line(px + 150, fy, px + 150, fy - 22, S_ALIGN))
    e.extend(dim_v(px + 14, fy - 60, fy, "ingresso ~60"))
    e.extend(dim_v(px + 156, fy - 22, fy, "uscita ~22"))
    e.append(path("M %s %s Q %s %s %s %s" % (_f(px + 20), _f(fy - 58), _f(px + 90), _f(fy - 48), _f(px + 150), _f(fy - 20)), S_FOLD))
    e.append(text(px + 85, fy - 52, "striscia B5 (arco discendente)", 2.6, "middle", T_BLUE))
    e.append(text(px, fy + 22, "Pedone rif.: H 48, base 30, collo 12, testa 16.  Re: base 50 (l'imbuto non deve bloccarlo).", 2.6, style=T_TXT))
    return e


# ---------------------------------------------------------------- rendering pagina
def page_frame(content_elems, page_no, total, title_sub):
    e = []
    # cornice margine (non tagliare)
    e.append(rect(MARGIN, MARGIN, A4_W - 2 * MARGIN, A4_H - 2 * MARGIN, S_FRAME))
    # crocini di registro agli angoli (tratto-punto)
    for (cx, cy) in [(MARGIN, MARGIN), (A4_W - MARGIN, MARGIN), (MARGIN, A4_H - MARGIN), (A4_W - MARGIN, A4_H - MARGIN)]:
        e.append(line(cx - 4, cy, cx + 4, cy, S_ALIGN))
        e.append(line(cx, cy - 4, cx, cy + 4, S_ALIGN))
    # intestazione
    e.append(text(MARGIN, 13.5, "Guida gravitazionale pezzi scacchi - sagome 1:1", 3.6, style=T_CODE))
    e.append(text(A4_W - MARGIN, 13.5, "Foglio %d / %d" % (page_no, total), 3.4, "end", style=T_TXT))
    e.append(text(MARGIN, 18.0, title_sub, 2.8, style=T_GREY))
    # barra di scala 100 mm
    sy = 26.0
    e.append(line(MARGIN, sy, MARGIN + 100, sy, S_CUT))
    for t in range(0, 101, 10):
        e.append(line(MARGIN + t, sy - 1.6, MARGIN + t, sy + 1.6, S_CUT))
    e.append(text(MARGIN, sy - 2.2, "SCALA DI CONTROLLO: questa barra deve misurare 100 mm (stampa a 100%, 1:1)", 2.7, style=T_RED))
    e.append(text(MARGIN + 100 + 3, sy + 1, "100 mm", 2.8, style=T_TXT))
    # contenuto
    e.extend(content_elems)
    # pie' di pagina
    e.append(text(A4_W / 2, A4_H - MARGIN + 4, "Guida gravitazionale pezzi scacchi - scala 1:1 - Foglio %d/%d" % (page_no, total),
                  2.4, "middle", T_GREY))
    return e


def place_parts_on_page(placements):
    e = []
    for (p, k, x, y) in placements:
        ax = CONTENT_X0 + x
        ay = CONTENT_Y0 + y
        body = "".join(p.elems)
        e.append('<g transform="translate(%s,%s)">%s</g>' % (_f(ax), _f(ay), body))
        # riquadro leggero d'ingombro per leggibilita
        e.append(rect(ax - 1, ay - 1, p.w + 2, p.h + 2, "fill:none;stroke:#eeeeee;stroke-width:0.15"))
    return e


# ---------------------------------------------------------------- scrittura file
def svg_header(w, h, extra_defs=""):
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<svg xmlns="http://www.w3.org/2000/svg" '
            'xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" '
            'xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.0.dtd" '
            'width="%smm" height="%smm" viewBox="0 0 %s %s">\n'
            '<defs><pattern id="hatch" patternUnits="userSpaceOnUse" width="2.2" height="2.2" '
            'patternTransform="rotate(45)">'
            '<line x1="0" y1="0" x2="0" y2="2.2" style="stroke:#f0a000;stroke-width:0.5"/></pattern></defs>\n'
            '%s') % (_f(w), _f(h), _f(w), _f(h), extra_defs)


def flatten(seq):
    out = []
    for el in seq:
        if isinstance(el, (list, tuple)):
            out.extend(flatten(el))
        else:
            out.append(el)
    return out


def write_single(path_, elems):
    body = svg_header(A4_W, A4_H) + "".join(flatten(elems)) + "\n</svg>\n"
    with open(path_, "w", encoding="utf-8") as f:
        f.write(body)


def write_combined(path_, pages_elems):
    n = len(pages_elems)
    stepx = A4_W + 12.0
    total_w = A4_W + (n - 1) * stepx
    namedview = ['<sodipodi:namedview inkscape:document-units="mm" showborder="true">']
    body = []
    for i, els in enumerate(pages_elems):
        ox = i * stepx
        namedview.append('<inkscape:page x="%s" y="0" width="%s" height="%s" id="pg%d"/>' % (_f(ox), _f(A4_W), _f(A4_H), i + 1))
        body.append('<g transform="translate(%s,0)">%s</g>' % (_f(ox), "".join(flatten(els))))
    namedview.append('</sodipodi:namedview>')
    out = svg_header(total_w, A4_H, extra_defs="".join(namedview) + "\n") + "".join(flatten(body)) + "\n</svg>\n"
    with open(path_, "w", encoding="utf-8") as f:
        f.write(out)


def validate_xml(path_):
    with open(path_, "r", encoding="utf-8") as f:
        minidom.parseString(f.read())


# ---------------------------------------------------------------- main
def main():
    if not os.path.isdir(OUT):
        os.makedirs(OUT)

    parts = build_parts()
    part_pages = pack(parts)
    check_overlaps(part_pages)

    # elenco pagine: speciali + parti
    specials = [
        (cover_page(), "Copertina - legenda - indice parti"),
        (assembly_page(), "Vista d'assieme con i codici dei componenti"),
        (montaggio_ab(), "Montaggio - moduli A e B"),
        (montaggio_c_union(), "Montaggio - modulo C e unione"),
        (quote_page(), "Tavola quotata (mm)"),
    ]
    total = len(specials) + len(part_pages)

    pages_full = []
    pno = 0
    for content, sub in specials:
        pno += 1
        pages_full.append(page_frame(content, pno, total, sub))
    for idx, placements in enumerate(part_pages):
        pno += 1
        codes = ", ".join(sorted(set(p.code for (p, k, x, y) in placements)))
        sub = "Sagome da ritagliare - parti: " + codes
        content = place_parts_on_page(placements)
        pages_full.append(page_frame(content, pno, total, sub))

    # scrivi file per-pagina
    written = []
    for i, els in enumerate(pages_full):
        fn = os.path.join(OUT, "foglio-%02d.svg" % (i + 1))
        write_single(fn, els)
        validate_xml(fn)
        written.append(fn)

    # scrivi file combinato multi-pagina
    combined = os.path.join(OUT, "guida-pezzi-tutto.svg")
    write_combined(combined, pages_full)
    validate_xml(combined)

    # report di verifica
    print("=== Verifica generazione ===")
    print("Parti distinte: %d  |  pezzi fisici totali: %d" % (len(parts), sum(p.qty for p in parts)))
    print("Pagine totali: %d  (%d doc + %d sagome)" % (total, len(specials), len(part_pages)))
    for i, placements in enumerate(part_pages):
        for (p, k, x, y) in placements:
            assert x >= -1e-6 and y >= -1e-6
            assert x + p.w <= CONTENT_W + 1e-6, "%s esce a dx" % p.code
            assert y + p.h <= CONTENT_H + 1e-6, "%s esce in basso" % p.code
        print("  foglio sagome %d: %s" % (i + 1, ", ".join("%s(%dx%d)" % (p.code, round(p.w), round(p.h)) for (p, k, x, y) in placements)))
    for riga in verifica_passaggio_re():
        print(riga)
    print("Tutti i tracciati validati come XML ben formato.")
    print("File per-pagina: %d in %s/" % (len(written), os.path.relpath(OUT, HERE)))
    print("File combinato:  %s" % os.path.relpath(combined, HERE))


if __name__ == "__main__":
    main()
