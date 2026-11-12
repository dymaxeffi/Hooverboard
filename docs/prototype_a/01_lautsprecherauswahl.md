# Prototyp A – Schritt 1: Lautsprecher aus dem Bestand auswählen

**Ziel:** Aus den ca. 40 vorhandenen Lautsprechern den besten Antrieb finden. Dazu braucht es nur Multimeter, Messschieber, Lineal, Münzen und eine einstellbare Gleichstromquelle.

**Dauer:** etwa 1 h für die Sichtung aller 40, dann etwa 10 min pro Lautsprecher der engeren Wahl.

**Ergebnis:**
- die ausgefüllte Tabelle `lautsprecher_messung.csv`
- die Auswertung mit `python calculations/pressure_actuator/speaker_select.py`. Sie erzeugt `lautsprecher_auswertung.md` mit Rangliste, Bauform und Vorwiderstand.

---

## Warum nicht einfach den grössten oder stärksten?

Für unseren Aktuator zählt der **Druck pro Ampere**, und der ist **Bl / Fläche**:
- **Bl** ist die Antriebskraft pro Ampere (Magnet × Spulendraht), in T·m bzw. N/A.
- Die **Fläche** ist die Fläche, die auf die Luftkammer drückt.

Ein grosser Konus hat viel Fläche und braucht daher viel Strom für wenig Druck. Die Beispielrechnung zeigt: Ein normaler Ø40-Lautsprecher, **direkt** als Kammerwand eingesetzt, erreicht an 5 V nur ≈ 2 kPa. Das ist zu knapp.

**Lösung: Bauform „Lautsprecher als Motor“.** Der Konus bleibt offen. Ein leichter Stössel auf der Staubkappe treibt eine kleine, geplottete Membran Ø20 mm (wirksam 2,05 cm²) in einer eigenen Kammer an. Die Fläche ist 4–7-mal kleiner, also steigt der Druck pro Ampere um denselben Faktor. Zusätzlich müssen Polkernbohrung und Stoffkappe nicht mehr abgedichtet werden. Das Skript bewertet beide Bauformen und wählt je Lautsprecher die bessere.

Ein **zu starker** Lautsprecher ist kein Problem: Ein Vorwiderstand begrenzt den Druck. Diese Grenze wirkt passiv und gilt auch dann, wenn der Verstärker im Fehlerfall Gleichspannung ausgibt (Sicherheitsanforderung S1).

---

## Stufe 1 – Sichtung (alle Lautsprecher, je ca. 1 min)

Pro Lautsprecher eine Zeile in `lautsprecher_messung.csv` anlegen (Tabellenkalkulation oder Texteditor):

| Spalte | Was | Wie |
|---|---|---|
| `id` | eigene Nummer | Klebeetikett auf den Korb: L01, L02 … |
| `beschreibung` | Herkunft / Aufdruck | z. B. „Bluetooth-Box rot, 4Ω 3W“ |
| `d_aussen_mm` | Korbdurchmesser | Messschieber |
| `d_sd_mm` | **wirksamer** Membrandurchmesser | Konus **plus halbe Sickenbreite** auf jeder Seite (Mitte der Sicke zu Mitte der Sicke) |
| `re_ohm` | Gleichstromwiderstand | Multimeter Ω-Bereich, Messleitungen vorher kurzschliessen und den Wert abziehen |
| `nenn_w` | Nennleistung | Aufdruck, sonst leer lassen |
| `staubkappe` | `dicht` oder `gewebe` | Gegenlicht: Stoffkappe ist luftdurchlässig |
| `polkernbohrung` | `ja` / `nein` | Loch hinten mittig im Magnet |
| `sicke` | `gummi`, `schaum`, `stoff`, `papier` | |
| `zustand` | `ok` oder Mangel | Sicke rissig/bröselig, Konus eingedrückt, Kratzen beim sanften Drücken → **aussortieren** |

**Gleich aussortieren:**
- Piezo-Hochtöner: sie haben kein Bl.
- Defekte Lautsprecher.
- Re unter 2 Ω oder über 16 Ω.
- Lautsprecher, deren Konus sich beim sanften Andrücken nicht frei und ohne Kratzen bewegen lässt.

**In die engere Wahl (Stufe 2) kommen 5–8 Lautsprecher:** schwere, kräftige Magnete im Verhältnis zur Grösse, Re 3–8 Ω, Korb Ø30–60 mm, Gummisicke. Kleine Handy- und Laptop-Lautsprecher sind meist zu schwach. Ein Versuch mit dem stärksten davon schadet aber nicht.

---

## Stufe 2 – Bl und Federsteifigkeit messen (Nullabgleich)

**Prinzip:** Eine bekannte Masse drückt den Konus nach unten. Dann wird ein Gleichstrom so weit erhöht, dass der Konus **genau wieder in der Ausgangslage** steht. In dieser Lage trägt die Aufhängung nichts, die ganze Gewichtskraft trägt die Spule:

  **Bl = m · g / I**  (g = 9,81 m/s²)

