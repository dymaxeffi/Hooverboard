"""M08 – Blendenmessstrecke DN50 mit Wechselblenden (Prüfstand A0, BOM A0-13).

Hybrid: Ein- und Auslaufstück gedruckt (gleiches Teil, Flanschanbohrung 25.4 mm vor
Blende, Messstutzen eingeleimt); Wechselblenden gelasert (Ø exakt, graviert);
optional scharfkantige Blende aus geplottetem PET 0.19 mm auf gelasertem Stützring
(abströmseitige "Fase" = grösserer Stützring-Ø) – näher an ISO 5167 als 3-mm-Holz.
Dichtungen geplottet. Durchflusskoeffizienten MÜSSEN kalibriert werden (z. B. gegen
Flügelrad-Anemometer A0-09); Normwerte gelten für diese Geometrie nicht.
"""

from __future__ import annotations

import math

from mechlib import fab, geom2d as g2
from mechlib.airline import DN, FT, GASKET_T, OD, bolt_pts, gasket_2d, messstutzen, tube_body
from mechlib.cadbridge import xform
from mechlib.common import T, flat_pose, label
from mechlib.module import Module, Part

LEN = 100.0                  # 2·D Ein-/Auslauf je Seite (Kompromiss Bauraum/Messgüte)
TAP = 25.4                   # Flanschanbohrung
SIZES = [15, 20, 25, 30, 35, 40]
RHO, C_ANN = 1.19, 0.61      # ANN: Luft 20 °C, 450 m ü. M.; Durchflusszahl scharfkantig


def plate_2d(d, inner_extra=0.0):
    g = g2.circle(OD).union(g2.rect(24, 14, (0, OD / 2 + 4), r=2)).difference(g2.circle(d + inner_extra))
    for p in bolt_pts():
        g = g.difference(g2.circle(fab.M4_CLR, p))
    return g


def dp_at(q_ls, d):
    beta = d / DN
    a = math.pi * (d / 1000) ** 2 / 4
    v = q_ls / 1000 / (C_ANN * a) * math.sqrt(1 - beta ** 4)
    return RHO / 2 * v ** 2


def q_at(dp, d):
    beta = d / DN
    a = math.pi * (d / 1000) ** 2 / 4
    return C_ANN * a * math.sqrt(2 * dp / RHO) / math.sqrt(1 - beta ** 4) * 1000


DP_MIN, DP_MAX = 50.0, 2000.0     # sinnvoller U-Rohr-Bereich (±1 mm Ablesung ≈ 10 Pa)


