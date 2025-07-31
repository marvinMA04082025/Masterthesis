import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

from Pth        import Pth, c_p, b
from massenstrom import m_dot

#Konstanten
VLS = 8_000 # Volllaststunden [h/a]
N_SAMPLES = 100_000

# Monte-Carlo-Sampler:  Tiefe x  & Gradient g
x_samples = np.random.uniform(1700, 2200, N_SAMPLES)     # [m]
g_samples = np.random.uniform(0.028, 0.033, N_SAMPLES)   # [°C/m]

# Wärmeleistung (W) über dein Pth-Modul berechnen
P_W = Pth(x_samples, g_samples, m_dot=m_dot, c_p=c_p, b=b)

# Jahresarbeit in GWh_th
Q_GWh = P_W * VLS / 1_000_000_000   # 1 GWh = 3.6 · 10¹² J

# --- Auswertung -----------------------------------
mean = np.mean(Q_GWh)
p10, p50, p90 = np.percentile(Q_GWh, [10, 50, 90])

print(f"⌀ Mittelwert : {mean:8.2f} GWh_th/a")
print(f"P10          : {p10:8.2f} GWh_th/a")
print(f"P50 (Median) : {p50:8.2f} GWh_th/a")
print(f"P90          : {p90:8.2f} GWh_th/a")

# Histogram
plt.figure(figsize=(7,4))
plt.hist(Q_GWh,
         bins=60,
         weights=np.ones_like(Q_GWh)*100/Q_GWh.size,
         edgecolor="black")
plt.gca().yaxis.set_major_formatter(PercentFormatter())  # y-Achse in %
plt.xlabel("annual heat prodution [GWh$_{th}$/a]")
plt.ylabel("Frequency [%]")
plt.title(f"Monte-Carlo-Verteilung of Q  (n = {N_SAMPLES:,})")
plt.grid(axis="y", ls=":")
plt.tight_layout()
plt.show()

#  PARAMETER

F_LOWER, F_UPPER = 0.10, 0.20
HEAT_PRICE = 80
BINS = 60

#  PUMPENANTEIL SAMPLEN  &  OPEX (= variable Betriebskosten)

f_samples   = np.random.uniform(F_LOWER, F_UPPER, Q_GWh.size)
E_pump_GWh  = Q_GWh * f_samples
opex_eur    = E_pump_GWh * 1_000 * HEAT_PRICE

#  STATISTIK  (Mittelwert + P10 / P50 / P90)
mean, p10, p50, p90 = (
    np.mean(opex_eur),
    *np.percentile(opex_eur, [10, 50, 90])
)

print("Variable OPEX – Pumpenkosten ")
print(f"⌀ Mittelwert : {mean:10,.0f} € /a")
print(f"P10          : {p10:10,.0f} € /a")
print(f"P50 (Median) : {p50:10,.0f} € /a")
print(f"P90          : {p90:10,.0f} € /a")

#  MONTE-CARLO-DIAGRAMM  (Kostenverteilung in %)

plt.figure(figsize=(7, 4))

# Umrechnung in Mio. €
opex_mio_eur = opex_eur / 1_000_000

plt.hist(opex_mio_eur,
         bins=BINS,
         weights=np.ones_like(opex_mio_eur) * 100 / opex_mio_eur.size,
         edgecolor="black")
plt.gca().yaxis.set_major_formatter(PercentFormatter())  # y-Achse in %
plt.xlabel("annual Opex-costs (pumps) [Mio. €]")
plt.ylabel("Frequency [%]")
plt.title(f"Monte-Carlo-Distribution of the pumping costs")
plt.grid(axis="y", ls=":")
plt.tight_layout()
plt.show()

# ---------------------------------------------------------------------------
#  OPEX bei festen Pumpenanteilen 10 % und 20 %
# ---------------------------------------------------------------------------
for f_fixed in [0.10, 0.20]:
    E_pump_GWh_fixed = Q_GWh * f_fixed
    opex_eur_fixed = E_pump_GWh_fixed * 1_000 * HEAT_PRICE
    mean_fixed = np.mean(opex_eur_fixed)
    p10_fixed, p50_fixed, p90_fixed = np.percentile(opex_eur_fixed, [10, 50, 90])

    print(f"\n=== OPEX bei festem Pumpenanteil {f_fixed * 100:.0f} % =============================")
    print(f"⌀ Mittelwert : {mean_fixed:10,.0f} € /a")
    print(f"P10          : {p10_fixed:10,.0f} € /a")
    print(f"P50 (Median) : {p50_fixed:10,.0f} € /a")
    print(f"P90          : {p90_fixed:10,.0f} € /a")

# ---------------------------------------------------------------------------
#  OPEX bei festen Pumpenanteilen 10 % und 20 % – nur Minimum & Maximum
# ---------------------------------------------------------------------------
for f_fixed in [0.10, 0.20]:
    E_pump_GWh_fixed = Q_GWh * f_fixed
    opex_eur_fixed = E_pump_GWh_fixed * 1_000 * HEAT_PRICE
    min_val = np.min(opex_eur_fixed)
    max_val = np.max(opex_eur_fixed)

    print(f"\n=== OPEX bei festem Pumpenanteil {f_fixed * 100:.0f} % =============================")
    print(f"Minimum : {min_val:10,.0f} € /a")
    print(f"Maximum : {max_val:10,.0f} € /a")