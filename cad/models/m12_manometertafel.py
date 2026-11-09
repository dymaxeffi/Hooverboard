"""M12 – U-Rohr-Manometertafel mit verschiebbarer Nullpunktskala (BOM A0-07).

Hybrid: Tafel gelasert (Löcher + Beschriftung graviert); Skalenstreifen geplottet
(Stift zeichnet mm-Teilung, Messer schneidet Kontur) – billig, austauschbar, in den
gedruckten Führungen verschiebbar → Nullpunkt ohne Nachfüllen einstellen;
Schlauchclips und Führungen gedruckt; Aufstellung mit Standard-Winkelfüssen.
"""

from __future__ import annotations

import math

import cadquery as cq

from mechlib import fab, geom2d as g2
from mechlib.cadbridge import extrude, xform
from mechlib.common import HC, T, label, plate_pose, winkelfuss, winkelfuss_pose
from mechlib.module import Module, Part

W, H = 160.0, 248.0
X_LEG, R_BEND, Y_BEND = 30.0, 30.0, 50.0
Y0, RANGE = 145.0, 90                    # Nullpunkt, ± Skalenbereich je Schenkel (mm)
X_STRIP, W_STRIP, L_STRIP = 50.0, 20.0, 2 * RANGE + 20
TUBE_OD = 8.0
CLIP_Y = (70.0, 145.0, 220.0)
GUIDE_Y = (Y0 - RANGE + 5, Y0 + RANGE - 5)
RHO_W, G = 998.0, 9.81
FRONT = [[-1, 0, 0], [0, -1, 0], [0, 0, 1]]   # Druck-y (Höhe über Fuss) → −y (vor die Tafel), Druck-z → Höhe


def clip():
    """Schlauchclip OD8: C-Ring 270°, Fuss mit M3-Loch. Flach gedruckt (Profil in XY)."""
    ring = g2.circle(TUBE_OD + 3.2, (0, TUBE_OD / 2 + 1.6)).difference(g2.circle(TUBE_OD + 0.2, (0, TUBE_OD / 2 + 1.6)))
    ring = ring.difference(g2.rect_xy(-TUBE_OD * 0.42, TUBE_OD / 2 + 3.5, TUBE_OD * 0.42, 20))   # Einschnapp-Öffnung
    foot = g2.rect_xy(-11, 0, 11, 2.5)
    g = ring.union(foot)
    body = extrude(g, 8.0)
    for x in (-7.5, 7.5):
        body = body.cut(xform(extrude(g2.circle(fab.M3_CLR + HC), 4), [[1, 0, 0], [0, 0, 1], [0, -1, 0]], (x, -1, 4)))
    return body


def guide():
    """Skalenführung: U-Kanal über Streifen (0.45 mm Karton + 0.25 Spiel), 2× M3."""
    g = g2.rect_xy(-W_STRIP / 2 - 8, 0, W_STRIP / 2 + 8, 3.0).difference(g2.rect_xy(-W_STRIP / 2 - 0.3, 0, W_STRIP / 2 + 0.3, 0.8))
    body = extrude(g, 10.0)
    for x in (-W_STRIP / 2 - 4, W_STRIP / 2 + 4):
        body = body.cut(xform(extrude(g2.circle(fab.M3_CLR + HC), 4), [[1, 0, 0], [0, 0, 1], [0, -1, 0]], (x, -0.5, 5)))
    return body


def scale_strip():
    s = g2.rect(W_STRIP, L_STRIP, r=1.0)
    pen = None
    for k in range(-RANGE, RANGE + 1):
        w = 8.0 if k % 10 == 0 else (5.0 if k % 5 == 0 else 3.0)
        l = g2.rect_xy(-W_STRIP / 2 + 0.8, k - 0.15, -W_STRIP / 2 + 0.8 + w, k + 0.15)
        pen = l if pen is None else pen.union(l)
        if k % 10 == 0:
            pen = pen.union(g2.text(str(abs(k)), 3.0, (W_STRIP / 2 - 5.0, k)))
    return s, pen


