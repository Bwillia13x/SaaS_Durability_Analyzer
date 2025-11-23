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
            border-right: 1px solid #F0F0F0;
        }
        
        section[data-testid="stSidebar"] .block-container {
            padding-top: 3rem;
            padding-left: 2rem;
            padding-right: 2rem;
            padding-bottom: 2rem;
        }
        
        /* Main container - generous spacing */
        .main .block-container {
            padding-left: 3rem;
            padding-right: 3rem;
            padding-top: 2.5rem;
            padding-bottom: 3rem;
            max-width: 1280px;
        }
        
        /* Typography: Typography is the primary design element */
        h1, h2, h3, h4, h5, h6 {
            font-weight: 600;
            color: #000000;
            letter-spacing: -0.015em;
            line-height: 1.15;
        }
        
        h1 {
            font-size: 2.75rem;
            font-weight: 700;
            margin-bottom: 1rem;
            margin-top: 0;
            color: #000000;
            letter-spacing: -0.02em;
        }
        
        h2 {
            font-size: 1.625rem;
            font-weight: 600;
            margin-top: 2rem;
            margin-bottom: 1.25rem;
            color: #000000;
            letter-spacing: -0.015em;
        }
        
        h3 {
            font-size: 1.125rem;
            font-weight: 600;
            margin-top: 1.5rem;
            margin-bottom: 0.75rem;
            color: #1D1D1F;
            letter-spacing: -0.01em;
        }
        
        h4 {
            font-size: 0.95rem;
            font-weight: 500;
            margin-top: 1rem;
            margin-bottom: 0.625rem;
            color: #1D1D1F;
            letter-spacing: -0.005em;
        }
        
        /* Body text - optimized readability */
        p, label, .stMarkdown, body {
            color: #505054;
            font-weight: 400;
            line-height: 1.6;
            font-size: 15px;
        }
        
        /* Metric Cards - Refined simplicity with enhanced polish */
        [data-testid="stMetric"] {
            background-color: #FFFFFF;
            padding: 24px 22px;
            border-radius: 8px;
            box-shadow: 0 0.5px 2px rgba(0, 0, 0, 0.035);
            border: 1px solid #EEEEEE;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
        }
        
        [data-testid="stMetric"]:hover {
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
            border-color: #E0E0E0;
            transform: translateY(-1px);
        }
        
        /* Metric Label - Subtle, minimal */
        [data-testid="stMetricLabel"] {
            color: #76767A;
            font-size: 11px;
            font-weight: 500;
            text-transform: none;
            letter-spacing: 0.3px;
            margin-bottom: 10px;
            text-transform: uppercase;
            opacity: 0.8;
        }
        
        /* Metric Value - Large, dominant */
        [data-testid="stMetricValue"] {
            color: #000000;
            font-size: 34px;
            font-weight: 700;
            margin-top: 0;
            line-height: 1.1;
            letter-spacing: -0.02em;
        }
        
        /* Metric Delta */
        [data-testid="stMetricDelta"] {
            font-weight: 500;
            font-size: 12px;
            margin-top: 8px;
            color: #76767A;
            letter-spacing: 0.2px;
        }
        
        /* Buttons - Minimal, refined with smooth interactions */
        .stButton > button {
            background-color: #000000;
            color: #FFFFFF;
            border: 1px solid #000000;
            border-radius: 6px;
            padding: 10px 22px;
            font-weight: 500;
            font-size: 13px;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
            letter-spacing: 0.3px;
        }
        
        .stButton > button:hover {
            background-color: #1D1D1F;
            border-color: #1D1D1F;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            transform: translateY(-1px);
        }
        
        .stButton > button:active {
            transform: translateY(0);
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
        }
        
        /* Slider - Refined styling */
        .stSlider [data-baseweb="slider"] {
            margin-top: 14px;
            margin-bottom: 16px;
        }
        
        .stSlider [data-baseweb="slider"] > div {
            opacity: 0.95;
        }
        
        /* Text Input - Minimal borders with refined focus state */
        .stTextInput > div > div > input {
            border-radius: 6px;
            border: 1px solid #D8D8DB;
            padding: 10px 12px;
            font-size: 14px;
            transition: all 0.2s ease;
            background-color: #FFFFFF;
            font-weight: 400;
            letter-spacing: -0.005em;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #000000;
            box-shadow: 0 0 0 3px rgba(0, 0, 0, 0.08);
            outline: none;
        }
        
        .stTextInput > div > div > input::placeholder {
            color: #A0A0A3;
            opacity: 0.7;
        }
        
        /* Alerts - Simplified, minimal color */
        .stAlert {
            background-color: #FFFFFF;
            border: 1px solid #E8E8E8;
            border-left: 3px solid #767680;
            border-radius: 6px;
            padding: 16px 18px;
            margin: 20px 0;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
        }
        
        .stAlert p {
            margin: 0;
            color: #505054;
            font-size: 14px;
            line-height: 1.5;
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
            border-top: 1px solid #F0F0F0;
            margin: 3rem 0;
            opacity: 0.6;
        }
        
        /* Expander - Refined appearance */
        .streamlit-expanderHeader {
            background-color: #FFFFFF;
            border: 1px solid #E8E8E8;
            border-radius: 6px;
            transition: all 0.2s ease;
            padding: 14px 16px;
        }
        
        .streamlit-expanderHeader:hover {
            background-color: #FAFAFA;
            border-color: #D8D8DB;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        }
        
        .streamlit-expander [data-testid="stContentContainer"] {
            padding-top: 12px;
        }
        
        /* Plotly Charts - Minimal, clean */
        .js-plotly-plot .plotly .main-svg {
            background-color: transparent !important;
        }
        
        .plotly .xtick text, .plotly .ytick text {
            font-size: 12px !important;
            font-weight: 400 !important;
            fill: #767680 !important;
            letter-spacing: 0.2px !important;
        }
        
        /* Caption - Refined color and spacing */
        .stCaption {
            color: #76767A;
            font-size: 12px;
            line-height: 1.5;
            font-weight: 400;
            letter-spacing: 0.2px;
            margin-top: 6px;
        }
        
        /* Columns - Better spacing */
        .stColumnContainer > .stColumn {
            gap: 32px;
        }
        
        /* Remove unnecessary borders and decorations */
        [data-testid="stColumn"] {
            padding: 0;
        }
        
        /* Section spacing improvements */
        .stMarkdown {
            margin-top: 0.5rem;
            margin-bottom: 0.5rem;
        }
        </style>
    """, unsafe_allow_html=True)

def card_container(key=None):
    """Minimal container for sections."""
    return st.container()
