# Modular Motion Lab – Phase 1: Druckwellen-Aktuator, Konzeptvergleich

Stand 2026-11-10 · Status: **Konzeptbewertung abgeschlossen (Entwurf zur Entscheidung)** · keine CAD-Konstruktion, keine Druckdateien.

**Nachweisstufen:** **B** = berechnet (Formel, nachvollziehbar) · **S** = simuliert (`calculations/pressure_actuator/model.py`) · **G** = geschätzt (Datenblatt-Grössenordnung, Erfahrungswert) · **E** = experimentell belegt. **Für diese Phase liegen keine E-Werte vor.** Alle Zahlen sind vor dem Bau des Demonstrators zu messen.

**Abgrenzung:** Diese Phase betrifft nur einen **technischen Funktionsdemonstrator**, der gegen eine Prüfkammer arbeitet. Er hat keine körperberührende Fläche und keine Anwendung am Menschen.

---

## 1. Ziel

Drei Funktionskonzepte für einen kompakten, elektrisch betriebenen Aktuator vergleichen. Der Aktuator erzeugt in einer kleinen Luftkammer periodische Über- und Unterdruckwellen. Ergebnis ist eine begründete Architektur für den ersten DIY-Prototyp, der mit dem Bambu Lab H2S (FDM), dem 10-W-Laser und dem Schneidplotter gebaut werden kann.

## 2. Recherche: öffentlich dokumentierte Druckwellen-Prinzipien

| Quelle | Dokumentiertes Prinzip | Relevanz |
|---|---|---|
| Patentfamilie Novoluto/Lenke (z. B. US 9,763,851; CA 2 978 739; US 12,329,710) – Grundlage der „Pleasure Air“-Technologie | Eine Antriebseinheit ändert das Volumen einer **ersten Kammer**. Diese ist über ein Verbindungselement mit einer **zweiten, zum Körper offenen Kammer** verbunden. Es entsteht ein Druckfeld aus **abwechselndem Über- und Unterdruck**, die Hohlraumwand ist flexibel. Spätere Fassungen enthalten Sensoren und Ergonomievarianten. | Kernprinzip: **Volumenverdrängung ohne Nettoströmung**. Die konkrete Kammer- und Gehäuseausführung ist geschützt und wird hier **nicht** nachgebaut. |
| Patent „Device for stimulating … variable pressure field“ (US-PDF 12576003) | Antrieb erzeugt in einer abgeschlossenen Kammer pneumatische Wechseldruckfelder von **≈ 0,5–150 Hz**, Druckdifferenz **≈ 20 mbar (2 kPa) oder mehr**, gemessen an der Gehäuseöffnung. | Plausible **Zielgrössen** für den Demonstrator (Designangaben, keine Messungen). |
| Patent „Methods for enhancing female orgasm“ (US-PDF 10646399) | Saugbetonte Variante: Überdruck ≈ 20–100 Pa, Unterdruck ≈ −1 bis −5 kPa. | Zeigt eine andere Architektur mit Gleichanteil (Dauersog). Für Konzept C relevant, aus Sicherheitssicht kritisch. |
| Medizinische Luftpuls-Generatoren (HFCWO, z. B. US 7,785,280; 7,121,808; 7,770,479) | Motor mit Nocken, Scotch-Yoke oder Kurbel bewegt Membranen in einer Kammer. Frequenz = Motordrehzahl, typ. **5–25 Hz**. „Kleineres Totvolumen → grösserer Druckpuls“. | Bewährte Mechanik für **Konzept B**, bestätigt den Totvolumen-Effekt (Abschnitt 4). |
| Produktbeschreibungen (Womanizer, Handel) | „Luftfenster öffnet und schliesst“, berührungsloses Druckwellenprinzip; neuere Geräte mit veränderter Innenströmung für langsamere Pulse. | Nur qualitativ, keine technischen Daten. |

**Unabhängige Messungen an Konsumgeräten wurden nicht gefunden.** Die Zielwerte unten sind deshalb Projektannahmen.

**Schutzrechte:** Das Grundprinzip (verdrängte erste Kammer, offene zweite Kammer, Wechseldruckfeld) ist durch die Novoluto-Patentfamilie beansprucht. Eine **private, nicht gewerbliche** Nutzung für einen Demonstrator ist nach Schweizer Recht (Art. 9 Abs. 1 lit. a PatG) in der Regel zulässig. Vor jeder Veröffentlichung von Bauanleitungen, vor Verkauf oder Weitergabe ist eine Freedom-to-operate-Prüfung durch eine Fachperson nötig. **Keine Rechtsberatung.**

