# Verfahrensgrenzen, Materialfreigaben und Fertigungsfreigabe – Bambu Lab H2S Laser Full Combo

Stand 2026-11-09. Zahlenwerte werden ausschliesslich in `cad/mechlib/fab.py` gepflegt; diese Seite erklärt Herkunft, Regeln und Freigabe.

> **Status: Keine Fertigungsfreigabe.** Alle Herstellerwerte stammen aus Händler- und Fachpresseangaben. Die offiziellen Bambu-Lab-Seiten (bambulab.com, wiki.bambulab.com) waren aus der Entwicklungsumgebung nicht abrufbar. Freigabe erst nach bestandenem Kalibrierlauf M00 auf dem eigenen Gerät mit der eigenen Materialcharge (Abschnitt 5).

## 1. Recherchierte Gerätewerte

| Merkmal | Wert | Quelle | Status |
|---|---|---|---|
| Druck-Bauraum | 340 × 320 × 340 mm | Bambu Lab Store / 3D Printing Industry (Phase 0) | Herstellerangabe, ungeprüft |
| Laser | 10 W Diode, 455 nm | mehrere Händler | Herstellerangabe, ungeprüft |
| Laser-Arbeitsfläche H2S | 310 × 260 mm (andere Quellen: 310 × 270) | Ultimate 3D Printing Store, 3D Labstore | **kleinerer Wert verwendet** |
| Max. Schnittdicke Laser | 5 mm Lindensperrholz, 1 Durchgang | 3D Printing Industry (H2S-Launch) | Herstellerangabe; Händler nennen teils 6 mm → nicht verwendet |
| Schnittgeschwindigkeit 10 W | 3 mm Linde ≈ 5 mm/s, 4 mm ≈ 4 mm/s, 6 mm ≈ 2 mm/s | Händlertabelle (Laser-Modul H2D/H2C) | Startwert für Matrix M00-P04 |
| Laser: Acryl | nur schwarzes/opakes Acryl bis 3 mm; transparentes Acryl nicht | Händlerangaben | im Projekt nicht verwendet |
| Schneidmodul-Fläche H2S | 297.5 × 300 mm (Zeichnen 300 × 255 mm) | Händler | Herstellerangabe, ungeprüft |
| Max. Materialdicke Schneidmodul | 0.5 mm | Bambu-Lab-Spezifikation **H2D** (Suchergebnis) | für H2S angenommen, prüfen |
| Messerdruck | 50–600 gf, Messer 45° × 0.35 mm | Bambu-Lab-Spezifikation **H2D** (Suchergebnis) | für H2S angenommen, prüfen |

