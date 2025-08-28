import numpy as np
import matplotlib.pyplot as plt

T_surface   = 10.0       # °C  Oberflächentemperatur
T_measured  = 15.0       # °C  gemessene Temperatur
depth_min   = 1700       # m   Starttiefe
depth_max   = 2200       # m   Endtiefe
grad_min    = 0.028      # °C/m   untere Gradientgrenze
grad_max    = 0.033      # °C/m   obere Gradientgrenze
n_samples   = 100_000    # Anzahl Monte-Carlo-Samples
seed        = 42         # setzt einen pseudo-zufälligen Startwert

rng = np.random.default_rng(seed)

# Zufällige Tiefe und Gradient für jedes Sample
depths     = rng.uniform(depth_min, depth_max, n_samples)
gradients  = rng.uniform(grad_min, grad_max, n_samples)

# b = Achsenabschnitt
b = T_surface - T_measured        # hier −5 K

# ΔT berechnen
delta_T = gradients * depths + b  # ndarray (n_samples,)

#Statistik ausgeben 
mean = delta_T.mean()
std  = delta_T.std(ddof=1)
ci95 = 1.96 * std / np.sqrt(n_samples)
p10, p50, p90 = np.percentile(delta_T, [10, 50, 90])

print(f"{n_samples:,} Simulationen")
print(f"Ø ΔT   : {mean:.2f} K  ± {ci95:.2f} K  (95 %-KI)")
print(f"Median : {p50:.2f} K  (10.–90. Perzentil: {p10:.2f}–{p90:.2f} K)")
print()

#Plots
# 1) Hexbin-Plot ΔT vs. Tiefe
plt.figure(figsize=(8, 5))
hb = plt.hexbin(depths, delta_T, gridsize=60, cmap="viridis", bins="log")
plt.colorbar(hb, label="log10(Anzahl)")
plt.xlabel("Depth z (m)")
plt.ylabel("ΔT (K)")
plt.title("Monte-Carlo-Verteilung von ΔT(z)")
plt.tight_layout()
plt.show()

# 2) Histogramm ΔT in Prozent
weights = np.ones_like(delta_T) / len(delta_T) * 100   # Normalisierung auf 100 %
plt.figure(figsize=(7, 4))
plt.hist(delta_T, bins=60, weights=weights)
plt.axvline(mean, color="k", linestyle="--", label=f"Mittel = {mean:.2f} K")
plt.fill_betweenx([0, weights.max()],
                  mean - ci95, mean + ci95,
                  alpha=0.2, label="95 %-KI")
plt.xlabel("ΔT (K)")
plt.ylabel("Häufigkeit (%)")
plt.title("ΔT-Verteilung (Monte-Carlo)")
plt.legend()
plt.tight_layout()
plt.show()
