import streamlit as st
import pandas as pd
import plotly.express as px
from src.finance.epv_model import GreenwaldEPV
from src.ai.parser import analyze_growth_spend
from src.data.sec_fetcher import SECFetcher
from src.data.market_data import get_market_snapshot
from src.ui.styles import apply_ive_style

st.set_page_config(page_title="SaaS EPV Analyzer", layout="wide")
apply_ive_style()

st.title("SaaS Earnings Power Value (EPV) Analyzer")
st.markdown("""
This tool normalizes a SaaS company's Income Statement to find its "Steady State" earnings using the Bruce Greenwald EPV framework.
It separates "Growth Investment" from "Maintenance" spend to reveal the true earnings power.
""")

# --- DATA LAYER ---
fetcher = SECFetcher()

# --- AI ANALYZER ---
@st.cache_data
def get_ai_estimates(mda_text, financials):
    return analyze_growth_spend(mda_text, financials)

# --- SIDEBAR ---
with st.sidebar:
    st.header("Analysis Parameters")
    ticker_input = st.text_input("Ticker Symbol", value="SHOP")
    cost_of_capital = st.slider("Cost of Capital (WACC)", 0.05, 0.15, 0.10, 0.005)
    
    st.divider()
    st.markdown("### 🤖 AI Sensitivity Overrides")
    st.caption("Adjust the AI's estimated maintenance split.")

    # Fetch Data First to get AI defaults
    financials = fetcher.get_financials(ticker_input)
    mda_text = fetcher.get_mda_text(ticker_input)
    market_data = get_market_snapshot(ticker_input)
    
    # Run AI (or get cached)
    ai_result = get_ai_estimates(mda_text, financials)
    
    # Interactive Sliders initialized with AI values
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
    
    st.divider()
    st.caption("Note: Dragging sliders updates metrics in real-time.")

# --- MAIN APP LOGIC ---
if market_data.get('company_name'):
    st.header(f"{market_data['company_name']}")
    st.caption(f"{ticker_input} • Current Price: ${market_data['price']:.2f}")
else:
    st.header(f"Analysis for {ticker_input}")

# Run Financial Model
model = GreenwaldEPV()
current_adjustments = {
    "maintenance_sga_percent": maint_sga,
    "maintenance_rnd_percent": maint_rnd
}

results = model.calculate_normalized_earnings(financials, current_adjustments)
epv_value = model.get_epv(results['nopat'], cost_of_capital)

# Rule of 40 Calcs
rev_growth = (financials['revenue'] - financials['prev_revenue']) / financials['prev_revenue'] * 100
gaap_margin = financials['ebit'] / financials['revenue'] * 100
adj_margin = results['nopat'] / financials['revenue'] * 100

rule_40_gaap = model.calculate_rule_of_40(rev_growth, gaap_margin)
rule_40_adj = model.calculate_rule_of_40(rev_growth, adj_margin)

# --- DISPLAY COLUMNS ---
col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.subheader("GAAP (Reported)")
    st.metric(label="Reported EBIT", value=f"${financials['ebit']/1e9:.1f}B", delta_color="off")
    st.metric(label="Rule of 40", value=f"{rule_40_gaap:.1f}%")
    
    with st.container():
        st.caption(f"GAAP Rule of 40: {rule_40_gaap:.1f}% (Growth {rev_growth:.1f}% + Margin {gaap_margin:.1f}%)")
        st.caption("Reported earnings heavily penalized by Growth Capex.")

