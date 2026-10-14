import math
import streamlit as st

# ==========================================
# CONSTANTS
# ==========================================
DENSITY_WATER = 1000.0  # kg/m^3
GRAVITY = 9.81  # m/s^2

# ==========================================
# CORE CALCULATION FUNCTIONS
# ==========================================


def calculate_hydraulic_power(discharge: float, head: float) -> float:
    """Calculates Hydraulic Power (Ph) in Watts."""
    return DENSITY_WATER * GRAVITY * discharge * head


def calculate_shaft_power(torque: float, speed_rpm: float) -> float:
    """Calculates Shaft Power (Ps) in Watts from mechanical parameters."""
    omega = (2 * math.pi * speed_rpm) / 60.0
    return torque * omega


def calculate_overall_efficiency(
    shaft_power: float, hydraulic_power: float
) -> float:
    """Calculates Overall Efficiency (eta) as a percentage."""
    if hydraulic_power == 0:
        return 0.0
    return (shaft_power / hydraulic_power) * 100.0


def calculate_discharge_required(
    target_power: float, head: float, efficiency_percent: float
) -> float:
    """Calculates the discharge (Q) required in m^3/s for a desired shaft power output."""
    efficiency_decimal = efficiency_percent / 100.0
    denominator = efficiency_decimal * DENSITY_WATER * GRAVITY * head
    if denominator == 0:
        return 0.0
    return target_power / denominator


# ==========================================
# STREAMLIT UI LAYOUT
# ==========================================
st.set_page_config(
    page_title="Hydraulic Turbine Calculator", page_icon="🌊", layout="centered"
)

st.title("🌊 Hydraulic Turbine Calculator")
st.markdown("Perform hydraulic and mechanical power calculations for turbines.")

# Navigation via Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "💧 Hydraulic Power",
        "⚙️ Shaft Power",
        "📈 Efficiency",
        "🚰 Required Discharge",
        "📊 All-in-One",
    ]
)

# ------------------------------------------
# TAB 1: Hydraulic Power
# ------------------------------------------
with tab1:
    st.header("Calculate Hydraulic Power ($P_h$)")
    st.latex(r"P_h = \rho \cdot g \cdot Q \cdot H")

    col1, col2 = st.columns(2)
    with col1:
        q_val = st.number_input(
            "Discharge $Q$ ($m^3/s$)",
            min_value=0.0,
            value=1.5,
            step=0.1,
            key="ph_q",
        )
    with col2:
        h_val = st.number_input(
            "Net Head $H$ (m)", min_value=0.0, value=25.0, step=0.5, key="ph_h"
        )

    p_h_watts = calculate_hydraulic_power(q_val, h_val)
    p_h_kw = p_h_watts / 1000.0
    p_h_mw = p_h_kw / 1000.0

    st.subheader("Results")
    m1, m2 = st.columns(2)
    m1.metric(label="Hydraulic Power (kW)", value=f"{p_h_kw:,.2f} kW")
    m2.metric(label="Hydraulic Power (MW)", value=f"{p_h_mw:,.3f} MW")

# ------------------------------------------
# TAB 2: Shaft Power
# ------------------------------------------
with tab2:
    st.header("Calculate Shaft Power ($P_s$)")
    st.latex(r"P_s = \frac{2 \pi \cdot N \cdot T}{60}")

    col1, col2 = st.columns(2)
    with col1:
        t_val = st.number_input(
            "Torque $T$ ($N \cdot m$)",
            min_value=0.0,
            value=5000.0,
            step=100.0,
            key="ps_t",
        )
    with col2:
        n_val = st.number_input(
            "Rotational Speed $N$ (RPM)",
            min_value=0.0,
            value=500.0,
            step=10.0,
            key="ps_n",
        )

    p_s_watts = calculate_shaft_power(t_val, n_val)
    p_s_kw = p_s_watts / 1000.0
    hp_val = p_s_kw * 1.34102  # Horsepower conversion

    st.subheader("Results")
    m1, m2 = st.columns(2)
    m1.metric(label="Shaft Power (kW)", value=f"{p_s_kw:,.2f} kW")
    m2.metric(label="Mechanical Power (HP)", value=f"{hp_val:,.2f} HP")