Quellen: [3D Printing Industry – H2S Launch](https://3dprintingindustry.com/news/bambu-lab-launches-the-new-h2s-technical-specifications-and-pricing-243603/) · [Ultimate 3D Printing Store – H2S](https://ultimate3dprintingstore.com/products/bambu-lab-h2s-3d-printer) · [3D Labstore – H2S](https://3dlabstore.com.hk/3d-printers/bambulab/h2s-ams-2-pro-combo?lang=en) · [Bambu Lab H2D Tech Specs (es)](https://bambulab.com/es/h2d/tech-specs) · [Dynamism – Laser Module 10 W](https://www.dynamism.com/bambu-lab/bambu-lab-laser-module-10w.html)

## 2. Daraus abgeleitete Konstruktionsregeln (konservativ)

| Regel | Wert | Begründung |
|---|---|---|
| Laser-Serienmaterial | 3 mm Pappel-/Linden-Lasersperrholz | deutlich unter 5 mm Herstellergrenze → 1 Durchgang mit Reserve, weniger Verkohlung |
| Laser-Konstruktionsgrenze | 4 mm (nur nach Test M00-P04) | Reserve zu 5 mm; Leimfugen variieren je Charge |
| Laser-Nutzfläche | 300 × 250 mm | Arbeitsfläche minus 5 mm Rand |
| Kerf | 0.15 mm (Annahme) | wird an M00-P01 gemessen; **Kompensation steckt in den Dateien → in Bambu Studio keinen zusätzlichen Offset einstellen** |
| Mindeststeg Laser | 2 mm | Bruch und Durchbrand bei dünneren Stegen in 3-mm-Sperrholz |
| Plotter-Materialdicke | ≤ 0.5 mm | Herstellergrenze, keine Reserve möglich → 0.5-mm-Materialien nur nach Test |
| Kleinstes Plottermerkmal | Ø/Steg ≥ 3 mm, Innenecken R ≥ 0.8 mm | 45°-Schleppmesser hat Versatz, reisst in scharfen Innenecken |
| FDM-Wand | ≥ 1.2 mm (3 Linien à 0.4) | |
| FDM-Bohrungen | +0.10 mm auf Ø (senkrecht), waagrechte Bohrungen als Tropfen | FDM-Löcher schrumpfen; Tropfen druckt ohne Stützen |
| 608-Lagersitz | Ø 22.05 (Annahme) | M00-P05 Lochleiter 21.95–22.20 |
| Zahnräder FDM | Flankenspiel 0.30 mm, Achsabstand +0.10 mm | M02/M03-Prüfung rechnet mit diesen Werten kollisionsfrei |

Alle Regeln werden von `cad/build_all.py` für jedes Teil automatisch geprüft (Arbeitsfläche, Bauraum, Mindeststeg, Material, Dicke, Kollisionen in der Baugruppe).

## 3. Materialfreigaben (Positivliste)

Alles, was nicht in `cad/mechlib/materials.py` steht, ist für das jeweilige Verfahren **nicht freigegeben**.

| Verfahren | Freigegeben | Nur nach Testschnitt | Bemerkung |
|---|---|---|---|
| FDM | PETG, ASA, TPU 95A, PLA (nur Lehren) | – | ASA: Styrol → geschlossener Bauraum + Abluft/Filter |
| Laser | Lasersperrholz Pappel/Linde 3 mm (E1, laserfähiger Leim), Graukarton 1–2 mm unbeschichtet | Lasersperrholz 4 mm | Holzart und Leim vom Händler als „laser-geeignet“ deklariert |
| Plotter | Papier 120–160 g/m², Fotokarton ≤ 0.45 mm | PET-Folie 0.19 mm, Faserdichtungspapier 0.5 mm (chlorfrei deklariert), Silikonfolie 0.5 mm | Dicke immer mit Messschieber prüfen |

### Verbotene Materialien im Laser

| Material | Grund |
|---|---|
| PVC, Vinyl, Kunstleder | Chlorwasserstoff (HCl) – giftig, korrodiert Gerät |
| PTFE und andere fluorierte Kunststoffe | Fluorwasserstoff |
| Polycarbonat, ABS | giftige Dämpfe, Brand, schmilzt |
| PE-/PP-/PS-Schaum, HDPE | schmilzt und brennt tropfend |
| Glas-/Kohlefaser-Verbund | Faserstaub, Brand |
| chromgegerbtes Leder | Chrom(VI)-Verbindungen |
| transparentes Acryl, PET, Glas, Metall | 455 nm wird durchgelassen/reflektiert → kein Schnitt, Streulicht |
| unbekannte, beschichtete oder nicht deklarierte Platten (auch MDF unbekannter Herkunft) | Zusammensetzung unbekannt = nicht freigegeben |

Folien (PET, Dichtungspapier, Silikon) werden **nur geplottet**. Der Plotter arbeitet ohne Wärme; PVC-Folie wäre dort technisch schneidbar, wird im Projekt aber nicht verwendet (keine Dichtungen/Membranen aus PVC).

Quellen Laser-Verbotsliste: [Epilog – unsafe materials](https://www.epiloglaser.com/en-au/how-it-works/faq/laser-machine-unsafe-materials/) · [Bristol Hackspace](https://wiki.bristolhackspace.org/_export/xhtml/equipment/cnc/laser/materials) · [Protohaven Material Safety](https://wiki.protohaven.org/books/tool-guides/page/materials/revisions/1451) · [Emory TechLab](https://ats.emory.edu/sdl/student-resources/prohibited-laser-cutter-materials.html)

## 4. Sicherheit je Verfahren

| Verfahren | Gefährdung | Massnahme |
|---|---|---|
| Laser | Brand (Sperrholz, Karton) | nie unbeaufsichtigt; Flammensensor des Geräts nicht überbrücken; CO₂- oder Wasserlöscher griffbereit; Wabenbett/Krümelschublade nach jedem Job reinigen |
| Laser | Rauch, Feinstaub, Leimdämpfe | Abluft/Filter laut Hersteller in Betrieb; Klappe erst nach Nachlaufzeit öffnen |
| Laser | Augenschaden 455 nm | nur bei geschlossenem Gehäuse und intakten Sicherheitsschaltern; keine Manipulation |
| Plotter | Schnittverletzung | Messer nur mit Werkzeug wechseln, Messerhalter nicht in die Tasche |
| FDM | Verbrennung (Düse 230–260 °C, Bett), Emissionen | Abkühlen lassen; ASA nur mit Abluft/Filter |
| Montage | Pressen der 608-Lager | Schraubstock mit Zulage, nur Aussenring belasten, Schutzbrille |

## 5. Freigabeprozedur (vor Fertigung jedes Moduls)

1. **Material prüfen:** Dicke an 4 Stellen messen. Wenn die Sperrholzdicke von 3.0 mm abweicht: `PLY_T` in `fab.py` anpassen.
2. **M00-P04 Leistungs-/Geschwindigkeitsmatrix** (3 mm, dann ggf. 4 mm): Jedes Quadrat als eigenes Objekt mit der beschrifteten Leistung/Geschwindigkeit anlegen. Kriterium: Quadrat fällt ohne Nachhelfen heraus, Rückseite nicht verkohlt. Gewählt wird der schnellste Satz mit 20 % Leistungsreserve. Wenn bei 4 mm kein Satz besteht, bleibt `PLY4` gesperrt.
3. **M00-P01 Kerf-Kamm** (ohne Kompensation geschnitten): 9 Finger mit Messschieber messen, `KERF = 10.00 − Mittelwert`. Eintragen.
4. **M00-P02/P03 Schlitzleiter + Prüflasche:** Der schmalste Schlitz, der die Lasche von Hand saugend aufnimmt, bestimmt `SLOT_CLR`.
5. **M00-P05 FDM-Coupon (PETG):** Kleinste Bohrung, in die ein 608 mit Schraubstock gepresst werden kann und nicht herausfällt → `PRESS_608`. Bohrung, auf der eine Ø8-h9-Welle spielfrei, aber leicht dreht → `CLR_SLIDE`/`HOLE_COMP`.
6. **M00-P06 Plotter-Testmuster** je Plottermaterial: Messerdruck in 50-gf-Schritten erhöhen, bis Kontur und Ø3-Löcher sauber auslösen und die Trägermatte nur angeritzt ist. Wert pro Material notieren. Wenn ein Material bei 600 gf nicht durchtrennt wird, ist es für den Plotter nicht geeignet (Status bleibt TEST).
7. `python cad/build_all.py` → alle Exporte werden mit den gemessenen Werten neu erzeugt, und alle Prüfungen müssen ✅ zeigen.
8. Messwerte mit Datum, Materialcharge und Firmware-Stand in `testing/fertigung_kalibrierung.md` protokollieren. Erst dann gilt das Modul als **fertigungsfreigegeben (Gate G5)**.

## 6. Hinweise für Bambu Studio

- SVG/DXF sind in mm. Ebenen: `CUT` rot (durchschneiden), `ENGRAVE` blau (gravieren), `SCORE` grün (Plotter: Stift, Laser: anritzen).
- Pro Modul gibt es Einzelteildateien **und** einen fertig verschachtelten Bogen (`*_bogenN.svg`). Die Bögen enthalten alle Stückzahlen.
- Plotter: Erst Stift (`SCORE`), dann Messer (`CUT`), sonst verrutscht der ausgeschnittene Streifen.
- FDM: STEP/STL liegen bereits in Druckorientierung (Bettseite z = 0). Richtwerte PETG: 0.2 mm Schicht, 4 Wände, 40 % Gyroid. Zahnräder, Wellen und Exzenter mit 100 % Infill.
