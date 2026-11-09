"""Tests der parametrischen Mechanikmodule (cad/). Prüfen Konstruktion und Fertigungsregeln
rechnerisch (Stufe B) – keine Aussage über reale Funktion (Stufe E)."""

import importlib
import math
import sys
from pathlib import Path

import pytest

pytest.importorskip("cadquery")
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "cad"))

from build_all import MODULES  # noqa: E402
from mechlib import fab, geom2d as g2  # noqa: E402
from mechlib.gears import contact_ratio, spur_gear  # noqa: E402
from mechlib.materials import LASER_FORBIDDEN, MATERIALS, check_material  # noqa: E402


@pytest.mark.parametrize("name", MODULES)
def test_module_checks_pass(name):
    mod = importlib.import_module(f"models.{name}").build()
    bad = [c for c in mod.run_checks() if not c[1]]
    assert not bad, bad


def test_twelve_function_modules():
    assert len([m for m in MODULES if not m.startswith("m00")]) == 12


def test_every_module_uses_at_least_two_processes_or_is_justified():
    single = []
    for name in MODULES[1:]:
        mod = importlib.import_module(f"models.{name}").build()
        procs = {p.process for p in mod.parts if p.qty > 0}
        if len(procs) < 2:
            single.append(mod.mid)
    assert single == []


def test_kerf_compensation_grows_outline_shrinks_holes():
    k = 0.2
    part = g2.rect(40, 20).difference(g2.circle(10))
    comp = g2.kerf_comp(part, k)
    minx, miny, maxx, maxy = comp.bounds
    assert maxx - minx == pytest.approx(40 + k, abs=1e-3)
    hole = comp.interiors[0]
    xs = [c[0] for c in hole.coords]
    assert max(xs) - min(xs) == pytest.approx(10 - k, abs=0.01)


def test_narrow_web_detected():
    ok = g2.rect(50, 30).difference(g2.rect(10, 10, (0, 8)))      # Steg 2 mm
    thin = g2.rect(50, 30).difference(g2.rect(10, 10, (0, 9.5)))  # Steg 0.5 mm
    assert g2.min_web_ok(ok, 2.0)
    assert not g2.min_web_ok(thin, 2.0)


def test_gear_pitch_area_and_contact_ratio():
    g = spur_gear(1.5, 48, 0.0)
    rp = 1.5 * 48 / 2
    assert g.area == pytest.approx(math.pi * rp**2, rel=0.03)
    assert contact_ratio(1.5, 16, 48) > 1.2


def test_no_pvc_or_unknown_plastic_allowed_in_laser():
    laser_mats = [m for m in MATERIALS.values() if m.process == "laser"]
    for m in laser_mats:
        assert not any(w in m.name.upper() for w in ("PVC", "VINYL", "ABS", "PC ", "PTFE", "PET"))
    assert check_material("PVC", "laser")             # unbekannt → Fehler
    assert check_material("PET019", "laser")          # Plottermaterial → im Laser nicht frei
    assert any("PVC" in n for n, _ in LASER_FORBIDDEN)


def test_process_limits_enforced():
    assert check_material("PLY4", "laser", 5.0)       # > Konstruktionsgrenze
    assert check_material("GASKET05", "plotter", 0.8)  # > 0.5 mm Plotter
    assert fab.LASER_MAX_CUT_RULE.value < fab.LASER_MAX_CUT_SPEC.value


def test_dxf_export_roundtrip(tmp_path):
    import ezdxf
    g = g2.kerf_comp(g2.rect(20, 10).difference(g2.circle(4)), fab.KERF.value)
    g2.export_dxf({"CUT": g}, tmp_path / "t.dxf")
    doc = ezdxf.readfile(tmp_path / "t.dxf")
    polys = list(doc.modelspace().query("LWPOLYLINE"))
    assert len(polys) == 2 and all(p.closed for p in polys) and all(p.dxf.layer == "CUT" for p in polys)
