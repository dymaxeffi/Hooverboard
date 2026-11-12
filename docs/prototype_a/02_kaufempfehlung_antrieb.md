# Prototyp A – Kaufempfehlung Antrieb

## Empfehlung: Dayton Audio ND65-4

2,5-Zoll-Breitbandlautsprecher (Ø63 mm, Neodym-Magnet, Aluminiumkonus, 4 Ω), eingesetzt in der Bauform **„Lautsprecher als Motor“**: Ein Stössel auf der Staubkappe treibt eine geplottete Membran Ø20 mm.

| Datenblattwert (G) | Wert | Warum wichtig |
|---|---|---|
| Bl | ≈ 2,7 T·m | viel Kraft pro Ampere |
| Re | ≈ 3,6 Ω (aus Bl/√Re = 1,43) | wenig Spannung nötig |
| Cms (Nachgiebigkeit) | ≈ 1,27 mm/N → Federsteifigkeit 0,79 N/mm | weiche Aufhängung, frisst wenig Kraft |
| Xmax | ±3,5 mm | viel Reserve für Leckkompensation |
| Fs | ≈ 90 Hz | unproblematisch: Die Membrankammer dominiert die Steifigkeit |
| Belastbarkeit | 15 W RMS | grosse thermische Reserve (Betrieb ≈ 0,1 W) |

**Berechnet mit diesen Werten** (B aus G, `lautsprecher_auswertung_kaufkandidaten.md`):

| Grösse | Wert |
|---|---|
| Druck pro Ampere (Membran 2,05 cm²) | 13 kPa/A |
| Strom / Leistung für ±2 kPa | 0,24 A / 0,1 W |
| Ohne Begrenzung im Dichtfall an 5 V | 16,6 kPa → **muss begrenzt werden** |
| Vorwiderstand | rechnerisch 11,2 Ω → **12 Ω** (Normwert), begrenzt auf ≈ 3,8 kPa |
| Mit Leck (0,3 mm Hub), mit 12 Ω | ≈ 2,6 kPa (≥ 2 kPa Ziel) |

Bezugsquellen (Beispiele, Preis und Lieferzeit selbst prüfen; G: ca. CHF 20–35):
- [Dayton Audio Produktseite](https://www.daytonaudio.com/product/63/nd65-4-2-1-2-aluminum-cone-full-range-driver-4-ohm)
- [Parts Express](https://www.parts-express.com/Dayton-Audio-ND65-4-2-1-2-Aluminum-Cone-Full-Range-Driver-290-204)
- [Audiophonics (EU)](https://www.audiophonics.fr/en/midrange-midbass-full-range/dayton-audio-nd65-4-speaker-driver-full-range-aluminium-15w-4-ohm-83db-85hz-20khz-o63cm-p-12827.html)

Datenquellen: [Loudspeaker Database ND65-4](https://loudspeakerdatabase.com/Dayton/ND65-4) · [Speakerbox Lite ND65-4](https://speakerboxlite.com/subwoofers/dayton-audio-nd65-4/specifications)

**Bitte die 4-Ω-Version bestellen (ND65-4), nicht die 8-Ω-Version (ND65-8).**

## Gleich mitbestellen

| Teil | Spezifikation | Zweck |
|---|---|---|
| Vorwiderstand | **12 Ω, ≥ 3 W** (Draht- oder Zementwiderstand) | passive Druckbegrenzung (S1). Im Gleichstrom-Fehler fallen ≈ 1 W an, 3 W gibt Reserve |
| Optional zweites Exemplar | ND65-4 | Ersatz bzw. Vergleich, falls der Stössel-Klebeversuch misslingt |

Verstärker, Mikrocontroller, Drucksensor und Netzteil folgen in Schritt 2 (Elektronik). Erst bestellen, wenn diese Liste steht, dann fällt nur einmal Versand an.

## Warum kein Exciter?

Exciter (Körperschallwandler) sind für das Anregen von Platten gebaut. Ihre Aufhängung ist steif, und die Federsteifigkeit fehlt in den Datenblättern meist (für Visaton EX 45 S und Dayton DAEX25 nicht gefunden). Schon bei 0,15 mm Hub könnte die Feder ein Vielfaches der Druckkraft fressen. Bei ±0,41 N Druckkraft ist das nicht abschätzbar. Ein dokumentierter Lautsprecher mit weicher Aufhängung ist planbar.

## Alternativen (falls ND65-4 nicht lieferbar)

Gesucht ist ein Lautsprecher mit diesen Eckwerten:
- 4 Ω, Ø50–80 mm
- **Bl ≥ 2 T·m**
- **Cms ≥ 0,8 mm/N** (Feder ≤ 1,25 N/mm)
- Xmax ≥ ±1 mm
- flache, geschlossene Staubkappe als Klebefläche für den Stössel

Die Datenblattwerte lassen sich in `lautsprecher_kaufkandidaten.csv` eintragen (Spalten `bl_tm`, `cms_mm_n`) und mit `python calculations/pressure_actuator/speaker_select.py docs/prototype_a/lautsprecher_kaufkandidaten.csv` bewerten.

## Nach Eintreffen

Datenblattwerte sind Herstellerangaben (G). Bl und Federsteifigkeit wie in Schritt 1 nachmessen (Münz-Nullabgleich) und in `lautsprecher_messung.csv` eintragen. Erst mit den gemessenen Werten wird der Vorwiderstand endgültig festgelegt.
