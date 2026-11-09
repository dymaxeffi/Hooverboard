"""M00 – Kalibrier- und Freigabecoupons (Voraussetzung für Fertigungsfreigabe aller Module).

Ergebnisse werden in mechlib/fab.py eingetragen (KERF, SLOT_CLR, PRESS_608, HOLE_COMP,
CLR_SLIDE, GEAR_BACKLASH), danach alle Exporte neu erzeugen. Laser-Leistungsgrenze
und Plottergrenze werden hier am eigenen Gerät + eigener Materialcharge nachgewiesen.
"""

from __future__ import annotations

import cadquery as cq

from mechlib import fab, geom2d as g2
from mechlib.cadbridge import extrude
from mechlib.common import HC, label
from mechlib.module import Module, Part

SPEEDS = [3, 4, 5, 6, 8]              # mm/s
POWERS = [70, 80, 90, 100]            # %


def kerf_comb():
    """10 Streifen à 10.00 mm in einem Stück (ohne Kompensation). Kerf = (100 − Summe Streifenbreiten)/10."""
    from shapely.geometry import MultiLineString
    g = g2.rect_xy(0, 0, 100, 25)
    lines = MultiLineString([[(10 * i, 25), (10 * i, 5)] for i in range(1, 10)])   # je 1 Schnitt, Steg unten hält
    eng = label("KERF 10x10.00", (50, 2.5), 2.5)
    return g, eng, lines


def slot_ladder():
    widths = [round(2.80 + 0.05 * i, 2) for i in range(9)]
    g = g2.rect_xy(0, 0, 9 * 12 + 4, 30)
    eng = None
    for i, w in enumerate(widths):
        x = 4 + 12 * i + 4
        g = g.difference(g2.rect_xy(x - w / 2, 12, x + w / 2, 30))
        t = label(f"{w:.2f}", (x, 6), 2.2)
        eng = t if eng is None else eng.union(t)
    return g, eng, widths


def tab_piece():
    g = g2.rect_xy(0, 0, 40, 30).union(g2.rect_xy(10, 30, 30, 45))
    return g, label("TAB", (20, 12), 4)


def power_matrix():
    g = None
    eng = None
    for i, v in enumerate(SPEEDS):
        for j, pw in enumerate(POWERS):
            x, y = 6 + 22 * i, 6 + 22 * j
            sq = g2.rect_xy(x, y, x + 14, y + 14)
            g = sq if g is None else g.union(sq)
            t = label(f"{pw}/{v}", (x + 7, y + 17.5), 2.2)
            eng = t if eng is None else eng.union(t)
    frame = g2.rect_xy(0, 0, 22 * len(SPEEDS) + 4, 22 * len(POWERS) + 4)
    return frame.difference(g), eng


def fdm_coupon():
    """Lochleiter 608-Sitz 21.95–22.20, Wellenbohrung 8.0–8.5, M3/Mutterfalle."""
    seats = [21.95, 22.00, 22.05, 22.10, 22.15, 22.20]
    pins = [8.0, 8.1, 8.2, 8.3, 8.4, 8.5]
    w = 6 * 28 + 4
    body = cq.Workplane("XY").box(w, 64, 7.0, centered=False)
    for i, d in enumerate(seats):
        body = body.cut(cq.Workplane("XY").circle(d / 2).extrude(7).translate((4 + 14 + 28 * i, 18, 0)))
        body = body.cut(cq.Workplane("XY").circle(pins[i] / 2).extrude(7).translate((4 + 14 + 28 * i, 46, 0)))
    for i, d in enumerate(seats):  # Prägung als 0.4-mm-Vertiefung
        txt = extrude(g2.text(f"{d:.2f}", 3.0, (4 + 14 + 28 * i, 4)), 0.4, 6.6)
        body = body.cut(txt)
        body = body.cut(extrude(g2.text(f"{pins[i]:.1f}", 3.0, (4 + 14 + 28 * i, 58)), 0.4, 6.6))
    return body, seats, pins


def plot_test():
    g = g2.rect_xy(0, 0, 120, 60)
    pen = label("PLOT TEST  Druck: ____ gf", (60, 55), 3.0)
    for i, d in enumerate([3.0, 4.0, 5.0, 6.0, 8.0]):
        g = g.difference(g2.circle(d, (12 + 20 * i, 40)))
    for i, s in enumerate([3.0, 5.0, 10.0]):
        g = g.difference(g2.rect(s, s, (15 + 25 * i, 18), r=fab.CUT_MIN_RADIUS.value))
    for i, b in enumerate([1.0, 2.0, 3.0]):          # Stege zwischen zwei Schlitzen
        x = 82 + 12 * i
        g = g.difference(g2.rect_xy(x - 3, 8, x, 28)).difference(g2.rect_xy(x + b, 8, x + b + 3, 28))
    return g, pen


def build() -> Module:
    kc, kce, kcl = kerf_comb()
    sl, sle, widths = slot_ladder()
    tb, tbe = tab_piece()
    pm, pme = power_matrix()
    fc, seats, pins = fdm_coupon()
    pt, pte = plot_test()
    parts = [
        Part("M00-P01", "Kerf-Kamm", "laser", "PLY3", 1, profile=kc, engrave=kce, no_kerf=True, cut_lines=kcl,
             orientation="flach", rationale="Bestimmt KERF: 9 Finger (Soll 10.00) messen; KERF = 10.00 − Mittelwert der Fingerbreiten."),
        Part("M00-P02", "Schlitzleiter", "laser", "PLY3", 1, profile=sl, engrave=sle,
             orientation="flach", rationale="Bestimmt SLOT_CLR: welcher Schlitz nimmt TAB saugend auf."),
        Part("M00-P03", "Prüflasche", "laser", "PLY3", 1, profile=tb, engrave=tbe, orientation="flach",
             rationale="Gegenstück zur Schlitzleiter, gleiche Charge."),
        Part("M00-P04", "Leistungs-Geschwindigkeits-Matrix", "laser", "PLY3", 1, profile=pm, engrave=pme, no_kerf=True,
             orientation="flach; jedes Quadrat eigenes Objekt mit eigenen Parametern",
             rationale="Weist Durchschnitt 3 mm (bzw. 4 mm TEST) am eigenen Gerät nach – Freigabegrenze."),
        Part("M00-P05", "FDM-Toleranzcoupon", "fdm", "PETG", 1, shape=fc, orientation="flach",
             rationale="Bestimmt PRESS_608 (Lager presst mit Hand+Schraubstock, fällt nicht heraus) und Wellenspiel."),
        Part("M00-P06", "Plotter-Testmuster", "plotter", "CARD05", 1, profile=pt, engrave=pte, test_feature=True,
             orientation="je Material: PAPER160, CARD05, PET019, GASKET05, SIL05",
             rationale="Weist kleinste Löcher/Stege und Messerdruck je Material nach (≤ 0.5 mm, 50–600 gf)."),
    ]
    for p in parts:
        p.poses = []
    return Module(
        "m00", "Kalibrier- und Freigabecoupons",
        "Nachweis der tatsächlichen Gerätegrenzen (Laser, Plotter, FDM) vor der Fertigungsfreigabe. Kein Funktionsmodul.",
        parts,
        hardware=[("608-2RS (Prüflager)", 1, 0.8), ("Welle Ø8 h9 (Prüfstift)", 1, 1.0)],
        assembly=["Siehe manufacturing/process_limits.md, Abschnitt Freigabeprozedur."],
        function_test="Alle Coupons bestanden und Werte in fab.py eingetragen → Freigabe G5 möglich.",
    )
