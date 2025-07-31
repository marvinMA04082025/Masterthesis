
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import truncnorm

# --------------------------------------------------
# Einstellungen
# --------------------------------------------------
N_SIM = 10_000                  # Anzahl Simulationen
SEED   = 42                     # Reproduzierbarkeit

# Truncated-Normal-Hilfsfunktion
def truncated_normal(mean, std, low, upp, size, rng):
    a, b = (low - mean) / std, (upp - mean) / std
    return truncnorm.rvs(a, b, loc=mean, scale=std, size=size, random_state=rng)

# Zufallszahlgenerator
rng = np.random.default_rng(SEED)

# --------------------------------------------------
# 1) Tiefen simulieren [m]
# --------------------------------------------------
depth_m = truncated_normal(mean=1950, std=150, low=1700, upp=2200,
                           size=N_SIM, rng=rng)

# Bruttobohrkosten [€]
B_brutto_eur = 2*(0.131223 * depth_m**2 + 2_508.990455 * depth_m + 1_643_364.545458)

# Netto-Bohrkosten = 60 % der Brutto­kosten  [€]
B_netto_eur = B_brutto_eur

# --------------------------------------------------
# 2) Leitungslängen simulieren [m]
# --------------------------------------------------
length_m = truncated_normal(mean=2000, std=500, low=1000, upp=3000,
                            size=N_SIM, rng=rng)

# Pipelinekosten [€]
P_eur = 700.0 * length_m

# --------------------------------------------------
# 3) Netto CAPEX [€]  (ohne Subventionen)
# --------------------------------------------------
Capex_netto_eur = B_netto_eur + P_eur

# --------------------------------------------------
# 4) In Millionen € umrechnen
# --------------------------------------------------
B_netto_mio  = B_netto_eur   / 1e6
P_mio        = P_eur         / 1e6
Capex_mio    = Capex_netto_eur / 1e6

# --------------------------------------------------
# 5) Visualisierungen
# --------------------------------------------------
# 2D-Scatter Bohrkosten vs. Pipelinekosten
plt.figure(figsize=(8,6))
plt.scatter(B_netto_mio, P_mio, s=3, alpha=0.3)
plt.xlabel("Netto-Bohrkosten [Mio €]")
plt.ylabel("Pipelinekosten [Mio €]")
plt.title("Joint Distribution: Bohr- vs. Pipelinekosten")
plt.tight_layout()
plt.show()

# Histogramm Netto CAPEX
plt.figure(figsize=(8,5))
plt.hist(Capex_mio, bins=50, edgecolor="black", alpha=0.7)
plt.xlabel("Netto CAPEX [Mio €]")
plt.ylabel("Häufigkeit")
plt.title("Histogramm Netto CAPEX")
plt.tight_layout()
plt.show()

# --------------------------------------------------
# 6) Kennzahlen ausgeben
# --------------------------------------------------
print("Ø Netto-Bohrkosten  [Mio €]:", np.mean(B_netto_mio).round(3))
print("Ø Pipelinekosten    [Mio €]:", np.mean(P_mio).round(3))
print("Ø Netto CAPEX       [Mio €]:", np.mean(Capex_mio).round(3))
print()
print("Perzentile Netto CAPEX [Mio €]:")
print("P10 :", (np.percentile(Capex_netto_eur, 10)/1e6).round(3))
print("Median (P50):", (np.percentile(Capex_netto_eur, 50)/1e6).round(3))
print("P90 :", (np.percentile(Capex_netto_eur, 90)/1e6).round(3))
