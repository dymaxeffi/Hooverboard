"""Physikalische Grundmodelle fuer HOVERBOARD MINI.

Einzige Quelle fuer alle Berechnungsformeln des Projekts. Andere Skripte
(Abschaetzungen, Simulationen, CAD-Pruefungen) importieren von hier und
fuehren keine eigenen Formelkopien.

Alle Funktionen verwenden SI-Einheiten (m, kg, s, N, Pa, W, J).

Status: Modellgleichungen aus der Lehrbuchphysik (Bernoulli, Massenerhaltung,
Strahltheorie). Sie sind *nicht* experimentell fuer dieses Projekt validiert.
Die empirischen Beiwerte (Ausflusszahl, Wirkungsgrade, Leckspalt) sind
Annahmen und werden in Prototyp A gemessen.
"""

from __future__ import annotations

import math

G = 9.80665  # Normfallbeschleunigung [m/s^2]
R_AIR = 287.05  # spezifische Gaskonstante trockene Luft [J/(kg K)]


# ---------------------------------------------------------------- Atmosphaere

def air_density(altitude_m: float = 0.0, temperature_c: float | None = None) -> float:
    """Luftdichte nach Normatmosphaere (ISA, Troposphaere).

    Der Druck folgt der ISA-Hoehenformel. Wird ``temperature_c`` angegeben,
    ersetzt sie die ISA-Temperatur (wichtig: warme Halle = geringere Dichte
    = mehr Volumenstrom bei gleichem Druck).
    """
    if altitude_m < -500 or altitude_m > 11000:
        raise ValueError("Modell nur fuer -500 m bis 11000 m gueltig")
    t_isa = 288.15 - 0.0065 * altitude_m
    p = 101325.0 * (t_isa / 288.15) ** 5.25588
    t = t_isa if temperature_c is None else temperature_c + 273.15
    return p / (R_AIR * t)


# ------------------------------------------------------------------ Geometrie

def rounded_rect_area(length: float, width: float, corner_radius: float) -> float:
    """Flaeche eines Rechtecks mit gerundeten Ecken."""
    _check_rounded_rect(length, width, corner_radius)
    return length * width - (4.0 - math.pi) * corner_radius**2


def rounded_rect_perimeter(length: float, width: float, corner_radius: float) -> float:
    """Umfang eines Rechtecks mit gerundeten Ecken."""
    _check_rounded_rect(length, width, corner_radius)
    return 2.0 * (length + width) - (8.0 - 2.0 * math.pi) * corner_radius


def _check_rounded_rect(length: float, width: float, r: float) -> None:
    if length <= 0 or width <= 0 or r < 0 or 2 * r > min(length, width):
        raise ValueError("ungueltige Rechteckgeometrie")


# ------------------------------------------------------------- Luftkissen

def cushion_pressure(weight_n: float, cushion_area_m2: float) -> float:
    """Erforderlicher Kissenueberdruck p = W / A (statisches Gleichgewicht).

    Gilt fuer ein Plenum mit gleichfoermigem Druck. Impuls des Randstrahls
    und Schuerzen-Membrankraefte sind vernachlaessigt.
    """
    if cushion_area_m2 <= 0:
        raise ValueError("Flaeche muss positiv sein")
    return weight_n / cushion_area_m2


def escape_velocity(pressure_pa: float, rho: float) -> float:
    """Austrittsgeschwindigkeit am Leckspalt nach Bernoulli v = sqrt(2p/rho)."""
    if pressure_pa < 0:
        raise ValueError("Druck muss >= 0 sein")
    return math.sqrt(2.0 * pressure_pa / rho)


def leakage_flow(pressure_pa: float, perimeter_m: float, gap_m: float,
                 discharge_coeff: float, rho: float) -> float:
    """Volumenstrom durch den Umfangsspalt Q = Cd * L * h * v.

    ``gap_m`` ist der *effektive* Spalt zwischen Schuerze/Rand und Boden.
    Bei einer Schuerze ist das nicht die Schwebehoehe des Decks, sondern ein
    Spalt von wenigen Millimetern - der wichtigste unbekannte Parameter.
    """
    if gap_m < 0 or perimeter_m <= 0 or not 0 < discharge_coeff <= 1:
        raise ValueError("ungueltige Leckparameter")
    return discharge_coeff * perimeter_m * gap_m * escape_velocity(pressure_pa, rho)


def air_power(pressure_pa: float, flow_m3s: float) -> float:
    """Hydraulische (pneumatische) Leistung P = p * Q."""
    return pressure_pa * flow_m3s


def electrical_power(air_power_w: float, eta_fan: float, eta_drive: float) -> float:
    """Elektrische Eingangsleistung aus Luftleistung.

    eta_fan:   Geblaesewirkungsgrad inkl. Kanal-/Plenumsverluste
    eta_drive: Motor * Regler (ESC)
    """
    if not (0 < eta_fan <= 1 and 0 < eta_drive <= 1):
        raise ValueError("Wirkungsgrade muessen in (0, 1] liegen")
    return air_power_w / (eta_fan * eta_drive)


