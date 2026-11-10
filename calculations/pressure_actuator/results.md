# Druckwellen-Aktuator – Berechnungsergebnisse (Phase 1)

Erzeugt mit `python calculations/pressure_actuator/model.py`. Stufen: **B** berechnet, **S** simuliert, **G** geschätzt. Experimentell belegte Werte (**E**): keine.

## 1. Benötigtes Verdrängervolumen (B)

Ziel ±2.0 kPa, dichte Kammer: dV = p·V0/(γ·p0).

| V0 | dV für ±2 kPa | dV für ±5 kPa (Grenze) |
|---|---|---|
| 1 cm³ | 14 mm³ | 35 mm³ |
| 2 cm³ | 28 mm³ | 70 mm³ |
| 4 cm³ | 56 mm³ | 141 mm³ |
| 8 cm³ | 113 mm³ | 282 mm³ |

Helmholtz-Resonanz (Kammer 2 cm³, Düse Ø6 × 5 mm): **2042 Hz (B)** → Betrieb 5–150 Hz liegt weit darunter, Kammer verhält sich quasistatisch (Druck folgt dem Volumen, keine Resonanzüberhöhung).

## 2. Verdrängervolumen und Eigensicherheit (B)

Wird die Düse in **Hubmitte** dicht verschlossen, ist die Amplitude durch das Hubvolumen begrenzt (p = γ·p0·dV/V0, linear). Das ist der Normalbetrieb im Dichtfall – **nicht** der Sicherheitsnachweis (siehe unten).

| Konzept | wirksame Fläche | Hub (Amplitude) | dV | V0 | Amplitude dicht | ≤ 5 kPa? |
|---|---|---|---|---|---|---|
| A Voice-Coil Ø40 bei Xmax | 800 mm² | 0.50 mm | 400 mm³ | 4 cm³ | 14.2 kPa | nein |
| B Exzenter e = 0.5 mm | 205 mm² | 0.50 mm | 103 mm³ | 2 cm³ | 7.3 kPa | nein |

**Ungünstigster Fall (Gutachten Safety):** Düse wird in der Endlage dicht verschlossen, die Entlüftung ist verstopft, der Verdränger durchfährt den vollen Doppelhub; exakte Adiabate (B):

| Konzept / Variante | dV (Amplitude) | V0 | p_worst | ≤ 5 kPa? |
|---|---|---|---|---|
| B e = 0.50 mm | 103 mm³ | 2 cm³ | 15.7 kPa | nein |
| B e = 0.34 mm | 70 mm³ | 2 cm³ | 10.4 kPa | nein |
| B e = 0.15 mm | 31 mm³ | 2 cm³ | 4.5 kPa | ja |
| B e = 0.34 mm, V0 = 5 cm³ | 70 mm³ | 5 cm³ | 4.0 kPa | ja |

Grenze B: dV ≤ 34.4 mm³ bei V0 = 2 cm³ → **e ≤ 0.17 mm** (B); mit Toleranz e = 0.15 mm. Dann beträgt die Amplitude im Dichtfall nur ±2.2 kPa (B): **Eigensicherheit über die Geometrie kostet Reserve gegen Leckage** – das ist der zentrale Zielkonflikt von B.

**Konzept A – kraftbegrenzt statt hubbegrenzt (Gutachten Mechatronik/Pneumatik):** Die Luftfeder der Kammer (k = γ·p0·Sd²/V0 = 22.7 kN/m, B) dominiert, die Resonanz liegt bei ≈ 1.1 kHz (B, bewegte Masse 0.5 g G). Der Druck folgt der Kraft: p_max = Bl·U/(Re·Sd), unabhängig vom Moment des Verschliessens.

| Treiber (G) | Bl | Re | Sd | p_max bei 5 V | p_max bei 12 V |
|---|---|---|---|---|---|
| Ø40, 4 Ω | 1.5 T·m | 3.2 Ω | 8.0 cm² | 2.9 kPa | 7.0 kPa |
| Ø40, 4 Ω schwach | 1.0 T·m | 3.2 Ω | 8.0 cm² | 2.0 kPa | 4.7 kPa |
| Ø28, 8 Ω | 0.6 T·m | 7.0 Ω | 3.5 cm² | 1.2 kPa | 2.9 kPa |
| Exciter + Membran Ø20 (A2) | 2.0 T·m | 3.6 Ω | 2.0 cm² | 13.6 kPa | 32.5 kPa |

