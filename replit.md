# SaaS EPV Analyzer

## Overview
This is a professional-grade Streamlit application that performs Earnings Power Value (EPV) analysis for SaaS companies using the Bruce Greenwald framework. The application normalizes income statements to find "steady state" earnings by separating growth investments from maintenance spending.

## Project Structure
```
.
├── main.py                    # Main Streamlit application
├── src/
│   ├── ai/                   # AI/LLM integration layer
│   │   ├── client.py         # OpenAI API wrapper
│   │   ├── parser.py         # Response parsing logic
│   │   └── prompts.py        # Prompt templates
│   ├── data/                 # Data fetching layer
│   │   ├── market_data.py    # Market data via yfinance
│   │   └── sec_fetcher.py    # SEC EDGAR filing retrieval
│   ├── finance/              # Financial analysis layer
│   │   ├── adjustments.py    # Normalization adjustments
│   │   └── epv_model.py      # Greenwald EPV calculations
│   └── ui/
│       └── styles.py         # UI styling
├── notebooks/                # Jupyter notebooks for analysis
└── requirements.txt          # Python dependencies
```

## Key Features
- **Real-time Financial Data**: Fetches live data from SEC EDGAR and Yahoo Finance
- **AI-Powered Analysis**: Uses OpenAI to analyze MD&A sections and estimate maintenance spending
- **Interactive Dashboard**: Streamlit-based UI with real-time parameter adjustments
- **Greenwald EPV Framework**: Implements the full EPV methodology including:
  - Normalized EBIT calculations
  - Reproduction value estimation
  - Franchise value (moat) analysis
  - Rule of 40 scoring

## Environment Setup
This project is configured to run on Replit with:
- **Python 3.11**
- **Streamlit** running on `0.0.0.0:5000`
- CORS and XSRF protection disabled for Replit proxy compatibility
- **PostgreSQL Database**: Development database is provisioned and ready

### Database Configuration
A PostgreSQL database is available for development:
- **Access**: Via `DATABASE_URL` environment variable
- **Environment Variables**: `PGHOST`, `PGPORT`, `PGUSER`, `PGPASSWORD`, `PGDATABASE`
- **Status**: Ready to use for future features that may require data persistence

## Running the Application
The application runs automatically via the configured workflow. To manually start:
```bash
streamlit run main.py
```

## API Keys Configuration
The application is configured to use optional API keys for enhanced features:

### OpenAI (for AI analysis)
- **Status**: ✓ Configured
- **Purpose**: Analyzes SEC filings to estimate maintenance vs growth spending
- **Fallback**: Uses simulated analysis with reasonable defaults
- **Model**: `OPENAI_MODEL` (default: gpt-5.1, fallback: gpt-4o)
- **Reasoning**: `OPENAI_REASONING` (default: high)

### Financial Modeling Prep (for enhanced financial data)
- **Status**: ✓ Configured
- **Purpose**: More reliable financial data than Yahoo Finance
- **Fallback**: Uses Yahoo Finance or mock data when API has issues

## Deployment
Configured for Replit Autoscale deployment:
- **Type**: Autoscale (stateless web application)
- **Port**: 5000
- **Command**: `streamlit run main.py`

## Technologies Used
- **Streamlit**: Web application framework
- **Pandas**: Data manipulation
- **Plotly**: Interactive charts
- **OpenAI**: AI-powered financial analysis
- **yfinance**: Market data
- **SEC EDGAR**: Company filings

## User Preferences
None specified yet.

## Design Philosophy
The interface embodies Jony Ives' principles of extreme simplicity and refinement:
- **Pure white backgrounds** - fundamental material aesthetic
- **Typography as hero** - text drives the design, not decorative elements
- **Generous negative space** - breathing room between elements
- **Minimal color palette** - black, white, subtle grays only
- **Refined details** - subtle shadows, minimal borders, smooth transitions
- **Essential elements only** - every component serves a purpose
- **Premium through restraint** - luxury achieved through simplicity

## Recent Changes
- **2025-11-23**: Complete platform refinement and design transformation
  - Configured Python 3.11 environment with all dependencies
  - Set up Streamlit on port 5000 with Replit proxy compatibility
  - Implemented comprehensive EPV analysis engine
  - Set up PostgreSQL development database
  - Designed professional UI/UX with aesthetic refinements
  - Applied Jony Ives' minimalist design philosophy
  - Removed all emoji and visual clutter
  - Established pure white backgrounds and typography-focused design
  - Configured API integrations (OpenAI + Financial Modeling Prep)
  - Optimized spacing, typography, and visual hierarchy

## Deployment Status
✓ App is fully configured and ready for production deployment
- Development workflow running on port 5000
- All dependencies installed and verified
- Database provisioned and accessible
- Streamlit security settings configured for Replit environment
- API keys configured (OpenAI + Financial Modeling Prep)
- Ready to be published to production

## How to Publish
1. Click the **Publish** button in the top-right of your Replit workspace
2. Choose your deployment options
3. Your app will get a live URL that you can share with anyone
