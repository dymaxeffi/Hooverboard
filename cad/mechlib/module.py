"""Modul-/Teile-Framework: Export (STEP/STL/DXF/SVG), Baugruppe, Pruefungen, Doku."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

import cadquery as cq
from shapely import affinity
from shapely.ops import unary_union

from . import fab, geom2d as g2
from .cadbridge import extrude, solid_of
from .materials import MATERIALS, check_material

ROOT = Path(__file__).resolve().parents[2]
OUT_FDM = ROOT / "manufacturing" / "3d_print"
OUT_LASER = ROOT / "manufacturing" / "laser_cut"
OUT_PLOT = ROOT / "manufacturing" / "plotter"
OUT_ASM = ROOT / "cad" / "assemblies"
OUT_DOC = ROOT / "manufacturing" / "modules"

DENSITY = {"PETG": 1.27, "ASA": 1.07, "TPU95A": 1.21, "PLA": 1.24}
PRICE_KG = {"PETG": 20.0, "ASA": 25.0, "TPU95A": 30.0, "PLA": 18.0}
FILL_FACTOR = 0.65   # ANN: Masse/Vollvolumen bei 3 Perimetern + 25–40 % Gyroid
PLY_CHF_M2 = 15.0    # ANN


def slug(s: str) -> str:
    s = s.lower().replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
    return re.sub(r"[^a-z0-9]+", "_", s).strip("_")


@dataclass
class Part:
    pid: str
    name: str
    process: str                      # fdm | laser | plotter
    material: str
    qty: int = 1
    shape: cq.Workplane | None = None  # FDM: in Druckorientierung (z=0 Bett)
    profile: object = None             # Laser/Plotter: Nennkontur (shapely)
    engrave: object = None             # Laser: Gravur; Plotter: Stiftlinien
    thickness: float | None = None
    poses: list[Callable] = field(default_factory=list)  # Platzierungen in Baugruppe
    orientation: str = ""
    rationale: str = ""
    notes: str = ""
    no_kerf: bool = False              # Kalibrierteile: bewusst OHNE Kompensation
    test_feature: bool = False         # Prüfmuster: Unterschreitung Mindestmass ist Absicht
    cut_lines: object = None           # zusätzliche offene Schnittlinien (nur Export)

    def solid(self) -> cq.Workplane:
        if self.shape is not None:
            return self.shape
        t = self.thickness or MATERIALS[self.material].thickness
        return extrude(self.profile, t)

    def cut_geometry(self):
        if self.process == "laser" and not self.no_kerf:
            return g2.kerf_comp(self.profile, fab.KERF.value)
        return self.profile


@dataclass
class Module:
    mid: str
    title: str
    purpose: str
    parts: list[Part]
    hardware: list[tuple[str, int, float]] = field(default_factory=list)  # (Text, Stk, CHF/Stk)
    assembly: list[str] = field(default_factory=list)
    checks: list[tuple[str, bool, str]] = field(default_factory=list)      # modulspezifisch
    function_test: str = ""
    allow_touch: set = field(default_factory=set)  # Paare (pidA, pidB) mit gewolltem Presssitz

    # ---------------------------------------------------------- Pruefungen
    def run_checks(self, interference=True) -> list[tuple[str, bool, str]]:
        res = list(self.checks)
        for p in self.parts:
            if p.process == "fdm":
                bb = p.solid().val().BoundingBox()
                ok = (bb.xlen <= fab.PRINT_VOLUME_X.value and bb.ylen <= fab.PRINT_VOLUME_Y.value
                      and bb.zlen <= fab.PRINT_VOLUME_Z.value)
                res.append((f"{p.pid} Bauraum", ok, f"{bb.xlen:.1f}×{bb.ylen:.1f}×{bb.zlen:.1f} mm"))
                res.append((f"{p.pid} liegt auf Bett", abs(bb.zmin) < 1e-3, f"zmin={bb.zmin:.3f}"))
                res.append((f"{p.pid} Solid gültig", p.solid().val().isValid(), ""))
            else:
                g = p.cut_geometry()
                minx, miny, maxx, maxy = g.bounds
                w, h = maxx - minx, maxy - miny
                if p.process == "laser":
                    aw = fab.LASER_AREA_X.value - 2 * fab.LASER_MARGIN.value
                    ah = fab.LASER_AREA_Y.value - 2 * fab.LASER_MARGIN.value
                    web = fab.LASER_MIN_WEB.value
                else:
                    aw, ah, web = fab.CUT_AREA_X.value - 10, fab.CUT_AREA_Y.value - 10, fab.CUT_MIN_FEATURE.value
                fits = (w <= aw and h <= ah) or (h <= aw and w <= ah)
                res.append((f"{p.pid} Arbeitsfläche", fits, f"{w:.1f}×{h:.1f} mm in {aw:.0f}×{ah:.0f}"))
                nr = [] if p.test_feature else g2.narrow_regions(p.profile, web)
                res.append((f"{p.pid} Mindeststeg {web} mm", not nr,
                            f"{len(nr)} zu schmale Bereiche" if nr else ("Prüfmuster – absichtlich" if p.test_feature else "")))
                if p.engrave is not None and p.process == "laser":
                    res.append((f"{p.pid} Gravur innerhalb Teil", p.profile.buffer(0.01).contains(p.engrave), ""))
            issues = check_material(p.material, p.process, p.thickness)
            for issue in issues:
                res.append((f"{p.pid} Material", False, issue))
            if not issues:
                res.append((f"{p.pid} Material {p.material}", True, MATERIALS[p.material].status))
        if interference:
            res += self.interference()
        return res

    def instances(self):
        out = []
        for p in self.parts:
            base = p.solid()
            for i, pose in enumerate(p.poses):
                out.append((f"{p.pid}#{i + 1}", p, pose(base)))
        return out

    def interference(self, tol=0.5):
        inst = [(n, p, solid_of(wp)) for n, p, wp in self.instances()]
        bad = []
        for i in range(len(inst)):
            for j in range(i + 1, len(inst)):
                (na, pa, a), (nb, pb, b) = inst[i], inst[j]
                if (pa.pid, pb.pid) in self.allow_touch or (pb.pid, pa.pid) in self.allow_touch:
                    continue
                ba, bb = a.BoundingBox(), b.BoundingBox()
                if (ba.xmax < bb.xmin or bb.xmax < ba.xmin or ba.ymax < bb.ymin or bb.ymax < ba.ymin
                        or ba.zmax < bb.zmin or bb.zmax < ba.zmin):
                    continue
                vol = a.intersect(b).Volume()
                if vol > tol:
                    bad.append(f"{na}↔{nb}: {vol:.1f} mm³")
        return [("Baugruppe kollisionsfrei", not bad, "; ".join(bad[:6]))]

    # ---------------------------------------------------------- Kosten
    def cost(self):
        fdm = laser = 0.0
        mass = 0.0
        for p in self.parts:
            if p.process == "fdm":
                m = p.solid().val().Volume() / 1000 * DENSITY[p.material] * FILL_FACTOR * p.qty
                mass += m
                fdm += m / 1000 * PRICE_KG[p.material]
            elif p.process == "laser":
                a = p.profile.envelope.area * p.qty * 1.3 / 1e6
                laser += a * PLY_CHF_M2
        hw = sum(q * c for _, q, c in self.hardware)
        return {"fdm_g": mass, "fdm": fdm, "laser": laser, "hardware": hw, "total": fdm + laser + hw + 0.5}

    # ---------------------------------------------------------- Export
    def export(self) -> list[Path]:
        files = []
        for p in self.parts:
            stem = f"{p.pid}_{slug(p.name)}"
            if p.process == "fdm":
                d = OUT_FDM / self.mid
                d.mkdir(parents=True, exist_ok=True)
                cq.exporters.export(p.solid(), str(d / f"{stem}.step"))
                cq.exporters.export(p.solid(), str(d / f"{stem}.stl"), tolerance=0.02, angularTolerance=0.15)
                files += [d / f"{stem}.step", d / f"{stem}.stl"]
            else:
                d = (OUT_LASER if p.process == "laser" else OUT_PLOT) / self.mid
                layers = {"CUT": p.cut_geometry() if p.cut_lines is None else _multi([p.cut_geometry(), p.cut_lines])}
                if p.engrave is not None:
                    layers["ENGRAVE" if p.process == "laser" else "SCORE"] = p.engrave
                g2.export_dxf(layers, d / f"{stem}.dxf")
                g2.export_svg(layers, d / f"{stem}.svg", title=f"{p.pid} {p.name} – {p.material} – {p.qty} Stk")
                files += [d / f"{stem}.dxf", d / f"{stem}.svg"]
        files += self._export_sheets()
        if self.instances():
            files.append(self.export_assembly())
        return files

    def _export_sheets(self):
        files = []
        for proc, root, aw, ah in (("laser", OUT_LASER, fab.LASER_AREA_X.value - 2 * fab.LASER_MARGIN.value,
                                    fab.LASER_AREA_Y.value - 2 * fab.LASER_MARGIN.value),
                                   ("plotter", OUT_PLOT, fab.CUT_AREA_X.value - 10, fab.CUT_AREA_Y.value - 10)):
            by_mat = {}
            for p in self.parts:
                if p.process == proc:
                    for k in range(p.qty):
                        by_mat.setdefault(p.material, []).append(((p.pid, k), p))
            for mat, items in by_mat.items():
                nest_items = [((pid, k), p.cut_geometry().envelope) for (pid, k), p in items]
                sheets = g2.shelf_nest(nest_items, aw, ah)
                lookup = {(pid, k): p for (pid, k), p in items}
                for si, sheet in enumerate(sheets, 1):
                    cut, eng = [], []
                    for key, placed_env in sheet:
                        p = lookup[key]
                        env = p.cut_geometry().envelope
                        # gleiche Transformation wie Huellrechteck: Rotation erkennen
                        rot = abs((env.bounds[2] - env.bounds[0]) - (placed_env.bounds[2] - placed_env.bounds[0])) > 1e-6
                        geo, en = p.cut_geometry(), p.engrave
                        if rot:
                            geo = affinity.rotate(geo, 90, origin=(0, 0))
                            en = affinity.rotate(en, 90, origin=(0, 0)) if en is not None else None
                        dx = placed_env.bounds[0] - geo.bounds[0]
                        dy = placed_env.bounds[1] - geo.bounds[1]
                        cut.append(affinity.translate(geo, dx, dy))
                        if en is not None:
                            eng.append(affinity.translate(en, dx, dy))
                    layers = {"CUT": unary_union(cut) if proc == "plotter" else _multi(cut)}
                    if eng:
                        layers["ENGRAVE" if proc == "laser" else "SCORE"] = _multi(eng)
                    stem = f"{self.mid}_{slug(mat)}_bogen{si}"
                    g2.export_svg(layers, root / self.mid / f"{stem}.svg", title=f"{self.mid} {mat} Bogen {si}")
                    g2.export_dxf(layers, root / self.mid / f"{stem}.dxf")
                    files += [root / self.mid / f"{stem}.svg", root / self.mid / f"{stem}.dxf"]
        return files

    def export_assembly(self) -> Path:
        colors = {"fdm": cq.Color(0.15, 0.45, 0.85), "laser": cq.Color(0.82, 0.68, 0.45),
                  "plotter": cq.Color(0.9, 0.9, 0.9)}
        asm = cq.Assembly(name=self.mid)
        for n, p, wp in self.instances():
            asm.add(wp, name=n.replace("#", "_"), color=colors[p.process])
        OUT_ASM.mkdir(parents=True, exist_ok=True)
        path = OUT_ASM / f"{self.mid}_baugruppe.step"
        asm.export(str(path))                                   # gross, nicht versioniert (regenerierbar)
        glb = OUT_ASM / f"{self.mid}_baugruppe.glb"
        asm.export(str(glb), tolerance=0.05, angularTolerance=0.3)
        return glb


def _multi(geoms):
    from shapely.geometry import GeometryCollection
    return GeometryCollection(geoms)
