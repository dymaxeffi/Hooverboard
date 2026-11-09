"""M02 – Stirnradstufe i = 3 (z 16/48, m 1.5) zwischen zwei gelaserten Seitenschilden.

Hybrid: Der Laser setzt den Achsabstand auf ±0.1 mm in beide Schilde (beide aus
derselben Datei, gemeinsam geschnitten); gedruckte Lagerflansche nehmen 608-Lager
im Presssitz auf; Zahnräder werden flach gedruckt (Evolvente in der Druckebene).
Axialsicherung ohne Stellringe: Distanzhülse – Rad – Nabe – Distanzhülse zwischen
den Innenringen, Rad mit M3-Madenschraube auf der Welle.
"""

from __future__ import annotations

import math

from shapely import affinity

from mechlib import fab
from mechlib.common import (T, axis_y_pose, distanzhuelse, gear_part, griffhuelse, kurbel, lagerflansch_608,
                            plate_pose, seitenschild, winkelfuss, winkelfuss_pose)
from mechlib.gears import center_distance, contact_ratio, spur_gear
from mechlib.module import Module, Part

M, Z1, Z2, B = 1.5, 16, 48, 10.0
A = center_distance(M, Z1, Z2) + fab.GEAR_CD_ADD.value
ZAX = 45.0
X1, X2 = -A / 2, A / 2
YI = 25.0                       # Innenfläche Seitenschild
YO = YI + T                     # Aussenfläche
YB = YI - 1.0                   # Lager-Innenseite (Topf steht 1 mm vor)


def mesh_check():
    bl = fab.GEAR_BACKLASH.value
    p = spur_gear(M, Z1, bl)
    w = affinity.translate(affinity.rotate(spur_gear(M, Z2, bl), 180 / Z2, origin=(0, 0)), A, 0)
    worst_overlap, min_gap = 0.0, 1e9
    for k in range(24):
        ang = k * 360 / Z1 / 24 * 2
        pp = affinity.rotate(p, ang, origin=(0, 0))
        ww = affinity.rotate(w, -ang * Z1 / Z2, origin=(A, 0))
        worst_overlap = max(worst_overlap, pp.intersection(ww).area)
        min_gap = min(min_gap, pp.distance(ww))
    return worst_overlap, min_gap


