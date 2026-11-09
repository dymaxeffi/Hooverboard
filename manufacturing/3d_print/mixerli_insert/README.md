# Mixerli v2.0 Insert und Hülsen – Druckvorlagen für Bambu Lab H2S

Einsatzplatte für das Gehäuse des Miniverstärkers: Grundplatte 125,6 × 107,6 × 1,6 mm,
Rahmen bis 2,6 mm, vier Dome ⌀ 8,8 mm × 10,4 mm hoch mit M4-Bohrung.
Dazu vier Distanzhülsen M4: außen ⌀ 7,5 mm, innen ⌀ 4,4 mm, 11,8 mm lang.

## Dateien

| Datei | Variante | Prozess |
|---|---|---|
| `mixerli_v2.0_insert_M4_through_H2S_PETG.3mf` | M4-Durchgangsloch ⌀ 4,4 mm | 0.20mm Standard @BBL H2S |
| `mixerli_v2.0_insert_M4_thread_H2S_PETG.3mf` | M4-Gewinde modelliert (Kern ⌀ 3,4 / außen ⌀ 4,7 mm, mit Druckspiel) | 0.12mm High Quality @BBL H2S (feinere Schichten für das Gewinde) |
| `mixerli_v2.0_sleeves_M4_H2S_PETG.3mf` | 4 Distanzhülsen M4, stehend, je ein eigenes Objekt (2 × 2, 20-mm-Raster) | 0.20mm Standard @BBL H2S |
| `stl/` | Original-STL | – |
| `build_3mf.py` | erzeugt die .3mf neu | – |

## Voreinstellungen (in beiden Projekten)

- Drucker: **Bambu Lab H2S, 0.4-mm-Düse**
- Filament: **Bambu PETG HF** (245 °C Düse, 70 °C Bett)
- Druckplatte: **Textured PEI Plate**
- Lage: flach auf der Unterseite, Bettmitte – **keine Stützen nötig**
- Abweichungen vom Systemprofil: **4 Wandlinien** (Dome praktisch massiv), **25 % Füllung**

Alle anderen Werte kommen aus dem Bambu-Systemprofil.

## Drucken

1. `.3mf` in Bambu Studio öffnen (Frage nach Projekteinstellungen mit **Ja** übernehmen).
2. Im Filamentfeld das tatsächlich geladene AMS-Fach zuordnen.
3. **Plate slicen** → Vorschau kurz prüfen → **Drucken**.

Grobe Schätzung ohne Slicer: Insert ca. 22–25 g, Hülsen zusammen ca. 2 g PETG. Die genaue Druckzeit zeigt Bambu Studio nach dem Slicen.

## Hinweise

- **Hülsen:** stehen aufrecht, keine Stützen. Bei 1,55 mm Wandstärke druckt der Slicer sie praktisch massiv.
  Bambu Studio verlangsamt kleine Schichten automatisch, damit PETG abkühlt.

- **Welche Variante?** Für häufiges Öffnen: Durchgangsloch + Mutter oder Gewindeeinsatz.
  Das gedruckte Gewinde reicht für wenige Montagen; Schraube beim ersten Mal langsam eindrehen,
  bei Bedarf mit M4-Gewindebohrer nachschneiden.
- **Wärme:** PETG hält bis ca. 70 °C. Wird es im Gehäuse wärmer (Endstufe, Kühlkörper),
  in Bambu Studio auf **Bambu ASA @BBL H2S** wechseln.
- In der Gewinde-STL waren 62 leere Restflächen (Fläche 0) aus dem CAD-Export; `build_3mf.py` entfernt sie.
  Das Bauteil selbst ist geschlossen und unverändert.
- Die Projekte sind **nicht vorgesliced** (in der Build-Umgebung lief kein Bambu Studio).
  Slicen dauert in Bambu Studio wenige Sekunden.

## Neu erzeugen

```bash
pip install trimesh numpy networkx scipy matplotlib
git clone --depth 1 --filter=blob:none --sparse https://github.com/bambulab/BambuStudio
git -C BambuStudio sparse-checkout set resources/profiles/BBL
python build_3mf.py BambuStudio/resources/profiles/BBL
```
