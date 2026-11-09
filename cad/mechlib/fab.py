"""Fertigungsparameter und Verfahrensgrenzen – Bambu Lab H2S Laser Full Combo.

Status wie in calculations/hoverlib/parameters.py:
  SPEC - Herstellerangabe (hier: nur aus Haendler-/Fachpresse-Quellen, an
         offizieller Bambu-Lab-Spezifikation noch NICHT geprueft)
  ANN  - Annahme, wird durch Messung am Testcoupon (m00) ersetzt
  RULE - Konstruktionsregel des Projekts (bewusst konservativer als SPEC)

Nach jeder Kalibriermessung: Wert hier eintragen, ``python cad/build_all.py``
ausfuehren, alle Exporte werden neu erzeugt.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Param:
    value: float
    unit: str
    status: str
    note: str


# ----------------------------------------------------------------- FDM-Druck
PRINT_VOLUME_X = Param(340.0, "mm", "SPEC", "H2S Bauraum (Einzeldüse)")
PRINT_VOLUME_Y = Param(320.0, "mm", "SPEC", "H2S Bauraum")
PRINT_VOLUME_Z = Param(340.0, "mm", "SPEC", "H2S Bauraum")
NOZZLE = Param(0.4, "mm", "RULE", "Standarddüse 0.4 mm")
MIN_WALL = Param(1.2, "mm", "RULE", ">= 3 Perimeter bei 0.4 mm Düse")
CLR_SLIDE = Param(0.20, "mm", "ANN", "radiales Spiel Drehgelenk/Gleitsitz FDM-FDM bzw. FDM-Stahl")
CLR_LOOSE = Param(0.30, "mm", "ANN", "radiales Spiel Montage ohne Funktion")
PRESS_608 = Param(22.05, "mm", "ANN", "Druckmass Bohrung für 608-Aussenring (Nenn 22.00), Presssitz")
HOLE_COMP = Param(0.10, "mm", "ANN", "Zuschlag auf Durchmesser senkrechter Bohrungen (FDM schrumpft innen)")

# ------------------------------------------------------------------- Laser
LASER_POWER = Param(10.0, "W", "SPEC", "Diodenlaser 455 nm")
LASER_AREA_X = Param(310.0, "mm", "SPEC", "Bearbeitungsfläche H2S (Quellen: 310x260 bzw. 310x270)")
LASER_AREA_Y = Param(260.0, "mm", "SPEC", "kleinerer der beiden Quellwerte verwendet")
LASER_MAX_CUT_SPEC = Param(5.0, "mm", "SPEC", "Lindensperrholz, 1 Durchgang – unbestätigt")
LASER_MAX_CUT_RULE = Param(4.0, "mm", "RULE", "Konstruktionsgrenze; Serienmaterial 3 mm")
PLY_T = Param(3.0, "mm", "ANN", "Laser-Sperrholz Pappel/Linde, NENNdicke – vor Export messen!")
KERF = Param(0.15, "mm", "ANN", "Schnittfugenbreite 3 mm Pappel (Kamm-Coupon m00)")
SLOT_CLR = Param(0.05, "mm", "ANN", "Zuschlag Steckschlitz für Schiebesitz Holz-Holz")
LASER_MIN_WEB = Param(2.0, "mm", "RULE", "min. Steg zwischen Schnitten (Verkohlung/Bruch)")
LASER_MARGIN = Param(5.0, "mm", "RULE", "Randabstand zur Bearbeitungsflächengrenze")

# --------------------------------------------------------------- Plotter
CUT_AREA_X = Param(297.5, "mm", "SPEC", "Schneidfläche H2S Cutting Module")
CUT_AREA_Y = Param(300.0, "mm", "SPEC", "Schneidfläche H2S Cutting Module")
CUT_MAX_T_SPEC = Param(0.5, "mm", "SPEC", "max. Materialdicke Messermodul")
CUT_FORCE_MAX = Param(600.0, "gf", "SPEC", "Messerdruck 50–600 gf")
CUT_MIN_FEATURE = Param(3.0, "mm", "RULE", "kleinster Lochdurchmesser/Steg (45°-Messer, Schleppversatz)")
CUT_MIN_RADIUS = Param(0.8, "mm", "RULE", "Innenecken verrunden (Schleppmesser reisst sonst)")

# ----------------------------------------------------------- Normteile
B608_D, B608_d, B608_B = 22.0, 8.0, 7.0          # Rillenkugellager 608
M3_CLR, M3_NUT_AF, M3_NUT_H = 3.4, 5.5, 2.4
M4_CLR, M4_NUT_AF, M4_NUT_H = 4.5, 7.0, 3.2
SHAFT_D = 8.0                                    # Silberstahl/Edelstahl h9
GRID = 20.0                                      # Systemraster Rasterplatte (mm)

# --------------------------------------------- Luftstrecke DN50 (m07–m09)
DN = 50.0              # lichte Weite
FL_OD = 84.0           # Flansch-Aussendurchmesser
FL_PCD = 68.0          # Lochkreis 4 x M4
FL_T = 6.0             # Flanschdicke Druck


def v(p) -> float:
    """Zahlenwert eines Param oder einer Zahl."""
    return p.value if isinstance(p, Param) else float(p)


def all_params() -> dict[str, Param]:
    return {k: val for k, val in globals().items() if isinstance(val, Param)}

# ------------------------------------------------------------ Zahnraeder FDM
GEAR_BACKLASH = Param(0.30, "mm", "ANN", "Flankenspiel (Umfang) gedruckter Zahnräder, PETG, 0.4-Düse")
GEAR_CD_ADD = Param(0.10, "mm", "ANN", "Zuschlag Achsabstand für FDM-Masshaltigkeit")
