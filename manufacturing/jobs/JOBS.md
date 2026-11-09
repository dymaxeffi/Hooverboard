# Fertigungsaufträge Bambu Lab H2S

> Automatisch erzeugt von `cad/jobs.py`. Ein vollständiger Satz aller Module M00–M12.

## Reihenfolge

1. **Kalibrierung zuerst:** Druckplatte 1, Laserbogen `laser_*_kalibrierung_*`, Plotterbogen `plotter_*_kalibrierung_*`. Auswerten nach `manufacturing/process_limits.md` §5, Werte in `cad/mechlib/fab.py` eintragen, dann `python cad/build_all.py && python cad/jobs.py` → alle folgenden Dateien sind auf dein Gerät abgestimmt.
2. Danach die Serienplatten und -bögen in beliebiger Reihenfolge.

## Druck (FDM) – Bambu Studio

Datei öffnen (Teile liegen bereits auf dem Bett und in Druckorientierung). Bei der Frage „Als einzelnes Objekt mit mehreren Teilen laden?“ **Nein** wählen. Drucker **Bambu Lab H2S, 0.4-mm-Düse**, Platte **Textured PEI**, Prozess **0.20mm Standard @BBL H2S**, dann die Profilwerte unten global setzen → *Slice* → *Drucken*.

| Profil | Filament | Wände | Füllung | Muster | Decke/Boden | Brim | Hinweis |
|---|---|---|---|---|---|---|---|
| kalibrierung | PETG | 4 | 40 % | Gyroid | 5/4 | aus | ZUERST drucken und messen (process_limits.md §5) – erst danach die anderen Platten. |
| standard | PETG | 4 | 40 % | Gyroid | 5/4 | auto | Funktionsteile allgemein. |
| voll | PETG | 5 | 100 % | Rectilinear | 6/5 | auto | Zahnräder, Nocken, Wellen, Stifte, Exzenter, Sperrrad – volle Füllung für Steifigkeit und Verschleiss. |
| tpu | TPU95A | 3 | 25 % | Gyroid | 4/4 | aus | Langsam (Profil „Bambu TPU 95A“), kein AMS-Durchlauf falls Hersteller abrät. |

Stützstrukturen: **aus** (alle Teile sind stützenfrei konstruiert: Tropfenbohrungen, 45°-Fasen).

| Nr | Datei | Profil | Filament | Teile | max. Höhe mm | Filament g | Inhalt |
|---|---|---|---|---|---|---|---|
| 1 | `druck/druck_01_kalibrierung_petg.3mf` | kalibrierung | PETG | 1 | 7 | ≈ 48 | M00-P05×1 |
| 2 | `druck/druck_02_standard_petg.3mf` | standard | PETG | 14 | 100 | ≈ 409 | M02-P02×4, M03-P07×1, M04-P02×2, M05-P04×1, M07-P01×1, M08-P01×2, M09-P01×1, M09-P04×1, M10-P01×1 |
| 3 | `druck/druck_03_standard_petg.3mf` | standard | PETG | 62 | 60 | ≈ 123 | M02-P05×2, M02-P06×2, M02-P07×4, M02-P08×1, M02-P09×1, M03-P04×1, M03-P05×1, M03-P08×1, M03-P09×1, M04-P05×1, M04-P06×1, M04-P08×1, M04-P09×2, M04-P10×1, M04-P11×1, M04-P12×4, M04-P13×1, M04-P14×1, M05-P05×2, M06-P02×2, M06-P05×1, M06-P06×2, M06-P07×1, M06-P08×1, M06-P09×4, M06-P10×1, M06-P11×1, M07-P06×1, M09-P03×1, M11-P02×3, M12-P02×7, M12-P03×4, M12-P05×4 |
| 4 | `druck/druck_04_voll_petg.3mf` | voll | PETG | 14 | 93 | ≈ 148 | M02-P03×1, M02-P04×1, M03-P06×1, M04-P03×1, M04-P07×1, M05-P07×2, M06-P03×1, M07-P02×1, M08-P02×2, M11-P04×3 |
| 5 | `druck/druck_05_tpu_tpu95a.3mf` | tpu | TPU95A | 5 | 10 | ≈ 9 | M01-P03×4, M05-P06×1 |

Filament gesamt ≈ 738 g (Schätzung aus Volumen, ANN).

## Laser und Schneidplotter

Bögen sind modulübergreifend verschachtelt und passen in die Arbeitsfläche (Laser 300 × 250 mm, Plotter 287 × 290 mm). Import als SVG (mm) in die Laser-/Schneidfunktion der Bambu-Software. Ebenen: **rot CUT** = durchschneiden, **blau ENGRAVE** = gravieren, **grün SCORE** = Stift (Plotter). Schnittfuge ist in den Konturen kompensiert → in der Software **keinen Kerf-Offset** einstellen. Teile mit Gravur: erst gravieren, dann schneiden.

