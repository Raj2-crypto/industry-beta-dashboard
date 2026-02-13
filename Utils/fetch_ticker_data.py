import yfinance as yf

def fetch_ticker_data(ticker_symbol):
    try:
        stock = yf.Ticker(ticker_symbol)
        info = stock.info or {}
        financials = stock.financials
        balance_sheet = stock.balance_sheet
        return info, financials, balance_sheet
    except Exception:
        return None, None, None
