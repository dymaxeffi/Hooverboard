# Prototyp A – Schritt 3a: Mechanik- und Pneumatik-Konzept, Einkaufsliste

Stand 2026-11-13. Die CAD-Konstruktion (Schritt 3b) folgt, sobald der Tang Band W1-2121S da ist. Vorher müssen seine Masse und die Frage „Staubkappe oder Phasenstöpsel?“ geklärt sein. Nachweisstufen wie im Konzept: B berechnet, G geschätzt, E gemessen.

## 1. Aufbau

```
 Rückgehäuse          Lautsprecher          Luftraum        Membran     Druckkammer        Prüfadapter
 (Lüftungsgitter) ─── W1-2121S ──Stössel──► (entlüftet!) ── Ø20/12 ───  V0 ≈ 1,5 cm³ ─Düse─► ≤ 1 cm³
                                                                          │  │  │           (Leckeinsätze,
                                                                          │  │  └─ Kugelventile S1b (Über-/Unterdruck)
                                                                          │  └──── Dosiernadel 27G = Entlüftung S2
                                                                          └─────── Sensoranschluss → MPXV7007DP
```

| Element | Ausführung | Warum |
|---|---|---|
| **Lautsprecher** | Tang Band W1-2121S, Konus Richtung Membran, Korb in gedrucktem Gehäuse (PETG) geklemmt | Antrieb aus Schritt 1b |
| **Stössel** | gedruckt (PETG, 100 % Füllung, ≈ 0,3 g G). Koppelscheibe Ø12–15 mm auf die Staubkappe geklebt (2K-Epoxid). Bei Phasenstöpsel: Ringmitnehmer am Konus. Membranseitig M2-Mutterfalle | leicht, steif, kein Zusatzlager: Die Zentrierspinne des Lautsprechers führt den Stössel |
| **Luftraum Konus ↔ Membran** | **grossflächig zur Umgebung entlüftet** (Öffnungen ≥ Konusfläche, mit Fingerschutzgitter) | Sonst entsteht ein zweites, geschlossenes Luftpolster, das wie eine Feder gegen den Antrieb arbeitet |
| **Membran** | geplottete Silikonfolie 0,5 mm (Variante TPU 0,15 mm). Klemmdurchmesser 20 mm, Mittelplatte 12 mm, mechanisch geklemmt: zwei gedruckte Scheiben + M2-Schraube in den Stössel, **kein Kleben** | Silikon lässt sich kaum verkleben. Das Mittelloch (Plotter-Minimum 3 mm) wird von den Scheiben abgedichtet |
| **Membranklemmung** | zwei gedruckte Ringe, 4 × M2 oder M3, Membran als eigene Dichtung | definierte Einspannung = definierte wirksame Fläche (2,05 cm²) |
| **Druckkammer** | gedruckt, ≥ 4 Wände, 100 % Füllung um die Kammer, V0 ≈ 1,5 cm³. Düse Ø6 × 5 mm | kleines V0 = viel Druck pro Hub. Helmholtz-Resonanz ≈ 2 kHz, weit über dem Betrieb |
| **Sensoranschluss** | Schlauchtülle Ø3 an der Kammer, Silikonschlauch ID 3 mm, **so kurz wie möglich** (100 mm ≈ 0,7 cm³) | Schlauchvolumen addiert sich zu V0 und senkt den Druck |
| **Entlüftung S2** | stumpfe **Dosiernadel 27G × 1"** (ID 0,21 mm, L 25,4 mm) mit Luer-Lock in gedrucktem Luer-Sitz | τ = 0,14–0,18 s (B), Eckfrequenz ≈ 1 Hz. Gleichanteil 5 → 0,2 kPa in < 0,6 s, 5 Hz bleibt unbeeinflusst |
| **Überdruckventil S1b** | 2 × **Kugel-Gewichtsventil**: Stahlkugel Ø10 mm (4,11 g) auf senkrechtem, konischem Sitz Ø3,5 mm, eines für Über- und eines für Unterdruck | öffnet bei p = m·g/A = **4,2 kPa** (B), passiv, ohne Feder, Toleranz ±0,1 mm Sitz → ±6 %. Gerät muss aufrecht stehen |
| **Prüfadapter** | gedruckt, ≤ 1 cm³, auf die Düse gesteckt (O-Ring). Wechselbare Leckeinsätze: Messingplättchen 0,5 mm mit gebohrtem Loch Ø0,5 / 1,0 / 2,0 / 3,0 mm, dazu ein Blindstopfen | gebohrte Löcher sind genauer (±0,02 mm G) als gelaserte oder geplottete in dieser Grösse |

### Schutzstaffel Druck (B aus Datenblatt G)

| Stufe | Wirkt bei | Art |
|---|---|---|
| Vorwiderstand 18 Ω an 5 V | max. 3,6 kPa im Dichtfall | passiv, elektrisch |
| Fensterkomparator LM393 | 4,0 kPa | Hardware, ohne Software |
| Kugelventile S1b | 4,2 kPa (statisch) | passiv, pneumatisch |
| **Projektgrenze** | **5,0 kPa** | – |