### Startparameter Laser 10 W (bis zur eigenen Matrix M00-P04)

| Material | Vorgang | Leistung | Geschwindigkeit | Durchgänge | Quelle |
|---|---|---|---|---|---|
| Pappel/Linde 3 mm | Schneiden | 100 % | 5 mm/s | 1 | Händlertabelle 10 W (3 mm Linde 5 mm/s), **ungeprüft** |
| Pappel/Linde 3 mm | Gravieren | 20–30 % | 200–300 mm/s | 1 | Erfahrungswert, Matrix bestätigen |
| Pappel/Linde 4 mm | Schneiden | 100 % | 4 mm/s | 1 | nur nach bestandener Matrix (PLY4 = TEST) |

Sicherheit: nie unbeaufsichtigt, Abluft an, Feuerlöscher bereit, nur Materialien aus der Positivliste.

### Plotter

Messerdruck je Material mit dem Testmuster M00-P06 ermitteln (in 50-gf-Schritten). Folien auf Trägermatte; bei Bögen mit SCORE-Ebene zuerst Stift, dann Messer.

| Datei | Material | Gruppe | Teile |
|---|---|---|---|
| `laser/laser_ply3_kalibrierung_01.svg` | Laser-Sperrholz Pappel/Linde 3 mm (E1, laserfähiger Leim) (FREI) | kalibrierung | M00-P01×1, M00-P02×1, M00-P03×1, M00-P04×1 |
| `laser/laser_ply3_serie_01.svg` | Laser-Sperrholz Pappel/Linde 3 mm (E1, laserfähiger Leim) (FREI) | serie | M12-P01×1 |
| `laser/laser_ply3_serie_02.svg` | Laser-Sperrholz Pappel/Linde 3 mm (E1, laserfähiger Leim) (FREI) | serie | M01-P01×1 |
| `laser/laser_ply3_serie_03.svg` | Laser-Sperrholz Pappel/Linde 3 mm (E1, laserfähiger Leim) (FREI) | serie | M01-P02×1 |
| `laser/laser_ply3_serie_04.svg` | Laser-Sperrholz Pappel/Linde 3 mm (E1, laserfähiger Leim) (FREI) | serie | M04-P01×2, M06-P01×2 |
| `laser/laser_ply3_serie_05.svg` | Laser-Sperrholz Pappel/Linde 3 mm (E1, laserfähiger Leim) (FREI) | serie | M05-P02×2, M08-P03a×1, M08-P03b×1, M08-P03c×1, M08-P03d×1, M08-P03e×1 |
| `laser/laser_ply3_serie_06.svg` | Laser-Sperrholz Pappel/Linde 3 mm (E1, laserfähiger Leim) (FREI) | serie | M02-P01×2, M08-P03f×1, M08-P06×1 |
| `laser/laser_ply3_serie_07.svg` | Laser-Sperrholz Pappel/Linde 3 mm (E1, laserfähiger Leim) (FREI) | serie | M03-P01×1, M05-P01×2, M05-P03×2, M07-P03×1, M07-P04×1, M11-P01×1, M11-P03×6 |
| `laser/laser_ply3_serie_08.svg` | Laser-Sperrholz Pappel/Linde 3 mm (E1, laserfähiger Leim) (FREI) | serie | M03-P02×2, M03-P03×2, M04-P04×2, M06-P04×2, M07-P05×2 |
| `plotter/plotter_card05_kalibrierung_01.svg` | Fotokarton ≤ 0.5 mm (300 g/m²) (FREI) | kalibrierung | M00-P06×1 |
| `plotter/plotter_card05_serie_01.svg` | Fotokarton ≤ 0.5 mm (300 g/m²) (FREI) | serie | M11-P05×1, M12-P04×2 |
| `plotter/plotter_gasket05_serie_01.svg` | Faserdichtungspapier 0.5 mm, Zellulose/NBR-frei, chlorfrei deklariert (TEST) | serie | M07-P07×2, M08-P05×2, M09-P05×1, M09-P06×2, M10-P02×1 |
| `plotter/plotter_pet019_serie_01.svg` | PET-Folie 0.19 mm (PET-A/PET-G, klar, als PET deklariert) (TEST) | serie | M08-P04a×1, M08-P04b×1, M08-P04c×1, M08-P04d×1, M08-P04e×1, M08-P04f×1, M09-P02×1 |
