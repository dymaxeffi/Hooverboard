"""Standardelemente, die von mehreren Modulen verwendet werden.

Alle FDM-Teile werden in Druckorientierung erzeugt (Bettseite z=0).
"""

from __future__ import annotations

import math

import cadquery as cq
from shapely import affinity
from shapely.geometry import Polygon

from . import fab, geom2d as g2
from .cadbridge import extrude, teardrop, xform
from .gears import spur_gear

T = fab.PLY_T.value
HC = fab.HOLE_COMP.value


def label(text: str, at=(0, 0), h=3.5, rot=0.0):
    t = g2.text(text, h, at)
    return affinity.rotate(t, rot, origin=at) if rot else t


# ------------------------------------------------------------ Lagerflansch 608
LF_OD, LF_PCD, LF_CUP, LF_FL_T, LF_H = 42.0, 34.0, 26.0, 4.0, 8.0


def lagerflansch_608() -> cq.Workplane:
    """Flanschgehäuse für 608: Flansch aussen am Seitenschild, Topf (Ø26) steckt im Laserloch.
    Druck: Flansch unten, Lagersitz oben offen → runder, masshaltiger Sitz ohne Stützen."""
    fl = g2.circle(LF_OD)
    for k in range(3):
        a = math.radians(90 + 120 * k)
        fl = fl.difference(g2.circle(fab.M3_CLR + HC, (LF_PCD / 2 * math.cos(a), LF_PCD / 2 * math.sin(a))))
    fl = fl.difference(g2.circle(12.0))
    body = extrude(fl, LF_FL_T)
    cup = extrude(g2.circle(LF_CUP).difference(g2.circle(12.0)), LF_H - LF_FL_T, LF_FL_T)
    seat = cq.Workplane("XY").circle(fab.PRESS_608.value / 2).extrude(fab.B608_B).translate((0, 0, LF_H - fab.B608_B))
    # Einführfase 0.4 mm am Sitz
    fase = cq.Workplane("XY").workplane(offset=LF_H - 0.4).circle(fab.PRESS_608.value / 2).workplane(offset=0.4) \
        .circle(fab.PRESS_608.value / 2 + 0.4).loft()
    return body.union(cup).cut(seat).cut(fase)


def lagerflansch_cutout(c):
    """Laserausschnitt im Seitenschild für einen Lagerflansch bei c (Topf + 3 Schraubenlöcher)."""
    g = g2.circle(LF_CUP + 0.4, c)
    for k in range(3):
        a = math.radians(90 + 120 * k)
        g = g.union(g2.circle(fab.M3_CLR, (c[0] + LF_PCD / 2 * math.cos(a), c[1] + LF_PCD / 2 * math.sin(a))))
    return g


# ------------------------------------------------------------ Winkelfuss
WF_W, WF_L, WF_H, WF_T = 12.0, 20.0, 18.0, 4.0
WF_HOLE_Z = 10.0


def winkelfuss() -> cq.Workplane:
    """L-Winkel 20×18, Breite 12. Druck liegend (L-Profil in XY, Breite in Z) → Schichten
    laufen durch beide Schenkel; Löcher waagrecht im Druck als Tropfen."""
    prof = Polygon([(0, 0), (WF_L, 0), (WF_L, WF_T), (WF_T + 3, WF_T), (WF_T, WF_T + 3), (WF_T, WF_H), (0, WF_H)])
    body = extrude(prof, WF_W)
    # Loch im liegenden Schenkel (senkrecht zur Rasterplatte): Achse = Druck-Y
    h1 = cq.Workplane("XZ").center(WF_T + 8.0, WF_W / 2).circle((fab.M3_CLR + HC) / 2).extrude(-20).translate((0, -5, 0))
    # Loch im stehenden Schenkel (durch Seitenschild): Achse = Druck-X
    h2 = cq.Workplane("YZ").center(WF_HOLE_Z, WF_W / 2).circle((fab.M3_CLR + HC) / 2).extrude(20).translate((-5, 0, 0))
    return body.cut(h1).cut(h2)


def winkelfuss_pose(x, y_face, side):
    """Winkelfuss in Baugruppe: stehender Schenkel liegt an Ebene y=y_face an (Lochachse y,
    Loch bei x, Höhe WF_HOLE_Z), liegender Schenkel auf z=0 zeigt nach side·y."""
    if side > 0:
        return lambda wp: xform(wp, [[0, 0, 1], [1, 0, 0], [0, 1, 0]], (x - WF_W / 2, y_face, 0))
    return lambda wp: xform(wp, [[0, 0, -1], [-1, 0, 0], [0, 1, 0]], (x + WF_W / 2, y_face, 0))


# ------------------------------------------------------------ Seitenschild (Laser)
def seitenschild(width: float, height: float, bearings=(), holes=(), extra_cut=None, foot_x=(-40, 40),
                 text: str = "", corner=4.0, text_at=None):
    """Stehende Laserplatte, 2D-Koordinaten: x horizontal, y = Höhe über Rasterplatte (0..height).
    bearings: Lagerflansch-Mittelpunkte; holes: (d, (x,y)); foot_x: M3-Löcher für Winkelfüsse."""
    g = g2.rect_xy(-width / 2, 0, width / 2, height / 2).union(g2.rect(width, height, (0, height / 2), r=corner))
    for c in bearings:
        g = g.difference(lagerflansch_cutout(c))
    for d, c in holes:
        g = g.difference(g2.circle(d, c))
    for x in foot_x:
        g = g.difference(g2.circle(fab.M3_CLR, (x, WF_HOLE_Z)))
    if extra_cut is not None:
        g = g.difference(extra_cut)
    eng = label(text, text_at or (0, height - 7), 3.5) if text else None
    return g, eng


