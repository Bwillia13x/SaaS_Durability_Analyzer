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
            "company_name": name
        }
        
    except Exception as e:
        print(f"⚠️ Market Data Error for {ticker}: {e}. Using mock fallback.")
        return {
            "price": 75.50,
            "market_cap": 98_000_000_000, # $98B
            "company_name": f"{ticker} (Mock)"
        }
