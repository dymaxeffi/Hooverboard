# Rahmenbox – parametrische, materialsparende Faltverpackung

Einteilige, klebstofffreie Verpackung aus Packpapier oder dünnem Karton für kleine Designobjekte (X und Y bis 200 mm, Z bis 90 mm).
Rückwand und vier Seitenwände sind geschlossen. Die Front ist ein umlaufender Rahmen mit Gehrungsecken. Das Produkt bleibt durch die Öffnung sichtbar, und der Rahmen ist zugleich der Verschluss.

> Nebenprojekt im Repository. Es hat keinen Bezug zum Hoverboard und keine Abhängigkeiten zum übrigen Code.

**Generator:** `rahmenbox-generator.html` im Browser öffnen (lokal, offline, ohne Installation).

| Funktion | Umsetzung |
|---|---|
| Parameter | X, Y, Z, Rahmenbreite w, Materialstärke t, Flächengewicht, Verschlusstechnik (5 Varianten), Eckzungen, Bogengrösse, Rand, Teileabstand, Falzlinien-Art |
| Vorschau flach | Schnittmuster mit Schnitt-/Falzlinien, Masse, Kennzahlen |
| Vorschau gefaltet | 3D-Faltsimulation mit Schieberegler/Animation, drehbar |
| Export | SVG 1:1 (mm) mit Ebenen *Schnitt* (rot), *Falz* (blau) und *Info* (grün, nicht schneiden). Falze wahlweise als eigene Ebene oder als Perforation |
| Material | Fläche, Umriss, Masse, Schnitt- und Falzlänge pro Box |
| Nesting | Anordnung auf dem Bogen, Stück pro Bogen, Verschnitt in %, Nutzung bei Rollenware |
| Faltanleitung | automatisch erzeugte Schritte mit Bild je Schritt |
| Prüfung | geometrische Prüfungen bei jeder Änderung (siehe unten) |
| Vergleich | alle Varianten für die aktuellen Masse: berechnete und qualitative Kriterien |

---

## 1 Recherche

*Grundlage ist Fachwissen aus Verpackungstechnik, Origami und Kirigami. Es wurden keine Live-Quellen abgefragt. Normbezüge (FEFCO) dienen nur zur Einordnung.*

### 1.1 Selbstarretierende Faltmechanismen
- **Steckdeckel (Tuck-End)**, z. B. bei Faltschachteln: Eine Einstecklasche wird zwischen Wand und Staublaschen geklemmt. Die Verbindung hält über Reibung und ist robust, braucht aber eine grosse Lasche und doppelte Lagen.
- **Crash-Lock- und Snap-Lock-Boden**: Diagonal gefaltete Bodenlaschen hintergreifen sich und richten sich beim Aufstellen selbst auf. Die Sperre entsteht durch die Geometrie, nicht durch Reibung.
- **Masu-Box (Origami)**: Die Eckquadrate werden nicht weggeschnitten, sondern als Dreiecke (Gussets) eingefaltet und durch die umgelegten Ränder gehalten. Die Ecken sind dicht und schubsteif, aber mehrlagig.
- **Mailer-Box (FEFCO 0427)**: einteilig, mit eingerollten Doppelwänden und Zungen in Schlitzen. Sehr stabil, aber materialintensiv.

### 1.2 Steck- und Hakenverbindungen
- **Tab-and-Slot mit Pfeilkopf**: Der Hals wird im Schlitz geführt, der Widerhaken hintergreift die Schlitzkante. Die Verbindung sperrt in allen drei Richtungen. Wie gut sie hält, hängt von der Steifigkeit des Materials ab.
- **Hook-Lock**: zwei gegenläufig eingeschnittene Laschen, die sich verhaken (Einschnitt bis zur Mitte). Typisch für Trays.

### 1.3 Puzzle- und Interlock-Verschlüsse
- **Puzzle-Hinterschnitt**: Formschluss in der Ebene. Senkrecht zur Ebene hält er nur durch Klemmung. Das funktioniert erst ab einer gewissen Materialdicke und Steifigkeit.
- **Weben (Über-Unter)**: Zwei Laschen liegen abwechselnd übereinander und untereinander. So arbeiten Papierflechtwerk und viele Kirigami-Verbinder.

