# Systemanforderungen – HOVERBOARD MINI

Stand: Phase 0, Entwurf v0.1 – **noch nicht freigegeben**.
Änderungen an freigegebenen Anforderungen nur über das Decision Log (`documentation/decision_log.md`).

Status-Legende: **REQ** = Vorgabe Auftraggeber · **ABG** = vom Team abgeleitet/vorgeschlagen (Freigabe nötig) · **OFFEN** = Wert fehlt

## 1. Funktion

| ID | Anforderung | Wert | Status | Nachweis |
|---|---|---|---|---|
| SR-F-01 | Board trägt einen Piloten schwebend | 30 kg, 1.30 m | REQ | Test D (nur Ballast) |
| SR-F-02 | Schwebehöhe | 20–50 mm – **Definition offen (OQ-01)**. Vorschlag: Abstand Unterkante starre Struktur ↔ Boden | REQ / OFFEN | Messung |
| SR-F-03 | Kontrolliertes, stabiles Schweben im Stand | Neigung ≤ 5° bei Nennlast zentrisch (ABG) | ABG | Test C |
| SR-F-04 | Vorwärtsfahrt | Höchstgeschwindigkeit software-begrenzt, Vorschlag ≤ 2.0 m/s (OQ-03) | ABG | Test C/D |
| SR-F-05 | Bremsen | Aktiv (Gegenschub) **und** passiv (Kissen ablassen → Schürzenreibung) | ABG | Test C/D |
| SR-F-06 | Richtungswechsel | Gier-Steuerung durch Differenzschub; Gewichtsverlagerung allein ist **nicht** zulässig als Steuerung | REQ/ABG | Test C/D |
| SR-F-07 | Betriebsdauer | Vorschlag ≥ 10 min (OQ-04) | OFFEN | Test D |
| SR-F-08 | Untergrund | Vorschlag Gen. 1: glatter Hallenboden; weitere Böden nur nach Messung (OQ-02) | OFFEN | Test A0/C |
| SR-F-09 | Steigfähigkeit | Vorschlag ≤ 2° Rampe | ABG | Test C |

## 2. Physik und Leistung

| ID | Anforderung | Wert | Status |
|---|---|---|---|
| SR-P-01 | Auslegungsgewicht Gebläse | 1.25 × (Pilot + Board) | ABG |
| SR-P-02 | Eigengewicht Board | Ziel ≤ 12.5 kg, Grenze 18 kg (Massenbudget) | ABG |
| SR-P-03 | Elektrische Dauerleistung | Ziel ≤ 1.5 kW (aus Phase-0-Abschätzung, unbestätigt) | ABG |
| SR-P-04 | Schub-Reserve Vortrieb | ≥ 58 N gesamt (Phase-0-Rechnung) | ABG |

## 3. Abmessungen und Ergonomie

| ID | Anforderung | Wert | Status |
|---|---|---|---|
| SR-E-01 | Länge × Breite | 700–850 × 400–550 mm vorläufig; Optimierung in Phase 1 (Zielkonflikt Z-01) | REQ (vorläufig) |
| SR-E-02 | Standfläche | Seitliche Schrittstellung, Fussabstand ≥ Schulterbreite des Piloten; rutschfeste Trittflächen | ABG |
| SR-E-03 | Auf-/Absteigen | Nur im abgesenkten Zustand (Kissen aus) möglich und vorgesehen | ABG |
| SR-E-04 | Bedienung | Handsteuerung des Piloten **plus** übergeordneter Not-Aus/Totmann einer Aufsichtsperson (OQ-09) | ABG |

## 4. Sicherheit (Auszug, Details in `safety/`)

| ID | Anforderung | Status |
|---|---|---|
| SR-S-01 | Kein Zugriff auf rotierende Teile (Fingerschutz an allen Ein- und Auslässen) | ABG |
| SR-S-02 | Sicherer Zustand = alle Antriebe aus → Board setzt aus ≤ 50 mm Höhe ab und bremst durch Reibung | ABG |
| SR-S-03 | Not-Aus wirkt hardwareseitig (Leistungstrennung), unabhängig von Software | ABG |
| SR-S-04 | Funkverlust → sicherer Zustand innerhalb ≤ 0.5 s (Wert in Phase 6 bestätigen) | ABG |
| SR-S-05 | Akku mit BMS, Überstrom-, Unterspannungs-, Übertemperaturschutz; Sicherung am Pack | ABG |
| SR-S-06 | Nennspannung im Schutzkleinspannungsbereich, Vorschlag ≤ 48 V DC (Grenzwert zu verifizieren) | ABG |
| SR-S-07 | Struktur übersteht Missbrauch: 100 kg Person statisch auf dem Deck ohne Bruch (nicht schwebend) | ABG |
| SR-S-08 | Dynamischer Lastfaktor Sprung/Aufsteigen: Struktur auf 3 × Pilotengewicht + Sicherheitsfaktor auslegen | ABG |
| SR-S-09 | Kein bemannter Test ohne unabhängige Sicherheitsprüfung durch reale Fachpersonen | REQ |

## 5. Fertigung, Kosten, Wartung

| ID | Anforderung | Status |
|---|---|---|
| SR-M-01 | Möglichst viele Teile mit Bambu Lab H2S (Druck 340 × 320 × 340 mm, 10-W-Diodenlaser) | REQ |
| SR-M-02 | Primär tragende Teile nur aus Werkstoffen mit belastbaren Kennwerten (kein ungeprüftes FDM) | REQ |
| SR-M-03 | Modular: Gebläse, Antriebe, Akku, Elektronik werkzeugarm tauschbar | REQ |
| SR-M-04 | Handelsübliche Komponenten, Lieferbarkeit CH/EU | REQ |
| SR-M-05 | Budget-Obergrenze | OFFEN (OQ-05) |
| SR-M-06 | Keine kostenpflichtige Software, sofern Alternativen existieren (Python, CadQuery, FreeCAD, KiCad) | REQ |

## 6. Lärm

| ID | Anforderung | Status |
|---|---|---|
| SR-N-01 | Schalldruckpegel am Ohr des Piloten und in 1 m Abstand messen; Grenzwert festlegen (OQ-07) | OFFEN |
