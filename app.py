import streamlit as st
import yfinance as yf

st.set_page_config(
    page_title="Nivaara Capital",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# DARK THEME CSS
# =========================================================
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0b0e13;
        color: #e6e6e6;
    }
    [data-testid="stSidebar"] {
        background-color: #10141b;
    }
    /* Top nav bar */
    .nv-navbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 14px 28px;
        background-color: #12161f;
        border: 1px solid #1f2530;
        border-radius: 14px;
        margin-bottom: 18px;
    }
    .nv-brand {
        font-size: 1.3rem;
        font-weight: 700;
        color: #f5f5f5;
        letter-spacing: 0.5px;
    }
    .nv-brand span { color: #d4af37; }
    .nv-navlinks {
        display: flex;
        gap: 30px;
        font-size: 0.95rem;
        color: #b8bfc9;
    }
    .nv-navlinks span { opacity: 0.85; }

    /* Ticker strip */
    .nv-ticker-strip {
        background-color: #12161f;
        border: 1px solid #1f2530;
        border-radius: 10px;
        padding: 10px 20px;
        margin-bottom: 20px;
        font-size: 0.9rem;
        color: #b8bfc9;
    }

    /* Hero card */
    .nv-hero {
        background: linear-gradient(135deg, #12161f 0%, #171c26 100%);
        border: 1px solid #1f2530;
        border-radius: 16px;
        padding: 34px 40px;
        margin-bottom: 22px;
    }
    .nv-hero h1 {
        font-size: 2.4rem;
        margin-bottom: 6px;
        color: #f5f5f5;
    }
    .nv-hero p {
        color: #9aa3af;
        font-size: 1.05rem;
        max-width: 680px;
    }
    .nv-pill {
        display: inline-block;
        background-color: rgba(212, 175, 55, 0.12);
        color: #d4af37;
        border: 1px solid rgba(212, 175, 55, 0.35);
        border-radius: 20px;
        padding: 4px 14px;
        font-size: 0.78rem;
        letter-spacing: 0.5px;
        margin-bottom: 14px;
    }

    /* Section card */
    .nv-card {
        background-color: #12161f;
        border: 1px solid #1f2530;
        border-radius: 14px;
        padding: 24px;
        height: 100%;
    }
    .nv-card:hover {
        border-color: #d4af37;
        transition: 0.2s ease-in-out;
    }
    .nv-card h3 {
        color: #f5f5f5;
        margin-bottom: 4px;
    }
    .nv-card p {
        color: #9aa3af;
        font-size: 0.92rem;
    }
    .nv-tag {
        font-size: 0.72rem;
        color: #6f7883;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Section header row */
    .nv-section-header {
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        margin-top: 8px;
        margin-bottom: 4px;
    }
    .nv-section-header h2 {
        color: #f5f5f5;
        font-size: 1.3rem;
    }
    .nv-section-header a {
        color: #6fa8ff;
        font-size: 0.85rem;
        text-decoration: none;
    }

    hr { border-color: #1f2530; }

    [data-testid="stMetricValue"] {
        color: #f5f5f5;
    }
    [data-testid="stMetricLabel"] {
        color: #9aa3af;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# TOP NAV BAR (mirrors Portfolio / Gold / Screener style nav,
# repointed to Nivaara's own modules)
# =========================================================
st.markdown(
    """
    <div class="nv-navbar">
        <div class="nv-brand">🏛️ NIVAARA <span>CAPITAL</span></div>
        <div class="nv-navlinks">
            <span>🎯 Financial Planner</span>
            <span>📊 Portfolio Tracker</span>
            <span>⚙️ More</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================================================
# LIVE INDEX TICKER STRIP (best-effort, non-blocking)
# Purely cosmetic — does not touch planner/tracker logic.
# =========================================================
@st.cache_data(ttl=300)
def get_index_snapshot():
    tickers = {"NIFTY 50": "^NSEI", "SENSEX": "^BSESN", "NIFTY BANK": "^NSEBANK"}
    snapshot = {}
    for label, symbol in tickers.items():
        try:
            hist = yf.Ticker(symbol).history(period="2d")
            if len(hist) >= 2:
                last, prev = hist["Close"].iloc[-1], hist["Close"].iloc[-2]
                change_pct = ((last - prev) / prev) * 100
                snapshot[label] = (last, change_pct)
        except Exception:
            pass
    return snapshot

snapshot = get_index_snapshot()

if snapshot:
    strip_items = []
    for label, (value, change_pct) in snapshot.items():
        color = "#3ddc84" if change_pct >= 0 else "#ff5c5c"
        arrow = "▲" if change_pct >= 0 else "▼"
        strip_items.append(
            f"<b style='color:#e6e6e6'>{label}</b> {value:,.2f} "
            f"<span style='color:{color}'>{arrow} {abs(change_pct):.2f}%</span>"
        )
    st.markdown(
        f"<div class='nv-ticker-strip'>{'&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;'.join(strip_items)}</div>",
        unsafe_allow_html=True
    )
else:
    st.markdown(
        "<div class='nv-ticker-strip'>Live index data unavailable right now — markets snapshot will refresh shortly.</div>",
        unsafe_allow_html=True
    )

# =========================================================
# HERO SECTION
# =========================================================
st.markdown(
    """
    <div class="nv-hero">
        <div class="nv-pill">INSTITUTIONAL-GRADE • GOAL-BASED • DATA-DRIVEN</div>
        <h1>Wealth Intelligence, Engineered.</h1>
        <p>
            Nivaara Capital fuses quantitative market analysis with disciplined
            goal-based financial planning — giving you the same rigor
            institutional desks use, distilled into a clean personal cockpit.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================================================
# MODULE CARDS (Financial Planner / Portfolio Tracker)
# =========================================================
st.markdown(
    """
    <div class="nv-section-header">
        <h2>Your Modules</h2>
    </div>
    """,
    unsafe_allow_html=True
)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown(
        """
        <div class="nv-card">
            <div class="nv-tag">Module 01</div>
            <h3>🎯 Financial Planner</h3>
            <p>
                Convert any life goal into an inflation-adjusted target and a
                precise required monthly SIP — retirement, education, a home,
                or anything in between.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.page_link("pages/1_Financial_Planner.py", label="Open Financial Planner", icon="➡️")

with col2:
    st.markdown(
        """
        <div class="nv-card">
            <div class="nv-tag">Module 02</div>
            <h3>📊 Portfolio Tracker</h3>
            <p>
                Track live performance across your holdings, compare
                normalized returns, and review volatility and cumulative
                return metrics at a glance.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.page_link("pages/2_Portfolio_Tracker.py", label="Open Portfolio Tracker", icon="➡️")

# =========================================================
# MARKET & SECTORS STRIP (Tickertape-style grid, cosmetic)
# =========================================================
st.markdown(
    """
    <div class="nv-section-header" style="margin-top: 28px;">
        <h2>Market Snapshot</h2>
    </div>
    """,
    unsafe_allow_html=True
)

if snapshot:
    m1, m2, m3 = st.columns(3)
    cols = [m1, m2, m3]
    for i, (label, (value, change_pct)) in enumerate(snapshot.items()):
        with cols[i % 3]:
            st.metric(label, f"{value:,.2f}", delta=f"{change_pct:.2f}%")
else:
    st.caption("Live snapshot could not be loaded. Open Portfolio Tracker for full market data.")

st.divider()
st.caption(
    "Nivaara Capital is a personal analytics platform for educational and planning "
    "purposes and does not constitute investment advice."
)
