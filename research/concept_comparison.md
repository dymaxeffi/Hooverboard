# Methodischer Vergleich der Schwebeprinzipien – Phase 0

> **Status: VORLÄUFIG.** Die Bewertungen sind begründete Einschätzungen auf Basis der Phase-0-Berechnungen,
> keine Messergebnisse. Der endgültige Konzeptentscheid erfolgt in Phase 1 (Gate G1) mit Daten aus Prototyp A0.
> Quelle der Matrix: `calculations/hoverlib/decision.py` (gerechnet, nicht von Hand summiert).

## 1. Methode

1. **Ausschlusskriterien (K.O.)** zuerst – ein Konzept, das eine harte Anforderung nicht erfüllen kann, wird unabhängig von der Punktzahl verworfen:
   - elektrische Leistung > 5 kW (mit Akkus in Boardgrösse und vertretbaren Kosten/Risiken nicht darstellbar)
   - kein sicherer Zustand bei Antriebsausfall
   - Schwebehöhe 2–5 cm grundsätzlich nicht erreichbar
   - Funktion nur auf Spezialboden
2. **Gewichtete Bewertung** 1–5 je Kriterium, Score normiert auf 100.
3. **Sensitivitätsprüfung** (Phase 1): Ändert sich die Rangfolge, wenn ein Gewicht um ±5 Punkte verschoben wird? Wenn ja, ist der Entscheid nicht robust und braucht Messdaten.
4. Jede Bewertung wird in Phase 1 mit Zahl oder Messung begründet (Spalte „Begründung“ unten).

**„Erforderliche Auftriebskraft“** ist für alle Konzepte gleich (= Gewicht) und wird daher nicht gepunktet, sondern über die Schub-Reserve im K.O.-Kriterium berücksichtigt.
**Wirkungsgrad** und **Energiebedarf** korrelieren stark; Wirkungsgrad hat deshalb nur 5 % Gewicht, um Doppelzählung zu begrenzen.

## 2. Konzepte

| ID | Konzept | Kurzbeschreibung |
|---|---|---|
| K1 | Schürzen-Luftkissen, Single-Fan | Ein Gebläse speist Kissen; Teilstrom nach hinten für Vortrieb/Lenkung (Ruder). Klassischer Kleinhovercraft-Aufbau. |
| K2 | Luftkissen ohne Schürze | Starres Plenum oder Randstrahl (Peripheral Jet); Spalt = Schwebehöhe. |
| K3 | Mehrere Impeller mit Bodeneffekt | EDFs blasen direkt nach unten; Bodeneffekt reduziert Leistung leicht. |
| K4 | Aktiv geregelter Schub (freier Flug) | Multicopter-Prinzip, Lage über Schubregelung. |
| K5 | Hybrid: Luftkissen + separater Vortrieb | Hubgebläse nur für Kissen, zwei unabhängige Vortriebe für Schub, Bremsen, Gieren. |
| K5b | Hybrid mit Mehrkammer-Kissen | Wie K5, Kissen in Kammern geteilt, optional mit geregelten Kammerdrücken für Lagestabilität. |
| K6 | Luftlager (Air Caster) | Industrielle Technik, hoher Druck, Spalt < 1 mm. |
| K7 | Wirbelstrom-Magnetschweben | Rotierende Magnete über leitfähigem Metallboden. |

## 3. Vorläufige Entscheidungsmatrix

| Konzept | Sicherheit (20) | Energie (15) | Stabilität (10) | Steuerbarkeit (10) | Herstellbarkeit (10) | Kosten (10) | Wirkungsgrad (5) | Gewicht (5) | Geräusch (5) | Reparierbarkeit (5) | Untergrund (5) | **Score** | K.O. |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| K5 Hybrid | 4 | 4 | 3 | 4 | 4 | 4 | 4 | 3 | 3 | 4 | 3 | **75** | – |
| K1 Single-Fan | 4 | 4 | 4 | 3 | 2 | 4 | 5 | 4 | 3 | 4 | 3 | **73** | – |
| K5b Mehrkammer | 4 | 4 | 4 | 4 | 3 | 3 | 4 | 3 | 3 | 3 | 3 | **72** | – |
| K2 ohne Schürze | 3 | 1 | 2 | 3 | 3 | 2 | 1 | 2 | 1 | 3 | 3 | **45** | (4–10 kW, Grenzfall) |
| K6 Air Caster | 4 | 5 | 4 | 2 | 3 | 3 | 5 | 4 | 4 | 4 | 1 | 73 | Höhe nicht erreichbar |
| K7 Magnet | 3 | 2 | 3 | 2 | 1 | 1 | 2 | 2 | 4 | 2 | 1 | 43 | Spezialboden |
| K3 Impeller | 2 | 1 | 2 | 3 | 3 | 1 | 1 | 2 | 1 | 3 | 3 | 39 | ≈ 40 kW |
| K4 Freier Flug | 1 | 1 | 2 | 4 | 2 | 1 | 1 | 1 | 1 | 2 | 4 | 34 | 23–75 kW, Absturz |

## 4. Begründungen (Kurzfassung)

- **K1 vs. K5:** K1 ist leichter und effizienter (ein Motor), aber Lenken über Ruder funktioniert nur bei Fahrt, Bremsen braucht Schubumkehr, die ein Single-Fan nicht hat. Herstellbarkeit tiefer, weil der Luftstrom aufgeteilt werden muss (Abstimmung schwierig). K5 trennt Hub und Vortrieb → Gieren im Stand, aktives Bremsen, einfachere Regelung.
- **K5b:** Beste Stabilität bei Lastversatz eines Kindes; mehr Komplexität. Ergänzung zu K5, kein Ersatz.
- **K2:** Physikalisch möglich, aber Faktor ≈ 10 mehr Leistung, laut, wirbelt Staub auf. Kein K.O. im strengen Sinn bei 20 mm (≈ 4 kW), aber klar unterlegen.
- **K3/K4:** Leistungsbedarf um Grössenordnungen zu hoch (siehe `research/physical_feasibility.md`). Bei Ausfall kein sicherer Zustand (K4).
- **K6:** Hohe Punktzahl, aber Spalt < 1 mm verfehlt die Höhenanforderung und funktioniert nur auf sehr glatten, dichten Böden → verworfen. Nützlich als Referenz für Schürzen-Leckage-Messungen.
- **K7:** Bekanntes Prinzip, braucht leitfähigen Spezialboden → verworfen.

## 5. Vorläufige Empfehlung

**K5 (Schürzen-Luftkissen + separater, differenziell geregelter Vortrieb) als Basiskonzept, K5b (Kammerung) als Stabilitätsoption.**
K1 und K5 liegen nur 2 Punkte auseinander → der Entscheid ist **nicht robust**. Gate G1 entscheidet mit Messdaten zu Leckspalt, Gebläsekennlinie, Schürzenschleppen und Kippsteifigkeit.

## 6. In Phase 1 zu ergänzen

- Randstrahl-Modell für K2 (Literatur), um K2 fair zu bewerten
- Sensitivitätsanalyse der Gewichte
- Bewertung durch Messwerte statt Einschätzung
