import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import truncnorm
from mpl_toolkits.mplot3d import Axes3D

n_sim = 10000

# Funktion für Truncated Normal
def truncated_normal(mean, std, low, upp, size):
    a, b = (low - mean) / std, (upp - mean) / std
    return truncnorm.rvs(a, b, loc=mean, scale=std, size=size)

# Tiefe simulieren (in m)

x = truncated_normal(1950, 150, 1700, 2200, n_sim)

# Bruttobohrkosten berechnen (in €)
B_brutto = 2*(0.131223 * x**2 + 2508.990455 * x + 1_643_364.545458)

# Netto-Bohrkosten (in €)
B_netto = 0.6 * B_brutto

# Subventionen (in €)
S = 0.4 * B_brutto

# Länge simulieren (in m)
l = truncated_normal(2000, 500, 1000, 3000, n_sim)

# Pipelinekosten (in €)
P = 700.0 * l

# Netto Capex
Capex_netto = B_netto + P

# Alles in Mio €
B_netto_mio = B_netto / 1e6
S_mio = S / 1e6
P_mio = P / 1e6
Capex_netto_mio = Capex_netto / 1e6

# 3D-Plot

fig = plt.figure(figsize=(10,7))
ax = fig.add_subplot(111, projection='3d')

ax.scatter(B_netto_mio, P_mio, S_mio, s=2, alpha=0.3)

ax.set_xlabel('net drilling costs (Mio €)')
ax.set_ylabel('pipeline costs (Mio €)')
ax.set_zlabel('subsidies (Mio €)')
ax.set_title('Joint Distribution with bivariate normal distribution')

plt.show()

# Histogramm Netto Capex
plt.figure(figsize=(10,6))

# Absolutes Histogramm berechnen
counts, bins = np.histogram(Capex_netto_mio, bins=50)

# In Prozent umrechnen
counts_percent = counts / counts.sum() * 100

# Histogramm manuell plotten
bin_centers = 0.5 * (bins[1:] + bins[:-1])
plt.bar(bin_centers, counts_percent, width=(bins[1] - bins[0]), color='lightgreen', edgecolor='black')

plt.title('Histogram net capex costs (Mio €)')
plt.xlabel('net capex costs(Mio €)')
plt.ylabel('Frequency (%)')
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()

# Ergebnisse ausgeben

print("Ø Netto-Bohrkosten (Mio €):", np.mean(B_netto_mio))
print("Ø Pipelinekosten (Mio €):", np.mean(P_mio))
print("Ø Subventionen (Mio €):", np.mean(S_mio))
print("Ø Netto Capex (Mio €):", np.mean(Capex_netto_mio))
print("90. Perzentil Netto Capex (Mio €):", np.percentile(Capex_netto_mio, 90))


print("Perzentile Netto Capex (Mio €):")
print("P10:", np.percentile(Capex_netto, 10))
print("P50 (Median):", np.percentile(Capex_netto, 50))
print("P90:", np.percentile(Capex_netto, 90))
