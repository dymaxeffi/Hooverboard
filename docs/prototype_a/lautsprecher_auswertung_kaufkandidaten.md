# Prototyp A – Auswertung Lautsprecher

> Automatisch erzeugt von `calculations/pressure_actuator/speaker_select.py` aus `docs/prototype_a/lautsprecher_kaufkandidaten.csv`.

Annahmen: Verstärker 5.0 V Spitze (H-Brücke an 5 V, ungünstigster Fall), Ziel ±2 kPa, Reserve ≥ 3 kPa, Begrenzung 4 kPa (Projektgrenze 5 kPa). Bl und Re gemessen (E), alle abgeleiteten Werte berechnet (B) mit dem Modell „Kammer steifer als Aufhängung“.

Bauformen: **direkt** = Konus bildet die Kammerwand (Fläche Sd); **Motor** = Konus offen, Stössel auf der Staubkappe treibt eine geplottete Membran Ø20/12 (wirksam 2.05 cm²). Je Lautsprecher ist die bessere Bauform gezeigt.

| Rang | ID | Beschreibung | Bauform | wirks. Fläche cm² | Re Ω | Bl T·m | Feder N/mm | kPa/A | p_max 5 V ohne Begrenzung | Vorwiderstand | dicht max. (begrenzt) | mit Leck, 0,3 mm Hub | Strom für 2 kPa | Leistung 2 kPa | Status | Hinweise |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | W1-2121S | Tang Band W1-2121S 1.75in Alu Neodym 4 Ohm (Datenblattwerte G) | motor | 2.05 | 3.5 | 3.14 | 1.05 | 15.30 | 21.9 kPa | 15.6 Ω | 4.0 kPa | 2.5 kPa | 0.23 A / 0.8 V | 0.09 W | **geeignet** |  |
| 2 | ND65-4 | Dayton Audio ND65-4 2.5in Alu Neodym 4 Ohm (Datenblattwerte G) | motor | 2.05 | 3.6 | 2.70 | 0.79 | 13.15 | 18.5 kPa | 12.9 Ω | 4.0 kPa | 2.8 kPa | 0.24 A / 0.9 V | 0.10 W | **geeignet** |  |
| 3 | CE32A-4 | Dayton CE32A-4 1.25in Mini 4 Ohm (Bl abgeleitet; Cms GESCHAETZT aus Fs 262 Hz und Mms 0.3 g) | motor | 2.05 | 3.6 | 1.59 | 0.81 | 7.75 | 10.8 kPa | 6.1 Ω | 4.0 kPa | 2.8 kPa | 0.41 A / 1.5 V | 0.30 W | **geeignet** |  |
| 4 | NSW1-205-8A | Aura Cougar NSW1-205-8A 1in Neodym 8 Ohm (Datenblattwerte G) | motor | 2.05 | 5.5 | 1.90 | 0.96 | 9.26 | 8.4 kPa | 6.1 Ω | 4.0 kPa | 2.6 kPa | 0.37 A / 2.0 V | 0.37 W | **geeignet** |  |

## Empfehlung

**W1-2121S – Tang Band W1-2121S 1.75in Alu Neodym 4 Ohm (Datenblattwerte G), Bauform motor**: braucht für ±2 kPa nur 0.09 W (0.23 A Spitze). Vorwiderstand 15.6 Ω (Belastbarkeit ≥ 1.1 W für den DC-Fehlerfall) begrenzt p_max auf 4.0 kPa.

Ersatz: ND65-4, CE32A-4, NSW1-205-8A.

Kriterien: dicht max. ≥ 3 kPa nach Begrenzung, **und** mit Leck (Hub 0.3 mm, Aufhängungskraft abgezogen, Vorwiderstand eingerechnet) ≥ 2 kPa, Effektivstrom bei 2 kPa ≤ 50 % des Nennstroms, Rang nach Leistungsbedarf (weniger Wärme = besser). Ein zu starker Lautsprecher ist kein Nachteil: Vorwiderstand begrenzt ihn sicher, auch wenn der Verstärker im Fehlerfall Gleichspannung ausgibt. Die Sicherheitsgrenze p_max vernachlässigt die Aufhängung und liegt damit auf der sicheren Seite; der Vorwiderstand wird danach bemessen.
