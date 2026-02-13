import yfinance as yf

# ─────────────────────────────────────────────
# EXCHANGE RATE
# ─────────────────────────────────────────────

def get_exchange_rate(source_currency, target_currency="INR"):
    source_currency = source_currency.upper()
    target_currency = target_currency.upper()

    if source_currency == target_currency:
        return 1.0

    ticker = f"{source_currency}{target_currency}=X"
    print(f"FX ticker: {ticker}")

    try:
        hist = yf.Ticker(ticker).history(period="5d")
        if not hist.empty:
            return float(hist["Close"].iloc[-1])
    except Exception:
        pass

    try:
        ticker_inv = f"{target_currency}{source_currency}=X"
        print(f"FX inverse ticker: {ticker_inv}")
        hist = yf.Ticker(ticker_inv).history(period="5d")
        if not hist.empty:
            rate_inv = float(hist["Close"].iloc[-1])
            if rate_inv != 0:
                return 1.0 / rate_inv
    except Exception:
        pass

    print(f"⚠️ Could not fetch {source_currency} to {target_currency}. Using 1.0")
    return 1.0



# Example usage:
if __name__ == "__main__":
    source = "USD"
    target = "INR"
    rate = get_exchange_rate(source, target)
    print(f"Exchange rate from {source} to {target}: {rate:.4f}")