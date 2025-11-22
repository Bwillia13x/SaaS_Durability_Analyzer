# Agents Guide

This repository is intended to be used together with advanced coding agents (e.g., Cursor, Windsurf, codexcli, GitHub Copilot Workspace).

The goal is to reliably build and extend the **SaaS Durability Analyzer** using Bruce Greenwalds EPV framework, with clean separation between:

- `src/data`   Data ingestion (SEC/FMP/yfinance, MD&A text, market data)
- `src/finance`   EPV math and financial logic
- `src/ai`   LLM prompts, parsing, and robustness
- `main.py`   Streamlit UI and investor-facing presentation

---

## Primary Instructions for Agents

The **canonical build instructions** for this project live in:

- `instructions overview.md`

Any coding agent you spin up should:

1. Open and read `instructions overview.md` in full.  
2. Follow the phases described there:
   - Phase 1: Project scaffold & setup
   - Phase 2: Data ingestion (`src/data/sec_fetcher.py`)
   - Phase 3: AI normalization logic (`src/ai/parser.py`)
   - Phase 4: Financial modeling (`src/finance/epv_model.py`)
   - Phase 5: Streamlit dashboard (`main.py`)
   - Phase 6: "Institutional Polish" (sliders, Rule of 40, robustness)
3. Treat the existing code as the current baseline, extending it rather than rewriting from scratch.

---

## Recommended Startup Prompt (for any agent)

When you start a new coding agent in this repo, give it instructions along these lines (paraphrased):

> You are a senior Python engineer and financial modeler.
> You are working in a project that implements a SaaS Earnings Power Value (EPV) analyzer using Streamlit.
> First, open and read the file `instructions overview.md` and follow the Phases 18 described there.
> Then inspect `main.py`, `src/data`, `src/finance`, and `src/ai` to understand the current implementation.
> Your job is to extend and refine the existing code without breaking working behavior, focusing on:
>   clean separation of data, finance, and AI layers
>   robust AI parsing with retries and fallbacks
>   institutional-grade UI/metrics (Rule of 40, EPV vs market cap, sensitivity sliders).

You can adapt that prompt for:

- **codexcli** (terminal-based agent)
- **Cursor / Windsurf** (IDE-integrated agents)
- **Copilot Workspace** or similar tools

---

## Conventions for Agents

- **Do not commit secrets.** API keys must live only in `.env` or external secret stores.
- Prefer **small, focused changes** over large rewrites.
- Keep the architecture boundaries:
  - `data`  external world (APIs, files, MD&A text)
  - `finance`  pure math and valuation
  - `ai`  prompts and JSON parsing / robustness
  - `main.py`  UX and investor storytelling.
- When in doubt, align behavior with what is written in `instructions overview.md`.
