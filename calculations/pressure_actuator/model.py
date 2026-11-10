"""Druckwellen-Aktuator – physikalisches Grobmodell (Phase 1, Konzeptvergleich).

Nachweisstufen: B = berechnet (geschlossene Formel), S = simuliert (dieses ODE-Modell),
G = geschätzt (Datenblatt-/Erfahrungswert), E = experimentell (liegt NICHT vor).

Modell: Luftkammer Volumen V0 (Verdrängerkammer + Düsenkammer + Kanäle), Verdränger
ändert das Volumen sinusförmig um ±dV. Die Düsenöffnung ist im Demonstrator gegen eine
Prüfkammer bzw. Prüfplatte gerichtet; die unvollständige Abdichtung wird als Leck-
blende A_L modelliert (turbulente Blendenströmung), zusätzlich eine Entlüftungsbohrung
(Bleed), die den Mittelwert auf Umgebungsdruck zurückführt.

    dp/dt = γ·p0/V(t) · ( −dV/dt − Q_leak(p) )
    Q_leak = sign(p) · Cd · A_L · √(2|p|/ρ)

Annahmen: adiabatisch. Die thermische Grenzschicht ist bei 5 Hz ≈ 1.2 mm, bei 150 Hz ≈ 0.22 mm dick (B);
in mm-Kammern ist der Vorgang bei tiefen Frequenzen teils isotherm → realer Druck 10–25 % tiefer (G).
Für Sicherheitsnachweise ist die adiabatische Rechnung damit konservativ.
Kanal-Trägheit vernachlässigt (gilt weit unterhalb der Helmholtz-Resonanz, s. helmholtz()).
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp

P0, GAMMA, RHO, C_SOUND, CD = 101_325.0, 1.4, 1.19, 343.0, 0.62
P_TARGET = 2_000.0      # Pa Amplitude Zielwert Demonstrator (≈ 20 mbar, Patent-Grössenordnung)
P_LIMIT = 5_000.0       # Pa harte Projektgrenze |p| (Projektannahme, KEIN physiologischer Grenzwert)


def p_closed(dv, v0):
    """B: Druckamplitude bei dichter Kammer, adiabatisch, kleine Auslenkung."""
    return GAMMA * P0 * dv / v0


def dv_needed_closed(p, v0):
    return p * v0 / (GAMMA * P0)


def p_leak_dominated(dv, f, a_leak):
    """B: Grenzfall Leck dominiert (Kompressibilität vernachlässigt): Q_peak = dV·ω = Cd·A·√(2p/ρ)."""
    q = dv * 2 * math.pi * f
    return RHO / 2 * (q / (CD * a_leak)) ** 2


def helmholtz(v0, d_neck, l_neck):
    """B: Helmholtz-Resonanz Kammer + Düse, Endkorrektur 2·0.85·r (geflanscht)."""
    a = math.pi * d_neck**2 / 4
    l_eff = l_neck + 1.7 * d_neck / 2
    return C_SOUND / (2 * math.pi) * math.sqrt(a / (v0 * l_eff))


MU = 1.81e-5            # Pa·s Viskosität Luft 20 °C


def g_capillary(d, l):
    """B: laminarer Leitwert Kapillare (Hagen-Poiseuille), Q = G·Δp."""
    return math.pi * d**4 / (128 * MU * l)


BLEED = (0.2e-3, 30e-3)  # Entlüftungskapillare Ø0.2 × 30 mm (Gutachten Pneumatik)


def bleed_tau(v0, d=BLEED[0], l=BLEED[1]):
    """B: Zeitkonstante Druckabbau über Kapillare: τ = V0/(γ·p0·G)."""
    return v0 / (GAMMA * P0 * g_capillary(d, l))


def p_worst_double_stroke(dv, v0):
    """B (exakt, adiabat): Düse in Endlage (V0+dV) dicht verschlossen, Bleed verstopft,
    Verdränger fährt auf V0−dV → Spitzendruck."""
    return P0 * (((v0 + dv) / (v0 - dv)) ** GAMMA - 1)


def dv_max_double_stroke(p_lim, v0):
    r = (1 + p_lim / P0) ** (1 / GAMMA)
    return v0 * (r - 1) / (r + 1)


def p_thermal(dT, T=293.15):
    """B: statischer Druck dichter Kammer bei Erwärmung dT (isochor)."""
    return P0 * dT / T


def p_force_limited(bl, u, re, sd):
    """B: Voice-Coil, Kammer steifigkeitsbestimmt → Druck durch Spannung begrenzt (DC/statisch)."""
    return bl * u / re / sd


def simulate(dv, v0, f, a_leak, cycles=40, bleed=False, v_extra=0.0):
    """S: eingeschwungene Druckamplitude (max, min) in Pa. v_extra: Zusatzvolumen (Prüfkammer, Schlauch)."""
    w = 2 * math.pi * f
    gb = g_capillary(*BLEED) if bleed else 0.0
    v0 = v0 + v_extra

    def rhs(t, y):
        p = y[0]
        v = v0 - dv * math.sin(w * t)
        dvdt = -dv * w * math.cos(w * t)
        q = math.copysign(CD * a_leak * math.sqrt(2 * abs(p) / RHO), p) if a_leak > 0 else 0.0
        q += gb * p
        return [GAMMA * (P0 + p) / v * (-dvdt - q)]

    t_end = cycles / f
    sol = solve_ivp(rhs, (0, t_end), [0.0], max_step=1 / f / 200, rtol=1e-7, atol=1e-3)
    tail = sol.t > t_end - 5 / f
    return float(sol.y[0][tail].max()), float(sol.y[0][tail].min())


# ---------------------------------------------------------------- Konzeptparameter
# A: Voice-Coil (Kleinlautsprecher Ø40 mm als Verdränger), B: Exzenter + Membran Ø20/12,
# C: Mikropumpe + Ventile (Mitteldruck-Quelle, Pulse durch Ventile).
SD_A = 8.0e-4            # m² wirksame Membranfläche 40-mm-Treiber (G, typ. 7–9 cm²)
XMAX_A = 0.5e-3          # m lineare Auslenkung (G, Kleintreiber 0.3–1 mm)
D_CLAMP_B, D_PLATE_B, E_B = 20e-3, 12e-3, 0.5e-3


def a_eff_membrane(d_clamp, d_plate):
    """B: wirksame Fläche Membran mit starrer Mittelplatte (Kegelstumpf-Näherung)."""
    return math.pi / 12 * (d_clamp**2 + d_clamp * d_plate + d_plate**2)


V0 = 2.0e-6              # m³ Totvolumen (2 cm³) – Konstruktionsziel kompakte Kammer
V0_A = 4.0e-6            # A: Kammer vor Lautsprechermembran etwas grösser (Ø40-Fläche)


def report() -> str:
    L = ["# Druckwellen-Aktuator – Berechnungsergebnisse (Phase 1)", "",
         "Erzeugt mit `python calculations/pressure_actuator/model.py`. Stufen: **B** berechnet, **S** simuliert, "
         "**G** geschätzt. Experimentell belegte Werte (**E**): keine.", ""]
    # Grundgrössen
    L += ["## 1. Benötigtes Verdrängervolumen (B)", "",
          f"Ziel ±{P_TARGET / 1000:.1f} kPa, dichte Kammer: dV = p·V0/(γ·p0).", "",
          "| V0 | dV für ±2 kPa | dV für ±5 kPa (Grenze) |", "|---|---|---|"]
    for v in (1e-6, 2e-6, 4e-6, 8e-6):
        L.append(f"| {v * 1e6:.0f} cm³ | {dv_needed_closed(P_TARGET, v) * 1e9:.0f} mm³ | {dv_needed_closed(P_LIMIT, v) * 1e9:.0f} mm³ |")
    fh = helmholtz(V0, 6e-3, 5e-3)
    L += ["", f"Helmholtz-Resonanz (Kammer 2 cm³, Düse Ø6 × 5 mm): **{fh:.0f} Hz (B)** → Betrieb 5–150 Hz liegt weit "
          "darunter, Kammer verhält sich quasistatisch (Druck folgt dem Volumen, keine Resonanzüberhöhung).", ""]
    # Konzeptwerte
    a_b = a_eff_membrane(D_CLAMP_B, D_PLATE_B)
    dv_a = SD_A * XMAX_A
    dv_b = a_b * E_B
    L += ["## 2. Verdrängervolumen und Eigensicherheit (B)", "",
          "Wird die Düse in **Hubmitte** dicht verschlossen, ist die Amplitude durch das Hubvolumen begrenzt "
          "(p = γ·p0·dV/V0, linear). Das ist der Normalbetrieb im Dichtfall – **nicht** der Sicherheitsnachweis (siehe unten).", "",
          "| Konzept | wirksame Fläche | Hub (Amplitude) | dV | V0 | Amplitude dicht | ≤ 5 kPa? |", "|---|---|---|---|---|---|---|"]
    for name, a, x, v in (("A Voice-Coil Ø40 bei Xmax", SD_A, XMAX_A, V0_A), ("B Exzenter e = 0.5 mm", a_b, E_B, V0)):
        dv = a * x
        pm = p_closed(dv, v)
        L.append(f"| {name} | {a * 1e6:.0f} mm² | {x * 1e3:.2f} mm | {dv * 1e9:.0f} mm³ | {v * 1e6:.0f} cm³ | "
                 f"{pm / 1000:.1f} kPa | {'ja' if pm <= P_LIMIT else 'nein'} |")
    dvm = dv_max_double_stroke(P_LIMIT, V0)
    L += ["", "**Ungünstigster Fall (Gutachten Safety):** Düse wird in der Endlage dicht verschlossen, die Entlüftung ist "
          "verstopft, der Verdränger durchfährt den vollen Doppelhub; exakte Adiabate (B):", "",
          "| Konzept / Variante | dV (Amplitude) | V0 | p_worst | ≤ 5 kPa? |", "|---|---|---|---|---|"]
    for name, dv, v in (("B e = 0.50 mm", a_b * 0.50e-3, V0), ("B e = 0.34 mm", a_b * 0.34e-3, V0),
                        ("B e = 0.15 mm", a_b * 0.15e-3, V0), ("B e = 0.34 mm, V0 = 5 cm³", a_b * 0.34e-3, 5e-6)):
        pw = p_worst_double_stroke(dv, v)
        L.append(f"| {name} | {dv * 1e9:.0f} mm³ | {v * 1e6:.0f} cm³ | {pw / 1000:.1f} kPa | {'ja' if pw <= P_LIMIT else 'nein'} |")
    L += ["", f"Grenze B: dV ≤ {dvm * 1e9:.1f} mm³ bei V0 = 2 cm³ → **e ≤ {dvm / a_b * 1e3:.2f} mm** (B); mit Toleranz e = 0.15 mm. "
          f"Dann beträgt die Amplitude im Dichtfall nur ±{p_closed(a_b * 0.15e-3, V0) / 1000:.1f} kPa (B): "
          "**Eigensicherheit über die Geometrie kostet Reserve gegen Leckage** – das ist der zentrale Zielkonflikt von B.", "",
          "**Konzept A – kraftbegrenzt statt hubbegrenzt (Gutachten Mechatronik/Pneumatik):** Die Luftfeder der Kammer "
          f"(k = γ·p0·Sd²/V0 = {GAMMA * P0 * SD_A ** 2 / V0_A / 1000:.1f} kN/m, B) dominiert, die Resonanz liegt bei ≈ 1.1 kHz (B, "
          "bewegte Masse 0.5 g G). Der Druck folgt der Kraft: p_max = Bl·U/(Re·Sd), unabhängig vom Moment des Verschliessens.", "",
          "| Treiber (G) | Bl | Re | Sd | p_max bei 5 V | p_max bei 12 V |", "|---|---|---|---|---|---|"]
    for name, bl, re, sd in (("Ø40, 4 Ω", 1.5, 3.2, 8e-4), ("Ø40, 4 Ω schwach", 1.0, 3.2, 8e-4),
                             ("Ø28, 8 Ω", 0.6, 7.0, 3.5e-4), ("Exciter + Membran Ø20 (A2)", 2.0, 3.6, 2.05e-4)):
        L.append(f"| {name} | {bl} T·m | {re} Ω | {sd * 1e4:.1f} cm² | {p_force_limited(bl, 5, re, sd) / 1000:.1f} kPa | "
                 f"{p_force_limited(bl, 12, re, sd) / 1000:.1f} kPa |")
    L += ["", "→ A an einer **fest 5-V-Versorgung** (kein USB-PD) ist mit dem richtigen Treiber elektrisch begrenzt; an 12 V "
          "nicht. Sprunganregung kann kurzzeitig bis ≈ 2× überschwingen (G) → Flankensteilheit in Firmware und Hardware begrenzen. "
          "Der Exciter A2 mit kleiner Membran braucht eine Spannungsbegrenzung < 5 V oder ein kleineres Bl.", "",
          f"**Statischer Druck durch Erwärmung** einer dichten Kammer (Bleed verstopft): +10 K → {p_thermal(10) / 1000:.1f} kPa, "
          f"+20 K → {p_thermal(20) / 1000:.1f} kPa (B). Keine Geometrie- oder Spannungsgrenze erfasst diesen Fall → passives "
          "Zweiwege-Überdruckventil als zweite Barriere (Abschnitt 7).", "",
          f"**Entlüftung (Bleed) als Kapillare** Ø{BLEED[0] * 1e3:.1f} × {BLEED[1] * 1e3:.0f} mm: τ = {bleed_tau(V0):.2f} s bei 2 cm³ (B) → "
          f"Eckfrequenz {1 / (2 * math.pi * bleed_tau(V0)):.1f} Hz; Gleichanteil 5 → 0.2 kPa in {bleed_tau(V0) * math.log(25):.2f} s. "
          "Die frühere Bohrung Ø0.3–0.5 mm entlüftete 30× zu schnell und vernichtete die Amplitude unter 30 Hz.", "",
          "C: Eine Mikromembranpumpe (Typ 370, G) erreicht 40–80 kPa Überdruck bzw. −40 kPa Unterdruck → **nicht eigensicher**, "
          "die Sicherheit hängt vollständig an Ventilen, Sensor und Firmware.", ""]
    # Simulation über Frequenz und Leck
    L += ["## 3. Druckamplitude mit Leck (S)", "",
          "Leckblende A_L bildet die unvollständige Abdichtung an der Düse nach (Prüfadapter im Demonstrator). Diese Tabellen "
          "verwenden die ursprünglichen Auslegungswerte (B: e = 0.5 mm) zur Darstellung des Leckeinflusses – nach der Sicherheits"
          "korrektur ist B auf e ≤ 0.15 mm begrenzt (Amplituden dann ≈ 30 %). "
          "Werte: eingeschwungen, Spitze positiv / negativ in kPa.", ""]
    for name, dv, v in (("B (dV = %.0f mm³, V0 = 2 cm³)" % (dv_b * 1e9), dv_b, V0),
                        ("A (dV = 100 mm³ ≈ 0.12 mm Hub, V0 = 4 cm³)", 100e-9, V0_A)):
        L += [f"**Konzept {name}**", "", "| f | dicht | Leck Ø0.5 mm | Leck Ø1 mm | Leck Ø2 mm | Leck Ø3 mm |", "|---|---|---|---|---|---|"]
        for f in (10, 30, 60, 100, 150):
            row = []
            for d in (0, 0.5e-3, 1e-3, 2e-3, 3e-3):
                pmax, pmin = simulate(dv, v, f, math.pi * d**2 / 4)
                row.append(f"+{pmax / 1000:.2f} / {pmin / 1000:.2f}")
            L.append(f"| {f} Hz | " + " | ".join(row) + " |")
        L.append("")
    L += ["**Einfluss Entlüftungskapillare und Prüfkammer** (Konzept B, e = 0.15 mm, V0 = 2 cm³, ohne Leckblende) (S):", "",
          "| f | ohne Bleed | mit Kapillare | mit Kapillare + 5 cm³ Prüfkammer |", "|---|---|---|---|"]
    dv15 = a_b * 0.15e-3
    for f in (5, 10, 30, 100):
        r = [simulate(dv15, V0, f, 0.0), simulate(dv15, V0, f, 0.0, bleed=True),
             simulate(dv15, V0, f, 0.0, bleed=True, v_extra=5e-6)]
        L.append(f"| {f} Hz | " + " | ".join(f"+{a / 1000:.2f} / {b / 1000:.2f}" for a, b in r) + " |")
    L += ["", "Die Prüfkammer vergrössert das Volumen und senkt den Druck stark → Modell und Messung immer mit dem "
          "tatsächlichen Gesamtvolumen (inkl. Schlauch zum Sensor) vergleichen; der Sicherheitsnachweis S1 erfolgt mit "
          "Blindstopfen **direkt an der Düse**.", ""]
    L += ["Lesart: Mit dichter Kammer ist der Druck frequenzunabhängig (reiner Volumeneffekt). Je grösser das Leck, desto "
          "stärker fällt die Amplitude bei tiefen Frequenzen ab (Luft entweicht innerhalb einer Periode). Für ein Leck "
          "Ø2 mm braucht man bei 30 Hz ein Vielfaches des Hubvolumens → **Abdichtung/Düsengeometrie ist die wichtigste "
          "Einflussgrösse**, nicht die Antriebskraft. Nichtlinear: im Dichtfall sind die Überdruckspitzen grösser als die Unterdruckspitzen (+7.75 / −6.86 kPa).", ""]
    # Kräfte und Leistung
    f_a = P_TARGET * SD_A
    f_b = P_TARGET * a_b
    global P_LEAK_W, I_RMS_A
    P_LEAK_W = P_TARGET * CD * math.pi * 0.25e-6 * math.sqrt(2 * P_TARGET / RHO) / 2
    I_RMS_A = f_a / 1.5 / math.sqrt(2)
    L += ["## 4. Kräfte, Leistung, Antrieb (B/G)", "",
          "| Grösse | A Voice-Coil | B Exzenter | C Pumpe + Ventile |", "|---|---|---|---|",
          "| Druck pro Strom | Bl/Sd: Ø40 (Bl 1.5) 1.9 kPa/A; Ø28 (Bl 0.6) 1.7 kPa/A; Exciter A2 (Bl 2) 9.8 kPa/A (B aus G) | – | – |",
          f"| Kraft auf Verdränger bei 2 kPa | {f_a:.2f} N (B) | {f_b:.2f} N (B) | – |",
          f"| Antriebsmoment / Strom | Bl ≈ 1.5 T·m (G) → I ≈ {f_a / 1.5:.1f} A Spitze | M = F·e = {f_b * E_B * 1e3:.2f} mN·m (B) | Pumpe 3–6 V, 0.2–0.4 A (G) |",
          f"| Pneumatische Leistung (dicht, Blindleistung) | ≈ 0 W | ≈ 0 W | – |",
          f"| Pneumatische Wirkleistung Leck Ø1 mm, ±2 kPa (obere Schranke p·Q_peak/2) | ≈ {P_LEAK_W:.2f} W (B) | gleich | Pumpe muss Leckstrom nachliefern |",
          f"| Elektrische Leistung bei 2 kPa dicht | Ø40/4 Ω: {I_RMS_A ** 2 * 3.2:.1f} W; Ø28/8 Ω (Bl 0.6): ≈ 5.4 W, 9.3 V Spitze → an 5 V nicht erreichbar; Exciter A2: ≈ 0.15 W (B aus G) | 0.5–1.5 W (G, Motor 130/N20 ohne Getriebe) | 2–4 W (G, 2 Pumpen + 2 Ventile; Ventilspulen je 1–2 W) |",
          "| Drehzahl / Frequenz | direkt 1–200 Hz (Verstärker, untere Grenzfrequenz des Moduls prüfen) | f = n/60; stabiler Lauf Bürstenmotor erst ab ≈ 600–900 min⁻¹ → **≈ 10–150 Hz** (G); Gimbal-BLDC mit FOC ab ≈ 1 Hz | Ventile 10–20 ms (G) → ≈ 5–25 Hz |", ""]
    # Geräusch grob
    L += ["## 5. Geräusch (G – nur Grössenordnung, Messung nötig)", "",
          "Tieffrequente Druckschwankungen (5–150 Hz) sind wenig hörbar (A-Bewertung −70…−17 dB). Hörbar sind vor allem: "
          "Gehäuse-/Lagergeräusche und Harmonische (B: Motorbürsten ~kHz, Unwucht; C: Pumpe + Ventilklicken; "
          "A: Oberwellen und Gehäuseresonanzen). Ziel Demonstrator: < 50 dB(A) in 30 cm – Messung mit Klasse-2-Messgerät (A0-11).", ""]
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    out = Path(__file__).with_name("results.md")
    out.write_text(report(), encoding="utf-8")
    print(out.read_text(encoding="utf-8"))
