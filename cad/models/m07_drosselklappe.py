"""M07 – Drosselklappe DN50 mit gravierter Winkelskala und Klemmhebel.

Hybrid: Gehäuse gedruckt (Rohr + Flansche + Lagerbosse, stehend, überhangfrei durch
Tropfenprofile); Klappenscheibe und Skala gelasert (eben, rund, Skala graviert);
Klappenwelle gedruckt (stehend, Abflachung trägt die Scheibe); Hebel gelasert
(Vierkant exakt); Flanschdichtungen geplottet.
Zweck: Einstellbarer Strömungswiderstand für die Gebläsekennlinie (Prüfstand A0).
"""

from __future__ import annotations

import math

import cadquery as cq
from shapely import affinity
from shapely.geometry import Polygon

from mechlib import fab, geom2d as g2
from mechlib.airline import DN, FT, GASKET_T, gasket_2d, prism_x, tube_body
from mechlib.cadbridge import extrude, printed_from_asm, teardrop, xform
from mechlib.common import HC, T, flat_pose, label
from mechlib.module import Module, Part

LEN = 70.0
ZS = LEN / 2                 # Wellenachse
DS = 10.0                    # Wellendurchmesser
X_SP = 48.0                  # Zapfenbeginn (ausserhalb Flanschradius 42)
SQ = 6.0
D_DISC = DN - 1.0
R_SLOT = 32.0


def yz_pose(x0):
    """2D-Laserteil in YZ-Ebene stellen: 2D-x → y, 2D-y → z (relativ Wellenachse), Dicke → +x ab x0."""
    return lambda wp: xform(wp, [[0, 0, 1], [1, 0, 0], [0, 1, 0]], (x0, 0, ZS))


def d_profile(d=14.0, flat=5.5):
    return g2.circle(d).difference(g2.rect_xy(-10, flat, 10, 10))


def body():
    b = tube_body(LEN)
    boss_l = prism_x(teardrop(18, (0, ZS), up=(0, -1)), -34.0, 0.0)
    boss_r = prism_x(teardrop(18, (0, ZS), up=(0, -1)), 0.0, X_SP)
    spig = prism_x(affinity.translate(d_profile(), 0, ZS), X_SP, X_SP + T)
    b = b.union(boss_l).union(boss_r).union(spig)
    b = b.cut(prism_x(teardrop(DS + 0.3 + HC, (0, ZS), up=(0, 1)), -40, X_SP + T + 1))
    return b.cut(cq.Workplane("XY").circle(DN / 2).extrude(LEN))


def shaft_asm():
    seg = lambda d, x0, x1: prism_x(g2.circle(d, (0, ZS)), x0, x1)
    s = seg(14, -36, -34).union(seg(DS, -34, -25.5))
    half = g2.circle(DS, (0, ZS)).intersection(g2.rect_xy(-6, ZS - 6, 6, ZS))
    s = s.union(prism_x(half, -25.5, 25.5)).union(seg(DS, 25.5, X_SP + T))
    s = s.union(prism_x(g2.rect(SQ, SQ, (0, ZS)), X_SP + T, X_SP + T + 2 * T))
    for x in (-12.0, 12.0):
        s = s.cut(cq.Workplane("XY").circle(fab.M3_CLR / 2).extrude(20).translate((x, 0, ZS - 10)))
    s = s.cut(prism_x(g2.circle(2.5, (0, ZS)), X_SP + T + 2 * T - 8, X_SP + T + 2 * T + 1))
    return s


