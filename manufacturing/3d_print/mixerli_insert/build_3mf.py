"""Erzeugt druckfertige Bambu-Studio-Projekte (.3mf) für den Bambu Lab H2S.

Eingabe:  STL-Dateien in ./stl/
Ausgabe:  *.3mf in diesem Ordner (Drucker, Prozess, Filament, Druckplatte voreingestellt)

Die Druckereinstellungen stammen aus den offiziellen Bambu-Studio-Systemprofilen
(github.com/bambulab/BambuStudio, resources/profiles/BBL). Pfad per Argument:

    python build_3mf.py /pfad/zu/BambuStudio/resources/profiles/BBL

Nur die in OVERRIDES genannten Werte weichen vom Systemprofil ab; beim Öffnen
setzt Bambu Studio alle übrigen Werte auf das aktuelle Systemprofil.
"""
import glob
import io
import json
import os
import sys
import zipfile
from datetime import date

import numpy as np
import trimesh

HERE = os.path.dirname(os.path.abspath(__file__))
APP_VERSION = "02.03.00.70"

PRINTER = "Bambu Lab H2S 0.4 nozzle"
FILAMENT = "Bambu PETG HF @BBL H2S"
BED = "Textured PEI Plate"
BED_CENTER = (170.0, 160.0)  # H2S: 340 x 320 mm

# name, STL, Prozess-Systemprofil, Abweichungen vom Prozessprofil[, Aufteilung]
JOBS = [
    ("mixerli_v2.0_insert_M4_through", "mixerli_v2.0_insert_M4_through.stl",
     "0.20mm Standard @BBL H2S",
     {"wall_loops": "4", "sparse_infill_density": "25%"}),
    ("mixerli_v2.0_insert_M4_thread", "mixerli_v2.0_insert_M4_thread.stl",
     "0.12mm High Quality @BBL H2S",
     {"wall_loops": "4", "sparse_infill_density": "25%"}),
    ("mixerli_v2.0_sleeves_M4", "mixerli_v2.0_sleeves_M4.stl",
     "0.20mm Standard @BBL H2S",
     {"wall_loops": "4", "sparse_infill_density": "25%"},
     (2, 20.0)),  # 4 Hülsen einzeln, 2 x 2 im 20-mm-Raster
]


def load_profiles(base):
    idx = {}
    for f in glob.glob(os.path.join(base, "**", "*.json"), recursive=True):
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        if isinstance(d, dict) and "name" in d:
            idx[d["name"]] = d
    return idx


def resolve(idx, name):
    """Wie Bambu Studio: Elternprofil -> include-Vorlagen -> eigene Werte."""
    d = idx[name]
    out = resolve(idx, d["inherits"]) if d.get("inherits") else {}
    inc = d.get("include", [])
    for i in [inc] if isinstance(inc, str) else inc:
        out.update({k: v for k, v in resolve(idx, i).items()
                    if k not in ("name", "inherits", "instantiation", "from", "type")})
    out.update(d)
    return out


META_KEYS = {"type", "name", "inherits", "from", "instantiation", "setting_id",
             "description", "include", "compatible_printers",
             "compatible_printers_condition", "compatible_prints",
             "compatible_prints_condition", "renamed_from", "base_id", "filament_id"}


def project_config(idx, process, overrides):
    m = resolve(idx, PRINTER)
    p = resolve(idx, process)
    f = resolve(idx, FILAMENT)
    cfg = {}
    for d in (m, p, f):
        cfg.update({k: v for k, v in d.items() if k not in META_KEYS})
    cfg.update(overrides)
    variants = f.get("filament_extruder_variant", ["Direct Drive Standard"])
    cfg.update({
        "printer_settings_id": PRINTER,
        "print_settings_id": process,
        "filament_settings_id": [FILAMENT],
        "filament_ids": [f.get("filament_id", "")],
        "filament_self_index": ["1"] * len(variants),
        "filament_map": ["1"],
        "filament_colour": ["#2B2B2B"],
        "curr_bed_type": BED,
        "nozzle_volume_type": ["Standard"],
        "print_compatible_printers": p.get("compatible_printers", [PRINTER]),
        "different_settings_to_system": [";".join(sorted(overrides)), "", ""],
        "inherits_group": ["", "", ""],
        "from": "project",
        "name": "project_settings",
        "version": APP_VERSION,
    })
    return cfg


