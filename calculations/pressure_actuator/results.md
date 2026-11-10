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

Wenn die Düse vollständig dicht verschlossen wird, ist der grösste mögliche Druck durch das Hubvolumen begrenzt (p_max = γ·p0·dV/V0). Liegt dieser Wert unter der Grenze, ist das Konzept **eigensicher** gegen Überdruck.

| Konzept | wirksame Fläche | Hub (Amplitude) | dV | V0 | p_max dicht | eigensicher (≤ 5 kPa)? |
|---|---|---|---|---|---|---|
| A Voice-Coil Ø40 bei Xmax | 800 mm² | 0.50 mm | 400 mm³ | 4 cm³ | 14.2 kPa | nein → Hub begrenzen oder V0 erhöhen |
| B Exzenter e = 0.5 mm | 205 mm² | 0.50 mm | 103 mm³ | 2 cm³ | 7.3 kPa | nein → Hub begrenzen oder V0 erhöhen |

B eigensicher, wenn V0 ≥ 2.9 cm³ oder Exzentrizität ≤ 0.34 mm (B). A: Amplitude elektronisch begrenzt (Strombegrenzung) – Xmax allein ergibt dicht 14.2 kPa → eigensicher nur mit mechanischem Hubanschlag (s. Sicherheit).

C: Eine Mikromembranpumpe (Typ 370, G) erreicht 40–80 kPa Überdruck bzw. −40 kPa Unterdruck → **nicht eigensicher**, Überdruck-/Unterdruckventil und Drucksensor zwingend.

## 3. Druckamplitude mit Leck (S)

Leckblende A_L bildet die unvollständige Abdichtung an der Düse nach (Prüfkammer im Demonstrator). Werte: eingeschwungen, Spitze positiv / negativ in kPa.

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

Lesart: Mit dichter Kammer ist der Druck frequenzunabhängig (reiner Volumeneffekt). Je grösser das Leck, desto stärker fällt die Amplitude bei tiefen Frequenzen ab (Luft entweicht innerhalb einer Periode). Für ein Leck Ø2 mm braucht man bei 30 Hz ein Vielfaches des Hubvolumens → **Abdichtung/Düsengeometrie ist die wichtigste Einflussgrösse**, nicht die Antriebskraft. Nichtlinear: Unterdruckspitzen etwas grösser als Überdruckspitzen.

## 4. Kräfte, Leistung, Antrieb (B/G)

| Grösse | A Voice-Coil | B Exzenter | C Pumpe + Ventile |
|---|---|---|---|
| Kraft auf Verdränger bei 2 kPa | 1.60 N (B) | 0.41 N (B) | – |
| Antriebsmoment / Strom | Bl ≈ 1.5 T·m (G) → I ≈ 1.1 A Spitze | M = F·e = 0.21 mN·m (B) | Pumpe 3–6 V, 0.2–0.4 A (G) |
| Pneumatische Leistung (dicht, Blindleistung) | ≈ 0 W | ≈ 0 W | – |
| Pneumatische Wirkleistung Leck Ø1 mm, ±2 kPa (obere Schranke p·Q_peak/2) | ≈ 0.03 W (B) | gleich | Pumpe muss Leckstrom nachliefern |
| Elektrische Leistung | 2.3–4.6 W bei 2 kPa dicht (B aus G: Bl, Re 4–8 Ω); Ø28-Treiber ≈ ¼ | 0.5–1.5 W (G, Motor 130/N20 ohne Getriebe) | 2–4 W (G, Pumpe + 2 Ventile) |
| Drehzahl / Frequenz | direkt 1–200 Hz (Verstärker) | f = n/60 → 300–9000 min⁻¹ für 5–150 Hz | Ventile 5–30 Hz (Schaltzeit 5–15 ms, G) |

## 5. Geräusch (G – nur Grössenordnung, Messung nötig)

Tieffrequente Druckschwankungen (5–150 Hz) sind wenig hörbar (A-Bewertung −70…−17 dB). Hörbar sind vor allem: Gehäuse-/Lagergeräusche und Harmonische (B: Motorbürsten ~kHz, Unwucht; C: Pumpe + Ventilklicken; A: Oberwellen und Gehäuseresonanzen). Ziel Demonstrator: < 50 dB(A) in 30 cm – Messung mit Klasse-2-Messgerät (A0-11).

