#!/usr/bin/env python3
"""
Monte-Carlo-Simulation des Kapitalwerts (NPV) für ein 30-jähriges Energie­projekt
Autor: ChatGPT (17 Jul 2025)

• CapEx, Produktion (Q) und OPEX₁ sind als Log-Normal per P10/P50/P90 kalibriert
• 10 000 Zufalls­ziehungen (n_sim) – beliebig anpassbar
• Ergebnis: Histogramm & tabellarische Kennzahlen
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------- Eingabe -----------------------------
# Capital expenditure (CapEx)       – € absolut
CAPEX_P10 = 5_124_498.589876813
CAPEX_P50 = 5_621_832.615362095
CAPEX_P90 = 6_112_616.303802238

# Produktion Q (GWh_th pro Jahr)
Q_P10 = 77.66
Q_P50 = 88.76
Q_P90 = 100.70

# OPEX im 1. Jahr                   – € absolut
OPEX_P10 = 1_842_494.42
OPEX_P50 = 2_493_592.47
OPEX_P90 = 3_218_984.25

# Modellparameter
PRICE_PER_MWH = 80.0    # €/MWh
OPEX_GROWTH   = 0.02     # +2 % p. a.
DISCOUNT_RATE = 0.06     # 6 % p. a.
YEARS         = 30       # Projektlaufzeit
N_SIM         = 10_000   # Anzahl Simulationen
RNG_SEED      = 42       # Reproduzierbarkeit
# ------------------------------------------------------------------

def lognormal_params(p10, p50, p90):
    """gibt μ, σ der zugr. Log-Normal in natural-log-Space zurück"""
    z10, z90 = -1.2815515655446004, 1.2815515655446004  # Φ⁻¹(0.10), Φ⁻¹(0.90)
    mu    = np.log(p50)
    sigma = (np.log(p90) - np.log(p10)) / (z90 - z10)
    return mu, sigma

# Verteilungsparameter kalibrieren
MU_CAPEX,  SIG_CAPEX  = lognormal_params(CAPEX_P10,  CAPEX_P50,  CAPEX_P90)
MU_Q,      SIG_Q      = lognormal_params(Q_P10,      Q_P50,      Q_P90)
MU_OPEX1,  SIG_OPEX1  = lognormal_params(OPEX_P10,   OPEX_P50,   OPEX_P90)

# Zufalls­generator
rng = np.random.default_rng(RNG_SEED)

# Zufalls­ziehungen
capex_draw   = rng.lognormal(MU_CAPEX,  SIG_CAPEX,  N_SIM)  # €
q_draw       = rng.lognormal(MU_Q,      SIG_Q,      N_SIM)  # GWh/a
opex1_draw   = rng.lognormal(MU_OPEX1,  SIG_OPEX1,  N_SIM)  # €

# Zeitreihen-Faktoren
t = np.arange(1, YEARS + 1)
discount = 1.0 / (1.0 + DISCOUNT_RATE) ** t
opex_fac = (1.0 + OPEX_GROWTH) ** (t - 1)

# Jahres-Cashflows
revenue_y1 = q_draw[:, None] * 1_000 * PRICE_PER_MWH          # €/a
opex_year  = opex1_draw[:, None] * opex_fac                   # €/a
net_cf     = revenue_y1 - opex_year                           # €/a

# Abgezinste Operationen & NPV
disc_ops = (net_cf * discount).sum(axis=1)
npv      = -capex_draw + disc_ops                             # €/sim

# ----------------- Kennzahlen -----------------
stats = {
    "Mean NPV (M€)"  : np.mean(npv)        / 1e6,
    "Median NPV (M€)": np.median(npv)      / 1e6,
    "P05 NPV (M€)"   : np.percentile(npv, 5)  / 1e6,
    "P10 NPV (M€)"   : np.percentile(npv, 10) / 1e6,
    "P90 NPV (M€)"   : np.percentile(npv, 90) / 1e6,
    "P95 NPV (M€)"   : np.percentile(npv, 95) / 1e6,
    "Prob NPV < 0"   : np.mean(npv < 0)
}
stats_df = pd.DataFrame(stats, index=["Value"]).T
print("\nMonte-Carlo-Ergebnisse (n = {:,})".format(N_SIM))
print(stats_df)

# ----------------- Histogramm -----------------
plt.figure(figsize=(8, 5))
plt.hist(npv / 1e6, bins=50)
plt.axvline(0, linestyle="dashed")
plt.xlabel("NPV (Million €)")
plt.ylabel("Häufigkeit")
plt.title("Verteilung des Kapitalwerts (Monte-Carlo)")
plt.tight_layout()
plt.show()
