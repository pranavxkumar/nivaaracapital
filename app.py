import streamlit as st
import pandas as pd

# --- CALCULATION ENGINE ---
def calculate_future_value(pv, rate, years):
    return pv * (1 + rate) ** years

def calculate_required_sip(fv, rate, years):
    if rate == 0:
        return fv / (years * 12)
    monthly_rate = rate / 12
    months = years * 12
    return (fv * monthly_rate) / (((1 + monthly_rate) ** months) - 1)

# --- WEBSITE DASHBOARD ---
st.set_page_config(page_title="Financial Planning Engine", layout="wide")
st.title("AI Financial Planning Engine")
st.markdown("---")

st.header("What-If Goal Simulator")
st.write("Adjust the parameters below to dynamically recalculate the required investments for your goals.")

col1, col2, col3, col4 = st.columns(4)
goal_name = col1.text_input("Goal Name", value="Travel Fund")
current_cost = col2.number_input("Current Cost (₹)", value=350000, step=10000)
years = col3.number_input("Years to Goal", value=2.0, step=0.5)

inflation = col1.slider("Expected Inflation (%)", 0.0, 15.0, 6.0) / 100
returns = col2.slider("Expected Portfolio Return (%)", 0.0, 20.0, 8.0) / 100

if st.button("Calculate Plan Requirement"):
    # Run the math
    future_cost = calculate_future_value(current_cost, inflation, years)
    required_sip = calculate_required_sip(future_cost, returns, years)
    
    # Show the results
    st.success(f"### Future Goal Cost: ₹ {future_cost:,.2f}")
    st.info(f"### Required Monthly SIP: ₹ {required_sip:,.2f}")
    
    # Show a simple chart
    months = int(years * 12)
    sip_array = [required_sip * i for i in range(1, months + 1)]
    chart_data = pd.DataFrame({"Cumulative Investment": sip_array})
    st.line_chart(chart_data)
