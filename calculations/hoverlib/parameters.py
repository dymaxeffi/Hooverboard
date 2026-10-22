"""Zentrale Projektparameter (Phase 0).

Jeder Wert traegt einen Status:
  REQ  - Anforderung des Auftraggebers (nicht stillschweigend aendern)
  ANN  - Annahme, muss durch Messung/Datenblatt ersetzt werden
  PHYS - physikalische Konstante / Standardmodell

CAD (cad/parameters/), Simulation und Abschaetzungen lesen diese Werte,
damit es keine parallelen Parametersaetze gibt.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Param:
    value: float
    unit: str
    status: str  # REQ | ANN | PHYS
    note: str


# ------------------------------------------------------------- Anforderungen
PILOT_MASS = Param(30.0, "kg", "REQ", "Pilotengewicht laut Auftrag")
PILOT_HEIGHT = Param(1.30, "m", "REQ", "Pilotengroesse laut Auftrag")
HOVER_HEIGHT_MIN = Param(0.02, "m", "REQ", "Ziel-Schwebehoehe min. (Definition offen, siehe OQ-01)")
HOVER_HEIGHT_MAX = Param(0.05, "m", "REQ", "Ziel-Schwebehoehe max.")

# ---------------------------------------------------------------- Umgebung
SITE_ALTITUDE = Param(450.0, "m", "ANN", "Schweizer Mittelland, Testhalle")
SITE_TEMPERATURE = Param(20.0, "degC", "ANN", "Hallentemperatur")

# ------------------------------------------------------- Startgeometrie Board
BOARD_LENGTH = Param(0.80, "m", "ANN", "vorlaeufig, Mitte des Zielbereichs 0.70-0.85")
BOARD_WIDTH = Param(0.50, "m", "ANN", "vorlaeufig, Mitte des Zielbereichs 0.40-0.55")
CORNER_RADIUS = Param(0.12, "m", "ANN", "Eckradius Grundriss")
CUSHION_AREA_FRACTION = Param(0.85, "-", "ANN",
                              "wirksame Kissenflaeche / Grundriss (Schuerze nach innen eingezogen)")

# ------------------------------------------------------------ Massenbudget
@dataclass(frozen=True)
class MassBudget:
    name: str
    items: dict = field(default_factory=dict)

    @property
    def board_mass(self) -> float:
        return sum(self.items.values())


# Alle Positionen ANN - werden ab Phase 2 durch CAD-Massen ersetzt.
MASS_BUDGETS = {
    "leicht": MassBudget("leicht", {
        "Tragstruktur/Deck": 2.8, "Schuerze": 0.6, "Hubgeblaese inkl. Motor": 1.0,
        "Vortrieb": 1.0, "Akku": 1.8, "Elektronik/Kabel": 0.5, "Schutz/Kleinteile": 0.8}),
    "nominal": MassBudget("nominal", {
        "Tragstruktur/Deck": 4.0, "Schuerze": 1.0, "Hubgeblaese inkl. Motor": 1.5,
        "Vortrieb": 1.5, "Akku": 2.5, "Elektronik/Kabel": 0.8, "Schutz/Kleinteile": 1.2}),
    "schwer": MassBudget("schwer", {
        "Tragstruktur/Deck": 6.0, "Schuerze": 1.5, "Hubgeblaese inkl. Motor": 2.5,
        "Vortrieb": 2.0, "Akku": 3.5, "Elektronik/Kabel": 1.0, "Schutz/Kleinteile": 1.5}),
}

LIFT_MARGIN = Param(1.25, "-", "ANN",
                    "Auslegungsreserve Gewicht fuer Geblaeseauslegung (Kleidung, Dynamik, Schwerpunkt)")

# ------------------------------------------------------ empirische Beiwerte
DISCHARGE_COEFF = Param(0.6, "-", "ANN", "scharfkantiger Spalt, Lehrbuchwert; messen in A0")
SKIRT_GAPS_MM = (1.0, 2.0, 3.0, 5.0)  # ANN: effektiver Leckspalt mit Schuerze
NO_SKIRT_GAPS_MM = (20.0, 30.0, 50.0)  # REQ-abgeleitet: Spalt = Schwebehoehe ohne Schuerze
ETA_FAN = (0.30, 0.45, 0.60)  # ANN: pessimistisch / nominal / optimistisch
ETA_DRIVE = Param(0.85, "-", "ANN", "BLDC-Motor x ESC im Teillastbereich")

# Freier Flug
EDF_FIGURE_OF_MERIT = Param(0.60, "-", "ANN", "Guetegrad Impeller bezogen auf offenen Rotor")
OPEN_ROTOR_FIGURE_OF_MERIT = Param(0.65, "-", "ANN", "gute Multicopter-Propeller")
EDF_HUB_RATIO = Param(0.40, "-", "ANN", "Naben-/Durchmesserverhaeltnis Impeller")

# Vortrieb
CDA_PILOT = Param(0.45, "m^2", "ANN", "stehendes Kind ~1.30 m, Cd*A")
ROLL_RESIST_SKIRT = Param(0.05, "-", "ANN",
                          "Schuerzen-Schleppbeiwert F/(m g) - voellig unbekannt, Schluesselmessung")

# Akku
USABLE_BATTERY_FRACTION = Param(0.75, "-", "ANN", "nutzbarer Anteil Li-Ion/LiPo inkl. Reserve")
