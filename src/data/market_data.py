import os
import time
import requests
import yfinance as yf
import pandas as pd

def get_market_snapshot(ticker):
    """
    Fetches current market data for a given ticker using yfinance.
    Falls back to mock data if yfinance fails or ticker is invalid.
    
    Args:
        ticker (str): Stock ticker symbol
        
    Returns:
        dict: Contains 'price', 'market_cap', 'company_name'
    """
    api_key = os.getenv("FMP_API_KEY")
    last_error = None

    # Try FMP first if API key is present
    if api_key:
        try:
            url = f"https://financialmodelingprep.com/api/v3/quote/{ticker}?apikey={api_key}"
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            if data:
                q = data[0]
                price = q.get("price")
                market_cap = q.get("marketCap")
                name = q.get("name") or ticker
                if price is not None and market_cap is not None:
                    return {
                        "price": price,
                        "market_cap": market_cap,
                        "company_name": name,
                        "is_mock": False,
                        "source": "fmp"
                    }
        except Exception as e:
            last_error = e
            # fall through to yfinance

    for attempt in range(3):
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # yfinance info dictionary usually contains these keys
            price = info.get('currentPrice') or info.get('regularMarketPrice')
            market_cap = info.get('marketCap')
            name = info.get('longName') or info.get('shortName') or ticker
            
            if price is None or market_cap is None:
                 raise ValueError("Missing price or market cap data")
             
            return {
                "price": price,
                "market_cap": market_cap,
                "company_name": name,
                "is_mock": False,
                "source": "yfinance"
            }
            
        except Exception as e:
            last_error = e
            if attempt < 2:
                time.sleep(1 * (attempt + 1))
                continue
    
    print(f"⚠️ Market Data Error for {ticker}: {last_error}. Using mock fallback.")
    return {
        "price": 75.50,
        "market_cap": 98_000_000_000, # $98B
        "company_name": f"{ticker} (Mock)",
        "is_mock": True,
        "source": "mock"
    }
