# Sicherheit – Vorläufige Gefahrenliste (Phase 0)

Die vollständige Gefahrenanalyse (FMEA, Fehlerbaum) folgt in Phase 9 und läuft ab Phase 1 mit.
**Die simulierten Teamrollen ersetzen keine unabhängige Prüfung durch reale Fachpersonen.**

## 1. Grundsatz

Sicherer Zustand: **alle Antriebe stromlos → Board setzt aus ≤ 5 cm auf und wird durch Schürzenreibung gebremst.** Das ist der wichtigste Sicherheitsvorteil des Luftkissens gegenüber freiem Flug und muss in jeder Konstruktionsentscheidung erhalten bleiben.

## 2. Gefährdungen (erste Liste)

| ID | Gefährdung | Ursache (Beispiele) | Erste Schutzidee |
|---|---|---|---|
| H-01 | Auftriebsverlust | Gebläse-, Akku-, Schürzenausfall | unkritisch aus ≤ 5 cm, aber Sturz des Piloten bei Fahrt möglich → Geschwindigkeitsbegrenzung |
| H-02 | Kippen, Sturz | Schwerpunktverlagerung, einseitiges Aufsetzen, Hindernis | Kammerung, niedriger Schwerpunkt, max. 2 m/s, Schutzausrüstung |
| H-03 | Rotierende Teile | Finger, Haare, Kleidung, Fremdkörper | geschlossene Gitter an allen Ein-/Auslässen (Fingerprobe), Ummantelung |
| H-04 | Bruch von Propeller/Impeller | Fremdkörper, Ermüdung, Überdrehzahl | Ummantelung als Splitterschutz, Drehzahlbegrenzung |
| H-05 | Mechanisches Strukturversagen | Sprung, Missbrauch, Ermüdung FDM | Auslegung SR-S-07/08, nur geprüfte Werkstoffe tragend |
| H-06 | Akkubrand | Kurzschluss, Beschädigung, Überladung | BMS, Sicherung, Schutzgehäuse, Laden auf nicht brennbarer Unterlage unter Aufsicht |
| H-07 | Elektrischer Fehler | Kabelbruch, Wackelkontakt, Kurzschluss | Zugentlastung, verpolsichere Stecker, Sicherungen |
| H-08 | Software-/Sensorfehler | falscher Höhen-/Lagewert, Absturz Firmware | Watchdog, Plausibilitätsprüfung, Hardware-Not-Aus |
| H-09 | Unerwartete Beschleunigung | Steuerfehler, Funkstörung | Rampenbegrenzung, Totmann, Failsafe |
| H-10 | Kollision | Board gleitet weiter, keine Reibung | Bremsen per Absetzen, abgesperrter Testbereich, Stossfänger |
| H-11 | Auf- und Absteigen | Board bewegt sich unter dem Fuss | Antriebe nur bei Bestätigung + Pilot steht; Aufsteigen nur abgesenkt |
| H-12 | Lärm | Gebläse | Messung, Gehörschutz |
| H-13 | Geschleuderte Partikel | Ausströmende Kissenluft | Augenschutz, sauberer Boden |

## 3. Rechtliche Themen Schweiz (zu prüfen – keine Rechtsberatung)

Folgende Erlasse **könnten** relevant sein. Einordnung muss durch eine Fachperson/Fachstelle erfolgen:

- Produktsicherheitsgesetz (PrSG, SR 930.11) – Inverkehrbringen
- Spielzeugverordnung (VSS, SR 817.023.11) – falls als Spielzeug für Kinder eingestuft
- Maschinenverordnung (MaschV, SR 819.14) bzw. EU-Maschinenrecht
- Produktehaftpflichtgesetz (PrHG, SR 221.112.944), Obligationenrecht – Haftung
- Strassenverkehrsrecht (SVG, VRV, VTS) – Einordnung als „fahrzeugähnliches Gerät“ und Benutzung auf öffentlichem Grund
- Luftfahrtrecht (BAZL) – vermutlich nicht anwendbar auf ein Luftkissenfahrzeug, abklären
- Elektro: Niederspannungs-Installationsverordnung, EMV-Verordnung (VEMV), Akku-Transport (UN 38.3) und Entsorgung
- Gehörschutz/Lärm: Vorgaben Suva

SR-Nummern vor Verwendung an fedlex.admin.ch prüfen.

## 4. Offene Sicherheitsnachweise

Alle. Es liegt noch kein einziger Sicherheitsnachweis vor.
