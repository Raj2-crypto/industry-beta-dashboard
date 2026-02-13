import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)  # Ensure project root is in sys.path for imports
import pandas as pd
from Utils.fetch_ticker_data import fetch_ticker_data
from Utils.get_exchange_rate import get_exchange_rate
from Utils.to_inr_millions import to_inr_millions
from Utils.calc_cost_of_debt import calc_cost_of_debt
from Utils.calc_effective_tax_rate import calc_effective_tax_rate

def get_financial_data(ticker_symbol):
    info, financials, balance_sheet = fetch_ticker_data(ticker_symbol)

    if info is None:
        return None

    currency_raw = info.get("currency")
    if not currency_raw:
        return None
    currency = currency_raw.upper()
    exchange_rate = get_exchange_rate(currency, "INR")

    market_cap_native = info.get("marketCap") or 0
    total_debt_native = info.get("totalDebt") or 0
    cash_native       = info.get("totalCash") or 0
    revenue_native    = info.get("totalRevenue") or 0
    beta              = info.get("beta", None)

    cost_of_debt      = calc_cost_of_debt(financials, total_debt_native)
    effective_tax_rate = calc_effective_tax_rate(financials)

    fx = lambda v: to_inr_millions(v, exchange_rate)
    market_cap_inr = fx(market_cap_native)
    total_debt_inr = fx(total_debt_native)
    cash_inr       = fx(cash_native)
    revenue_inr    = fx(revenue_native)

    firm_value_inr       = market_cap_inr + total_debt_inr
    enterprise_value_inr = market_cap_inr + total_debt_inr - cash_inr

    cash_fv  = (cash_inr / firm_value_inr)       if firm_value_inr > 0   else 0.0
    gross_de = (total_debt_inr / market_cap_inr)  if market_cap_inr > 0  else 0.0
    ev_sales = (enterprise_value_inr / revenue_inr) if revenue_inr > 0   else 0.0

    return {
        "Company":                ticker_symbol,
        "Currency":               currency,
        "Exchange Rate (to INR)": round(exchange_rate, 4),
        "Levered Beta":           round(beta, 2) if beta is not None else None,
        "Market Cap (M)":        round(market_cap_inr, 2),
        "Total Debt (M)":        round(total_debt_inr, 2),
        "Firm Value (M)":        round(firm_value_inr, 2),
        "Cash (M)":              round(cash_inr, 2),
        "Enterprise Value (M)":  round(enterprise_value_inr, 2),
        "Cash/Firm Value":        f"{cash_fv:.2%}",
        "Pre-Tax Cost of Debt":   f"{cost_of_debt:.2%}",
        "Marginal Tax Rate":      f"{effective_tax_rate:.2%}",
        "Gross D/E Ratio":        round(gross_de, 2),
        "Revenue (M)":           round(revenue_inr, 2),
        "EV/Sales":               round(ev_sales, 2),
    }

