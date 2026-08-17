import streamlit as st
import pandas as pd

st.set_page_config(page_title="Financial Planner | Nivaara Capital", layout="wide")

# --- CALCULATION ENGINE ---
def calculate_future_value(pv, rate, years):
    """Calculates Future Value: FV = PV(1+r)^n"""
    return pv * (1 + rate) ** years

def calculate_required_sip(fv, rate, years):
    """Calculates Annuity / Systematic Investment Plan"""
    if rate == 0:
        return fv / (years * 12)
    monthly_rate = rate / 12
    months = years * 12
    return (fv * monthly_rate) / (((1 + monthly_rate) ** months) - 1)

# --- DASHBOARD ---
st.title("Goal-Based Financial Planner")
st.markdown("Map your required cash flows against expected market returns and inflation.")
st.markdown("---")

col1, col2, col3, col4 = st.columns(4)
goal_name = col1.text_input("Goal Name", value="Core Retirement Corpus")
current_cost = col2.number_input("Present Value (₹)", value=1000000, step=100000)
years = col3.number_input("Time Horizon (Years)", value=10.0, step=1.0)

inflation = col1.slider("Expected Inflation (%)", 0.0, 15.0, 6.0) / 100
returns = col2.slider("Expected Portfolio Return (%)", 0.0, 20.0, 10.0) / 100

if st.button("Run Simulation"):
    future_cost = calculate_future_value(current_cost, inflation, years)
    required_sip = calculate_required_sip(future_cost, returns, years)
    
    col_res1, col_res2 = st.columns(2)
    col_res1.success(f"**Inflation-Adjusted Target:** ₹ {future_cost:,.2f}")
    col_res2.info(f"**Required Monthly Deployment:** ₹ {required_sip:,.2f}")
    
    months = int(years * 12)
    sip_array = [required_sip * i for i in range(1, months + 1)]
    chart_data = pd.DataFrame({"Cumulative Capital": sip_array})
    st.area_chart(chart_data)
