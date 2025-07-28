import numpy as np
import matplotlib.pyplot as plt

# Konstanten
T_surface, T_measured = 10.0, 15.0          # °C
b        = T_surface - T_measured           # −5 K
m_dot    = 55.1786268                       # kg/s
c_p      = 3_700.59                         # J/(kg·K)

n_samples = 100_000
seed       = 42

# Gradient‑Parameter  (≈ ±3 σ deckt 0.028–0.033 °C/m)
μ_g,  σ_g = 0.0305, 0.00083                 # °C m⁻¹

# NEU: Tiefe als Gleichverteilung in [1700, 2200] m
z_min, z_max = 1_700.0, 2_200.0             # m


rng = np.random.default_rng(seed)

# 1) z und g ziehen, Ausreißer nachziehen
depths    = rng.uniform(z_min, z_max, n_samples)

# Gradienten: Normalverteilung, nur positive Werte zulassen
gradients = rng.normal(μ_g, σ_g, n_samples)
mask = gradients > 0
while np.any(~mask):                        # unplausible Werte ersetzen
    n_bad = (~mask).sum()
    gradients[~mask] = rng.normal(μ_g, σ_g, n_bad)
    mask = gradients > 0

#2) ΔT und P_th berechnen
delta_T = gradients * depths + b            # K
P_th_kW = m_dot * c_p * delta_T / 1_000     # kW

#3) Statistik

def stats(a):
    mean = a.mean()
    ci95 = 1.96 * a.std(ddof=1) / np.sqrt(len(a))
    p10, p50, p90 = np.percentile(a, [10, 50, 90])
    return mean, ci95, p10, p50, p90

μ_dT, ci_dT, p10_dT, p50_dT, p90_dT = stats(delta_T)
μ_P , ci_P , p10_P , p50_P , p90_P  = stats(P_th_kW)

print(f"{n_samples:,} MC‑Samples  (z ~ U({z_min:.0f}–{z_max:.0f} m), g ~ N)")
print(f"ΔT :  Ø {μ_dT:6.2f} K  ±{ci_dT:5.2f} K   "
      f"(10.–90 %: {p10_dT:.2f}–{p90_dT:.2f} K)")
print(f"P  :  Ø {μ_P :7.1f} kW ±{ci_P :6.1f} kW  "
      f"(10.–90 %: {p10_P :.1f}–{p90_P :.1f} kW)\n")

#4) Plots
## Hexbin ΔT vs. Tiefe
plt.figure(figsize=(8, 5))
plt.hexbin(depths, delta_T, gridsize=60, bins="log", cmap="viridis")
plt.colorbar(label="log₁₀(N)")
plt.xlabel("depth z (m)")
plt.ylabel("ΔT (K)")
plt.title("ΔT – MC with z ∈ [1700, 2200] m")
plt.margins(x=0)
plt.tight_layout()
plt.show()

## Hexbin P_th vs. Tiefe
plt.figure(figsize=(8, 5))
plt.hexbin(depths, P_th_kW, gridsize=60, bins="log", cmap="plasma")
plt.colorbar(label="log₁₀(N)")
plt.xlabel("depth z (m)")
plt.ylabel("P_th (kW)")
plt.title("P_th – derived from the ΔT-values")
plt.margins(x=0)
plt.tight_layout()
plt.show()

## Histogramme (in %)
weights = np.ones_like(delta_T) / n_samples * 100
fig, ax = plt.subplots(1, 2, figsize=(13, 4))

ax[0].hist(delta_T, bins=60, weights=weights)
ax[0].axvline(μ_dT, ls="--")
ax[0].fill_betweenx([0, weights.max()], μ_dT - ci_dT, μ_dT + ci_dT, alpha=0.2)
ax[0].set_xlabel("ΔT (K)")
ax[0].set_ylabel("Frequency (%)")
ax[0].set_title("ΔT‑Distribution")

ax[1].hist(P_th_kW, bins=60, weights=weights, color="tab:orange")
ax[1].axvline(μ_P, ls="--", color="k")
ax[1].fill_betweenx([0, weights.max()], μ_P - ci_P, μ_P + ci_P, alpha=0.2, color="tab:orange")
ax[1].set_xlabel("P_th (kW)")
ax[1].set_ylabel("Frequency (%)")
ax[1].set_title("P_th‑Distribution")

fig.suptitle("Histograms (z ∈ [1700, 2200] m, %-scale)")
fig.tight_layout()
plt.show()
