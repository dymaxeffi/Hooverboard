"""M10 – Fingerschutzgitter DN50 (Ein-/Auslass Gebläse und Luftstrecke).

Verfahrenswahl: reines FDM-Teil + geplottete Dichtung. Ein gelasertes Holzgitter
wäre bei 1.2-mm-Stegen zu fragil und brandgefährdet; ein Laser-Holzrahmen brächte
keinen Vorteil, weil der gedruckte Flansch das Gitter bereits trägt.
Öffnungsweite e ist Parameter; Sicherheitsabstand zum bewegten Teil ist eine
Einbauforderung, die vor Inbetriebnahme gegen ISO 13857 (inkl. Werte für Kinder)
von einer Fachperson zu prüfen ist.
"""

from __future__ import annotations

import math

from mechlib import fab, geom2d as g2
from mechlib.airline import DN, GASKET_T, OD, bolt_pts, flange_2d, gasket_2d
from mechlib.cadbridge import extrude
from mechlib.common import flat_pose
from mechlib.module import Module, Part

E = 6.0          # Schlüsselweite Sechseck (Parameter); Eckmass = E/cos30°
RIB = 1.2
T_GRID = 4.0
SAFETY_MIN = 25.0  # ANN: Mindestabstand Gitter → Rotor; durch Fachperson nach ISO 13857 bestätigen


def grid_2d():
    pitch = E + RIB
    holes = []
    n = int(DN / pitch) + 3
    for i in range(-n, n + 1):
        for j in range(-n, n + 1):
            x = i * pitch + (j % 2) * pitch / 2
            y = j * pitch * math.sqrt(3) / 2
            if math.hypot(x, y) < DN / 2 + pitch:
                holes.append(g2.hexagon(E, (x, y), rot=30))
    from shapely.ops import unary_union
    cells = unary_union(holes).intersection(g2.circle(DN))
    return cells


def build() -> Module:
    cells = grid_2d()
    flange = g2.circle(OD)
    for p in bolt_pts():
        flange = flange.difference(g2.circle(fab.M4_CLR + fab.HOLE_COMP.value, p))
    part2d = flange.difference(cells)
    phi = cells.area / (math.pi * (DN / 2) ** 2)
    zeta = (1 + 0.707 * math.sqrt(1 - phi) - phi) ** 2 / phi ** 2     # Idelchik, dünne Lochplatte (ANN)
    dp10 = zeta * 1.19 / 2 * 10 ** 2
    e_corner = E / math.cos(math.radians(30))
    parts = [
        Part("M10-P01", f"Schutzgitter e{E:.0f}", "fdm", "PETG", 1, shape=extrude(part2d, T_GRID).union(
             extrude(flange_2d(), 6.0)), poses=[lambda wp: wp], orientation="flach (Gitter in Druckebene, keine Brücken)",
             rationale="1.2-mm-Stege + Flansch einteilig, flach gedruckt = fest, maßhaltig, nicht brennbar wie dünnes Holz."),
        Part("M10-P02", "Flanschdichtung", "plotter", "GASKET05", 1, profile=gasket_2d(), poses=[flat_pose(-GASKET_T)],
             orientation="–", rationale="Standarddichtung DN50"),
    ]
    checks = [
        ("Öffnung (Schlüsselweite) ≤ 6 mm", E <= 6.0, f"e = {E} mm, Eckmass {e_corner:.1f} mm"),
        ("Steg ≥ 3 × 0.4-Düse? (≥ 1.2 mm)", RIB >= 3 * fab.NOZZLE.value - 1e-9, f"{RIB} mm"),
        ("Freie Fläche ≥ 55 %", phi >= 0.55, f"φ = {phi * 100:.0f} %, ζ ≈ {zeta:.2f}, Δp(10 m/s) ≈ {dp10:.0f} Pa"),
        ("Sicherheitsabstand zum Rotor als Einbauforderung dokumentiert", True,
         f"≥ {SAFETY_MIN:.0f} mm (ANN) – Prüfung ISO 13857 durch Fachperson offen"),
    ]
    return Module(
        "m10", "Fingerschutzgitter DN50",
        "Berührschutz für Ein- und Auslässe (Gefährdung H-03). Ersetzt keine Sicherheitsbewertung.",
        parts,
        hardware=[("M4×(Flanschpaket+10) + Mutter", 4, 0.12)],
        assembly=["Gitter mit Dichtung zwischen Gebläseadapter und Luftstrecke einsetzen, Gitterseite zum Rotor.",
                  f"Abstand Gitter–Rotorblatt messen und dokumentieren (Soll ≥ {SAFETY_MIN:.0f} mm, ANN)."],
        checks=checks,
        function_test="Prüfstift Ø6 h11 darf keine Öffnung passieren (Schlüsselweite), Prüffinger (IEC 61032 Sonde B, "
                      "kalibriert, nicht gedruckt) erreicht den Rotor nicht. 50 N Fingerdruck auf Gittermitte: kein Bruch.",
    )
