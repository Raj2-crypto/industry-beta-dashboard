
# pre-tax cost of debt = interest expense / total debt
def calc_cost_of_debt(financials, total_debt_native):
    try:
        if financials is not None and not financials.empty:
            if "Interest Expense" in financials.index:
                interest_expense = abs(financials.loc["Interest Expense"].iloc[0])
                if total_debt_native > 0:
                    return interest_expense / total_debt_native
    except Exception:
        pass
    return 0.0