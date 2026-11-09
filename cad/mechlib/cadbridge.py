"""Brücke shapely-2D → CadQuery-Solid, plus kleine 3D-Helfer fuer FDM-Teile."""

from __future__ import annotations

import math

import cadquery as cq
from shapely.geometry import Polygon

from . import geom2d as g2


def _as_circle(pts):
    """Erkennt Ringe aus geom2d.circle (gleichabständige Punkte auf Kreis) → (cx, cy, r) oder None."""
    if len(pts) < 20:
        return None
    n = len(pts)
    cx = sum(p[0] for p in pts) / n
    cy = sum(p[1] for p in pts) / n
    rs = [math.hypot(p[0] - cx, p[1] - cy) for p in pts]
    r = sum(rs) / n
    if max(abs(q - r) for q in rs) > 2e-3:
        return None
    seg = [math.dist(pts[i], pts[(i + 1) % n]) for i in range(n)]
    if max(seg) - min(seg) > 2e-3:
        return None
    return cx, cy, r


def _wire(coords, smooth=False) -> cq.Wire:
    pts = list(coords)[:-1]
    if smooth:
        step = max(1, len(pts) // 180)
        vs = [cq.Vector(x, y, 0) for x, y in pts[::step]]
        return cq.Wire.assembleEdges([cq.Edge.makeSpline(vs + [vs[0]], periodic=False)])
    c = _as_circle(pts)
    if c is not None:
        return cq.Wire.assembleEdges([cq.Edge.makeCircle(c[2], cq.Vector(c[0], c[1], 0))])
    return cq.Wire.makePolygon([cq.Vector(x, y, 0) for x, y in pts], close=True)


def extrude(geom, h: float, z0: float = 0.0, smooth: bool = False) -> cq.Workplane:
    """Extrudiert (Multi)Polygon mit Loechern um h in +z. smooth=True: Aussenkontur als
    B-Spline (fuer glatte Freiformkurven wie Nocken; nicht fuer Konturen mit Ecken)."""
    solids = []
    for p in g2.polys(geom):
        if not smooth and not any(_as_circle(list(r.coords)[:-1]) for r in [p.exterior, *p.interiors]):
            p = p.simplify(0.005)
        outer = _wire(p.exterior.coords, smooth)
        inners = [_wire(i.coords) for i in p.interiors]
        face = cq.Face.makeFromWires(outer, inners)
        solids.append(cq.Solid.extrudeLinear(face, cq.Vector(0, 0, h)))
    wp = cq.Workplane("XY").newObject([cq.Compound.makeCompound(solids) if len(solids) > 1 else solids[0]])
    return wp.translate((0, 0, z0)) if z0 else wp


def teardrop(d: float, c=(0.0, 0.0), up=(0, 1)) -> Polygon:
    """Tropfenbohrung fuer waagrechte Bohrungen im Druck (Spitze zeigt nach oben im Druck)."""
    r = d / 2
    a = math.atan2(up[1], up[0])
    tip = (c[0] + r * math.sqrt(2) * math.cos(a), c[1] + r * math.sqrt(2) * math.sin(a))
    l1 = (c[0] + r * math.cos(a + math.pi / 4) * 1, c[1] + r * math.sin(a + math.pi / 4))
    l2 = (c[0] + r * math.cos(a - math.pi / 4), c[1] + r * math.sin(a - math.pi / 4))
    return g2.circle(d, c).union(Polygon([l1, tip, l2, c]))


def cyl(d: float, h: float, c=(0, 0, 0)) -> cq.Workplane:
    return cq.Workplane("XY").circle(d / 2).extrude(h).translate(c)


def place(wp: cq.Workplane, rot=((0, 0, 0),), t=(0, 0, 0)) -> cq.Workplane:
    """Rotationen (Liste Euler-Schritte in Grad um X,Y,Z nacheinander) und Translation."""
    out = wp
    for rx, ry, rz in rot:
        if rx:
            out = out.rotate((0, 0, 0), (1, 0, 0), rx)
        if ry:
            out = out.rotate((0, 0, 0), (0, 1, 0), ry)
        if rz:
            out = out.rotate((0, 0, 0), (0, 0, 1), rz)
    return out.translate(t)


def solid_of(wp: cq.Workplane) -> cq.Shape:
    vals = [v for v in wp.vals() if isinstance(v, cq.Shape)]
    return vals[0] if len(vals) == 1 else cq.Compound.makeCompound(vals)


def xform(wp: cq.Workplane, rows, t=(0, 0, 0)) -> cq.Workplane:
    """Starre Abbildung p' = R·p + t; rows = 3×3 Rotationsmatrix (det = +1, wird geprueft)."""
    import numpy as np
    R = np.array(rows, dtype=float)
    assert abs(np.linalg.det(R) - 1) < 1e-9, "keine eigentliche Drehung (Spiegelung)"
    from OCP.BRepBuilderAPI import BRepBuilderAPI_Transform
    from OCP.gp import gp_Trsf
    tr = gp_Trsf()
    tr.SetValues(*R[0], t[0], *R[1], t[1], *R[2], t[2])
    out = []
    for v in wp.vals():
        if isinstance(v, cq.Shape):
            out.append(cq.Shape.cast(BRepBuilderAPI_Transform(v.wrapped, tr, True).Shape()))
    return wp.newObject(out)


def printed_from_asm(asm_wp: cq.Workplane, rows):
    """FDM-Teil, das in Baugruppenkoordinaten modelliert wurde, in Druckorientierung bringen.
    rows = Drehung Baugruppe→Druck. Rueckgabe (druck_wp, pose), pose bildet Druck→Baugruppe ab."""
    import numpy as np
    R = np.array(rows, dtype=float)
    rot = xform(asm_wp, R.tolist())
    bb = rot.val().BoundingBox()
    t = (-bb.center.x, -bb.center.y, -bb.zmin)
    printed = rot.translate(t)
    Rt = R.T
    tt = -Rt @ np.array(t)
    return printed, (lambda wp: xform(wp, Rt.tolist(), tuple(tt)))
