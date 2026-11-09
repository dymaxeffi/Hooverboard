"""2D-Geometrie fuer Laser- und Plotterteile (shapely) + Export DXF/SVG.

Konvention: Teile werden NENNmass konstruiert. ``kerf_comp`` vergroessert
Aussenkonturen um kerf/2 und verkleinert Innenkonturen (Loecher) um kerf/2
– genau das, was ``buffer(+kerf/2)`` bei Polygonen mit Loechern tut.
In Bambu Studio / Bambu Suite darf deshalb KEIN zusaetzlicher Kerf-Offset
eingestellt werden (doppelte Kompensation).
"""

from __future__ import annotations

import math
from pathlib import Path

import ezdxf
import shapely
from shapely import affinity
from shapely.geometry import LineString, MultiLineString, MultiPolygon, Point, Polygon, box
from shapely.ops import unary_union

CHORD_TOL = 0.01  # mm Sehnenfehler fuer Kreise


def _segs(r: float) -> int:
    if r <= CHORD_TOL:
        return 8
    return max(24, int(math.ceil(math.pi / math.acos(1 - CHORD_TOL / r))))


def circle(d: float, c=(0.0, 0.0)) -> Polygon:
    r = d / 2
    n = _segs(r)
    return Polygon([(c[0] + r * math.cos(2 * math.pi * i / n), c[1] + r * math.sin(2 * math.pi * i / n))
                    for i in range(n)])


def rect(w: float, h: float, c=(0.0, 0.0), r: float = 0.0) -> Polygon:
    b = box(c[0] - w / 2, c[1] - h / 2, c[0] + w / 2, c[1] + h / 2)
    if r > 0:
        b = b.buffer(-r, join_style="mitre").buffer(r, quad_segs=max(4, _segs(r) // 4))
    return b


def rect_xy(x0, y0, x1, y1) -> Polygon:
    return box(min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1))


def slot(p0, p1, w: float) -> Polygon:
    return LineString([p0, p1]).buffer(w / 2, quad_segs=_segs(w / 2) // 4)


def hexagon(af: float, c=(0.0, 0.0), rot=0.0) -> Polygon:
    r = af / math.sqrt(3)
    return Polygon([(c[0] + r * math.cos(math.radians(rot + 60 * i)),
                     c[1] + r * math.sin(math.radians(rot + 60 * i))) for i in range(6)])


def arc_slot(center, r: float, a0: float, a1: float, w: float) -> Polygon:
    n = max(16, int(abs(a1 - a0) / 2))
    pts = [(center[0] + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
            center[1] + r * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]
    return LineString(pts).buffer(w / 2, quad_segs=8)


def round_inner(g, r: float):
    """Innenecken verrunden (Plotter-Regel)."""
    return g.buffer(r, quad_segs=8).buffer(-r, quad_segs=8) if r > 0 else g


def largest(g) -> Polygon:
    if isinstance(g, MultiPolygon):
        return max(g.geoms, key=lambda p: p.area)
    return g


def kerf_comp(g, kerf: float):
    if kerf == 0:
        return g
    return g.buffer(kerf / 2, join_style="mitre", mitre_limit=3.0)


def polys(g) -> list[Polygon]:
    if g.is_empty:
        return []
    if isinstance(g, Polygon):
        return [g]
    out = []
    for gg in getattr(g, "geoms", []):
        out += polys(gg)
    return out


def lines(g) -> list[list[tuple[float, float]]]:
    """Alle Konturen (Polygonringe + Linien) als Punktlisten."""
    out = []
    if g is None or g.is_empty:
        return out
    if isinstance(g, (Polygon, MultiPolygon)):
        for p in polys(g):
            out.append(list(p.exterior.coords))
            out.extend(list(i.coords) for i in p.interiors)
    elif isinstance(g, LineString):
        out.append(list(g.coords))
    elif isinstance(g, MultiLineString):
        out.extend(list(l.coords) for l in g.geoms)
    else:
        for gg in getattr(g, "geoms", []):
            out.extend(lines(gg))
    return out


# ------------------------------------------------------------- Gravurtext
def text(s: str, height: float, pos=(0.0, 0.0), anchor="center"):
    """Text als Polygone (matplotlib-Font, kein externes Font-File noetig)."""
    from matplotlib.font_manager import FontProperties
    from matplotlib.textpath import TextPath

    tp = TextPath((0, 0), s, size=height, prop=FontProperties(family="DejaVu Sans", weight="bold"))
    rings = [Polygon(p) for p in tp.to_polygons() if len(p) >= 3]
    g = Polygon()
    # Even-odd: Ringe nach Flaeche sortieren, Loecher (Innenringe von O, A ...) abziehen
    for r in sorted(rings, key=lambda p: -abs(p.area)):
        r = r.buffer(0)
        if g.intersection(r).area > 0.5 * r.area:
            g = g.difference(r)
        else:
            g = g.union(r)
    minx, miny, maxx, maxy = g.bounds
    dx = {"center": -(minx + maxx) / 2, "left": -minx, "right": -maxx}[anchor]
    return affinity.translate(g, pos[0] + dx, pos[1] - (miny + maxy) / 2).simplify(0.01)


# ------------------------------------------------------------- Export
LAYERS = {  # name: (DXF-Farbe ACI, SVG-Farbe, Bedeutung)
    "CUT": (1, "#ff0000", "Durchschnitt"),
    "ENGRAVE": (5, "#0000ff", "Gravur / Flaechengravur"),
    "SCORE": (3, "#00a000", "Linie anritzen (Laser) bzw. Stift (Plotter)"),
}


def export_dxf(layers: dict, path: Path) -> None:
    doc = ezdxf.new("R2010", units=ezdxf.units.MM)
    msp = doc.modelspace()
    for name, (aci, _, _) in LAYERS.items():
        doc.layers.add(name, color=aci)
    for name, g in layers.items():
        for pts in lines(g):
            closed = len(pts) > 2 and pts[0] == pts[-1]
            msp.add_lwpolyline([(round(x, 4), round(y, 4)) for x, y in (pts[:-1] if closed else pts)],
                               close=closed, dxfattribs={"layer": name})
    path.parent.mkdir(parents=True, exist_ok=True)
    doc.saveas(path)


def export_svg(layers: dict, path: Path, title: str = "") -> None:
    allg = unary_union([g for g in layers.values() if g is not None and not g.is_empty])
    minx, miny, maxx, maxy = allg.bounds
    pad = 1.0
    w, h = maxx - minx + 2 * pad, maxy - miny + 2 * pad
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.3f}mm" height="{h:.3f}mm" '
           f'viewBox="0 0 {w:.3f} {h:.3f}">', f"<title>{title}</title>"]
    for name, g in layers.items():
        color = LAYERS[name][1]
        fill = color if name == "ENGRAVE" else "none"
        out.append(f'<g id="{name}" stroke="{color}" stroke-width="0.05" fill="{fill}" fill-rule="evenodd">')
        if name == "ENGRAVE":
            for p in polys(g):
                d = ""
                for ring in [p.exterior, *p.interiors]:
                    c = [(x - minx + pad, maxy - y + pad) for x, y in ring.coords]
                    d += "M" + " L".join(f"{x:.3f},{y:.3f}" for x, y in c) + " Z "
                out.append(f'<path d="{d.strip()}"/>')
            g = None
        for pts in lines(g):
            c = [(x - minx + pad, maxy - y + pad) for x, y in pts]
            closed = len(pts) > 2 and pts[0] == pts[-1]
            out.append('<path d="M' + " L".join(f"{x:.3f},{y:.3f}" for x, y in c) + (" Z" if closed else "") + '"/>')
        out.append("</g>")
    out.append("</svg>")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(out), encoding="utf-8")


