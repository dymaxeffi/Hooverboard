"""Prüft die Lautsprecher-Auswertung (Prototyp A) gegen Handrechnung."""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "calculations" / "pressure_actuator"))
import speaker_select as ss  # noqa: E402

ROW = dict(id="T1", beschreibung="Test", d_sd_mm="33", re_ohm="3.4", nenn_w="3", staubkappe="dicht",
           polkernbohrung="nein", zustand="ok", bl_masse_g="13.2", bl_auslenkung_mm="0.2", bl_strom_a="0.09")


def test_bl_null_method():
    e = ss.evaluate(ROW)
    assert e["bl"] == pytest.approx(0.0132 * 9.81 / 0.09, rel=1e-9)
    assert e["k_s"] == pytest.approx(0.0132 * 9.81 / 0.0002, rel=1e-9)


def test_pressure_limit_and_series_resistor():
    e = ss.evaluate(ROW, "motor")
    sd = ss.A_PISTON
    assert e["p_max"] == pytest.approx(e["bl"] * ss.U_AMP / (3.4 * sd))
    assert e["p_max_capped"] == pytest.approx(ss.P_CAP, rel=1e-6)   # Vorwiderstand begrenzt exakt
    assert e["p_reach"] < e["p_max"]                                # Aufhängung frisst Kraft


def test_direct_vs_motor_area():
    d, m = ss.evaluate(ROW, "direkt"), ss.evaluate(ROW, "motor")
    assert d["sd_cm2"] == pytest.approx(math.pi * 3.3**2 / 4, rel=1e-6)
    assert m["kpa_per_a"] > d["kpa_per_a"] * 4
