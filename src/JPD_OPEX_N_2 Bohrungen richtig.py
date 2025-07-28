import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 – erforderlich für 3‑D‑Plots
from matplotlib.ticker import PercentFormatter, FuncFormatter

# 1) Eingabedaten

# 1a) Variable OPEX – diskrete Stützstellen (10% … 20% Pumpenleistung)
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

# Standardabweichung (Normalverteilung: (P90 - P10) ≈ 2 · 1.2816 · σ)
sigma_var_vals = (p90_var_vals - p10_var_vals) / (2 * 1.2816)

# Interpolationsfunktionen für μ und σ über den gesamten 10–20‑%‑Bereich
interp_mu_var = interp1d(percentages_discrete, p50_var_vals, kind="linear")
interp_sigma_var = interp1d(percentages_discrete, sigma_var_vals, kind="linear")

# 1b) Feste OPEX (unabhängig von der Pumpenleistung)
mu_fix = 112_510.80
sigma_fix = (122_284.96 - 102_673.75) / (2 * 1.2816)

# 1c) CAPEX (eine Verteilung – unabhängig von der Pumpenleistung)
# Werte stammen vom Nutzer (Komma→Punkt bereits umgesetzt)
p10_capex = 9_149_191.926
p50_capex = 9_840_863.755
p90_capex = 10_536_205.594
sigma_capex = (p90_capex - p10_capex) / (2 * 1.2816)

# Anteil der CAPEX, der als zusätzliche OPEX‑Komponente modelliert wird
capex_to_opex_ratio = 0.02  # entspricht 2%

# 2) Monte‑Carlo‑Simulation

n_sim = 10_000

# 2a) Zufällige Pumpenleistung zwischen 10% und 20%
pumpenleistung_samples = np.random.uniform(10, 20, n_sim)

# Arrays vorbereiten
fix_costs = np.empty(n_sim)
var_costs = np.empty(n_sim)

# 2b) OPEX‑Samples (fix + variabel) für jede Pumpenlast
for i, pct in enumerate(pumpenleistung_samples):
    mu_var = float(interp_mu_var(pct))
    sigma_var = float(interp_sigma_var(pct))

    fix_sample = np.random.normal(mu_fix, sigma_fix)
    var_sample = np.random.normal(mu_var, sigma_var)

    fix_costs[i] = fix_sample
    var_costs[i] = var_sample

# Erstes OPEX‑Gesamtkonstrukt (ohne CAPEX‑Anteil) – wird gleich erweitert
total_opex = fix_costs + var_costs

# 2c) CAPEX‑Samples (unabhängig vom Loop)
capex_samples = np.random.normal(p50_capex, sigma_capex, n_sim)


# 2d) **NEU**: 2‑%‑Anteil der CAPEX als zusätzliche OPEX‑Kosten

opex_from_capex = capex_to_opex_ratio * capex_samples

# Angepasste OPEX (inkl. CAPEX‑Anteil)
total_opex += opex_from_capex  # inplace‑Addition spart Speicher

# Gesamt‑Life‑Cycle‑Kosten
total_life_cycle = total_opex + capex_samples

# 3) Perzentil‑Auswertung

def pct(arr: np.ndarray, q: int | float) -> float:
    return np.percentile(arr, q)

p10_opex, p50_opex, p90_opex = pct(total_opex, 10), pct(total_opex, 50), pct(total_opex, 90)
p10_capex_sim, p50_capex_sim, p90_capex_sim = pct(capex_samples, 10), pct(capex_samples, 50), pct(capex_samples, 90)
p10_total, p50_total, p90_total = pct(total_life_cycle, 10), pct(total_life_cycle, 50), pct(total_life_cycle, 90)

# 4) Plots

plt.style.use("default")  # Zur Sicherheit – keine Farben explizit festlegen

# 4a) 3‑D‑Scatter – OPEX‑Simulation (in Mio. €)
fig1 = plt.figure(figsize=(10, 6))
ax = fig1.add_subplot(111, projection="3d")

# Fix- und Variable OPEX in Millionen Euro umrechnen
fix_mio = fix_costs / 1_000_000
var_mio = var_costs / 1_000_000

sc = ax.scatter(fix_mio, var_mio, pumpenleistung_samples,
                c=pumpenleistung_samples, cmap="viridis", s=2, alpha=0.5)

ax.set_xlabel("capex costs (Mio. €)")
ax.set_ylabel("opex costs (Mio. €)")
ax.set_zlabel("pump compacity share [%]")
ax.set_title("Joint Probability Distribution of the opex costs")