def cushion_lift_power(weight_n: float, area_m2: float, perimeter_m: float,
                       gap_m: float, discharge_coeff: float, rho: float,
                       eta_fan: float, eta_drive: float) -> dict:
    """Komplette Luftkissen-Kette: Druck -> Volumenstrom -> Leistungen."""
    p = cushion_pressure(weight_n, area_m2)
    q = leakage_flow(p, perimeter_m, gap_m, discharge_coeff, rho)
    pa = air_power(p, q)
    return {
        "pressure_pa": p,
        "escape_velocity_ms": escape_velocity(p, rho),
        "flow_m3s": q,
        "air_power_w": pa,
        "electrical_power_w": electrical_power(pa, eta_fan, eta_drive),
    }


# ---------------------------------------------------- Freier Flug (Strahltheorie)

def ideal_hover_power_open_rotor(thrust_n: float, disk_area_m2: float, rho: float) -> float:
    """Ideale Schwebeleistung offener Rotor (Impulstheorie): T^1.5 / sqrt(2 rho A)."""
    if disk_area_m2 <= 0 or thrust_n < 0:
        raise ValueError("ungueltige Rotorparameter")
    return thrust_n**1.5 / math.sqrt(2.0 * rho * disk_area_m2)


def real_hover_power(thrust_n: float, disk_area_m2: float, rho: float,
                     figure_of_merit: float, eta_drive: float) -> float:
    """Elektrische Schwebeleistung mit Guetegrad (Figure of Merit) und Antriebswirkungsgrad.

    Der Guetegrad wird auf die Leistung des *offenen* Rotors gleicher
    Flaeche bezogen; der Mantelvorteil eines Impellers steckt damit im FM.
    """
    if not (0 < figure_of_merit <= 1.5 and 0 < eta_drive <= 1):
        raise ValueError("ungueltige Wirkungsgrade")
    return ideal_hover_power_open_rotor(thrust_n, disk_area_m2, rho) / (figure_of_merit * eta_drive)


def annulus_area(diameter_m: float, hub_ratio: float) -> float:
    """Durchstroemte Ringflaeche eines Impellers/Rotors."""
    if not 0 <= hub_ratio < 1:
        raise ValueError("Nabenverhaeltnis in [0, 1)")
    return math.pi * diameter_m**2 / 4.0 * (1.0 - hub_ratio**2)


def ground_effect_power_factor(height_m: float, rotor_radius_m: float) -> tuple[float, bool]:
    """Leistungsfaktor im Bodeneffekt nach Cheeseman & Bennett (1955).

    Bei konstantem Schub sinkt die induzierte Leistung naeherungsweise um
    k = 1 - (R / 4z)^2. Rueckgabe (k, gueltig). Das Modell ist fuer
    z/R < ~0.5 nicht belastbar (Singularitaet bei z = R/4); dann wird
    gueltig=False gemeldet und k konservativ auf 1.0 gesetzt.
    """
    if height_m <= 0 or rotor_radius_m <= 0:
        raise ValueError("Hoehe und Radius muessen positiv sein")
    valid = height_m / rotor_radius_m >= 0.5
    if not valid:
        return 1.0, False
    return 1.0 - (rotor_radius_m / (4.0 * height_m)) ** 2, True


def jet_velocity(thrust_n: float, disk_area_m2: float, rho: float) -> float:
    """Voll entwickelte Strahlgeschwindigkeit offener Rotor: v = sqrt(2T/(rho A))."""
    return math.sqrt(2.0 * thrust_n / (rho * disk_area_m2))


# ------------------------------------------------------------- Vortrieb

def aero_drag(speed_ms: float, cd_a_m2: float, rho: float) -> float:
    """Luftwiderstand D = 0.5 rho v^2 (Cd*A)."""
    return 0.5 * rho * speed_ms**2 * cd_a_m2


def momentum_drag(flow_m3s: float, speed_ms: float, rho: float) -> float:
    """Impulswiderstand der angesaugten Kissenluft D = rho Q v."""
    return rho * flow_m3s * speed_ms


def slope_force(mass_kg: float, slope_deg: float) -> float:
    """Hangabtriebskraft."""
    return mass_kg * G * math.sin(math.radians(slope_deg))


# ------------------------------------------------------- Energie & Stabilitaet

def battery_energy_wh(power_w: float, duration_s: float, usable_fraction: float) -> float:
    """Benoetigte Nenn-Akkuenergie fuer Leistung ueber Dauer bei nutzbarem Anteil."""
    if not 0 < usable_fraction <= 1:
        raise ValueError("nutzbarer Anteil in (0, 1]")
    return power_w * duration_s / 3600.0 / usable_fraction


def cg_offset_moment(mass_kg: float, offset_m: float) -> float:
    """Kippmoment einer Masse mit Hebelarm zum Druckmittelpunkt."""
    return mass_kg * G * offset_m


def combined_cg_shift(pilot_mass: float, pilot_shift_m: float, total_mass: float) -> float:
    """Verschiebung des Gesamtschwerpunkts, wenn sich der Pilot um pilot_shift bewegt."""
    if total_mass <= 0:
        raise ValueError("Gesamtmasse muss positiv sein")
    return pilot_mass * pilot_shift_m / total_mass
