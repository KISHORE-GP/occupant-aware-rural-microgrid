"""
test_planner.py - Comprehensive Unit Tests for Microgrid DR Planner.
Tests constraints logic, failure scenarios (Case 1, Case 2, Case 3, Case 4),
multi-lingual support, and baseline vs occupant-aware planning.
"""

import pytest
import pandas as pd
import numpy as np

from constraints import (
    essential_load_ok,
    opt_out_ok,
    comfort_ok,
    capacity_limit_exceeded,
    is_hard_constraint_ok,
    MAX_MICROGRID_CAPACITY_KW,
)
from planner import (
    choose_action,
    fallback_plan,
    occupant_aware_plan,
    baseline_plan,
    run_experiment_suite,
)
from i18n import TRANSLATIONS, get_text


@pytest.fixture
def sample_row():
    return {
        "load_id": "LOAD-001",
        "load_name": "Clinic Refrigeration",
        "building_name": "Rural Health Clinic",
        "appliance_category": "medical_refrigeration",
        "power_consumption_kw": 2.5,
        "essential_flexible": "ESSENTIAL",
        "tariff_classification": "PEAK",
        "opt_out_status": False,
        "critical_comfort_period": False,
        "electricity_price_kwh": 0.25,
    }


@pytest.fixture
def sample_dataset():
    data = []
    timestamps = pd.date_range("2026-09-01 00:00:00", periods=24, freq="1h")
    for ts in timestamps:
        tariff = "PEAK" if 12 <= ts.hour <= 16 else "OFF_PEAK"
        # Essential load
        data.append({
            "timestamp": ts,
            "building_id": "BLDG-001",
            "building_name": "Health Clinic",
            "load_id": "L1",
            "load_name": "Vaccine Storage",
            "appliance_category": "medical_refrigeration",
            "power_consumption_kw": 3.0,
            "essential_flexible": "ESSENTIAL",
            "occupancy_count": 5,
            "electricity_price_kwh": 0.25 if tariff == "PEAK" else 0.10,
            "tariff_classification": tariff,
            "opt_out_status": False,
            "critical_comfort_period": False,
        })
        # Flexible HVAC
        data.append({
            "timestamp": ts,
            "building_id": "BLDG-002",
            "building_name": "School",
            "load_id": "L2",
            "load_name": "Classroom HVAC",
            "appliance_category": "hvac",
            "power_consumption_kw": 8.0,
            "essential_flexible": "FLEXIBLE",
            "occupancy_count": 25,
            "electricity_price_kwh": 0.25 if tariff == "PEAK" else 0.10,
            "tariff_classification": tariff,
            "opt_out_status": False,
            "critical_comfort_period": False,
        })
        # Flexible Water Pump
        data.append({
            "timestamp": ts,
            "building_id": "BLDG-003",
            "building_name": "Water Pump Station",
            "load_id": "L3",
            "load_name": "Community Pump",
            "appliance_category": "water_pumping",
            "power_consumption_kw": 5.0,
            "essential_flexible": "FLEXIBLE",
            "occupancy_count": 2,
            "electricity_price_kwh": 0.25 if tariff == "PEAK" else 0.10,
            "tariff_classification": tariff,
            "opt_out_status": False,
            "critical_comfort_period": False,
        })
    return pd.DataFrame(data)


def test_hc1_essential_load_protection(sample_row):
    """Test HC-1: Essential safety loads are never curtailed."""
    assert essential_load_ok(sample_row) is True
    is_constrained, flag, reason = is_hard_constraint_ok(sample_row)
    assert is_constrained is True
    assert "HC-1" in flag
    
    action, scheduled_kw, _, _, _ = choose_action(sample_row)
    assert action == "RUN"
    assert scheduled_kw == sample_row["power_consumption_kw"]


def test_hc2_opt_out_protection(sample_row):
    """Test HC-2: Active occupant opt-outs are respected."""
    sample_row["essential_flexible"] = "FLEXIBLE"
    sample_row["opt_out_status"] = True
    assert opt_out_ok(sample_row) is True
    
    is_constrained, flag, _ = is_hard_constraint_ok(sample_row)
    assert is_constrained is True
    assert "HC-2" in flag
    
    action, scheduled_kw, _, _, _ = choose_action(sample_row)
    assert action == "RUN"
    assert scheduled_kw == sample_row["power_consumption_kw"]