## 3. Gemeinsame Randbedingungen (Projektannahmen)

| Grösse | Wert | Status |
|---|---|---|
| Druckamplitude Ziel | ±2 kPa (±20 mbar) in der Prüfkammer | Annahme, angelehnt an die Patentangabe |
| Frequenzbereich | 5–150 Hz | Annahme (Patent 0,5–150 Hz) |
| **Harte Druckgrenze** | **\|p\| ≤ 5 kPa** in jedem Fehlerfall | Projektgrenze für den Demonstrator. **Kein validierter physiologischer Grenzwert** – vor jeder späteren Anwendung durch Fachpersonen festzulegen |
| Gleichanteil (Dauersog/-druck) | ≤ 0,2 kPa nach 1 s (Entlüftung) | Annahme: Wechseldruck, kein Vakuum aufbauen |
| Totvolumen V0 | 1–4 cm³ | Konstruktionsziel kompakt |
| Versorgung | extern, SELV ≤ 12 V DC, strombegrenzt | Pflicht |
| Prüfling | Prüfkammer mit wechselbaren Leckblenden statt Körperkontakt | Pflicht |

## 4. Physikalische Grundlagen (Ergebnisse siehe `calculations/pressure_actuator/results.md`)

**Druck aus Volumenänderung (B):** Bei dichter Kammer und adiabatischer Verdichtung gilt

  p ≈ γ · p0 · ΔV / V0  (γ = 1,4, p0 = 101,3 kPa)

| V0 | ΔV für ±2 kPa | ΔV für ±5 kPa |
|---|---|---|
| 1 cm³ | 14 mm³ | 35 mm³ |
| 2 cm³ | 28 mm³ | 70 mm³ |
| 4 cm³ | 56 mm³ | 141 mm³ |

Die benötigten Hubvolumen sind **sehr klein**: 28 mm³ entsprechen einer Membran Ø20 mm mit nur ≈ 0,14 mm Hub. Bei realer Wärmeübertragung (Exponent 1,0–1,4) fällt der Druck bis ≈ 30 % tiefer aus (G).

**Helmholtz-Resonanz (B):** Kammer 2 cm³ mit Düse Ø6 × 5 mm → f_H ≈ 2 kHz. Der Betrieb bei 5–150 Hz liegt weit darunter. Die Kammer verhält sich quasistatisch, eine Resonanzüberhöhung tritt nicht auf. Diese Resonanz wird erst bei langen, dünnen Kanälen oder grossen Volumen wichtig.

**Leck dominiert (S):** Die unvollständige Abdichtung an der Düse ist die wichtigste Einflussgrösse. Simulation Konzept B (ΔV = 103 mm³, V0 = 2 cm³), Spitzenwerte in kPa:

| f | dicht | Leck Ø0,5 | Leck Ø1 | Leck Ø2 |
|---|---|---|---|---|
| 10 Hz | ±7,3 | ±1,5 | ±0,1 | ±0,01 |
| 30 Hz | ±7,3 | ±5,4 | ±0,9 | ±0,06 |
| 100 Hz | ±7,3 | ±7,1 | ±4,8 | ±0,6 |
| 150 Hz | ±7,3 | ±7,2 | ±6,0 | ±1,3 |

Folgerungen:
1. Bei dichter Kammer ist die Druckamplitude **frequenzunabhängig** und nur durch das Hubvolumen bestimmt. Daraus folgt die Möglichkeit, ein Konzept **eigensicher** auszulegen (Abschnitt 7).
2. Mit Leck fällt die Amplitude bei tiefen Frequenzen stark ab (Luft entweicht innerhalb einer Periode). Für tiefe Frequenzen mit Leck braucht man viel mehr Hubvolumen. Das spricht für Konzepte mit **grossem, einstellbarem Hub**. Gleichzeitig wird der Dichtfall dadurch gefährlicher.
3. Die eingespeiste Wirkleistung ist klein (≈ 0,03 W bei Leck Ø1 mm, B). Der elektrische Bedarf wird durch die Wandlerverluste bestimmt, nicht durch die Pneumatik.

---

## 5. Konzepte

### Konzept A – Elektromagnetische Membran (Voice-Coil)

![Konzept A](img/konzept_a_voicecoil.svg)

**Prinzip:** Ein Kleinlautsprecher (Ø28–40 mm, Schwingspule im Magnetfeld) dient als Kolben. Die Membranvorderseite bildet mit der Düse die Druckkammer V0. Die Rückseite ist geschlossen (Rückvolumen), damit kein Schall nach hinten abstrahlt. Ein Klasse-D-Verstärker, angesteuert von einem Mikrocontroller, gibt Frequenz, Amplitude und Kurvenform frei vor.

