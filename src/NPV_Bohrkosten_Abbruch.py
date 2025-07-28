import numpy as np
import matplotlib.pyplot as plt

# Parameters
CAPEX_P10 = 7_818_000
CAPEX_P50 = 8_433_000
CAPEX_P90 = 9_059_000
N_SIM     = 10_000
RNG_SEED  = 42
bins      = 60

def lognormal_mu_sigma(p10, p50, p90):
    """μ, σ einer Log-Normalverteilung aus P10/P50/P90"""
    z10, z90 = -1.2815515655446004, 1.2815515655446004
    mu    = np.log(p50)
    sigma = (np.log(p90) - np.log(p10)) / (z90 - z10)
    return mu, sigma

mu_capex, sig_capex = lognormal_mu_sigma(CAPEX_P10, CAPEX_P50, CAPEX_P90)

# Simulate failure NPV: -CapEx (100% Fehlschlag)
rng = np.random.default_rng(RNG_SEED)
npv_failure = -rng.lognormal(mu_capex, sig_capex, N_SIM)  # [€]

# Histogram weights to convert counts to percentage
weights = np.ones_like(npv_failure) / N_SIM * 100  # each sample represents 0.01%

# Plot
plt.figure(figsize=(8, 5))
plt.hist(npv_failure / 1e6, bins=bins, weights=weights,
         alpha=0.75, label="NPV – Failure")

median_fail = np.median(npv_failure) / 1e6
plt.axvline(median_fail, linestyle="dashed", linewidth=2,
            label=f"Median: {median_fail:,.1f}M€")

# --- zero line for reference ------------------------------------------
plt.axvline(0, linewidth=1, label="0€‐axis")
xmin, xmax = plt.xlim()
plt.xlim(xmin, max(0, xmax))        # sicherstellen, dass 0 rechts sichtbar ist
# -----------------------------------------------------------------------

plt.xlabel("NPV (Million €)")
plt.ylabel("Frequency (%)")
plt.title("Distrbution of the Net Present Value (Monte‑Carlo)")
plt.legend()
plt.tight_layout()
plt.show()
