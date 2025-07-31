import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal
from scipy.interpolate import interp1d

# Diskrete Stützpunkte der Pumpenkosten
percentages_discrete = np.arange(10, 21, 1)
p50_var_vals = np.array([1598220, 1758042, 1917864, 2077686, 2237508,
                         2397330, 2557152, 2716974, 2876796, 3036618, 3196440])
p10_var_vals = np.array([1398060, 1537866, 1677672, 1817478, 1957284,
                         2097090, 2236896, 2376702, 2516508, 2656314, 2796120])
p90_var_vals = np.array([1812600, 1993860, 2175120, 2356380, 2537640,
                         2718900, 2900160, 3081420, 3262680, 3443940, 3625200])

# σ berechnen
sigma_var_vals = (p90_var_vals - p10_var_vals) / (2 * 1.2816)

# Interpolationsfunktionen
interp_mu_var = interp1d(percentages_discrete, p50_var_vals, kind='linear')
interp_sigma_var = interp1d(percentages_discrete, sigma_var_vals, kind='linear')

# Fixkosten-Parameter
mu_fix = 112510.80
sigma_fix = (122284.96 - 102673.75) / (2 * 1.2816)

# Anzahl Simulationen
n_sim = 10000

# Zufällige Pumpenleistungen zwischen 10 % und 20 %
pumpenleistung_samples = np.random.uniform(10, 20, n_sim)

# Arrays vorbereiten
fix_costs = []
var_costs = []
total_opex = []

# Simulation
for pct in pumpenleistung_samples:
    mu_var = interp_mu_var(pct)
    sigma_var = interp_sigma_var(pct)

    # Unabhängige Normalverteilungen
    fix_sample = np.random.normal(mu_fix, sigma_fix)
    var_sample = np.random.normal(mu_var, sigma_var)

    total = fix_sample + var_sample

    fix_costs.append(fix_sample)
    var_costs.append(var_sample)
    total_opex.append(total)

fix_costs = np.array(fix_costs)
var_costs = np.array(var_costs)
total_opex = np.array(total_opex)

# P10, P50, P90 berechnen
p10 = np.percentile(total_opex, 10)
p50 = np.percentile(total_opex, 50)
p90 = np.percentile(total_opex, 90)

# -----------------------------------------
# Plot 1: 3D Scatter Plot (separat)
# -----------------------------------------
fig1 = plt.figure(figsize=(10, 6))
ax = fig1.add_subplot(111, projection='3d')

sc = ax.scatter(fix_costs, var_costs, pumpenleistung_samples,
                c=pumpenleistung_samples, cmap='viridis', s=2, alpha=0.5)

ax.set_xlabel('Fixkosten (€)')
ax.set_ylabel('Variable Kosten (€)')
ax.set_zlabel('Pumpenleistung [%]')
ax.set_title('3D Scatter Plot: Opex Simulation')

cb = plt.colorbar(sc, ax=ax, pad=0.1)
cb.set_label('Pumpenleistung [%]')

plt.tight_layout()
plt.show()

# -----------------------------------------
# Plot 2: Histogramm (separat)
# -----------------------------------------
plt.figure(figsize=(10, 6))

counts, bins, patches = plt.hist(total_opex, bins=50, color='skyblue', edgecolor='black', density=True, alpha=0.7)

plt.axvline(p10, color='red', linestyle='--', linewidth=2, label=f'P10 = {p10:,.0f} €')
plt.axvline(p50, color='black', linestyle='-', linewidth=2, label=f'P50 = {p50:,.0f} €')
plt.axvline(p90, color='green', linestyle='--', linewidth=2, label=f'P90 = {p90:,.0f} €')

plt.title('Histogramm der Gesamt-OPEX-Kosten')
plt.xlabel('Gesamt-OPEX (€)')
plt.ylabel('Dichte')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

print(f"P10 OPEX: {p10:,.2f} €")
print(f"P50 OPEX: {p50:,.2f} €")
print(f"P90 OPEX: {p90:,.2f} €")
