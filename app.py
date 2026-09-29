"""
app.py - Complete Streamlit Interface for Occupant-Aware Demand-Response Planner.
Features:
- Current Microgrid State (Load data, Occupancy, Comfort range, Tariff, Opt-out choices)
- Multi-Lingual UI Support (English & Tamil)
- Objective Mode Selection (Peak Reduction Mode vs Comfort Mode)
- Failure Scenario Selector (Normal, Case 1: Missing Occupancy, Case 2: User Opt-Out, Case 3: Comfort Conflict, Case 4: Capacity Limit)
- Recommended Actions Table with plain-language explanations
- Authorised Operator Override with role logging
- System Status Banner (NORMAL MODE vs FALLBACK MODE — Conservative Operation)
- Baseline vs Occupant-Aware Comparison Table
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
import streamlit as st

# Import planner logic and translations
from planner import (
    SimpleBaselineController,
    SimpleOccupantAwarePlanner,
    SimpleOverrideManager,
)
from i18n import TRANSLATIONS, get_text

# Page Setup
st.set_page_config(
    page_title="Rural Microgrid DR Planner",
    page_icon="⚡",
    layout="wide",
)

# Session state for override log
if "override_mgr" not in st.session_state:
    st.session_state.override_mgr = SimpleOverrideManager()


@st.cache_data
def load_dataset():
    data_path = Path(__file__).resolve().parent / "data.csv"
    if data_path.exists():
        df = pd.read_csv(data_path, parse_dates=["timestamp"])
    else:
        st.error("data.csv not found!")
        st.stop()
    return df.head(72 * 16).copy()  # Sample window for fast dashboard rendering


def main():
    df_raw = load_dataset()

    # -----------------------------------------------------------------
    # SIDEBAR CONTROLS
    # -----------------------------------------------------------------
    st.sidebar.header(TRANSLATIONS["en"]["sidebar_header"])

    lang_choice = st.sidebar.selectbox(
        TRANSLATIONS["en"]["select_lang"],
        options=["en", "ta"],
        format_func=lambda x: "English" if x == "en" else "தமிழ் (Tamil)",
    )
    t = TRANSLATIONS[lang_choice]

    # Failure Scenario Selector
    scenario = st.sidebar.selectbox(
        t["select_scenario"],
        options=[
            "NORMAL",
            "CASE_1_MISSING_OCC",
            "CASE_2_OPT_OUT",
            "CASE_3_COMFORT_CONFLICT",
            "CASE_4_CAPACITY_LIMIT",
        ],
        format_func=lambda x: {
            "NORMAL": t["scenario_normal"],
            "CASE_1_MISSING_OCC": t["scenario_c1"],
            "CASE_2_OPT_OUT": t["scenario_c2"],
            "CASE_3_COMFORT_CONFLICT": t["scenario_c3"],
            "CASE_4_CAPACITY_LIMIT": t["scenario_c4"],
        }[x],
    )

    st.sidebar.markdown("---")

    # Objective Mode Selector (Peak Reduction Mode vs Comfort Mode)
    mode_choice = st.sidebar.radio(
        t["obj_mode"],
        options=["PEAK_REDUCTION", "OCCUPANT_COMFORT"],
        format_func=lambda x: {
            "PEAK_REDUCTION": t["mode_peak"],
            "OCCUPANT_COMFORT": t["mode_comfort"],
        }[x],
    )

    # Header
    st.title(t["title"])

    # Controllers
    baseline = SimpleBaselineController()
    planner = SimpleOccupantAwarePlanner()

    # Execute
    df_base, metrics_base = baseline.run(df_raw)
    df_plan, recommendations, metrics_plan, system_status = planner.plan(
        df_raw, mode=mode_choice, scenario=scenario, lang=lang_choice
    )

    # -----------------------------------------------------------------
    # 1. SYSTEM STATUS BANNER (NORMAL vs FALLBACK)
    # -----------------------------------------------------------------
    if "FALLBACK" in system_status or "காப்பு" in system_status:
        st.error(f"⚠️ **{t['banner_fallback']}**")
        st.warning(t["warning_fallback"])
    else:
        st.success(f"🟢 **{t['banner_normal']}**")

    st.markdown("---")

    # -----------------------------------------------------------------
    # 2. CURRENT MICROGRID STATE
    # -----------------------------------------------------------------
    st.subheader(t["sec_state"])

    curr_df = df_raw.head(16)
    total_dem = curr_df["power_consumption_kw"].sum()
    ess_dem = curr_df[curr_df["essential_flexible"] == "ESSENTIAL"]["power_consumption_kw"].sum()
    flex_dem = curr_df[curr_df["essential_flexible"] == "FLEXIBLE"]["power_consumption_kw"].sum()
    tariff_val = curr_df["tariff_classification"].iloc[0]
    avg_occ = int(curr_df["occupancy_count"].mean()) if not curr_df["occupancy_count"].isna().all() else 0

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric(t["metric_total_dem"], f"{total_dem:.1f} kW")
    c2.metric(t["metric_peak_dem"], f"{metrics_plan['peak_demand_kw']} kW")
    c3.metric(t["metric_tariff"], tariff_val)
    c4.metric(t["metric_occ_count"], f"{avg_occ} {t['persons']}")
    c5.metric(t["metric_ess_load"], f"{ess_dem:.1f} kW")
    c6.metric(t["metric_flex_load"], f"{flex_dem:.1f} kW")

    st.markdown("---")

    # -----------------------------------------------------------------
    # 3. PLANNER RECOMMENDATIONS & EXPLANATIONS
    # -----------------------------------------------------------------
    st.subheader(t["sec_recs"])

    df_recs = pd.DataFrame(recommendations)
    if not df_recs.empty:
        df_recs_display = df_recs[[
            "action_id", "building_name", "load_name", "action",
            "reason", "peak_reduction_kw", "comfort_impact",
            "opt_out_status", "constraint_flag"
        ]].copy()

        df_recs_display.columns = [
            t["col_action_id"], t["col_bldg_name"], t["col_load_name"],
            t["col_action"], t["col_reason"], t["col_peak_red"],
            t["col_comfort_impact"], t["col_opt_status"], t["col_constraint_flag"]
        ]

        st.dataframe(df_recs_display, use_container_width=True)

    st.markdown("---")

    # -----------------------------------------------------------------
    # 4. AUTHORISED OPERATOR OVERRIDE
    # -----------------------------------------------------------------
    st.subheader(t["sec_override"])
    st.caption(t["caption_prototype"])

    with st.form("override_form"):
        col_act, col_role, col_status = st.columns(3)

        act_options = [r["action_id"] + " - " + r["load_name"] for r in recommendations] if recommendations else ["None"]
        selected_act = col_act.selectbox(t["label_select_act"], options=act_options)

        role_map = {
            t["role_microgrid_op"]: "Microgrid Operator",
            t["role_bldg_mgr"]: "Building Manager",
            t["role_admin"]: "Community Admin",
        }
        operator_role = col_role.selectbox(t["label_op_role"], options=list(role_map.keys()))

        dec_map = {
            t["dec_approve"]: "Approve",
            t["dec_reject"]: "Reject",
            t["dec_override"]: "Override",
        }
        override_status = col_status.selectbox(t["label_decision"], options=list(dec_map.keys()))

        override_reason = st.text_input(t["label_reason"], value=t["default_reason"])

        submit_override = st.form_submit_button(t["btn_submit_override"])

        if submit_override and selected_act != "None":
            act_id = selected_act.split(" - ")[0]
            load_n = selected_act.split(" - ")[1]
            rec = st.session_state.override_mgr.add_override(
                action_id=act_id,
                load_name=load_n,
                operator_role=operator_role,
                status=override_status,
                reason=override_reason,
            )
            st.success(f"Logged Override: {rec['action_id']} -> {rec['status']} by {rec['operator_role']}")

    overrides_list = st.session_state.override_mgr.get_overrides()
    if overrides_list:
        st.caption(t["recent_log"])
        st.dataframe(pd.DataFrame(overrides_list), use_container_width=True)

    st.markdown("---")

    # -----------------------------------------------------------------
    # 5. BASELINE VS OCCUPANT-AWARE COMPARISON TABLE
    # -----------------------------------------------------------------
    st.subheader(t["sec_comp"])

    comp_data = [
        {
            t["col_metric"]: t["metric_peak_kw"],
            t["col_baseline"]: metrics_base["peak_demand_kw"],
            t["col_occ_aware"]: metrics_plan["peak_demand_kw"],
        },
        {
            t["col_metric"]: t["metric_peak_pct"],
            t["col_baseline"]: f"{metrics_base['peak_reduction_pct']}%",
            t["col_occ_aware"]: f"{metrics_plan['peak_reduction_pct']}%",
        },
        {
            t["col_metric"]: t["metric_comf_viol"],
            t["col_baseline"]: metrics_base["comfort_violations"],
            t["col_occ_aware"]: metrics_plan["comfort_violations"],
        },
        {
            t["col_metric"]: t["metric_opt_viol"],
            t["col_baseline"]: metrics_base["opt_out_violations"],
            t["col_occ_aware"]: metrics_plan["opt_out_violations"],
        },
        {
            t["col_metric"]: t["metric_cost"],
            t["col_baseline"]: f"${metrics_base['total_cost']}",
            t["col_occ_aware"]: f"${metrics_plan['total_cost']}",
        },
    ]

    st.table(pd.DataFrame(comp_data))


if __name__ == "__main__":
    main()