**Solenoid-Variante:** Ein Hubmagnet (Zugmagnet + Feder) wurde geprüft und **verworfen**. Er arbeitet nur in zwei Lagen (Ein/Aus), erzeugt harte Anschlagklicks und Oberwellen, braucht hohe Halteströme und lässt sich in der Amplitude kaum regeln.

| Merkmal | Wert | Stufe |
|---|---|---|
| Wirksame Fläche Sd | 3,5 cm² (Ø28) … 8 cm² (Ø40) | G |
| Lineare Auslenkung Xmax | ±0,3–1 mm | G |
| ΔV max (Ø40, Xmax 0,5 mm) | 400 mm³ – weit mehr als nötig | B |
| Hub für ±2 kPa (dicht, V0 4 cm³) | 0,07 mm | B |
| Kraft bei 2 kPa | 1,6 N (Ø40) bzw. 0,7 N (Ø28) | B |
| Strom bei 2 kPa (Bl ≈ 1,5 T·m) | ≈ 1,1 A Spitze (Ø40) | B aus G |
| Elektrische Leistung | ≈ 2–5 W (Ø40), ≈ 0,6–1,2 W (Ø28) | B aus G |
| Frequenzbereich | 1–200 Hz, unterhalb Eigenresonanz des Treibers (typ. 150–300 Hz, durch Luftfeder höher) stark gedämpft linear | G |
| Abmessungen Aktuator | Ø45 × 35 mm, gesamt ≈ 50 × 50 × 60 mm | G |
| Teile | ≈ 12 (davon 6 gefertigt) | G |

**Druckverlauf:** Beliebige Kurvenform (Sinus, Rechteck mit Flanken, Burst, Rampen). Die Amplitude ist unabhängig von der Frequenz regelbar. Mit Drucksensor ist eine geschlossene Druckregelung möglich.

**Geräusch:** Es gibt keine rotierenden Teile. Hörbar sind Oberwellen, Gehäuseresonanzen und Luft an der Düse. Bei geschlossenem Rückvolumen wird das voraussichtlich das leiseste Konzept (G).

**Fertigung:**
- FDM: Gehäuse, Kammer, Düse, Hubanschlag-Ring und Treiberklemmung (PETG; PLA für Passproben).
- Plotter: Flachdichtungen und eine optionale Schutzfolie vor dem Konus.
- Laser: Prüfstand-Grundplatte, Leckblenden-Satz.

Die Membran ist ein **Kaufteil** (Lautsprecher), daher hängt die Funktion nicht von der unbekannten Folie ab.

**Risiken:**
- Gleichstromfehler: Ein defekter Verstärker legt DC an die Spule. Die Membran bleibt ausgelenkt, es entsteht statischer Druck und die Spule überhitzt.
- Der Lautsprecherkonus ist nicht für statische Druckdifferenzen ausgelegt (Ermüdung, Sicke).
- Die Amplitude ist nicht geometrisch begrenzt: Xmax allein ergibt im Dichtfall 14 kPa. Ein **mechanischer Hubanschlag** ist Pflicht.

### Konzept B – Motorisierte Membran (Exzenter + Pleuel)

![Konzept B](img/konzept_b_exzenter.svg)

**Prinzip:** Ein DC-Motor ohne Getriebe treibt einen Exzenter. Ein Pleuel bewegt eine Mittelplatte, die in eine eingespannte Elastomermembran eingeklebt ist. Es gibt keine Ventile: Die Membran verdrängt Luft in V0, und die Luft schwingt durch die Düse hin und her. Die Frequenz entspricht Drehzahl/60.

| Merkmal | Wert | Stufe |
|---|---|---|
| Membran Ø20, Mittelplatte Ø12 → A_eff | 205 mm² | B |
| Exzentrizität e | 0,25 / 0,34 / 0,5 mm (Wechselexzenter) | Annahme |
| ΔV bei e = 0,5 mm | 103 mm³ → dicht 7,3 kPa (V0 2 cm³) | B |
| **Eigensicher (≤ 5 kPa dicht)** | **e ≤ 0,34 mm bei V0 = 2 cm³** oder V0 ≥ 2,9 cm³ bei e = 0,5 mm | B |
| Kraft / Moment bei 2 kPa | 0,41 N / 0,21 mN·m (+ Membransteifigkeit, Reibung) | B |
| Drehzahl für 5–150 Hz | 300–9000 min⁻¹ → Motor 130 oder N20 ohne Getriebe | B |
| Elektrische Leistung | 0,5–1,5 W | G |
| Abmessungen | ≈ 35 × 30 × 60 mm | G |
| Teile | ≈ 16 (davon 8 gefertigt) | G |

