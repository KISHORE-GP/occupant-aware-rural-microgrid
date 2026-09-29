"""
constraints.py - Simple Hard and Soft Constraints Logic for Microgrid DR Planner.
Contains function-based constraint evaluation:
- Hard constraints: essential loads (HC-1), active opt-outs (HC-2), comfort bounds (HC-3), microgrid capacity (HC-4).
- Soft constraints: comfort penalty, tariff cost benefit, shift inconvenience.
"""

from typing import Dict, Any, Tuple
from i18n import get_text

MAX_MICROGRID_CAPACITY_KW = 120.0


def essential_load_ok(row: Dict[str, Any]) -> bool:
    """HC-1: Essential safety loads must never be curtailed."""
    return row.get("essential_flexible", "") == "ESSENTIAL"


def opt_out_ok(row: Dict[str, Any], scenario: str = "NORMAL") -> bool:
    """HC-2: Active occupant opt-outs must be respected."""
    val = row.get("opt_out_status", False)
    if isinstance(val, str):
        is_opt_out = val.lower() in ["true", "1", "yes"]
    else:
        is_opt_out = bool(val)

    category = row.get("appliance_category", "")
    if scenario == "CASE_2_OPT_OUT" and category in ["hvac", "water_pumping"]:
        is_opt_out = True
    return is_opt_out


def comfort_ok(row: Dict[str, Any], scenario: str = "NORMAL") -> bool:
    """HC-3: Hard thermal bounds & critical comfort windows must be protected."""
    if scenario == "CASE_3_COMFORT_CONFLICT" or row.get("critical_comfort_period", False):
        return True
    return False


def capacity_limit_exceeded(row: Dict[str, Any], total_grid_demand: float = 0.0, scenario: str = "NORMAL") -> bool:
    """HC-4: Microgrid total demand must not exceed safe limit (120 kW)."""
    if row.get("essential_flexible", "") == "ESSENTIAL":
        return False
    if scenario == "CASE_4_CAPACITY_LIMIT" or total_grid_demand > MAX_MICROGRID_CAPACITY_KW:
        return True
    return False


def is_hard_constraint_ok(
    row: Dict[str, Any],
    scenario: str = "NORMAL",
    total_grid_demand: float = 0.0,
    lang: str = "en",
) -> Tuple[bool, str, str]:
    """
    Evaluates whether any Hard Constraint prevents standard curtailment or forces emergency curtailment.
    Returns (is_constrained, constraint_flag, reason).
    """
    if essential_load_ok(row):
        return True, get_text("hc1_flag", lang=lang), get_text("hc1_reason", lang=lang)

    if opt_out_ok(row, scenario):
        opt_reason = row.get('opt_out_reason', 'Preference')
        return True, get_text("hc2_flag", lang=lang), get_text("hc2_reason_fmt", lang=lang, reason=opt_reason)

    if comfort_ok(row, scenario):
        return True, get_text("hc3_flag", lang=lang), get_text("hc3_reason", lang=lang)

    if capacity_limit_exceeded(row, total_grid_demand=total_grid_demand, scenario=scenario):
        return True, get_text("hc4_flag", lang=lang), get_text("hc4_reason", lang=lang)

    return False, get_text("no_hc_flag", lang=lang), get_text("no_hc_reason", lang=lang)


def soft_penalty(row: Dict[str, Any], action: str, mode: str = "PEAK_REDUCTION") -> float:
    """
    Calculates soft constraint penalty score for candidate action.
    """
    penalty = 0.0
    category = row.get("appliance_category", "")
    tariff = row.get("tariff_classification", "OFF_PEAK")

    if action == "CURTAIL":
        penalty += 10.0 if (category == "hvac" and mode == "PEAK_REDUCTION") else 25.0
    elif action == "SHIFT":
        penalty += 2.0
    elif action == "RUN" and tariff == "PEAK":
        penalty += 15.0

    return penalty


