"""Fertigungsaufträge für Bambu Studio / H2S: Druckplatten (.3mf) und Laser-/Plotterbögen
modulübergreifend, gruppiert nach Material und Einstellungsprofil.

    python cad/jobs.py

Ergebnis: manufacturing/jobs/ (siehe JOBS.md dort). Die 3MF-Dateien enthalten Geometrie in
Druckorientierung, bereits auf dem Bett angeordnet. Slicen erfolgt in Bambu Studio mit den
im Dateinamen/JOBS.md genannten Profilen (kein G-Code: Düse, Filament und Firmware sind
gerätespezifisch und hier nicht verifizierbar).
"""

from __future__ import annotations

import importlib
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from build_all import MODULES  # noqa: E402
from mechlib import fab, geom2d as g2  # noqa: E402
from mechlib.materials import MATERIALS  # noqa: E402
from mechlib.module import DENSITY, ROOT, slug  # noqa: E402

OUT = ROOT / "manufacturing" / "jobs"
BED_X, BED_Y = fab.PRINT_VOLUME_X.value - 20, fab.PRINT_VOLUME_Y.value - 20   # 10 mm Rand
GAP = 6.0

# Einstellungsprofile (Bambu Studio, Prozess „0.20mm Standard @BBL H2S“ als Basis)
PROFILES = {
    "kalibrierung": dict(mat="PETG", walls=4, infill=40, pattern="Gyroid", top=5, bottom=4, brim="aus",
                         note="ZUERST drucken und messen (process_limits.md §5) – erst danach die anderen Platten."),
    "standard": dict(mat="PETG", walls=4, infill=40, pattern="Gyroid", top=5, bottom=4, brim="auto",
                     note="Funktionsteile allgemein."),
    "voll": dict(mat="PETG", walls=5, infill=100, pattern="Rectilinear", top=6, bottom=5, brim="auto",
                 note="Zahnräder, Nocken, Wellen, Stifte, Exzenter, Sperrrad – volle Füllung für Steifigkeit und Verschleiss."),
    "tpu": dict(mat="TPU95A", walls=3, infill=25, pattern="Gyroid", top=4, bottom=4, brim="aus",
                note="Langsam (Profil „Bambu TPU 95A“), kein AMS-Durchlauf falls Hersteller abrät."),
}
VOLL = {"M02-P03", "M02-P04", "M03-P06", "M04-P03", "M04-P07", "M05-P07", "M06-P03", "M07-P02", "M08-P02", "M11-P04"}
FILL = {"standard": 0.65, "kalibrierung": 0.65, "voll": 1.0, "tpu": 0.5}


def profile_of(p):
    if p.material == "TPU95A":
        return "tpu"
    if p.pid.startswith("M00"):
        return "kalibrierung"
    return "voll" if p.pid in VOLL else "standard"


@dataclass
class Item:
    pid: str
    name: str
    shape: object
    w: float
    d: float
    rot: bool = False
    x: float = 0.0
    y: float = 0.0


def collect():
    fdm, flat = {}, {}
    for name in MODULES:
        mod = importlib.import_module(f"models.{name}").build()
        for p in mod.parts:
            if p.qty == 0:
                continue
            if p.process == "fdm":
                s = p.solid()
                bb = s.val().BoundingBox()
                s = s.translate((-bb.xmin, -bb.ymin, -bb.zmin))
                for k in range(p.qty):
                    fdm.setdefault(profile_of(p), []).append(Item(p.pid, p.name, s, bb.xlen, bb.ylen))
            else:
                for k in range(p.qty):
                    flat.setdefault((p.process, p.material), []).append(p)
    return fdm, flat