def build() -> Module:
    board = g2.rect_xy(-W / 2, 0, W / 2, H / 2).union(g2.rect(W, H, (0, H / 2), r=5))
    eng = label("M12 U-ROHR  Δp = ρ·g·(h1+h2)", (0, H - 8), 3.5).union(label("1 mm WS = 9.8 Pa", (0, H - 15), 3.0))
    for y in CLIP_Y:
        for sx in (-1, 1):
            for dx in (-7.5, 7.5):
                board = board.difference(g2.circle(fab.M3_CLR, (sx * X_LEG + dx, y)))
    for sx in (-1, 1):                        # Bogenclip unten
        board = board.difference(g2.circle(fab.M3_CLR, (sx * 7.5, Y_BEND - R_BEND)))
    for y in GUIDE_Y:
        for sx in (-1, 1):
            for dx in (-W_STRIP / 2 - 4, W_STRIP / 2 + 4):
                board = board.difference(g2.circle(fab.M3_CLR, (sx * X_STRIP + dx, y)))
    for x in (-40.0, 40.0):
        board = board.difference(g2.circle(fab.M3_CLR, (x, 10.0)))
    board = board.difference(g2.circle(6.0, (0, H - 25)))    # Aufhängeloch
    strip, pen = scale_strip()
    # Clips auf Vorderseite (−y), Tafel y 0..T
    clip_poses = []
    for y in CLIP_Y:
        for sx in (-1, 1):
            clip_poses.append((lambda x, z: (lambda wp: xform(wp, FRONT, (x, 0, z - 4))))(sx * X_LEG, y))
    clip_poses.append(lambda wp: xform(wp, FRONT, (0, 0, Y_BEND - R_BEND - 4)))
    guide_poses = [(lambda x, z: (lambda wp: xform(wp, FRONT, (x, 0, z - 5))))(sx * X_STRIP, y)
                   for y in GUIDE_Y for sx in (-1, 1)]
    dp_range = RHO_W * G * 2 * RANGE / 1000
    parts = [
        Part("M12-P01", "Tafel", "laser", "PLY3", 1, profile=board, engrave=eng, poses=[plate_pose(0.0)],
             orientation="flach, Gravur vorn",
             rationale="Grosse ebene Tafel mit 36 Bohrungen + Formel graviert: Laser; fällt in 300×250-Feld."),
        Part("M12-P02", "Schlauchclip OD8", "fdm", "PETG", 7, shape=clip(), poses=clip_poses,
             orientation="flach (C-Profil in Druckebene)", rationale="Schnappring braucht Elastizität von PETG."),
        Part("M12-P03", "Skalenführung", "fdm", "PETG", 4, shape=guide(), poses=guide_poses,
             orientation="flach", rationale="Kanal 0.8 mm hält Karton reibschlüssig, verschiebbar."),
        Part("M12-P04", "Skalenstreifen ±90 mm", "plotter", "CARD05", 2, profile=strip, engrave=pen, poses=[],
             orientation="Stift: Teilung + Ziffern, dann Messer: Kontur",
             rationale="Plotter zeichnet 1-mm-Teilung (Stift) und schneidet aus; austauschbar, Nullpunkt verschiebbar."),
        Part("M12-P05", "Winkelfuss", "fdm", "PETG", 4, shape=winkelfuss(),
             poses=[winkelfuss_pose(x, T, 1) for x in (-40, 40)] + [winkelfuss_pose(x, 0.0, -1) for x in (-40, 40)],
             orientation="liegend", rationale="Standardelement M01-P05"),
    ]
    checks = [
        ("Biegeradius U-Bogen ≥ 30 mm (PU 8/6, ANN)", R_BEND >= 30, f"R = {R_BEND} mm"),
        ("Messbereich ≥ ±1.5 kPa (Kissendruck Phase 0 ≈ 1.1 kPa)", dp_range >= 1500, f"±{dp_range:.0f} Pa (Summe beider Schenkel)"),
        ("Skalenstreifen in Plotterfläche", L_STRIP <= fab.CUT_AREA_Y.value - 10, f"{L_STRIP:.0f} mm"),
        ("Schenkel-Abstand ≥ 2·Biegeradius", 2 * X_LEG >= 2 * R_BEND, f"{2 * X_LEG:.0f} mm"),
    ]
    return Module(
        "m12", "U-Rohr-Manometertafel mit Nullpunktskala",
        "Differenzdruckmessung (Kissendruck, Blenden-Δp M08, Öffnungsdruck M09) ohne Elektronik. Wasser mit "
        "Lebensmittelfarbe; Ablesung beider Schenkel, Δp = ρ·g·(h₁+h₂).",
        parts,
        hardware=[("PU-Schlauch 8×6 mm transparent, 0.8 m (kein PVC nötig)", 1, 2.5), ("M3×10 + Mutter (Clips, Führungen)", 22, 0.08),
                  ("M3×10 + Mutter (Winkelfüsse)", 8, 0.08), ("Lebensmittelfarbe, Wasser", 1, 0.20)],
        assembly=[
            "Clips und Skalenführungen auf die Tafel schrauben (Muttern hinten).",
            "Schlauch als U einclipsen (Bogen unten), Enden über Messstutzen (M08/M09) bzw. offen.",
            "Wasser einfüllen bis ≈ Mitte, Blasen entfernen; Tafel mit Wasserwaage lotrecht stellen.",
            "Skalenstreifen in die Führungen schieben und auf Meniskus-Unterkante auf 0 stellen.",
        ],
        checks=checks,
        function_test="Beide Schenkel offen: Pegel gleich (±0.5 mm). Einseitig Spritze 100 mm WS: h₁+h₂ = 100 ± 2 mm; "
                      "nach 10 min kein Pegelabfall (dicht).",
    )
