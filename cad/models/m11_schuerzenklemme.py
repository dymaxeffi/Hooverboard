"""M11 – Schürzen-Klemmleiste mit Exzenterspannern (Prüfstand A0, Schürze am Plattformrand).

Hybrid: Klemmleiste gelasert (280 mm gerade, verzugsfrei); Spannbock = flach gedruckte
Basis mit zwei eingesteckten Laserwangen (Wangenprofil exakt, keine Überhänge im Druck);
Exzenterhebel flach gedruckt (Drehloch senkrecht = rund); Bohrschablone geplottet (Karton).
Prinzip: Exzenter e = 1 mm, Kreisradius 8 mm → selbsthemmend bei μ ≥ e/R = 0.125.
"""

from __future__ import annotations

import math

import cadquery as cq
from shapely.geometry import Polygon

from mechlib import fab, geom2d as g2
from mechlib.cadbridge import extrude, xform
from mechlib.common import HC, T, flat_pose, label
from mechlib.module import Module, Part

L_STRIP, W_STRIP, Y_STRIP = 280.0, 20.0, 2.0
PIV = (12.0, 12.0)           # (y, z) Drehpunkt
E_EX, R_EX = 1.0, 8.0
MU = 0.3                     # ANN Holz/PETG
X_CL = (-100.0, 0.0, 100.0)
LEVER_W = 8.0
XW = (LEVER_W / 2 + 0.3, LEVER_W / 2 + 0.3 + T)      # Wangen |x|
BASE = (24.0, 46.0)          # y-Bereich Basis
SCREW_X, SCREW_Y = 13.0, 35.0


def yz_pose(x0, x=0.0):
    """2D (u=y, v=z) Laserteil in YZ-Ebene, Dicke → +x ab x0."""
    return lambda wp: xform(wp, [[0, 0, 1], [1, 0, 0], [0, 1, 0]], (x0 + x, 0, 0))


def cheek_2d():
    arm = g2.slot(PIV, (BASE[0] + 6, 10.0), 12.0)
    body = g2.rect_xy(BASE[0] + 2, 0.0, BASE[1] - 2, 14.0)
    g = arm.union(body).union(g2.circle(14, PIV))
    g = g.difference(g2.rect_xy(-5, -5, BASE[0] - 0.5, Y_STRIP + 0 + T + 1.5).difference(g2.circle(14, PIV)))
    g = g.difference(g2.rect_xy(-5, -5, BASE[0] - 0.5, T + 1.5))   # Freiraum über Leiste (≥ 1.5 mm)
    g = g.difference(g2.rect_xy(-5, -5, BASE[0] + 2, 6.0)).difference(g2.rect_xy(BASE[1] - 2, -5, BASE[1] + 5, 6.0))
    return g.difference(g2.circle(fab.M4_CLR, PIV))


def lever_2d():
    """Exzenterhebel im gespannten Zustand: Exzentermittelpunkt e unter dem Drehpunkt, Griff nach +y."""
    ex = g2.circle(2 * R_EX, (PIV[0], PIV[1] - E_EX))
    handle = g2.slot(PIV, (PIV[0] + 45.0, PIV[1] + 2.0), 10.0)
    return ex.union(handle).difference(g2.circle(fab.M4_CLR + HC, PIV))


def base_part():
    w = 2 * (XW[1] + 9.0)
    b = cq.Workplane("XY").box(w, BASE[1] - BASE[0], 6.0, centered=(True, False, False)).translate((0, BASE[0], 0))
    for sx in (-1, 1):
        x0 = XW[0] if sx > 0 else -XW[1]
        b = b.cut(cq.Workplane("XY").box(T + 0.1, BASE[1] - BASE[0] - 4 + 0.1, 6.0, centered=False)
                  .translate((x0 - 0.05, BASE[0] + 2 - 0.05, 0)))
        b = b.cut(cq.Workplane("XY").circle(2.1).extrude(6).translate((sx * SCREW_X, SCREW_Y, 0)))
        b = b.cut(cq.Workplane("XY").workplane(offset=3.5).circle(2.1).workplane(offset=2.5).circle(4.1).loft()
                  .translate((sx * SCREW_X, SCREW_Y, 0)))
    return b


