"""Phase 0: erste physikalische Abschaetzung des Auftriebs- und Leistungsbedarfs.

Ausfuehren:  python calculations/phase0_estimate.py
Ergebnis:    calculations/results/phase0_estimate.md (wird ueberschrieben)

Alle Ergebnisse sind BERECHNUNGEN auf Basis von Annahmen (siehe
hoverlib/parameters.py). Es sind keine Messwerte.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from hoverlib import parameters as P  # noqa: E402
from hoverlib import physics as ph  # noqa: E402

OUT = Path(__file__).resolve().parent / "results" / "phase0_estimate.md"


def fmt(x: float, nd: int = 0) -> str:
    return f"{x:,.{nd}f}".replace(",", "'")


def board_geometry(length: float, width: float, r: float) -> tuple[float, float]:
    area = ph.rounded_rect_area(length, width, r) * P.CUSHION_AREA_FRACTION.value
    # Leckumfang: Umfang der eingezogenen Kissenkontur (Flaechenverhaeltnis -> Laengenfaktor)
    perim = ph.rounded_rect_perimeter(length, width, r) * math.sqrt(P.CUSHION_AREA_FRACTION.value)
    return area, perim


def main() -> str:
    rho = ph.air_density(P.SITE_ALTITUDE.value, P.SITE_TEMPERATURE.value)
    L, B, R = P.BOARD_LENGTH.value, P.BOARD_WIDTH.value, P.CORNER_RADIUS.value
    area, perim = board_geometry(L, B, R)
    eta_d = P.ETA_DRIVE.value
    cd = P.DISCHARGE_COEFF.value
    lines: list[str] = []
    w = lines.append

    w("# Phase 0 – Erste physikalische Abschätzung (automatisch erzeugt)\n")
    w("> **Status: BERECHNUNG auf Basis von Annahmen.** Keine Messwerte, keine Simulation, "
      "keine experimentelle Bestätigung. Erzeugt von `calculations/phase0_estimate.py`; "
      "Parameter in `calculations/hoverlib/parameters.py`.\n")

    w("## 1. Randbedingungen\n")
    w(f"- Luftdichte ρ = {rho:.3f} kg/m³ (ISA-Druck {P.SITE_ALTITUDE.value:.0f} m ü. M., "
      f"{P.SITE_TEMPERATURE.value:.0f} °C)")
    w(f"- Board-Grundriss {L*1000:.0f} × {B*1000:.0f} mm, Eckradius {R*1000:.0f} mm")
    w(f"- Wirksame Kissenfläche A = {area:.3f} m², Leckumfang U = {perim:.2f} m "
      f"(Flächenanteil {P.CUSHION_AREA_FRACTION.value})")
    w(f"- Ausflusszahl Cd = {cd} (ANN), Antriebswirkungsgrad η_Motor·ESC = {eta_d} (ANN)")
    w(f"- Gebläsewirkungsgrad η_Fan = {' / '.join(str(e) for e in P.ETA_FAN)} "
      "(pessimistisch / nominal / optimistisch, ANN)\n")

    # ---- Massen
    w("## 2. Massenbudget (Annahmen, vor CAD)\n")
    w("| Position | leicht [kg] | nominal [kg] | schwer [kg] |")
    w("|---|---:|---:|---:|")
    keys = list(P.MASS_BUDGETS["nominal"].items.keys())
    for k in keys:
        w(f"| {k} | " + " | ".join(f"{P.MASS_BUDGETS[s].items[k]:.1f}" for s in P.MASS_BUDGETS) + " |")
    w("| **Board gesamt** | " + " | ".join(f"**{b.board_mass:.1f}**" for b in P.MASS_BUDGETS.values()) + " |")
    w("| Pilot | " + " | ".join(f"{P.PILOT_MASS.value:.1f}" for _ in P.MASS_BUDGETS) + " |")
    totals = {s: b.board_mass + P.PILOT_MASS.value for s, b in P.MASS_BUDGETS.items()}
    w("| **Gesamtmasse m** | " + " | ".join(f"**{t:.1f}**" for t in totals.values()) + " |")
    w("| Gewichtskraft m·g [N] | " + " | ".join(fmt(t * ph.G) for t in totals.values()) + " |")
    w(f"| Auslegung m·g·{P.LIFT_MARGIN.value} [N] | "
      + " | ".join(fmt(t * ph.G * P.LIFT_MARGIN.value) for t in totals.values()) + " |\n")
    w("Beobachtung: Das Board wiegt in allen Szenarien 30–60 % der Pilotenmasse. "
      "Eigengewicht ist damit ein Haupttreiber des Leistungsbedarfs.\n")

    m_nom = totals["nominal"]
    w_nom = m_nom * ph.G
    w_des = w_nom * P.LIFT_MARGIN.value

    # ---- Luftkissen mit Schuerze
    w("## 3. Konzept K1 – Luftkissen mit Schürze (nominale Masse)\n")
    p_nom = ph.cushion_pressure(w_nom, area)
    p_des = ph.cushion_pressure(w_des, area)
    w(f"- Kissendruck nominal p = {fmt(p_nom)} Pa (= {p_nom/9.80665:.0f} mm Wassersäule), "
      f"Auslegung {fmt(p_des)} Pa")
    w(f"- Austrittsgeschwindigkeit am Spalt v = {ph.escape_velocity(p_nom, rho):.1f} m/s\n")
    w("| eff. Leckspalt h [mm] | Q [m³/s] | Luftleistung [W] | P_el η_Fan=0.30 [W] | "
      "P_el 0.45 [W] | P_el 0.60 [W] | P_el Auslegung, 0.45 [W] |")
    w("|---:|---:|---:|---:|---:|---:|---:|")
    k1_rows = {}
    for h in P.SKIRT_GAPS_MM:
        r = ph.cushion_lift_power(w_nom, area, perim, h / 1000, cd, rho, P.ETA_FAN[1], eta_d)
        rd = ph.cushion_lift_power(w_des, area, perim, h / 1000, cd, rho, P.ETA_FAN[1], eta_d)
        pels = [ph.electrical_power(r["air_power_w"], e, eta_d) for e in P.ETA_FAN]
        k1_rows[h] = (r, rd)
        w(f"| {h:.0f} | {r['flow_m3s']:.3f} | {fmt(r['air_power_w'])} | "
          + " | ".join(fmt(x) for x in pels) + f" | {fmt(rd['electrical_power_w'])} |")
    w("")
    w("Der effektive Leckspalt bestimmt die Leistung linear. Er hängt von Schürzenbauart, "
      "Untergrund und Druck ab und ist **die wichtigste unbekannte Grösse** → Messung in Prototyp A.\n")

    # ---- ohne Schuerze
    w("## 4. Konzept K2 – Luftkissen ohne Schürze (Spalt = Schwebehöhe)\n")
    w("| Schwebehöhe [mm] | Q [m³/s] | Luftleistung [W] | P_el η_Fan=0.45 [W] |")
    w("|---:|---:|---:|---:|")
    for h in P.NO_SKIRT_GAPS_MM:
        r = ph.cushion_lift_power(w_nom, area, perim, h / 1000, cd, rho, P.ETA_FAN[1], eta_d)
        w(f"| {h:.0f} | {r['flow_m3s']:.2f} | {fmt(r['air_power_w'])} | {fmt(r['electrical_power_w'])} |")
    w("")
    w("Einfaches Plenum-Modell. Ein Randstrahl-Design (Peripheral Jet) kann den Bedarf senken; "
      "der Effekt wird in Phase 1 mit Literaturmodell quantifiziert, nicht hier angenommen.\n")

    # ---- freier Flug
    w("## 5. Konzepte K3/K4 – Impeller / Rotoren mit Schub = Gewicht\n")
    w(f"Schub T = {fmt(w_nom)} N (nur Schweben, ohne Steuerreserve). "
      f"Guetegrad Impeller {P.EDF_FIGURE_OF_MERIT.value}, offener Rotor "
      f"{P.OPEN_ROTOR_FIGURE_OF_MERIT.value} (ANN).\n")
    w("| Anordnung | Strahlfläche [m²] | Strahlgeschw. [m/s] | P_ideal [W] | P_el [W] | "
      "P_el bei T/W = 1.5 [W] |")
    w("|---|---:|---:|---:|---:|---:|")
    configs = [
        ("4 × Impeller Ø 90 mm", 4, 0.090, P.EDF_HUB_RATIO.value, P.EDF_FIGURE_OF_MERIT.value),
        ("4 × Impeller Ø 120 mm", 4, 0.120, P.EDF_HUB_RATIO.value, P.EDF_FIGURE_OF_MERIT.value),
        ("8 × Impeller Ø 120 mm", 8, 0.120, P.EDF_HUB_RATIO.value, P.EDF_FIGURE_OF_MERIT.value),
        ("4 × Propeller Ø 0.25 m (Grenzfall Grundriss)", 4, 0.25, 0.0, P.OPEN_ROTOR_FIGURE_OF_MERIT.value),
    ]
    ff = {}
    for name, n, d, hub, fm in configs:
        a = n * ph.annulus_area(d, hub)
        pid = ph.ideal_hover_power_open_rotor(w_nom, a, rho)
        pel = ph.real_hover_power(w_nom, a, rho, fm, eta_d)
        pel15 = ph.real_hover_power(1.5 * w_nom, a, rho, fm, eta_d)
        ff[name] = pel
        w(f"| {name} | {a:.4f} | {ph.jet_velocity(w_nom, a, rho):.0f} | {fmt(pid)} | {fmt(pel)} | {fmt(pel15)} |")
    w("")
    k, valid = ph.ground_effect_power_factor(0.03, 0.06)
    w(f"Bodeneffekt (Cheeseman–Bennett) für Ø 120 mm bei 30 mm Höhe: z/R = 0.5 → Faktor {k:.2f} "
      f"(Grenze der Modellgültigkeit: {'ja' if valid else 'nein'}). Kleinere Höhen liegen ausserhalb "
      "des Modells; dort geht ein Impeller-Board physikalisch in ein Luftkissen ohne Schürze über.\n")

    # ---- Vergleich
    k1_nom = k1_rows[3.0][0]["electrical_power_w"]
    w("## 6. Grössenordnungsvergleich (nominal)\n")
    w(f"- K1 Schürze, Spalt 3 mm, η_Fan 0.45: **≈ {fmt(k1_nom, 0)} W elektrisch**")
    k2 = ph.cushion_lift_power(w_nom, area, perim, 0.03, cd, rho, P.ETA_FAN[1], eta_d)["electrical_power_w"]
    w(f"- K2 ohne Schürze, 30 mm: **≈ {fmt(k2)} W** (Faktor {k2/k1_nom:.0f})")
    best_ff = ff["8 × Impeller Ø 120 mm"]
    w(f"- K3 8 × Impeller Ø 120 mm: **≈ {fmt(best_ff)} W** (Faktor {best_ff/k1_nom:.0f}), "
      "ohne Steuerreserve\n")

    # ---- Parameterstudie Groesse
    w("## 7. Parameterstudie Board-Grösse (K1, Spalt 3 mm, η_Fan 0.45)\n")
    w("Seitenverhältnis B/L = 0.6; Strukturmasse skaliert mit Grundfläche "
      "(nominal 4.0 kg bei 0.8 × 0.5 m), übrige Board-Massen konstant.\n")
    w("| L × B [mm] | A_Kissen [m²] | m_ges [kg] | p [Pa] | P_el [W] |")
    w("|---|---:|---:|---:|---:|")
    nom = P.MASS_BUDGETS["nominal"]
    ref_area = ph.rounded_rect_area(L, B, R)
    for Ls in (0.60, 0.70, 0.80, 0.90, 1.00, 1.20):
        Bs = 0.6 * Ls
        rs = min(R, 0.24 * Bs)
        a_s, u_s = board_geometry(Ls, Bs, rs)
        struct = nom.items["Tragstruktur/Deck"] * ph.rounded_rect_area(Ls, Bs, rs) / ref_area
        m = P.PILOT_MASS.value + nom.board_mass - nom.items["Tragstruktur/Deck"] + struct
        r = ph.cushion_lift_power(m * ph.G, a_s, u_s, 0.003, cd, rho, P.ETA_FAN[1], eta_d)
        w(f"| {Ls*1000:.0f} × {Bs*1000:.0f} | {a_s:.3f} | {m:.1f} | {fmt(r['pressure_pa'])} | "
          f"{fmt(r['electrical_power_w'])} |")
    w("")
    w("Physik: P ∝ p^1.5 · U. Grössere Fläche senkt den Druck stärker als der Umfang wächst – "
      "**grössere Boards brauchen weniger Hubleistung**, sind aber schwerer, sperriger und "
      "teurer. Das widerspricht dem Ziel „möglichst kompakt“ (siehe Zielkonflikt Z-01).\n")

    # ---- Vortrieb
    w("## 8. Vortrieb (nominal)\n")
    v = 2.0
    q3 = k1_rows[3.0][0]["flow_m3s"]
    d_aero = ph.aero_drag(v, P.CDA_PILOT.value, rho)
    d_mom = ph.momentum_drag(q3, v, rho)
    d_skirt = P.ROLL_RESIST_SKIRT.value * m_nom * ph.G
    f_acc = m_nom * 0.5
    f_slope = ph.slope_force(m_nom, 2.0)
    w(f"Bei v = {v} m/s (Gehtempo, vorgeschlagene Höchstgeschwindigkeit):\n")
    w(f"- Luftwiderstand Pilot+Board: {d_aero:.1f} N")
    w(f"- Impulswiderstand Kissenluft: {d_mom:.1f} N")
    w(f"- Schürzenschleppen (Beiwert {P.ROLL_RESIST_SKIRT.value}, ANN): {d_skirt:.1f} N")
    w(f"- Beschleunigung 0.5 m/s²: {f_acc:.1f} N")
    w(f"- Steigung 2°: {f_slope:.1f} N")
    total = d_aero + d_mom + d_skirt + f_acc + f_slope
    w(f"- **Summe ≈ {total:.0f} N** → 2 Antriebe à ≈ {total/2:.0f} N, Bremsen mit gleichem Betrag "
      "(Reversierung oder Schubumlenkung nötig).\n")
    props = {}
    for d in (0.20, 0.30):
        a_prop = 2 * ph.annulus_area(d, 0.15)
        props[d] = ph.real_hover_power(total, a_prop, rho, P.OPEN_ROTOR_FIGURE_OF_MERIT.value, eta_d)
        w(f"- Statischer Schub {total:.0f} N mit 2 × Ø {d*1000:.0f} mm Propellern: ≈ {fmt(props[d])} W "
          "elektrisch (Spitze, nicht Dauer)")
    w("\nGrössere Propeller senken die Vortriebsleistung deutlich, kosten aber Bauraum und "
      "erhöhen das Risiko an rotierenden Teilen (Zielkonflikt Z-04).\n")
    p_prop = props[0.30]

    # ---- Energie
    w("## 9. Energiebedarf\n")
    p_cruise = k1_nom + 0.3 * p_prop
    w(f"Annahme (ANN): Dauerleistung = Hub (Spalt 3 mm) + 30 % der Vortriebsspitze "
      f"(Ø 300 mm) ≈ {fmt(p_cruise)} W.\n")
    w("| Flugzeit | Nenn-Akkuenergie [Wh] | Masse bei 150 Wh/kg Pack (ANN) [kg] |")
    w("|---|---:|---:|")
    for mins in (5, 10, 15):
        e = ph.battery_energy_wh(p_cruise, mins * 60, P.USABLE_BATTERY_FRACTION.value)
        w(f"| {mins} min | {fmt(e)} | {e/150:.2f} |")
    w("")

    # ---- Stabilitaet
    w("## 10. Schwerpunkt und Kippstabilität\n")
    for shift in (0.05, 0.10, 0.15):
        cg = ph.combined_cg_shift(P.PILOT_MASS.value, shift, m_nom)
        w(f"- Pilot verlagert sich um {shift*100:.0f} cm → Gesamtschwerpunkt wandert {cg*100:.1f} cm, "
          f"Kippmoment {ph.cg_offset_moment(m_nom, cg):.0f} N·m")
    w("")
    w("Ein einzelnes Plenum mit gleichförmigem Druck hat **kein** aufrichtendes Moment aus dem Druck "
      "selbst; die Rückstellung kommt allein aus der Schürzengeometrie. Gegenmassnahmen "
      "(Kammerung/Kiel, Bag-and-Finger, aktive Regelung) werden in Phase 1 bewertet.\n")

    text = "\n".join(lines)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(text, encoding="utf-8")
    return text


if __name__ == "__main__":
    print(main())