# ------------------------------------------------------------- Nesting
def shelf_nest(items, area_w: float, area_h: float, gap: float = 3.0):
    """Einfaches Regal-Nesting. items: Liste (key, geom). Rueckgabe: Liste Blaetter,
    jedes Blatt = Liste (key, verschobene geom). Teile werden ggf. um 90° gedreht."""
    prepared = []
    for key, g in items:
        minx, miny, maxx, maxy = g.bounds
        if (maxx - minx) > area_w and (maxy - miny) <= area_w:
            g = affinity.rotate(g, 90, origin=(0, 0))
        prepared.append((key, g))
    prepared.sort(key=lambda kg: -(kg[1].bounds[3] - kg[1].bounds[1]))
    sheets, cur, x, y, row_h = [], [], 0.0, 0.0, 0.0
    for key, g in prepared:
        minx, miny, maxx, maxy = g.bounds
        w, h = maxx - minx, maxy - miny
        if w > area_w or h > area_h:
            raise ValueError(f"{key}: {w:.1f}x{h:.1f} mm passt nicht in {area_w}x{area_h} mm")
        if x + w > area_w:
            x, y, row_h = 0.0, y + row_h + gap, 0.0
        if y + h > area_h:
            sheets.append(cur)
            cur, x, y, row_h = [], 0.0, 0.0, 0.0
        cur.append((key, affinity.translate(g, x - minx, y - miny)))
        x += w + gap
        row_h = max(row_h, h)
    if cur:
        sheets.append(cur)
    return sheets


def narrow_regions(g, w: float):
    """Bereiche schmaler als w (Stege und Oeffnungen), per morphologischem Oeffnen/Schliessen.
    Rechtwinklige Ecken erzeugen nur kleine Reste und werden ignoriert."""
    r = w / 2 - 1e-3
    corner = 1.6 * (1 - math.pi / 4) * r * r + 0.02
    bad = []
    for d in (g.difference(g.buffer(-r).buffer(r)), g.buffer(r).buffer(-r).difference(g)):
        bad += [p for p in polys(d.buffer(-1e-4)) if p.area > corner]   # -1e-4: Haarbrücken trennen
    return bad


def min_web_ok(g, w: float) -> bool:
    return not narrow_regions(g, w)
