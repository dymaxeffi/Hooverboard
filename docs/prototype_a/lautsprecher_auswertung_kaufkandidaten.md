# Prototyp A – Auswertung Lautsprecher

> Automatisch erzeugt von `calculations/pressure_actuator/speaker_select.py` aus `docs/prototype_a/lautsprecher_kaufkandidaten.csv`.

Annahmen: Verstärker 4.5 V Spitze (Klasse-D-BTL an 5 V), Ziel ±2 kPa, Reserve ≥ 3 kPa, Begrenzung 4 kPa (Projektgrenze 5 kPa). Bl und Re gemessen (E), alle abgeleiteten Werte berechnet (B) mit dem Modell „Kammer steifer als Aufhängung“.

Bauformen: **direkt** = Konus bildet die Kammerwand (Fläche Sd); **Motor** = Konus offen, Stössel auf der Staubkappe treibt eine geplottete Membran Ø20/12 (wirksam 2.05 cm²). Je Lautsprecher ist die bessere Bauform gezeigt.

| Rang | ID | Beschreibung | Bauform | wirks. Fläche cm² | Re Ω | Bl T·m | Feder N/mm | kPa/A | p_max 5 V ohne Begrenzung | Vorwiderstand | dicht max. (begrenzt) | mit Leck, 0,3 mm Hub | Strom für 2 kPa | Leistung 2 kPa | Status | Hinweise |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | ND65-4 | Dayton Audio ND65-4 2.5in Alu Neodym 4 Ohm (Datenblattwerte G) | motor | 2.05 | 3.6 | 2.70 | 0.79 | 13.15 | 16.6 kPa | 11.2 Ω | 4.0 kPa | 2.8 kPa | 0.24 A / 0.9 V | 0.10 W | **geeignet** |  |

## Empfehlung

**ND65-4 – Dayton Audio ND65-4 2.5in Alu Neodym 4 Ohm (Datenblattwerte G), Bauform motor**: braucht für ±2 kPa nur 0.10 W (0.24 A Spitze). Vorwiderstand 11.2 Ω (Belastbarkeit ≥ 1.0 W für den DC-Fehlerfall) begrenzt p_max auf 4.0 kPa.

Kriterien: dicht max. ≥ 3 kPa nach Begrenzung, **und** mit Leck (Hub 0.3 mm, Aufhängungskraft abgezogen, Vorwiderstand eingerechnet) ≥ 2 kPa, Effektivstrom bei 2 kPa ≤ 50 % des Nennstroms, Rang nach Leistungsbedarf (weniger Wärme = besser). Ein zu starker Lautsprecher ist kein Nachteil: Vorwiderstand begrenzt ihn sicher, auch wenn der Verstärker im Fehlerfall Gleichspannung ausgibt. Die Sicherheitsgrenze p_max vernachlässigt die Aufhängung und liegt damit auf der sicheren Seite; der Vorwiderstand wird danach bemessen.
