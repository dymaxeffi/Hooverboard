"""Gewichtete Entscheidungsmatrix fuer die Schwebeprinzipien.

Status: VORLAEUFIG (Phase 0). Bewertungen 1-5 sind Experteneinschaetzungen
des simulierten Teams auf Basis der Phase-0-Berechnungen und muessen in
Phase 1 mit Messdaten aus Prototyp A0 begruendet bzw. korrigiert werden.
"""

from __future__ import annotations

# Gewichte in Prozent (Summe 100). "Erforderliche Auftriebskraft" ist fuer
# alle Konzepte = Gewicht und wird daher nicht bewertet, sondern als
# Ausschlusskriterium (Schub/Gewicht-Reserve) behandelt.
WEIGHTS = {
    "Sicherheit": 20,
    "Energiebedarf": 15,
    "Stabilitaet": 10,
    "Steuerbarkeit": 10,
    "Herstellbarkeit": 10,
    "Kosten": 10,
    "Wirkungsgrad": 5,
    "Eigengewicht": 5,
    "Geraeusch": 5,
    "Reparierbarkeit": 5,
    "Untergrund": 5,
}

CONCEPTS = {
    "K1 Schuerzen-Luftkissen, Single-Fan (Vortrieb aus Kissenluft)":
        dict(zip(WEIGHTS, (4, 4, 4, 3, 2, 4, 5, 4, 3, 4, 3))),
    "K2 Luftkissen ohne Schuerze (Plenum/Randstrahl)":
        dict(zip(WEIGHTS, (3, 1, 2, 3, 3, 2, 1, 2, 1, 3, 3))),
    "K3 Mehrere Impeller mit Bodeneffekt":
        dict(zip(WEIGHTS, (2, 1, 2, 3, 3, 1, 1, 2, 1, 3, 3))),
    "K4 Aktiv geregelter Schub (freier Flug, Multicopter)":
        dict(zip(WEIGHTS, (1, 1, 2, 4, 2, 1, 1, 1, 1, 2, 4))),
    "K5 Hybrid: Schuerzen-Luftkissen + separater Vortrieb":
        dict(zip(WEIGHTS, (4, 4, 3, 4, 4, 4, 4, 3, 3, 4, 3))),
    "K5b Hybrid mit Mehrkammer-Kissen + aktiver Kammerregelung":
        dict(zip(WEIGHTS, (4, 4, 4, 4, 3, 3, 4, 3, 3, 3, 3))),
    "K6 Luftlager (Air Caster, Mikrospalt)":
        dict(zip(WEIGHTS, (4, 5, 4, 2, 3, 3, 5, 4, 4, 4, 1))),
    "K7 Wirbelstrom-Magnetschweben (leitfaehiger Boden)":
        dict(zip(WEIGHTS, (3, 2, 3, 2, 1, 1, 2, 2, 4, 2, 1))),
}

# Ausschlusskriterien (K.O.) - unabhaengig von der Punktzahl
KNOCKOUT = {
    "K3 Mehrere Impeller mit Bodeneffekt": "Leistungsbedarf ~40 kW elektrisch (Faktor >50 zu K1)",
    "K4 Aktiv geregelter Schub (freier Flug, Multicopter)":
        "~23-75 kW, Absturzrisiko aus Hoehe bei Ausfall, keine sichere Rueckfallebene",
    "K6 Luftlager (Air Caster, Mikrospalt)":
        "erfuellt 2-5 cm Schwebehoehe nicht; nur auf sehr glatten, dichten Boeden",
    "K7 Wirbelstrom-Magnetschweben (leitfaehiger Boden)":
        "braucht Spezialboden aus Metall; nicht allgemein einsetzbar",
}


def weighted_score(scores: dict) -> float:
    """Gewichtete Punktzahl normiert auf 0-100 (5 Punkte = 100)."""
    if set(scores) != set(WEIGHTS):
        raise ValueError("Bewertung muss alle Kriterien enthalten")
    if any(not 1 <= s <= 5 for s in scores.values()):
        raise ValueError("Bewertungen muessen zwischen 1 und 5 liegen")
    return sum(WEIGHTS[k] * s for k, s in scores.items()) / 5.0


def ranking() -> list[tuple[str, float, str | None]]:
    rows = [(name, weighted_score(s), KNOCKOUT.get(name)) for name, s in CONCEPTS.items()]
    return sorted(rows, key=lambda r: (r[2] is not None, -r[1]))


def markdown_table() -> str:
    head = "| Konzept | " + " | ".join(f"{k} ({w})" for k, w in WEIGHTS.items()) + " | Score | K.O. |"
    sep = "|---|" + "---:|" * len(WEIGHTS) + "---:|---|"
    lines = [head, sep]
    for name, score, ko in ranking():
        s = CONCEPTS[name]
        lines.append(f"| {name} | " + " | ".join(str(s[k]) for k in WEIGHTS)
                     + f" | **{score:.0f}** | {ko or '–'} |")
    return "\n".join(lines)


if __name__ == "__main__":
    print(markdown_table())
