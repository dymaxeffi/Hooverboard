"""Evolventen-Stirnraeder und Zahnstangen (2D, shapely), parametrisch.

Ohne Profilverschiebung, Eingriffswinkel 20°. Flankenspiel wird als
Zahndickenreduktion pro Rad (je die Haelfte von ``backlash``) eingebracht.
Fuss ohne Trochoide (fuer FDM unkritisch, da Fussausrundung beim Druck
ohnehin verrundet); Mindestzaehnezahl ohne Unterschnitt am Gegenrad pruefen.
"""

from __future__ import annotations

import math

from shapely.geometry import Polygon

ALPHA = math.radians(20.0)


def inv(a: float) -> float:
    return math.tan(a) - a


def spur_gear(m: float, z: int, backlash: float = 0.15, n_flank: int = 8, n_arc: int = 4) -> Polygon:
    rp = m * z / 2
    rb = rp * math.cos(ALPHA)
    ra = rp + m
    rf = rp - 1.25 * m
    psi = math.pi / (2 * z) - (backlash / 2) / (2 * rp)  # halber Zahnwinkel am Teilkreis
    r_start = max(rb, rf)

    def phi(r):  # Winkel Flanke ab Zahnmitte
        if r <= rb:
            return psi + inv(ALPHA)
        return psi + inv(ALPHA) - inv(math.acos(rb / r))

    radii = [r_start + (ra - r_start) * i / n_flank for i in range(n_flank + 1)]
    pts = []
    for k in range(z):
        tc = 2 * math.pi * k / z
        flank = [(r, phi(r)) for r in radii]
        if rf < rb:
            flank.insert(0, (rf, phi(rb)))
        right = [(r, tc - a) for r, a in flank]
        left = [(r, tc + a) for r, a in reversed(flank)]
        a_tip0, a_tip1 = right[-1][1], left[0][1]
        tip = [(ra, a_tip0 + (a_tip1 - a_tip0) * i / n_arc) for i in range(1, n_arc)]
        a_r0 = left[-1][1]
        a_r1 = 2 * math.pi * (k + 1) / z - flank[0][1]
        root = [(rf, a_r0 + (a_r1 - a_r0) * i / n_arc) for i in range(1, n_arc)]
        for r, a in right + tip + left + root:
            pts.append((r * math.cos(a), r * math.sin(a)))
    return Polygon(pts).buffer(0)


def rack(m: float, n_teeth: int, backlash: float = 0.15, base_h: float = 6.0) -> Polygon:
    """Zahnstange, Teillinie bei y=0, Zaehne zeigen nach +y, Ruecken bei y=-(1.25m+base_h).
    Zahnmitten bei x = k * pi * m, k = 0..n_teeth-1."""
    p = math.pi * m
    ha, hf = m, 1.25 * m
    t = math.tan(ALPHA)
    s = p / 2 - backlash / 2           # Zahndicke Teillinie
    pts = [(-p / 2, -hf - base_h)]
    for k in range(n_teeth):
        xc = k * p
        pts += [(xc - s / 2 - hf * t, -hf), (xc - s / 2 + ha * t, ha), (xc + s / 2 - ha * t, ha), (xc + s / 2 + hf * t, -hf)]
    pts += [((n_teeth - 1) * p + p / 2, -hf), ((n_teeth - 1) * p + p / 2, -hf - base_h)]
    pts.insert(1, (-p / 2, -hf))
    return Polygon(pts).buffer(0)


def center_distance(m: float, z1: int, z2: int) -> float:
    return m * (z1 + z2) / 2


def contact_ratio(m: float, z1: int, z2: int) -> float:
    r1, r2 = m * z1 / 2, m * z2 / 2
    ra1, ra2 = r1 + m, r2 + m
    rb1, rb2 = r1 * math.cos(ALPHA), r2 * math.cos(ALPHA)
    a = r1 + r2
    g = math.sqrt(ra1**2 - rb1**2) + math.sqrt(ra2**2 - rb2**2) - a * math.sin(ALPHA)
    return g / (math.pi * m * math.cos(ALPHA))
