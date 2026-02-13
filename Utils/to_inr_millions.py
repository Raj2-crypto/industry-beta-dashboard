def to_inr_millions(val, exchange_rate):
    if not val:
        return 0.0
    return (val * exchange_rate) / 1_000_000
