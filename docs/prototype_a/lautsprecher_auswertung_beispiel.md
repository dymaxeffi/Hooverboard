# Prototyp A – Auswertung Lautsprecher

> Automatisch erzeugt von `calculations/pressure_actuator/speaker_select.py` aus `docs/prototype_a/lautsprecher_beispiel.csv`.

Annahmen: Verstärker 5.0 V Spitze (H-Brücke an 5 V, ungünstigster Fall), Ziel ±2 kPa, Reserve ≥ 3 kPa, Begrenzung 4 kPa (Projektgrenze 5 kPa). Bl und Re gemessen (E), alle abgeleiteten Werte berechnet (B) mit dem Modell „Kammer steifer als Aufhängung“.

Bauformen: **direkt** = Konus bildet die Kammerwand (Fläche Sd); **Motor** = Konus offen, Stössel auf der Staubkappe treibt eine geplottete Membran Ø20/12 (wirksam 2.05 cm²). Je Lautsprecher ist die bessere Bauform gezeigt.

| Rang | ID | Beschreibung | Bauform | wirks. Fläche cm² | Re Ω | Bl T·m | Feder N/mm | kPa/A | p_max 5 V ohne Begrenzung | Vorwiderstand | dicht max. (begrenzt) | mit Leck, 0,3 mm Hub | Strom für 2 kPa | Leistung 2 kPa | Status | Hinweise |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | BSP4 | BEISPIEL Tieftöner 50 mm 4 Ohm | motor | 2.05 | 3.6 | 2.35 | 0.37 | 11.47 | 15.9 kPa | 10.7 Ω | 4.0 kPa | 3.5 kPa | 0.22 A / 0.8 V | 0.09 W | **geeignet** |  |
| 2 | BSP1 | BEISPIEL Breitband 40 mm 4 Ohm | motor | 2.05 | 3.4 | 1.44 | 0.65 | 7.01 | 10.3 kPa | 5.4 Ω | 4.0 kPa | 3.1 kPa | 0.42 A / 1.4 V | 0.30 W | **geeignet** |  |
| 3 | BSP2 | BEISPIEL Kleinlautsprecher 28 mm 8 Ohm | motor | 2.05 | 7.2 | 0.58 | 0.36 | 2.80 | 1.9 kPa | – | 1.9 kPa | 1.4 kPa | 0.90 A / 6.5 V | 2.92 W | **zu schwach** | Strom 171 % Nennstrom, Stössel auf Gewebekappe: Klebefläche verstärken |
| 4 | BSP3 | BEISPIEL Laptop-Lautsprecher 20x30 mm | motor | 2.05 | 7.8 | 0.36 | 0.27 | 1.75 | 1.1 kPa | – | 1.1 kPa | 0.7 kPa | 1.37 A / 10.7 V | 7.28 W | **zu schwach** | Strom 270 % Nennstrom |
| – | BSP5 | BEISPIEL ohne Bl-Messung | – | – | 7.0 | – | – | – | – | – | – | – | – | – | Bl messen |  |

## Empfehlung

**BSP4 – BEISPIEL Tieftöner 50 mm 4 Ohm, Bauform motor**: braucht für ±2 kPa nur 0.09 W (0.22 A Spitze). Vorwiderstand 10.7 Ω (Belastbarkeit ≥ 1.3 W für den DC-Fehlerfall) begrenzt p_max auf 4.0 kPa.

Ersatz: BSP1.

Kriterien: dicht max. ≥ 3 kPa nach Begrenzung, **und** mit Leck (Hub 0.3 mm, Aufhängungskraft abgezogen, Vorwiderstand eingerechnet) ≥ 2 kPa, Effektivstrom bei 2 kPa ≤ 50 % des Nennstroms, Rang nach Leistungsbedarf (weniger Wärme = besser). Ein zu starker Lautsprecher ist kein Nachteil: Vorwiderstand begrenzt ihn sicher, auch wenn der Verstärker im Fehlerfall Gleichspannung ausgibt. Die Sicherheitsgrenze p_max vernachlässigt die Aufhängung und liegt damit auf der sicheren Seite; der Vorwiderstand wird danach bemessen.
