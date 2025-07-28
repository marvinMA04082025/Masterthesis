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
plt.ylabel("frequency (%)")
plt.title("Distrbution of the Net Present Value (Monte‑Carlo)")
plt.legend()
plt.tight_layout()
plt.show()

# Simulate NPV with 40% subsidy on drilling (i.e., 40% refund of CAPEX)
npv_failure_sub = -0.6 * rng.lognormal(mu_capex, sig_capex, N_SIM)  # 60% Verlust

# Plot both distributions
plt.figure(figsize=(9, 5))
plt.hist(npv_failure / 1e6, bins=bins, weights=weights,
         alpha=0.6, label="NPV – No Subsidy")
plt.hist(npv_failure_sub / 1e6, bins=bins, weights=weights,
         alpha=0.6, label="NPV – With Subsidy")

# Median lines
median_fail = np.median(npv_failure) / 1e6
median_sub  = np.median(npv_failure_sub) / 1e6
plt.axvline(median_fail, linestyle="dashed", linewidth=2,
            label=f"Median No Subsidy: {median_fail:,.1f}M€")
plt.axvline(median_sub, linestyle="dashed", linewidth=2, color="green",
            label=f"Median With Subsidy: {median_sub:,.1f}M€")

# Zero line
plt.axvline(0, linewidth=1, color="black", label="0€‐axis")
xmin, xmax = plt.xlim()
plt.xlim(xmin, max(0, xmax))

plt.xlabel("NPV (Million €)")
plt.ylabel("frequency (%)")
plt.title("NPV Distribution in Failure Case (with/without Subsidy)")
plt.legend()
plt.tight_layout()
plt.show()
