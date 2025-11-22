# SaaS EPV Analyzer

A professional-grade project architecture designed to impress a technical investor. It separates Financial Logic (Greenwald), Data Fetching (SEC/APIs), and AI Logic (LLM adjustments) into clean, modular components.

This structure demonstrates scalable, production-ready code.

## Overview

- **src/data**: Data Ingestion Layer (SEC EDGAR, Market Data)
- **src/finance**: The Greenwald Logic Layer (EPV Formula, Adjustments)
- **src/ai**: The Intelligence Layer (OpenAI/Anthropic Wrapper, Prompts, Parsers)

## Usage

1. Install dependencies: `pip install -r requirements.txt`
2. Run the dashboard: `streamlit run main.py`
