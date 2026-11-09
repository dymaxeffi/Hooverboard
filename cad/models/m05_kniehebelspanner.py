"""M05 – Kniehebelspanner: gelaserte Glieder, gedruckte Gelenkbuchsen.

Viergelenk: Gestell A–D (gedruckter Bock), Spannarm A–B (2 Laserplatten aussen),
Handhebel D–C (2 Laserplatten innen), Koppel C–B (2 Lagen verleimt, Mitte).
Gespannt: D, C, B nahezu fluchtend, 2° über Totpunkt → selbsthemmend.
Jedes Gelenk: gedrucktes Gelenkrohr Ø8 (Lagerfläche) + M4-Schraube, die nur das Rohr klemmt.
Einsatz: Schürze/Teile am Prüfstand A0 klemmen, Haltekraft ohne Werkzeug.
"""

from __future__ import annotations

import math

import cadquery as cq
from shapely import affinity
from shapely.geometry import Point

from mechlib import fab, geom2d as g2
from mechlib.cadbridge import extrude, printed_from_asm, xform
from mechlib.common import HC, T, label, plate_pose, tube
from mechlib.module import Module, Part

Z0 = 24.0                       # Höhe Gestellgelenke über Rasterplatte
A = (0.0, Z0)
D = (40.0, Z0)
B0 = (10.0, Z0 + 25.0)          # Arm-Gelenkpunkt B, gespannt (vor Übertotpunkt-Korrektur)
DC = 20.0
TIP0 = (-70.0, Z0 - 6.0)        # Druckstück-Achse am Arm
OVER = 2.0                      # Grad über Totpunkt
OPEN = 80                       # Öffnungswinkel Handhebel; bei ≈ 85° liegt die Koppel am Bock an (Endanschlag)
L_BC = math.dist(D, B0) - DC
L_AB = math.dist(A, B0)
BUSH = 8.0                      # Gelenkrohr-Aussen-Ø = Laserloch-Ø
Y_ARM = (3.2, 3.2 + T)          # Arm mittlere Lage
Y_HAND = (6.6, 6.6 + T)         # Handhebel aussen → überstreicht Gelenk B (Stift ohne Kopf)


def solve(phi):
    """Handhebelwinkel phi (Grad, D→C) → (C, B, Armdrehung in Grad ggü. B0)."""
    C = (D[0] + DC * math.cos(math.radians(phi)), D[1] + DC * math.sin(math.radians(phi)))
    # B = Schnitt Kreis(A, L_AB) ∩ Kreis(C, L_BC); Zweig nahe B0
    d = math.dist(A, C)
    if d > L_AB + L_BC or d < abs(L_AB - L_BC):
        return None
    a = (L_AB**2 - L_BC**2 + d**2) / (2 * d)
    h = math.sqrt(max(L_AB**2 - a**2, 0))
    ex, ey = (C[0] - A[0]) / d, (C[1] - A[1]) / d
    px, py = A[0] + a * ex, A[1] + a * ey
    cands = [(px - h * ey, py + h * ex), (px + h * ey, py - h * ex)]
    B = min(cands, key=lambda q: math.dist(q, B0))
    rot = math.degrees(math.atan2(B[1] - A[1], B[0] - A[0]) - math.atan2(B0[1] - A[1], B0[0] - A[0]))
    return C, B, rot


PHI_T = math.degrees(math.atan2(B0[1] - D[1], B0[0] - D[0]))  # Totpunkt: C auf D–B0


def tip_after(rot):
    return affinity.rotate(Point(TIP0), rot, origin=A).coords[0]


