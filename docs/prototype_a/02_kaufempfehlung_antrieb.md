# Prototyp A – Kaufempfehlung Antrieb

> **Aktualisiert:** Der zuerst empfohlene ND65-4 (Ø63 mm) ist für ein kompaktes Gerät zu gross. Kleinere Treiber funktionieren in der Bauform „Lautsprecher als Motor“ ebenfalls, weil die kleine Membran Ø20 die Druckarbeit macht und der Lautsprecher nur Kraft liefert. Die Baugrösse wird dann im Wesentlichen durch den Korbdurchmesser und die Einbautiefe bestimmt.

## Vergleich kleiner Treiber (Datenblattwerte G, berechnet B)

Auswertung: `lautsprecher_auswertung_kaufkandidaten.md`.

| Treiber | Nenngrösse | Bl | Re | Feder | Strom / Leistung für 2 kPa | Vorwiderstand (rechn. → Normwert) | Datenlage |
|---|---|---|---|---|---|---|---|
| **Dayton Audio CE32A-4** | **1¼" (≈ Ø32 mm)** | 1,59 T·m | 3,6 Ω | ≈ 0,8 N/mm (**geschätzt**) | 0,41 A / 0,3 W | 6,1 → **6,8 Ω** | Bl aus Bl/√Re abgeleitet, Cms nicht veröffentlicht |
| Aura Cougar NSW1-205-8A | 1" | 1,9 T·m | 5,5 Ω | 0,96 N/mm | 0,37 A / 0,4 W | 6,1 → **6,8 Ω** | Quellen teils widersprüchlich (Xmax, Vas) |
| **Tang Band W1-2121S** | 1¾" | 3,14 T·m | 3,5 Ω | 1,05 N/mm | 0,23 A / 0,09 W | 15,6 → **18 Ω** | konsistent in mehreren Quellen |
| Dayton Audio ND65-4 | 2½" (Ø63 mm) | 2,7 T·m | 3,6 Ω | 0,79 N/mm | 0,24 A / 0,10 W | 13,2 → 15 Ω | gut dokumentiert, **zu gross** |

Alle vier erreichen im Dichtfall die Begrenzung von 4 kPa und mit Leck (0,3 mm Hub) 2,5–2,8 kPa. Die Aussenmasse (Korb, Tiefe) bitte vor der Bestellung im Datenblatt des Händlers prüfen; die Nenngrösse in Zoll bezieht sich auf die Membran, der Korb ist etwas grösser.

## Empfehlung

**Gewählt (2026-11-12): Tang Band W1-2121S als Hauptantrieb**, Vorwiderstand **18 Ω, ≥ 3 W**.

> **Aktualisiert:** Treiber ist jetzt eine H-Brücke DRV8833 (der Verstärker PAM8302A ist nicht lieferbar). Sie kann im Fehlerfall die vollen 5 V ausgeben, deshalb ist der Vorwiderstand auf 5 V ausgelegt (vorher 4,5 V). Mit 18 Ω: p_max 3,6 kPa, mit Leck 2,0 kPa, Fehlerstrom 0,23 A (Widerstand 1,0 W, Spule 0,19 W) (B aus G). Nach der Bl-Messung ggf. 15–16 Ω.

**Vor der Bestellung prüfen:** Hat der Treiber in der Mitte eine bewegliche Staubkappe oder einen **feststehenden Phasenstöpsel**? Bei einem Phasenstöpsel wird der Stössel nicht mittig geklebt, sondern über einen **ringförmigen Mitnehmer** am Konus um den Stöpsel angekoppelt (Konstruktion Schritt 3).

Weitere Optionen:

- **Kompakt:** **Dayton Audio CE32A-4** – kleinster Kandidat und günstig. Die Federsteifigkeit ist geschätzt, deshalb nach Eintreffen unbedingt mit dem Münz-Nullabgleich nachmessen.
- **Sicher dokumentiert und stärker:** **Tang Band W1-2121S** – etwas grösser, aber mit den verlässlichsten Daten und der grössten Reserve.

Da beide günstig sind, lohnt es sich, **2 × CE32A-4 und 1 × W1-2121S** zu bestellen und am Prototyp zu vergleichen.

Bezugsquellen (Beispiele):
- [CE32A-4 bei Parts Express](https://parts-express.com/Dayton-Audio-CE32A-4-1-1-4-Mini-Speaker-4-Ohm-285-103) · [CE32A-4 bei Soundimports (EU)](https://www.soundimports.eu/dayton-audio-ce32a-4.html) · [Hersteller](https://daytonaudio.com/product/1138/ce32a-4-1-1-4-mini-speaker-driver-4-ohm)
- [W1-2121S bei Parts Express](https://www.parts-express.com/Tang-Band-W1-2121S-1-3-4-Aluminum-Full-Range-Neodymium-Driv-264-825) · [W1-2121S bei Nonsolospeakers (EU)](https://www.nonsolospeakers.com/en/home/1780-w1-2121s-175-full-range-tb-speakers-tang-band.html)

Datenquellen: [Loudspeaker Database W1-2121S](https://loudspeakerdatabase.com/TangBand/W1-2121S) · [Loudspeaker Database CE32A-4](https://loudspeakerdatabase.com/Dayton/CE32A-4) · [Dayton Datenblatt CE32A-4](https://daytonaudio.com/images/resources/285-103-dayton-audio-ce32a-4-spec-sheet.pdf) · [Speakerbox Lite NSW1-205-8A](https://speakerboxlite.com/subwoofers/aura-nsw1-205-8a/specifications)

## Gleich mitbestellen

| Teil | Spezifikation | Zweck |
|---|---|---|
| Vorwiderstände | je 2 × **6,8 Ω, 15 Ω, 18 Ω**, je ≥ 3 W (Draht/Zement) | passive Druckbegrenzung (S1), passend zu jedem Kandidaten; endgültiger Wert nach Messung |

Verstärker, Mikrocontroller, Drucksensor und Netzteil folgen in Schritt 2 – am besten zusammen bestellen.

---

## Ursprüngliche Empfehlung (zu gross): Dayton Audio ND65-4

> Historisch, nicht mehr gültig: Die Werte in diesem Abschnitt sind noch mit 4,5 V Verstärkerspannung berechnet. Mit der H-Brücke (5 V) wären 15 Ω nötig.


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

### Zubehör (nur für ND65-4)

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
