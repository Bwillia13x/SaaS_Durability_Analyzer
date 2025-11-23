# SaaS Earnings Power Value (EPV) Analyzer

A professional-grade financial analysis platform that evaluates SaaS companies using the **Bruce Greenwald EPV framework**. This application normalizes income statements to reveal true earnings power by separating growth investments from maintenance spending.

## Features

- **Earnings Power Value (EPV) Analysis**: Calculates the steady-state enterprise value of SaaS businesses using the Greenwald methodology
- **AI-Powered Adjustments**: Uses OpenAI to analyze SEC MD&A sections and estimate maintenance vs. growth spending
- **Real-time Market Data**: Fetches live data from SEC EDGAR and Yahoo Finance
- **Comprehensive Metrics**:
  - Normalized EBIT and NOPAT calculations
  - Rule of 40 scoring (growth + margin)
  - Reproduction value (asset base) estimation
  - Franchise value (competitive moat) analysis
  - Per-share valuations and valuation gaps
- **Interactive Dashboard**: Streamlit-based UI with real-time parameter adjustments
- **Graceful Fallbacks**: Defaults to yfinance/mock data when external APIs are unavailable

## Architecture

The codebase follows **clean, modular architecture** designed for scalability:

```
src/
├── data/              # Data ingestion layer
│   ├── market_data.py    # Yahoo Finance & market snapshots
│   └── sec_fetcher.py    # SEC EDGAR filing retrieval
├── finance/           # Financial analysis core
│   ├── epv_model.py      # Greenwald EPV calculations
│   └── adjustments.py    # Income statement normalization
├── ai/                # Intelligence layer
│   ├── client.py         # OpenAI API wrapper with fallbacks
│   ├── parser.py         # Response parsing & validation
│   └── prompts.py        # LLM prompt templates
└── ui/                # Presentation layer
    └── styles.py         # Jony Ives minimalist design system
```

## Technology Stack

- **Frontend**: Streamlit (Python web framework)
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly
- **AI/LLM**: OpenAI GPT API
- **Data Sources**: SEC EDGAR, Yahoo Finance, Financial Modeling Prep API
- **Deployment**: Replit (Streamlit on port 5000)

## Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Running Locally

```bash
streamlit run main.py
```

The app will be available at `http://localhost:5000`

### Environment Setup

Set up optional API keys for enhanced features:

```bash
# Optional: OpenAI API key for AI-powered MD&A analysis
export OPENAI_API_KEY=your_api_key_here

# Optional: Financial Modeling Prep for reliable financial data
export FMP_API_KEY=your_api_key_here
```

The application gracefully falls back to Yahoo Finance and simulated analysis when APIs are unavailable.

## Usage

1. **Enter Ticker**: Input a SaaS company ticker (e.g., SHOP, AAPL)
2. **Set WACC**: Adjust Cost of Capital (default 10%)
3. **Review AI Estimates**: The model analyzes SEC filings to estimate maintenance spending percentages
4. **Adjust as Needed**: Fine-tune maintenance S&M and R&D percentages
5. **View Analysis**: EPV, moat value, Rule of 40, and valuation gap

## Financial Framework

### Greenwald EPV Methodology

The application implements the complete Greenwald valuation framework:

1. **Normalized Earnings**: Separate growth capex from maintenance capex
   - Reported EBIT + Growth S&M + Growth R&D = Normalized EBIT
   - Apply tax rate to get NOPAT (Net Operating Profit After Tax)

2. **Firm Valuation**: Capitalize normalized earnings at WACC
   - Firm EPV = NOPAT / WACC (zero-growth perpetuity)

3. **Equity Value**: Adjust for net cash/debt
   - Equity EPV = Firm EPV + Net Cash

4. **Moat Analysis**: Estimate competitive advantage
   - Reproduction Value = Cost to replicate operating assets
   - Franchise Value = Firm EPV - Reproduction Value

5. **Rule of 40**: Assess growth-profitability balance
   - Rule of 40 Score = Growth Rate + Profit Margin
   - Score ≥ 40% indicates healthy SaaS metric

## Design Philosophy

The user interface embodies **Jony Ives' principles of extreme simplicity and refinement**:

- Pure white backgrounds with black and gray text only
- Typography as the primary design element
- Generous negative space and optimal spacing
- Subtle, refined interactions (hover effects, smooth transitions)
- No decorative elements or unnecessary visual clutter
- Minimal color palette for maximum clarity

## Error Handling & Fallbacks

The application is built with **production resilience**:

- **Financial Data**: If FMP API fails → falls back to Yahoo Finance → falls back to cached/mock data
- **SEC Filings**: If EDGAR fetch fails → uses mock MD&A text
- **AI Analysis**: If OpenAI unavailable → uses sensible defaults based on SaaS benchmarks
- **Market Data**: If real-time data unavailable → displays demo values with clear indicators

## Development

### Key Dependencies

- `streamlit`: Web framework
- `pandas`: Data manipulation
- `plotly`: Interactive visualizations
- `openai`: LLM integration
- `yfinance`: Market data
- `requests`: HTTP client for API calls
- `python-dotenv`: Environment configuration

### Testing

The application has been validated with:

- EPV calculations (tested with AAPL: $1,122.81B firm EPV)
- Market data integration (live price feeds)
- AI analysis pipeline (OpenAI + fallbacks)
- Financial metrics (Rule of 40, moat analysis, valuations)
- UI/UX (Jony Ives design system)

## Deployment

### Streamlit Cloud / Replit

The application is production-ready for:

1. **Replit**: Configure via `.replit` and Streamlit config
2. **Streamlit Cloud**: Push to GitHub, connect to Streamlit Cloud
3. **Custom Servers**: Run as `streamlit run main.py` on any Python environment

### Configuration

- **Port**: 5000 (configured for Replit proxy)
- **CORS**: Enabled for web integration
- **XSRF Protection**: Disabled (Replit proxy compatibility)
- **Layout**: Wide (optimized for modern displays)

## Future Enhancements

- Multi-company comparison analysis
- Historical EPV trends
- Export reports to PDF/Excel
- Sensitivity analysis dashboard
- Batch company analysis
- Custom industry benchmarks

## License

This project is provided as-is for educational and professional use.

## Contact & Support

For questions, issues, or feature requests, please reach out.