→ A an einer **fest 5-V-Versorgung** (kein USB-PD) ist mit dem richtigen Treiber elektrisch begrenzt; an 12 V nicht. Sprunganregung kann kurzzeitig bis ≈ 2× überschwingen (G) → Flankensteilheit in Firmware und Hardware begrenzen. Der Exciter A2 mit kleiner Membran braucht eine Spannungsbegrenzung < 5 V oder ein kleineres Bl.

**Statischer Druck durch Erwärmung** einer dichten Kammer (Bleed verstopft): +10 K → 3.5 kPa, +20 K → 6.9 kPa (B). Keine Geometrie- oder Spannungsgrenze erfasst diesen Fall → passives Zweiwege-Überdruckventil als zweite Barriere (Abschnitt 7).

**Entlüftung (Bleed) als Kapillare** Ø0.2 × 30 mm: τ = 0.19 s bei 2 cm³ (B) → Eckfrequenz 0.8 Hz; Gleichanteil 5 → 0.2 kPa in 0.63 s. Die frühere Bohrung Ø0.3–0.5 mm entlüftete 30× zu schnell und vernichtete die Amplitude unter 30 Hz.

C: Eine Mikromembranpumpe (Typ 370, G) erreicht 40–80 kPa Überdruck bzw. −40 kPa Unterdruck → **nicht eigensicher**, die Sicherheit hängt vollständig an Ventilen, Sensor und Firmware.

## 3. Druckamplitude mit Leck (S)

Leckblende A_L bildet die unvollständige Abdichtung an der Düse nach (Prüfadapter im Demonstrator). Diese Tabellen verwenden die ursprünglichen Auslegungswerte (B: e = 0.5 mm) zur Darstellung des Leckeinflusses – nach der Sicherheitskorrektur ist B auf e ≤ 0.15 mm begrenzt (Amplituden dann ≈ 30 %). Werte: eingeschwungen, Spitze positiv / negativ in kPa.

**Konzept B (dV = 103 mm³, V0 = 2 cm³)**

| f | dicht | Leck Ø0.5 mm | Leck Ø1 mm | Leck Ø2 mm | Leck Ø3 mm |
|---|---|---|---|---|---|
| 10 Hz | +7.75 / -6.86 | +1.49 / -1.48 | +0.10 / -0.10 | +0.01 / -0.01 | +0.00 / -0.00 |
| 30 Hz | +7.75 / -6.85 | +5.44 / -5.37 | +0.89 / -0.89 | +0.06 / -0.06 | +0.01 / -0.01 |
| 60 Hz | +7.75 / -6.86 | +6.79 / -6.70 | +2.77 / -2.76 | +0.23 / -0.23 | +0.05 / -0.05 |
| 100 Hz | +7.75 / -6.86 | +7.13 / -7.03 | +4.82 / -4.76 | +0.63 / -0.63 | +0.13 / -0.13 |
| 150 Hz | +7.75 / -6.86 | +7.24 / -7.14 | +6.04 / -5.96 | +1.33 / -1.33 | +0.29 / -0.29 |

**Konzept A (dV = 100 mm³ ≈ 0.12 mm Hub, V0 = 4 cm³)**

| f | dicht | Leck Ø0.5 mm | Leck Ø1 mm | Leck Ø2 mm | Leck Ø3 mm |
|---|---|---|---|---|---|
| 10 Hz | +3.66 / -3.44 | +1.22 / -1.22 | +0.10 / -0.10 | +0.01 / -0.01 | +0.00 / -0.00 |
| 30 Hz | +3.66 / -3.44 | +3.05 / -3.03 | +0.78 / -0.78 | +0.06 / -0.06 | +0.01 / -0.01 |
| 60 Hz | +3.66 / -3.44 | +3.42 / -3.40 | +2.00 / -1.99 | +0.22 / -0.22 | +0.04 / -0.04 |
| 100 Hz | +3.66 / -3.44 | +3.51 / -3.48 | +2.85 / -2.83 | +0.57 / -0.57 | +0.12 / -0.12 |
| 150 Hz | +3.66 / -3.44 | +3.54 / -3.51 | +3.22 / -3.20 | +1.11 / -1.11 | +0.27 / -0.27 |

