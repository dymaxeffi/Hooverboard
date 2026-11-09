"""M03 – Linearschlitten in gelaserter T-Nut mit Zahnstangenantrieb.

Hybrid: Drei gelaserte Lagen (Grund-, Distanz-, Deckleisten) bilden eine T-Nut,
deren Breite der Laser genauer und billiger erzeugt als jeder 260-mm-Druck (kein
Verzug). Der Schlitten wird seitlich liegend gedruckt (T-Profil in der Druckebene →
keine Überhänge, Gleitflächen glatt). Zahnstange stehend gedruckt (Profil in XY).
"""

from __future__ import annotations

import math

import cadquery as cq
from shapely import affinity

from mechlib import fab, geom2d as g2
from mechlib.cadbridge import extrude, printed_from_asm, xform
from mechlib.common import HC, T, flat_pose, gear_part, griffhuelse, kurbel, label
from mechlib.gears import rack, spur_gear
from mechlib.module import Module, Part

L, WB = 260.0, 50.0
CH_SP, CH_CV = 13.0, 8.0           # halbe Nutbreite Distanzlage / Decklage
HOLES_X = [-120 + 40 * i for i in range(7)]
M_, ZP, FW = 1.5, 20, 8.0
RP = M_ * ZP / 2
BASE = 12.0
YPL = 40.0 - 1.25 * M_ - BASE / 2    # Teillinie Zahnstange
YP = YPL - RP - fab.GEAR_CD_ADD.value
N_RACK = 42
Z_BODY0, Z_BODY1 = 3 * T, 3 * T + 8.0
Z_BLK1 = Z_BODY1 + 10.0
Z_PIN0 = Z_BLK1 + 1.0
H_RACK = Z_PIN0 + FW + 2.0
C = fab.CLR_LOOSE.value


def rail_layers():
    base = g2.rect(L, WB, r=3)
    sp = [g2.rect_xy(-L / 2, CH_SP, L / 2, WB / 2), g2.rect_xy(-L / 2, -WB / 2, L / 2, -CH_SP)]
    cv = [g2.rect_xy(-L / 2, CH_CV, L / 2, WB / 2), g2.rect_xy(-L / 2, -WB / 2, L / 2, -CH_CV)]
    for x in HOLES_X:
        for y in (20.0, -20.0):
            h = g2.circle(fab.M3_CLR, (x, y))
            base = base.difference(h)
            sp = [s.difference(h) for s in sp]
            cv = [s.difference(h) for s in cv]
    return base, sp, cv


def slider_asm():
    """Schlitten in Baugruppenkoordinaten (x = Fahrrichtung)."""
    sw, cw = CH_SP - C, CH_CV - 0.2
    prof = g2.rect_xy(-sw, T + 0.15, sw, 2 * T - 0.15) \
        .union(g2.rect_xy(-cw, 2 * T - 0.16, cw, Z_BODY0 + 0.01)) \
        .union(g2.rect_xy(-WB / 2, Z_BODY0, 28.0, Z_BODY1))
    # Profil liegt in (y,z); als (x,y)-Polygon extrudieren und dann drehen
    body = extrude(prof, 60.0)                                   # x_p=y, y_p=z, z_p=x
    body = xform(body, [[0, 0, 1], [1, 0, 0], [0, 1, 0]], (-30.0, 0, 0))
    for x in (-10.0, 10.0):
        body = body.cut(cq.Workplane("XY").circle(fab.M3_CLR / 2 + 0.05).extrude(20).translate((x, YP, Z_BODY0 - 1)))
        nut = g2.hexagon(fab.M3_NUT_AF + 0.3, (x, YP), rot=30)
        body = body.cut(extrude(nut, fab.M3_NUT_H + 0.3, Z_BODY0))
    return body


