"""Funktionsschemata A, B, C (Prinzipskizzen, nicht massstäblich) → docs/img/*.svg"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Circle, FancyArrowPatch, Polygon, Rectangle  # noqa: E402

OUT = Path(__file__).resolve().parents[2] / "docs" / "img"
HOUSING, AIR, MEMB, DRIVE, SAFE = "#9aa5b1", "#d8ecfa", "#2a7ab8", "#e0a030", "#c0392b"


def base(title):
    fig, ax = plt.subplots(figsize=(7.5, 4.6))
    ax.set_xlim(0, 150); ax.set_ylim(-8, 92); ax.set_aspect("equal"); ax.axis("off")
    ax.set_title(title, fontsize=10, loc="left")
    return fig, ax


def label(ax, x, y, t, tx, ty, color="black"):
    ax.annotate(t, (x, y), (tx, ty), fontsize=7, color=color,
                arrowprops=dict(arrowstyle="-", lw=0.6, color=color))


def chamber_and_nozzle(ax, x0=60):
    # Druckkammer + Düse + Prüfkammer (statt Körperkontakt)
    ax.add_patch(Rectangle((x0, 30), 22, 30, fc=AIR, ec="k", lw=1))
    ax.add_patch(Rectangle((x0 + 22, 40), 14, 10, fc=AIR, ec="k", lw=1))
    ax.add_patch(Rectangle((x0 + 36, 25), 24, 40, fc="#eef6ee", ec="k", lw=1, ls="--"))
    ax.text(x0 + 48, 66.5, "Prüfadapter ≤ 1 cm³\n(Demonstrator)", ha="center", fontsize=6.5)
    ax.add_patch(Rectangle((x0 + 47, 25), 2, 4, fc="w", ec="k"))
    label(ax, x0 + 48, 27, "Leckblende A_L\n(wechselbar)", x0 + 52, 12)
    ax.add_patch(Circle((x0 + 55, 58), 2.5, fc="w", ec="k")); ax.text(x0 + 55, 58, "p", ha="center", va="center", fontsize=6)
    label(ax, x0 + 55, 55.5, "Drucksensor ±7 kPa (analog)", x0 + 64, 48)
    ax.add_patch(Rectangle((x0 + 8, 60), 4, 4, fc=SAFE, ec="k"))
    label(ax, x0 + 10, 64, "Kapillare (Bleed) +\nÜberdruckventil S1b", x0 - 2, 80, SAFE)
    ax.text(x0 + 11, 45, "V0", ha="center", fontsize=8)
    label(ax, x0 + 29, 45, "Düse", x0 + 29, 20)


def concept_a():
    fig, ax = base("Konzept A – elektromagnetische Membran (Voice-Coil)")
    ax.add_patch(Rectangle((10, 20), 50, 50, fc=HOUSING, ec="k", alpha=.4))
    ax.add_patch(Rectangle((14, 34), 12, 22, fc="#555", ec="k"))           # Magnet
    ax.add_patch(Rectangle((26, 38), 6, 14, fc=DRIVE, ec="k"))             # Spule
    ax.add_patch(Polygon([[32, 30], [56, 22], [56, 68], [32, 60]], fc="none", ec=MEMB, lw=2.5))
    ax.add_patch(Rectangle((56, 28), 4, 34, fc=MEMB, ec="k"))             # Membran/Konus
    ax.add_patch(Rectangle((50, 66), 6, 3, fc=SAFE, ec="k")); ax.add_patch(Rectangle((50, 21), 6, 3, fc=SAFE, ec="k"))
    label(ax, 53, 69, "Hubanschlag", 40, 82, SAFE)
    label(ax, 20, 45, "Magnet", 6, 80); label(ax, 29, 50, "Schwingspule", 22, 12)
    label(ax, 58, 30, "Membran/Konus\n(Sd 3.5–8 cm²)", 30, 4)
    ax.add_patch(FancyArrowPatch((63, 15), (63, 25), arrowstyle="<->", mutation_scale=8))
    ax.text(26, 72, "geschlossenes Rückvolumen", fontsize=6.5)
    chamber_and_nozzle(ax)
    ax.text(2, -6, "Verstärker (Klasse D) + MCU: Frequenz, Amplitude, Kurvenform frei; Strombegrenzung", fontsize=6.5)
    return fig


def concept_b():
    fig, ax = base("Konzept B – DC-Motor, Exzenter, Pleuel, Membran")
    ax.add_patch(Rectangle((6, 34), 18, 22, fc=DRIVE, ec="k")); ax.text(15, 45, "DC-\nMotor", ha="center", va="center", fontsize=7)
    ax.add_patch(Circle((30, 45), 5, fc="#ddd", ec="k")); ax.add_patch(Circle((31.5, 45), 1.2, fc="k"))
    label(ax, 30, 50, "Exzenter e (wechselbar)", 14, 76)
    ax.plot([31.5, 52], [45, 45], color="k", lw=3); label(ax, 42, 45, "Pleuel", 38, 28)
    ax.add_patch(Rectangle((52, 38), 3, 14, fc="#333", ec="k"))           # Mittelplatte
    ax.plot([58, 58], [26, 64], color=MEMB, lw=3); ax.plot([55, 58], [52, 64], color=MEMB, lw=2); ax.plot([55, 58], [38, 26], color=MEMB, lw=2)
    label(ax, 58, 30, "Membran Ø20 mit\nMittelplatte Ø12", 30, 6)
    ax.add_patch(Rectangle((44, 52), 4, 6, fc=SAFE, ec="k")); label(ax, 46, 58, "Hubanschlag", 40, 86, SAFE)
    ax.add_patch(Rectangle((2, 24), 56, 42, fc="none", ec=HOUSING, lw=1.5, ls=":"))
    ax.text(4, 68, "Schutzgehäuse (bewegte Teile)", fontsize=6.5)
    chamber_and_nozzle(ax)
    ax.text(2, -6, "Frequenz = Drehzahl/60, Hub fest durch e; Amplitude zusätzlich über Bleed-Nadelventil", fontsize=6.5)
    return fig


def concept_c():
    fig, ax = base("Konzept C – Mikropumpe mit Ventilsteuerung")
    ax.add_patch(Rectangle((4, 56), 20, 14, fc=DRIVE, ec="k")); ax.text(14, 63, "Pumpe\nDruck", ha="center", va="center", fontsize=6.5)
    ax.add_patch(Rectangle((4, 20), 20, 14, fc=DRIVE, ec="k")); ax.text(14, 27, "Pumpe\nSaug", ha="center", va="center", fontsize=6.5)
    ax.add_patch(Rectangle((28, 58), 10, 10, fc="#fff", ec="k")); ax.text(33, 63, "P+", ha="center", va="center", fontsize=6)
    ax.add_patch(Rectangle((28, 22), 10, 10, fc="#fff", ec="k")); ax.text(33, 27, "P−", ha="center", va="center", fontsize=6)
    label(ax, 30, 58, "Puffer + Überdruckventil", 2, 82, SAFE); label(ax, 30, 32, "Puffer + Unterdruckventil", 2, 8, SAFE)
    for y in (63, 27):
        ax.plot([24, 28], [y, y], "k"); ax.plot([38, 48], [y, y], "k")
        ax.add_patch(Rectangle((44, y - 4), 6, 8, fc="#bbb", ec="k"))
    label(ax, 47, 67, "Magnetventil 3/2", 40, 80)
    ax.plot([50, 60, 60], [63, 63, 50], "k"); ax.plot([50, 60, 60], [27, 27, 40], "k")
    ax.add_patch(Rectangle((52, 44), 6, 4, fc=SAFE, ec="k")); label(ax, 55, 44, "NO-Ventil: stromlos offen\n= Druckentlastung", 64, 8, SAFE)
    chamber_and_nozzle(ax)
    ax.text(2, -6, "Pulsform durch Ventiltakt (PWM); DC-Anteil (Dauersog) möglich → aktive Druckregelung zwingend", fontsize=6.5)
    return fig


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for n, f in (("konzept_a_voicecoil", concept_a), ("konzept_b_exzenter", concept_b), ("konzept_c_pumpe_ventile", concept_c)):
        fig = f(); fig.savefig(OUT / f"{n}.svg"); fig.savefig(OUT / f"{n}.png", dpi=110); plt.close(fig)
        print(OUT / f"{n}.svg")
