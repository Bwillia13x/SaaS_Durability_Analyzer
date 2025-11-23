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

## Optional API Keys
The application works with mock data by default but can use real data with these optional API keys:

### OpenAI (for AI analysis)
- **Key**: `OPENAI_API_KEY`
- **Purpose**: Analyzes SEC filings to estimate maintenance vs growth spending
- **Fallback**: Uses simulated analysis with reasonable defaults

### Financial Modeling Prep (for enhanced financial data)
- **Key**: `FMP_API_KEY`
- **Purpose**: More reliable financial data than Yahoo Finance
- **Fallback**: Uses Yahoo Finance or mock data

### OpenAI Model Configuration
- **Model**: `OPENAI_MODEL` (default: gpt-5.1, fallback: gpt-4o)
- **Reasoning**: `OPENAI_REASONING` (default: high)

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

## Recent Changes
- **2025-11-23**: Initial project import and Replit environment setup
  - Configured Python 3.11 environment
  - Installed all dependencies from requirements.txt
  - Set up Streamlit configuration for port 5000 with CORS disabled
  - Configured workflow and deployment settings
  - Created project documentation
  - Set up PostgreSQL development database
