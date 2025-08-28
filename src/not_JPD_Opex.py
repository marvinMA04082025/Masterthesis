import numpy as np

# Triangular Verteilung für CAPEX
capex_samples = np.random.triangular(
    left=5133687.53,
    mode=5625539.90,
    right=6114248.02,
    size=10000
)

# Fixkosten = 2 % CAPEX
fixkosten_samples = 0.02 * capex_samples

# Triangular Verteilung für variable Kosten (hier 10 % Anteil)
var_cost_samples = np.random.triangular(
    left=1398060.00,
    mode=1598220.00,
    right=1812600.00,
    size=10000
)

# Gesamte Opex
opex_samples = fixkosten_samples + var_cost_samples

print("Mean Opex:", np.mean(opex_samples))
print("P10 Opex:", np.percentile(opex_samples, 10))
print("P50 Opex:", np.percentile(opex_samples, 50))
print("P90 Opex:", np.percentile(opex_samples, 90))
