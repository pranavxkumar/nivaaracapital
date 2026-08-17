import streamlit as st

st.set_page_config(page_title="Financial Planner | Nivaara Capital", page_icon="🎯", layout="wide")


# ---------- DETERMINISTIC MATH (UNCHANGED — DO NOT MODIFY) ----------
def calculate_future_value(pv, rate, years):
    return pv * (1 + rate) ** years


def calculate_required_sip(fv, rate, years):
    if rate == 0:
        return fv / (years * 12)
    monthly_rate = rate / 12
    months = years * 12
    return (fv * monthly_rate) / (((1 + monthly_rate) ** months) - 1)


# =========================================================
# DARK THEME CSS (matches app.py)
# =========================================================
st.markdown(
    """
    <style>
    .stApp { background-color: #0b0e13; color: #e6e6e6; }
    [data-testid="stSidebar"] { background-color: #10141b; }
    .nv-navbar {
        padding: 14px 28px;
        background-color: #12161f;
        border: 1px solid #1f2530;
        border-radius: 14px;
        margin-bottom: 20px;
    }
    .nv-navbar span { font-size: 1.3rem; font-weight: 700; color: #f5f5f5; }
    .nv-navbar span.gold { color: #d4af37; }
    .nv-card {
        background-color: #12161f;
        border: 1px solid #1f2530;
        border-radius: 14px;
        padding: 22px 26px;
        margin-bottom: 10px;
    }
    [data-testid="stMetricValue"] { color: #f5f5f5; }
    [data-testid="stMetricLabel"] { color: #9aa3af; }
    hr { border-color: #1f2530; }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    "<div class='nv-navbar'><span>🏛️ NIVAARA</span> <span class='gold'>CAPITAL</span></div>",
    unsafe_allow_html=True
)

# ---------- HEADER ----------
st.title("🎯 Financial Goal Planner")
st.caption("Model any life goal into an inflation-adjusted target and a monthly deployment plan.")
st.divider()

# ---------- INPUTS (SIDEBAR) ----------
with st.sidebar:
    st.header("Goal Parameters")

    with st.expander("📌 Goal Details", expanded=True):
        goal_name = st.text_input("Goal Name", value="Retirement Corpus")
        current_cost = st.number_input(
            "Current Cost (₹)", min_value=0.0, value=2_500_000.0, step=50_000.0, format="%.2f"
        )
        years = st.number_input("Years to Goal", min_value=1, value=15, step=1)

    with st.expander("📈 Assumptions", expanded=True):
        inflation_pct = st.slider("Expected Inflation (%)", 0.0, 15.0, 6.0, step=0.25)
        return_pct = st.slider("Expected Annual Return (%)", 0.0, 25.0, 12.0, step=0.25)

# ---------- CALCULATIONS (UNCHANGED LOGIC) ----------
inflation_rate = inflation_pct / 100
return_rate = return_pct / 100

future_value = calculate_future_value(current_cost, inflation_rate, years)
required_sip = calculate_required_sip(future_value, return_rate, years)

# ---------- RESULTS DASHBOARD ----------
st.subheader(f"Plan Summary — {goal_name}")

metric_col1, metric_col2, metric_col3 = st.columns(3)

with metric_col1:
    st.metric("Current Cost", f"₹{current_cost:,.0f}")

with metric_col2:
    st.metric(
        "Inflation-Adjusted Target",
        f"₹{future_value:,.0f}",
        delta=f"+₹{future_value - current_cost:,.0f} over {years} yrs"
    )

with metric_col3:
    st.metric(
        "Required Monthly Deployment",
        f"₹{required_sip:,.0f}",
        delta="per month, SIP"
    )

st.divider()

# ---------- DETAIL BREAKDOWN ----------
with st.expander("🔍 View Calculation Breakdown", expanded=False):
    detail_col1, detail_col2 = st.columns(2)

    with detail_col1:
        st.markdown("**Future Value Assumptions**")
        st.write(f"- Present Value: ₹{current_cost:,.2f}")
        st.write(f"- Inflation Rate: {inflation_pct:.2f}%")
        st.write(f"- Time Horizon: {years} years")
        st.write(f"- **Future Value: ₹{future_value:,.2f}**")

    with detail_col2:
        st.markdown("**SIP Assumptions**")
        st.write(f"- Target Corpus: ₹{future_value:,.2f}")
        st.write(f"- Expected Annual Return: {return_pct:.2f}%")
        st.write(f"- Investment Horizon: {years * 12} months")
        st.write(f"- **Required Monthly SIP: ₹{required_sip:,.2f}**")

st.caption("Projections are deterministic estimates based on the assumptions above and are not guarantees of future performance.")
