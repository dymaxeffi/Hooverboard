"""M06 – Klinkengesperre (Rücklaufsperre) mit gedrucktem Sperrrad und gelaserter Klinke.

Hybrid: Sperrrad gedruckt (Sägezahn + Nabe, Profil in Druckebene). Klinke aus zwei
verleimten Laserlagen (6 mm) – formgenaue Spitze, die per Konstruktion aus
"Hüllkörper minus aufgeweitetes Rad" entsteht (0.4 mm Spiel). Drehpunkt so gelegt,
dass die Zahnkraft die Klinke ins Rad zieht (selbsteinrastend).
"""

from __future__ import annotations

import math

from shapely import affinity
from shapely.geometry import Point, Polygon

from mechlib import fab, geom2d as g2
from mechlib.common import (T, axis_y_pose, griffhuelse, hub_part, kurbel, label, lagerflansch_608, plate_pose,
                            seitenschild, tube, winkelfuss, winkelfuss_pose)
from mechlib.module import Module, Part

Z, RA, RF, W = 12, 30.0, 24.0, 6.0
ZAX = 45.0
PIV = (-40.0, 29.0)            # Klinkendrehpunkt relativ Radmitte
TAIL = (-56.0, 29.0)
HOOK = (-56.0, 59.0)
YI, YO = 25.0, 25.0 + T
XC = -20.0
CLR = 0.4


def wheel2d(n=12):
    pts = []
    pitch = 2 * math.pi / Z
    for i in range(Z):
        th = math.pi / 2 + i * pitch
        for k in range(n + 1):           # Rampe: RF bei th-pitch → RA bei th
            a = th - pitch + pitch * k / n
            r = RF + (RA - RF) * k / n
            pts.append((r * math.cos(a), r * math.sin(a)))
        pts.append((RF * math.cos(th), RF * math.sin(th)))
    return Polygon(pts).buffer(0)


def pawl2d(wheel):
    rough = g2.slot(TAIL, PIV, 12).union(g2.circle(16, PIV)).union(g2.slot(PIV, (-4.0, 27.5), 10)).union(
        Polygon([(-8, 31.5), (-0.2, 31.5), (-0.2, 24.6), (-8, 24.6)])).difference(
        g2.rect_xy(-31, 10, -7.5, 27.2))                 # Unterseite frei über Nachbarzahn
    p = g2.largest(rough.difference(wheel.buffer(CLR, join_style="mitre")))
    p = g2.largest(p.buffer(-1.0, join_style="round").buffer(1.0, join_style="round"))  # Spitzen/Grate entfernen
    p = p.difference(g2.circle(8.2, PIV)).difference(g2.circle(fab.M3_CLR, TAIL))
    return p


