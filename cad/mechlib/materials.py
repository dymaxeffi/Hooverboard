"""Materialfreigaben je Verfahren (Positivliste). Alles, was hier nicht steht, ist
fuer das jeweilige Verfahren NICHT freigegeben – insbesondere unbekannte Kunststoffe."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Material:
    key: str
    name: str
    process: str          # fdm | laser | plotter
    thickness: float | None
    status: str           # FREI = freigegeben, TEST = nur nach bestandenem Testcoupon
    hazards: str
    cost_note: str


MATERIALS = {m.key: m for m in [
    # ---------------- FDM
    Material("PETG", "PETG (Markenfilament mit Datenblatt)", "fdm", None, "FREI",
             "Düse 230–250 °C; Raumlüftung; keine Lebensmittelfreigabe", "≈ 20 CHF/kg"),
    Material("ASA", "ASA", "fdm", None, "FREI",
             "Styrol-Emissionen: geschlossener Bauraum + Abluft/Filter, nicht im Wohnraum ohne Lüftung", "≈ 25 CHF/kg"),
    Material("TPU95A", "TPU 95A", "fdm", None, "FREI", "langsam drucken; Raumlüftung", "≈ 30 CHF/kg"),
    Material("PLA", "PLA", "fdm", None, "FREI", "nur Lehren/Schablonen; erweicht ab ≈ 55 °C", "≈ 18 CHF/kg"),
    # ---------------- Laser (10 W Diode, 455 nm)
    Material("PLY3", "Laser-Sperrholz Pappel/Linde 3 mm (E1, laserfähiger Leim)", "laser", 3.0, "FREI",
             "Rauch/Funken: Abluft an, nie unbeaufsichtigt, Feuerlöscher bereit, Wabenbett sauber",
             "≈ 15 CHF/m² (ANN)"),
    Material("PLY4", "Laser-Sperrholz Pappel/Linde 4 mm", "laser", 4.0, "TEST",
             "wie PLY3; Mehrfachdurchgang erhöht Brandrisiko", "≈ 18 CHF/m² (ANN)"),
    Material("CARD_L", "Graukarton 1–2 mm (ohne Beschichtung)", "laser", 1.5, "FREI",
             "leicht entflammbar: Luftunterstützung, Aufsicht", "≈ 8 CHF/m²"),
    # ---------------- Plotter (Cutting Module, max. 0.5 mm)
    Material("PAPER160", "Papier 120–160 g/m²", "plotter", 0.2, "FREI", "keine", "≈ 0.10 CHF/Bogen"),
    Material("CARD05", "Fotokarton ≤ 0.5 mm (300 g/m²)", "plotter", 0.45, "FREI", "keine", "≈ 0.50 CHF/Bogen"),
    Material("PET019", "PET-Folie 0.19 mm (PET-A/PET-G, klar, als PET deklariert)", "plotter", 0.19, "TEST",
             "nie lasern (455 nm schneidet klares PET nicht, Schmelze)", "≈ 1 CHF/A4"),
    Material("GASKET05", "Faserdichtungspapier 0.5 mm, Zellulose/NBR-frei, chlorfrei deklariert", "plotter", 0.5,
             "TEST", "nur Luft ≤ 60 °C; an Grenze der Plotterdicke", "≈ 3 CHF/A4"),
    Material("SIL05", "Silikonfolie 0.5 mm, Shore A 40–60", "plotter", 0.5, "TEST",
             "Schleppmesser verzieht weiches Material: Trägerfolie verwenden", "≈ 4 CHF/A4"),
]}

LASER_FORBIDDEN = [
    ("PVC / Vinyl / Kunstleder", "Chlorwasserstoff (HCl) – giftig, zerstört Optik und Mechanik"),
    ("PTFE / fluorierte Kunststoffe", "Fluorwasserstoff, Perfluorverbindungen"),
    ("Polycarbonat (PC, Makrolon)", "brennt, verfärbt, giftige Dämpfe"),
    ("ABS", "Blausäure/Styrol, schmilzt statt zu schneiden"),
    ("PE-/PP-/PS-Schaum, HDPE", "schmilzt, brennt tropfend"),
    ("Glas-/Kohlefaser-Verbund, Epoxid", "Faserstaub, Brand"),
    ("chromgegerbtes Leder", "Chrom(VI)-Verbindungen"),
    ("transparentes Acryl, PET, Glas, Metalle", "455-nm-Diode transmittiert/reflektiert – kein Schnitt, Streulicht"),
    ("unbekannte Kunststoffe, beschichtete Platten, MDF unbekannter Herkunft", "nicht deklariert = nicht freigegeben"),
]


def check_material(key: str, process: str, thickness: float | None = None) -> list[str]:
    from . import fab
    m = MATERIALS.get(key)
    if m is None:
        return [f"Material {key} nicht in Positivliste"]
    issues = []
    if m.process != process:
        issues.append(f"{key} ist für {m.process}, nicht für {process} freigegeben")
    t = thickness if thickness is not None else m.thickness
    if process == "laser" and t is not None and t > fab.LASER_MAX_CUT_RULE.value:
        issues.append(f"{key}: {t} mm > Laser-Konstruktionsgrenze {fab.LASER_MAX_CUT_RULE.value} mm")
    if process == "plotter" and t is not None and t > fab.CUT_MAX_T_SPEC.value:
        issues.append(f"{key}: {t} mm > Plotter-Grenze {fab.CUT_MAX_T_SPEC.value} mm")
    return issues