def build() -> Module:
    pipe = tube_body(LEN, taps=[LEN - TAP])
    z_pl = LEN + GASKET_T
    parts = [
        Part("M08-P01", "Ein-/Auslaufstück", "fdm", "PETG", 2, shape=pipe,
             poses=[lambda wp: wp, lambda wp: xform(wp, [[1, 0, 0], [0, -1, 0], [0, 0, -1]], (0, 0, 2 * LEN + 2 * GASKET_T + T))],
             orientation="stehend, Flansch auf Bett; Messbohrung als Tropfen (stützenfrei)",
             rationale="Rohr mit Flanschen und Messboss = 3D-Form → Druck; identisches Teil zweimal, gedreht eingebaut."),
        Part("M08-P02", "Messstutzen", "fdm", "PETG", 2, shape=messstutzen(),
             poses=[(lambda zz: (lambda wp: xform(wp, [[0, 0, 1], [0, 1, 0], [-1, 0, 0]], (DN / 2 + 3 + 8 - 8.0, 0, zz))))(z)
                    for z in (LEN - TAP, LEN + 2 * GASKET_T + T + TAP)],
             orientation="stehend", rationale="Widerhaken rotationssymmetrisch → stehend gedruckt formgenau."),
        Part("M08-P05", "Flanschdichtung", "plotter", "GASKET05", 2, profile=gasket_2d(),
             poses=[flat_pose(LEN), flat_pose(LEN + GASKET_T + T)], orientation="–",
             rationale="dünne Dichtung = Plotter; keine thermische Randschädigung."),
    ]
    for i, d in enumerate(SIZES):
        tag = "abcdef"[i]
        eng = label(f"d{d} β{d / DN:.2f}".replace("0.", "."), (0, OD / 2 + 4), 3.2)
        parts.append(Part(f"M08-P03{tag}", f"Blende d{d}", "laser", "PLY3", 1, profile=plate_2d(d), engrave=eng,
                          poses=[flat_pose(z_pl)] if d == 25 else [], orientation="flach, Gravur zuströmseitig",
                          rationale="Bohrung Ø auf ±0.05 mm (Kerf kompensiert), Satz in einem Job; Lasche mit Gravur "
                                    "verhindert Verwechslung."))
    for i, d in enumerate(SIZES):
        tag = "abcdef"[i]
        parts.append(Part(f"M08-P04{tag}", f"PET-Blende d{d} scharfkantig", "plotter", "PET019", 1,
                          profile=g2.round_inner(plate_2d(d), fab.CUT_MIN_RADIUS.value), poses=[],
                          orientation="–",
                          rationale="0.19 mm Kante ≈ scharfkantig; Plotter schneidet PET ohne Schmelze (Laser 455 nm "
                                    "schneidet klares PET nicht)."))
    parts.append(Part("M08-P06", "Stützring für PET-Blenden", "laser", "PLY3", 1,
                      profile=plate_2d(SIZES[-1], 6.0), engrave=label("STUETZ d+6", (0, OD / 2 + 4), 3.0), poses=[],
                      orientation="abströmseitig hinter PET-Blende",
                      rationale="Stützt PET-Folie gegen Δp-Durchbiegung; Ø = dmax + 6 mm wirkt als Abströmfase. "
                                "Für kleinere d zusätzliche Ringe mit d+6 nach Bedarf (Parameter)."))
    ranges = [(d, q_at(DP_MIN, d), q_at(DP_MAX, d)) for d in SIZES]
    table = ", ".join(f"d{d}: {a:.1f}–{b:.1f} l/s" for d, a, b in ranges)
    overlap = all(ranges[i + 1][1] < ranges[i][2] for i in range(len(ranges) - 1))
    checks = [
        ("β-Bereich 0.3–0.8", all(0.3 <= d / DN <= 0.8 for d in SIZES), f"β = {SIZES[0] / DN:.2f} … {SIZES[-1] / DN:.2f}"),
        ("Messbohrung 25.4 mm vor/nach Blende (Flanschanbohrung)", abs(TAP - 25.4) < 0.01, f"{TAP} mm, Bohrung Ø3.2"),
        ("Scharfkantige PET-Variante: Dicke ≤ 0.05·D", 0.19 <= 0.05 * DN,
         f"PET 0.19 mm ≤ {0.05 * DN:.1f} mm; Holzblende {T} mm ist NICHT normkonform → nur kalibriert verwenden"),
        (f"Messbereiche ({DP_MIN:.0f}–{DP_MAX:.0f} Pa) benachbarter Blenden überlappen lückenlos", overlap, table),
    ]
    return Module(
        "m08", "Blendenmessstrecke DN50 mit Wechselblenden",
        "Volumenstrommessung für die Gebläsekennlinie am Prüfstand A0: Δp über Blende mit U-Rohr (M12). "
        "Q = C·A·√(2Δp/ρ)/√(1−β⁴), C ≈ 0.61 nur als Startwert – Kalibrierung zwingend.",
        parts,
        hardware=[("M4×25 + Mutter + 2 Scheiben (Blendenflansch)", 4, 0.12), ("PU-/Silikonschlauch ID 6 mm, 2 m", 1, 3.0),
                  ("Sekundenkleber/Epoxid (Messstutzen)", 1, 0.20)],
        assembly=[
            "Messstutzen in die Sitze der beiden Rohrstücke einkleben; Bohrung Ø3.2 innen gratfrei entgraten (Grat verfälscht Δp).",
            "Einlauf (Messboss zur Blende) – Dichtung – Blende (Gravur zuströmseitig) – Dichtung – Auslauf (Messboss zur Blende).",
            "4× M4 über Kreuz handfest; Blendenlasche zeigt nach oben (Verwechslungsschutz).",
            "PET-Variante: PET-Blende zuströmseitig, Stützring abströmseitig, beide zwischen die Dichtungen.",
        ],
        checks=checks,
        function_test="Dichtheit: Auslass zu, 1 kPa Überdruck, Druckabfall < 10 % in 60 s. Kalibrierung: je Blende "
                      "5 Volumenströme gegen Anemometer (Rohr 10·D hinter Auslauf), C(Re) als Tabelle in testing/ ablegen.",
    )