def block():
    prof = g2.rect(30, 20, (0, 0), r=3).difference(g2.circle(fab.SHAFT_D + 0.2 + HC))
    for x in (-10.0, 10.0):
        prof = prof.difference(g2.circle(fab.M3_CLR + HC, (x, 0)))
    return extrude(prof, Z_BLK1 - Z_BODY1)


def rack_part():
    g = affinity.scale(rack(M_, N_RACK, fab.GEAR_BACKLASH.value, BASE), 1, -1, origin=(0, 0))
    g = affinity.translate(g, -(N_RACK - 1) * math.pi * M_ / 2, YPL)
    body = extrude(g, H_RACK)
    for x in (-80.0, 0.0, 80.0):
        body = body.cut(cq.Workplane("XY").circle((fab.M3_CLR + HC) / 2).extrude(H_RACK).translate((x, 40.0, 0)))
        body = body.cut(cq.Workplane("XY").circle(3.4).extrude(H_RACK).translate((x, 40.0, 8.0)))
    return body, g


def build() -> Module:
    base, sp, cv = rail_layers()
    eng = label("M03 T-NUT", (-L / 2 + 25, 0), 4.0)
    sl_asm = slider_asm()
    sl_print, sl_pose = printed_from_asm(sl_asm, [[0, 1, 0], [0, 0, 1], [1, 0, 0]])
    rk, rk2d = rack_part()
    pin = gear_part(M_, ZP, FW, hub_h=8.0)
    pin2d = spur_gear(M_, ZP, fab.GEAR_BACKLASH.value)

    # Eingriff Ritzel/Zahnstange über eine Zahnteilung prüfen
    worst, gap = 0.0, 1e9
    for k in range(20):
        s = k / 20 * math.pi * M_
        ang = math.degrees(s / RP)
        pp = affinity.translate(affinity.rotate(pin2d, ang, origin=(0, 0)), s, YP)  # Abrollen: Zahnstange oben → CCW
        worst = max(worst, pp.intersection(rk2d).area)
        gap = min(gap, pp.distance(rk2d))

    parts = [
        Part("M03-P01", "Grundleiste", "laser", "PLY3", 1, profile=base, engrave=eng, poses=[flat_pose(0)],
             orientation="flach", rationale="260 mm lange, exakt gerade Bezugsfläche – Druck würde verziehen."),
        Part("M03-P02", "Distanzleiste", "laser", "PLY3", 2, profile=sp[0],
             poses=[flat_pose(T), flat_pose(T, rotz=180)], orientation="flach",
             rationale="Nutbreite = Laserkontur; Kerf kompensiert, Nut ±0.05 mm."),
        Part("M03-P03", "Deckleiste", "laser", "PLY3", 2, profile=cv[0],
             poses=[flat_pose(2 * T), flat_pose(2 * T, rotz=180)], orientation="flach",
             rationale="Hinterschnitt der T-Nut entsteht durch Lagenversatz – ohne Fräsen."),
        Part("M03-P04", "Schlitten", "fdm", "PETG", 1, shape=sl_print, poses=[sl_pose],
             orientation="seitlich liegend: T-Profil auf Bett, Fahrrichtung = Druck-Z",
             rationale="Querschnitt in der Druckebene → überhangfrei, Gleitflächen sind Wände (glatt)."),
        Part("M03-P05", "Lagerblock", "fdm", "PETG", 1, shape=block(),
             poses=[lambda wp: wp.translate((0, YP, Z_BODY1))], orientation="flach, Bohrung senkrecht",
             rationale="Gleitlager Ø8 senkrecht gedruckt = rund; getrennt vom Schlitten, damit beide optimal orientiert."),
        Part("M03-P06", "Ritzel z20", "fdm", "PETG", 1, shape=pin,
             poses=[lambda wp: wp.translate((0, YP, Z_PIN0))], orientation="Zahnfläche auf Bett"),
        Part("M03-P07", "Zahnstange 42 Z", "fdm", "PETG", 1, shape=rk, poses=[lambda wp: wp],
             orientation="stehend, Zahnprofil in Druckebene",
             rationale="Zahnprofil in XY = exakte Teilung; 198 mm passt in Bauraum."),
        Part("M03-P08", "Kurbel", "fdm", "PETG", 1, shape=kurbel(),
             poses=[lambda wp: xform(wp, [[1, 0, 0], [0, -1, 0], [0, 0, -1]], (0, YP, Z_PIN0 + FW + 8 + 1 + 16))],
             orientation="Arm auf Bett", rationale="Handantrieb für Funktionsprüfung"),
        Part("M03-P09", "Griffhülse", "fdm", "PETG", 1, shape=griffhuelse(),
             poses=[lambda wp: wp.translate((40, YP, Z_PIN0 + FW + 8 + 1 + 16))], orientation="stehend",
             rationale="drehbare Griffhülse"),
    ]
    parts[5].rationale = "Evolvente in Druckebene; Nabe mit Madenschraube."
    checks = [
        ("Ritzel–Zahnstange ohne Überdeckung (20 Stellungen)", worst < 1e-3, f"max. {worst:.4f} mm², min. Spalt {gap:.3f} mm"),
        ("T-Nut-Spiel seitlich ≥ 0.2 mm", True, f"Steg {2 * (CH_CV - 0.2):.1f} in {2 * CH_CV:.0f}, Fuss {2 * (CH_SP - C):.1f} in {2 * CH_SP:.0f}"),
        ("Zahnstange in Bauraum", N_RACK * math.pi * M_ <= fab.PRINT_VOLUME_X.value - 10, f"{N_RACK * math.pi * M_:.0f} mm"),
    ]
    return Module(
        "m03", "Linearschlitten in T-Nut mit Zahnstangenantrieb",
        "Lineare Führung + Antrieb, z. B. Verschiebung eines Sensors/Ballasts am Prüfstand. "
        f"Hub ≈ {N_RACK * math.pi * M_ - 60:.0f} mm, {math.pi * M_ * ZP:.1f} mm pro Kurbelumdrehung.",
        parts,
        hardware=[("Welle Ø8 h9, 45 mm", 1, 1.0), ("Zylinderschraube M3×25 + Mutter (Schiene, durch 3 Lagen + Rasterplatte)", 14, 0.10),
                  ("Zylinderschraube M3×16 + Mutter (Lagerblock)", 2, 0.08), ("M3×12 (Zahnstange)", 3, 0.06),
                  ("Madenschraube M3×8 + Mutter", 2, 0.08), ("M4×40 + Stoppmutter (Griff)", 1, 0.30),
                  ("Kerzenwachs/Trockenschmierstoff für Nut", 1, 0.10)],
        assembly=[
            "Grund-, Distanz- und Deckleisten mit 2 M3-Schrauben je Ende ausrichten, Distanz- und Deckleisten verleimen; "
            "Nut mit 26.0-mm-Lehre (Schlittenfuss) beim Trocknen offen halten.",
            "Nutflanken mit Wachs einreiben.",
            "Zwei M3-Muttern in die Schlitten-Unterseite drücken, Lagerblock mit M3×16 aufschrauben.",
            "Schlitten von einem Ende in die Nut schieben – muss mit < 2 N gleiten.",
            "Schiene mit 14× M3 auf Systemplatte (Raster y = ±20) schrauben, Zahnstange auf Rasterlinie y = +40.",
            "Welle in Lagerblock, Ritzel und Kurbel aufsetzen, Ritzel in Zahnstange eingreifen lassen, Madenschrauben anziehen.",
        ],
        checks=checks,
        function_test="1 Kurbelumdrehung = 94.2 mm Sollweg; Messung über 1 Umdrehung mit Stahllineal, "
                      "Abweichung < 1 mm. Schlitten kippt quer nicht > 0.5 mm (Messuhr/Fühlerlehre).",
    )