def pack(items):
    """Regalpacking auf das Bett, grösste Teile zuerst; dreht um 90°, wenn nötig/günstiger."""
    items = sorted(items, key=lambda i: -max(i.w, i.d) * min(i.w, i.d))
    plates, cur, x, y, row = [], [], 0.0, 0.0, 0.0
    for it in items:
        if it.w < it.d and it.d <= BED_X:          # lange Seite in x
            it.rot, it.w, it.d = True, it.d, it.w
        if it.w > BED_X or it.d > BED_Y:
            raise ValueError(f"{it.pid} passt nicht aufs Bett")
        if x + it.w > BED_X:
            x, y, row = 0.0, y + row + GAP, 0.0
        if y + it.d > BED_Y:
            plates.append(cur)
            cur, x, y, row = [], 0.0, 0.0, 0.0
        it.x, it.y = x, y
        cur.append(it)
        x += it.w + GAP
        row = max(row, it.d)
    if cur:
        plates.append(cur)
    return plates


def mesh(item):
    s = item.shape
    if item.rot:
        s = s.rotate((0, 0, 0), (0, 0, 1), 90)
        bb = s.val().BoundingBox()
        s = s.translate((-bb.xmin, -bb.ymin, 0))
    off = (10 + item.x + (fab.PRINT_VOLUME_X.value - 20 - BED_X) / 2, 10 + item.y, 0)
    verts, idx, tris = [], {}, []
    for v in s.vals():
        vs, fs = v.tessellate(0.02, 0.2)
        local = []
        for q in vs:
            key = (round(q.x + off[0], 4), round(q.y + off[1], 4), round(q.z, 4))
            if key not in idx:
                idx[key] = len(verts)
                verts.append(key)
            local.append(idx[key])
        for f in fs:
            t = (local[f[0]], local[f[1]], local[f[2]])
            if len(set(t)) == 3:
                tris.append(t)
    from collections import Counter
    edges = Counter(tuple(sorted(e)) for a, b, c in tris for e in ((a, b), (b, c), (c, a)))
    open_edges = sum(1 for n in edges.values() if n != 2)
    if open_edges:
        raise ValueError(f"{item.pid}: Netz nicht geschlossen ({open_edges} offene Kanten)")
    return verts, tris