def build() -> Module:
    phi_c = PHI_T - OVER                 # gespannt: über Totpunkt hinaus (Uhrzeigersinn)
    C, B, rot_c = solve(phi_c)
    # Armgeometrie (gespannt, ohne Drehung; dann um rot_c drehen)
    arm = g2.slot(A, B0, 14).union(g2.slot(A, TIP0, 14))
    arm = arm.difference(g2.circle(BUSH, A)).difference(g2.circle(BUSH, B0)).difference(g2.circle(fab.M4_CLR, TIP0))
    arm = affinity.rotate(arm, rot_c, origin=A)
    hand_dir = math.radians(phi_c)
    grip = (C[0] - 5.0, C[1] + 75.0)
    hand = g2.slot(D, C, 14).union(g2.slot(C, grip, 14))
    hand = hand.difference(g2.circle(BUSH, D)).difference(g2.circle(BUSH, C))
    link = g2.slot(C, B, 12).difference(g2.circle(BUSH, C)).difference(g2.circle(BUSH, B))

    # Öffnungsweg
    open_states = [solve(phi_c + k) for k in range(0, OPEN + 1, 5)]
    lifts = [tip_after(s[2])[1] - tip_after(rot_c)[1] for s in open_states if s]
    reach = len(lifts) == len(open_states)
    lift_max = max(lifts) if lifts else 0.0
    # Totpunkt-Durchgang: Arm bewegt sich zwischen Totpunkt und gespannt minimal zurück
    _, _, rot_t = solve(PHI_T)
    back = tip_after(rot_c)[1] - tip_after(rot_t)[1]   # Nachdrücken beim Durchgang
    # Kraftübersetzung 3° vor Totpunkt (virtuelle Arbeit)
    s1, s2 = solve(PHI_T + 3.5), solve(PHI_T + 2.5)
    dz_tip = abs(tip_after(s1[2])[1] - tip_after(s2[2])[1])
    grip_r = math.dist(D, grip)
    ratio = (math.radians(1.0) * grip_r) / max(dz_tip, 1e-9)

    # Gestellbock in Baugruppenkoordinaten: Fuss 70×30×5, Lasche (|y|<3) mit zwei Gelenkaugen
    foot = cq.Workplane("XY").box(80, 40, 5, centered=(True, True, False)).translate((20, 0, 0))
    lug2d = g2.circle(16, A).union(g2.circle(16, D)).union(g2.rect_xy(-8, 0, 8, Z0)).union(g2.rect_xy(32, 0, 48, Z0))
    lug2d = lug2d.difference(g2.circle(BUSH + 0.2, A)).difference(g2.circle(BUSH + 0.2, D))
    lug = xform(extrude(lug2d, 6), [[1, 0, 0], [0, 0, -1], [0, 1, 0]], (0, 3, 0))
    bock = foot.union(lug)
    for x in (0.0, 40.0):
        for y in (-10.0, 10.0):
            bock = bock.cut(cq.Workplane("XY").circle(fab.M3_CLR / 2 + 0.05).extrude(6).translate((x, y, 0)))
    bock_print, bock_pose = printed_from_asm(bock, [[1, 0, 0], [0, 1, 0], [0, 0, 1]])

    # Bewegungsprüfung 2D über den Öffnungsweg (je Lage gegen Rohre/Bock der anderen Lagen)
    lug_xz = lug2d
    sweep_hits = []
    for k in range(0, OPEN + 1, 5):
        Ck, Bk, rk = solve(phi_c + k)
        hand_k = affinity.rotate(hand, k, origin=D)
        arm_k = affinity.rotate(arm, rk - rot_c, origin=A)
        link_k = g2.slot(Ck, Bk, 12)
        if arm_k.intersection(g2.circle(BUSH, Ck)).area > 0.01 or arm_k.intersection(g2.circle(BUSH, D)).area > 0.01:
            sweep_hits.append(f"Arm/Rohr C,D bei {k}°")
        if link_k.intersection(lug_xz).area > 0.01:
            sweep_hits.append(f"Koppel/Bock bei {k}°")
        if arm_k.intersection(g2.rect_xy(-20, 0, 60, 5.0)).area > 0.01:
            sweep_hits.append(f"Arm/Fuss bei {k}°")

    yl = lambda y0: plate_pose(y0)
    stack = 2 * Y_HAND[1] + 0.2
    stack_a = 2 * Y_ARM[1] + 0.2
    parts = [
        Part("M05-P01", "Spannarm", "laser", "PLY3", 2, profile=arm, engrave=label("M05", (A[0] - 35, A[1] - 3), 3.5, rot=0),
             poses=[yl(Y_ARM[0]), yl(-Y_ARM[1])], orientation="flach",
             rationale="Flaches Biegeteil mit exakten Gelenkabständen: Laser; zwei Platten aussen = symmetrische Lastaufnahme."),
        Part("M05-P02", "Handhebel", "laser", "PLY3", 2, profile=hand, poses=[yl(Y_HAND[0]), yl(-Y_HAND[1])],
             orientation="flach", rationale="Hebel lang/schlank, Sperrholz in Faserrichtung steif und bruchzäh."),
        Part("M05-P03", "Koppel", "laser", "PLY3", 2, profile=link, poses=[yl(0.0), yl(-T)],
             orientation="flach; 2 Lagen verleimt (6 mm)",
             rationale="höchstbelastetes Glied (Druck): Doppellage, Lochabstand bestimmt Totpunktlage → Laser."),
        Part("M05-P04", "Gestellbock", "fdm", "PETG", 1, shape=bock_print, poses=[bock_pose],
             orientation="Fuss auf Bett, Lasche stehend; Gelenkaugen Ø8.2 waagrecht im Druck → mit Reibahle Ø8 H8 nacharbeiten",
             rationale="3D-Form (Fuss + Lasche) in einem Teil, verschraubt auf Raster."),
        Part("M05-P05", "Gelenkrohr lang (D, C)", "fdm", "PETG", 2, shape=tube(BUSH, fab.M4_CLR + 0.1, stack),
             poses=[(lambda c: (lambda wp: xform(wp, [[1, 0, 0], [0, 0, 1], [0, -1, 0]], (c[0], -stack / 2, c[1]))))(c)
                    for c in (D, C)],
             orientation="stehend",
             rationale="Gelenk als Verschleissteil: PETG-Rohr läuft in Holzbohrung, billig ersetzbar; M4 klemmt nur das Rohr."),
        Part("M05-P07", "Gelenkstift (A, B)", "fdm", "PETG", 2, shape=tube(BUSH, 2.5, stack_a),
             poses=[(lambda c: (lambda wp: xform(wp, [[1, 0, 0], [0, 0, 1], [0, -1, 0]], (c[0], -stack_a / 2, c[1]))))(c)
                    for c in (A, B)],
             orientation="stehend, 100 % Infill",
             rationale="kopfloser Stift, in die Armplatten eingeleimt (Bock bzw. Koppel drehen darauf) – "
                       "der Handhebel überstreicht A und B beim Öffnen ohne Kollision."),
        Part("M05-P06", "Druckstück", "fdm", "TPU95A", 1,
             shape=extrude(g2.circle(16).difference(g2.circle(fab.M4_CLR)), 10),
             poses=[(lambda tp: (lambda wp: wp.translate((tp[0], 0, tp[1] - 10 - 7.0 - 1))))(tip_after(rot_c))],
             orientation="flach", rationale="weiches, rutschfestes Druckstück schont Schürzengewebe."),
    ]
    checks = [
        (f"Bewegungsraum 0–{OPEN}° kollisionsfrei (2D, lagenweise)", not sweep_hits, "; ".join(sweep_hits[:4])),
        (f"Viergelenk über {OPEN}° Öffnung lösbar", reach, ""),
        ("Öffnungshub Druckstück ≥ 20 mm", lift_max >= 20, f"{lift_max:.1f} mm bei {OPEN}° Hebelweg"),
        ("Übertotpunkt: Öffnen erzwingt Nachdrücken 0 < Δ ≤ 0.5 mm (selbsthemmend)", 0 < back <= 0.5,
         f"Δ = {back:.3f} mm bei {OVER}° Übertotpunkt"),
        ("Kraftübersetzung 3° vor Totpunkt ≥ 10", ratio >= 10, f"≈ {ratio:.0f} : 1 (Griff → Druckstück)"),
        ("Koppellänge plausibel", L_BC > 2 * BUSH, f"L_BC = {L_BC:.2f} mm, L_AB = {L_AB:.2f} mm"),
    ]
    return Module(
        "m05", "Kniehebelspanner",
        f"Werkzeuglose Klemmung (Öffnungshub {lift_max:.0f} mm, selbsthemmend über Totpunkt). "
        "Einsatz: Schürzenproben, Bauteile, Blendenstrecke am Prüfstand fixieren.",
        parts,
        hardware=[("M4×25 + 2 Scheiben + Stoppmutter (Gelenke D, C)", 2, 0.20), ("Kunststoffscheibe 8.4×16×1 (Distanz C)", 6, 0.03), ("M4×20 + Mutter (Druckstück)", 1, 0.10),
                  ("M3×12 + Mutter (Bock auf Raster)", 4, 0.08), ("Weissleim (Koppel)", 1, 0.05)],
        assembly=[
            "Koppellagen verleimen, mit 8-mm-Dorn in beiden Löchern ausrichten.",
            "Gelenkstift B durch Armplatten und Koppel, Armplatten bündig auf den Stift leimen (Koppel muss frei drehen – Papierstreifen als Distanz).",
            "Gelenkstift A durch Armplatten und Bock, Armplatten aufleimen (Bock dreht frei); langes Rohr (D) durch Handhebelplatten aussen + Bock, M4×25.",
            "Langes Rohr (C) durch Handhebelplatten + Koppel (Distanzscheiben 3.5 mm je Seite), M4×25.",
            "M4-Schrauben nur so fest anziehen, dass sich die Platten auf den Rohren frei drehen (Rohr klemmt, Platten nicht).",
            "Druckstück am Arm verschrauben, Höhe mit Scheiben einstellen: Spannung tritt 3–5° vor Totpunkt ein.",
        ],
        checks=checks,
        function_test="Klemmen eines 6-mm-Sperrholzstreifens: Hebel rastet hörbar über Totpunkt, Streifen lässt sich "
                      "mit 20 N Zug nicht herausziehen; 100 Spannzyklen ohne Spielzunahme > 0.3 mm am Druckstück.",
        allow_touch=set(),
    )
