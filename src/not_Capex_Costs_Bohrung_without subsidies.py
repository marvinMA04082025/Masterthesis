import numpy as np
import pandas as pd
from scipy.stats import truncnorm

#Parameters
n_sim = 10_000
rng = np.random.default_rng(42)

# Truncated normal helper
def truncated_normal(mean, std, low, upp, size, rng):
    a, b = (low - mean) / std, (upp - mean) / std
    return truncnorm.rvs(a, b, loc=mean, scale=std, size=size, random_state=rng)


# Pipeline length distribution
l = truncated_normal(mean=2000, std=500, low=1000, upp=3000, size=n_sim, rng=rng)
P = 700.0 * l  # €

# Fixed Brutto-Bohrkosten scenarios (in €)
scenarios = {
    "P10": 7_818_000,
    "P50": 8_433_000,
    "P90": 9_059_000,
}
#P10 : 7.818
#Median (P50): 8.433
#P90 : 9.059
results = []

for label, B_brutto in scenarios.items():
    B_netto = 0.6 * B_brutto  # € after 40% subsidy
    Capex = B_netto + P  # € with subsidy
    Capex_no_sub = B_brutto + P  # € without subsidy

    results.append({
        "Szenario": label,
        "B_brutto (M€)": B_brutto / 1e6,
        "B_netto (M€)": B_netto / 1e6,
        "Capex Mean (M€)": Capex.mean() / 1e6,
        "Capex Mean (ohne Subv.) (M€)": Capex_no_sub.mean() / 1e6,
        "Capex P10 (M€)": np.percentile(Capex, 10) / 1e6,
        "Capex Median (M€)": np.percentile(Capex, 50) / 1e6,
        "Capex P90 (M€)": np.percentile(Capex, 90) / 1e6,
    })

df = pd.DataFrame(results).set_index("Szenario").round(2)

print(df.to_markdown())
