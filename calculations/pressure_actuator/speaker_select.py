"""Prototyp A – Auswahl des Lautsprechers aus dem Bestand.

    python calculations/pressure_actuator/speaker_select.py [csv]

Standard-Eingabe: docs/prototype_a/lautsprecher_messung.csv (falls leer: Beispieldatei).
Ausgabe: docs/prototype_a/lautsprecher_auswertung.md

Physik (siehe docs/pressure_actuator_concepts.md, Abschnitt 5 A):
Die Kammer ist viel steifer als die Lautsprecheraufhängung → Druck folgt der Kraft:
    p = Bl·I / Sd            (Druck pro Ampere = Bl/Sd)
    p_max = Bl·U / (Re·Sd)   (Grenze an fester Versorgungsspannung U, auch im DC-Fehler)
Bl wird mit dem Nullabgleich gemessen: Masse m auf den Konus, Gleichstrom I so lange
erhöhen, bis der Konus wieder in der Ausgangslage steht → Bl = m·g / I.
"""

from __future__ import annotations

import csv
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DIR = ROOT / "docs" / "prototype_a"
G = 9.81
U_AMP = 4.5          # V Spitze, Klasse-D-BTL an 5 V (≈ 0.5 V Verlust, Annahme)
P_TARGET = 2000.0    # Pa Zielamplitude
P_REACH = 3000.0     # Pa erforderliche Reserve (Leck, Spulenerwärmung +35 % Re)
P_CAP = 4000.0       # Pa Begrenzung (S1, Abbruchschwelle)
P_LIMIT = 5000.0     # Pa Projektgrenze
# Bauform „Lautsprecher als Motor“: Stössel auf Staubkappe treibt eigene Membran (Ø20, Mittelplatte Ø12)
D_CLAMP, D_PLATE = 20e-3, 12e-3
X_OP = 0.3e-3        # m Betriebshub-Annahme (Leckkompensation) für den Federanteil der Aufhängung
A_PISTON = math.pi / 12 * (D_CLAMP**2 + D_CLAMP * D_PLATE + D_PLATE**2)   # 2.05 cm²


