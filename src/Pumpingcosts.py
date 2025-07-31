import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

# --- deine bestehenden Imports -------------------
from Pth        import Pth, c_p, b          # b  = oberflächennahe Start-ΔT [°C]
from massenstrom import m_dot               # m_dot = Massenstrom [kg/s]

# --- Konstanten -----------------------------------
VLS = 8_000                                 # Volllaststunden [h/a]
N_SAMPLES = 100_000                         # Anzahl MC-Stichproben

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
plt.xlabel("Jährliche Wärmeproduktion Q [GWh$_{th}$/a]")
plt.ylabel("Häufigkeit [%]")
plt.title(f"Monte-Carlo-Verteilung von Q  (n = {N_SAMPLES:,})")
plt.grid(axis="y", ls=":")
plt.tight_layout()
plt.show()

# --- Parameter, die du ggf. anpassen möchtest -----------------------------
F_PUMP_MIN = 0.10            # Untere Annahme: 10 % von Q
F_PUMP_MAX = 0.20            # Obere Annahme: 20 % von Q

ELEC_PRICE =  180   # [€/MWh]  – z.B. Ø Industriestrompreis, beliebig ändern
# --------------------------------------------------------------------------

# Q_GWh kommt direkt aus deiner vorigen MC-Simulation  ----------------------
# (siehe Code von davor: Q_GWh = P_W * VLS / 1_000_000_000)

# Pumpenenergie in GWh_th/a
E_pump_low  = Q_GWh * F_PUMP_MIN
E_pump_high = Q_GWh * F_PUMP_MAX

# Wahlweise Jahreskosten in € (je Szenario)
cost_low  = E_pump_low  * 1_000  * ELEC_PRICE   # 1 GWh = 1 000 MWh
cost_high = E_pump_high * 1_000  * ELEC_PRICE

# ----------------------------- Auswertung ---------------------------------
import numpy as np

def stats(arr):
    """liefert Mittelwert + P10/P50/P90 als Tupel"""
    mean = np.mean(arr)
    p10, p50, p90 = np.percentile(arr, [10, 50, 90])
    return mean, p10, p50, p90

meanE_lo, p10E_lo, p50E_lo, p90E_lo = stats(E_pump_low)
meanE_hi, p10E_hi, p50E_hi, p90E_hi = stats(E_pump_high)

meanC_lo, p10C_lo, p50C_lo, p90C_lo = stats(cost_low)
meanC_hi, p10C_hi, p50C_hi, p90C_hi = stats(cost_high)

print("=== Pumpenenergiebedarf =====================================")
print(f"10 %-Szenario  ⌀ {meanE_lo:6.2f} GWh  |  P10 {p10E_lo:6.2f}  "
      f"P50 {p50E_lo:6.2f}  P90 {p90E_lo:6.2f}")
print(f"20 %-Szenario  ⌀ {meanE_hi:6.2f} GWh  |  P10 {p10E_hi:6.2f}  "
      f"P50 {p50E_hi:6.2f}  P90 {p90E_hi:6.2f}")

print("\n=== Jährliche Pumpenstromkosten (Preis = "
      f"{ELEC_PRICE} €/MWh) ===============================")
print(f"10 %-Szenario  ⌀ {meanC_lo:10,.0f} €  |  P10 {p10C_lo:10,.0f}  "
      f"P50 {p50C_lo:10,.0f}  P90 {p90C_lo:10,.0f}")
print(f"20 %-Szenario  ⌀ {meanC_hi:10,.0f} €  |  P10 {p10C_hi:10,.0f}  "
      f"P50 {p50C_hi:10,.0f}  P90 {p90C_hi:10,.0f}")


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

# ---------------------------------------------------------------------------
#  PARAMETER
# ---------------------------------------------------------------------------
F_LOWER, F_UPPER = 0.10, 0.20        # Pumpenanteil an Eigenleistung 10–20 %
HEAT_PRICE = 170                     # [€/MWh_th]  Fernwärme-Arbeitspreis
BINS = 60                            # Histogramm-Auflösung

# ---------------------------------------------------------------------------
#  PUMPENANTEIL SAMPLEN  &  KOSTEN BERECHNEN
# ---------------------------------------------------------------------------
f_samples   = np.random.uniform(F_LOWER, F_UPPER, Q_GWh.size)   # Anteil je Case
E_pump_GWh  = Q_GWh * f_samples                                 # Energiebedarf
cost_heat   = E_pump_GWh * 1_000 * HEAT_PRICE                   # €/a (1 GWh = 1 000 MWh)

# ---------------------------------------------------------------------------
#  STATISTIK
# ---------------------------------------------------------------------------
mean   = np.mean(cost_heat)
p10, p50, p90 = np.percentile(cost_heat, [10, 50, 90])
print(f"=== Pumpenkosten basierend auf Wärmepreis =============================")
print(f"⌀ Mittelwert : {mean:10,.0f} € /a")
print(f"P10          : {p10:10,.0f} € /a")
print(f"P50 (Median) : {p50:10,.0f} € /a")
print(f"P90          : {p90:10,.0f} € /a")

# ---------------------------------------------------------------------------
#  MONTE-CARLO-DIAGRAMM
# ---------------------------------------------------------------------------
plt.figure(figsize=(7,4))
plt.hist(cost_heat,
         bins=BINS,
         weights=np.ones_like(cost_heat) * 100 / cost_heat.size,
         edgecolor="black")
plt.gca().yaxis.set_major_formatter(PercentFormatter())  # y-Achse in %
plt.xlabel("Jährliche Pumpenkosten [€] (Basis: Wärmepreis)")
plt.ylabel("Häufigkeit [%]")
plt.title(f"Monte-Carlo-Verteilung Pumpenkosten "
          f"(f ∼ U({F_LOWER:.2f} … {F_UPPER:.2f}), n = {cost_heat.size:,})")
plt.grid(axis="y", ls=":")
plt.tight_layout()
plt.show()
