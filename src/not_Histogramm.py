import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from massenstrom import m_dot          #  kg/s  – kommt aus massenstrom.py

# ----------------------- Konstanten -----------------------
c_p       = 4186            # J/(kg·K)  – Wasser
b         = -5              # K
gradients = np.linspace(0.028, 0.033, 6)
x         = np.arange(1700, 2201, 1)   # 1700-2200 m (Schritt 100 m)
# ----------------------------------------------------------

def delta_T(x_val, g_val, b_val=b):
    """ΔT(x) = g·x + b"""
    return g_val * x_val + b_val

def Pth_kW(x_val, g_val, m_flow=m_dot, c_p_val=c_p, b_val=b):
    """Thermische Leistung in kW"""
    return m_flow * c_p_val * delta_T(x_val, g_val, b_val) / 1_000

# ---------- Leistungswerte für alle 6 g-Werte sammeln ----------
P_all = np.concatenate([Pth_kW(x, g) for g in gradients])   # Array Länge 54

# ---------- Prozent-Gewichte definieren ------------------------
weights = np.ones_like(P_all) * 100 / P_all.size            # Summe = 100 %

# ---------- Histogramm plotten ---------------------------------
plt.figure()
plt.hist(P_all,
         bins=100,               # Klassenzahl nach Wunsch anpassen
         weights=weights,
         edgecolor="black")
plt.xlabel("Thermische Leistung P (kW)")
plt.ylabel("Häufigkeit (%)")
plt.title("Histogramm von P(x) für g = 0.028 … 0.033 °C/m")
plt.grid(True)
plt.tight_layout()
plt.show()



n_bins = 20                                    # Anzahl Klassen
counts, bin_edges = np.histogram(P_all, bins=n_bins)
percent = counts * 100 / P_all.size            # Summe = 100 %


# DataFrame bauen
df_hist = pd.DataFrame({
    "Bin_min_kW": bin_edges[:-1],
    "Bin_max_kW": bin_edges[1:],
    "Häufigkeit_%": percent.round(2)
})

# 5a) Tabelle in der Konsole
print("\nHistogramm-Prozentverteilung (insg. 100 %):")
print(df_hist.to_string(index=False, float_format="{:8.2f}".format))