**Einfluss Entlüftungskapillare und Prüfkammer** (Konzept B, e = 0.15 mm, V0 = 2 cm³, ohne Leckblende) (S):

| f | ohne Bleed | mit Kapillare | mit Kapillare + 5 cm³ Prüfkammer |
|---|---|---|---|
| 5 Hz | +2.22 / -2.14 | +2.16 / -2.15 | +0.62 / -0.62 |
| 10 Hz | +2.22 / -2.14 | +2.18 / -2.17 | +0.62 / -0.62 |
| 30 Hz | +2.22 / -2.14 | +2.19 / -2.18 | +0.62 / -0.62 |
| 100 Hz | +2.22 / -2.14 | +2.19 / -2.18 | +0.63 / -0.62 |

Die Prüfkammer vergrössert das Volumen und senkt den Druck stark → Modell und Messung immer mit dem tatsächlichen Gesamtvolumen (inkl. Schlauch zum Sensor) vergleichen; der Sicherheitsnachweis S1 erfolgt mit Blindstopfen **direkt an der Düse**.

Lesart: Mit dichter Kammer ist der Druck frequenzunabhängig (reiner Volumeneffekt). Je grösser das Leck, desto stärker fällt die Amplitude bei tiefen Frequenzen ab (Luft entweicht innerhalb einer Periode). Für ein Leck Ø2 mm braucht man bei 30 Hz ein Vielfaches des Hubvolumens → **Abdichtung/Düsengeometrie ist die wichtigste Einflussgrösse**, nicht die Antriebskraft. Nichtlinear: im Dichtfall sind die Überdruckspitzen grösser als die Unterdruckspitzen (+7.75 / −6.86 kPa).

## 4. Kräfte, Leistung, Antrieb (B/G)

| Grösse | A Voice-Coil | B Exzenter | C Pumpe + Ventile |
|---|---|---|---|
| Druck pro Strom | Bl/Sd: Ø40 (Bl 1.5) 1.9 kPa/A; Ø28 (Bl 0.6) 1.7 kPa/A; Exciter A2 (Bl 2) 9.8 kPa/A (B aus G) | – | – |
| Kraft auf Verdränger bei 2 kPa | 1.60 N (B) | 0.41 N (B) | – |
| Antriebsmoment / Strom | Bl ≈ 1.5 T·m (G) → I ≈ 1.1 A Spitze | M = F·e = 0.21 mN·m (B) | Pumpe 3–6 V, 0.2–0.4 A (G) |
| Pneumatische Leistung (dicht, Blindleistung) | ≈ 0 W | ≈ 0 W | – |
| Pneumatische Wirkleistung Leck Ø1 mm, ±2 kPa (obere Schranke p·Q_peak/2) | ≈ 0.03 W (B) | gleich | Pumpe muss Leckstrom nachliefern |
| Elektrische Leistung bei 2 kPa dicht | Ø40/4 Ω: 1.8 W; Ø28/8 Ω (Bl 0.6): ≈ 5.4 W, 9.3 V Spitze → an 5 V nicht erreichbar; Exciter A2: ≈ 0.15 W (B aus G) | 0.5–1.5 W (G, Motor 130/N20 ohne Getriebe) | 2–4 W (G, 2 Pumpen + 2 Ventile; Ventilspulen je 1–2 W) |
| Drehzahl / Frequenz | direkt 1–200 Hz (Verstärker, untere Grenzfrequenz des Moduls prüfen) | f = n/60; stabiler Lauf Bürstenmotor erst ab ≈ 600–900 min⁻¹ → **≈ 10–150 Hz** (G); Gimbal-BLDC mit FOC ab ≈ 1 Hz | Ventile 10–20 ms (G) → ≈ 5–25 Hz |

## 5. Geräusch (G – nur Grössenordnung, Messung nötig)

Tieffrequente Druckschwankungen (5–150 Hz) sind wenig hörbar (A-Bewertung −70…−17 dB). Hörbar sind vor allem: Gehäuse-/Lagergeräusche und Harmonische (B: Motorbürsten ~kHz, Unwucht; C: Pumpe + Ventilklicken; A: Oberwellen und Gehäuseresonanzen). Ziel Demonstrator: < 50 dB(A) in 30 cm – Messung mit Klasse-2-Messgerät (A0-11).