def build() -> Module:
    plate, eng = seitenschild(130, 90, bearings=[(X1, ZAX), (X2, ZAX)], text="M02 i=3  m1.5")
    gear1 = gear_part(M, Z1, B)
    gear2 = gear_part(M, Z2, B).rotate((0, 0, 0), (0, 0, 1), 180 / Z2)
    hub = 10.0
    s_short, s_long = YB - (B / 2 + hub), YB - B / 2
    lf = lagerflansch_608()

    parts = [
        Part("M02-P01", "Seitenschild", "laser", "PLY3", 2, profile=plate, engrave=eng,
             poses=[plate_pose(YI), plate_pose(-YO)], orientation="flach; beide Schilde im selben Job",
             rationale="Achsabstand und Lagerlöcher als präzise 2D-Kontur: Laser schneller, steifer und "
                       "billiger als gedruckte Platte; Schilde identisch → Wellen parallel."),
        Part("M02-P02", "Lagerflansch 608", "fdm", "PETG", 4, shape=lf,
             orientation="Flansch auf Bett", rationale="siehe M01-P04 (Standardelement)"),
        Part("M02-P03", "Ritzel z16", "fdm", "PETG", 1, shape=gear1,
             poses=[axis_y_pose(X1, ZAX, -B / 2)], orientation="Zahnfläche auf Bett, Nabe oben",
             rationale="Evolvente in der Druckebene = beste Profiltreue; Nabe mit Mutterfalle integriert."),
        Part("M02-P04", "Rad z48", "fdm", "PETG", 1, shape=gear2,
             poses=[axis_y_pose(X2, ZAX, -B / 2)], orientation="Zahnfläche auf Bett, Nabe oben",
             rationale="wie P03"),
        Part("M02-P05", f"Distanzhülse {s_short:.0f}", "fdm", "PETG", 2, shape=distanzhuelse(s_short),
             poses=[axis_y_pose(x, ZAX, B / 2 + hub) for x in (X1, X2)], orientation="stehend",
             rationale="Länge passt exakt zur Baugruppe; Druck einfacher als Rohr ablängen."),
        Part("M02-P06", f"Distanzhülse {s_long:.0f}", "fdm", "PETG", 2, shape=distanzhuelse(s_long),
             poses=[axis_y_pose(x, ZAX, -YB) for x in (X1, X2)], orientation="stehend", rationale="wie P05"),
        Part("M02-P07", "Winkelfuss", "fdm", "PETG", 4, shape=winkelfuss(),
             poses=[winkelfuss_pose(x, s * YO, s) for x in (-40, 40) for s in (1, -1)],
             orientation="liegend", rationale="Standardelement M01-P05"),
        Part("M02-P08", "Kurbel", "fdm", "PETG", 1, shape=kurbel(),
             poses=[lambda wp: axis_y_pose(X1, ZAX, YO + 4 + 1 + 16, flip=True)(wp)],
             orientation="Arm auf Bett, Nabe oben", rationale="Antrieb für Funktionsprüfung"),
        Part("M02-P09", "Griffhülse", "fdm", "PETG", 1, shape=griffhuelse(),
             poses=[axis_y_pose(X1 + 40, ZAX, YO + 4 + 1 + 16)], orientation="stehend",
             rationale="drehbare Griffhülse auf M4-Schraube"),
    ]
    # Lagerflansch-Posen: Flanschaussenseite bei |y| = YO + 4, Topf zeigt nach innen
    parts[1].poses = [axis_y_pose(x, ZAX, YO + 4.0, flip=True) for x in (X1, X2)] + \
                     [axis_y_pose(x, ZAX, -(YO + 4.0), flip=False) for x in (X1, X2)]

    ov, gap = mesh_check()
    cr = contact_ratio(M, Z1, Z2)
    checks = [
        ("Zahneingriff ohne Überdeckung (24 Stellungen)", ov < 1e-3, f"max. Überlappfläche {ov:.4f} mm², min. Spalt {gap:.3f} mm"),
        ("Profilüberdeckung ε ≥ 1.2", cr >= 1.2, f"ε = {cr:.2f}"),
        ("Rad vollständig innerhalb Schildkontur (Fingerschutz oben offen nur 50 mm breit)",
         ZAX + M * Z2 / 2 + M <= 90 - 3, f"Radoberkante {ZAX + M * Z2 / 2 + M:.1f} mm"),
        ("Rad frei über Rasterplatte", ZAX - (M * Z2 / 2 + M) >= 3, f"Abstand {ZAX - (M * Z2 / 2 + M):.1f} mm"),
        ("Ritzel z ≥ 14 (Unterschnittgrenze praktisch, α=20°)", Z1 >= 14, f"z1={Z1}"),
    ]
    return Module(
        "m02", "Stirnradstufe i = 3 (z16/z48, m 1.5)",
        "Untersetzungsstufe für Antriebe (z. B. Verstellungen am Prüfstand, Lehrmodell Getriebe). "
        "Abtrieb: Welle Ø8 am Rad, freies Ende −y.",
        parts,
        hardware=[("Rillenkugellager 608-2RS", 4, 0.80), ("Welle Ø8 h9 Silberstahl 110 mm (Ritzel)", 1, 2.0),
                  ("Welle Ø8 h9 Silberstahl 90 mm (Rad)", 1, 1.8), ("Zylinderschraube M3×12 + Mutter (Flansche)", 12, 0.10),
                  ("Madenschraube M3×8 + Mutter (Naben)", 3, 0.08), ("M3×10 + Mutter (Winkelfüsse)", 8, 0.10),
                  ("M4×40 + 2 Scheiben + Stoppmutter (Griff)", 1, 0.30)],
        assembly=[
            "Lager 608 in die vier Lagerflansche pressen (Schraubstock + Zulage, nur Aussenring belasten).",
            "Je zwei Lagerflansche von aussen in die Seitenschilde stecken, mit 3× M3×12 verschrauben (Muttern innen).",
            "Winkelfüsse an die Seitenschilde schrauben, ein Schild auf die Systemplatte (Löcher Raster ±40 mm) setzen.",
            "Welle durch Lager, lange Distanzhülse, Zahnrad (Nabe Richtung +y), kurze Hülse, zweites Lager schieben; "
            "zweites Schild aufsetzen, Füsse verschrauben.",
            "Räder axial auf Flucht bringen (Hülsen liegen an Innenringen an), Madenschrauben anziehen.",
            "Kurbel auf Ritzelwelle (+y), 1 mm Abstand zum Flansch, Madenschraube anziehen; Griffhülse montieren.",
        ],
        checks=checks,
        function_test="Kurbel 3 Umdrehungen → Abtrieb exakt 1 Umdrehung (Markierung). Leerlauf-Drehmoment am "
                      "Ritzel < 0.05 N·m (Federwaage an Kurbel < 1.2 N bei 40 mm). Flankenspiel an Rad "
                      "fühlbar, aber < 0.5 mm am Teilkreis. Kein Klemmen über 10 Abtriebsumdrehungen.",
    )