**Einstellbares Hubvolumen:**
1. **Wechselexzenter** (gedruckt mit Stahlstift oder Kugellager): einfach, eigensicher.
2. **Verstellbare Kurbel** (Langloch und Klemmschraube): stufenlos, aber nur im Stillstand verstellbar.
3. **Bleed-Nadelventil** an der Kammer: Die Amplitude lässt sich im Betrieb absenken, aber nicht erhöhen.

Die Amplitude ist bei dichter Kammer unabhängig von der Drehzahl. Mit Leck steigt sie mit der Frequenz (Tabelle Abschnitt 4).

**Mechanische Belastung:** Die Pleuelkraft liegt unter 1 N. Kritisch sind die **Lastwechsel**: 100 Hz ergeben 3,6·10⁵ Zyklen pro Stunde.
- Gleitlager aus PETG würden verschleissen und quietschen. Für Exzenter und Pleuelauge sind **Miniatur-Kugellager 683/693** vorgesehen.
- Die Membran muss Biegewechsel aushalten (Materialfrage).
- Die Unwucht von Exzenter und Pleuel erzeugt Gehäusevibrationen. Ein Gegengewicht am Exzenter ist nötig.

**Geräusch:** Bürstenmotor (Kommutator-Geräusch im kHz-Bereich), Lager, Unwucht. Voraussichtlich lauter als A (G). Ein bürstenloser Motor wäre leiser, aber teurer und braucht einen eigenen Regler.

**Miniaturisierung:** Gut machbar. N20-Motor Ø12, Exzenter Ø8, Membran Ø16 ergeben ein Gehäuse von ≈ 25 × 25 × 50 mm. Das kleinere A_eff wird mit grösserem e ausgeglichen.

**Fertigung:**
- FDM: Gehäuse, Kammer, Exzenter, Pleuel, Membranklemmring.
- Plotter: Membran und Dichtungen.
- Laser: Prüfstand, Leckblenden.

**Höchster Eigenfertigungsanteil.** Die Funktion hängt direkt von der Membranfolie ab.

### Konzept C – Mikropumpe mit Ventilsteuerung

![Konzept C](img/konzept_c_pumpe_ventile.svg)

**Prinzip:** Je eine Mikromembranpumpe (Typ 370, 3–6 V) füllt einen Überdruck- und einen Unterdruckpuffer. Zwei 3/2-Magnetventile verbinden die Kammer abwechselnd mit P+ und P−. Ein stromlos offenes Ventil entlastet die Kammer bei Abschaltung zur Atmosphäre. Die Pulsform entsteht durch den Ventiltakt.

| Merkmal | Wert | Stufe |
|---|---|---|
| Pumpe Typ 370: Förderstrom / max. Druck | 1–2 l/min, 40–80 kPa bzw. −40 kPa | G |
| Ventilschaltzeit | 5–15 ms → praktisch **5–30 Hz** | G |
| Druckanstiegszeit in 2 cm³ bei Puffer 5 kPa, Ventil Ø1 mm | ≈ 1–3 ms (sehr schnell, durch Ventil begrenzt) | B (Grössenordnung) |
| Elektrische Leistung | 2–4 W (2 Pumpen + 2 Ventile) | G |
| Abmessungen | ≈ 70 × 50 × 40 mm | G |
| Teile | ≈ 22 (davon 4 gefertigt) | G |

**Stärken:**
- Erzeugt **Gleichanteile** (Dauersog oder Dauerdruck) und sehr tiefe Frequenzen.
- Pulsformen mit Pausen sind möglich.
- Die Pumpe liegt räumlich getrennt, die Kammer kann sehr klein sein.

**Schwächen:**
- Es entsteht keine reine Wechseldruckwelle, sondern geschaltete Druckstösse mit Nettoströmung.
- Die Ventile begrenzen die Frequenz auf etwa 30 Hz und klicken.
- Es braucht zwei Pumpen, Puffer und viele Kaufteile.
- **Die Pumpen können ein Vielfaches der Druckgrenze erzeugen.** Die Sicherheit hängt deshalb an Ventilen, Sensor und Firmware statt an der Geometrie.

**Fertigung:**
- FDM: Gehäuse, Puffer, Verteilerblock (Dichtheit von FDM-Kanälen ist kritisch, siehe Risiken).
- Plotter: Dichtungen.
- Laser: Prüfstand.