def build() -> Module:
    wheel = wheel2d()
    pawl = pawl2d(wheel)
    # Eingriffstiefe: tiefster Punkt der Klinke im Zahngrund
    depth = RA - min(Point(0, 0).distance(Point(c)) for c in pawl.exterior.coords if c[0] > -6)
    # Selbsteinrastung: Moment der Zahnkraft (−x an Kontakt r≈27) um Drehpunkt
    contact = (0.0, 27.0)
    mz = (contact[0] - PIV[0]) * 0.0 - (contact[1] - PIV[1]) * (-1.0)
    gap = pawl.distance(wheel)

    plate, eng = seitenschild(130, 115, bearings=[(-XC, ZAX)],
                              holes=[(fab.M4_CLR, (PIV[0] - XC, ZAX + PIV[1])), (fab.M3_CLR, (HOOK[0] - XC, ZAX + HOOK[1]))],
                              foot_x=(-40, 40), text="M06 SPERRE")
    s_hub = YI - 1 - (W / 2 + 10)
    s_long = YI - 1 - W / 2
    zk = YO + 4 + 1 + 16
    parts = [
        Part("M06-P01", "Seitenschild", "laser", "PLY3", 2, profile=plate, engrave=eng,
             poses=[plate_pose(YI, x=XC), plate_pose(-YO, x=XC)], orientation="flach",
             rationale="Lage Radachse ↔ Klinkendrehpunkt bestimmt Funktion → Laser legt beide exakt fest."),
        Part("M06-P02", "Lagerflansch 608", "fdm", "PETG", 2, shape=lagerflansch_608(),
             poses=[axis_y_pose(0, ZAX, YO + 4, flip=True), axis_y_pose(0, ZAX, -(YO + 4))],
             orientation="Flansch auf Bett", rationale="Standardelement M01-P04"),
        Part("M06-P03", f"Sperrrad z{Z}", "fdm", "PETG", 1,
             shape=hub_part(affinity.scale(wheel, 1, -1, origin=(0, 0)), W),   # axis_y_pose spiegelt Druck-y
             poses=[axis_y_pose(0, ZAX, -W / 2)], orientation="Scheibe auf Bett, Nabe oben",
             rationale="Sägezahn + Nabe in einem Teil; Zahnflanken als Wände (glatt, masshaltig)."),
        Part("M06-P04", "Klinke", "laser", "PLY3", 2, profile=pawl, engrave=None,
             poses=[plate_pose(0.0, z=ZAX), plate_pose(-T, z=ZAX)], orientation="flach; 2 Lagen verleimt",
             rationale="Klinke ist ein Flachteil mit kritischer Spitzenkontur: Laser formgenau; "
                       "Doppellage 6 mm = Radbreite."),
        Part("M06-P05", "Klinkenachse (Rohr)", "fdm", "PETG", 1, shape=tube(8.0, fab.M4_CLR + 0.1, 2 * YI),
             poses=[axis_y_pose(PIV[0], ZAX + PIV[1], -YI)], orientation="stehend",
             rationale="Gleitlager der Klinke, M4-Schraube klemmt Rohr zwischen den Schilden (versteift Rahmen)."),
        Part("M06-P06", "Klinkenhülse", "fdm", "PETG", 2, shape=tube(12.0, 8.0 + 0.2, YI - T - 0.3),
             poses=[axis_y_pose(PIV[0], ZAX + PIV[1], T + 0.3), axis_y_pose(PIV[0], ZAX + PIV[1], -YI)],
             orientation="stehend", rationale="zentriert Klinke axial"),
        Part("M06-P07", "Distanzhülse Nabe", "fdm", "PETG", 1, shape=tube(11.0, fab.SHAFT_D + 0.3, s_hub),
             poses=[axis_y_pose(0, ZAX, W / 2 + 10)], orientation="stehend", rationale="Axialsicherung"),
        Part("M06-P08", "Distanzhülse lang", "fdm", "PETG", 1, shape=tube(11.0, fab.SHAFT_D + 0.3, s_long),
             poses=[axis_y_pose(0, ZAX, -(YI - 1))], orientation="stehend", rationale="Axialsicherung"),
        Part("M06-P09", "Winkelfuss", "fdm", "PETG", 4, shape=winkelfuss(),
             poses=[winkelfuss_pose(x, s * YO, s) for x in (XC - 40, XC + 40) for s in (1, -1)],
             orientation="liegend", rationale="Standardelement M01-P05"),
        Part("M06-P10", "Kurbel", "fdm", "PETG", 1, shape=kurbel(),
             poses=[axis_y_pose(0, ZAX, zk, flip=True)], orientation="Arm auf Bett", rationale="Antrieb"),
        Part("M06-P11", "Griffhülse", "fdm", "PETG", 1, shape=griffhuelse(),
             poses=[axis_y_pose(40, ZAX, zk)], orientation="stehend", rationale="Griff"),
    ]
    checks = [
        ("Klinke greift ≥ 2 mm in Zahnlücke", depth >= 2.0, f"Eingriffstiefe {depth:.2f} mm (Zahnhöhe {RA - RF:.0f} mm)"),
        ("Klinke berührungsfrei in Ruhelage (Spiel)", gap >= CLR - 0.05, f"Spalt {gap:.2f} mm"),
        ("Selbsteinrastend: Zahnkraft dreht Klinke ins Rad", mz < 0, f"Mz = {mz:.1f}·F (negativ = ins Rad)"),
        ("Klinkenspitze min. Steg ≥ 2 mm", g2.min_web_ok(pawl, fab.LASER_MIN_WEB.value), ""),
    ]
    return Module(
        "m06", "Klinkengesperre (Rücklaufsperre)",
        "Lässt Drehung im Uhrzeigersinn (Blick von −y) frei und sperrt die Gegenrichtung in 30°-Schritten. "
        "Einsatz: Halten von Seilwinden/Höhenverstellungen, Lehrmodell Gesperre.",
        parts,
        hardware=[("Rillenkugellager 608-2RS", 2, 0.80), ("Welle Ø8 h9, 90 mm", 1, 1.8),
                  ("M4×60 + Scheiben + Stoppmutter (Klinkenachse)", 1, 0.25), ("M3×16 + Mutter (Federhaken, Schwanz)", 2, 0.08),
                  ("Zugfeder Ø5×25 oder Gummiring", 1, 0.40), ("M3×12 + Mutter (Flansche)", 6, 0.10),
                  ("M3×10 + Mutter (Winkelfüsse)", 8, 0.10), ("Madenschraube M3×8 + Mutter", 2, 0.08),
                  ("M4×40 + Stoppmutter (Griff)", 1, 0.30), ("Weissleim", 1, 0.05)],
        assembly=[
            "Klinkenlagen verleimen (8-mm-Dorn im Drehloch zum Ausrichten).",
            "Rahmen wie M02 aufbauen, Sperrrad mit Hülsen auf Welle; Nabe Richtung +y.",
            "Klinkenachse: Rohr mit Hülsen und Klinke zwischen die Schilde, M4×60 durch.",
            "Feder von Klinkenschwanz (M3) nach oben zum Federhaken spannen – Klinke liegt mit leichtem Druck auf.",
        ],
        checks=checks,
        function_test="Kurbel in Freilaufrichtung: gleichmässiges Klicken, 12 Rasten/Umdrehung. Gegenrichtung: "
                      "Rad sperrt nach ≤ 30° und hält 2 N·m (50 N an 40-mm-Kurbel) ohne Abrutschen. Lösen durch Druck "
                      "auf Klinkenschwanz.",
    )
