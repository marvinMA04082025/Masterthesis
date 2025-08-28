import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

n_sim = 10000

# Tiefe simulieren (in m)
x = np.random.uniform(1700, 2200, n_sim)

# Bruttobohrkosten berechnen (in €)
B_brutto = 0.131223 * x**2 + 2508.990455 * x + 1_643_364.545458

# Netto-Bohrkosten (in €)
B_netto = 0.6 * B_brutto

# Subventionen (in €)
S = 0.4 * B_brutto

# Pipeline-Länge simulieren (in m)
l = np.random.uniform(1000, 3000, n_sim)

# Pipelinekosten (in €)
P = 700.0 * l

# Netto Capex
Capex_netto = B_netto + P

# Alles in Mio €
B_netto_mio = B_netto / 1e6
S_mio = S / 1e6
P_mio = P / 1e6
Capex_netto_mio = Capex_netto / 1e6

# 3D-Scatter-Plot
fig = plt.figure(figsize=(10,7))
ax = fig.add_subplot(111, projection='3d')

ax.scatter(B_netto_mio, P_mio, S_mio, s=2, alpha=0.3)

ax.set_xlabel('Netto-Bohrkosten (Mio €)')
ax.set_ylabel('Pipelinekosten (Mio €)')
ax.set_zlabel('Subventionen (Mio €)')
ax.set_title('Joint Distribution: Bohrkosten, Pipelinekosten, Subventionen')

plt.show()

# Ergebniswerte
print("Ø Netto-Bohrkosten (Mio €):", np.mean(B_netto_mio))
print("Ø Pipelinekosten (Mio €):", np.mean(P_mio))
print("Ø Subventionen (Mio €):", np.mean(S_mio))
print("Ø Netto Capex (Mio €):", np.mean(Capex_netto_mio))
print("90. Perzentil Netto Capex (Mio €):", np.percentile(Capex_netto_mio, 90))