def evaluate(r: dict, variant: str = "direkt") -> dict:
    """variant 'direkt': Konus bildet Kammerwand (Fläche Sd). 'motor': Konus offen, Stössel treibt Membran A_PISTON."""
    out = dict(r)
    out["variant"] = variant
    re = float(r["re_ohm"])
    has_cone = bool(r.get("d_sd_mm", "").strip())       # Exciter/Stössel-Wandler: kein Konus → nur Motor-Bauform
    if variant == "direkt" and not has_cone:
        variant = out["variant"] = "motor"
    sd = math.pi * (float(r["d_sd_mm"]) / 1000) ** 2 / 4 if variant == "direkt" else A_PISTON
    out["sd_cm2"] = sd * 1e4
    notes = []
    if r.get("zustand", "ok").strip().lower() not in ("ok", ""):
        notes.append("defekt")
    bl = None
    if r.get("bl_masse_g") and r.get("bl_strom_a"):
        bl = float(r["bl_masse_g"]) / 1000 * G / float(r["bl_strom_a"])
    elif r.get("bl_tm"):                                  # Datenblattwert (G) statt Messung
        bl = float(r["bl_tm"])
    out["bl"] = bl
    if bl is None:
        out["status"] = "Bl messen"
        out["notes"] = notes
        return out
    out["kpa_per_a"] = bl / sd / 1000
    out["p_max"] = bl * U_AMP / (re * sd)            # Sicherheitsgrenze (ohne Aufhängung → konservativ)
    k_s = None
    if r.get("bl_auslenkung_mm") and r.get("bl_masse_g"):
        k_s = float(r["bl_masse_g"]) / 1000 * G / (float(r["bl_auslenkung_mm"]) / 1000)
    elif r.get("cms_mm_n"):                               # Datenblatt: Nachgiebigkeit Cms → k = 1/Cms
        k_s = 1 / (float(r["cms_mm_n"]) / 1000)
    out["k_s"] = k_s
    f_spring = (k_s or 0.0) * X_OP                    # Kraft, die die Aufhängung bei Betriebshub frisst
    if k_s is None:
        notes.append("Auslenkung messen (Federanteil fehlt)")
    i2k = (P_TARGET * sd + f_spring) / bl
    out["i_2k"] = i2k
    out["u_2k"] = i2k * re
    out["p_2k"] = i2k**2 * re / 2                     # Sinus, Wirkleistung in Re
    # Thermische Reserve: Effektivstrom ≤ 50 % Nennstrom (schlechte Kühlung bei kleinem Hub)
    if r.get("nenn_w"):
        i_rated = math.sqrt(float(r["nenn_w"]) / re)
        out["i_ratio"] = (i2k / math.sqrt(2)) / i_rated
        if out["i_ratio"] > 0.5:
            notes.append(f"Strom {out['i_ratio'] * 100:.0f} % Nennstrom")
    # Vorwiderstand, falls zu stark
    rs = 0.0
    if out["p_max"] > P_CAP:
        rs = bl * U_AMP / (P_CAP * sd) - re
    out["r_series"] = rs
    out["p_max_capped"] = bl * U_AMP / ((re + rs) * sd)
    # Betrieb mit Leck: Hub X_OP nötig, Aufhängung zieht Kraft ab; Vorwiderstand mitgerechnet
    out["p_leak"] = max(0.0, (bl * U_AMP / (re + rs) - f_spring) / sd)
    if variant == "direkt" and r.get("staubkappe", "").strip().lower().startswith("gewebe"):
        notes.append("Staubkappe abdichten")
    if variant == "direkt" and r.get("polkernbohrung", "").strip().lower() == "ja":
        notes.append("Polkernbohrung abdichten")
    if variant == "motor" and r.get("staubkappe", "").strip().lower().startswith("gewebe"):
        notes.append("Stössel auf Gewebekappe: Klebefläche verstärken")
    if out["p_max_capped"] < P_REACH or out["p_leak"] < P_TARGET:
        out["status"] = "zu schwach"
    elif "defekt" in notes:
        out["status"] = "defekt"
    elif any(n.startswith("Strom") for n in notes):
        out["status"] = "thermisch knapp"
    else:
        out["status"] = "geeignet"
    out["notes"] = notes
    return out


def rank_key(e):
    order = {"geeignet": 0, "thermisch knapp": 1, "zu schwach": 2, "defekt": 3, "Bl messen": 4}
    return (order[e["status"]], e.get("p_2k", 1e9))


