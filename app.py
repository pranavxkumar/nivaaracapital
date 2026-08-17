import streamlit as st

st.set_page_config(
    page_title="Nivaara Capital",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- HERO ----------
st.markdown(
    """
    <div style="text-align:center; padding: 2rem 0 1rem 0;">
        <h1 style="font-size: 3rem; margin-bottom: 0;">🏛️ Nivaara Capital</h1>
        <p style="font-size: 1.15rem; color: gray; margin-top: 0.3rem;">
            Institutional-Grade Wealth Intelligence, Built for the Individual Investor
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()

# ---------- PLATFORM DESCRIPTION ----------
col_left, col_right = st.columns([1.3, 1])

with col_left:
    st.subheader("Where Quantitative Rigor Meets Goal-Based Planning")
    st.write(
        """
        Nivaara Capital fuses **institutional-style quantitative analysis** with
        **personal, goal-based financial planning**. Every projection is grounded
        in deterministic financial mathematics, and every market view is powered
        by live data — so you can plan with the same discipline used by
        professional asset managers, without the complexity.

        Whether you're mapping out a child's education fund, a retirement
        corpus, or tracking the real-time risk profile of your equity
        holdings, Nivaara gives you a clean, data-driven cockpit to do it from.
        """
    )

with col_right:
    with st.container(border=True):
        st.markdown("**Platform Snapshot**")
        c1, c2 = st.columns(2)
        c1.metric("Modules", "2")
        c2.metric("Data Source", "Live")
        c1.metric("Methodology", "Deterministic")
        c2.metric("Focus", "Goals + Markets")

st.divider()

# ---------- FEATURE HIGHLIGHTS ----------
st.subheader("Explore the Platform")

feat_col1, feat_col2 = st.columns(2, gap="large")

with feat_col1:
    with st.container(border=True):
        st.markdown("### 🎯 Financial Planner")
        st.write(
            """
            Translate any financial goal — a home, a wedding, retirement —
            into an actionable, inflation-adjusted number and a precise
            monthly investment target.
            """
        )
        st.markdown(
            """
            - Inflation-adjusted future value modeling
            - Required monthly SIP calculation
            - Clean, expander-based input workflow
            """
        )
        st.page_link("pages/1_Financial_Planner.py", label="Open Financial Planner", icon="➡️")

with feat_col2:
    with st.container(border=True):
        st.markdown("### 📊 Portfolio Tracker")
        st.write(
            """
            Monitor live market performance across your chosen tickers with
            normalized comparison charts and institutional-style risk
            analytics.
            """
        )
        st.markdown(
            """
            - Live price data via yFinance
            - Normalized multi-asset performance chart
            - Volatility & cumulative return metrics
            """
        )
        st.page_link("pages/2_Portfolio_Tracker.py", label="Open Portfolio Tracker", icon="➡️")

st.divider()

st.caption(
    "Nivaara Capital is a personal analytics platform for educational and planning "
    "purposes and does not constitute investment advice."
)