def plate_pose(y_plane, x=0.0, z=0.0):
    """Laserplatte (2D in XY, Dicke +z) aufstellen: 2D-y → Höhe z, Dicke belegt y_plane..y_plane+T."""
    return lambda wp: xform(wp, [[1, 0, 0], [0, 0, -1], [0, 1, 0]], (x, y_plane + T, z))


def flat_pose(z0=0.0, x=0.0, y=0.0, rotz=0.0):
    """Laserplatte flach liegend ab Höhe z0."""
    c, s_ = math.cos(math.radians(rotz)), math.sin(math.radians(rotz))
    return lambda wp: xform(wp, [[c, -s_, 0], [s_, c, 0], [0, 0, 1]], (x, y, z0))


def axis_y_pose(x, z, y0, flip=False):
    """FDM-Rotationsteil (Achse = Druck-z) auf Baugruppenachse parallel y legen.
    flip=False: Druck-z → +y ab y0; flip=True: Druck-z → -y ab y0."""
    if not flip:
        return lambda wp: xform(wp, [[1, 0, 0], [0, 0, 1], [0, -1, 0]], (x, y0, z))
    return lambda wp: xform(wp, [[1, 0, 0], [0, 0, -1], [0, 1, 0]], (x, y0, z))


# ------------------------------------------------------------ Zahnrad mit Nabe
def gear_part(m, z, width, bore=fab.SHAFT_D, hub_d=None, hub_h=10.0, grub=True, backlash=None):
    """Gedrucktes Stirnrad, Nabe oben (Druck: Zahnradseite auf Bett → saubere Verzahnung).
    Madenschraube M3 radial in Nabe, Mutter in Schlitz von oben eingelegt."""
    bl = fab.GEAR_BACKLASH.value if backlash is None else backlash
    prof = spur_gear(m, z, bl).difference(g2.circle(bore + HC))
    body = extrude(prof, width)
    if hub_h > 0:
        hub_d = hub_d or min(bore + 10, m * (z - 2.5) - 1)
        hub = extrude(g2.circle(hub_d).difference(g2.circle(bore + HC)), hub_h, width)
        body = body.union(hub)
        if grub:
            zc = width + hub_h / 2
            screw = cq.Workplane("YZ").circle((fab.M3_CLR) / 2).extrude(hub_d).translate((0, 0, zc))
            nut = cq.Workplane("XY").rect(fab.M3_NUT_H + 0.3, fab.M3_NUT_AF + 0.3).extrude(hub_h) \
                .translate((bore / 2 + 2.0 + fab.M3_NUT_H / 2, 0, zc - (fab.M3_NUT_AF + 0.3) / 2))
            body = body.cut(screw).cut(nut)
    return body


def distanzhuelse(length, d_in=fab.SHAFT_D + 0.3, d_out=11.0):
    return extrude(g2.circle(d_out).difference(g2.circle(d_in + HC)), length)


def kurbel(arm=40.0, bore=fab.SHAFT_D):
    """Handkurbel mit Nabe + Madenschraube; Griffzapfen für M4-Schraube + gedruckte Hülse."""
    prof = g2.slot((0, 0), (arm, 0), 16).difference(g2.circle(bore + HC)).difference(g2.circle(fab.M4_CLR + HC, (arm, 0)))
    body = extrude(prof, 6)
    hub = extrude(g2.circle(18).difference(g2.circle(bore + HC)), 10, 6)
    screw = cq.Workplane("YZ").circle(fab.M3_CLR / 2).extrude(-20).translate((0, 0, 11))
    nut = cq.Workplane("XY").rect(fab.M3_NUT_H + 0.3, fab.M3_NUT_AF + 0.3).extrude(10) \
        .translate((-(bore / 2 + 2.0 + fab.M3_NUT_H / 2), 0, 11 - (fab.M3_NUT_AF + 0.3) / 2))
    return body.union(hub).cut(screw).cut(nut)


def griffhuelse():
    return extrude(g2.circle(14).difference(g2.circle(fab.M4_CLR + 0.3 + HC)), 30)


def hub_part(profile2d, width, bore=fab.SHAFT_D, hub_d=18.0, hub_h=10.0, smooth=False):
    """Beliebige 2D-Scheibe (Nocken, Klinkenrad) mit Nabe + M3-Madenschraube."""
    body = extrude(profile2d.difference(g2.circle(bore + HC)), width, smooth=smooth)
    hub = extrude(g2.circle(hub_d).difference(g2.circle(bore + HC)), hub_h, width)
    zc = width + hub_h / 2
    screw = cq.Workplane("YZ").circle(fab.M3_CLR / 2).extrude(hub_d).translate((0, 0, zc))
    nut = cq.Workplane("XY").rect(fab.M3_NUT_H + 0.3, fab.M3_NUT_AF + 0.3).extrude(hub_h) \
        .translate((bore / 2 + 2.0 + fab.M3_NUT_H / 2, 0, zc - (fab.M3_NUT_AF + 0.3) / 2))
    return body.union(hub).cut(screw).cut(nut)


def tube(d_out, d_in, length):
    return extrude(g2.circle(d_out).difference(g2.circle(d_in + HC)), length)