# ------------------------------------------
# TAB 3: Overall Efficiency
# ------------------------------------------
with tab3:
    st.header("Calculate Overall Efficiency ($\eta$)")
    st.latex(r"\eta = \left( \frac{P_s}{P_h} \right) \times 100")

    col1, col2 = st.columns(2)
    with col1:
        ps_kw_input = st.number_input(
            "Shaft Power $P_s$ (kW)",
            min_value=0.0,
            value=300.0,
            step=10.0,
            key="eff_ps",
        )
    with col2:
        ph_kw_input = st.number_input(
            "Hydraulic Power $P_h$ (kW)",
            min_value=0.01,
            value=367.87,
            step=10.0,
            key="eff_ph",
        )

    eff_res = calculate_overall_efficiency(ps_kw_input, ph_kw_input)

    st.subheader("Results")
    st.metric(label="Overall Efficiency", value=f"{eff_res:.2f} %")
    if eff_res > 100:
        st.warning(
            "⚠️ Efficiency exceeds 100%. Please check your power input values."
        )

# ------------------------------------------
# TAB 4: Discharge Required
# ------------------------------------------
with tab4:
    st.header("Calculate Discharge Required ($Q$)")
    st.latex(r"Q = \frac{P_s}{\eta \cdot \rho \cdot g \cdot H}")

    col1, col2, col3 = st.columns(3)
    with col1:
        p_target_kw = st.number_input(
            "Target Shaft Power (kW)",
            min_value=0.0,
            value=300.0,
            step=10.0,
            key="req_p",
        )
    with col2:
        h_req_val = st.number_input(
            "Net Head $H$ (m)",
            min_value=0.01,
            value=25.0,
            step=0.5,
            key="req_h",
        )
    with col3:
        eff_req_val = st.number_input(
            "Overall Efficiency (%)",
            min_value=0.01,
            max_value=100.0,
            value=85.0,
            step=1.0,
            key="req_eff",
        )

    q_required = calculate_discharge_required(
        p_target_kw * 1000.0, h_req_val, eff_req_val
    )

    st.subheader("Results")
    st.metric(
        label="Required Flow Rate ($Q$)", value=f"{q_required:.3f} m³/s"
    )

# ------------------------------------------
# TAB 5: All-in-One Analysis
# ------------------------------------------
with tab5:
    st.header("Complete Turbine Assessment")
    st.markdown("Analyze hydraulic power, shaft power, and efficiency together.")

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Hydraulic Input")
        q_all = st.number_input(
            "Discharge $Q$ ($m^3/s$)", min_value=0.0, value=2.0, key="all_q"
        )
        h_all = st.number_input(
            "Net Head $H$ (m)", min_value=0.0, value=30.0, key="all_h"
        )

    with c2:
        st.subheader("Mechanical Output")
        t_all = st.number_input(
            "Torque $T$ ($N \cdot m$)", min_value=0.0, value=8000.0, key="all_t"
        )
        n_all = st.number_input(
            "Speed $N$ (RPM)", min_value=0.0, value=600.0, key="all_n"
        )

    ph_all_w = calculate_hydraulic_power(q_all, h_all)
    ps_all_w = calculate_shaft_power(t_all, n_all)

    ph_all_kw = ph_all_w / 1000.0
    ps_all_kw = ps_all_w / 1000.0
    eff_all = calculate_overall_efficiency(ps_all_kw, ph_all_kw)
    loss_kw = max(0.0, ph_all_kw - ps_all_kw)

    st.divider()
    st.subheader("Performance Summary")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Hydraulic Power", f"{ph_all_kw:,.2f} kW")
    k2.metric("Shaft Power", f"{ps_all_kw:,.2f} kW")
    k3.metric("Efficiency", f"{eff_all:.2f} %")
    k4.metric("Power Loss", f"{loss_kw:,.2f} kW")