### 1.4 Windradverschlüsse
- **Pinwheel / Twist-Lock**: Vier Laschen greifen zyklisch untereinander. Jede wird von der nächsten gehalten, die letzte schiebt man unter die erste. Bekannt von Faltschachteldeckeln und Origami-Umschlägen. Kein Kleber nötig. Die Sperre wirkt nur senkrecht zur Ebene.

### 1.5 Bogenausnutzung
- **Ineinandergreifende Nutzen**: Kreuzförmige Zuschnitte lassen sich in einem schrägen Gitter verschachteln. Die Arme eines Zuschnitts füllen dabei die freien Ecken des Nachbarn. Das ist dichter als ein Raster aus umschreibenden Rechtecken.
- **Common-Line-Cutting**: Benachbarte Nutzen teilen sich eine Schnittlinie. Das spart Steg und Schneidweg, setzt aber Abstand 0 und gerade Kanten voraus.
- **Rolle vs. Bogen**: Auf einer Endlosbahn bestimmt allein die Gitterdichte die Ausnutzung. Auf kleinen Einzelbögen dominieren die Randverluste.

### 1.6 Folgerungen für die Konstruktion
1. Ein Kreuzzuschnitt mit trapezförmigen Rahmenlaschen erzeugt die Frontöffnung allein durch die Geometrie. Nichts wird herausgeschnitten, und die Gehrungen entstehen von selbst.
2. Die freien Ecken des Kreuzes sind ohnehin Verschnitt. Dort lassen sich kleine Eckzungen ohne Mehrverbrauch an Bogenfläche unterbringen (beim Endlosgitter kosten sie etwas Dichte).
3. Die Verriegelung gehört in die Gehrungsfuge. Dort liegen die Laschen ohnehin aneinander.
4. Für dünnes Papier eignen sich biegsame Zungen (Windrad, Weben). Für Karton eignen sich formschlüssige Verbindungen (Pfeil, Puzzle).

---

## 2 Grundkonstruktion

```
            ┌─Rahmen oben─┐            Rahmenlasche = Trapez mit 45°-Gehrungen,
            │  Wand oben  │            an der Vorderkante jeder Wand angelenkt.
   ┌────┬───┼─────────────┼───┬────┐
   │Rah-│ W │             │ W │Rah-│   Rückwand X×Y in der Mitte,
   │men │ a │  Rückwand   │ a │men │   Wände (Tiefe Z) an allen vier Kanten.
   │ l. │ n │             │ n │ r. │
   └────┴─d─┼─────────────┼─d─┴────┘   Eckzungen (optional) an den Enden
            │  Wand unten │            der Seitenwände, im sonst leeren Kreuzeck.
            └─Rahmen unten┘
```

- **Öffnung:** Die vier Trapeze reichen nur w nach innen. Die lichte Öffnung beträgt ≈ (X + t − 2w) × (Y + t − 2w).
- **Einlagiger Rahmen:** keine Doppelwände. Nur die Verriegelungselemente (Zunge, Pfeil) liegen kurz zweilagig.
- **Öffnen:** Die oberen Ecken entriegeln, dann klappt die obere Wand mitsamt Rahmenlasche als Deckel auf (Scharnier an der Rückwand). Bei der Faltecke (E) klappt man nur die Rahmenlaschen auf.
- **Materialstärke:** Das Modell rechnet mit Mittelflächen. Rückwand und Wände erhalten eine Zugabe von t. Die Seitenwände sind um t kürzer, damit die Eckzungen innen an Ober- und Unterwand anliegen. Die Gehrungsfuge beträgt g = max(0.25 mm, 0.8 t).
- **Faltsinn:** Alle Falze sind Talfalze zur Innenseite. Ausnahme ist die Diagonale der Faltecke (Bergfalz). Die Vorschau zeigt die Innenseite.

## 3 Fünf Lösungsansätze

| | Prinzip | Sperrt | Material |
|---|---|---|---|
| **A Windrad-Gehrung** | Je eine Zunge an der im Uhrzeigersinn folgenden Gehrung, zyklisch unter die nächste Lasche | senkrecht zur Front (zyklisch) | minimal |
| **B Verschränkte Gehrung („Webecke“)** | Jede Gehrung ist geteilt: aussen liegt die Seitenlasche unter der Deckellasche, innen umgekehrt | senkrecht, jede Ecke unabhängig | minimal |
| **C Puzzle-Gehrung** | Hinterschnittener Knopf der Deckel-/Bodenlasche in einer Bucht der Seitenlasche | in der Ebene (Zug und Schub über die Fuge) | minimal |
| **D Pfeillasche & Schlitz** | Pfeil an der Gehrung, durch einen Schlitz in der Seitenlasche gesteckt | in allen 3 Richtungen | minimal |
| **E Origami-Faltecke + Windrad** | Eckquadrate als Gusset nach innen gelegt, Rahmen wie A | Ecken schubsteif, Rahmen wie A | +20 … +50 % |

