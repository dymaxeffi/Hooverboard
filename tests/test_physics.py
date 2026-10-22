"""Plausibilitaets- und Konsistenztests fuer hoverlib.physics.

Diese Tests pruefen Formeln gegen Handrechnungen und physikalische
Skalierungsgesetze. Sie sagen nichts ueber die Realitaet des Boards aus.
"""

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "calculations"))

from hoverlib import parameters as P  # noqa: E402
from hoverlib import physics as ph  # noqa: E402


def test_air_density_sea_level_isa():
    assert ph.air_density(0.0) == pytest.approx(1.225, abs=0.001)


def test_air_density_decreases_with_altitude_and_heat():
    assert ph.air_density(450) < ph.air_density(0)
    assert ph.air_density(0, 35) < ph.air_density(0, 15)


def test_rounded_rect_limits():
    assert ph.rounded_rect_area(0.8, 0.5, 0) == pytest.approx(0.4)
    assert ph.rounded_rect_perimeter(0.8, 0.5, 0) == pytest.approx(2.6)
    # Kreis als Grenzfall
    assert ph.rounded_rect_area(1, 1, 0.5) == pytest.approx(math.pi / 4)
    assert ph.rounded_rect_perimeter(1, 1, 0.5) == pytest.approx(math.pi)
    with pytest.raises(ValueError):
        ph.rounded_rect_area(0.5, 0.5, 0.3)


def test_cushion_pressure_hand_calc():
    # 400 N auf 0.4 m^2 -> 1000 Pa
    assert ph.cushion_pressure(400, 0.4) == pytest.approx(1000)


def test_escape_velocity_bernoulli():
    rho = 1.2
    assert ph.escape_velocity(1200, rho) == pytest.approx(math.sqrt(2000))


def test_leakage_power_scales_with_p_1_5_and_linear_gap():
    rho = 1.2
    def power(p, h):
        return ph.air_power(p, ph.leakage_flow(p, 2.0, h, 0.6, rho))
    assert power(2000, 0.003) / power(1000, 0.003) == pytest.approx(2**1.5)
    assert power(1000, 0.006) / power(1000, 0.003) == pytest.approx(2.0)


def test_electrical_power_exceeds_air_power():
    assert ph.electrical_power(100, 0.5, 0.8) == pytest.approx(250)
    with pytest.raises(ValueError):
        ph.electrical_power(100, 0, 0.8)


def test_momentum_theory_hand_calc():
    # T=100 N, A=1 m^2, rho=1.25 -> P = 1000/sqrt(2.5)
    assert ph.ideal_hover_power_open_rotor(100, 1.0, 1.25) == pytest.approx(1000 / math.sqrt(2.5))


def test_momentum_power_equals_half_thrust_times_jet_velocity():
    t, a, rho = 400.0, 0.05, 1.2
    p = ph.ideal_hover_power_open_rotor(t, a, rho)
    assert p == pytest.approx(0.5 * t * ph.jet_velocity(t, a, rho))


def test_ground_effect_validity_flag():
    k, valid = ph.ground_effect_power_factor(0.01, 0.06)
    assert not valid and k == 1.0
    k, valid = ph.ground_effect_power_factor(0.12, 0.06)
    assert valid and 0 < k < 1


def test_cg_shift():
    assert ph.combined_cg_shift(30, 0.1, 42.5) == pytest.approx(30 * 0.1 / 42.5)


def test_battery_energy():
    assert ph.battery_energy_wh(600, 600, 0.75) == pytest.approx(600 * 600 / 3600 / 0.75)


def test_skirt_concept_far_cheaper_than_free_flight_at_nominal_mass():
    """Kernaussage der Phase-0-Abschaetzung als Regressionstest."""
    rho = ph.air_density(P.SITE_ALTITUDE.value, P.SITE_TEMPERATURE.value)
    m = P.MASS_BUDGETS["nominal"].board_mass + P.PILOT_MASS.value
    w = m * ph.G
    area = ph.rounded_rect_area(0.8, 0.5, 0.12) * P.CUSHION_AREA_FRACTION.value
    perim = ph.rounded_rect_perimeter(0.8, 0.5, 0.12)
    k1 = ph.cushion_lift_power(w, area, perim, 0.005, 0.6, rho, 0.30, 0.85)["electrical_power_w"]
    a_edf = 8 * ph.annulus_area(0.12, 0.4)
    k3 = ph.real_hover_power(w, a_edf, rho, 0.6, 0.85)
    # selbst pessimistisches K1 ist >10x guenstiger als optimistisches K3
    assert k3 / k1 > 10


def test_requirements_unchanged():
    """Freigegebene Anforderungen duerfen nicht stillschweigend geaendert werden."""
    assert P.PILOT_MASS.value == 30.0 and P.PILOT_MASS.status == "REQ"
    assert P.PILOT_HEIGHT.value == 1.30
    assert (P.HOVER_HEIGHT_MIN.value, P.HOVER_HEIGHT_MAX.value) == (0.02, 0.05)


def test_estimate_script_runs(tmp_path, monkeypatch):
    import phase0_estimate as est
    monkeypatch.setattr(est, "OUT", tmp_path / "out.md")
    text = est.main()
    assert "BERECHNUNG" in text and (tmp_path / "out.md").exists()


def test_decision_weights_sum_to_100():
    from hoverlib import decision
    assert sum(decision.WEIGHTS.values()) == 100


def test_decision_knockouts_rank_last():
    from hoverlib import decision
    r = decision.ranking()
    ko_flags = [ko is not None for _, _, ko in r]
    assert ko_flags == sorted(ko_flags)