with col2:
    st.subheader("AI-Adjusted EPV")
    
    # Metrics Grid
    c1, c2 = st.columns(2)
    c1.metric(label="Normalized EBIT", value=f"${results['normalized_ebit']/1e9:.1f}B", delta=f"+${(results['normalized_ebit'] - financials['ebit'])/1e9:.1f}B")
    c2.metric(label="Adjusted Rule of 40", value=f"{rule_40_adj:.1f}%", delta=f"{rule_40_adj - rule_40_gaap:.1f}% Upgrade")
    
    st.success(f"Adjusted Rule of 40: {rule_40_adj:.1f}% (Growth {rev_growth:.1f}% + Adj Margin {adj_margin:.1f}%)")
    
    st.markdown("---")
    
    # EPV vs Market Cap
    mcap_billions = market_data['market_cap'] / 1e9
    
    # Calculate Equity Value (Firm EPV + Cash - Debt)
    firm_epv = epv_value
    cash = financials.get('cash', 0)
    debt = financials.get('debt', 0)
    shares = financials.get('shares_outstanding', 1)
    
    equity_epv = model.calculate_equity_value(firm_epv, cash, debt)
    epv_per_share = equity_epv / shares
    
    # Calculate Reproduction Value (Assets)
    repro_value = model.calculate_reproduction_value(financials)
    franchise_value = firm_epv - repro_value
    
    st.subheader("Valuation Conclusion")
    
    # Metrics Row
    m1, m2, m3 = st.columns(3)
    m1.metric(label="Firm EPV", value=f"${firm_epv/1e9:.1f}B", help="Operations Value")
    m2.metric(label="Net Cash", value=f"${(cash - debt)/1e9:.1f}B", help="Cash - Debt")
    m3.metric(label="Equity EPV", value=f"${equity_epv/1e9:.1f}B", help="Target Market Cap")
    
    st.markdown("#### Per Share Analysis")
    
    # Per Share Metrics
    ps1, ps2, ps3 = st.columns(3)
    ps1.metric(label="Target Price (EPV)", value=f"${epv_per_share:.2f}")
    ps2.metric(label="Current Price", value=f"${market_data['price']:.2f}")
    
    upside = (epv_per_share - market_data['price']) / market_data['price'] * 100
    if upside > 0:
        ps3.metric(label="Upside", value=f"{upside:.1f}%", delta=f"+{upside:.1f}%")
    else:
        ps3.metric(label="Downside", value=f"{upside:.1f}%", delta=f"{upside:.1f}%")
    
    st.markdown("---")
    st.subheader("🏰 Durability & Moat Analysis")
    st.caption("Comparison of Earnings Power (EPV) vs. Cost to Replicate (Reproduction Value). Positive Franchise Value indicates a Moat.")
    
    d1, d2 = st.columns(2)
    d1.metric(label="Reproduction Value (Assets)", value=f"${repro_value/1e9:.1f}B", help="Cost to replicate the platform (Book Equity + R&D Adj)")
    d2.metric(label="Franchise Value (Moat)", value=f"${franchise_value/1e9:.1f}B", delta=f"${franchise_value/1e9:.1f}B", help="EPV - Reproduction Value")
    
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

st.markdown("---")

# --- CHARTING ---
st.subheader("GAAP vs True Earnings Power")
chart_df = pd.DataFrame({
    "Metric": ["Reported EBIT", "Normalized EBIT"],
    "Amount ($B)": [financials['ebit'] / 1e9, results['normalized_ebit'] / 1e9]
})

fig = px.bar(
    chart_df, 
    x="Metric", 
    y="Amount ($B)", 
    color="Metric",
    color_discrete_map={"Reported EBIT": "#FF3B30", "Normalized EBIT": "#007AFF"},
    text_auto='.1f'
)
fig.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font_family="-apple-system, BlinkMacSystemFont, sans-serif",
    showlegend=False,
    margin=dict(l=20, r=20, t=30, b=20),
    yaxis=dict(showgrid=True, gridcolor="#E5E5E5"),
    xaxis=dict(showgrid=False)
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# AI Reasoning Section
st.subheader("🧐 AI Analyst Reasoning")
if "⚠️" in ai_result['reasoning']:
    st.warning(ai_result['reasoning'])
else:
    st.info(ai_result['reasoning'])

st.markdown("### Detailed Adjustments")
st.json(current_adjustments)
