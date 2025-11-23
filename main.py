"""
SaaS Earnings Power Value (EPV) Analyzer

A professional-grade financial analysis platform that evaluates SaaS companies using 
the Bruce Greenwald EPV framework. This application normalizes income statements to 
reveal true earnings power by separating growth investments from maintenance spending.

The application fetches real-time market data, analyzes SEC filings with AI, and 
provides comprehensive valuation metrics including moat analysis and Rule of 40 scoring.

Author: Financial Analysis Team
Framework: Streamlit + Greenwald EPV Methodology
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from src.finance.epv_model import GreenwaldEPV
from src.ai.parser import analyze_growth_spend
from src.data.sec_fetcher import SECFetcher
from src.data.market_data import get_market_snapshot
from src.ui.styles import apply_ive_style

st.set_page_config(page_title="SaaS EPV Analyzer", layout="wide", initial_sidebar_state="expanded")
apply_ive_style()

st.markdown("# SaaS Earnings Power Value Analyzer")
st.markdown("""
This tool normalizes a SaaS company's Income Statement using the Bruce Greenwald EPV framework.
It reveals true earnings power by separating growth investments from maintenance spending.
""")
st.markdown("")

# --- CACHED HELPERS ---
@st.cache_data(show_spinner=False)
def load_financials(ticker: str):
    return SECFetcher().get_financials(ticker)

@st.cache_data(show_spinner=False)
def load_mda_text(ticker: str):
    return SECFetcher().get_mda_text(ticker)

@st.cache_data(show_spinner=False)
def load_market_data(ticker: str):
    return get_market_snapshot(ticker)

@st.cache_data(show_spinner=False)
def get_ai_estimates(mda_text, financials):
    return analyze_growth_spend(mda_text, financials)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("## Analysis Parameters")
    ticker_input = st.text_input("Ticker Symbol", value="SHOP", placeholder="e.g., AAPL, SHOP")
    cost_of_capital = st.slider("Cost of Capital (WACC)", 0.05, 0.15, 0.10, 0.005)
    
    st.markdown("")
    st.markdown("## AI Adjustments")
    st.markdown("")

    # Ticker Validation
    ticker_clean = ticker_input.strip().upper()
    if not ticker_clean or not (1 <= len(ticker_clean) <= 5) or not ticker_clean.isalpha():
        st.error("Invalid Ticker. Please enter 1-5 letters (e.g., AAPL, SHOP).")
        st.stop()
    
    # Fetch Data First to get AI defaults
    with st.spinner("Analyzing financials & SEC filings..."):
        financials = load_financials(ticker_clean)
        mda_result = load_mda_text(ticker_clean)
        market_data = load_market_data(ticker_clean)
        
        # Run AI (or get cached)
        ai_result = get_ai_estimates(mda_result['text'], financials)
    
    # Interactive Sliders initialized with AI values
    # Display current assumption overrides inline if possible
    st.caption(f"AI Estimates: Maint S&M {float(ai_result['maintenance_sga_percent']):.1%} • Maint R&D {float(ai_result['maintenance_rnd_percent']):.1%}")
    st.markdown("")

    maint_sga = st.slider(
        "Maintenance S&M %", 
        0.0, 1.0, 
        float(ai_result['maintenance_sga_percent']),
        help="Portion of S&M used to retain existing customers."
    )

    maint_rnd = st.slider(
        "Maintenance R&D %", 
        0.0, 1.0, 
        float(ai_result['maintenance_rnd_percent']),
        help="Portion of R&D required to maintain the platform."
    )
    

# --- MAIN APP LOGIC ---
if market_data.get('company_name'):
    col_title, col_badge = st.columns([3, 1])
    with col_title:
        st.header(f"{market_data['company_name']}")
        
        # Market Data Freshness
        price_suffix = " (Demo values)" if market_data.get("is_mock") else f" (As of {pd.Timestamp.now().strftime('%H:%M')})"
        st.caption(f"{ticker_clean} • Current Price: ${market_data['price']:.2f}{price_suffix}")
        
    with col_badge:
        # Status Badges
        status_text = "Mock Data" if (market_data.get("is_mock") or financials.get("is_mock")) else "Live Data"
        st.caption(status_text)
        
        if mda_result.get("is_mock"):
            st.caption("Using Mock MD&A (SEC Fetch Failed)")

else:
    st.header(f"Analysis for {ticker_clean}")

# Run Financial Model
model = GreenwaldEPV()
current_adjustments = {
    "maintenance_sga_percent": maint_sga,
    "maintenance_rnd_percent": maint_rnd
}

results = model.calculate_normalized_earnings(financials, current_adjustments)
epv_value = model.get_epv(results['nopat'], cost_of_capital)

# Rule of 40 Calcs
prev_revenue = financials['prev_revenue'] or 1  # guard against divide-by-zero
rev_growth = (financials['revenue'] - prev_revenue) / prev_revenue * 100
gaap_margin = financials['ebit'] / financials['revenue'] * 100
adj_margin = results['nopat'] / financials['revenue'] * 100

rule_40_gaap = model.calculate_rule_of_40(rev_growth, gaap_margin)
rule_40_adj = model.calculate_rule_of_40(rev_growth, adj_margin)

# --- DISPLAY COLUMNS ---
col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.markdown("## GAAP")
    st.metric(label="Reported EBIT", value=f"${financials['ebit']/1e9:.1f}B", delta_color="off")
    st.metric(label="Rule of 40", value=f"{rule_40_gaap:.1f}%")

with col2:
    st.markdown("## Adjusted")
    
    # Metrics Grid
    c1, c2 = st.columns(2)
    c1.metric(label="Normalized EBIT", value=f"${results['normalized_ebit']/1e9:.1f}B", delta=f"+${(results['normalized_ebit'] - financials['ebit'])/1e9:.1f}B")
    c2.metric(label="Adjusted Rule of 40", value=f"{rule_40_adj:.1f}%", delta=f"{rule_40_adj - rule_40_gaap:.1f}% Upgrade")
    
    if rule_40_adj >= 40:
        st.success(f"Rule of 40: {rule_40_adj:.1f}% (Growth {rev_growth:.1f}% + Margin {adj_margin:.1f}%)")
    else:
        st.info(f"Rule of 40: {rule_40_adj:.1f}% (Growth {rev_growth:.1f}% + Margin {adj_margin:.1f}%)")
    
    # EPV vs Market Cap
    mcap_billions = market_data['market_cap'] / 1e9
    
    # Calculate Equity Value (Firm EPV + Cash - Debt)
    firm_epv = epv_value
    cash = financials.get('cash', 0)
    debt = financials.get('debt', 0)
    shares = financials.get('shares_outstanding', 1)
    
    equity_epv = model.calculate_equity_value(firm_epv, cash, debt)
    epv_per_share = equity_epv / shares
    
    # Calculate Reproduction Value (Operating Assets, ex-cash) to avoid cash double-count
    repro_value = model.calculate_reproduction_value(financials)
    franchise_value = firm_epv - repro_value
    
    st.markdown("## Valuation")
    
    # Metrics Row
    m1, m2, m3 = st.columns(3)
    m1.metric(label="Firm EPV", value=f"${firm_epv/1e9:.1f}B", help="Operations Value (Zero Growth)")
    m2.metric(label="Net Cash", value=f"${(cash - debt)/1e9:.1f}B", help="Cash - Debt")
    m3.metric(label="Equity EPV", value=f"${equity_epv/1e9:.1f}B", help="Target Market Cap")
    
    # Footnote for EPV
    st.caption("Note: Firm EPV assumes zero growth. It is the steady-state earnings power capitalized at WACC.")
    
    st.markdown("### Per Share")
    
    # Per Share Metrics
    ps1, ps2, ps3 = st.columns(3)
    ps1.metric(label="Target Price (EPV)", value=f"${epv_per_share:.2f}")
    ps2.metric(label="Current Price", value=f"${market_data['price']:.2f}")
    
    upside = (epv_per_share - market_data['price']) / market_data['price'] * 100
    if upside > 0:
        ps3.metric(label="Upside", value=f"{upside:.1f}%", delta=f"+{upside:.1f}%")
    else:
        ps3.metric(label="Downside", value=f"{upside:.1f}%", delta=f"{upside:.1f}%")
    
    st.markdown("## Moat & Durability")
    
    d1, d2 = st.columns(2)
    d1.metric(label="Reproduction Value (Assets)", value=f"${repro_value/1e9:.1f}B", help="Cost to replicate the platform (Book Equity + R&D Adj)")
    
    moat_delta_color = "normal" if franchise_value > 0 else "inverse"
    d2.metric(
        label="Franchise Value (Moat)", 
        value=f"${franchise_value/1e9:.1f}B", 
        delta=f"${franchise_value/1e9:.1f}B", 
        delta_color=moat_delta_color,
        help="EPV - Reproduction Value"
    )
    
    # Footnote for Moat
    st.caption("Note: Reproduction Value excludes cash to avoid double-counting and capitalizes current R&D over 3 years as a proxy for product/platform replacement.")
    
    if franchise_value > 0:
        st.success(f"**Wide Moat:** The business generates returns significantly above the cost to replicate its assets. (Franchise Value is {franchise_value/firm_epv*100:.0f}% of Firm EPV)")
    else:
        st.error("**No Moat:** The business is destroying value relative to its asset base, or the industry is highly competitive.")

    st.markdown("---")

    if equity_epv > market_data['market_cap']:
        discount = (equity_epv - market_data['market_cap']) / equity_epv * 100
        st.success(f"**Undervalued:** Trading at a **{discount:.1f}% discount** to Equity EPV.")
    else:
        premium = (market_data['market_cap'] - equity_epv) / equity_epv * 100
        st.error(f"**Overvalued:** Trading at a **{premium:.1f}% premium** to Equity EPV.")
    
    st.metric(label="Current Market Cap", value=f"${mcap_billions:.1f}B")

st.markdown("")

# --- CHARTING ---
st.markdown("## Earnings Analysis")

# Create two charts side-by-side
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.caption("Earnings Impact ($B)")
    earnings_df = pd.DataFrame({
        "Metric": ["Reported EBIT", "Normalized EBIT"],
        "Amount ($B)": [financials['ebit'] / 1e9, results['normalized_ebit'] / 1e9]
    })
    fig_earnings = px.bar(
        earnings_df, 
        x="Metric", 
        y="Amount ($B)", 
        color="Metric",
        color_discrete_map={"Reported EBIT": "#FF3B30", "Normalized EBIT": "#007AFF"},
        text_auto='.1f'
    )
    fig_earnings.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_family="-apple-system, BlinkMacSystemFont, sans-serif",
        showlegend=False,
        margin=dict(l=20, r=20, t=30, b=20),
        yaxis=dict(showgrid=True, gridcolor="#E5E5E5"),
        xaxis=dict(showgrid=False)
    )
    st.plotly_chart(fig_earnings, use_container_width=True, width='stretch')

with chart_col2:
    st.caption("Valuation Gap ($B)")
    val_df = pd.DataFrame({
        "Metric": ["Market Cap", "Equity EPV"],
        "Value ($B)": [mcap_billions, equity_epv / 1e9]
    })
    fig_val = px.bar(
        val_df,
        x="Metric",
        y="Value ($B)",
        color="Metric",
        color_discrete_map={"Market Cap": "#8E8E93", "Equity EPV": "#34C759"},
        text_auto='.1f'
    )
    fig_val.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_family="-apple-system, BlinkMacSystemFont, sans-serif",
        showlegend=False,
        margin=dict(l=20, r=20, t=30, b=20),
        yaxis=dict(showgrid=True, gridcolor="#E5E5E5"),
        xaxis=dict(showgrid=False)
    )
    st.plotly_chart(fig_val, use_container_width=True, width='stretch')

st.markdown("")

# AI Reasoning Section
st.markdown("## Analysis Details")
with st.expander("See Detailed Analysis", expanded=False):
    if "⚠️" in ai_result['reasoning']:
        st.warning(ai_result['reasoning'])
    else:
        st.info(ai_result['reasoning'])
    
    st.markdown("### Detailed Adjustments")
    st.json(current_adjustments)

# Summary Chip
summary_text = f"AI Estimate: {ai_result['maintenance_sga_percent']*100:.0f}% Maint S&M, {ai_result['maintenance_rnd_percent']*100:.0f}% Maint R&D"
st.caption(f"Summary: {summary_text}")
