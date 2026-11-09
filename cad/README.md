# CAD – parametrische Mechanikmodule (CadQuery + shapely)

Zwölf Funktionsmodule (M01–M12) und ein Kalibriermodul (M00) für den Bambu Lab H2S Laser Full Combo, kombiniert aus FDM-Druck, 10-W-Laser und Schneidplotter. Übersicht, Teilelisten und Prüfprotokolle: `manufacturing/modules/README.md`.

```bash
pip install cadquery shapely ezdxf matplotlib pytest
python cad/build_all.py          # prüfen + alle Dateien erzeugen (~40 s)
python cad/build_all.py --check  # nur prüfen
python cad/render_previews.py    # Vorschaubilder manufacturing/modules/img/
python -m pytest                 # inkl. tests/test_cad_modules.py
```

## Aufbau

| Pfad | Inhalt |
|---|---|
| `mechlib/fab.py` | **einzige Quelle** aller Fertigungsparameter (Kerf, Spiele, Gerätegrenzen) mit Status SPEC/ANN/RULE |
| `mechlib/materials.py` | Material-Positivliste je Verfahren, Laser-Verbotsliste, Prüffunktion |
| `mechlib/geom2d.py` | 2D-Konstruktion (shapely), Kerf-Kompensation, Mindeststeg-Prüfung, DXF/SVG, Gravurtext, Nesting |
| `mechlib/gears.py` | Evolventenräder und Zahnstangen |
| `mechlib/cadbridge.py` | 2D → CadQuery-Solid, starre Transformationen, Tropfenbohrungen |
| `mechlib/common.py` | Standardelemente: Lagerflansch 608, Winkelfuss, Seitenschild, Zahnrad-/Nockennabe, Kurbel |
| `mechlib/airline.py` | Flanschstandard DN50 (M07–M10), Messstutzen |
| `mechlib/module.py` | Teil/Modul-Modell, Prüfungen (Bauraum, Arbeitsfläche, Steg, Material, Kollision), Export |
| `models/mXX_*.py` | je Modul eine `build()`-Funktion; modulspezifische Funktionsprüfungen (Zahneingriff, Kinematik, …) |
| `assemblies/` | Baugruppen als `.glb` (versioniert) und `.step` (lokal erzeugt, gitignored) |

## Konventionen

- Masse in mm. Baugruppe: z nach oben, Oberseite Systemplatte M01 = z 0, 20-mm-Raster.
- **Laser-/Plotterteile** werden als Nennkontur konstruiert. Der Export kompensiert die Schnittfuge (Aussenkontur +kerf/2, Löcher −kerf/2). In Bambu Studio daher **keinen** Kerf-Offset einstellen.
- **FDM-Teile** werden in Druckorientierung erzeugt (Bettseite z = 0); `poses` legen sie in die Baugruppe.
- Jedes Teil trägt eine Begründung der Verfahrenswahl (`rationale`), die in die Moduldoku übernommen wird.
- Nach jeder Änderung an `fab.py` alles neu erzeugen; die Prüfungen schlagen fehl, wenn eine Regel verletzt wird.
