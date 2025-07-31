import numpy as np
import pandas as pd
from scipy.stats import truncnorm

#Parameter
N_SIM = 10_000
RNG = np.random.default_rng(42)

# Trunkierte Normalverteilung für die Pipeline-Länge
def truncated_normal(mean, std, low, upp, size, rng):
    a, b = (low - mean) / std, (upp - mean) / std
    return truncnorm.rvs(a, b, loc=mean, scale=std, size=size, random_state=rng)

# Pipeline-Länge [m] und -Kosten [€]
length = truncated_normal(mean=2000, std=500, low=1000, upp=3000, size=N_SIM, rng=RNG)
pipeline_cost = 700.0 * length  # €/m

# Fixe Brutto-Bohrkosten [€] pro Szenario
scenarios = {
    "P10": 12_874_705,
    "P50": 14_077_173,
    "P90": 15_289_907,
}

#Simulation
rows = []
for label, b_brutto in scenarios.items():
    capex_no_sub = b_brutto + pipeline_cost  # ungesubventioniert
    rows.append(
        {
            "Szenario": label,
            "CAPEX P10 o.S. (M€)": np.percentile(capex_no_sub, 10) / 1e6,
            "CAPEX P50 o.S. (M€)": np.percentile(capex_no_sub, 50) / 1e6,
            "CAPEX P90 o.S. (M€)": np.percentile(capex_no_sub, 90) / 1e6,
        }
    )

df = pd.DataFrame(rows).set_index("Szenario").round(2)
print(df.to_markdown())
