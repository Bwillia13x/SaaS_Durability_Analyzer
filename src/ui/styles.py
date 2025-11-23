import streamlit as st

def apply_ive_style():
    st.markdown("""
        <style>
        /* Main App Background with subtle gradient */
        .stApp {
            background: linear-gradient(135deg, #F5F5F7 0%, #FAFAFA 100%);
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }
        
        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #FFFFFF 0%, #FAFAFA 100%);
            border-right: 1px solid #E8E8E8;
        }
        
        section[data-testid="stSidebar"] .block-container {
            padding-top: 2.5rem;
            padding-left: 1.5rem;
            padding-right: 1.5rem;
        }
        
        /* Main container padding */
        .main .block-container {
            padding-left: 2rem;
            padding-right: 2rem;
            padding-top: 2rem;
        }
        
        /* Typography */
        h1, h2, h3, h4, h5, h6 {
            font-weight: 600;
            color: #1D1D1F;
            letter-spacing: -0.02em;
            margin-top: 1.5rem;
            margin-bottom: 1rem;
        }
        
        h1 {
            font-size: 2.75rem;
            font-weight: 700;
            color: #1D1D1F;
            margin-bottom: 1rem;
        }
        
        h2 {
            font-size: 1.6rem;
            color: #1D1D1F;
            font-weight: 600;
            margin-top: 1.5rem;
            margin-bottom: 1rem;
        }
        
        h3 {
            font-size: 1.25rem;
            color: #1D1D1F;
            font-weight: 600;
            margin-top: 1.25rem;
            margin-bottom: 0.75rem;
        }
        
        h4 {
            font-size: 1.05rem;
            color: #1D1D1F;
            font-weight: 500;
            margin-top: 1rem;
        }
        
        p, label, .stMarkdown {
            color: #505054;
            font-weight: 400;
            line-height: 1.6;
        }
        
        /* Metrics Cards - Enhanced */
        [data-testid="stMetric"] {
            background: #FFFFFF;
            padding: 24px;
            border-radius: 16px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
            border: 1px solid #EFEFEF;
            transition: all 0.25s ease;
        }
        
        [data-testid="stMetric"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.08);
            border-color: #E5E5E5;
        }
        
        [data-testid="stMetricLabel"] {
            color: #86868B;
            font-size: 13px;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        [data-testid="stMetricValue"] {
            color: #1D1D1F;
            font-size: 32px;
            font-weight: 700;
            margin-top: 0.5rem;
        }
        
        [data-testid="stMetricDelta"] {
            font-weight: 600;
            font-size: 14px;
            margin-top: 0.5rem;
        }
        
        /* Buttons - Enhanced */
        .stButton > button {
            background: linear-gradient(135deg, #007AFF 0%, #0051D5 100%);
            color: white;
            border: none;
            border-radius: 24px;
            padding: 12px 28px;
            font-weight: 600;
            box-shadow: 0 4px 12px rgba(0, 122, 255, 0.25);
            transition: all 0.3s ease;
            font-size: 15px;
        }
        
        .stButton > button:hover {
            background: linear-gradient(135deg, #0066D6 0%, #003D9E 100%);
            box-shadow: 0 8px 20px rgba(0, 122, 255, 0.35);
            transform: translateY(-1px);
        }
        
        /* Sliders */
        .stSlider [data-baseweb="slider"] {
            margin-top: 12px;
            margin-bottom: 8px;
        }
        
        /* Text Input */
        .stTextInput > div > div > input {
            border-radius: 12px;
            border: 1.5px solid #E5E5E5;
            padding: 10px 14px;
            font-size: 15px;
            transition: all 0.2s ease;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #007AFF;
            box-shadow: 0 0 0 3px rgba(0, 122, 255, 0.1);
        }
        
        /* Alerts/Info Boxes */
        .stAlert {
            background-color: #FFFFFF;
            border: none;
            border-left: 4px solid #007AFF;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0, 122, 255, 0.08);
            padding: 16px 20px;
            margin: 16px 0;
        }
        
        .stSuccess {
            border-left-color: #34C759 !important;
            box-shadow: 0 2px 8px rgba(52, 199, 89, 0.12) !important;
        }
        
        .stError {
            border-left-color: #FF3B30 !important;
            box-shadow: 0 2px 8px rgba(255, 59, 48, 0.12) !important;
        }
        
        .stWarning {
            border-left-color: #FF9500 !important;
            box-shadow: 0 2px 8px rgba(255, 149, 0, 0.12) !important;
        }
        
        .stInfo {
            border-left-color: #007AFF !important;
            box-shadow: 0 2px 8px rgba(0, 122, 255, 0.12) !important;
        }
        
        /* Dividers */
        hr {
            border: none;
            border-top: 1px solid #E8E8E8;
            margin: 40px 0;
        }
        
        /* Expander */
        .streamlit-expanderHeader {
            background-color: #F8F8FA;
            border-radius: 12px;
            border: 1px solid #E5E5E5;
            transition: all 0.2s ease;
        }
        
        .streamlit-expanderHeader:hover {
            background-color: #F0F0F2;
            border-color: #D0D0D2;
        }
        
        /* Plotly Chart Container */
        .js-plotly-plot .plotly .main-svg {
            background-color: transparent !important;
        }
        
        /* Custom Classes for Containers */
        .card-container {
            background: linear-gradient(135deg, #FFFFFF 0%, #FAFAFA 100%);
            padding: 28px;
            border-radius: 20px;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.05);
            margin-bottom: 24px;
            border: 1px solid #F0F0F0;
        }
        
        /* Section containers */
        .section-header {
            padding-bottom: 1rem;
            margin-bottom: 1.5rem;
            border-bottom: 2px solid rgba(0, 122, 255, 0.15);
        }
        
        /* Caption styling */
        .stCaption {
            color: #86868B;
            font-size: 13px;
            line-height: 1.5;
            margin-top: 0.5rem;
        }
        
        /* Improved spacing */
        .stColumnContainer > .stColumn {
            gap: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

def card_container(key=None):
    """
    Helper to create a styled container. 
    Streamlit doesn't allow direct HTML wrapping of widgets easily, 
    so we just use this to mark sections if needed or inject CSS classes.
    """
    return st.container()