def mesh_xml(mesh, oid):
    v = "\n".join(f'     <vertex x="{x:.9g}" y="{y:.9g}" z="{z:.9g}"/>' for x, y, z in mesh.vertices)
    t = "\n".join(f'     <triangle v1="{a}" v2="{b}" v3="{c}"/>' for a, b, c in mesh.faces)
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<model unit="millimeter" xml:lang="en-US" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02" '
        'xmlns:BambuStudio="http://schemas.bambulab.com/package/2021" '
        'xmlns:p="http://schemas.microsoft.com/3dmanufacturing/production/2015/06" requiredextensions="p">\n'
        ' <metadata name="BambuStudio:3mfVersion">1</metadata>\n <resources>\n'
        f'  <object id="{oid}" p:UUID="{oid:04x}0000-81cb-4c03-9d28-80fed5dfa1dc" type="model">\n'
        f'   <mesh>\n    <vertices>\n{v}\n    </vertices>\n    <triangles>\n{t}\n    </triangles>\n   </mesh>\n'
        '  </object>\n </resources>\n <build/>\n</model>\n')


def main_model_xml(title, objs):
    """objs: Liste (name, mesh, (tx, ty, tz)); Netz i liegt in 3D/Objects/object_i.model."""
    today = date.today().isoformat()
    n = len(objs)
    res, items = [], []
    for i, (_, _, (tx, ty, tz)) in enumerate(objs, 1):
        res.append(f'''  <object id="{n + i}" p:UUID="{i:08x}-61cb-4c03-9d28-80fed5dfa1dc" type="model">
   <components>
    <component p:path="/3D/Objects/object_{i}.model" objectid="{i}" p:UUID="{i:04x}0000-b206-40ff-9872-83e8017abed1" transform="1 0 0 0 1 0 0 0 1 0 0 0"/>
   </components>
  </object>''')
        items.append(f'  <item objectid="{n + i}" p:UUID="{n + i:08x}-b1ec-4553-aec9-835e5b724bb4" '
                     f'transform="1 0 0 0 1 0 0 0 1 {tx:g} {ty:g} {tz:g}" printable="1"/>')
    res, items = "\n".join(res), "\n".join(items)
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<model unit="millimeter" xml:lang="en-US" xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02" xmlns:BambuStudio="http://schemas.bambulab.com/package/2021" xmlns:p="http://schemas.microsoft.com/3dmanufacturing/production/2015/06" requiredextensions="p">
 <metadata name="Application">BambuStudio-{APP_VERSION}</metadata>
 <metadata name="BambuStudio:3mfVersion">1</metadata>
 <metadata name="CreationDate">{today}</metadata>
 <metadata name="ModificationDate">{today}</metadata>
 <metadata name="Title">{title}</metadata>
 <metadata name="Thumbnail_Middle">/Metadata/plate_1.png</metadata>
 <metadata name="Thumbnail_Small">/Metadata/plate_1.png</metadata>
 <resources>
{res}
 </resources>
 <build p:UUID="2c7c17d8-22b5-4d84-8835-1976022ea369">
{items}
 </build>
</model>
'''


def model_settings_xml(title, objs):
    n = len(objs)
    obj_xml, inst_xml, asm_xml = [], [], []
    for i, (name, mesh, (tx, ty, tz)) in enumerate(objs, 1):
        faces = len(mesh.faces)
        obj_xml.append(f'''  <object id="{n + i}">
    <metadata key="name" value="{name}"/>
    <metadata key="extruder" value="1"/>
    <metadata face_count="{faces}"/>
    <part id="1" subtype="normal_part">
      <metadata key="name" value="{name}"/>
      <metadata key="matrix" value="1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1"/>
      <mesh_stat face_count="{faces}" edges_fixed="0" degenerate_facets="0" facets_removed="0" facets_reversed="0" backwards_edges="0"/>
    </part>
  </object>''')
        inst_xml.append(f'''    <model_instance>
      <metadata key="object_id" value="{n + i}"/>
      <metadata key="instance_id" value="0"/>
      <metadata key="identify_id" value="{100 + i}"/>
    </model_instance>''')
        asm_xml.append(f'   <assemble_item object_id="{n + i}" instance_id="0" '
                       f'transform="1 0 0 0 1 0 0 0 1 {tx:g} {ty:g} {tz:g}" offset="0 0 0" />')
    obj_xml, inst_xml, asm_xml = "\n".join(obj_xml), "\n".join(inst_xml), "\n".join(asm_xml)
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<config>
{obj_xml}
  <plate>
    <metadata key="plater_id" value="1"/>
    <metadata key="plater_name" value="{title}"/>
    <metadata key="locked" value="false"/>
    <metadata key="thumbnail_file" value="Metadata/plate_1.png"/>
{inst_xml}
  </plate>
  <assemble>
{asm_xml}
  </assemble>
</config>
'''


def model_rels_xml(n):
    rels = "\n".join(f' <Relationship Target="/3D/Objects/object_{i}.model" Id="rel-{i}" '
                     'Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/>' for i in range(1, n + 1))
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">\n'
            f'{rels}\n</Relationships>\n')


