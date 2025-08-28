import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 – required for 3‑D plots

# ------------------------------
# 1) Input data
# ------------------------------
# 1a) Variable OPEX – discrete support points (10% … 20% Pumpenleistung)
percentages_discrete = np.arange(10, 21, 1)

p50_var_vals = np.array([
    1_598_220, 1_758_042, 1_917_864, 2_077_686, 2_237_508,
    2_397_330, 2_557_152, 2_716_974, 2_876_796, 3_036_618, 3_196_440,
])

p10_var_vals = np.array([
    1_398_060, 1_537_866, 1_677_672, 1_817_478, 1_957_284,
    2_097_090, 2_236_896, 2_376_702, 2_516_508, 2_656_314, 2_796_120,
])

p90_var_vals = np.array([
    1_812_600, 1_993_860, 2_175_120, 2_356_380, 2_537_640,
    2_718_900, 2_900_160, 3_081_420, 3_262_680, 3_443_940, 3_625_200,
])

# Standard deviation (assume Normal: (P90 - P10) ≈ 2 · 1.2816 · σ)
sigma_var_vals = (p90_var_vals - p10_var_vals) / (2 * 1.2816)

# Linear interpolation functions for μ and σ across the entire 10–20% range
interp_mu_var = interp1d(percentages_discrete, p50_var_vals, kind="linear")
interp_sigma_var = interp1d(percentages_discrete, sigma_var_vals, kind="linear")

# 1b) Fixed OPEX (unabhängig von der Pumpenleistung)
# Gegebene Perzentile
p10_fix = 9_149_191.926 * 0.02
p90_fix = 10_536_205.594 *0.02
# Erwartungswert und Streuung
mu_fix = (p10_fix + p90_fix) / 2
sigma_fix = (p90_fix - p10_fix) / (2 * 1.2816)

# 1c) CAPEX (single distribution – independent of Pumpenleistung)
# Values supplied by user (comma → dot conversion already applied)
p10_capex = 9_149_191.926
p50_capex = 9_840_863.755
p90_capex = 10_536_205.594
sigma_capex = (p90_capex - p10_capex) / (2 * 1.2816)

# ------------------------------
# 2) Monte‑Carlo Simulation
# ------------------------------
n_sim = 10_000

# 2a) Random Pumpenleistung between 10% and 20%
pumpenleistung_samples = np.random.uniform(10, 20, n_sim)

# Prepare arrays
fix_costs = np.empty(n_sim)
var_costs = np.empty(n_sim)
total_opex = np.empty(n_sim)

# 2b) Draw OPEX samples (fix + variable) for each pump‑load sample
for i, pct in enumerate(pumpenleistung_samples):
    mu_var = float(interp_mu_var(pct))
    sigma_var = float(interp_sigma_var(pct))

    fix_sample = np.random.normal(mu_fix, sigma_fix)
    var_sample = np.random.normal(mu_var, sigma_var)

    fix_costs[i] = fix_sample
    var_costs[i] = var_sample
    total_opex[i] = fix_sample + var_sample

# 2c) Draw CAPEX samples (independent of loop)
capex_samples = np.random.normal(p50_capex, sigma_capex, n_sim)

total_life_cycle = total_opex + capex_samples

# ------------------------------
# 3) Percentile evaluation
# ------------------------------

def pct(arr, q):
    return np.percentile(arr, q)

p10_opex, p50_opex, p90_opex = pct(total_opex, 10), pct(total_opex, 50), pct(total_opex, 90)
p10_capex, p50_capex_sim, p90_capex_sim = pct(capex_samples, 10), pct(capex_samples, 50), pct(capex_samples, 90)
p10_total, p50_total, p90_total = pct(total_life_cycle, 10), pct(total_life_cycle, 50), pct(total_life_cycle, 90)

# ------------------------------
# 4) Plots
# ------------------------------
# 4a) 3‑D scatter (unchanged)
fig1 = plt.figure(figsize=(10, 6))
ax = fig1.add_subplot(111, projection="3d")
sc = ax.scatter(fix_costs, var_costs, pumpenleistung_samples,
                c=pumpenleistung_samples, cmap="viridis", s=2, alpha=0.5)
ax.set_xlabel("Fixkosten (€)")
ax.set_ylabel("Variable Kosten (€)")
ax.set_zlabel("Pumpenleistung [%]")
ax.set_title("3D‑Scatter: OPEX‑Simulation")
fig1.colorbar(sc, ax=ax, pad=0.1, label="Pumpenleistung [%]")
plt.tight_layout()
plt.show()

# 4b) Histogram – CAPEX
plt.figure(figsize=(10, 6))
plt.hist(capex_samples, bins=50, density=True, alpha=0.7, edgecolor="black")
plt.axvline(p10_capex, color="red", linestyle="--", linewidth=2, label=f"P10 = {p10_capex:,.0f} €")
plt.axvline(p50_capex_sim, color="black", linewidth=2, label=f"P50 = {p50_capex_sim:,.0f} €")
plt.axvline(p90_capex_sim, color="green", linestyle="--", linewidth=2, label=f"P90 = {p90_capex_sim:,.0f} €")
plt.title("Histogramm der CAPEX‑Kosten")
plt.xlabel("CAPEX (€)")
plt.ylabel("Dichte")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# 4c) Histogram – Total Life‑Cycle Costs
plt.figure(figsize=(10, 6))
plt.hist(total_life_cycle, bins=50, density=True, alpha=0.7, edgecolor="black")
plt.axvline(p10_total, color="red", linestyle="--", linewidth=2, label=f"P10 = {p10_total:,.0f} €")
plt.axvline(p50_total, color="black", linewidth=2, label=f"P50 = {p50_total:,.0f} €")
plt.axvline(p90_total, color="green", linestyle="--", linewidth=2, label=f"P90 = {p90_total:,.0f} €")
plt.title("Histogramm der Gesamt‑Life‑Cycle‑Kosten (OPEX + CAPEX)")
plt.xlabel("Gesamtkosten (€)")
plt.ylabel("Dichte")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# ------------------------------
# 5) Console output
# ------------------------------
print("===== Percentile Results =====")
print(f"OPEX   – P10: {p10_opex:,.0f} €,  P50: {p50_opex:,.0f} €,  P90: {p90_opex:,.0f} €")
print(f"CAPEX  – P10: {p10_capex:,.0f} €,  P50: {p50_capex_sim:,.0f} €,  P90: {p90_capex_sim:,.0f} €")
print(f"TOTAL  – P10: {p10_total:,.0f} €,  P50: {p50_total:,.0f} €,  P90: {p90_total:,.0f} €")
