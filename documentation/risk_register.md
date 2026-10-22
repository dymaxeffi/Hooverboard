# Risiko- und Zielkonfliktregister – Phase 0

Bewertung: Wahrscheinlichkeit (W) und Auswirkung (A) je 1–5, Risikozahl = W × A. Vorläufig.

## 1. Widersprüche und Zielkonflikte in den Anforderungen

| ID | Konflikt | Erläuterung | Vorschlag |
|---|---|---|---|
| Z-01 | Kompakt ↔ Leistung, Lärm, Akkumasse | P ∝ p^1.5·U; 600 × 360 mm braucht ≈ 1.7 × die Leistung von 800 × 480 mm | Grösse erst nach A0-Messung festlegen; 800 × 500 mm als Start |
| Z-02 | „Schweben 2–5 cm“ ↔ effizientes Luftkissen | Mit Schürze ist der Luftspalt mm-gross; 2–5 cm *freier* Spalt kostet 4–10 kW | Schwebehöhe als Bodenabstand der starren Struktur definieren (OQ-01) |
| Z-03 | Geringer Lärm ↔ hoher Kissendruck / kleine Gebläse | Höherer Druck verlangt höhere Blattspitzengeschwindigkeit | Grössere, langsamere Gebläse; Messung |
| Z-04 | Grosse Propeller (effizient) ↔ Sicherheit, Kompaktheit | Ø 300 mm statt 200 mm spart ≈ 0.7 kW Spitze, aber mehr Gefährdung | Ummantelung + Gitter zwingend |
| Z-05 | Steuerung durch Gewichtsverlagerung ↔ Kontrollierbarkeit | Kein Bodenkontakt → keine Lenkkräfte aus Gewichtsverlagerung | Differenzschub, Schwerpunkt nur als Störgrösse |
| Z-06 | Bremsen ↔ reibungsfreies Schweben | Bremsen braucht Gegenschub oder Absetzen | Beides vorsehen; Absetzen = sicherer Zustand |
| Z-07 | H2S als Hauptfertigung ↔ Board 800 × 500 mm | Druckraum 340 × 320 × 340 mm; 10-W-Diodenlaser schneidet nur dünnes Holz (Herstellerdaten verifizieren) | Deck aus Sperrholz extern/zuschneiden oder segmentiert; H2S für Halter, Kanäle, Gitter, Gehäuse |
| Z-08 | Niedrige Kosten ↔ Sicherheit | BMS, Qualitätszellen, Not-Aus-Hardware kosten | Sicherheit wird nicht gekürzt (REQ) |
| Z-09 | Leicht ↔ robust | Kind springt auf → dynamische Last; Missbrauch durch Erwachsene | SR-S-07/08 |
| Z-10 | „Real flugfähig“ ↔ Physik | Freier Flug braucht 23–75 kW | Projekt als Luftkissenfahrzeug führen (D-002) |
| Z-11 | Pilot ist ein Kind (30 kg, 1.30 m) | Höchste Sorgfaltspflicht, Spielzeug-/Produktrecht kann greifen | Nur Ballast-Tests; externe Prüfung vor jedem bemannten Einsatz |

## 2. Technische Risiken

| ID | Risiko | W | A | RZ | Massnahme |
|---|---|---:|---:|---:|---|
| R-01 | Effektiver Leckspalt deutlich > 3 mm (Leistung ≥ 1.5 kW) | 3 | 4 | 12 | A0-Messung, Schürzenvarianten, grössere Fläche |
| R-02 | Gebläse erreicht 1.3–1.6 kPa nicht bei nötigem Volumenstrom | 3 | 5 | 15 | Kennlinie messen, bevor gekauft wird in Menge |
| R-03 | Kippen bei Schwerpunktverlagerung, Schürze setzt einseitig auf | 4 | 4 | 16 | Kammerung, breitere Basis, Kipp-Test A0 |
| R-04 | Schürzenschleppen viel höher als angenommen (Vortrieb unterdimensioniert) | 3 | 3 | 9 | Schleppkraft in A0 messen |
| R-05 | Board schwerer als 18 kg | 3 | 3 | 9 | Massenkontrolle aus CAD ab Phase 4 |
| R-06 | Akkubrand (LiPo, mechanische Beschädigung, Überlast) | 2 | 5 | 10 | BMS, Sicherung, geschützter Einbau, Laden nur unter Aufsicht |
| R-07 | Lärm > Grenzwert | 4 | 3 | 12 | Messung A0, Schalldämpfung, grössere Gebläse |
| R-08 | FDM-Teile versagen bei Vibration/Ermüdung | 3 | 4 | 12 | Nur Sekundärteile drucken; Ermüdungstest |
| R-09 | Fremdkörper werden angesaugt/geschleudert | 3 | 3 | 9 | Ansauggitter, Testboden sauber |
| R-10 | Funk-/Sensorfehler → unkontrollierte Beschleunigung | 2 | 5 | 10 | Watchdog, Failsafe, Totmann, Geschwindigkeitsbegrenzung |
| R-11 | Rechtslage verhindert Nutzung (öffentlicher Grund, Spielzeugrecht) | 3 | 3 | 9 | Frühe Klärung (Phase 1/9) |
| R-12 | H2S-Laser kann vorgesehene Materialien nicht schneiden | 3 | 2 | 6 | Offizielle Spezifikation prüfen, Probeschnitte |
| R-13 | Untergrund (Fugen, Teppich, Aussen) erhöht Leckage stark | 4 | 3 | 12 | Gen. 1 nur Hallenboden; Untergründe in A0 messen |
| R-14 | Kostenüberschreitung | 3 | 2 | 6 | 3 Kostenvarianten, Budget festlegen (OQ-05) |

Höchste Risiken: **R-03 Kippen**, **R-02 Gebläsekennlinie**, R-01/R-07/R-08/R-13.
