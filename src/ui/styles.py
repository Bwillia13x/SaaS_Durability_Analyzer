import streamlit as st

def apply_ive_style():
    st.markdown("""
        <style>
        /* Jony Ives Design Philosophy: Extreme Simplicity and Refinement */
        
        /* Pure white background - fundamental material */
        .stApp {
            background-color: #FFFFFF;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
        }
        
        /* Sidebar - minimal, clean */
        section[data-testid="stSidebar"] {
            background-color: #FFFFFF;
            border-right: 1px solid #F5F5F5;
        }
        
        section[data-testid="stSidebar"] .block-container {
            padding-top: 3rem;
            padding-left: 2rem;
            padding-right: 2rem;
        }
        
        /* Main container - generous spacing */
        .main .block-container {
            padding-left: 3rem;
            padding-right: 3rem;
            padding-top: 3rem;
            max-width: 1200px;
        }
        
        /* Typography: Typography is the primary design element */
        h1, h2, h3, h4, h5, h6 {
            font-weight: 600;
            color: #000000;
            letter-spacing: -0.01em;
            line-height: 1.2;
        }
        
        h1 {
            font-size: 3rem;
            font-weight: 600;
            margin-bottom: 2rem;
            margin-top: 0;
            color: #000000;
        }
        
        h2 {
            font-size: 1.75rem;
            font-weight: 600;
            margin-top: 2.5rem;
            margin-bottom: 1.5rem;
            color: #000000;
        }
        
        h3 {
            font-size: 1.25rem;
            font-weight: 500;
            margin-top: 1.5rem;
            margin-bottom: 1rem;
            color: #000000;
        }
        
        h4 {
            font-size: 1rem;
            font-weight: 500;
            margin-top: 1rem;
            margin-bottom: 0.75rem;
            color: #1D1D1F;
        }
        
        /* Body text */
        p, label, .stMarkdown, body {
            color: #505054;
            font-weight: 400;
            line-height: 1.7;
            font-size: 16px;
        }
        
        /* Metric Cards - Refined simplicity */
        [data-testid="stMetric"] {
            background-color: #FFFFFF;
            padding: 28px 24px;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
            border: 1px solid #F5F5F5;
            transition: all 0.2s ease;
        }
        
        [data-testid="stMetric"]:hover {
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
            border-color: #E5E5E5;
        }
        
        /* Metric Label - Subtle, minimal */
        [data-testid="stMetricLabel"] {
            color: #767680;
            font-size: 12px;
            font-weight: 400;
            text-transform: none;
            letter-spacing: 0;
            margin-bottom: 8px;
        }
        
        /* Metric Value - Large, dominant */
        [data-testid="stMetricValue"] {
            color: #000000;
            font-size: 36px;
            font-weight: 600;
            margin-top: 0;
            line-height: 1.2;
        }
        
        /* Metric Delta */
        [data-testid="stMetricDelta"] {
            font-weight: 500;
            font-size: 13px;
            margin-top: 6px;
            color: #767680;
        }
        
        /* Buttons - Minimal, refined */
        .stButton > button {
            background-color: #000000;
            color: #FFFFFF;
            border: 1px solid #000000;
            border-radius: 6px;
            padding: 10px 24px;
            font-weight: 500;
            font-size: 14px;
            transition: all 0.2s ease;
            box-shadow: none;
        }
        
        .stButton > button:hover {
            background-color: #1D1D1F;
            border-color: #1D1D1F;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
        }
        
        /* Sliders */
        .stSlider [data-baseweb="slider"] {
            margin-top: 12px;
            margin-bottom: 12px;
        }
        
        /* Text Input - Minimal borders */
        .stTextInput > div > div > input {
            border-radius: 6px;
            border: 1px solid #D5D5D7;
            padding: 10px 12px;
            font-size: 15px;
            transition: all 0.2s ease;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #000000;
            box-shadow: 0 0 0 2px rgba(0, 0, 0, 0.05);
        }
        
        /* Alerts - Simplified, minimal color */
        .stAlert {
            background-color: #FFFFFF;
            border: 1px solid #E5E5E5;
            border-left: 2px solid #767680;
            border-radius: 6px;
            padding: 16px;
            margin: 20px 0;
        }
        
        .stSuccess {
            border-left-color: #34C759 !important;
        }
        
        .stError {
            border-left-color: #FF3B30 !important;
        }
        
        .stWarning {
            border-left-color: #FF9500 !important;
        }
        
        .stInfo {
            border-left-color: #007AFF !important;
        }
        
        /* Dividers - Very subtle */
        hr {
            border: none;
            border-top: 1px solid #F5F5F5;
            margin: 3rem 0;
        }
        
        /* Expander */
        .streamlit-expanderHeader {
            background-color: #FFFFFF;
            border: 1px solid #E5E5E5;
            border-radius: 6px;
            transition: all 0.2s ease;
        }
        
        .streamlit-expanderHeader:hover {
            background-color: #F5F5F5;
            border-color: #D5D5D7;
        }
        
        /* Plotly Charts - Transparent background */
        .js-plotly-plot .plotly .main-svg {
            background-color: transparent !important;
        }
        
        /* Caption - Refined color */
        .stCaption {
            color: #767680;
            font-size: 13px;
            line-height: 1.6;
        }
        
        /* Columns - Better spacing */
        .stColumnContainer > .stColumn {
            gap: 32px;
        }
        
        /* Remove unnecessary borders and decorations */
        [data-testid="stColumn"] {
            padding: 0;
        }
        </style>
    """, unsafe_allow_html=True)

def card_container(key=None):
    """Minimal container for sections."""
    return st.container()