def write_3mf(path: Path, plate, title):
    objs, build = [], []
    for i, it in enumerate(plate, 1):
        v, t = mesh(it)
        vx = "".join(f'<vertex x="{a}" y="{b}" z="{c}"/>' for a, b, c in v)
        tx = "".join(f'<triangle v1="{a}" v2="{b}" v3="{c}"/>' for a, b, c in t)
        objs.append(f'<object id="{i}" name="{it.pid} {it.name}" type="model"><mesh><vertices>{vx}</vertices>'
                    f'<triangles>{tx}</triangles></mesh></object>')
        build.append(f'<item objectid="{i}"/>')
    model = ('<?xml version="1.0" encoding="UTF-8"?>\n<model unit="millimeter" xml:lang="de-CH" '
             'xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02">'
             f'<metadata name="Title">{title}</metadata><metadata name="Designer">HOVERBOARD MINI cad/jobs.py</metadata>'
             f'<resources>{"".join(objs)}</resources><build>{"".join(build)}</build></model>')
    ct = ('<?xml version="1.0" encoding="UTF-8"?>\n<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
          '<Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
    rels = ('<?xml version="1.0" encoding="UTF-8"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Target="/3D/3dmodel.model" Id="rel0" '
            'Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", ct)
        z.writestr("_rels/.rels", rels)
        z.writestr("3D/3dmodel.model", model)


def main():
    fdm, flat = collect()
    lines_fdm, n = [], 0
    order = ["kalibrierung", "standard", "voll", "tpu"]
    total_g = 0.0
    for prof in order:
        for k, plate in enumerate(pack(fdm.get(prof, [])), 1):
            n += 1
            pr = PROFILES[prof]
            fname = f"druck_{n:02d}_{prof}_{pr['mat'].lower()}.3mf"
            write_3mf(OUT / "druck" / fname, plate, fname)
            g = sum(it.shape.val().Volume() for it in plate) / 1000 * DENSITY[pr["mat"]] * FILL[prof]
            total_g += g
            hmax = max(it.shape.val().BoundingBox().zlen for it in plate)
            parts = ", ".join(sorted({f"{it.pid}×{sum(1 for j in plate if j.pid == it.pid)}" for it in plate}))
            lines_fdm.append(f"| {n} | `druck/{fname}` | {prof} | {pr['mat']} | {len(plate)} | {hmax:.0f} | ≈ {g:.0f} | {parts} |")

    # Laser/Plotter: modulübergreifend je Material verschachteln
    lines_flat = []
    for (proc, mat), parts in sorted(flat.items()):
        if proc == "laser":
            aw = fab.LASER_AREA_X.value - 2 * fab.LASER_MARGIN.value
            ah = fab.LASER_AREA_Y.value - 2 * fab.LASER_MARGIN.value
        else:
            aw, ah = fab.CUT_AREA_X.value - 10, fab.CUT_AREA_Y.value - 10
        cal = [p for p in parts if p.pid.startswith("M00")]
        rest = [p for p in parts if not p.pid.startswith("M00")]
        for tag, group in (("kalibrierung", cal), ("serie", rest)):
            if not group:
                continue
            items = [((p.pid, i), p.cut_geometry().envelope) for i, p in enumerate(group)]
            lookup = {(p.pid, i): p for i, p in enumerate(group)}
            for si, sheet in enumerate(g2.shelf_nest(items, aw, ah), 1):
                from shapely import affinity
                cut, eng = [], []
                for key, env in sheet:
                    p = lookup[key]
                    geo, en = p.cut_geometry(), p.engrave
                    pe = p.cut_geometry().envelope
                    if abs((pe.bounds[2] - pe.bounds[0]) - (env.bounds[2] - env.bounds[0])) > 1e-6:
                        geo = affinity.rotate(geo, 90, origin=(0, 0))
                        en = affinity.rotate(en, 90, origin=(0, 0)) if en is not None else None
                        cl = affinity.rotate(p.cut_lines, 90, origin=(0, 0)) if p.cut_lines is not None else None
                    else:
                        cl = p.cut_lines
                    dx, dy = env.bounds[0] - geo.bounds[0], env.bounds[1] - geo.bounds[1]
                    cut.append(affinity.translate(geo, dx, dy))
                    if cl is not None:
                        cut.append(affinity.translate(cl, dx, dy))
                    if en is not None:
                        eng.append(affinity.translate(en, dx, dy))
                from shapely.geometry import GeometryCollection
                layers = {"CUT": GeometryCollection(cut)}
                if eng:
                    layers["ENGRAVE" if proc == "laser" else "SCORE"] = GeometryCollection(eng)
                folder = "laser" if proc == "laser" else "plotter"
                stem = f"{folder}_{slug(mat)}_{tag}_{si:02d}"
                g2.export_svg(layers, OUT / folder / f"{stem}.svg", title=stem)
                g2.export_dxf(layers, OUT / folder / f"{stem}.dxf")
                ids = ", ".join(sorted({f"{k[0]}×{sum(1 for kk, _ in sheet if kk[0] == k[0])}" for k, _ in sheet}))
                lines_flat.append(f"| `{folder}/{stem}.svg` | {MATERIALS[mat].name} ({MATERIALS[mat].status}) | {tag} | {ids} |")
    write_md(lines_fdm, lines_flat, total_g)
    print(f"{n} Druckplatten, {len(lines_flat)} Laser-/Plotterbögen, Filament ≈ {total_g:.0f} g → {OUT}")


def write_md(lines_fdm, lines_flat, total_g):
    L = ["# Fertigungsaufträge Bambu Lab H2S", "",
         "> Automatisch erzeugt von `cad/jobs.py`. Ein vollständiger Satz aller Module M00–M12.", "",
         "## Reihenfolge", "",
         "1. **Kalibrierung zuerst:** Druckplatte 1, Laserbogen `laser_*_kalibrierung_*`, Plotterbogen `plotter_*_kalibrierung_*`. "
         "Auswerten nach `manufacturing/process_limits.md` §5, Werte in `cad/mechlib/fab.py` eintragen, dann "
         "`python cad/build_all.py && python cad/jobs.py` → alle folgenden Dateien sind auf dein Gerät abgestimmt.",
         "2. Danach die Serienplatten und -bögen in beliebiger Reihenfolge.", "",
         "## Druck (FDM) – Bambu Studio", "",
         "Datei öffnen (Teile liegen bereits auf dem Bett und in Druckorientierung). Bei der Frage „Als einzelnes Objekt mit "
         "mehreren Teilen laden?“ **Nein** wählen. Drucker **Bambu Lab H2S, 0.4-mm-Düse**, Platte **Textured PEI**, "
         "Prozess **0.20mm Standard @BBL H2S**, dann die Profilwerte unten global setzen → *Slice* → *Drucken*.", "",
         "| Profil | Filament | Wände | Füllung | Muster | Decke/Boden | Brim | Hinweis |", "|---|---|---|---|---|---|---|---|"]
    for k, p in PROFILES.items():
        L.append(f"| {k} | {p['mat']} | {p['walls']} | {p['infill']} % | {p['pattern']} | {p['top']}/{p['bottom']} | {p['brim']} | {p['note']} |")
    L += ["", "Stützstrukturen: **aus** (alle Teile sind stützenfrei konstruiert: Tropfenbohrungen, 45°-Fasen).", "",
          "| Nr | Datei | Profil | Filament | Teile | max. Höhe mm | Filament g | Inhalt |", "|---|---|---|---|---|---|---|---|"]
    L += lines_fdm
    L += ["", f"Filament gesamt ≈ {total_g:.0f} g (Schätzung aus Volumen, ANN).", "",
          "## Laser und Schneidplotter", "",
          "Bögen sind modulübergreifend verschachtelt und passen in die Arbeitsfläche (Laser 300 × 250 mm, Plotter 287 × 290 mm). "
          "Import als SVG (mm) in die Laser-/Schneidfunktion der Bambu-Software. Ebenen: **rot CUT** = durchschneiden, "
          "**blau ENGRAVE** = gravieren, **grün SCORE** = Stift (Plotter). Schnittfuge ist in den Konturen kompensiert → "
          "in der Software **keinen Kerf-Offset** einstellen. Teile mit Gravur: erst gravieren, dann schneiden.", "",
          "### Startparameter Laser 10 W (bis zur eigenen Matrix M00-P04)", "",
          "| Material | Vorgang | Leistung | Geschwindigkeit | Durchgänge | Quelle |", "|---|---|---|---|---|---|",
          "| Pappel/Linde 3 mm | Schneiden | 100 % | 5 mm/s | 1 | Händlertabelle 10 W (3 mm Linde 5 mm/s), **ungeprüft** |",
          "| Pappel/Linde 3 mm | Gravieren | 20–30 % | 200–300 mm/s | 1 | Erfahrungswert, Matrix bestätigen |",
          "| Pappel/Linde 4 mm | Schneiden | 100 % | 4 mm/s | 1 | nur nach bestandener Matrix (PLY4 = TEST) |", "",
          "Sicherheit: nie unbeaufsichtigt, Abluft an, Feuerlöscher bereit, nur Materialien aus der Positivliste.", "",
          "### Plotter", "",
          "Messerdruck je Material mit dem Testmuster M00-P06 ermitteln (in 50-gf-Schritten). Folien auf Trägermatte; "
          "bei Bögen mit SCORE-Ebene zuerst Stift, dann Messer.", "",
          "| Datei | Material | Gruppe | Teile |", "|---|---|---|---|"]
    L += lines_flat
    (OUT / "JOBS.md").write_text("\n".join(L) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
