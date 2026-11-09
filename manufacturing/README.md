# Fertigung – Bambu Lab H2S Laser Full Combo

**Druck-/Laserfertig für Bambu Studio:** [`jobs/JOBS.md`](jobs/JOBS.md) (5 Druckplatten .3mf, verschachtelte Laser-/Plotterbögen, Startparameter)

**Mechanikmodule M01–M12 (+ Kalibrierung M00):** [`modules/README.md`](modules/README.md) · Verfahrensgrenzen, Materialien, Freigabe: [`process_limits.md`](process_limits.md)

| Ordner | Inhalt |
|---|---|
| `3d_print/mXX/` | STEP + STL je FDM-Teil, in Druckorientierung |
| `laser_cut/mXX/` | DXF + SVG je Laserteil (Kerf-kompensiert) und verschachtelte Bögen `*_bogenN` |
| `plotter/mXX/` | DXF + SVG je Plotterteil und Bögen (Stiftlinien in Ebene `SCORE`) |
| `jobs/` | modulübergreifende Aufträge: Druckplatten `.3mf`, Laser-/Plotterbögen je Material |
| `modules/` | automatisch erzeugte Moduldokumentation, Prüfprotokolle, Vorschaubilder |


## Bekannte Eckdaten (Stand Phase 0 – aktualisiert in process_limits.md)

Aus Händler- und Fachpresseangaben, **noch nicht an der offiziellen Bambu-Lab-Spezifikation geprüft** (Aufgabe Phase 5):

| Merkmal | Wert | Quelle |
|---|---|---|
| Bauraum Druck | 340 × 320 × 340 mm | Bambu Lab Store, 3D Printing Industry |
| Hotend | bis 350 °C | Händlerangaben |
| Bauraumheizung | bis 65 °C (aktiv) | Händlerangaben |
| Laser | 10 W, 455 nm Diodenlaser | Händlerangaben |
| Max. Schnittstärke | 5 mm (Lindensperrholz) – nur eine Quelle | Händlerangabe, **unbestätigt** |

## Folgerungen für die Konstruktion

- Das Deck (800 × 500 mm) passt weder in den Druckraum noch (vermutlich) in die Laser-Arbeitsfläche → Deck aus Sperrholz mit Säge/CNC, oder segmentiert mit verschraubten Stössen (Festigkeitsnachweis nötig).
- Ein blauer Diodenlaser schneidet **kein transparentes Acryl** und keine Metalle; PVC und andere chlorhaltige Kunststoffe dürfen grundsätzlich nicht gelasert werden (Salzsäuredämpfe). Nur ausdrücklich freigegebene Materialien verwenden.
- Geeignete H2S-Teile (vorläufig): Gebläseadapter, Luftkanäle, Fingerschutzgitter, Motorhalter (nach Nachweis), Akkuhalter, Elektronikgehäuse, Kabelführungen, Schablonen, Messadapter, Blendenplatten (Laser, Sperrholz).
- Materialien: PETG (zäh, preiswert), ASA (UV-/temperaturbeständiger, Bauraumheizung vorhanden). Festigkeit gedruckter Teile ist richtungsabhängig – Kennwerte werden in Phase 5 an Probekörpern ermittelt, nicht aus Datenblättern übernommen.