Alle Varianten sind kombinierbar: Eckzungen lassen sich ein- und ausschalten. Ein Puzzle-Knopf und eine Zunge an derselben Gehrung wären als weitere Mischform denkbar.

### Konstruktive Details
- **Zungen (A, B)** entstehen als Streifen an der Gehrung mit 45°-Anschrägung (Einführhilfe). Sie werden gegen die Nachbarlasche mit Randabstand m = max(0.8 mm, 3t) beschnitten und liegen deshalb immer vollständig verdeckt unter ihr.
- **Pfeil (D):** Halsbreite ≈ 0.24 w, Schlitz = Hals + 2·(0.2 + t/2). Die Pfeilbreite wird so gross wie möglich gewählt, solange der Kopf mit Randabstand m in die Seitenlasche passt. Die Schulter liegt 1.5 t hinter dem Schlitz.
- **Puzzle (C):** Kopfradius ≈ 0.16 w, Hals = 1.16 r, Passungsspiel 0.12 + 0.3 t (Knopf −½, Bucht +½).
- **Eckzungen:** Tiefe automatisch 0.28 X (5 … 15 mm). Sie beginnen eine Materialstärke vor der Rückwand und enden 1.5 t vor dem Rahmen.
- **Faltecke (E):** Die Dreiecke legen sich an das längere Wandpaar. Sie bilden einen geschlossenen Falzring: Das zweite Dreieck ist zugleich an der Nachbarwand angelenkt, was die Prüfung nachweist.

## 4 Geometrische Prüfung (im Generator, Tab „Prüfung“)

Der gefaltete Zustand wird nicht separat gezeichnet, sondern aus dem Schnittmuster berechnet. Jedes Teil wird dafür über einen Baum von Falzen um die Falzlinie gedreht. Geprüft wird:

1. **Einteiligkeit und Überlappungsfreiheit** des flachen Zuschnitts (Rastertest ≤ 0.5 mm).
2. **Rahmenlaschen in der Frontebene** (Abweichung aus der Rotation praktisch 0).
3. **Kollisionsfreiheit der Rahmenlaschen** in der Front, inklusive Puzzle-Knopf und Bucht mit Passungsspiel.
4. **Zungen bzw. Pfeilköpfe vollständig verdeckt** unter bzw. hinter der Nachbarlasche (Flächenanteil).
5. **Wandkanten geschlossen:** Der Versatz an den Ecken entspricht genau dem Lagenversatz.
6. **Eckzungen** liegen eine Materialstärke innen an Ober- und Unterwand, frei von Rückwand und Rahmen.
7. **Faltecken:** Der Falzring ist geschlossen (Kante Dreieck ↔ Nachbarwand fällt zusammen). Überlappung bei Z > Y wird gemeldet.
8. **Variantenspezifisch:** Zungengrösse, Widerhakenmass und Schneidbarkeit des Schlitzes, Steg hinter der Puzzlebucht, schneidbarer Hinterschnitt, Grenzen der Materialstärke.

Ergebnis einer Parameterreihe (X = Y = 60 mm, Z = 30 mm), kleinste Rahmenbreite **ohne Fehler**:

| Variante | t = 0.10 | t = 0.30 | t = 0.45 |
|---|---|---|---|
| A Windrad | 4 mm | 4 mm | 4 mm |
| B Webecke | 5.5 mm | 6 mm | 6.5 mm |
| C Puzzle | 4.5 mm | 4.5 mm | 5 mm |
| D Pfeil | 6.5 mm | 6.5 mm | 8 mm |
| E Faltecke | 4 mm | 4 mm | 4 mm |

Empfohlen sind w ≥ 8 mm, bei D w ≥ 10 mm. Erst dann werden die Verriegelungen gross genug, dass Toleranzen des Plotters nicht mehr dominieren.

## 5 Materialverbrauch und Verschnitt

