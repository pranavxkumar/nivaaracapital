import streamlit as st
import requests
import yfinance as yf
import pandas as pd
import numpy as np

# Page Configuration
st.set_page_config(page_title="Financial Planning Dashboard", layout="wide")

st.title("AI Financial Planning Engine")
st.markdown("---")

# Goal Simulator Section
st.header("What-If Goal Simulator")
st.write("Adjust the parameters below to dynamically recalculate the required investments for your goals.")

with st.container():
    col1, col2, col3, col4 = st.columns(4)
    
    goal_name = col1.text_input("Goal Name", value="European Travel")
    current_cost = col2.number_input("Current Cost (₹)", value=350000, step=10000)
    years = col3.number_input("Years to Goal", value=2.0, step=0.5)
    
    # Using sliders for return/inflation assumptions
    inflation = col1.slider("Expected Inflation (%)", 0.0, 15.0, 6.0) / 100
    returns = col2.slider("Expected Portfolio Return (%)", 0.0, 20.0, 8.0) / 100

if st.button("Calculate Plan Requirement"):
    payload = {
        "goal_name": goal_name,
        "current_cost": current_cost,
        "inflation_rate": inflation,
        "years": years,
        "expected_return": returns
    }
    
    # Call the FastAPI Backend Calculation Engine
    try:
        response = requests.post("http://127.0.0.1:8000/api/v1/plan/calculate_goal", json=payload)
        
        if response.status_code == 200:
            data = response.json()
            
            st.success(f"### Future Goal Cost: ₹ {data['future_cost']:,.2f}")
            st.info(f"### Required Monthly SIP: ₹ {data['required_monthly_sip']:,.2f}")
            
            # Simple projection chart visualization
            months = int(years * 12)
            sip_array = [data['required_monthly_sip'] * i for i in range(1, months + 1)]
            chart_data = pd.DataFrame({
                "Cumulative Investment": sip_array
            })
            st.line_chart(chart_data)
            
        else:
            st.error(f"Error calculating plan: {response.text}")
    except requests.exceptions.ConnectionError:
        st.error("Could not connect to the backend API. Make sure FastAPI is running on port 8000.")