def build() -> Module:
    strip = g2.rect(L_STRIP, W_STRIP, r=2)
    marks = None
    for x in X_CL:
        m = g2.rect(0.6, 6, (x, W_STRIP / 2 - 3))
        marks = m if marks is None else marks.union(m)
    marks = marks.union(label("M11", (-L_STRIP / 2 + 15, 0), 4.0))
    cheek = cheek_2d()
    lever = lever_2d()
    # Schablone: Kante = Plattformrand, Löcher Ø3.5 = Vorbohrmarke Holzschrauben
    tmpl = g2.rect_xy(-L_STRIP / 2, 0, L_STRIP / 2, 60.0)
    pen = None
    for x in X_CL:
        for sx in (-1, 1):
            tmpl = tmpl.difference(g2.circle(3.5, (x + sx * SCREW_X, SCREW_Y)))
        p = g2.rect(0.4, 50, (x, 30))
        pen = p if pen is None else pen.union(p)
    pen = pen.union(g2.rect_xy(-L_STRIP / 2, Y_STRIP, L_STRIP / 2, Y_STRIP + 0.4)).union(
        g2.rect_xy(-L_STRIP / 2, Y_STRIP + W_STRIP, L_STRIP / 2, Y_STRIP + W_STRIP + 0.4))
    tmpl = g2.round_inner(tmpl, fab.CUT_MIN_RADIUS.value)

    # Kontakt Exzenter ↔ Leistenoberkante (gespannt), Hub, Selbsthemmung
    from shapely import affinity
    contact_gap = lever.distance(g2.rect_xy(Y_STRIP, 0, Y_STRIP + W_STRIP, T))
    lever_open = affinity.rotate(lever, 180, origin=PIV)
    open_gap = lever_open.distance(g2.rect_xy(Y_STRIP, 0, Y_STRIP + W_STRIP, T))
    lever_poses = [yz_pose(-LEVER_W / 2, x) for x in X_CL]
    parts = [
        Part("M11-P01", "Klemmleiste", "laser", "PLY3", 1, profile=strip, engrave=marks,
             poses=[lambda wp: wp.translate((0, Y_STRIP + W_STRIP / 2, 0))], orientation="flach",
             rationale="280 mm gerade Druckleiste: Laser in Sekunden, verzugsfrei; Druck bräuchte 2 h und verzieht."),
        Part("M11-P02", "Spannbock-Basis", "fdm", "PETG", 3, shape=base_part(),
             poses=[(lambda x: (lambda wp: wp.translate((x, 0, 0))))(x) for x in X_CL],
             orientation="flach", rationale="Flaches Teil mit Wangenschlitzen und Senkungen – überhangfrei."),
        Part("M11-P03", "Wange", "laser", "PLY3", 6, profile=cheek,
             poses=[yz_pose(XW[0], x) for x in X_CL] + [yz_pose(-XW[1], x) for x in X_CL],
             orientation="flach", rationale="Wangenprofil mit Drehpunkt als 2D-Kontur exakt; ersetzt einen überhängenden Druck."),
        Part("M11-P04", "Exzenterhebel", "fdm", "PETG", 3, shape=extrude(lever, LEVER_W),
             poses=lever_poses, orientation="flach (Profil in Druckebene), 100 % Infill im Exzenter",
             rationale="Exzenterkontur + Drehloch in Druckebene → rund und genau; 8 mm breit."),
        Part("M11-P05", "Bohrschablone", "plotter", "CARD05", 1, profile=tmpl, engrave=pen, poses=[],
             orientation="Stift: Leistenkanten + Achsmarken; Messer: Kontur + Ø3.5-Körnerlöcher",
             rationale="Flexibel, legt sich an Plattformrand; Plotter zeichnet und schneidet in einem Durchgang."),
    ]
    checks = [
        ("Selbsthemmung Exzenter e < μ·R", E_EX < MU * R_EX, f"e = {E_EX} mm < {MU * R_EX:.1f} mm (μ = {MU}, ANN)"),
        ("Exzenter liegt gespannt an Leiste an (Spalt ≤ 0.05 mm, ohne Gewebe)", contact_gap <= 0.05, f"{contact_gap:.3f} mm"),
        ("Öffnungsspalt ≥ 1.5 mm (Gewebe einlegen)", open_gap >= 1.5, f"{open_gap:.2f} mm"),
        ("Wangen-Mindeststeg", g2.min_web_ok(cheek, fab.LASER_MIN_WEB.value), ""),
    ]
    return Module(
        "m11", "Schürzen-Klemmleiste mit Exzenterspannern",
        "Klemmt Schürzengewebe (0.1–0.5 mm) am Plattformrand des Prüfstands A0 werkzeuglos, wechselbar für "
        "Schürzenvarianten. Je 280 mm Leiste 3 Spanner; Plattformumfang ≈ 2.4 m → 9 Leisten (Eckbereiche gesondert).",
        parts,
        hardware=[("M4×20 + Stoppmutter + 2 Scheiben (Drehpunkt)", 3, 0.20), ("Spanplattenschraube 3.5×16 Senkkopf", 6, 0.03),
                  ("Weissleim (Wangen in Basis)", 1, 0.05)],
        assembly=[
            "Bohrschablone an Plattformkante anlegen, Ø3.5-Löcher ankörnen/vorbohren (Ø2.5), Achsmarken übertragen.",
            "Wangen in Basisschlitze leimen (Drehlöcher fluchtend mit M4-Schraube ausrichten).",
            "Exzenterhebel zwischen die Wangen, M4 mit Stoppmutter (Hebel muss frei drehen).",
            "Spannböcke mit 2× 3.5×16 an den Marken verschrauben.",
            "Gewebe über die Kante legen, Klemmleiste auflegen, Hebel nach innen umlegen.",
        ],
        checks=checks,
        function_test="Gewebestreifen 50 mm breit unter einem Spanner: Auszugskraft ≥ 30 N (Federwaage A0-10) ohne "
                      "Rutschen; Hebel öffnet nicht selbsttätig bei 100 Klopfstössen auf die Plattform.",
    )
