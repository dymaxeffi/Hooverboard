# Phase 0 – Erste physikalische Abschätzung (automatisch erzeugt)

> **Status: BERECHNUNG auf Basis von Annahmen.** Keine Messwerte, keine Simulation, keine experimentelle Bestätigung. Erzeugt von `calculations/phase0_estimate.py`; Parameter in `calculations/hoverlib/parameters.py`.

## 1. Randbedingungen

- Luftdichte ρ = 1.141 kg/m³ (ISA-Druck 450 m ü. M., 20 °C)
- Board-Grundriss 800 × 500 mm, Eckradius 120 mm
- Wirksame Kissenfläche A = 0.329 m², Leckumfang U = 2.21 m (Flächenanteil 0.85)
- Ausflusszahl Cd = 0.6 (ANN), Antriebswirkungsgrad η_Motor·ESC = 0.85 (ANN)
- Gebläsewirkungsgrad η_Fan = 0.3 / 0.45 / 0.6 (pessimistisch / nominal / optimistisch, ANN)

## 2. Massenbudget (Annahmen, vor CAD)

| Position | leicht [kg] | nominal [kg] | schwer [kg] |
|---|---:|---:|---:|
| Tragstruktur/Deck | 2.8 | 4.0 | 6.0 |
| Schuerze | 0.6 | 1.0 | 1.5 |
| Hubgeblaese inkl. Motor | 1.0 | 1.5 | 2.5 |
| Vortrieb | 1.0 | 1.5 | 2.0 |
| Akku | 1.8 | 2.5 | 3.5 |
| Elektronik/Kabel | 0.5 | 0.8 | 1.0 |
| Schutz/Kleinteile | 0.8 | 1.2 | 1.5 |
| **Board gesamt** | **8.5** | **12.5** | **18.0** |
| Pilot | 30.0 | 30.0 | 30.0 |
| **Gesamtmasse m** | **38.5** | **42.5** | **48.0** |
| Gewichtskraft m·g [N] | 378 | 417 | 471 |
| Auslegung m·g·1.25 [N] | 472 | 521 | 588 |

Beobachtung: Das Board wiegt in allen Szenarien 30–60 % der Pilotenmasse. Eigengewicht ist damit ein Haupttreiber des Leistungsbedarfs.

## 3. Konzept K1 – Luftkissen mit Schürze (nominale Masse)

- Kissendruck nominal p = 1'265 Pa (= 129 mm Wassersäule), Auslegung 1'581 Pa
- Austrittsgeschwindigkeit am Spalt v = 47.1 m/s

| eff. Leckspalt h [mm] | Q [m³/s] | Luftleistung [W] | P_el η_Fan=0.30 [W] | P_el 0.45 [W] | P_el 0.60 [W] | P_el Auslegung, 0.45 [W] |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0.062 | 79 | 309 | 206 | 155 | 288 |
| 2 | 0.125 | 158 | 619 | 412 | 309 | 576 |
| 3 | 0.187 | 237 | 928 | 619 | 464 | 864 |
| 5 | 0.312 | 394 | 1'546 | 1'031 | 773 | 1'441 |

Der effektive Leckspalt bestimmt die Leistung linear. Er hängt von Schürzenbauart, Untergrund und Druck ab und ist **die wichtigste unbekannte Grösse** → Messung in Prototyp A.

## 4. Konzept K2 – Luftkissen ohne Schürze (Spalt = Schwebehöhe)

| Schwebehöhe [mm] | Q [m³/s] | Luftleistung [W] | P_el η_Fan=0.45 [W] |
|---:|---:|---:|---:|
| 20 | 1.25 | 1'577 | 4'124 |
| 30 | 1.87 | 2'366 | 6'186 |
| 50 | 3.12 | 3'943 | 10'310 |

Einfaches Plenum-Modell. Ein Randstrahl-Design (Peripheral Jet) kann den Bedarf senken; der Effekt wird in Phase 1 mit Literaturmodell quantifiziert, nicht hier angenommen.

## 5. Konzepte K3/K4 – Impeller / Rotoren mit Schub = Gewicht

Schub T = 417 N (nur Schweben, ohne Steuerreserve). Guetegrad Impeller 0.6, offener Rotor 0.65 (ANN).

| Anordnung | Strahlfläche [m²] | Strahlgeschw. [m/s] | P_ideal [W] | P_el [W] | P_el bei T/W = 1.5 [W] |
|---|---:|---:|---:|---:|---:|
| 4 × Impeller Ø 90 mm | 0.0214 | 185 | 38'521 | 75'532 | 138'761 |
| 4 × Impeller Ø 120 mm | 0.0380 | 139 | 28'891 | 56'649 | 104'071 |
| 8 × Impeller Ø 120 mm | 0.0760 | 98 | 20'429 | 40'057 | 73'589 |
| 4 × Propeller Ø 0.25 m (Grenzfall Grundriss) | 0.1963 | 61 | 12'710 | 23'004 | 42'262 |

