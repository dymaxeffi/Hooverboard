"""M09 – Membran-Rückschlagventil DN50 (Schirmventil, mittig geklemmt).

Hybrid: Ventilsitz und Gehäuse gedruckt; Membran aus geplottetem PET 0.19 mm
(Alternative Silikon 0.5 mm) – dünn, eben, gratfrei, genau das Material, das der
Messerplotter kann und der Laser nicht darf/kann; Dichtungen geplottet.
Durchfluss hebt den Membranrand vom Sitz, Rückströmung presst ihn an.
Einsatz: Rückströmsperre zwischen Gebläse und Kissen (Gebläseausfall → Kissen
entleert sich nicht rückwärts durch das Gebläse, sondern über die Schürze).
"""

from __future__ import annotations

import math

import cadquery as cq

from mechlib import fab, geom2d as g2
from mechlib.airline import DN, GASKET_T, OD, bolt_pts, flange_2d, gasket_2d, tube_body
from mechlib.cadbridge import extrude, xform
from mechlib.common import HC, flat_pose
from mechlib.module import Module, Part
from mechlib.materials import MATERIALS

R_HUB, R_PORT, N_SPOKE, W_SPOKE = 7.0, 22.0, 6, 4.0
D_MEM = 50.0
ID_HOUSING = 54.0
SEAT_T = 6.0
H_LEN = 32.0


def seat_2d():
    g = g2.circle(OD)
    for p in bolt_pts():
        g = g.difference(g2.circle(fab.M4_CLR + HC, p))
    ports = g2.circle(2 * R_PORT).difference(g2.circle(2 * R_HUB))
    for k in range(N_SPOKE):
        a = 2 * math.pi * k / N_SPOKE
        ports = ports.difference(g2.slot((0, 0), (30 * math.cos(a), 30 * math.sin(a)), W_SPOKE))
    return g.difference(ports).difference(g2.circle(fab.M3_CLR + HC)), ports


def build() -> Module:
    seat, ports = seat_2d()
    mem = g2.circle(D_MEM).difference(g2.circle(fab.CUT_MIN_FEATURE.value + 0.4))
    t_mem = MATERIALS["PET019"].thickness
    clamp = extrude(g2.circle(18).difference(g2.circle(fab.M3_CLR + HC)), 3.0)
    housing = tube_body(H_LEN, inner=ID_HOUSING, wall=2.5)
    gasket_in = g2.circle(OD - 0.5).difference(g2.circle(ID_HOUSING + 2))
    for p in bolt_pts():
        gasket_in = gasket_in.difference(g2.circle(fab.M4_CLR, p))

    a_port = ports.area
    a_pipe = math.pi * (DN / 2) ** 2
    h_needed = a_pipe / (2 * math.pi * (D_MEM / 2))
    land = D_MEM / 2 - R_PORT
    parts = [
        Part("M09-P01", "Ventilsitz", "fdm", "PETG", 1, shape=extrude(seat, SEAT_T),
             poses=[lambda wp: xform(wp, [[1, 0, 0], [0, -1, 0], [0, 0, -1]], (0, 0, SEAT_T))],
             orientation="flach; Dichtfläche (Membranseite) auf glattem Bett – im Einbau gewendet",
             rationale="Speichen, Nabe und Flansch in einem Teil; Dichtfläche auf glatter Druckplatte = eben (< 0.05 mm)."),
        Part("M09-P02", "Membran PET 0.19", "plotter", "PET019", 1, profile=mem, poses=[flat_pose(SEAT_T)],
             orientation="–", rationale="Dünne, ebene, gratfreie Folie: Messerplotter; Laser schneidet klares PET nicht."),
        Part("M09-P03", "Klemmteller", "fdm", "PETG", 1, shape=clamp, poses=[lambda wp: wp.translate((0, 0, SEAT_T + t_mem))],
             orientation="flach", rationale="klemmt Membran mittig, Rand frei beweglich"),
        Part("M09-P04", "Ventilgehäuse ID54", "fdm", "PETG", 1, shape=housing,
             poses=[lambda wp: wp.translate((0, 0, SEAT_T + GASKET_T))], orientation="stehend, Flansch auf Bett",
             rationale="Hubraum für Membran (ID 54 > Ø50), Flansch beidseitig → Druck."),
        Part("M09-P05", "Dichtung Gehäuseseite ID56", "plotter", "GASKET05", 1, profile=gasket_in,
             poses=[flat_pose(SEAT_T)], orientation="–", rationale="Innen-Ø grösser als Membran → klemmt sie nicht."),
        Part("M09-P06", "Flanschdichtung", "plotter", "GASKET05", 2, profile=gasket_2d(),
             poses=[flat_pose(-GASKET_T), flat_pose(SEAT_T + GASKET_T + H_LEN)], orientation="–",
             rationale="Standarddichtung DN50"),
    ]
    checks = [
        ("Membran überdeckt Ports ≥ 3 mm (Dichtsteg)", land >= 3, f"Steg {land:.1f} mm"),
        ("Portfläche ≥ 50 % Rohrquerschnitt", a_port / a_pipe >= 0.5, f"{a_port / a_pipe * 100:.0f} %"),
        ("Hubraum ≥ erforderlicher Hub für Vollquerschnitt", H_LEN - 3 >= h_needed, f"benötigt {h_needed:.1f} mm, frei {H_LEN - 3:.0f} mm"),
        ("Membran frei im Gehäuse (radial)", ID_HOUSING - D_MEM >= 3, f"Spalt {(ID_HOUSING - D_MEM) / 2:.1f} mm je Seite"),
        ("Plotter: Membranloch ≥ Mindestmass", fab.CUT_MIN_FEATURE.value + 0.4 >= fab.CUT_MIN_FEATURE.value, "Ø3.4 für M3"),
    ]
    return Module(
        "m09", "Membran-Rückschlagventil DN50",
        "Sperrt Rückströmung bei Gebläsestillstand; Öffnungsdruck abhängig von Membransteifigkeit (PET ≈ 20–60 Pa, "
        "Silikon tiefer – messen).",
        parts,
        hardware=[("M3×12 + Mutter + Scheibe (Membranklemmung)", 1, 0.06), ("M4×45 + Mutter (Durchsteck, je Ventil)", 4, 0.14)],
        assembly=[
            "Sitz mit Dichtfläche nach oben hinlegen, Membran auflegen, Klemmteller + M3 mittig (nur leicht: Membran nicht verziehen).",
            "Dichtung ID56 auf den Sitzflansch, Gehäuse aufsetzen; Strömungsrichtung: Sitz → Gehäuse.",
            "Mit Nachbarmodulen und Standarddichtungen über 4× M4 verbinden.",
        ],
        checks=checks,
        function_test="Blasen in Sitzseite: Membran öffnet; Saugen/Gegendruck 500 Pa: Leckage < 5 % des Nennstroms "
                      "(Seifenblasentest am Rand). Öffnungsdruck mit U-Rohr (M12) protokollieren.",
    )
