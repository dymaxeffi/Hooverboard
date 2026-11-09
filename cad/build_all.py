"""Erzeugt alle Mechanikmodule: Prüfungen, Exporte (STEP/STL/DXF/SVG), Baugruppen, Doku.

    python cad/build_all.py            # alles
    python cad/build_all.py --check    # nur Prüfungen, keine Dateien
    python cad/build_all.py m02 m07    # Auswahl
"""

from __future__ import annotations

import importlib
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from mechlib import fab  # noqa: E402
from mechlib.materials import MATERIALS  # noqa: E402
from mechlib.module import OUT_DOC, ROOT  # noqa: E402

MODULES = ["m00_kalibrierung", "m01_systemplatte", "m02_stirnradstufe", "m03_linearschlitten", "m04_nockentrieb",
           "m05_kniehebelspanner", "m06_klinkengesperre", "m07_drosselklappe", "m08_blendenmessstrecke",
           "m09_membranventil", "m10_schutzgitter", "m11_schuerzenklemme", "m12_manometertafel"]

PROC = {"fdm": "FDM-Druck", "laser": "Laser 10 W", "plotter": "Schneidplotter"}


def rel(p: Path) -> str:
    return str(p.relative_to(ROOT)).replace("\\", "/")


def module_doc(mod, checks, files, cost) -> str:
    ok = sum(1 for c in checks if c[1])
    L = [f"# {mod.mid.upper()} – {mod.title}", "",
         "> Automatisch erzeugt von `cad/build_all.py` – nicht von Hand bearbeiten. Quelle: "
         f"`cad/models/{next(m for m in MODULES if m.startswith(mod.mid))}.py`", "",
         f"**Zweck:** {mod.purpose}", "",
         *( [f"![{mod.mid} Baugruppe](img/{mod.mid}.png)", "",
             f"3D-Ansicht: `cad/assemblies/{mod.mid}_baugruppe.glb` (z. B. im Browser-glTF-Viewer). "
             "Farben: blau = FDM, holz = Laser, grau = Plotter.", ""] if mod.mid != "m00" else [] ),
         f"**Status:** Konstruktion rechnerisch geprüft (Stufe B, {ok}/{len(checks)} Prüfungen bestanden). "
         "**Fertigungsfreigabe offen** bis Kalibriercoupons M00 auf dem eigenen Gerät bestanden sind "
         "(siehe `manufacturing/process_limits.md`).", "",
         "## Teile und Verfahrenswahl", "",
         "| Teil | Bezeichnung | Verfahren | Material | Stk | Orientierung / Hinweis | Begründung |",
         "|---|---|---|---|---|---|---|"]
    for p in mod.parts:
        if p.qty == 0:
            continue
        L.append(f"| {p.pid} | {p.name} | {PROC[p.process]} | {MATERIALS[p.material].name} "
                 f"({MATERIALS[p.material].status}) | {p.qty} | {p.orientation} | {p.rationale} |")
    std = [p for p in mod.parts if p.qty == 0]
    if std:
        L += ["", "Standardelemente (Stückzahl 0 hier, werden in anderen Modulen gezählt): "
              + ", ".join(f"{p.pid} {p.name}" for p in std)]
    L += ["", "## Normteile", "", "| Teil | Stk | ca. CHF/Stk |", "|---|---|---|"]
    L += [f"| {t} | {q} | {c:.2f} |" for t, q, c in mod.hardware]
    L += ["", "## Kosten (Richtwert, ANN)", "",
          f"FDM ≈ {cost['fdm_g']:.0f} g → CHF {cost['fdm']:.2f} · Sperrholz CHF {cost['laser']:.2f} · "
          f"Normteile CHF {cost['hardware']:.2f} · Plotter/Kleinmaterial CHF 0.50 · **Summe ≈ CHF {cost['total']:.2f}**", "",
          "## Montage", ""]
    L += [f"{i}. {s}" for i, s in enumerate(mod.assembly, 1)]
    L += ["", "## Funktionsprüfung (Stufe E – noch nicht durchgeführt)", "", mod.function_test, "",
          "## Rechnerische Prüfungen", "", "| Prüfung | Ergebnis | Detail |", "|---|---|---|"]
    L += [f"| {n} | {'✅' if ok_ else '❌'} | {d} |" for n, ok_, d in checks]
    L += ["", "## Dateien", ""]
    L += [f"- `{rel(f)}`" for f in files]
    return "\n".join(L) + "\n"


def overview(rows) -> str:
    L = ["# Mechanikmodule – Übersicht", "",
         "> Automatisch erzeugt von `cad/build_all.py`. Parameter: `cad/mechlib/fab.py`, Materialien: "
         "`cad/mechlib/materials.py`, Verfahrensgrenzen: `manufacturing/process_limits.md`.", "",
         "| Modul | Titel | FDM-Teile | Laserteile | Plotterteile | Prüfungen | Kosten ≈ CHF |",
         "|---|---|---|---|---|---|---|"]
    tot = 0.0
    for mod, checks, cost in rows:
        n = lambda pr: sum(p.qty for p in mod.parts if p.process == pr)
        ok = sum(1 for c in checks if c[1])
        flag = "✅" if ok == len(checks) else "❌"
        L.append(f"| [{mod.mid.upper()}]({mod.mid}.md) | {mod.title} | {n('fdm')} | {n('laser')} | {n('plotter')} | "
                 f"{flag} {ok}/{len(checks)} | {cost['total']:.0f} |")
        if mod.mid != "m00":
            tot += cost["total"]
    L += ["", f"Summe M01–M12 ≈ CHF {tot:.0f} (Richtwert; Filament, Sperrholz, Normteile; ohne Werkzeug/Strom).", "",
          "## Aktuelle Fertigungsparameter", "", "| Parameter | Wert | Status | Bedeutung |", "|---|---|---|---|"]
    for k, p in fab.all_params().items():
        L.append(f"| `{k}` | {p.value:g} {p.unit} | {p.status} | {p.note} |")
    return "\n".join(L) + "\n"


def main(argv):
    check_only = "--check" in argv
    sel = [a for a in argv if not a.startswith("-")]
    names = [m for m in MODULES if not sel or any(m.startswith(s) for s in sel)]
    rows, failed = [], []
    OUT_DOC.mkdir(parents=True, exist_ok=True)
    for name in names:
        t0 = time.time()
        mod = importlib.import_module(f"models.{name}").build()
        checks = mod.run_checks()
        cost = mod.cost()
        bad = [c for c in checks if not c[1]]
        failed += [(mod.mid, c) for c in bad]
        files = [] if check_only else mod.export()
        if not check_only:
            (OUT_DOC / f"{mod.mid}.md").write_text(module_doc(mod, checks, files, cost), encoding="utf-8")
        rows.append((mod, checks, cost))
        print(f"{mod.mid}: {len(checks) - len(bad)}/{len(checks)} Prüfungen ok, {len(files)} Dateien, "
              f"CHF {cost['total']:.2f}, {time.time() - t0:.1f} s")
        for c in bad:
            print("   ❌", c[0], "–", c[2])
    if not check_only and not sel:
        (OUT_DOC / "README.md").write_text(overview(rows), encoding="utf-8")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
