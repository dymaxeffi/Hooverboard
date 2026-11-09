"""Vorschaubilder (PNG) aller Baugruppen und Laserbögen für Doku und Sichtkontrolle.

    python cad/render_previews.py [m02 ...]
"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from mpl_toolkits.mplot3d.art3d import Poly3DCollection  # noqa: E402

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from build_all import MODULES  # noqa: E402
from mechlib.module import OUT_DOC  # noqa: E402

COL = {"fdm": (0.20, 0.45, 0.85), "laser": (0.85, 0.68, 0.42), "plotter": (0.75, 0.75, 0.75)}
LIGHT = np.array([0.4, -0.6, 0.7]) / np.linalg.norm([0.4, -0.6, 0.7])


def render(mod, path: Path):
    tris, cols = [], []
    for _, p, wp in mod.instances():
        for v in wp.vals():
            vs, fs = v.tessellate(0.2, 0.5)
            pts = np.array([[q.x, q.y, q.z] for q in vs])
            for f in fs:
                t = pts[list(f)]
                n = np.cross(t[1] - t[0], t[2] - t[0])
                ln = np.linalg.norm(n)
                shade = 0.45 + 0.55 * abs(n @ LIGHT / ln) if ln > 0 else 0.6
                tris.append(t)
                cols.append(tuple(min(1, c * shade) for c in COL[p.process]))
    if not tris:
        return False
    allp = np.concatenate(tris)
    fig = plt.figure(figsize=(6, 4.5), dpi=130)
    ax = fig.add_subplot(projection="3d")
    ax.add_collection3d(Poly3DCollection(tris, facecolors=cols, edgecolors="none"))
    lo, hi = allp.min(0), allp.max(0)
    c, r = (lo + hi) / 2, (hi - lo).max() / 2
    ax.set_xlim(c[0] - r, c[0] + r); ax.set_ylim(c[1] - r, c[1] + r); ax.set_zlim(c[2] - r, c[2] + r)
    ax.set_box_aspect((1, 1, 1)); ax.view_init(24, -58); ax.set_axis_off()
    ax.set_title(f"{mod.mid.upper()} {mod.title}\nblau = FDM · holz = Laser · grau = Plotter", fontsize=8)
    fig.tight_layout(); path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path); plt.close(fig)
    return True


def main(sel):
    for name in MODULES:
        if sel and not any(name.startswith(s) for s in sel):
            continue
        mod = importlib.import_module(f"models.{name}").build()
        ok = render(mod, OUT_DOC / "img" / f"{mod.mid}.png")
        print(name, "ok" if ok else "(keine Baugruppe)")


if __name__ == "__main__":
    main(sys.argv[1:])
