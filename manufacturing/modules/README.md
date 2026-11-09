# Mechanikmodule – Übersicht

> Automatisch erzeugt von `cad/build_all.py`. Parameter: `cad/mechlib/fab.py`, Materialien: `cad/mechlib/materials.py`, Verfahrensgrenzen: `manufacturing/process_limits.md`.

| Modul | Titel | FDM-Teile | Laserteile | Plotterteile | Prüfungen | Kosten ≈ CHF |
|---|---|---|---|---|---|---|
| [M00](m00.md) | Kalibrier- und Freigabecoupons | 1 | 4 | 1 | ✅ 24/24 | 4 |
| [M01](m01.md) | Systemplatte 290×190 mit 20-mm-Raster | 4 | 2 | 0 | ✅ 20/20 | 5 |
| [M02](m02.md) | Stirnradstufe i = 3 (z16/z48, m 1.5) | 16 | 2 | 0 | ✅ 42/42 | 12 |
| [M03](m03.md) | Linearschlitten in T-Nut mit Zahnstangenantrieb | 6 | 5 | 0 | ✅ 38/38 | 7 |
| [M04](m04.md) | Nockentrieb mit Gabel-Schwinghebel | 17 | 4 | 0 | ✅ 61/61 | 11 |
| [M05](m05.md) | Kniehebelspanner | 6 | 6 | 0 | ✅ 33/33 | 2 |
| [M06](m06.md) | Klinkengesperre (Rücklaufsperre) | 14 | 4 | 0 | ✅ 48/48 | 8 |
| [M07](m07.md) | Drosselklappe DN50 mit Winkelskala | 3 | 4 | 2 | ✅ 30/30 | 3 |
| [M08](m08.md) | Blendenmessstrecke DN50 mit Wechselblenden | 4 | 7 | 8 | ✅ 62/62 | 8 |
| [M09](m09.md) | Membran-Rückschlagventil DN50 | 3 | 0 | 4 | ✅ 27/27 | 2 |
| [M10](m10.md) | Fingerschutzgitter DN50 | 1 | 0 | 1 | ✅ 12/12 | 1 |
| [M11](m11.md) | Schürzen-Klemmleiste mit Exzenterspannern | 6 | 7 | 1 | ✅ 23/23 | 2 |
| [M12](m12.md) | U-Rohr-Manometertafel mit Nullpunktskala | 15 | 1 | 2 | ✅ 24/24 | 7 |

Summe M01–M12 ≈ CHF 68 (Richtwert; Filament, Sperrholz, Normteile; ohne Werkzeug/Strom).

## Aktuelle Fertigungsparameter

| Parameter | Wert | Status | Bedeutung |
|---|---|---|---|
| `PRINT_VOLUME_X` | 340 mm | SPEC | H2S Bauraum (Einzeldüse) |
| `PRINT_VOLUME_Y` | 320 mm | SPEC | H2S Bauraum |
| `PRINT_VOLUME_Z` | 340 mm | SPEC | H2S Bauraum |
| `NOZZLE` | 0.4 mm | RULE | Standarddüse 0.4 mm |
| `MIN_WALL` | 1.2 mm | RULE | >= 3 Perimeter bei 0.4 mm Düse |
| `CLR_SLIDE` | 0.2 mm | ANN | radiales Spiel Drehgelenk/Gleitsitz FDM-FDM bzw. FDM-Stahl |
| `CLR_LOOSE` | 0.3 mm | ANN | radiales Spiel Montage ohne Funktion |
| `PRESS_608` | 22.05 mm | ANN | Druckmass Bohrung für 608-Aussenring (Nenn 22.00), Presssitz |
| `HOLE_COMP` | 0.1 mm | ANN | Zuschlag auf Durchmesser senkrechter Bohrungen (FDM schrumpft innen) |
| `LASER_POWER` | 10 W | SPEC | Diodenlaser 455 nm |
| `LASER_AREA_X` | 310 mm | SPEC | Bearbeitungsfläche H2S (Quellen: 310x260 bzw. 310x270) |
| `LASER_AREA_Y` | 260 mm | SPEC | kleinerer der beiden Quellwerte verwendet |
| `LASER_MAX_CUT_SPEC` | 5 mm | SPEC | Lindensperrholz, 1 Durchgang – unbestätigt |
| `LASER_MAX_CUT_RULE` | 4 mm | RULE | Konstruktionsgrenze; Serienmaterial 3 mm |
| `PLY_T` | 3 mm | ANN | Laser-Sperrholz Pappel/Linde, NENNdicke – vor Export messen! |
| `KERF` | 0.15 mm | ANN | Schnittfugenbreite 3 mm Pappel (Kamm-Coupon m00) |
| `SLOT_CLR` | 0.05 mm | ANN | Zuschlag Steckschlitz für Schiebesitz Holz-Holz |
| `LASER_MIN_WEB` | 2 mm | RULE | min. Steg zwischen Schnitten (Verkohlung/Bruch) |
| `LASER_MARGIN` | 5 mm | RULE | Randabstand zur Bearbeitungsflächengrenze |
| `CUT_AREA_X` | 297.5 mm | SPEC | Schneidfläche H2S Cutting Module |
| `CUT_AREA_Y` | 300 mm | SPEC | Schneidfläche H2S Cutting Module |
| `CUT_MAX_T_SPEC` | 0.5 mm | SPEC | max. Materialdicke Messermodul |
| `CUT_FORCE_MAX` | 600 gf | SPEC | Messerdruck 50–600 gf |
| `CUT_MIN_FEATURE` | 3 mm | RULE | kleinster Lochdurchmesser/Steg (45°-Messer, Schleppversatz) |
| `CUT_MIN_RADIUS` | 0.8 mm | RULE | Innenecken verrunden (Schleppmesser reisst sonst) |
| `GEAR_BACKLASH` | 0.3 mm | ANN | Flankenspiel (Umfang) gedruckter Zahnräder, PETG, 0.4-Düse |
| `GEAR_CD_ADD` | 0.1 mm | ANN | Zuschlag Achsabstand für FDM-Masshaltigkeit |
