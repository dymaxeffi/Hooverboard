"""M04 – Nockentrieb mit gelasertem Gabel-Schwinghebel und gedruckten Gelenken.

Hybrid: Nocken gedruckt (beliebige Kontur, Nabe integriert); Schwinghebel als zwei
gelaserte Gabelplatten (steif, leicht, exakte Gelenkabstände), Gelenke als gedruckte
Rohr-/Distanzhülsen; Gestell = Doppelrahmen wie M02. Skala auf Seitenschild graviert.
Bewegungsgesetz: Zykloide (ruckbegrenzt), Hub 10 mm über 180°, Rücklauf 180°.
"""

from __future__ import annotations

import math

from shapely.geometry import Polygon

from mechlib import fab, geom2d as g2
from mechlib.common import (T, axis_y_pose, griffhuelse, hub_part, kurbel, lagerflansch_608, plate_pose,
                            seitenschild, tube, winkelfuss, winkelfuss_pose)
from mechlib.module import Module, Part

R0, RR, H = 25.0, 8.0, 10.0
ZAX = 45.0
XP, ZP = 70.0, ZAX + R0 + RR + H / 2      # Hebeldrehpunkt
XT = -30.0                                # Hebelspitze
YI, YO = 25.0, 25.0 + T
XC = 20.0                                 # Mitte Seitenschild
GAP = 8.4                                 # lichte Gabelweite
CW = 8.0                                  # Nockenbreite


def lift(th):
    """Zykloidisches Hubgesetz, th in rad 0..2π."""
    th %= 2 * math.pi
    if th <= math.pi:
        u = th / math.pi
        return H * (u - math.sin(2 * math.pi * u) / (2 * math.pi))
    u = (th - math.pi) / math.pi
    return H * (1 - (u - math.sin(2 * math.pi * u) / (2 * math.pi)))


def cam_profile(n=720):
    pitch = Polygon([((R0 + RR + lift(2 * math.pi * i / n)) * math.cos(2 * math.pi * i / n),
                      (R0 + RR + lift(2 * math.pi * i / n)) * math.sin(2 * math.pi * i / n)) for i in range(n)])
    return pitch, pitch.buffer(-RR, quad_segs=32)


def pressure_angle_max(n=720):
    worst = 0.0
    for i in range(n):
        th = 2 * math.pi * i / n
        ds = (lift(th + 1e-4) - lift(th - 1e-4)) / 2e-4
        worst = max(worst, math.degrees(math.atan2(abs(ds), R0 + RR + lift(th))))
    return worst