**Nesting-Verfahren:** Der Zuschnitt wird gerastert (≈ 0.6–2.5 mm, konservativ um eine Zelle vergrössert plus Teileabstand). Daraus wird der gesamte Kollisionsraum berechnet, also alle Versätze, bei denen sich zwei Zuschnitte überlappen (exakt über Zeilenintervalle). Dann wird das dichteste Translationsgitter gesucht, in dem die Kreuze ineinandergreifen, und auf den Bogen gelegt. Anschliessend füllt ein Bottom-Left-Fill in 4 Drehlagen die Lücken auf. Zum Vergleich laufen reine Bottom-Left-Fills (zeilen- und spaltenweise, mit verschiedenen Drehlagen). Spaltenweise findet z. B. Zickzack-Reihen. Das beste Ergebnis gewinnt.

Referenz 60 × 80 × 35 mm, w = 10 mm, t = 0.3 mm, Bogen 305 × 305 mm, Abstand 2 mm:

| Variante | Fläche/Box | ohne Eckzungen | Ausnutzung des Umrissrechtecks | Stück/Bogen | Nutzung Rolle (Gitter) | Schnittlänge |
|---|---|---|---|---|---|---|
| A Windrad | 188 cm² | 173 cm² | 72 % | 2 | 87 % | 0.69 m |
| B Webecke | 188 cm² | 173 cm² | 72 % | 2 | 86 % | 0.71 m |
| C Puzzle | 187 cm² | 171 cm² | 72 % | 2 | 86 % | 0.73 m |
| D Pfeil | 187 cm² | 172 cm² | 73 % | 2 | 86 % | 0.73 m |
| E Faltecke | 223 cm² | – | 85 % | 2 | 88 % | 0.62 m |

Erkenntnisse:
- **A–D unterscheiden sich im Material um weniger als 1 %.** Die Wahl des Verschlusses ist also eine Frage der Funktion, nicht des Materials.
- **Eckzungen kosten 8–16 % Fläche.** Bei sehr kleinen Produkten oder steifem Karton kann man auf sie verzichten.
- **Die Faltecke (E)** füllt ihr Rechteck gut (85 %), braucht aber **+19 % (60×80×35) bis +48 % (40×40×40) Material**. Die höhere „Nutzung“ auf dem Bogen ist trügerisch: Massgeblich ist die Bogenfläche pro Box, und die ist bei gleicher Stückzahl identisch.
- **Ineinandergreifendes Gitter:** Auf Rollenware erreichen die Kreuze 85–88 % Nutzung statt 56–73 % im Rechteckraster.
- **Kleine Bögen** (A4, 12″-Matte) verlieren durch die Ränder 50–70 %. Der Generator zeigt je Format die Stückzahl. Grössere Bögen oder Boxmasse, die sich auf das Bogenformat abstimmen lassen, bringen hier am meisten.

## 6 Bewertung

| Kriterium | A Windrad | B Webecke | C Puzzle | D Pfeil | E Faltecke |
|---|---|---|---|---|---|
| Material & Verschnitt | ●●●●● | ●●●●● | ●●●●● | ●●●●● | ●●○○○ |
| Stabilität | ●●●○○ | ●●●●○ | ●●●○○ | ●●●●● | ●●●●○ |
| Einfache Montage | ●●●●○ | ●●○○○ | ●●●●○ | ●●●○○ | ●●○○○ |
| Zuverlässigkeit Verschluss | ●●●○○ | ●●●●○ | ●●●○○ | ●●●●● | ●●●○○ |
| Wiederverschliessbarkeit | ●●●●○ | ●●●○○ | ●●●○○ | ●●●○○ | ●●●●○ |
| Packpapier 0.1–0.15 mm | ●●●●● | ●●●●● | ●○○○○ | ●○○○○ … ●●●○○ | ●●●●● |
| Karton 0.3–0.45 mm | ●●●●○ … ●●●○○ | ●●●●○ … ●●○○○ | ●●●●● | ●●●●● | ●●○○○ |
| Ästhetik | ●●●●○ | ●●●●○ | ●●●●● | ●●●○○ | ●●●○○ |

*Material und Verschnitt sind berechnet. Die übrigen Zeilen sind konstruktive Einschätzungen und müssen am Prototyp bestätigt werden.*