---

## 6. Vergleich

| # | Kriterium | A Voice-Coil | B Exzenter-Membran | C Pumpe + Ventile |
|---|---|---|---|---|
| 1 | Funktionsprinzip | Volumenverdrängung, elektrodynamisch | Volumenverdrängung, kinematisch | Druckquellen + Schaltventile |
| 2 | Aktuator / Leistung | Lautsprecher, 0,6–5 W | DC-Motor, 0,5–1,5 W | 2 Pumpen + 2–3 Ventile, 2–4 W |
| 3 | Druckverlauf | beliebig, sinus- bis pulsförmig | sinusähnlich, Amplitude fest durch e | Rechteckpulse, Gleichanteil möglich |
| 4 | Frequenz / Regelbarkeit | 1–200 Hz, f und p unabhängig | 5–150 Hz (Drehzahl), p nur über e/Bleed | 5–30 Hz, Tastverhältnis frei |
| 5 | Mechanische Komplexität | gering (keine Kinematik) | mittel (Lager, Pleuel, Unwucht) | hoch (Pneumatiknetz, Puffer, Ventile) |
| 6 | Abmessungen / Teile | ≈ 50×50×60 mm / ≈ 12 | ≈ 35×30×60 mm / ≈ 16 | ≈ 70×50×40 mm / ≈ 22 |
| 7 | Energie / Geräusch | mittel / leise (G) | gering / mittel (G) | mittel / laut (Pumpe, Klicken) (G) |
| 8 | Fertigbarkeit H2S/Laser/Plotter | gut, Membran Kaufteil | sehr gut, höchster Eigenanteil | mässig, überwiegend Kaufteile |
| 9 | Kosten Demonstrator (Tabelle 9) | ≈ CHF 40 | ≈ CHF 35 | ≈ CHF 70 |
| 10 | Hauptrisiko | DC-Fehler, Konus-Ermüdung, Hubbegrenzung | Membranermüdung, Lager, Vibration | Überdruck durch Pumpen, Dichtheit, Frequenzgrenze |

**Vor- und Nachteile kompakt**

| | Vorteile | Nachteile |
|---|---|---|
| A | Frei programmierbare Kurvenform, ideal als **Messplattform**. Leise, wenig Mechanik, Membran ist Kaufteil. | Nicht eigensicher ohne Anschlag. Strombedarf bei Ø40. Ausfallart DC. Abhängig von der Lautsprecherqualität. |
| B | Mit kleinem e **geometrisch eigensicher**. Billig, robust, bewährtes Prinzip (HFCWO), höchster Eigenfertigungsanteil. | Amplitude im Betrieb kaum verstellbar. Lager- und Unwuchtgeräusch. Membranmaterial entscheidend. |
| C | Gleichanteil und Pausen möglich, sehr tiefe Frequenzen. | Druckquelle stärker als die Grenze. Frequenz ≤ 30 Hz, laut, teuer, viele Teile. Prinzip weicht vom reinen Wechseldruckfeld ab. |

## 7. Sicherheit und Prüfkonzept

### 7.1 Mindestanforderungen (K.-o.-Kriterien, nicht kompensierbar)

| ID | Anforderung | Nachweis |
|---|---|---|
| S1 | \|p\| ≤ 5 kPa in der Kammer bei **jeder** Kombination aus vollständig verschlossener Düse und maximaler Ansteuerung | Rechnung p = γ·p0·ΔV/V0 und Messung mit verschlossener Düse |
| S2 | Kein statischer Unter- oder Überdruck: Entlüftungsbohrung (Bleed) Ø0,3–0,5 mm, Gleichanteil < 0,2 kPa nach 1 s | Sprungantwort messen |
| S3 | Mechanische Hubbegrenzung des Verdrängers (Anschlag), unabhängig von der Elektronik | Konstruktion, Prüfung mit Maximalansteuerung |
| S4 | Externe SELV-Versorgung ≤ 12 V DC, strombegrenzt, mit Sicherung (Polyfuse) im Gerät, kein Netzteil-Eigenbau, kein Akku in Phase 1 | Datenblatt Netzteil, Kurzschlusstest |
| S5 | Temperatur: Spule bzw. Motor ≤ 60 °C an der Oberfläche, NTC mit Abschaltung, Überstromabschaltung | Dauerlauf 30 min mit Thermoelement |
| S6 | Fehlerfall = drucklos: Abschaltung, Watchdog-Reset oder Ventil stromlos lassen die Kammer zur Atmosphäre entlasten | Fehlerinjektion (Stecker ziehen, MCU-Reset) |
| S7 | Bewegte Teile (Exzenter, Pleuel, Konus) vollständig eingehaust, Finger nicht erreichbar | Sichtprüfung, Prüfstift |
| S8 | Druckschwingung messtechnisch erfasst (nicht nur berechnet), bevor andere Eigenschaften bewertet werden | Messprotokoll |