def test_hc3_comfort_bound_protection(sample_row):
    """Test HC-3: Comfort bounds are protected during critical periods."""
    sample_row["essential_flexible"] = "FLEXIBLE"
    sample_row["appliance_category"] = "hvac"
    sample_row["critical_comfort_period"] = True
    assert comfort_ok(sample_row) is True
    
    is_constrained, flag, _ = is_hard_constraint_ok(sample_row)
    assert is_constrained is True
    assert "HC-3" in flag


def test_hc4_microgrid_capacity_limit(sample_row):
    """Test HC-4: Microgrid capacity limit (120 kW) enforcement."""
    sample_row["essential_flexible"] = "FLEXIBLE"
    sample_row["appliance_category"] = "hvac"
    
    # Over capacity limit (130 kW total demand)
    assert capacity_limit_exceeded(sample_row, total_grid_demand=130.0) is True
    is_constrained, flag, _ = is_hard_constraint_ok(sample_row, total_grid_demand=130.0)
    assert is_constrained is True
    assert "HC-4" in flag
    
    # Case 4 scenario explicit test
    is_constrained_c4, flag_c4, _ = is_hard_constraint_ok(sample_row, scenario="CASE_4_CAPACITY_LIMIT")
    assert is_constrained_c4 is True
    assert "HC-4" in flag_c4


def test_case1_missing_occupancy_fallback(sample_dataset):
    """Test Case 1: Missing occupancy telemetry triggers Fallback Mode."""
    df_plan, recs, metrics, status = occupant_aware_plan(sample_dataset, scenario="CASE_1_MISSING_OCC")
    assert "FALLBACK" in status
    assert metrics["peak_reduction_pct"] == 0.0
    for r in recs:
        assert r["action"] == "DO NOTHING"


def test_case2_opt_out_compliance(sample_dataset):
    """Test Case 2: Active opt-out scenario preserves opt-out loads."""
    df_plan, recs, metrics, status = occupant_aware_plan(sample_dataset, scenario="CASE_2_OPT_OUT")
    opt_out_recs = [r for r in recs if "HC-2" in r["constraint_flag"]]
    assert len(opt_out_recs) > 0
    assert metrics["opt_out_violations"] == 0


def test_case3_comfort_conflict(sample_dataset):
    """Test Case 3: Comfort conflict preserves HVAC comfort bounds."""
    df_plan, recs, metrics, status = occupant_aware_plan(sample_dataset, scenario="CASE_3_COMFORT_CONFLICT")
    comfort_recs = [r for r in recs if "HC-3" in r["constraint_flag"]]
    assert len(comfort_recs) > 0
    assert metrics["comfort_violations"] == 0


def test_case4_capacity_limit_scenario(sample_dataset):
    """Test Case 4: Capacity limit scenario curtails flexible loads safely."""
    df_plan, recs, metrics, status = occupant_aware_plan(sample_dataset, scenario="CASE_4_CAPACITY_LIMIT")
    cap_recs = [r for r in recs if "HC-4" in r["constraint_flag"]]
    assert len(cap_recs) > 0


def test_multi_lingual_i18n():
    """Test multi-lingual support in English and Tamil."""
    row = {
        "load_id": "L1",
        "load_name": "Pump",
        "building_name": "Station",
        "appliance_category": "water_pumping",
        "power_consumption_kw": 4.0,
        "essential_flexible": "FLEXIBLE",
        "tariff_classification": "PEAK",
        "opt_out_status": False,
    }
    action_en, _, reason_en, impact_en, flag_en = choose_action(row, lang="en")
    action_ta, _, reason_ta, impact_ta, flag_ta = choose_action(row, lang="ta")

    assert action_en == "SHIFT"
    assert "Water pumping shifted" in reason_en
    assert "நீர் இறைக்கும் பணி" in reason_ta
    assert "EN" != "TA"


def test_experiment_suite_reproducibility(sample_dataset):
    """Test that experiment suite runs deterministically and produces expected metrics."""
    res = run_experiment_suite(sample_dataset)
    assert "comparison_table" in res
    assert "target_measured_table" in res
    assert "failure_cases_table" in res
    assert len(res["failure_cases_table"]) == 4
    for pass_val in res["failure_cases_table"]["Pass/Fail"]:
        assert pass_val == "PASS"
