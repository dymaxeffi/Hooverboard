"""Gemeinsamer Flanschstandard der Luftstrecke DN50 (M07–M10).

Flansch Ø84, 4× M4 auf Lochkreis 68 (45°-Lage), lichte Weite 50. Alle Module
sind untereinander und mit dem Prüfstand-Gebläseadapter (A0-03) koppelbar.
Flachdichtungen werden geplottet (Faserdichtungspapier 0.5 mm, Option Silikon 0.5 mm).
"""

from __future__ import annotations

import math

import cadquery as cq

from . import fab, geom2d as g2
from .cadbridge import extrude, teardrop

DN, OD, PCD, FT = fab.DN, fab.FL_OD, fab.FL_PCD, fab.FL_T
TUBE_OD = DN + 6.0
GASKET_T = 0.5


def bolt_pts():
    return [(PCD / 2 * math.cos(math.radians(45 + 90 * k)), PCD / 2 * math.sin(math.radians(45 + 90 * k)))
            for k in range(4)]


def flange_2d(inner=DN, hole=fab.M4_CLR + fab.HOLE_COMP.value, od=OD):
    g = g2.circle(od).difference(g2.circle(inner))
    for p in bolt_pts():
        g = g.difference(g2.circle(hole, p))
    return g


def gasket_2d(inner=DN):
    """Plotterdichtung; Innenecken rund, Löcher ≥ 3 mm (Plotterregel)."""
    return flange_2d(inner, fab.M4_CLR, OD - 0.5)


def tube_body(length, inner=DN, wall=3.0, taps=()):
    """Rohrstück mit Flanschen an beiden Enden, stehend gedruckt (Achse = z).
    taps: Liste z-Positionen radialer Messbohrungen (Ø6.1-Sitz für Messstutzen, Richtung +x)."""
    od = inner + 2 * wall
    body = extrude(g2.circle(od).difference(g2.circle(inner)), length)
    body = body.union(extrude(flange_2d(inner), FT)).union(extrude(flange_2d(inner), FT, length - FT))
    for z in taps:
        r_out = od / 2 + 8
        boss = prism_x(teardrop(12.0, (0, z), up=(0, -1)), 0, r_out)     # Spitze unten → überhangfrei
        body = body.union(boss)
        body = body.cut(prism_x(teardrop(3.2, (0, z), up=(0, 1)), 0, r_out + 1))   # Messbohrung
        body = body.cut(prism_x(teardrop(6.1 + fab.HOLE_COMP.value, (0, z), up=(0, 1)), r_out - 8.5, r_out + 1))  # Stutzensitz
    body = body.cut(cq.Workplane("XY").circle(inner / 2).extrude(length))
    return body


def prism_x(profile_yz, x0, x1):
    """2D-Profil (u = y, v = z) entlang +x von x0 bis x1 extrudieren."""
    from .cadbridge import xform
    return xform(extrude(profile_yz, x1 - x0), [[0, 0, 1], [1, 0, 0], [0, 1, 0]], (x0, 0, 0))


def messstutzen():
    """Schlauchtülle für Schlauch ID 6 mm: Schaft Ø6 (eingeleimt), 2 Widerhaken Ø7.4, Bohrung Ø3."""
    w = cq.Workplane("XY").circle(3.0).extrude(8.0)
    w = w.union(cq.Workplane("XY").workplane(offset=8).circle(4.5).extrude(1.5))      # Bund
    z = 9.5
    for _ in range(2):
        w = w.union(cq.Workplane("XY").workplane(offset=z).circle(3.7).workplane(offset=5).circle(2.9).loft())
        z += 5
    return w.cut(cq.Workplane("XY").circle(1.5).extrude(z))