def report(rows, src):
    ev = []
    for r in rows:
        a, b = evaluate(r, "direkt"), evaluate(r, "motor")
        ev.append(min((a, b), key=rank_key) if a["bl"] is not None else a)
    ev.sort(key=rank_key)
    L = ["# Prototyp A – Auswertung Lautsprecher", "",
         f"> Automatisch erzeugt von `calculations/pressure_actuator/speaker_select.py` aus `{src.relative_to(ROOT)}`.", "",
         f"Annahmen: Verstärker {U_AMP} V Spitze (Klasse-D-BTL an 5 V), Ziel ±{P_TARGET / 1000:.0f} kPa, "
         f"Reserve ≥ {P_REACH / 1000:.0f} kPa, Begrenzung {P_CAP / 1000:.0f} kPa (Projektgrenze {P_LIMIT / 1000:.0f} kPa). "
         "Bl und Re gemessen (E), alle abgeleiteten Werte berechnet (B) mit dem Modell „Kammer steifer als Aufhängung“.", "",
         f"Bauformen: **direkt** = Konus bildet die Kammerwand (Fläche Sd); **Motor** = Konus offen, Stössel auf der Staubkappe "
         f"treibt eine geplottete Membran Ø20/12 (wirksam {A_PISTON * 1e4:.2f} cm²). Je Lautsprecher ist die bessere Bauform gezeigt.", "",
         "| Rang | ID | Beschreibung | Bauform | wirks. Fläche cm² | Re Ω | Bl T·m | Feder N/mm | kPa/A | p_max 5 V ohne Begrenzung | Vorwiderstand | dicht max. (begrenzt) | mit Leck, 0,3 mm Hub | Strom für 2 kPa | Leistung 2 kPa | Status | Hinweise |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for i, e in enumerate(ev, 1):
        if e["bl"] is None:
            L.append(f"| – | {e['id']} | {e.get('beschreibung', '')} | – | – | {float(e['re_ohm']):.1f} | – | – | – | – | – | – | – | – | – | "
                     f"{e['status']} | {', '.join(e['notes'])} |")
            continue
        rs = f"{e['r_series']:.1f} Ω" if e["r_series"] > 0 else "–"
        ks = f"{e['k_s'] / 1000:.2f}" if e["k_s"] else "–"
        L.append(f"| {i} | {e['id']} | {e.get('beschreibung', '')} | {e['variant']} | {e['sd_cm2']:.2f} | {float(e['re_ohm']):.1f} | {e['bl']:.2f} | "
                 f"{ks} | "
                 f"{e['kpa_per_a']:.2f} | {e['p_max'] / 1000:.1f} kPa | {rs} | {e['p_max_capped'] / 1000:.1f} kPa | {e['p_leak'] / 1000:.1f} kPa | "
                 f"{e['i_2k']:.2f} A / {e['u_2k']:.1f} V | {e['p_2k']:.2f} W | "
                 f"**{e['status']}** | {', '.join(e['notes'])} |")
    best = [e for e in ev if e["status"] == "geeignet"]
    L += ["", "## Empfehlung", ""]
    if best:
        b = best[0]
        L.append(f"**{b['id']} – {b.get('beschreibung', '')}, Bauform {b['variant']}**: braucht für ±2 kPa nur {b['p_2k']:.2f} W "
                 f"({b['i_2k']:.2f} A Spitze). " + (f"Vorwiderstand {b['r_series']:.1f} Ω (Belastbarkeit ≥ "
                 f"{(U_AMP / (float(b['re_ohm']) + b['r_series'])) ** 2 * b['r_series']:.1f} W für den DC-Fehlerfall) begrenzt "
                 f"p_max auf {b['p_max_capped'] / 1000:.1f} kPa." if b["r_series"] > 0 else
                 f"p_max {b['p_max'] / 1000:.1f} kPa liegt ohne Vorwiderstand unter der Begrenzung."))
        if len(best) > 1:
            L.append("")
            L.append("Ersatz: " + ", ".join(f"{e['id']}" for e in best[1:4]) + ".")
    else:
        L.append("Noch kein geeigneter Lautsprecher (Bl messen bzw. stärkeren Treiber wählen).")
    L += ["", f"Kriterien: dicht max. ≥ {P_REACH / 1000:.0f} kPa nach Begrenzung, **und** mit Leck (Hub {X_OP * 1e3:.1f} mm, Aufhängungskraft abgezogen, Vorwiderstand eingerechnet) ≥ {P_TARGET / 1000:.0f} kPa, Effektivstrom bei 2 kPa ≤ 50 % des Nennstroms, "
          "Rang nach Leistungsbedarf (weniger Wärme = besser). Ein zu starker Lautsprecher ist kein Nachteil: Vorwiderstand "
          "begrenzt ihn sicher, auch wenn der Verstärker im Fehlerfall Gleichspannung ausgibt. Die Sicherheitsgrenze p_max "
          "vernachlässigt die Aufhängung und liegt damit auf der sicheren Seite; der Vorwiderstand wird danach bemessen."]
    return "\n".join(L) + "\n"


def main(argv):
    src = Path(argv[0]).resolve() if argv else DIR / "lautsprecher_messung.csv"
    rows = [r for r in csv.DictReader(open(src, encoding="utf-8")) if r.get("id", "").strip()]
    if not rows:
        print(f"{src.name} ist noch leer → Beispieldatei wird ausgewertet.")
        src = DIR / "lautsprecher_beispiel.csv"
        rows = [r for r in csv.DictReader(open(src, encoding="utf-8")) if r.get("id", "").strip()]
    out = DIR / ("lautsprecher_auswertung.md" if src.name == "lautsprecher_messung.csv"
                 else src.name.replace("lautsprecher_", "lautsprecher_auswertung_").replace(".csv", ".md"))
    out.write_text(report(rows, src), encoding="utf-8")
    print(out.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main(sys.argv[1:])