def build() -> Module:
    disc = g2.circle(D_DISC).difference(g2.circle(fab.M3_CLR, (-12, 0))).difference(g2.circle(fab.M3_CLR, (12, 0)))
    disc_eng = label("M07", (0, 10), 4.0)
    # Skala: Sektor −15…105°, D-Loch, Bogenschlitz 0…90°, Teilstriche 10°
    sector = Polygon([(0, 0)] + [(48 * math.cos(math.radians(a)), 48 * math.sin(math.radians(a))) for a in range(-15, 106, 3)])
    scale = sector.union(g2.circle(30)).difference(d_profile(14.2, 5.6)).difference(g2.arc_slot((0, 0), R_SLOT, 0, 90, 4.6))
    ticks = None
    for a in range(0, 91, 10):
        r1 = 37.5 if a % 30 else 36.0
        l = g2.slot((r1 * math.cos(math.radians(a)), r1 * math.sin(math.radians(a))),
                    (42 * math.cos(math.radians(a)), 42 * math.sin(math.radians(a))), 0.5)
        ticks = l if ticks is None else ticks.union(l)
        if a % 30 == 0:
            ticks = ticks.union(label(str(a), (45.5 * math.cos(math.radians(a + 4)), 45.5 * math.sin(math.radians(a + 4))), 2.8))
    ticks = ticks.union(label("M07", (-8, -20), 3.0)).intersection(scale.buffer(-0.3))
    lever = g2.slot((0, 0), (46, 0), 14).union(g2.circle(16)).difference(g2.rect(SQ + 0.1, SQ + 0.1)) \
        .difference(g2.circle(fab.M4_CLR, (R_SLOT, 0)))
    knob = extrude(g2.circle(20).difference(g2.circle(fab.M4_CLR + HC)), 8).cut(
        extrude(g2.hexagon(fab.M4_NUT_AF + 0.3, rot=30), fab.M4_NUT_H + 0.4, 8 - fab.M4_NUT_H - 0.4))
    for k in range(12):
        knob = knob.cut(cq.Workplane("XY").circle(1.2).extrude(8).translate((10.4 * math.cos(k * math.pi / 6),
                                                                               10.4 * math.sin(k * math.pi / 6), 0)))
    sh_print, sh_pose = printed_from_asm(shaft_asm(), [[0, 1, 0], [0, 0, 1], [1, 0, 0]])
    gasket = gasket_2d()

    # Rotationsfreiheit der Scheibe (Versatz 0…T über Achse)
    r_sweep = math.hypot(D_DISC / 2, T)
    parts = [
        Part("M07-P01", "Gehäuse DN50", "fdm", "PETG", 1, shape=body(), poses=[lambda wp: wp],
             orientation="stehend (Rohrachse = Z), Flansch auf Bett; Bosse als Tropfenprofil stützenfrei",
             rationale="Rohr, Flansche, Lagerbosse und Skalenzapfen bilden eine 3D-Form: nur Druck sinnvoll."),
        Part("M07-P02", "Klappenwelle", "fdm", "PETG", 1, shape=sh_print, poses=[sh_pose],
             orientation="stehend, Kopf auf Bett, 100 % Infill",
             rationale="Kopf, Lagerzapfen, Abflachung und Vierkant in einem Teil; stehend = runde Lagerflächen."),
        Part("M07-P03", "Klappenscheibe", "laser", "PLY3", 1, profile=disc, engrave=disc_eng,
             poses=[flat_pose(ZS)], orientation="flach",
             rationale="Kreisrunde, ebene Scheibe mit 0.5 mm Ringspalt: Laser exakter und verzugsfreier als Druck."),
        Part("M07-P04", "Skalenplatte", "laser", "PLY3", 1, profile=scale, engrave=ticks, poses=[yz_pose(X_SP)],
             orientation="flach, Gravur vorn",
             rationale="Skala gravieren + D-Loch + Bogenschlitz in einem Job; kein Zusatzteil, keine Druckzeit."),
        Part("M07-P05", "Stellhebel", "laser", "PLY3", 2, profile=lever,
             poses=[yz_pose(X_SP + T), yz_pose(X_SP + 2 * T)], orientation="flach, 2 Lagen verleimt",
             rationale="Vierkantloch 6.1 mm passgenau (Kerf kompensiert); Doppellage = 6 mm Vierkantlänge."),
        Part("M07-P06", "Klemmknopf M4", "fdm", "PETG", 1, shape=knob,
             poses=[lambda wp: xform(wp, [[0, 0, -1], [0, 1, 0], [1, 0, 0]], (X_SP, R_SLOT * 0 + 0, ZS)) .translate((0, R_SLOT, 0))],
             orientation="flach, Mutterfalle oben", rationale="Rändelknopf mit eingelegter M4-Mutter, werkzeuglos."),
        Part("M07-P07", "Flanschdichtung", "plotter", "GASKET05", 2, profile=gasket,
             poses=[flat_pose(-GASKET_T), flat_pose(LEN)], orientation="–",
             rationale="0.5 mm Flachdichtung: Messerplotter schneidet ohne Brandkante; Laser für Dichtpapier nicht nötig."),
    ]
    checks = [
        ("Scheibe dreht frei im Rohr (Hüllradius < R)", r_sweep < DN / 2 - 0.15, f"Hüllradius {r_sweep:.2f} mm, R = {DN / 2} mm"),
        ("Skalen-/Hebelebene ausserhalb Flansch (x > 42)", X_SP > fab.FL_OD / 2, f"x = {X_SP} mm"),
        ("Vierkant passt durch Lagerbohrung (Montage)", math.hypot(SQ, SQ) < DS + 0.3, f"Diagonale {math.hypot(SQ, SQ):.2f} mm"),
    ]
    return Module(
        "m07", "Drosselklappe DN50 mit Winkelskala",
        "Stufenlos einstellbarer Strömungswiderstand 0–90° (klemmbar). Mit M08 ergibt sich die Gebläsekennlinie "
        "p(Q) am Prüfstand A0 ohne Blendenwechsel. Keine Absperrarmatur (Ringspalt 0.5 mm).",
        parts,
        hardware=[("M3×12 + Mutter (Scheibe)", 2, 0.06), ("M3×8 Blechschraube + Scheibe Ø9 (Hebelsicherung)", 1, 0.05),
                  ("M4×16 + Scheibe (Klemmung)", 1, 0.06), ("Mutter M4 (im Knopf)", 1, 0.03),
                  ("M4×20 + Mutter (Flansch, je Verbindung)", 4, 0.10), ("Weissleim", 1, 0.05)],
        assembly=[
            "Welle von −x durch Gehäuse schieben, Abflachung nach oben (Klappe zu = Scheibe waagrecht).",
            "Scheibe von oben ins Rohr legen, auf Abflachung mit 2× M3×12 verschrauben (Muttern unten).",
            "Skalenplatte auf D-Zapfen stecken (0° = Scheibe zu).",
            "Hebellagen verleimen, auf Vierkant stecken, mit Blechschraube + Scheibe axial sichern.",
            "M4×16 von vorn durch Hebel und Bogenschlitz, Klemmknopf hinten aufdrehen.",
            "Flanschdichtungen beidseitig, 4× M4 je Flansch über Kreuz anziehen.",
        ],
        checks=checks,
        function_test="Hebel 0–90° leichtgängig (< 0.1 N·m), Klemmung hält bei 1 kPa Vordruck. Leckstrom bei 0° "
                      "mit Gebläse messen und dokumentieren (Ringspalt bewusst, kein Absperrorgan).",
    )