**Erfüllbarkeit je Konzept**

| | S1 | S2 | S3 | S4 | S5 | S6 | S7 | S8 |
|---|---|---|---|---|---|---|---|---|
| A | mit Anschlag + Strombegrenzung + DC-Schutz (Koppelkondensator/DC-Detektor) | Bleed | Anschlagring | ja | NTC an Magnet/Spule | Membran federt zurück, Bleed | Gehäuse | ja |
| B | **geometrisch** über e und V0 | Bleed | Exzenter = Anschlag | ja | NTC am Motor, Stall-Erkennung | Motor aus = Membran steht, Bleed | Gehäuse | ja |
| C | **nur aktiv**: 2 mechanische Druckbegrenzungsventile + Sensor + Firmware | NO-Ventil + Bleed | entfällt | ja | NTC Pumpe | NO-Ventil (stromlos offen) | Gehäuse | ja |

Alle drei Konzepte erfüllen die Anforderungen nur mit den genannten Massnahmen. **C ist sicherheitstechnisch am schwächsten:** Die Druckquelle ist um den Faktor 8–16 stärker als die Grenze, und S1 hängt allein an mechanischen Ventilen, deren Ansprechdruck selbst geprüft werden muss.

### 7.2 Prüfaufbau Demonstrator

- **Prüfkammer** (FDM, PETG) mit definiertem Volumen (5 cm³) an der Düse. Wechselbare **Leckblenden** Ø0 (dicht), 0,5, 1, 2, 3 mm als Laserteile (bewährtes Prinzip aus M08) bilden reale Undichtheit nach.
- **Drucksensor** ±10 kPa differenziell (z. B. XGZP6897D, I²C, G), Abtastung ≥ 2 kHz (≥ 10 × f_max), statisch kalibriert gegen das U-Rohr M12.
- **Messgrössen:** p_max, p_min, Gleichanteil, Kurvenform/Oberwellen, Frequenz, Druck bei verschlossener Düse, Stromaufnahme, Temperatur nach 30 min, Schalldruckpegel dB(A) in 30 cm.
- **Reihenfolge:** zuerst Dichtfall bei minimaler Ansteuerung, dann schrittweise erhöhen. Abbruch bei \|p\| > 4 kPa (20 % Reserve zur Grenze).

## 8. Risikoanalyse

W = Wahrscheinlichkeit, A = Auswirkung (1 gering – 3 hoch), R = W·A.

| ID | Risiko | Konzept | W | A | R | Massnahme |
|---|---|---|---|---|---|---|
| R1 | Unbekannte Folie ungeeignet (Ermüdung, Gaspermeation, Weichmacher/PVC) | B (A, C für Dichtungen) | 3 | 2 | 6 | Folie identifizieren (s. u.), sonst definierte Folie kaufen: TPU 0,1–0,2 mm, Silikon 0,3–0,5 mm. **Unbekannte Folie nie lasern**, nur plotten |
| R2 | Überdruck im Dichtfall | C (A ohne Anschlag) | 2 | 3 | 6 | S1, S3; bei C zwei unabhängige Begrenzungsventile |
| R3 | Leck an der Düse verhindert Wirkung bei tiefen Frequenzen | alle | 3 | 2 | 6 | Grösseres ΔV bei kleinen f, Leckblenden-Messreihe |
| R4 | FDM-Kammer undicht (Porosität zwischen Schichten) | alle | 2 | 2 | 4 | ≥ 4 Wände, 100 % Füllung um Kammer, Dichtigkeitsprüfung Abfallzeit, ggf. Versiegelung |
| R5 | DC-Fehler Verstärker → Spule überhitzt, statischer Druck | A | 2 | 2 | 4 | Koppelkondensator oder DC-Erkennung, Polyfuse, NTC |
| R6 | Lagerverschleiss / Geräusch bei 3,6·10⁵ Lastwechseln/h | B | 2 | 2 | 4 | Kugellager 683/693, Gegengewicht |
| R7 | Ventil-Frequenzgrenze unterschreitet Zielbereich | C | 3 | 2 | 6 | – (Konzeptgrenze) |
| R8 | Lautsprecherkonus ermüdet unter statischem Druckanteil | A | 2 | 2 | 4 | Bleed (kein Gleichanteil), Hubanschlag, Treiber mit Gummisicke |
| R9 | Schutzrechte bei späterer Weitergabe | alle | 2 | 3 | 6 | FTO-Prüfung vor Veröffentlichung oder Verkauf |
| R10 | Adiabatische Rechnung überschätzt Druck um bis 30 % | alle | 3 | 1 | 3 | Messung, Auslegung mit Reserve |