CONTENT_TYPES = '''<?xml version="1.0" encoding="UTF-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
 <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
 <Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/>
 <Default Extension="png" ContentType="image/png"/>
 <Default Extension="gcode" ContentType="text/x.gcode"/>
</Types>
'''
RELS = '''<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
 <Relationship Target="/3D/3dmodel.model" Id="rel-1" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/>
 <Relationship Target="/Metadata/plate_1.png" Id="rel-2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/thumbnail"/>
</Relationships>
'''
SLICE_INFO = f'''<?xml version="1.0" encoding="UTF-8"?>
<config>
  <header>
    <header_item key="X-BBL-Client-Type" value="slicer"/>
    <header_item key="X-BBL-Client-Version" value="{APP_VERSION}"/>
  </header>
</config>
'''


def clean_mesh(path):
    mesh = trimesh.load(path)
    parts = mesh.split(only_watertight=False)
    if len(parts) > 1:  # leere Restflächen (Fläche 0) aus dem CAD-Export entfernen
        parts = [p for p in parts if p.area > 1e-6 and abs(p.volume) > 1e-6]
        mesh = trimesh.util.concatenate(parts)
    trimesh.repair.fix_normals(mesh)
    assert mesh.is_watertight, f"{path}: Netz nicht geschlossen"
    return mesh


def thumbnail(mesh):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    fig = plt.figure(figsize=(4, 4), dpi=128)
    ax = fig.add_subplot(projection="3d")
    tri = mesh.vertices[mesh.faces]
    light = np.clip(mesh.face_normals @ np.array([0.3, -0.5, 0.8]), 0.15, 1.0)
    col = np.outer(0.25 + 0.55 * light, [0.35, 0.55, 0.85])
    ax.add_collection3d(Poly3DCollection(tri, facecolors=np.clip(col, 0, 1), linewidths=0))
    lo, hi = mesh.bounds
    c, r = (lo + hi) / 2, (hi - lo).max() / 2
    ax.set_xlim(c[0] - r, c[0] + r); ax.set_ylim(c[1] - r, c[1] + r); ax.set_zlim(c[2] - r, c[2] + r)
    ax.view_init(elev=90, azim=-90); ax.set_axis_off()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", transparent=True, bbox_inches="tight", pad_inches=0)
    plt.close(fig)
    return buf.getvalue()


def build(idx, name, stl, process, overrides, split=None):
    """split=None: ein Objekt. split=(spalten, raster_mm): jeder Körper wird ein eigenes Objekt."""
    mesh = clean_mesh(os.path.join(HERE, "stl", stl))
    lo, hi = mesh.bounds
    if split:
        bodies = sorted(mesh.split(only_watertight=True), key=lambda b: tuple(b.bounds[0]))
        cols, pitch = split
        rows = -(-len(bodies) // cols)
        objs = []
        for k, body in enumerate(bodies):
            b_lo, b_hi = body.bounds
            body.apply_translation(-(b_lo + b_hi) / 2)
            r, c = divmod(k, cols)
            objs.append((f"{name}_{k + 1}", body,
                         (BED_CENTER[0] + (c - (cols - 1) / 2) * pitch,
                          BED_CENTER[1] - (r - (rows - 1) / 2) * pitch,
                          (b_hi[2] - b_lo[2]) / 2)))
    else:
        body = mesh.copy()
        body.apply_translation(-(lo + hi) / 2)  # Objektursprung = Mitte des Bauteils
        objs = [(name, body, (BED_CENTER[0], BED_CENTER[1], (hi[2] - lo[2]) / 2))]  # flach, Bettmitte
    cfg = project_config(idx, process, overrides)
    out = os.path.join(HERE, f"{name}_H2S_PETG.3mf")
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", CONTENT_TYPES)
        z.writestr("_rels/.rels", RELS)
        z.writestr("3D/3dmodel.model", main_model_xml(name, objs))
        z.writestr("3D/_rels/3dmodel.model.rels", model_rels_xml(len(objs)))
        for i, (_, body, _) in enumerate(objs, 1):
            z.writestr(f"3D/Objects/object_{i}.model", mesh_xml(body, i))
        z.writestr("Metadata/model_settings.config", model_settings_xml(name, objs))
        z.writestr("Metadata/project_settings.config", json.dumps(cfg, indent=4, ensure_ascii=False))
        z.writestr("Metadata/slice_info.config", SLICE_INFO)
        z.writestr("Metadata/plate_1.png", thumbnail(mesh))
    print(f"{out}: {len(objs)} Objekt(e), {len(mesh.faces)} Dreiecke, {mesh.volume / 1000:.1f} cm3")


if __name__ == "__main__":
    base = sys.argv[1] if len(sys.argv) > 1 else "/home/user/bambulab/bambustudio/resources/profiles/BBL"
    profiles = load_profiles(base)
    for job in JOBS:
        build(profiles, *job)
