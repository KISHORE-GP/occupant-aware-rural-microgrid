"""
i18n.py - Internationalization & Translation Dictionary for Microgrid DR Planner.

Supports English (en) and Tamil (ta) for all UI labels, constraint flags,
explanations, warnings, operator roles, decision status, and metrics.
"""

TRANSLATIONS = {
    "en": {
        # App UI Header & Sidebar
        "title": "⚡ Occupant-Aware Demand-Response Planner for Rural Microgrid",
        "sidebar_header": "🎛️ Planning Controls",
        "select_lang": "🌐 Language / மொழி",
        "select_scenario": "Select Test Scenario",
        "scenario_normal": "Normal Operation",
        "scenario_c1": "Case 1 — Missing Occupancy",
        "scenario_c2": "Case 2 — User Opt-Out",
        "scenario_c3": "Case 3 — Comfort Conflict",
        "scenario_c4": "Case 4 — Microgrid Capacity Limit (120 kW)",
        "obj_mode": "Objective Mode",
        "mode_peak": "Peak Reduction Mode",
        "mode_comfort": "Comfort Mode",

        # Status Banners
        "banner_normal": "🟢 NORMAL MODE",
        "banner_fallback": "⚠️ FALLBACK MODE — Conservative Operation",
        "warning_fallback": "WARNING: Occupancy data missing! Switched to FALLBACK MODE — Conservative Operation.",

        # Current Microgrid State
        "sec_state": "📊 Current Microgrid State",
        "metric_total_dem": "Total Demand",
        "metric_peak_dem": "Peak Demand",
        "metric_tariff": "Tariff",
        "metric_occ_count": "Occupancy Count",
        "metric_ess_load": "Essential Load",
        "metric_flex_load": "Flexible Load",
        "persons": "persons",

        # Recommendations
        "sec_recs": "🤖 Planner Recommendations & Explanations",
        "col_action_id": "Action ID",
        "col_bldg_name": "Building Name",
        "col_load_name": "Load Name",
        "col_action": "Action",
        "col_reason": "Explanation / Rationale",
        "col_peak_red": "Peak Reduction (kW)",
        "col_comfort_impact": "Comfort Impact",
        "col_opt_status": "Opt-Out Status",
        "col_constraint_flag": "Constraint Flag",

        # Operator Override
        "sec_override": "✍️ Authorised Operator Override",
        "caption_prototype": "Prototype Authorization Mechanism",
        "label_select_act": "Select Action to Override",
        "label_op_role": "Operator Role",
        "label_decision": "Decision",
        "label_reason": "Override Reason",
        "default_reason": "Manual operator intervention for local preference",
        "btn_submit_override": "Submit Operator Override",
        "role_microgrid_op": "Microgrid Operator",
        "role_bldg_mgr": "Building Manager",
        "role_admin": "Community Admin",
        "dec_approve": "Approve",
        "dec_reject": "Reject",
        "dec_override": "Override",
        "recent_log": "Recent Operator Overrides Log:",

        # Comparison Table
        "sec_comp": "⚖️ Baseline vs Occupant-Aware Comparison",
        "metric_peak_kw": "Peak Demand (kW)",
        "metric_peak_pct": "Peak Reduction (%)",
        "metric_comf_viol": "Comfort Violations",
        "metric_opt_viol": "Opt-Out Violations",
        "metric_cost": "Electricity Cost ($)",
        "col_metric": "Metric",
        "col_baseline": "Baseline",
        "col_occ_aware": "Occupant-Aware",

        # Constraints & Explanations
        "hc1_flag": "HC-1: Essential Load Protection",
        "hc1_reason": "HARD CONSTRAINT: Essential safety load protected.",
        "hc2_flag": "HC-2: Active Opt-Out Honored",
        "hc2_reason_fmt": "HARD CONSTRAINT: Active occupant opt-out honored ({reason}).",
        "hc3_flag": "HC-3: Thermal Bound Protected",
        "hc3_reason": "HARD CONSTRAINT: Comfort bound protected. Cannot curtail HVAC during critical comfort period.",
        "hc4_flag": "HC-4: Microgrid Capacity Limit Exceeded",
        "hc4_reason": "HARD CONSTRAINT: Microgrid capacity limit (120 kW) exceeded. Flexible load curtailed to protect transformer stability.",
        "no_hc_flag": "None",
        "no_hc_reason": "No hard constraint violation.",

        "shift_water_reason": "Peak tariff window. Water pumping shifted 30 mins to off-peak; storage buffered.",
        "shift_water_impact": "Zero (Water Tank Buffered)",
        "shift_water_flag": "SC-1: Soft Shift Preference",

        "curtail_hvac_reason": "Peak tariff window. HVAC output trimmed by 60% during peak tariff.",
        "curtail_hvac_impact": "Minor Thermal Drift (+1.2°C)",
        "curtail_hvac_flag": "SC-2: Comfort Penalty Trade-off",

        "curtail_flex_reason": "Peak tariff window. Flexible appliance power reduced by 50%.",
        "curtail_flex_impact": "Low",
        "curtail_flex_flag": "SC-3: Tariff Cost Reduction",

        "comfort_hvac_reason": "Comfort Mode Active: HVAC fully maintained for preferred indoor temperature.",
        "comfort_hvac_impact": "Optimal (Zero Drift)",
        "comfort_hvac_flag": "SC-4: Comfort Protection",

        "comfort_water_reason": "Comfort Mode Active: Water pumping shifted without occupant disruption.",
        "comfort_water_impact": "Zero",
        "comfort_water_flag": "SC-1: Soft Shift Preference",

        "comfort_flex_reason": "Comfort Mode Active: Disruption minimized.",
        "comfort_flex_impact": "Zero",
        "comfort_flex_flag": "SC-4: Disruption Minimization",

        "normal_op_reason_fmt": "Normal operation during {tariff} tariff window.",
        "fallback_reason": "FALLBACK MODE: Conservative operation active; occupancy unknown.",
        "fallback_status": "FALLBACK MODE — Conservative Operation",
        "fallback_flag": "FB-1: Conservative Fallback",
        "fallback_impact": "Safe Default",

        "opt_active": "Active",
        "opt_none": "None",
        "impact_none": "None",
        "impact_preserved": "None (Preserved)",
        "impact_protected": "Protected (Comfort Hard Bound)",
        "normal_status": "NORMAL MODE",
    },
    "ta": {
        # App UI Header & Sidebar
        "title": "⚡ கிராமப்புற நுண்மின்தொடருக்கான பயன்பாட்டாளர்-அறிந்த மின்தேவை-பதில் திட்டமிடுபவர்",
        "sidebar_header": "🎛️ திட்டமிடல் கட்டுப்பாடுகள்",
        "select_lang": "🌐 Language / மொழி",
        "select_scenario": "சோதனை சூழ்நிலையைத் தேர்ந்தெடுக்கவும்",
        "scenario_normal": "இயல்புநிலை இயக்கம்",
        "scenario_c1": "வழக்கு 1 — விடுபட்ட பயன்பாட்டாளர் தரவு",
        "scenario_c2": "வழக்கு 2 — பயனர் விலகல் (Opt-Out)",
        "scenario_c3": "வழக்கு 3 — வெப்பநிலை வசதி முரண்பாடு",
        "scenario_c4": "வழக்கு 4 — நுண்மின் திறன் எல்லை (120 kW)",
        "obj_mode": "குறிக்கோள் முறை",
        "mode_peak": "உச்ச மின்தேவை குறைப்பு முறை",
        "mode_comfort": "வசதி முறை",

        # Status Banners
        "banner_normal": "🟢 இயல்பு நிலை",
        "banner_fallback": "⚠️ காப்பு நிலை — பாதுகாப்பான இயக்கம்",
        "warning_fallback": "எச்சரிக்கை: பயன்பாட்டாளர் தரவு இல்லை! காப்பு நிலைக்கு மாற்றப்பட்டது.",

        # Current Microgrid State
        "sec_state": "📊 தற்போதைய நுண்மின்நிலை",
        "metric_total_dem": "மொத்த மின்தேவை",
        "metric_peak_dem": "உச்ச மின்தேவை",
        "metric_tariff": "மின்சாரக் கட்டணம்",
        "metric_occ_count": "பயன்பாட்டாளர் எண்ணிக்கை",
        "metric_ess_load": "அத்தியாவசியப் பயன்பாடு",
        "metric_flex_load": "மாற்றத்தக்கப் பயன்பாடு",
        "persons": "நபர்கள்",

        # Recommendations
        "sec_recs": "🤖 திட்டமிடுபவரின் பரிந்துரைகளும் விளக்கங்களும்",
        "col_action_id": "செயல்பாட்டு எண்",
        "col_bldg_name": "கட்டிடத்தின் பெயர்",
        "col_load_name": "சாதனத்தின் பெயர்",
        "col_action": "செயல்பாடு",
        "col_reason": "விளக்கம் / நியாயப்படுத்துதல்",
        "col_peak_red": "உச்ச குறைப்பு (kW)",
        "col_comfort_impact": "வெப்பநிலை வசதி தாக்கம்",
        "col_opt_status": "விலகல் நிலை",
        "col_constraint_flag": "கட்டுப்பாடு கொடி",

        # Operator Override
        "sec_override": "✍️ அதிகாரமளிக்கப்பட்ட இயக்குபவர் மாற்றம் (Override)",
        "caption_prototype": "அதிகாரமளிப்பு பொறிமுறை முன்மாதிரி",
        "label_select_act": "மாற்ற வேண்டிய செயல்பாட்டைத் தேர்ந்தெடுக்கவும்",
        "label_op_role": "இயக்குபவர் பொறுப்பு",
        "label_decision": "முடிவு",
        "label_reason": "காரணம்",
        "default_reason": "உள்ளூர் தேவைக்காக கையால் செய்யப்பட்ட மாற்றம்",
        "btn_submit_override": "இயக்குபவர் மாற்றத்தைச் சமர்ப்பி",
        "role_microgrid_op": "நுண்மின் இயக்குபவர்",
        "role_bldg_mgr": "கட்டிட மேலாளர்",
        "role_admin": "சமுதாய நிர்வாகி",
        "dec_approve": "அனுமதி",
        "dec_reject": "நிராகரிப்பு",
        "dec_override": "மாற்றம்",
        "recent_log": "சமீபத்திய இயக்குபவர் மாற்றங்களின் பதிவேடு:",

        # Comparison Table
        "sec_comp": "⚖️ அடிப்படை vs பயன்பாட்டாளர்-அறிந்த ஒப்பீடு",
        "metric_peak_kw": "உச்ச மின்தேவை (kW)",
        "metric_peak_pct": "உச்ச குறைப்பு (%)",
        "metric_comf_viol": "வெப்பநிலை வசதி மீறல்கள்",
        "metric_opt_viol": "விலகல் தேர்வு மீறல்கள்",
        "metric_cost": "மின்சார செலவு ($)",
        "col_metric": "அளவுரு",
        "col_baseline": "அடிப்படை",
        "col_occ_aware": "பயன்பாட்டாளர்-அறிந்த",

        # Constraints & Explanations
        "hc1_flag": "HC-1: அத்தியாவசிய பயன்பாட்டு பாதுகாப்பு",
        "hc1_reason": "கடுமையான கட்டுப்பாடு: அத்தியாவசிய பாதுகாப்பு பயன்பாடு பாதுகாக்கப்பட்டது.",
        "hc2_flag": "HC-2: பயன்பாட்டாளர் விலகல் தேர்வு மதிக்கப்பட்டது",
        "hc2_reason_fmt": "கடுமையான கட்டுப்பாடு: பயனர் விலகல் தேர்வு ({reason}) மதிக்கப்பட்டது.",
        "hc3_flag": "HC-3: வெப்பநிலை பாதுகாப்பு எல்லை",
        "hc3_reason": "கடுமையான கட்டுப்பாடு: வெப்பநிலை பாதுகாப்பு எல்லை பாதுகாக்கப்பட்டது. முக்கிய நேரத்தில் குளிர்சாதனத்தை குறைக்க முடியாது.",
        "hc4_flag": "HC-4: நுண்மின் திறன் எல்லை மீறப்பட்டது (120 kW)",
        "hc4_reason": "கடுமையான கட்டுப்பாடு: நுண்மின் திறன் எல்லை (120 kW) மீறப்பட்டது. மின்மாற்றி பாதுகாப்பிற்காக பயன்பாடு குறைக்கப்பட்டது.",
        "no_hc_flag": "எதுவுமில்லை",
        "no_hc_reason": "கடுமையான கட்டுப்பாடு மீறல் இல்லை.",

        "shift_water_reason": "உச்ச கட்டண நேரம். நீர் இறைக்கும் பணி 30 நிமிடங்கள் தள்ளிவைக்கப்பட்டது; நீர் சேமிப்பு பயன்படுத்தப்பட்டது.",
        "shift_water_impact": "பூஜ்ஜியம் (நீர் சேமிப்பு பாதுகாப்பு)",
        "shift_water_flag": "SC-1: தள்ளிவைப்பு முன்னுரிமை",

        "curtail_hvac_reason": "உச்ச கட்டண நேரம். உச்ச நேரத்தில் குளிர்சாதன பயன்பாடு 60% குறைக்கப்பட்டது.",
        "curtail_hvac_impact": "சிறிய வெப்பநிலை மாற்றம் (+1.2°C)",
        "curtail_hvac_flag": "SC-2: வெப்பநிலை வசதி ஈடுசெயல்",

        "curtail_flex_reason": "உச்ச கட்டண நேரம். மாற்றத்தக்க சாதனங்களின் பயன்பாடு 50% குறைக்கப்பட்டது.",
        "curtail_flex_impact": "குறைவு",
        "curtail_flex_flag": "SC-3: கட்டண செலவு குறைப்பு",

        "comfort_hvac_reason": "வசதி முறை செயல்பாட்டில்: விரும்பிய வெப்பநிலையை பராமரிக்க குளிர்சாதனம் முழுமையாக இயங்குகிறது.",
        "comfort_hvac_impact": "சிறந்தது (மாற்றமில்லை)",
        "comfort_hvac_flag": "SC-4: வெப்பநிலை பாதுகாப்பு",

        "comfort_water_reason": "வசதி முறை செயல்பாட்டில்: பயன்பாட்டாளருக்கு இடையூறின்றி நீர் இறைக்கும் பணி தள்ளிவைக்கப்பட்டது.",
        "comfort_water_impact": "பூஜ்ஜியம்",
        "comfort_water_flag": "SC-1: தள்ளிவைப்பு முன்னுரிமை",

        "comfort_flex_reason": "வசதி முறை செயல்பாட்டில்: இடையூறு குறைக்கப்பட்டது.",
        "comfort_flex_impact": "பூஜ்ஜியம்",
        "comfort_flex_flag": "SC-4: இடையூறு குறைப்பு",

        "normal_op_reason_fmt": "{tariff} கட்டண நேரத்தில் வழக்கமான இயக்கம்.",
        "fallback_reason": "காப்பு நிலை: பாதுகாப்பான இயக்கம் செயல்பாட்டில்; பயன்பாட்டாளர் எண்ணிக்கை தெரியவில்லை.",
        "fallback_status": "காப்பு நிலை — பாதுகாப்பான இயக்கம்",
        "fallback_flag": "FB-1: பாதுகாப்பான காப்பு நிலை",
        "fallback_impact": "பாதுகாப்பான இயல்புநிலை",

        "opt_active": "செயலில்",
        "opt_none": "எதுவுமில்லை",
        "impact_none": "எதுவுமில்லை",
        "impact_preserved": "பாதுகாக்கப்பட்டது (மாற்றமில்லை)",
        "impact_protected": "பாதுகாக்கப்பட்டது (வெப்பநிலை எல்லை)",
        "normal_status": "இயல்பு நிலை",
    },
}


def get_text(key: str, lang: str = "en", **kwargs) -> str:
    lang_dict = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
    text = lang_dict.get(key, TRANSLATIONS["en"].get(key, key))
    if kwargs:
        text = text.format(**kwargs)
    return text
