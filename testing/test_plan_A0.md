# Prüfstand A0 – Luftkissen-Grundversuch (unbemannt)

Status: Vorschlag Phase 0. Bau erst nach Freigabe G0 und D-004.

## 1. Ziel

Die drei Grössen messen, an denen der Konzeptentscheid hängt und die sich nicht berechnen lassen:

1. **Effektiver Leckspalt** Cd·h der Schürze auf verschiedenen Böden
2. **Gebläsekennlinie** p(Q) und elektrische Leistung eines realen Gebläses
3. **Schürzenschleppkraft** und **Kippverhalten** bei Lastversatz

Zusätzlich: Lärm, Verhalten bei Lastsprüngen, Schürzenverschleiss.

## 2. Aufbau

- **Plattform:** Sperrholzplatte 800 × 500 mm, Eckradius 120 mm (= Startgeometrie, keine Skalierungsfehler). Zuschnitt mit Stichsäge; Lochbild/Schablonen mit H2S-Laser oder -Druck.
- **Gebläse:** zunächst ein handelsüblicher **netzbetriebener Laubbläser** (keine Akku-Risiken in der Lernphase, Leistung einfach messbar). Anschluss über gedruckten Adapter in die Plattformmitte, mit Fingerschutzgitter am Einlass.
- **Schürzenvarianten:**
  - S0: ohne Schürze, starrer Rand mit einstellbaren Distanzklötzen (Referenz für Cd)
  - S1: einfache Membran-/Taschenschürze aus beschichtetem Gewebe oder Folie
  - S2: Membran mit zentralem Haltepunkt und Ausströmlöchern (bekannte Lehrmittel-Bauart)
  - S3 (optional): Längskiel → zwei Kammern, für Kipptest
- **Ballast:** verschlossene Wasserkanister in einer Halterung, mit Spanngurten gesichert, schrittweise 10 → 20 → 30 → 42.5 → 53 kg (Auslegungslast). Kein Mensch auf der Plattform.
- **Fesselung:** Leine zu festem Punkt, begrenzt Bewegung auf ≈ 1 m.

## 3. Messgrössen und Prüfmittel

| Grösse | Prüfmittel | Auflösung / Hinweis |
|---|---|---|
| Kissendruck p | U-Rohr-Wassermanometer (transparenter Schlauch) | 1 mm WS ≈ 9.8 Pa; ab Phase 3 elektronischer Differenzdrucksensor |
| Elektrische Leistung | Energiekostenmessgerät 230 V (vorher gegen bekannte Last prüfen) | Wirkleistung ablesen |
| Volumenstrom Q | Flügelrad-Anemometer am Gebläseeinlass (bekannte Fläche); Gegenprüfung mit Blendenplatten (lasergeschnitten) | Messunsicherheit gross → dokumentieren |
| Höhe Struktur | Messschieber/Massstab an 4 Ecken | ± 1 mm |
| Leckspalt | Fühlerlehre oder Lichtspalt mit Foto | qualitativ, Cd·h wird aus Q, p berechnet |
| Schleppkraft | Federwaage / Kofferwaage, langsamer gleichmässiger Zug | Mittelwert über 3 Züge |
| Neigung | Smartphone-Neigungsmesser (gegen Wasserwaage prüfen) | ± 0.5° |
| Lärm | Schallpegelmesser (Klasse 2 oder kalibrierte App), 1 m Abstand, 1.2 m Höhe | dB(A) |
| Masse | Personenwaage / Hängewaage für Ballast | ± 0.1 kg |

## 4. Versuchsmatrix

| Versuch | Variation | Ausgewertet |
|---|---|---|
| V1 | S0, Distanz 5/10/20 mm, Last 20 kg | Cd aus Q, p, Spalt → Referenz |
| V2 | S1/S2, Last 10…53 kg | p(m), P_el(m), Cd·h(m) |
| V3 | Gebläse gegen Blendenplatten | Kennlinie p(Q), Wirkungsgrad |
| V4 | S1/S2, Lastversatz 0/25/50/100 mm quer und längs | Neigung, Aufsetzen |
| V5 | Böden: Hallen-/Betonboden, Parkett/Laminat, Teppich, Asphalt (falls verfügbar) | Cd·h, Schleppkraft |
| V6 | Lastsprung (Gewicht absetzen, gesichert) | Absinken, Erholung |
| V7 | Dauerlauf 15 min | Erwärmung Gebläse, Schürzenverschleiss |

Jeder Messpunkt **3 ×** wiederholen. Rohdaten als CSV in `testing/data/A0/` mit Datum, Prüfmittel, Bedingungen (Temperatur, Luftdruck).

## 5. Akzeptanz (Datenqualität, nicht Produktfunktion)

- Wiederholbarkeit der Leistungsmessung ±10 %
- Druckmessung plausibel: p ≈ m·g / A innerhalb ±15 % (sonst Messfehler oder Flächenannahme falsch)
- Mindestens S1 oder S2 auf mind. 2 Böden mit allen Laststufen vermessen

## 6. Entscheidungsregeln für G1 (Vorschlag)

| Messergebnis bei Nennlast, glatter Boden | Folge |
|---|---|
| Cd·h ≤ 2 mm (≈ ≤ 0.6 kW el. hochgerechnet auf Akku-Gebläse) | K5 bestätigt, weiter mit 800 × 500 mm |
| Cd·h 2–4 mm | K5 machbar, Grösse/Schürze optimieren |
| Cd·h > 4 mm | Schürzenkonzept überarbeiten oder Fläche vergrössern; Anforderung „kompakt“ zur Diskussion stellen |
| Kippen/Aufsetzen schon bei 50 mm Versatz | Kammerung (K5b) wird Pflicht |

## 7. Abbruchbedingungen

Sofort Gebläse aus bei: Ballast verrutscht · Neigung > 15° · Schürze reisst · Geruch, Rauch oder ungewöhnliches Geräusch · Gebläse > Herstellergrenzen warm · Person im Gefahrenbereich.

## 8. Sicherheitsvorkehrungen

- Niemand steht oder sitzt auf der Plattform – auch nicht „kurz zum Testen“
- Gefahrenbereich 2 m, Zuschauer dahinter; Gehör- und Augenschutz für alle
- Fehlerstrom-Schutzschalter (FI/PRCD) im Netzanschluss; Kabel zugentlastet und vom Ansaugbereich fern
- Ansauggitter montiert, Boden vorher gereinigt (Fremdkörper)
- Kinder nur als Zuschauer ausserhalb des Gefahrenbereichs

## 9. Kosten

Ziel ≤ CHF 300 (Zielwert, nicht recherchiert). Positionen in `procurement/bom.csv` (Gruppe A0); Preise werden in Phase 1 recherchiert.
