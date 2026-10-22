# Physikalische Machbarkeit – Phase 0 (Vorbereitung Phase 1)

> **Nachweisstufe: B (berechnet).** Alle Zahlen stammen aus `calculations/phase0_estimate.py`
> (vollständige Tabellen: [`calculations/results/phase0_estimate.md`](../calculations/results/phase0_estimate.md)).
> Die Modelle sind Lehrbuchphysik; die empirischen Beiwerte sind Annahmen und werden in Prototyp A0 gemessen.

## 1. Kernaussage

**Bodengebundenes Schweben auf einem Luftkissen mit Schürze ist mit Akku-Technik im Bereich von etwa 0.2–1.5 kW elektrisch erreichbar. Freier Flug mit Impellern oder Rotoren braucht 20–75 kW und ist für dieses Projekt nicht vertretbar.**

Das ist keine Designvorliebe, sondern folgt aus der Strahltheorie: Die Leistung zum Tragen eines Gewichts sinkt mit der Fläche, über die Luft beschleunigt wird. Ein Luftkissen „stützt“ sich mit kleinem Überdruck auf die ganze Board-Fläche und verliert Luft nur durch einen Spalt von wenigen Millimetern. Ein Impeller muss die ganze Gewichtskraft über eine kleine Strahlfläche erzeugen.

## 2. Freier Flug vs. bodengebundenes Schweben

| | Bodengebundenes Schweben (Luftkissen) | Freier Flug (Schub = Gewicht) |
|---|---|---|
| Tragmechanismus | statischer Überdruck unter dem Board | Impuls eines Luftstrahls |
| Höhe | durch Schürze/Spalt fest, selbststabilisierend in der Höhe | beliebig, muss aktiv geregelt werden |
| Ausfall Antrieb | Board setzt aus 2–5 cm auf | Absturz |
| Leistung (nominal, 42.5 kg) | ca. 0.2–1.5 kW | ca. 23–75 kW |

Das Projekt wird daher als **Luftkissenfahrzeug (Hovercraft)** entwickelt, nicht als Fluggerät. Der Projekttitel „real flugfähig“ wird in diesem Sinn interpretiert (Vorschlag D-002, Freigabe nötig).

## 3. Kräfte

Massenbudget (Annahmen, vor CAD): Board 8.5 / **12.5** / 18 kg → Gesamtmasse 38.5 / **42.5** / 48 kg → Gewichtskraft 378 / **417** / 471 N. Gebläseauslegung mit Reserve 1.25: **521 N** (nominal).

## 4. Luftkissen mit Schürze (Board 800 × 500 mm)

- Kissenfläche 0.329 m² → Druck **≈ 1.27 kPa** (129 mm Wassersäule), Auslegung 1.58 kPa
- Austrittsgeschwindigkeit am Spalt ≈ 47 m/s
- Elektrische Hubleistung (η_Fan = 0.45):

| eff. Leckspalt | 1 mm | 2 mm | 3 mm | 5 mm |
|---|---:|---:|---:|---:|
| P_el nominal | 206 W | 412 W | 619 W | 1031 W |
| P_el Spannweite η_Fan 0.30–0.60 | 155–309 W | 309–619 W | 464–928 W | 773–1546 W |

**Wichtig:** Mit Schürze ist die „Schwebehöhe“ von 2–5 cm die Höhe der Schürze, nicht der Luftspalt. Der Luftspalt unter der Schürzenkante beträgt nur Millimeter. Ohne Schürze (Spalt = 20–50 mm) steigt der Bedarf auf **4–10 kW** (Faktor ≈ 10).

## 5. Einfluss der Board-Grösse

Bei gleichem Leckspalt gilt P ∝ p^1.5 · U. Grössere Boards senken den Druck stärker, als der Umfang wächst:

| L × B | 600 × 360 | 700 × 420 | 800 × 480 | 900 × 540 | 1000 × 600 |
|---|---:|---:|---:|---:|---:|
| Druck | 2.24 kPa | 1.68 kPa | 1.31 kPa | 1.06 kPa | 0.88 kPa |
| P_el (3 mm, η 0.45) | 1078 W | 815 W | 644 W | 528 W | 445 W |

→ Zielkonflikt Z-01: „Kompakt“ kostet Leistung, Akkumasse und vermutlich Lärm (höherer Druck = schnellere Gebläse). Empfehlung: Grösse nicht verkleinern, bevor Messungen vorliegen. 800 × 500 mm bleibt Startpunkt.

## 6. Vortrieb, Bremsen, Lenken

Kraftbedarf bei 2 m/s: Luftwiderstand ≈ 1 N, Impulswiderstand ≈ 0.4 N, **Schürzenschleppen ≈ 21 N (Annahme, völlig unbekannt)**, Beschleunigung 0.5 m/s² ≈ 21 N, Steigung 2° ≈ 15 N → **≈ 58 N**.
Statischer Schub 58 N braucht ≈ 2.1 kW (2 × Ø 200 mm) bzw. ≈ 1.4 kW (2 × Ø 300 mm) elektrisch als Spitze.

Folgen:
- Ein Luftkissenfahrzeug hat praktisch keine Bodenreibung. **Bremsen und Lenken brauchen aktiven Schub** (Gegenschub, Differenzschub) oder Absenken des Kissens.
- Gewichtsverlagerung verschiebt den Schwerpunkt (siehe 7) und erzeugt Drift, aber kein kontrolliertes Gieren → reicht als Steuerung nicht.

## 7. Schwerpunkt und Stabilität

Pilot verlagert sich um 5 / 10 / 15 cm → Gesamtschwerpunkt wandert 3.5 / 7.1 / 10.6 cm, Kippmoment 15 / 29 / 44 N·m.
Ein einzelnes Plenum mit gleichmässigem Druck erzeugt **kein** Rückstellmoment; nur die Schürzengeometrie hält das Board gerade. Bei einem Kind auf einem 50 cm breiten Board ist das das grösste funktionale Risiko (R-03). Kandidaten: Kammerung (Längs-/Querkiel), Bag-and-Finger-Schürze, aktiv geregelte Kammerdrücke (K5b).

## 8. Energie

Annahme Dauerleistung ≈ 1.05 kW (Hub bei 3 mm Spalt + 30 % Vortriebsspitze):
5 min → 116 Wh · 10 min → 233 Wh · 15 min → 349 Wh (Nennenergie bei 75 % nutzbarem Anteil).
Bei einer angenommenen Pack-Energiedichte von 150 Wh/kg sind das 0.8–2.3 kg – im Massenbudget enthalten.

## 9. Modellgrenzen

- Konstante Ausflusszahl Cd = 0.6; reale Schürzenspalte sind nicht scharfkantig und ändern sich mit Druck.
- Leckspalt als feste Grösse; in Wirklichkeit dynamisch (Bodenunebenheit, Schürzenflattern).
- Gebläse als Punkt mit festem Wirkungsgrad; reale p-Q-Kennlinien sind nötig (Messung A0).
- Kein Randstrahl-Modell, keine Schürzen-Membranmechanik, keine Dynamik (Phase 3).
- Bodeneffekt-Formel nur für z/R ≥ 0.5 gültig.
