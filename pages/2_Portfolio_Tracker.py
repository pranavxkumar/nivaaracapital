import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Portfolio Tracker | Nivaara Capital", layout="wide")

st.title("Multi-Asset Portfolio Tracker")
st.markdown("Live market data, historical timelines, and risk analytics.")
st.markdown("---")

# User Inputs for Tickers
default_tickers = ["^GSPC", "RELIANCE.NS", "HDFCBANK.NS"]
selected_tickers = st.multiselect("Select Assets (Tickers)", default_tickers + ["AAPL", "MSFT", "GC=F"], default=default_tickers)
timeframe = st.selectbox("Historical Timeline", ["1y", "5y", "10y", "max"], index=1)

if st.button("Fetch Market Data"):
    with st.spinner("Executing data query..."):
        try:
            # Pull historical closing prices
            data = yf.download(selected_tickers, period=timeframe)['Close']
            
            # Clean data for plotting
            if isinstance(data, pd.Series):
                data = data.to_frame(name=selected_tickers[0])
            
            # Normalized Performance Chart (Base 100)
            normalized_data = (data / data.iloc[0]) * 100
            
            st.subheader("Historical Asset Performance (Normalized to 100)")
            fig = px.line(normalized_data, x=normalized_data.index, y=normalized_data.columns, 
                          labels={'value': 'Normalized Value', 'index': 'Date'})
            st.plotly_chart(fig, use_container_width=True)
            
            # Basic Risk Analytics Engine
            st.subheader("Risk Analytics")
            daily_returns = data.pct_change().dropna()
            
            # Annualized Volatility calculation
            volatility = daily_returns.std() * np.sqrt(252)
            cumulative_return = (data.iloc[-1] / data.iloc[0]) - 1
            
            metrics_df = pd.DataFrame({
                "Total Return": cumulative_return.apply(lambda x: f"{x*100:.2f}%"),
                "Annualized Volatility": volatility.apply(lambda x: f"{x*100:.2f}%")
            })
            
            st.dataframe(metrics_df, use_container_width=True)
            
        except Exception as e:
            st.error(f"Error fetching data. Check ticker symbols. Detail: {e}")
