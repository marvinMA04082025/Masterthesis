def kwf(rate: float, years: int) -> float:
    if years <= 0:
        raise ValueError("years muss > 0 sein")
    if rate == 0:
        return 1 / years
    r_pow = (1 + rate) ** years
    return rate * r_pow / (r_pow - 1)

capex    = 8_000_000   # €
lifetime = 30          # Jahre

print("r [%] | KWF    | Annuität [€]")
print("-------------------------------")
for r_pct in range(6, 11):           # 6 … 10 %
    r = r_pct / 100
    factor = kwf(r, lifetime)
    ann    = factor * capex
    print(f"{r_pct:<5} | {factor:.4f} | {ann:,.0f}")