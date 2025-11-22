import streamlit as st

def apply_ive_style():
    st.markdown("""
        <style>
        /* Main App Background */
        .stApp {
            background-color: #F5F5F7;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }
        
        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #FFFFFF;
            border-right: 1px solid #E5E5E5;
        }
        
        section[data-testid="stSidebar"] .block-container {
            padding-top: 3rem;
        }
        
        /* Typography */
        h1, h2, h3, h4, h5, h6 {
            font-weight: 600;
            color: #1D1D1F;
            letter-spacing: -0.02em;
        }
        
        h1 {
            font-size: 2.5rem;
            font-weight: 700;
        }
        
        p, label, .stMarkdown {
            color: #424245;
            font-weight: 400;
        }
        
        /* Metrics Cards - targeting the container of metrics if possible, or individual metrics */
        [data-testid="stMetric"] {
            background-color: #FFFFFF;
            padding: 20px;
            border-radius: 16px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            border: 1px solid #F0F0F0;
            transition: transform 0.2s ease;
        }
        
        [data-testid="stMetric"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 16px rgba(0,0,0,0.08);
        }
        
        [data-testid="stMetricLabel"] {
            color: #86868B;
            font-size: 14px;
            font-weight: 500;
        }
        
        [data-testid="stMetricValue"] {
            color: #1D1D1F;
            font-size: 28px;
            font-weight: 600;
        }
        
        [data-testid="stMetricDelta"] {
            font-weight: 500;
            font-size: 13px;
        }
        
        /* Buttons */
        .stButton > button {
            background-color: #007AFF;
            color: white;
            border: none;
            border-radius: 20px;
            padding: 10px 24px;
            font-weight: 500;
            box-shadow: 0 2px 4px rgba(0,122,255,0.2);
            transition: all 0.2s ease;
        }
        
        .stButton > button:hover {
            background-color: #0066D6;
            box-shadow: 0 4px 8px rgba(0,122,255,0.3);
        }
        
        /* Sliders */
        .stSlider [data-baseweb="slider"] {
            margin-top: 10px;
        }
        
        /* Alerts/Info Boxes */
        .stAlert {
            background-color: #FFFFFF;
            border: none;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }
        
        /* Dividers */
        hr {
            border-color: #E5E5E5;
            margin: 30px 0;
        }
        
        /* Plotly Chart Container */
        .js-plotly-plot .plotly .main-svg {
            background-color: transparent !important;
        }
        
        /* Custom Classes for Containers */
        .card-container {
            background-color: #FFFFFF;
            padding: 24px;
            border-radius: 18px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.04);
            margin-bottom: 20px;
            border: 1px solid rgba(0,0,0,0.02);
        }
        
        /* Header tweaks */
        .main-header {
            padding-bottom: 2rem;
            border-bottom: 1px solid #E5E5E5;
            margin-bottom: 2rem;
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
