# Abnahmekriterien – Entwurf v0.1

Das Projekt gilt erst als **funktionsfähig**, wenn die Kriterien unten durch reproduzierbare Tests (mindestens 3 Wiederholungen, dokumentierte Messmittel) nachgewiesen sind. Rechnungen und Simulationen genügen nicht.

Nachweisstufe je Eigenschaft: **B** = berechnet · **S** = simuliert · **E** = experimentell bestätigt. Aktuell ist **keine** Eigenschaft auf Stufe E.

## Freigabe-Tore (Gates)

| Gate | Nach | Kriterium | Freigabe durch |
|---|---|---|---|
| G0 | Phase 0 | Anforderungen, Plan und Risiken vom Auftraggeber freigegeben | Auftraggeber |
| G1 | Phase 1 | Konzeptentscheid mit Berechnung **und** Messdaten aus Prototyp A0 | Auftraggeber |
| G2 | Phase 2 | Massen-/Leistungsbudget schliesst mit ≥ 20 % Reserve | Lead Systems |
| G3 | Phase 3 | Modelle an A0-Daten kalibriert, Abweichung dokumentiert | Test & Aero |
| G4 | Phase 4 | CAD kollisionsfrei, montierbar, Masse aus CAD ≤ Budget | CAD & Mechanik |
| G5–G7 | Phasen 5–7 | Fertigungs-, Elektronik- und BOM-Freigaben | jeweilige Disziplin |
| G8-B | Prototyp B | Skalenmodell schwebt und lenkt ferngesteuert | Test |
| G8-C | Prototyp C | Zielgrösse unbemannt mit Ballast: Kriterien AC-01…AC-08 erfüllt | Test & Sicherheit |
| G8-D | Prototyp D | Integriertes System, alle Fehlerfälle getestet | Test & Sicherheit |
| G9 | Sicherheit | Unabhängige Prüfung durch **reale** Fachperson, rechtliche Klärung | extern |

Ein bemannter Versuch ist **kein** Gate dieses Plans. Er wird erst nach G9 separat beantragt.

## Funktionale Kriterien (Prototyp C/D, unbemannt, Ballast = Nennlast)

| ID | Kriterium | Messmittel | Grenzwert (Vorschlag) |
|---|---|---|---|
| AC-01 | Schweben mit zentrischer Nennlast | Höhenmessung 4 Ecken | 20–50 mm (nach Definition OQ-01), Neigung ≤ 5° |
| AC-02 | Schweben mit Lastversatz ±50 mm quer, ±100 mm längs | Neigungsmesser | kein Schürzen-Aufsetzen, Neigung ≤ 8° |
| AC-03 | Leistungsaufnahme im Schweben | Leistungsmessung DC | ≤ SR-P-03 |
| AC-04 | Beschleunigung, Höchstgeschwindigkeit | Video/Odometrie | ≤ 2.0 m/s, nie überschritten |
| AC-05 | Bremsweg aus 2 m/s | Markierungen | Vorschlag ≤ 2 m |
| AC-06 | Not-Aus: Zeit bis Antriebe stromlos | Oszilloskop/Logger | ≤ 0.1 s (Vorschlag) |
| AC-07 | Funkverlust → sicherer Zustand | Logger | ≤ 0.5 s |
| AC-08 | Betriebsdauer bis Unterspannungsabschaltung | Logger | ≥ SR-F-07 |
| AC-09 | Temperaturen Motor/ESC/Akku nach Dauerlauf | Thermoelemente | unter Herstellergrenzen mit 15 K Abstand |
| AC-10 | Schalldruckpegel | Schallpegelmesser Kl. 2 | Grenzwert nach OQ-07 |
