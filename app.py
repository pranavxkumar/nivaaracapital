import streamlit as st

st.set_page_config(page_title="Nivaara Capital", page_icon="🏦", layout="wide")

st.title("🏦 Nivaara Capital")
st.markdown("### Institutional-Grade Financial Planning & Portfolio Analytics")
st.markdown("---")

st.write("""
Welcome to Nivaara Capital. This platform integrates core quantitative analysis with goal-based financial planning.

Use the sidebar to the left to navigate through our core modules:
*   **Financial Planner:** An engine to calculate inflation-adjusted goals, future values, and required capital deployment.
*   **Portfolio Tracker:** A live multi-asset tracking engine pulling real-time market data to monitor asset performance and risk metrics.
""")

st.info("👈 Select a tool from the sidebar to begin.")
