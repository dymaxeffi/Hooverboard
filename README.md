# HOVERBOARD MINI

Interdisziplinäre Entwicklung eines elektrisch betriebenen, kostengünstigen Schwebeboards für einen Piloten von 30 kg / 1.30 m, Ziel-Schwebehöhe 2–5 cm.

> **Projektstatus: Phase 0 abgeschlossen (Entwurf), wartet auf Freigabe G0.**
> Das Board existiert noch nicht. Keine Eigenschaft ist experimentell bestätigt.
> Flugfähigkeit ist ein Entwicklungsziel, keine nachgewiesene Eigenschaft.

## Grundprinzip

Physik vor Design. Messungen vor Behauptungen. Funktion vor Ästhetik.

Jede Angabe trägt eine Nachweisstufe: **B** berechnet · **S** simuliert · **E** experimentell bestätigt.
Annahmen sind in `calculations/hoverlib/parameters.py` als `ANN` markiert.

## Wichtigste Ergebnisse Phase 0 (Stufe B)

- Freier Flug (Impeller/Rotoren) braucht ≈ 23–75 kW → verworfen.
- Luftkissen mit Schürze braucht ≈ 0.2–1.5 kW elektrisch → Leitkonzept.
- Vorläufiges Konzept: **Schürzen-Luftkissen + separater, differenziell geregelter Vortrieb (K5)**.
- Grösste Unbekannte: effektiver Leckspalt der Schürze, Gebläsekennlinie, Kippverhalten → Prüfstand A0.

## Struktur

| Ordner | Inhalt |
|---|---|
| `requirements/` | Systemanforderungen, Abnahmekriterien |
| `research/` | Machbarkeit, Konzeptvergleich, Komponentenrecherche |
| `calculations/` | `hoverlib` (einzige Formel- und Parameterquelle), Abschätzungsskripte, Ergebnisse |
| `simulation/` | Dynamik- und Parametermodelle (ab Phase 3) |
| `cad/` | CadQuery-Modelle, Baugruppen, Exporte (ab Phase 4) |
| `electronics/`, `firmware/` | Elektronik und Steuerung (ab Phase 6) |
| `manufacturing/` | Fertigung mit Bambu Lab H2S |
| `procurement/` | Stückliste, Lieferanten |
| `testing/` | Prüfpläne und Messdaten |
| `safety/` | Gefahrenanalyse, rechtliche Fragen |
| `documentation/` | Projektplan, Decision Log, Risiken, offene Fragen |
| `tests/` | automatisierte Tests (pytest) |

## Verwenden

```bash
pip install pytest
python calculations/phase0_estimate.py     # erzeugt calculations/results/phase0_estimate.md
python calculations/hoverlib/decision.py   # Entscheidungsmatrix
python -m pytest
```

## Sicherheit

Es finden **keine Tests mit Personen** statt. Alle Versuche erfolgen unbemannt mit gesichertem Ballast. Ein bemannter Versuch setzt eine unabhängige Prüfung durch qualifizierte reale Fachpersonen und die Klärung der rechtlichen Anforderungen voraus (Gate G9). Die im Projekt simulierten Teamrollen ersetzen diese Prüfung nicht.

## Einstieg

1. `documentation/project_plan.md` – Phasen, Meilensteine, Abhängigkeiten
2. `documentation/risk_register.md` – Zielkonflikte und Risiken
3. `documentation/open_questions.md` – Fragen an den Auftraggeber
4. `research/physical_feasibility.md` – erste Physik
5. `testing/test_plan_A0.md` – erster Versuch ohne Person