**Begründungen:**
- *A:* Jede Lasche wird nur von ihrer Nachbarin gehalten, und das nur senkrecht zur Ebene. Kippt eine Wand nach aussen, sperrt in der Ebene nur die Reibung. Die letzte Zunge braucht biegsames Material, ideal also für Papier.
- *B:* Die Ecken sind unabhängig. Der Deckel lässt sich einzeln öffnen, ohne dass die unteren Ecken aufgehen. Dafür muss man an vier Stellen einfädeln.
- *C:* Die einzige Variante, die das Aufspreizen der Wände in der Rahmenebene formschlüssig verhindert, ohne den Rahmen zu durchstechen. Die Fuge wird zum Ornament. Senkrecht zur Ebene hält sie nur durch Klemmung, in dünnem Papier also unzuverlässig.
- *D:* Formschluss in allen Richtungen, die Konstruktion mit dem besten Halt. Die Schlitze sind sichtbar, und die Widerhaken nutzen sich beim Öffnen ab.
- *E:* Die Kanten sind dicht und die Ecken schubsteif. Dem stehen viel Mehrmaterial und mehrlagige Ecken gegenüber. Ob die Dreiecke ohne Kleber flach bleiben, ist offen.

**Empfehlung**
- **Packpapier / Kraftpapier:** **A Windrad** (oder B, falls der Deckel einzeln öffnen soll).
- **Karton 0.25–0.5 mm:** **D Pfeillasche** für maximale Sicherheit, **C Puzzle**, wenn die Konstruktion als Gestaltung sichtbar sein soll.
- Der Tab „Variantenvergleich“ rechnet die Empfehlung für die eingegebenen Masse und das gewählte Material neu (gewichtete Summe).

## 7 Was nur der physische Prototyp klärt

- Haltekraft der Zungen bzw. Pfeile gegen den Innendruck des Produkts. Kippen die Wände nach aussen (A, B)?
- Einrast- und Haltekraft der Puzzle-Knöpfe senkrecht zur Ebene. Passungsspiel je nach Messerbreite.
- Widerhaken: Einführbarkeit gegenüber Halt, Einreissen an den Schlitzenden (ggf. Entlastungslöcher), Verschleiss nach 10 Zyklen.
- Montierbarkeit der letzten Windradzunge bzw. der Webecken in steifem Karton.
- Faltecken: Bleiben sie ohne Kleber flach liegen?
- Rill- und Falzqualität am Plotter (Halbschnitt, Prägen, Perforation), Faserlaufrichtung und Rückfederung.
- Minimale schneidbare Details (Radien, Stege, Schlitzlängen): ein Testmuster schneiden.
- Massgenauigkeit: Die Falzzugabe t ist ein Modellansatz und muss mit dem echten Produkt kalibriert werden.

## 8 Hinweise zum Schneidplotter (z. B. Bambu Lab H2S)

- Das SVG ist im Massstab 1:1: `width`/`height` in mm, 1 Einheit im `viewBox` = 1 mm.
- Ebenen bzw. Farben: **rot = Schnitt**, **blau = Falz**, **grün = Info** (Bogenrand, vor dem Schneiden löschen oder ausblenden). In der Plotter-Software der blauen Ebene ein Rill-, Ritz- oder Stiftwerkzeug zuweisen. Falls keins verfügbar ist, im Generator „Perforation“ wählen: Die Falze werden dann als Strichschnitt ausgegeben (Länge und Steg einstellbar).
- Nutzbare Schneidfläche und unterstützte Werkzeuge des eigenen Geräts prüfen. Die Bogenvorgaben im Generator sind Startwerte.
- Schnittlinien sind zu Polylinien verkettet, damit der Plotter wenig absetzt.

## 9 Technik

Eine einzelne HTML-Datei ohne externe Bibliotheken. Der Geometriekern (`build`, `verify`, `nest`, SVG-Export) ist DOM-frei und lässt sich in Node testen:

```bash
# Kern aus der HTML-Datei extrahieren und testen
python3 -c "s=open('packaging/rahmenbox-generator.html').read();open('/tmp/core.js','w').write(s.split('<script>')[1].split('</script>')[0])"
node -e "const C=require('/tmp/core.js'); const O=C.build({variant:'haken',X:60,Y:80,Z:35,w:10,t:0.3,gsm:250,tuck:true}); console.log(C.verify(O).map(r=>r.lvl+' '+r.label).join('\n'))"
```

Die Einstellungen bleiben im Browser (`localStorage`) erhalten.