Die Absenkung ohne Strom liefert gleichzeitig die Federsteifigkeit der Aufhängung: k = m·g / x.

### Material

- Münzen als Gewicht (am besten auf der Küchenwaage wiegen). Richtwerte: 5 Fr. 13,2 g · 2 Fr. 8,8 g · 1 Fr. 4,4 g.
- Kartonscheibe Ø15–20 mm als Auflage, damit die Münze mittig und flach auf der Staubkappe liegt. Die Kartonscheibe wird mitgewogen.
- Stahllineal quer über den Korbrand, Messschieber mit Tiefenmass (oder Messuhr).
- **Stromquelle**, eine der folgenden:
  - Labornetzteil mit Strombegrenzung (am besten), oder
  - 1 Mignon-Batterie (1,5 V) plus Potentiometer 10–50 Ω bzw. mehrere Widerstände, Multimeter im **A-Bereich in Reihe**.

### Ablauf

1. Lautsprecher **waagrecht, Konus nach oben**, stabil hinlegen. Lineal quer über den Korb legen.
2. Mit dem Tiefenmass den Abstand Lineal → Mitte der Staubkappe messen: **Nullage** (zweimal, Mittelwert).
3. Kartonscheibe und Münze(n) mittig auflegen. Erneut messen. Die Differenz ist die Auslenkung `bl_auslenkung_mm`. Ziel: 0,1–1 mm. Bei weniger mehr Gewicht, bei mehr weniger Gewicht.
4. Strom einschalten, bei kleinstem Strom beginnen.
   - **Polarität:** Der Konus muss nach **oben** gehen. Geht er tiefer, die Anschlüsse tauschen.
5. Strom erhöhen, bis der Konus wieder bei der Nullage steht (±0,02 mm). Strom ablesen → `bl_strom_a`.
6. Strom aus. Masse inklusive Kartonscheibe in `bl_masse_g` eintragen.

**Sicherheit beim Messen:**
- Gleichstrom höchstens **10 s** am Stück, dann mindestens 30 s Pause.
- Strom höchstens die Hälfte des Nennstroms (Nennstrom = √(Nennleistung/Re), z. B. 3 W/4 Ω → 0,87 A → max. 0,43 A).
- Wird die Spule spürbar warm, Pause einlegen.
- Netzteil mit Strombegrenzung, kein Netzteil ohne Begrenzung direkt anschliessen.

**Genauigkeit:**
- Bl auf etwa ±5–10 % genau. Das reicht für die Auswahl.
- Fehlerquellen: schräg liegende Münze, Lineal nicht immer an derselben Stelle, Spulenerwärmung (Re steigt, der Strom bleibt aber gemessen).

### Sonderfall: Wandler mit Stössel (Exciter, Resonanzlautsprecher, Körperschallwandler)

Diese Wandler passen direkt zur Motor-Bauform: Der Stössel treibt die Membran, ein Umbau entfällt. Messung wie oben, mit folgenden Abweichungen:
- **Gehäuse bzw. Magnet fest einspannen** (Schraubstock mit Zulage oder Klebeknete auf der Tischplatte), **Stössel senkrecht nach oben**.
- Masse auf das Stösselende legen. Auslenkung und Nullage am Stösselende messen.
- In der CSV `d_sd_mm` **leer lassen**. Das Skript rechnet dann nur die Motor-Bauform. In `beschreibung` „Exciter“ bzw. „Stössel“ und den Aufdruck notieren.
- Bitte zusätzlich den **freien Hub** des Stössels messen: wie weit er sich von Hand ohne Anschlag in beide Richtungen bewegen lässt. Nötig sind mindestens ±0,3 mm.

---

## Auswertung

```bash
python calculations/pressure_actuator/speaker_select.py
```

Solange `lautsprecher_messung.csv` leer ist, rechnet das Skript die Beispieldatei. Das Ergebnis steht dann in `lautsprecher_auswertung_beispiel.md` (erfundene Werte, nur zur Demonstration).

Was das Skript je Lautsprecher und Bauform rechnet (B, aus deinen Messwerten):

| Grösse | Bedeutung |
|---|---|
| kPa/A | Druck pro Ampere = Bl / Fläche |
| erreichbar 5 V | Druck, der an 5 V maximal möglich ist, nach Abzug der Aufhängungskraft bei 0,3 mm Hub. Muss ≥ 3 kPa sein |
| p_max 5 V (Sicherheit) | obere Grenze ohne Abzug der Aufhängung. Danach wird der Vorwiderstand auf ≤ 4 kPa bemessen |
| Strom / Leistung für 2 kPa | weniger ist besser (Wärme). Rangkriterium |
| Vorwiderstand | begrenzt p_max auf 4 kPa. Belastbarkeit für den Gleichstrom-Fehlerfall wird angegeben |

**Bitte zurückmelden:** die ausgefüllte CSV (oder ein Foto der Tabelle). Danach lege ich im nächsten Schritt den Antrieb fest und konstruiere Stössel, Membranhalter und Kammer passend zum gewählten Lautsprecher.
