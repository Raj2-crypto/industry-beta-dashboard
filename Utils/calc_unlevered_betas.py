from numpy import median
import pandas as pd

def calc_unlevered_betas(df, marginal_tax_rate=0.25):
    M_L_beta           = df["Levered Beta"].dropna().median()
    M_debt_equity_ratio = df["Gross D/E Ratio"].dropna().median()
    Average_beta         = df["Levered Beta"].dropna().mean()


    cash_series        = pd.to_numeric(
        df["Cash/Firm Value"].str.replace("%", "", regex=False), errors="coerce"
    ) / 100
    M_cash_firm_value  = median(cash_series.dropna())

    debt   = M_debt_equity_ratio / (1 + M_debt_equity_ratio) * 100
    equity = 100 - debt
    cash   = M_cash_firm_value * 100

    unlevered_beta          = M_L_beta / (1 + (1 - marginal_tax_rate) * M_debt_equity_ratio)
    unlevered_beta_business = unlevered_beta / (1 - M_cash_firm_value)

    return {
        "Median Beta":               round(M_L_beta,3),
        "Average Beta":              round(Average_beta,3),
        "Median D/E Ratio":          round(M_debt_equity_ratio,3),
        "Debt % of Firm":            round(debt,3),
        "Equity % of Firm":          round(equity,3),
        "Cash % of Firm":            round(cash,3),
        "Unlevered Beta":            round(unlevered_beta,3),
        "Unlevered Beta (After correction of cash)": round(unlevered_beta_business,3)
    }