def build() -> Module:
    pitch, cam = cam_profile()
    from shapely import affinity
    cam_asm = affinity.translate(affinity.scale(cam, 1, -1, origin=(0, 0)), 0, ZAX)   # Druck-y → −z
    contact_gap = cam_asm.distance(g2.circle(2 * RR, (0.0, ZP)))
    undercut = abs(cam.buffer(RR, quad_segs=32).area - pitch.area) / pitch.area
    pa = pressure_angle_max()

    window = g2.rect_xy(XT - 10 - XC, ZP - 14, XT + 10 - XC, ZP + 14)
    plate, eng = seitenschild(130, 110, bearings=[(-XC, ZAX)], holes=[(fab.SHAFT_D + 0.2, (XP - XC, ZP)),
                                                                     (fab.M3_CLR, (XT - XC, 30.0))],
                              extra_cut=window.buffer(3, join_style="round"), foot_x=(-40, 40), text="M04 NOCKEN h=10")
    ticks = None
    for k in range(-8, 9):
        w = 6.0 if k % 5 == 0 else 3.5
        t = g2.rect_xy(XT + 13 - XC + 0.0, ZP + k - 0.15, XT + 13 - XC + w, ZP + k + 0.15)
        ticks = t if ticks is None else ticks.union(t)
    eng = eng.union(ticks)

    lever = g2.slot((XP, ZP), (XT, ZP), 16.0)
    lever = lever.difference(g2.circle(12.0, (XP, ZP))).difference(g2.circle(fab.M4_CLR, (0.0, ZP))) \
        .difference(g2.circle(fab.M3_CLR, (XT, ZP)))
    lever_eng = g2.text("M04", 4.0, ((XP + XT) / 2 + 15, ZP))

    lf = lagerflansch_608()
    s_hub = YI - 1 - (CW / 2 + 10)
    s_long = YI - 1 - CW / 2
    s_piv = YI - (GAP / 2 + T)
    zk = ZP + 1 + 16
    parts = [
        Part("M04-P01", "Seitenschild", "laser", "PLY3", 2, profile=plate, engrave=eng,
             poses=[plate_pose(YI, x=XC), plate_pose(-YO, x=XC)], orientation="flach",
             rationale="Lagerlage, Drehpunkt und Skala in einem Laserjob – Abstände exakt, Skala ohne Zusatzteil."),
        Part("M04-P02", "Lagerflansch 608", "fdm", "PETG", 2, shape=lf,
             poses=[axis_y_pose(0, ZAX, YO + 4, flip=True), axis_y_pose(0, ZAX, -(YO + 4))],
             orientation="Flansch auf Bett", rationale="Standardelement M01-P04"),
        Part("M04-P03", "Nocken zykloid h10", "fdm", "PETG", 1, shape=hub_part(cam, CW, smooth=True),
             poses=[axis_y_pose(0, ZAX, -CW / 2)], orientation="Scheibe auf Bett, Nabe oben",
             rationale="Freiformkontur + Nabe in einem Teil; Kontur in Druckebene = formgenau."),
        Part("M04-P04", "Hebelplatte", "laser", "PLY3", 2, profile=lever, engrave=lever_eng,
             poses=[plate_pose(GAP / 2), plate_pose(-GAP / 2 - T)], orientation="flach",
             rationale="Langer, schlanker Hebel: Sperrholz ist in Längsrichtung steifer als FDM-Schichten "
                       "und verzugsfrei; Lochabstände exakt."),
        Part("M04-P05", "Gelenkrohr", "fdm", "PETG", 1, shape=tube(12.0, fab.SHAFT_D + 0.3, GAP + 2 * T),
             poses=[axis_y_pose(XP, ZP, -GAP / 2 - T)], orientation="stehend",
             rationale="Gleitlager auf Ø8-Bolzen, in Hebelplatten eingeleimt."),
        Part("M04-P06", "Gabelhülse", "fdm", "PETG", 1, shape=tube(16.0, 12.0 + 0.1, GAP),
             poses=[axis_y_pose(XP, ZP, -GAP / 2)], orientation="stehend",
             rationale="hält Gabelweite exakt; einfacher Druck ohne Überhang (statt Bundbuchse)."),
        Part("M04-P07", "Rolle", "fdm", "PETG", 1, shape=tube(2 * RR, fab.M4_CLR + 0.1, GAP - 0.4),
             poses=[axis_y_pose(0, ZP, -(GAP - 0.4) / 2)], orientation="stehend",
             rationale="Rollenstössel senkt Reibung gegenüber Gleitstössel."),
        Part("M04-P08", "Spitzenhülse", "fdm", "PETG", 1, shape=tube(8.0, fab.M3_CLR, GAP),
             poses=[axis_y_pose(XT, ZP, -GAP / 2)], orientation="stehend", rationale="Zeiger + Federhaken"),
        Part("M04-P09", f"Drehpunkthülse {s_piv:.1f}", "fdm", "PETG", 2, shape=tube(12.0, fab.SHAFT_D + 0.3, s_piv),
             poses=[axis_y_pose(XP, ZP, GAP / 2 + T), axis_y_pose(XP, ZP, -YI)], orientation="stehend",
             rationale="zentriert Hebel zwischen den Schilden"),
        Part("M04-P10", "Distanzhülse Nabe", "fdm", "PETG", 1, shape=tube(11.0, fab.SHAFT_D + 0.3, s_hub),
             poses=[axis_y_pose(0, ZAX, CW / 2 + 10)], orientation="stehend", rationale="Axialsicherung"),
        Part("M04-P11", "Distanzhülse lang", "fdm", "PETG", 1, shape=tube(11.0, fab.SHAFT_D + 0.3, s_long),
             poses=[axis_y_pose(0, ZAX, -(YI - 1))], orientation="stehend", rationale="Axialsicherung"),
        Part("M04-P12", "Winkelfuss", "fdm", "PETG", 4, shape=winkelfuss(),
             poses=[winkelfuss_pose(x, s * YO, s) for x in (XC - 40, XC + 40) for s in (1, -1)],
             orientation="liegend", rationale="Standardelement M01-P05"),
        Part("M04-P13", "Kurbel", "fdm", "PETG", 1, shape=kurbel(),
             poses=[axis_y_pose(0, ZAX, YO + 4 + 1 + 16, flip=True)], orientation="Arm auf Bett",
             rationale="Handantrieb"),
        Part("M04-P14", "Griffhülse", "fdm", "PETG", 1, shape=griffhuelse(),
             poses=[axis_y_pose(40, ZAX, YO + 4 + 1 + 16)], orientation="stehend", rationale="Griff"),
    ]
    checks = [
        ("Nocken ohne Unterschnitt (Krümmung Bahnkurve > Rollenradius)", undercut < 0.002, f"Flächenabweichung {undercut * 100:.3f} %"),
        ("Max. Druckwinkel ≤ 30°", pa <= 30, f"{pa:.1f}°"),
        ("Rolle berührt Nocken in Baugruppe (Spalt ≤ 0.05 mm)", contact_gap <= 0.05,
         f"Spalt {contact_gap:.3f} mm bei Hub h/2"),
        ("Spitzenweg ±7 mm innerhalb Sichtfenster ±14 mm", H / 2 * (XP - XT) / XP <= 14, f"±{H / 2 * (XP - XT) / XP:.1f} mm"),
    ]
    return Module(
        "m04", "Nockentrieb mit Gabel-Schwinghebel",
        "Wandelt Drehung in definierte Schwingbewegung (Zykloide, Hub 10 mm, Übersetzung an der Spitze 1.43). "
        "Basis für Takt-/Ventilmechaniken; Hebelweg an gravierter Skala ablesbar.",
        parts,
        hardware=[("Rillenkugellager 608-2RS", 2, 0.80), ("Welle Ø8 h9, 90 mm (Nocken)", 1, 1.8),
                  ("Bolzen Ø8 h9, 65 mm (Drehpunkt) + 2 Stellringe DIN 705 Ø8", 1, 2.5),
                  ("M4×20 + Stoppmutter (Rollenachse)", 1, 0.15), ("M3×16 + Mutter (Spitze, Federhaken)", 2, 0.08),
                  ("Zugfeder Ø6×30, ca. 0.2 N/mm, oder Gummiring", 1, 0.40), ("M3×12 + Mutter (Flansche)", 6, 0.10),
                  ("M3×10 + Mutter (Winkelfüsse)", 8, 0.10), ("Madenschraube M3×8 + Mutter", 2, 0.08),
                  ("M4×40 + Stoppmutter (Griff)", 1, 0.30), ("Weissleim", 1, 0.10)],
        assembly=[
            "Gelenkrohr durch beide Hebelplatten, Gabelhülse dazwischen; Hebelplatten bündig aufleimen, Rolle mit M4 einsetzen (Achse nicht klemmen).",
            "Lager in Flansche pressen, Flansche in Seitenschilde schrauben, Winkelfüsse montieren.",
            "Nockenwelle wie bei M02 mit Distanzhülsen einsetzen; Nocken so drehen, dass die Rolle auf dem Grundkreis steht.",
            "Drehpunktbolzen durch Schild, Drehpunkthülse, Gelenkrohr, Hülse, Schild; Stellringe aussen.",
            "Feder von Spitzenschraube zu Federhakenschraube (M3 im Schild unter Spitze); Rolle muss bei jeder Stellung anliegen.",
        ],
        checks=checks,
        function_test="Kurbel langsam drehen: Zeiger läuft 0 → +7.1 mm → 0 (Skala), stossfrei, Rolle hebt nie ab "
                      "(Papierstreifen zwischen Rolle/Nocken bleibt eingeklemmt). 50 Umdrehungen ohne Klemmen.",
    )