fig1.colorbar(sc, ax=ax, pad=0.1, label="pump compacity share [%]")
plt.tight_layout()
plt.show()


# 4b) Histogramm – CAPEX
plt.figure(figsize=(10, 6))
plt.hist(capex_samples, bins=50, density=True, alpha=0.7, edgecolor="black")
plt.axvline(p10_capex_sim, linestyle="--", linewidth=2, label=f"P10 = {p10_capex_sim:,.0f} €")
plt.axvline(p50_capex_sim, linewidth=2, label=f"P50 = {p50_capex_sim:,.0f} €")
plt.axvline(p90_capex_sim, linestyle="--", linewidth=2, label=f"P90 = {p90_capex_sim:,.0f} €")
plt.title("Histogramm der CAPEX‑Kosten")
plt.xlabel("CAPEX (€)")
plt.ylabel("Dichte")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Dummy-Daten für total_opex generieren (falls Original nicht vorhanden)
np.random.seed(42)
n_sim = 10_000
dummy_opex = np.random.normal(2_000_000, 200_000, n_sim)

# Werte in Millionen Euro umrechnen
opex_mio = dummy_opex / 1_000_000

# Perzentile berechnen
p10_opex_mio, p50_opex_mio, p90_opex_mio = np.percentile(opex_mio, [10, 50, 90])

# Histogramm der OPEX-Kosten
plt.figure(figsize=(10, 6))
counts, bins, patches = plt.hist(opex_mio, bins=50, density=False, alpha=0.7, edgecolor="black")

# Y-Achse in Prozent
total = counts.sum()
plt.gca().yaxis.set_major_formatter(PercentFormatter(xmax=total))

# X-Achse: Millionen mit Komma
plt.gca().xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:,.1f}"))

# Perzentillinien
plt.axvline(p10_opex_mio, linestyle="--", linewidth=2, label=f"P10 = {p10_opex_mio:,.1f} Mio. €")
plt.axvline(p50_opex_mio, linewidth=2, label=f"P50 = {p50_opex_mio:,.1f} Mio. €")
plt.axvline(p90_opex_mio, linestyle="--", linewidth=2, label=f"P90 = {p90_opex_mio:,.1f} Mio. €")

plt.title("Histogram of the opex costs")
plt.xlabel("opex costs (Mio. €)")
plt.ylabel("frequency (%)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()








# 4c) Histogramm – Gesamt‑Life‑Cycle‑Kosten (OPEX + CAPEX) in Mio. € / y-Achse in %
plt.figure(figsize=(10, 6))

# Daten in Mio. € umrechnen
life_cycle_mio = total_life_cycle / 1_000_000
p10_mio, p50_mio, p90_mio = p10_total / 1_000_000, p50_total / 1_000_000, p90_total / 1_000_000

# Histogramm mit absoluten Häufigkeiten
counts, bins, patches = plt.hist(life_cycle_mio, bins=50, density=False,
                                 alpha=0.7, edgecolor="black")

# Y-Achse in Prozent
total = counts.sum()
plt.gca().yaxis.set_major_formatter(PercentFormatter(xmax=total))

# X-Achse Formatierung: Millionen mit Komma
plt.gca().xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:,.1f}"))

# Perzentillinien
plt.axvline(p10_mio, linestyle="--", linewidth=2, label=f"P10 = {p10_mio:,.1f} Mio. €")
plt.axvline(p50_mio, linewidth=2, label=f"P50 = {p50_mio:,.1f} Mio. €")
plt.axvline(p90_mio, linestyle="--", linewidth=2, label=f"P90 = {p90_mio:,.1f} Mio. €")

plt.title("Histogram of the opex costs")
plt.xlabel("opex costs (Mio. €)")
plt.ylabel("frequency (%)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# -----------------------------------------------------------------------------
# 5) Konsolenausgabe
# -----------------------------------------------------------------------------
print("===== Perzentil‑Ergebnisse (inkl. 2 % CAPEX in OPEX) =====")
print(f"OPEX   – P10: {p10_opex:,.0f} €,  P50: {p50_opex:,.0f} €,  P90: {p90_opex:,.0f} €")
print(f"CAPEX  – P10: {p10_capex_sim:,.0f} €,  P50: {p50_capex_sim:,.0f} €,  P90: {p90_capex_sim:,.0f} €")
print(f"TOTAL  – P10: {p10_total:,.0f} €,  P50: {p50_total:,.0f} €,  P90: {p90_total:,.0f} €")
