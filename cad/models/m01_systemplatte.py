"""M01 – Systemplatte (Rasterplatte) mit Mutterfallen, Füssen und Standardelementen.

Hybrid: zwei gelaserte Lagen (Lochlage Ø3.4 + Sechskantlage für M3-Muttern) bilden
eine steife 6-mm-Grundplatte mit 20-mm-Raster. Muttern werden von unten nur dort
eingelegt, wo sie gebraucht werden; die Sechskantlage verhindert das Mitdrehen.
Gedruckte Füsse (TPU) entkoppeln und schützen die Muttern.
"""

from __future__ import annotations

import cadquery as cq

from mechlib import fab, geom2d as g2
from mechlib.cadbridge import extrude
from mechlib.common import T, flat_pose, label, lagerflansch_608, winkelfuss
from mechlib.module import Module, Part

W, H, R0, NX, NY = 290.0, 190.0, 15.0, 14, 9


def grid_points():
    return [(R0 + 20 * i - W / 2, R0 + 20 * j - H / 2) for i in range(NX) for j in range(NY)]


def build() -> Module:
    pts = grid_points()
    outer = g2.rect(W, H, r=6)
    top = outer
    nuts = outer
    af = fab.M3_NUT_AF + 0.10  # Sechskant leicht übermass, Kerf ist separat kompensiert
    for p in pts:
        top = top.difference(g2.circle(fab.M3_CLR, p))
        nuts = nuts.difference(g2.hexagon(af, p, rot=30))
    eng = None
    for i in range(NX):
        t = label(str(i), (R0 + 20 * i - W / 2, H / 2 - 5.5), 3.0)
        eng = t if eng is None else eng.union(t)
    for j in range(NY):
        eng = eng.union(label(chr(65 + j), (-W / 2 + 6, R0 + 20 * j - H / 2 + 10), 3.0))
    eng = eng.union(label("M01 SYSTEMPLATTE 20 mm", (0, -H / 2 + 5.0), 3.0))

    # Fuss TPU: Ø24, 8 hoch, Senkung für Schraubenkopf von unten, sitzt unter Ecklöchern
    # Druck: Auflagefläche zur Platte auf dem Bett, Kopfsenkung oben (= in Baugruppe unten)
    foot = extrude(g2.circle(24), 8).cut(cq.Workplane("XY").circle((fab.M3_CLR + 0.1) / 2).extrude(8)) \
        .cut(cq.Workplane("XY").circle(3.3).extrude(4.5).translate((0, 0, 3.5)))
    corners = [(pts[0]), (pts[NY - 1]), (pts[-NY]), (pts[-1])]

    parts = [
        Part("M01-P01", "Lochlage", "laser", "PLY3", 1, profile=top, engrave=eng,
             poses=[flat_pose(T)], orientation="flach, Gravurseite oben",
             rationale="Grosse ebene Platte mit 126 präzisen Bohrungen: Laser in einem Durchgang, "
                       "Druck wäre teuer/langsam und verzugsgefährdet."),
        Part("M01-P02", "Mutterlage", "laser", "PLY3", 1, profile=nuts,
             poses=[flat_pose(0)], orientation="flach",
             rationale="Sechskant-Mutterfallen exakt im Raster; mit P01 verleimt → 6 mm Sandwich, "
                       "verdrehsicher, Muttern nach Bedarf."),
        Part("M01-P03", "Fuss", "fdm", "TPU95A", 4, shape=foot,
             orientation="Auflagefläche auf Bett, Kopfsenkung oben",
             rationale="Rutschfest und dämpfend; TPU nur im Druck verfügbar."),
        Part("M01-P04", "Lagerflansch 608 (Standard)", "fdm", "PETG", 0, shape=lagerflansch_608(),
             orientation="Flansch auf Bett, Lagersitz oben",
             rationale="Rotationssymmetrischer Presssitz: im Druck senkrecht → rund und masshaltig; "
                       "Laserplatte gibt die exakte Achslage vor."),
        Part("M01-P05", "Winkelfuss (Standard)", "fdm", "PETG", 0, shape=winkelfuss(),
             orientation="liegend, L-Profil auf Bett",
             rationale="Verbindet stehende Laserplatten mit dem Raster; L-Form mit Kehle nur gedruckt sinnvoll."),
    ]
    # Füsse unter die Ecken (Druck z=0 oben im Druck = Senkung; in Baugruppe unterhalb Platte)
    parts[2].poses = [(lambda c: (lambda wp: wp.rotate((0, 0, 0), (1, 0, 0), 180).translate((c[0], c[1], 0))))(c)
                      for c in corners]
    return Module(
        "m01", "Systemplatte 290×190 mit 20-mm-Raster",
        "Gemeinsame Basis aller Module: Prüfaufbauten schnell, reproduzierbar und ausgerichtet montieren. "
        "Enthält die Standardelemente Lagerflansch 608 und Winkelfuss, die andere Module verwenden.",
        parts,
        hardware=[("Mutter M3 DIN 934 (nach Bedarf, Richtwert)", 40, 0.03),
                  ("Zylinderschraube M3×10 (Füsse, von unten in Mutterfalle)", 4, 0.08),
                  ("Weissleim D3 (Lagen verleimen)", 1, 0.30)],
        assembly=[
            "P01 und P02 Rasterlöcher mit 2 M3-Schrauben an gegenüberliegenden Ecken ausrichten, dann flächig dünn verleimen (Schraubzwingen, Zulagen), 2 h trocknen.",
            "Ausrichtschrauben entfernen. Muttern von unten in die Sechskantfallen drücken, wo Module montiert werden.",
            "In die vier Eckfallen (A0, I0, A13, I13) Muttern einlegen, Füsse (P03) mit M3×10 von unten verschrauben.",
        ],
        function_test="Platte auf ebener Fläche: Kippeln < 0.5 mm; M3 in 5 beliebige Fallen eindrehen, Mutter dreht nicht mit.",
    )
