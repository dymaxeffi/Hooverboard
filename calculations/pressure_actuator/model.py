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

Annahmen: adiabatisch (f ≫ thermische Zeitkonstante, für f ≥ 5 Hz und mm-Kammern nur
näherungsweise – real liegt der Exponent zwischen 1.0 und 1.4 → Druck ggf. bis 30 % tiefer),
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


def simulate(dv, v0, f, a_leak, cycles=40):
    """S: eingeschwungene Druckamplitude (max, min) in Pa."""
    w = 2 * math.pi * f

    def rhs(t, y):
        p = y[0]
        v = v0 - dv * math.sin(w * t)
        dvdt = -dv * w * math.cos(w * t)
        q = math.copysign(CD * a_leak * math.sqrt(2 * abs(p) / RHO), p) if a_leak > 0 else 0.0
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
          "Wenn die Düse vollständig dicht verschlossen wird, ist der grösste mögliche Druck durch das Hubvolumen begrenzt "
          "(p_max = γ·p0·dV/V0). Liegt dieser Wert unter der Grenze, ist das Konzept **eigensicher** gegen Überdruck.", "",
          "| Konzept | wirksame Fläche | Hub (Amplitude) | dV | V0 | p_max dicht | eigensicher (≤ 5 kPa)? |", "|---|---|---|---|---|---|---|"]
    for name, a, x, v in (("A Voice-Coil Ø40 bei Xmax", SD_A, XMAX_A, V0_A), ("B Exzenter e = 0.5 mm", a_b, E_B, V0)):
        dv = a * x
        pm = p_closed(dv, v)
        L.append(f"| {name} | {a * 1e6:.0f} mm² | {x * 1e3:.2f} mm | {dv * 1e9:.0f} mm³ | {v * 1e6:.0f} cm³ | "
                 f"{pm / 1000:.1f} kPa | {'ja' if pm <= P_LIMIT else 'nein → Hub begrenzen oder V0 erhöhen'} |")
    v_safe_b = GAMMA * P0 * dv_b / P_LIMIT
    e_safe_b = P_LIMIT * V0 / (GAMMA * P0 * a_b)
    L += ["", f"B eigensicher, wenn V0 ≥ {v_safe_b * 1e6:.1f} cm³ oder Exzentrizität ≤ {e_safe_b * 1e3:.2f} mm (B). "
          f"A: Amplitude elektronisch begrenzt (Strombegrenzung) – Xmax allein ergibt dicht {p_closed(dv_a, V0_A) / 1000:.1f} kPa → "
          "eigensicher nur mit mechanischem Hubanschlag (s. Sicherheit).", "",
          "C: Eine Mikromembranpumpe (Typ 370, G) erreicht 40–80 kPa Überdruck bzw. −40 kPa Unterdruck → **nicht eigensicher**, "
          "Überdruck-/Unterdruckventil und Drucksensor zwingend.", ""]
    # Simulation über Frequenz und Leck
    L += ["## 3. Druckamplitude mit Leck (S)", "",
          "Leckblende A_L bildet die unvollständige Abdichtung an der Düse nach (Prüfkammer im Demonstrator). "
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
    L += ["Lesart: Mit dichter Kammer ist der Druck frequenzunabhängig (reiner Volumeneffekt). Je grösser das Leck, desto "
          "stärker fällt die Amplitude bei tiefen Frequenzen ab (Luft entweicht innerhalb einer Periode). Für ein Leck "
          "Ø2 mm braucht man bei 30 Hz ein Vielfaches des Hubvolumens → **Abdichtung/Düsengeometrie ist die wichtigste "
          "Einflussgrösse**, nicht die Antriebskraft. Nichtlinear: Unterdruckspitzen etwas grösser als Überdruckspitzen.", ""]
    # Kräfte und Leistung
    f_a = P_TARGET * SD_A
    f_b = P_TARGET * a_b
    global P_LEAK_W, I_RMS_A
    P_LEAK_W = P_TARGET * CD * math.pi * 0.25e-6 * math.sqrt(2 * P_TARGET / RHO) / 2
    I_RMS_A = f_a / 1.5 / math.sqrt(2)
    L += ["## 4. Kräfte, Leistung, Antrieb (B/G)", "",
          "| Grösse | A Voice-Coil | B Exzenter | C Pumpe + Ventile |", "|---|---|---|---|",
          f"| Kraft auf Verdränger bei 2 kPa | {f_a:.2f} N (B) | {f_b:.2f} N (B) | – |",
          f"| Antriebsmoment / Strom | Bl ≈ 1.5 T·m (G) → I ≈ {f_a / 1.5:.1f} A Spitze | M = F·e = {f_b * E_B * 1e3:.2f} mN·m (B) | Pumpe 3–6 V, 0.2–0.4 A (G) |",
          f"| Pneumatische Leistung (dicht, Blindleistung) | ≈ 0 W | ≈ 0 W | – |",
          f"| Pneumatische Wirkleistung Leck Ø1 mm, ±2 kPa (obere Schranke p·Q_peak/2) | ≈ {P_LEAK_W:.2f} W (B) | gleich | Pumpe muss Leckstrom nachliefern |",
          f"| Elektrische Leistung | {I_RMS_A ** 2 * 4:.1f}–{I_RMS_A ** 2 * 8:.1f} W bei 2 kPa dicht (B aus G: Bl, Re 4–8 Ω); Ø28-Treiber ≈ ¼ | 0.5–1.5 W (G, Motor 130/N20 ohne Getriebe) | 2–4 W (G, Pumpe + 2 Ventile) |",
          "| Drehzahl / Frequenz | direkt 1–200 Hz (Verstärker) | f = n/60 → 300–9000 min⁻¹ für 5–150 Hz | Ventile 5–30 Hz (Schaltzeit 5–15 ms, G) |", ""]
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