**Unbekannte Folie – Vorgehen:**
1. Dicke messen.
2. Dehnbarkeit und Rückstellung von Hand prüfen.
3. **Beilstein-Test** (Kupferdraht, Flamme, im Freien) auf Chlor: grüne Flamme bedeutet PVC/PVDC, dann für Membran und Laser ausgeschlossen.
4. Ohne sichere Identifikation nur für PLA-Passproben verwenden, nicht für Funktionsmembranen.

## 9. Vorläufige Stücklisten (Demonstrator, Kosten G, CHF)

**A – Voice-Coil**

| Teil | Stk | CHF |
|---|---|---|
| Kleinlautsprecher Ø28–40 mm, 4–8 Ω, 2–3 W, Gummisicke | 1 | 3–6 |
| Klasse-D-Verstärkermodul (z. B. MAX98357A I²S oder PAM8302) | 1 | 2–4 |
| Mikrocontroller-Board (ESP32-C3 / RP2040) | 1 | 4–6 |
| Drucksensor ±10 kPa differenziell, I²C | 1 | 5–10 |
| NTC 10 k, Polyfuse 1 A, Koppelkondensator, Kleinteile | 1 | 2 |
| Netzteil 5 V/2 A USB-C (SELV, zertifiziert) | 1 | 8 |
| Silikonschlauch, Schrauben, Dichtungen | – | 3 |
| PETG ≈ 40 g, Sperrholz Prüfstand | – | 2 |
| **Summe** | | **≈ 30–41** |

**B – Exzenter-Membran**

| Teil | Stk | CHF |
|---|---|---|
| DC-Motor 130 oder N20 ohne Getriebe, 6 V | 1 | 2–4 |
| Kugellager 683ZZ (3×7×3) | 2 | 2 |
| Stahlstift Ø3, Madenschraube | – | 1 |
| MOSFET-Treiber + Freilaufdiode, Hallsensor für Drehzahl | 1 | 2 |
| Membranfolie (TPU/Silikon, falls Folie ungeeignet) | 1 | 4 |
| Mikrocontroller, Drucksensor, NTC, Polyfuse, Netzteil (wie A) | – | 19–26 |
| PETG ≈ 50 g, Sperrholz, Schrauben | – | 3 |
| **Summe** | | **≈ 33–42** |

**C – Pumpe + Ventile**

| Teil | Stk | CHF |
|---|---|---|
| Mikromembranpumpe Typ 370 (Druck, Saug) | 2 | 8–12 |
| 3/2-Magnetventil 6–12 V (Mini) | 2 | 8–14 |
| 2/2-Magnetventil stromlos offen (Entlastung) | 1 | 4–7 |
| Druckbegrenzungsventil einstellbar (Über-/Unterdruck) | 2 | 6–10 |
| MOSFET-Treiber ×4, Freilaufdioden | 1 | 3 |
| Mikrocontroller, Drucksensor, NTC, Polyfuse | – | 11–18 |
| Netzteil 12 V/1 A (SELV) | 1 | 9 |
| Schläuche, Verbinder, Puffer (FDM), Schrauben | – | 6 |
| **Summe** | | **≈ 55–79** |

## 10. Bewertung

Punkte 1 (schlecht) – 5 (sehr gut).

| Kriterium | Gewicht | A | B | C |
|---|---|---|---|---|
| Eignung des Druckwellenprinzips | 25 % | 5 | 4 | 2 |
| Technische Realisierbarkeit | 20 % | 4 | 4 | 3 |
| Fertigbarkeit mit vorhandenen Maschinen | 20 % | 4 | 5 | 3 |
| Kompaktheit und Geräusch | 15 % | 4 | 3 | 2 |
| Kosten und Bauteilverfügbarkeit | 10 % | 4 | 5 | 3 |
| Einstellbarkeit und Erweiterbarkeit | 10 % | 5 | 3 | 4 |
| **Gewichtete Summe** | | **4,35** | **4,05** | **2,70** |
| Sicherheits-Mindestbedingungen S1–S8 | K.-o. | erfüllbar mit Anschlag + DC-Schutz | **geometrisch erfüllbar** | erfüllbar nur aktiv, schwächste Absicherung |

