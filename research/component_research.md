# Komponentenrecherche – Rahmen (Phase 0)

> **Status: Recherche-Plan.** Es sind bewusst **keine** Produkte, Preise oder Leistungsdaten eingetragen,
> die noch nicht an Datenblättern oder unabhängigen Messungen geprüft wurden. Ausgefüllt wird in Phase 1/6/7.

## Bewertungsregeln

1. Herstellerdatenblatt vorhanden und archiviert (Link + Abrufdatum)
2. Wenn möglich unabhängige Messung (Prüfstandsdaten, Tests Dritter) – Herstellerangaben aus dem RC-Bereich sind oft Spitzenwerte
3. Lieferbar in CH/EU, zweite Bezugsquelle vorhanden
4. Ersatzteile verfügbar

## Komponentenklassen und Kriterien

### Hubgebläse (Schlüsselkomponente)
Bedarf (berechnet, unbestätigt): ≈ 1.3–1.6 kPa bei ≈ 0.06–0.31 m³/s.
Zu vergleichende Klassen:
- **Akku-Laubbläser aus Werkzeug-Akkusystemen** – Radial- oder Axialgebläse mit fertigem Akku, BMS und Ladegerät. Potenziell günstig und sicherheitstechnisch geprüft; Kennlinie meist nicht veröffentlicht → messen.
- **Axialventilator mit Propeller im Ringkanal** (klassisches Hovercraft-Hubgebläse)
- **RC-Impeller (EDF) 90–120 mm** – hohe Drehzahl, laut, Kennlinie für Statikdruck oft unbekannt
- **DC-Radialgebläse 24/48 V aus der Industrie** – robust, Kennlinien verfügbar, eventuell schwer/teuer

Kriterien: p-Q-Kennlinie im Betriebspunkt, Wirkungsgrad, Masse, Lärm, Preis, Fingerschutz-Möglichkeit.

### Vortrieb
Ummantelte Propeller Ø 200–300 mm mit BLDC-Außenläufer, reversierbar (Bremsen). Statischer Schub je Antrieb ≥ 29 N (Rechnung). Alternative: Impeller.

### Energiespeicher
- Werkzeug-Akkupacks (geprüft, BMS integriert, austauschbar) – Leistungsgrenze je Pack prüfen
- LiPo-Packs aus dem RC-Bereich – hohe Leistung, aber ohne BMS → Brand-Risiko, nur mit Zusatzschutz
- Li-Ion-Pack 18650/21700 mit BMS (selbst konfektioniert oder fertig) – Fertigungsrisiko
Bedarf: 120–350 Wh, Dauerleistung ≈ 1–1.5 kW, Spitze ≈ 2.5 kW (Rechnung).

### Leistungselektronik
ESCs mit Telemetrie (Strom, Temperatur, Drehzahl) und Reversierung, z. B. Open-Source-Firmware-Ökosystem (AM32/BLHeli-Klasse – Eignung prüfen). Hauptschalter, Not-Aus-Schütz/Relais, Sicherungen, Vorladung.

### Steuerung und Sensorik
- Mikrocontroller oder Flight-Controller (ESP32-/STM32-Klasse); Eignung offener Firmware (z. B. ArduPilot Rover für Differenzschub) **unverifiziert**
- IMU (6-Achs), Höhensensoren (ToF oder Ultraschall, 4 Ecken), Druckaufnehmer im Plenum
- Funkstrecke mit Failsafe, Totmann-Sender für Aufsichtsperson

### Struktur und Schürze
- Birkensperrholz, Pappelsperrholz, Sandwich (XPS/PU-Schaum + Deckschicht) – Kennwerte aus Datenblättern
- Schürzenmaterial: PVC- oder PU-beschichtetes Gewebe, Nylon-Ripstop – Abrieb- und Reissfestigkeit prüfen
- Druckteile: PETG, ASA, PA-CF – nur für nicht primär tragende Teile ohne Festigkeitsnachweis
