# Engineering Decision Log

Status: **V** = vorgeschlagen · **F** = freigegeben · **Z** = zurückgezogen · **E** = ersetzt

Gescheiterte Ansätze werden hier nicht gelöscht, sondern mit Ursache als Z/E markiert.

| ID | Datum | Entscheid | Begründung | Annahmen | Status |
|---|---|---|---|---|---|
| D-001 | 2026-10-22 | Projektstruktur, Git, Python als einzige Berechnungsplattform (`calculations/hoverlib`), Parameter zentral in `parameters.py` | Keine parallelen Rechen-/CAD-Systeme; automatisierte Tests | – | V |
| D-002 | 2026-10-22 | Entwicklung als **bodengebundenes Luftkissenfahrzeug**, kein freier Flug | Freier Flug 23–75 kW vs. Luftkissen 0.2–1.5 kW (Rechnung Phase 0); Ausfall = Absetzen aus ≤ 5 cm | Massenbudget nominal, η-Annahmen | V |
| D-003 | 2026-10-22 | Vorläufiges Leitkonzept K5 (Schürzen-Kissen + separater Vortrieb), Option K5b | Gewichtete Matrix; Gierkontrolle im Stand, aktives Bremsen | Matrix nicht robust (K1 nur 2 Punkte dahinter) | V |
| D-004 | 2026-10-22 | Prüfstand A0 (unbemannt) in Phase 1 vorziehen | Konzeptentscheid hängt an 3 nicht berechenbaren Grössen | – | V (Freigabe nötig) |
| D-005 | 2026-10-22 | K3, K4, K6, K7 per Ausschlusskriterium verworfen | siehe `research/concept_comparison.md` | – | V |
| D-006 | 2026-10-22 | Board-Startgeometrie 800 × 500 mm, nicht verkleinern vor Messung | Kleinere Boards erhöhen Leistungsbedarf (P ∝ p^1.5·U) | Leckspalt unabhängig von Grösse | V |
| D-007 | 2026-10-22 | Primär tragende Struktur nicht aus FDM-Druck | Keine belastbaren Ermüdungskennwerte für gedruckte Teile in diesem Lastfall | – | V |
| D-008 | 2026-11-09 | Bibliothek aus 12 hybriden Mechanikmodulen (M01–M12) + Kalibriermodul M00 für H2S (FDM + 10-W-Laser + Schneidplotter), parametrisch in CadQuery/shapely (`cad/`) | Auftrag Fertigung; Module dienen Prüfstand A0 (M07–M12) und als wiederverwendbare Antriebs-/Führungsbausteine (M01–M06). Abweichung von `cad/parameters/README.md` (CAD erst nach G1/G2): betrifft nur Prüfstands- und Laborteile, nicht das Board | Gerätegrenzen nur aus Händlerangaben | V |
| D-009 | 2026-11-09 | Kerf-Kompensation in den Exportdateien, nicht im Slicer | eine Quelle (`fab.KERF`), Prüfungen rechnen mit kompensierter Geometrie; Doppelkompensation ausgeschlossen, wenn Bambu Studio Offset 0 | KERF 0.15 mm bis Messung M00-P01 | V |
| D-010 | 2026-11-09 | Laser-Serienmaterial 3 mm Lasersperrholz; 4 mm nur nach Test; > 4 mm gesperrt | Herstellerwert 5 mm (eine Quelle, Händler bis 6 mm) ohne Reserve; 3 mm schneidet sicher in 1 Durchgang | – | V |
| D-011 | 2026-11-09 | Positivliste je Verfahren; keine PVC-haltigen/unbekannten Kunststoffe im Laser; Folien (PET, Dichtpapier, Silikon) nur Plotter | Gesundheits- und Geräteschutz; 455 nm schneidet klares PET nicht | – | V |
| D-012 | 2026-11-09 | Keine Fertigungsfreigabe ohne Kalibrierlauf M00 am eigenen Gerät | Leistungsgrenzen Laser/Plotter sind nicht nachgewiesen (Anforderung 8) | – | V |
