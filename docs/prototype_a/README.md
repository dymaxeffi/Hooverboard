# Prototyp A – Voice-Coil-Druckwellen-Demonstrator

Grundlage: `docs/pressure_actuator_concepts.md` (Konzept A, Bedingungen in Abschnitt 11, Sicherheitsanforderungen S1–S13). Nur Funktionsdemonstrator gegen einen Prüfadapter, keine Anwendung am Menschen.

## Schritte

| Schritt | Inhalt | Status |
|---|---|---|
| **1** | **Lautsprecher aus dem Bestand auswählen** (Bl und Federsteifigkeit messen, Bauform wählen) → [01_lautsprecherauswahl.md](01_lautsprecherauswahl.md) | **in Arbeit, Messung durch dich** |
| 1b | Kaufempfehlung Antrieb (kompakt: Dayton CE32A-4 / Tang Band W1-2121S + Vorwiderstände) → [02_kaufempfehlung_antrieb.md](02_kaufempfehlung_antrieb.md) | **bereit zur Bestellung** |
| 2 | Elektronik und Einkaufsliste: Verstärker, Mikrocontroller, analoger Drucksensor, DC-Schutz, 5-V-Netzteil | offen |
| 3 | Konstruktion: Stössel, Membran (Plotter), Kammer, Düse, Prüfadapter ≤ 1 cm³, Leckblenden (Laser), Überdruckventil S1b | offen |
| 4 | Firmware: Signalgenerator (Frequenz, Amplitude, Kurvenform), Druckmessung, Abbruch bei 4 kPa | offen |
| 5 | Inbetriebnahme und Sicherheitsnachweise (S1 mit Blindstopfen, Fehlerinjektion) | offen |
| 6 | Messreihe: Druck über Frequenz × Leck × Kurvenform → Festlegung des Frequenzbereichs | offen |

Frequenzbereich und Zielamplitude werden in Schritt 6 anhand der Messungen festgelegt.
