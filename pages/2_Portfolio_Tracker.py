import streamlit as st
import pandas as pd
import yfinance as yf
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Portfolio Tracker | Nivaara Capital", page_icon="📊", layout="wide")

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
    [data-testid="stMetricValue"] { color: #f5f5f5; }
    [data-testid="stMetricLabel"] { color: #9aa3af; }
    hr { border-color: #1f2530; }
    .js-plotly-plot { border-radius: 12px; overflow: hidden; }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    "<div class='nv-navbar'><span>🏛️ NIVAARA</span> <span class='gold'>CAPITAL</span></div>",
    unsafe_allow_html=True
)

# ---------- HEADER ----------
st.title("📊 Portfolio Tracker")
st.caption("Live market performance and institutional-style risk analytics.")
st.divider()

# ---------- CONTROLS ----------
with st.container(border=True):
    control_col1, control_col2, control_col3 = st.columns([2, 1, 1])

    with control_col1:
        selected_tickers = st.multiselect(
            "Select Tickers",
            options=["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA", "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS"],
            default=["AAPL", "MSFT"]
        )

    with control_col2:
        timeframe = st.selectbox(
            "Timeframe",
            options=["1mo", "3mo", "6mo", "1y", "2y", "5y"],
            index=3
        )

    with control_col3:
        st.write("")
        st.write("")
        run_analysis = st.button("Refresh Data", type="primary", use_container_width=True)

st.divider()

# ---------- DATA FETCH (UNCHANGED LOGIC) ----------
if not selected_tickers:
    st.info("Select at least one ticker above to begin analysis.")
    st.stop()

with st.spinner("Fetching live market data..."):
    data = yf.download(selected_tickers, period=timeframe)['Close']
    if isinstance(data, pd.Series):
        data = data.to_frame(name=selected_tickers[0])

if data.empty:
    st.error("No data returned for the selected tickers/timeframe. Please adjust your selection.")
    st.stop()

# ---------- CHART LOGIC (UNCHANGED) ----------
normalized_data = (data / data.iloc[0]) * 100
fig = px.line(
    normalized_data,
    x=normalized_data.index,
    y=normalized_data.columns,
    labels={"value": "Normalized Performance (Base = 100)", "index": "Date", "variable": "Ticker"},
    title="Normalized Price Performance"
)
fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#12161f",
    plot_bgcolor="#12161f",
    legend_title_text="Ticker",
    hovermode="x unified",
    margin=dict(l=20, r=20, t=60, b=20),
    height=480,
)
fig.update_traces(line=dict(width=2.2))

st.subheader("Comparative Performance")
st.plotly_chart(fig, use_container_width=True)

st.divider()

# ---------- RISK ANALYTICS LOGIC (UNCHANGED) ----------
daily_returns = data.pct_change().dropna()
volatility = daily_returns.std() * np.sqrt(252)
cumulative_return = (data.iloc[-1] / data.iloc[0]) - 1

st.subheader("Risk & Return Metrics")

risk_df = pd.DataFrame({
    "Cumulative Return": cumulative_return,
    "Annualized Volatility": volatility
})
risk_df.index.name = "Ticker"

# Quick-glance metric cards
metric_cols = st.columns(len(risk_df))
for col, (ticker, row) in zip(metric_cols, risk_df.iterrows()):
    with col:
        with st.container(border=True):
            st.markdown(f"**{ticker}**")
            st.metric("Cumulative Return", f"{row['Cumulative Return'] * 100:.2f}%")
            st.metric("Ann. Volatility", f"{row['Annualized Volatility'] * 100:.2f}%")

# Full polished dataframe (dark-friendly gradient)
with st.expander("📋 View Full Risk Metrics Table", expanded=True):
    styled_df = risk_df.style.format({
        "Cumulative Return": "{:.2%}",
        "Annualized Volatility": "{:.2%}"
    }).background_gradient(subset=["Cumulative Return"], cmap="RdYlGn") \
      .background_gradient(subset=["Annualized Volatility"], cmap="OrRd")

    st.dataframe(styled_df, use_container_width=True)

st.caption("Data sourced live via yFinance. Risk metrics are historical and do not predict future performance.")