Die Kugelventile sichern vor allem langsame bzw. statische Fehler ab (Erwärmung, Gleichanteil). Schnelle Druckspitzen begrenzt der Vorwiderstand.

## 2. Einkaufsliste Mechanik und Pneumatik

Preise geschätzt (G). Filament (PETG) wird als vorhanden angenommen.

| # | Teil | Spezifikation | Menge | CHF (G) | Zweck |
|---|---|---|---|---|---|
| M1 | **Silikonfolie** | 0,5 mm, Shore A 40–60, ca. A4 | 1 | 8–15 | Membran (Plottertest: max. Dicke 0,5 mm) |
| M2 | TPU-Folie (Alternative) | 0,1–0,2 mm, ca. A4 | 1 | 8–12 | Vergleichsmembran |
| M3 | **Dosiernadeln stumpf, Luer-Lock** | Sortiment 14G–30G, Länge ½" und 1" (enthält **27G × 1"**) | 1 Set | 8–12 | Entlüftung S2, Reserve |
| M4 | Luer-Lock-Adapter | Luer-Lock weiblich ↔ Schlauchtülle 3 mm, Set | 1 Set | 5–8 | Nadel und Schläuche anschliessen |
| M5 | **Stahlkugeln** | Wälzlagerkugeln Ø10 mm (G100, Chromstahl), zusätzlich Ø8 und Ø12 zum Feinabstimmen | je 10 | 5–8 | Kugelventile S1b |
| M6 | Messingblech | 0,5 mm, ca. 100 × 100 mm | 1 | 5–8 | Leckeinsätze |
| M7 | Mini-Spiralbohrer HSS | Satz 0,3–1,6 mm und 1,5–3,0 mm, mit Stiftenklöbchen (Handhalter) | 1 Set | 10–18 | Löcher in den Leckeinsätzen, Sitze nachbohren |
| M8 | Gewindeeinsätze zum Einschmelzen | M2 (20 Stk) und M3 (50 Stk), Messing | 1 Set | 8–12 | lösbare Verschraubung im Druck |
| M9 | Schraubensortiment Edelstahl | Zylinderkopf M2 und M3, 6–20 mm, mit Muttern und Scheiben | 1 | 10–15 | Klemmringe, Membran-Mittelplatte |
| M10 | O-Ringe Sortiment | NBR, Schnurstärke 1–1,5 mm, ID 3–20 mm | 1 | 6–10 | Prüfadapter, Düse |
| M11 | Klebstoffe | 2K-Epoxid 5 min, Sekundenkleber Gel | je 1 | 8–12 | Stössel auf Staubkappe |
| M12 | Kapton-Klebeband | 10–20 mm | 1 | 4–6 | NTC am Magnet |
| M13 | Einwegspritzen Luer | 10 ml und 20 ml | je 2 | 2–3 | Komparator- und Ventilprüfung |
| M14 | Schlauch-T-Stücke | für Schlauch ID 3 mm, Kunststoff | 5 | 3–5 | Sensor und Kontroll-U-Rohr parallel |
| M15 | PU-Schlauch transparent | 6 × 8 mm, 1 m | 1 | 3–5 | U-Rohr-Manometer zur Kalibrierung (408 mm Wassersäule = 4 kPa) |

**Summe Mechanik/Pneumatik: ≈ CHF 95–145** (Sortimente bleiben grösstenteils übrig.)

**Gesamtbestellung Prototyp A:**

| Teil | CHF (G) |
|---|---|
| Antrieb (W1-2121S, Vorwiderstände) | ≈ 25–40 |
| Elektronik (Pflicht) | ≈ 70–105 |
| Mechanik/Pneumatik | ≈ 95–145 |
| **Summe** | **≈ CHF 190–290** |

Wer M7 (Bohrer), M9 (Schrauben) oder M10 (O-Ringe) schon hat, spart ≈ CHF 30–40.

## 3. Nach Eintreffen (Vorbereitung Schritt 3b)

1. **Tang Band ausmessen:**
   - Korbdurchmesser, Bautiefe, Lage und Abstand der Befestigungslöcher
   - Durchmesser und Höhe der Staubkappe bzw. des Phasenstöpsels
   - Ein Foto von vorne und von der Seite hilft.
2. **Bl und Federsteifigkeit** mit dem Münz-Nullabgleich messen (Schritt 1) → endgültiger Vorwiderstand.
3. **Silikonfolie:** Dicke an 4 Stellen messen. Danach plotte ich das Plotter-Testmuster (Schneiddruck, Mindestlochgrösse).
4. **Stahlkugeln** wiegen (Küchenwaage, 10 Stück auf einmal → Mittelwert). Daraus folgt der exakte Sitzdurchmesser für 4,2 kPa.
5. **Dosiernadel 27G:** Innendurchmesser laut Packung notieren (Hersteller variieren 0,20–0,21 mm).

Danach konstruiere ich in Schritt 3b alle Druck-, Laser- und Plotterteile passend zu den gemessenen Werten.