Bodeneffekt (Cheeseman–Bennett) für Ø 120 mm bei 30 mm Höhe: z/R = 0.5 → Faktor 0.75 (Grenze der Modellgültigkeit: ja). Kleinere Höhen liegen ausserhalb des Modells; dort geht ein Impeller-Board physikalisch in ein Luftkissen ohne Schürze über.

## 6. Grössenordnungsvergleich (nominal)

- K1 Schürze, Spalt 3 mm, η_Fan 0.45: **≈ 619 W elektrisch**
- K2 ohne Schürze, 30 mm: **≈ 6'186 W** (Faktor 10)
- K3 8 × Impeller Ø 120 mm: **≈ 40'057 W** (Faktor 65), ohne Steuerreserve

## 7. Parameterstudie Board-Grösse (K1, Spalt 3 mm, η_Fan 0.45)

Seitenverhältnis B/L = 0.6; Strukturmasse skaliert mit Grundfläche (nominal 4.0 kg bei 0.8 × 0.5 m), übrige Board-Massen konstant.

| L × B [mm] | A_Kissen [m²] | m_ges [kg] | p [Pa] | P_el [W] |
|---|---:|---:|---:|---:|
| 600 × 360 | 0.178 | 40.7 | 2'238 | 1'078 |
| 700 × 420 | 0.242 | 41.4 | 1'676 | 815 |
| 800 × 480 | 0.317 | 42.3 | 1'311 | 644 |
| 900 × 540 | 0.403 | 43.4 | 1'057 | 528 |
| 1000 × 600 | 0.499 | 44.6 | 875 | 445 |
| 1200 × 720 | 0.724 | 47.3 | 641 | 338 |

Physik: P ∝ p^1.5 · U. Grössere Fläche senkt den Druck stärker als der Umfang wächst – **grössere Boards brauchen weniger Hubleistung**, sind aber schwerer, sperriger und teurer. Das widerspricht dem Ziel „möglichst kompakt“ (siehe Zielkonflikt Z-01).

## 8. Vortrieb (nominal)

Bei v = 2.0 m/s (Gehtempo, vorgeschlagene Höchstgeschwindigkeit):

- Luftwiderstand Pilot+Board: 1.0 N
- Impulswiderstand Kissenluft: 0.4 N
- Schürzenschleppen (Beiwert 0.05, ANN): 20.8 N
- Beschleunigung 0.5 m/s²: 21.2 N
- Steigung 2°: 14.5 N
- **Summe ≈ 58 N** → 2 Antriebe à ≈ 29 N, Bremsen mit gleichem Betrag (Reversierung oder Schubumlenkung nötig).

- Statischer Schub 58 N mit 2 × Ø 200 mm Propellern: ≈ 2'140 W elektrisch (Spitze, nicht Dauer)
- Statischer Schub 58 N mit 2 × Ø 300 mm Propellern: ≈ 1'427 W elektrisch (Spitze, nicht Dauer)

Grössere Propeller senken die Vortriebsleistung deutlich, kosten aber Bauraum und erhöhen das Risiko an rotierenden Teilen (Zielkonflikt Z-04).

## 9. Energiebedarf

Annahme (ANN): Dauerleistung = Hub (Spalt 3 mm) + 30 % der Vortriebsspitze (Ø 300 mm) ≈ 1'047 W.

| Flugzeit | Nenn-Akkuenergie [Wh] | Masse bei 150 Wh/kg Pack (ANN) [kg] |
|---|---:|---:|
| 5 min | 116 | 0.78 |
| 10 min | 233 | 1.55 |
| 15 min | 349 | 2.33 |

## 10. Schwerpunkt und Kippstabilität

- Pilot verlagert sich um 5 cm → Gesamtschwerpunkt wandert 3.5 cm, Kippmoment 15 N·m
- Pilot verlagert sich um 10 cm → Gesamtschwerpunkt wandert 7.1 cm, Kippmoment 29 N·m
- Pilot verlagert sich um 15 cm → Gesamtschwerpunkt wandert 10.6 cm, Kippmoment 44 N·m

Ein einzelnes Plenum mit gleichförmigem Druck hat **kein** aufrichtendes Moment aus dem Druck selbst; die Rückstellung kommt allein aus der Schürzengeometrie. Gegenmassnahmen (Kammerung/Kiel, Bag-and-Finger, aktive Regelung) werden in Phase 1 bewertet.
