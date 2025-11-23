"""
SEC EDGAR Financial Data Fetcher

Retrieves real-time financial data and MD&A (Management Discussion & Analysis) 
sections from SEC EDGAR filings. This module handles:

- Fetching the latest 10-K forms for companies
- Extracting balance sheet and income statement data
- Parsing MD&A sections for qualitative analysis
- Error handling and fallback to mock data

The fetcher gracefully handles API failures and provides mock data when live 
data is unavailable, ensuring the application always has data to analyze.
"""

import os
import re
import time
import requests
import pandas as pd
import yfinance as yf
from html import unescape

class SECFetcher:
    def __init__(self):
        self._ticker_map_cache = None
        self._session = requests.Session()
        self._session.headers.update({
            "User-Agent": "SaaS EPV Analyzer (research contact: engineering@example.com)"
        })
        
    def get_financials(self, ticker):
        """
        Fetches financial data for the given ticker.
        """
        fallback = {
            "ticker": ticker,
            "revenue": 7_000_000_000,
            "cogs": 2_000_000_000,
            "prev_revenue": 5_600_000_000, # 25% Growth
            "ebit": -1_200_000_000,
            "sga": 2_500_000_000,
            "rnd": 1_800_000_000,
            "tax_rate": 0.21,
            "shares_outstanding": 1_300_000_000,
            "cash": 5_000_000_000,
            "debt": 2_000_000_000,
            "accounts_receivable": 600_000_000,
            "pp_and_e": 300_000_000,
            "other_assets": 200_000_000,
            "total_current_liabilities": 1_500_000_000,
            "book_value_equity": 6_000_000_000,
            "is_mock": True,
            "source": "mock"
        }

        def _safe_get(series, key):
            if series is None:
                return None
            val = series.get(key)
            if val is None or (isinstance(val, float) and pd.isna(val)):
                return None
            try:
                return float(val)
            except Exception:
                return None

        # Try FMP first if API key is available
        fmp_key = os.getenv("FMP_API_KEY")
        if fmp_key:
            try:
                fmp_data = self._fetch_fmp_financials(ticker, fmp_key)
                if fmp_data:
                    return fmp_data
            except Exception as e:
                last_error = e
                print(f"⚠️ FMP financials failed for {ticker}: {e}. Falling back to yfinance/mock.")
        else:
            last_error = None

        # Fallback to yfinance
        for attempt in range(3):
            try:
                stock = yf.Ticker(ticker)
                income_stmt = getattr(stock, "income_stmt", None)
                if income_stmt is None or income_stmt.empty:
                    income_stmt = getattr(stock, "financials", None)
                balance_sheet = getattr(stock, "balance_sheet", None)

                latest_income = income_stmt.iloc[:, 0] if income_stmt is not None and not income_stmt.empty else None
                prev_income = income_stmt.iloc[:, 1] if income_stmt is not None and income_stmt.shape[1] > 1 else None
                latest_balance = balance_sheet.iloc[:, 0] if balance_sheet is not None and not balance_sheet.empty else None

                revenue = _safe_get(latest_income, "Total Revenue") or _safe_get(latest_income, "Operating Revenue")
                cogs = _safe_get(latest_income, "Cost Of Revenue") or 0
                sga = _safe_get(latest_income, "Selling General Administrative") or 0
                rnd = _safe_get(latest_income, "Research Development") or 0
                ebit = _safe_get(latest_income, "Operating Income") or _safe_get(latest_income, "EBIT")

                prev_revenue = _safe_get(prev_income, "Total Revenue") or _safe_get(prev_income, "Operating Revenue")
                if prev_revenue is None and revenue:
                    prev_revenue = revenue * 0.8  # assume 20% y/y growth when prior period is missing

                tax_provision = _safe_get(latest_income, "Tax Provision")
                pretax_income = _safe_get(latest_income, "Pretax Income") or _safe_get(latest_income, "Income Before Tax")
                if pretax_income not in (None, 0) and tax_provision is not None:
                    tax_rate = max(min(tax_provision / pretax_income, 0.35), 0)
                else:
                    tax_rate = 0.21

                info = stock.info if hasattr(stock, "info") else {}
                shares_outstanding = info.get("sharesOutstanding") or fallback["shares_outstanding"]

                cash = _safe_get(latest_balance, "Cash And Cash Equivalents") or _safe_get(latest_balance, "Cash") or fallback["cash"]
                accounts_receivable = _safe_get(latest_balance, "Accounts Receivable") or fallback["accounts_receivable"]
                pp_and_e = _safe_get(latest_balance, "Property Plant Equipment") or fallback["pp_and_e"]
                other_assets = _safe_get(latest_balance, "Other Current Assets") or _safe_get(latest_balance, "Other Assets") or fallback["other_assets"]
                total_current_liabilities = _safe_get(latest_balance, "Total Current Liabilities") or fallback["total_current_liabilities"]
                book_value_equity = _safe_get(latest_balance, "Total Stockholder Equity") or fallback["book_value_equity"]

                total_debt = _safe_get(latest_balance, "Total Debt")
                if total_debt is None:
                    short_debt = _safe_get(latest_balance, "Short Long Term Debt") or 0
                    long_debt = _safe_get(latest_balance, "Long Term Debt") or 0
                    total_debt = short_debt + long_debt
                debt = total_debt if total_debt is not None else fallback["debt"]

                core_fields = [revenue, sga, rnd, ebit]
                if any(val is None for val in core_fields):
                    raise ValueError("Missing core income statement fields")

                return {
                    "ticker": ticker,
                    "revenue": revenue,
                    "cogs": cogs,
                    "prev_revenue": prev_revenue,
                    "ebit": ebit,
                    "sga": sga,
                    "rnd": rnd,
                    "tax_rate": tax_rate,
                    "shares_outstanding": shares_outstanding,
                    "cash": cash,
                    "debt": debt,
                    "accounts_receivable": accounts_receivable,
                    "pp_and_e": pp_and_e,
                    "other_assets": other_assets,
                    "total_current_liabilities": total_current_liabilities,
                    "book_value_equity": book_value_equity,
                    "is_mock": False,
                    "source": "yfinance"
                }

            except Exception as e:
                last_error = e
                if attempt < 2:
                    time.sleep(1 * (attempt + 1))
                    continue

        print(f"⚠️ SEC/YFinance fetch failed for {ticker}: {last_error}. Using mock fallback.")
        return fallback
        
    def get_mda_text(self, ticker):
        """
        Fetches MD&A text from the latest 10-K.
        """
        try:
            doc_html = self._fetch_latest_10k_html(ticker)
            if doc_html:
                extracted = self._extract_mda_section(doc_html)
                if extracted:
                    return {"text": extracted, "is_mock": False}
        except Exception as e:
            print(f"⚠️ MD&A fetch failed for {ticker}: {e}. Using mock text.")

        # Fallback narrative keeps AI working if SEC fetch fails
        return {
            "text": (
                f"Management Discussion & Analysis for {ticker}: "
                "Our Net Revenue Retention rate remained strong at 123%, driven by upsells to existing enterprise customers. "
                "We continue to invest aggressively in Sales & Marketing to capture market share in new geographies. "
                "Research & Development expenses increased as we launched our new 'Enterprise Grid' platform features."
            ),
            "is_mock": True
        }

    # --- Internal helpers ---
    def _fetch_latest_10k_html(self, ticker):
        """
        Best-effort fetch of the latest 10-K primary document HTML using SEC's public data endpoints.
        """
        cik = self._lookup_cik(ticker)
        if not cik:
            raise ValueError("CIK lookup failed")

        cik_padded = str(cik).zfill(10)
        submissions_url = f"https://data.sec.gov/submissions/CIK{cik_padded}.json"
        resp = self._session.get(submissions_url, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        recent = data.get("filings", {}).get("recent", {})
        forms = recent.get("form", [])
        accession_numbers = recent.get("accessionNumber", [])
        primary_docs = recent.get("primaryDocument", [])

        # Find latest 10-K
        target_idx = next((i for i, f in enumerate(forms) if f and f.lower() == "10-k"), None)
        if target_idx is None:
            raise ValueError("No 10-K filing found")

        accession = accession_numbers[target_idx].replace("-", "")
        primary_doc = primary_docs[target_idx]
        cik_no_prefix = str(int(cik))  # strip leading zeros

        filing_url = f"https://www.sec.gov/Archives/edgar/data/{cik_no_prefix}/{accession}/{primary_doc}"
        filing_resp = self._session.get(filing_url, timeout=10)
        filing_resp.raise_for_status()
        return filing_resp.text

    def _extract_mda_section(self, html_text):
        """
        Extracts the MD&A (Item 7) section from the filing HTML by locating Item 7 and ending at Item 7A or 8.
        """
        lower = html_text.lower()
        start_regex = re.compile(r'item\s+7\.?\s*(management|[^<]{0,80}discussion)')
        matches = list(start_regex.finditer(lower))
        if not matches:
            return None

        best_snippet = ""
        for match in matches:
            start_idx = match.start()
            tail = lower[start_idx:]
            end_match = re.search(r'item\s+7a\.?|item\s+8\.?', tail)

            # If the first Item 7A/8 is too close (e.g., table of contents), fall back to a fixed window.
            if end_match and end_match.start() > 2000:
                end_idx = start_idx + end_match.start()
            else:
                end_idx = start_idx + 8000

            raw = html_text[start_idx:end_idx]
            cleaned = re.sub(r'<[^>]+>', ' ', raw)  # strip tags
            cleaned = re.sub(r'\s+', ' ', cleaned).strip()
            cleaned = unescape(cleaned)

            if len(cleaned) > len(best_snippet):
                best_snippet = cleaned

        return best_snippet or None

    def _lookup_cik(self, ticker):
        """
        Resolves ticker to CIK using SEC's published ticker map.
        """
        if not self._ticker_map_cache:
            url = "https://www.sec.gov/files/company_tickers.json"
            resp = self._session.get(url, timeout=10)
            resp.raise_for_status()
            self._ticker_map_cache = resp.json()

        ticker_upper = ticker.upper()
        for entry in self._ticker_map_cache.values():
            if entry.get("ticker", "").upper() == ticker_upper:
                return entry.get("cik_str")
        return None

    # --- FMP Helpers ---
    def _fetch_fmp_financials(self, ticker, api_key):
        """
        Fetch financials using Financial Modeling Prep if an API key is present.
        """
        income_url = f"https://financialmodelingprep.com/api/v3/income-statement/{ticker}?limit=2&apikey={api_key}"
        balance_url = f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{ticker}?limit=1&apikey={api_key}"

        income_resp = self._session.get(income_url, timeout=10)
        income_resp.raise_for_status()
        income_data = income_resp.json()
        if not income_data:
            raise ValueError("Empty income statement from FMP")

        latest_income = income_data[0]
        prev_income = income_data[1] if len(income_data) > 1 else None

        bal_resp = self._session.get(balance_url, timeout=10)
        bal_resp.raise_for_status()
        bal_data = bal_resp.json()
        latest_balance = bal_data[0] if bal_data else None
        if latest_balance is None:
            raise ValueError("Empty balance sheet from FMP")

        def g(data, key, default=None):
            val = data.get(key) if data else None
            return val if val is not None else default

        revenue = g(latest_income, "revenue")
        cogs = g(latest_income, "costOfRevenue", 0)
        sga = g(latest_income, "sellingGeneralAndAdministrativeExpenses") or g(latest_income, "sellingAndMarketingExpenses") or 0
        rnd = g(latest_income, "researchAndDevelopmentExpenses", 0)
        ebit = g(latest_income, "operatingIncome") or g(latest_income, "ebit")

        prev_revenue = g(prev_income, "revenue")
        if prev_revenue is None and revenue:
            prev_revenue = revenue * 0.8

        income_tax = g(latest_income, "incomeTaxExpense")
        income_before_tax = g(latest_income, "incomeBeforeTax") or g(latest_income, "incomeBeforeTaxUSD")
        if income_before_tax not in (None, 0) and income_tax is not None:
            tax_rate = max(min(income_tax / income_before_tax, 0.35), 0)
        else:
            tax_rate = 0.21

        shares_outstanding = g(latest_income, "weightedAverageShsOutDil") or g(latest_income, "weightedAverageShsOut") or 1_300_000_000

        cash = g(latest_balance, "cashAndCashEquivalents") or g(latest_balance, "cashAndShortTermInvestments") or 0
        accounts_receivable = g(latest_balance, "netReceivables") or g(latest_balance, "accountsReceivables") or 0
        pp_and_e = g(latest_balance, "propertyPlantEquipmentNet") or 0
        other_assets = g(latest_balance, "otherCurrentAssets") or g(latest_balance, "otherAssets") or 0
        total_current_liabilities = g(latest_balance, "totalCurrentLiabilities") or 0
        book_value_equity = g(latest_balance, "totalStockholdersEquity") or 0

        total_debt = g(latest_balance, "totalDebt")
        if total_debt is None:
            short_debt = g(latest_balance, "shortTermDebt", 0)
            long_debt = g(latest_balance, "longTermDebt", 0)
            total_debt = short_debt + long_debt

        core_fields = [revenue, sga, rnd, ebit]
        if any(val is None for val in core_fields):
            raise ValueError("Missing core income statement fields from FMP")

        return {
            "ticker": ticker,
            "revenue": revenue,
            "cogs": cogs,
            "prev_revenue": prev_revenue,
            "ebit": ebit,
            "sga": sga,
            "rnd": rnd,
            "tax_rate": tax_rate,
            "shares_outstanding": shares_outstanding,
            "cash": cash,
            "debt": total_debt if total_debt is not None else 0,
            "accounts_receivable": accounts_receivable,
            "pp_and_e": pp_and_e,
            "other_assets": other_assets,
            "total_current_liabilities": total_current_liabilities,
            "book_value_equity": book_value_equity,
            "is_mock": False,
            "source": "fmp"
        }