**Begründungen:**
- **Prinzip:** A erzeugt das Wechseldruckfeld direkt und in beliebiger Form. B erzeugt es ebenfalls, aber nur sinusähnlich mit festem Hub. C schaltet Druckquellen, das ist eher Pulssog als Wechseldruckfeld, und die Frequenz endet bei etwa 30 Hz.
- **Realisierbarkeit:** A und B sind mit Standardteilen und einfacher Elektronik machbar. C braucht ein Pneumatiknetz mit Puffern und Begrenzungsventilen.
- **Fertigbarkeit:** B hat den höchsten Eigenanteil (Exzenter, Pleuel, Membran). A hat eine gekaufte Membran. C besteht überwiegend aus Kaufteilen, und die FDM-Verteiler sind dichtheitskritisch.
- **Kompaktheit/Geräusch:** A hat keine Rotation. B hat Motor- und Lagergeräusch sowie Unwucht. C hat Pumpe plus Ventilklicken.
- **Kosten:** B ist am günstigsten, C fast doppelt so teuer.
- **Einstellbarkeit:** A ist vollständig softwaredefiniert. C bietet Tastverhältnis und Gleichanteil. Bei B sind nur Frequenz und Wechselexzenter einstellbar.

## 11. Empfehlung

**Erster Prototyp: Konzept A (Voice-Coil) als Mess- und Funktionsplattform.** Die Freigabe ist an folgende Bedingungen geknüpft:
1. Mechanischer Hubanschlag, der den Dichtfall auf ≤ 5 kPa begrenzt (S1, S3).
2. DC-Schutz und Strombegrenzung im Verstärkerpfad (R5).
3. Bleed-Bohrung (S2).
4. Ein Lautsprecher Ø28–36 mm statt Ø40, um Strom und Kammervolumen zu senken.

**Begründung:** A hat die höchste Gesamtwertung. A misst vor allem genau die offenen Grössen, die für jedes spätere Produktkonzept entscheiden: welche Frequenzen, Amplituden und Kurvenformen bei welchem Leck welche Druckwelle ergeben. Diese Grössen lassen sich ohne Umbau per Software durchfahren.

**Konzept B ist die Rückfalloption mit geringem Abstand** (4,05). Mit den Messwerten aus A lässt sich der feste Exzenterhub von B gezielt auslegen. B ist sicherheitstechnisch das robusteste Konzept (geometrische Druckbegrenzung) und als kompaktes Endgerät vermutlich günstiger.

**Konzept C wird nicht weiterverfolgt.** Gründe sind die Sicherheitsarchitektur, die Frequenzgrenze, die Kosten und die Abweichung vom Wechseldruckprinzip.

## 12. Offene Fragen für die Entscheidung

1. Zielfrequenzbereich bestätigen: ist 5–150 Hz richtig, oder reicht 20–120 Hz?
2. Druckgrenze 5 kPa als Projektgrenze akzeptiert? (Die Wahl des Konzepts hängt davon ab.)
3. Zusammensetzung der vorhandenen Folie: Hersteller, Bezeichnung, Dicke?
4. Darf der erste Prototyp Kaufteile wie einen Lautsprecher enthalten, oder soll der Eigenfertigungsanteil maximal sein? (Im zweiten Fall Konzept B.)

## 13. Fachliche Gegenprüfung

*(wird nach der unabhängigen Prüfung ergänzt)*

## Quellen

- [Womanizer (pressure wave vibrator) – Wikipedia](https://en.wikipedia.org/wiki/Womanizer_(pressure_wave_vibrator))
- [US 9,763,851 Stimulation device (uspto.report)](https://uspto.report/patent/grant/9763851) · [US 2016/0213557 A1](https://insight.rpxcorp.com/pat/US20160213557A1) · [CA 2 978 739](https://brevets-patents.ic.gc.ca/opic-cipo/cpd/eng/patent/2978739/summary.html) · [US 12,329,710 B2](https://patentsgazette.uspto.gov/week24/OG/html/1535-3/US12329710-20250617.html)
- [Device for stimulating a human erogenous zone using a variable pressure field (USPTO PDF)](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12576003)
- [Methods for enhancing female orgasm (USPTO PDF)](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/10646399)
- [Variable stroke air pulse generator US 7,785,280](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/7785280) · [High frequency air pulse generator US 7,121,808](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/7121808) · [Scotch yoke US 7,770,479](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/7770479)
- [Sifted – Womanizer inventor](https://sifted.eu/articles/womanizer-inventor)
