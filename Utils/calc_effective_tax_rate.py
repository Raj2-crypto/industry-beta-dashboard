
def calc_effective_tax_rate(financials, default=0.25):
    try:
        if financials is not None and not financials.empty:
            if "Tax Provision" in financials.index and "Pretax Income" in financials.index:
                tax_provision = financials.loc["Tax Provision"].iloc[0]
                pre_tax_income = financials.loc["Pretax Income"].iloc[0]
                if pre_tax_income > 0:
                    return abs(tax_provision / pre_tax_income)
    except Exception:
        pass
    return default
