import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import truncnorm
from mpl_toolkits.mplot3d import Axes3D

n_sim = 10000

# Funktion für Truncated Normal
def truncated_normal(mean, std, low, upp, size):
    a, b = (low - mean) / std, (upp - mean) / std
    return truncnorm.rvs(a, b, loc=mean, scale=std, size=size)

# -------------------------------
# Tiefe simulieren (in m)
# -------------------------------
x = truncated_normal(1950, 150, 1700, 2200, n_sim)

# Bruttobohrkosten berechnen (in €)
B_brutto = 2*(0.131223 * x**2 + 2508.990455 * x + 1_643_364.545458)

# Netto-Bohrkosten (in €)
B_netto = 0.6 * B_brutto

# Subventionen (in €)
S = 0.4 * B_brutto

# -------------------------------
# Länge simulieren (in m)
# -------------------------------
l = truncated_normal(2000, 500, 1000, 3000, n_sim)

# Pipelinekosten (in €)
P = 700.0 * l

# -------------------------------
# Netto Capex berechnen
# -------------------------------
Capex_netto = B_netto + P

# -------------------------------
# Für Histogramm alles in Mio €
# -------------------------------
B_netto_mio = B_netto / 1e6
P_mio = P / 1e6

# -------------------------------
# 2D-Histogramm (Binning)
# -------------------------------
hist, xedges, yedges = np.histogram2d(B_netto_mio, P_mio, bins=20)

hist_percent = (hist / n_sim) * 100
# Position der Balken ermitteln
xpos, ypos = np.meshgrid(xedges[:-1], yedges[:-1], indexing="ij")

xpos = xpos.ravel()
ypos = ypos.ravel()
zpos = np.zeros_like(xpos)

dx = dy = (xedges[1] - xedges[0]) * 0.9   # 90% Balken-Breite
dz = hist_percent.ravel()

# -------------------------------
# Plotten
# -------------------------------
fig = plt.figure(figsize=(10,7))
ax = fig.add_subplot(111, projection='3d')

ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color='skyblue', alpha=0.8, edgecolor='black')

ax.set_xlabel('net drilling costs (Mio €)')
ax.set_ylabel('pipeline costs (Mio €)')
ax.set_zlabel('frequency [%]')
ax.set_title('Joint probability distribution of the capex costs frequency')

plt.show()

print("Perzentile Netto Capex (Mio €):")
print("P10:", np.percentile(Capex_netto, 10))
print("P50 (Median):", np.percentile(Capex_netto, 50))
print("P90:", np.percentile(Capex_netto, 90))
