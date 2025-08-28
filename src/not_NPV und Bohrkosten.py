import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#Eingabedaten
# CapEx-Quantile (€)
CAPEX_P10 = 5_124_498.589876813
CAPEX_P50 = 5_621_832.615362095
CAPEX_P90 = 6_112_616.303802238

# Produktion Q (GWh_th / Jahr)
Q_P10 = 77.66
Q_P50 = 88.76
Q_P90 = 100.70

# OPEX im 1. Jahr (€)
OPEX_P10 = 1_842_494.42
OPEX_P50 = 2_493_592.47
OPEX_P90 = 3_218_984.25

PRICE_PER_MWH = 80.0      # €/MWh
OPEX_GROWTH   = 0.02      # +2 % p. a.
YEARS         = 30
N_SIM         = 10_000
RNG_SEED      = 42

# Unsicherer Diskontsatz (Log-Normal-Quantile)
DIS_P10 = 0.0567          # 5,67 %
DIS_P50 = 0.0603          # 6,03 %
DIS_P90 = 0.0640          # 6,40 %

def lognormal_params(p10, p50, p90):
    z10, z90 = -1.2815515655446004, 1.2815515655446004   # Φ⁻¹(0.10), Φ⁻¹(0.90)
    mu    = np.log(p50)
    sigma = (np.log(p90) - np.log(p10)) / (z90 - z10)
    return mu, sigma


# ------ Verteilungsparameter für CapEx, Q, OPEX₁ 
MU_CAPEX,  SIG_CAPEX  = lognormal_params(CAPEX_P10,  CAPEX_P50,  CAPEX_P90)
MU_Q,      SIG_Q      = lognormal_params(Q_P10,      Q_P50,      Q_P90)
MU_OPEX1,  SIG_OPEX1  = lognormal_params(OPEX_P10,   OPEX_P50,   OPEX_P90)

# 1) BASELINE-SIMULATION (Diskontsatz fix = 6 %)
rng = np.random.default_rng(RNG_SEED)
capex_base = rng.lognormal(MU_CAPEX, SIG_CAPEX, N_SIM)
q_base     = rng.lognormal(MU_Q,     SIG_Q,     N_SIM)
opex1_base = rng.lognormal(MU_OPEX1, SIG_OPEX1, N_SIM)

t              = np.arange(1, YEARS + 1)
discount_fix   = 1.0 / (1.0 + 0.06)**t
opex_factor    = (1.0 + OPEX_GROWTH)**(t - 1)

revenue_base   = q_base[:, None] * 1_000 * PRICE_PER_MWH
opex_base_year = opex1_base[:, None] * opex_factor
net_cf_base    = revenue_base - opex_base_year

npv_base = -capex_base + (net_cf_base * discount_fix).sum(axis=1)


# 2) NEUE SIMULATION – UNSICHERER DISKONTSATZ

MU_DIS, SIG_DIS = lognormal_params(DIS_P10, DIS_P50, DIS_P90)

rng2 = np.random.default_rng(RNG_SEED + 1)          # anderer Seed
capex_new = rng2.lognormal(MU_CAPEX, SIG_CAPEX, N_SIM)
q_new     = rng2.lognormal(MU_Q,     SIG_Q,     N_SIM)
opex1_new = rng2.lognormal(MU_OPEX1, SIG_OPEX1, N_SIM)
dis_rate  = rng2.lognormal(MU_DIS,   SIG_DIS,   N_SIM)   # individueller Satz pro Lauf

discount_var = 1.0 / (1.0 + dis_rate[:, None])**t
revenue_new  = q_new[:, None] * 1_000 * PRICE_PER_MWH
opex_new     = opex1_new[:, None] * opex_factor
net_cf_new   = revenue_new - opex_new

npv_new = -capex_new + (net_cf_new * discount_var).sum(axis=1)

#Kennzahlen
def summary_stats(arr):
    return pd.Series({
        "Mean NPV (M€)"  : np.mean(arr)/1e6,
        "Median NPV (M€)": np.median(arr)/1e6,
        "P10 NPV (M€)"   : np.percentile(arr, 10)/1e6,
        "P90 NPV (M€)"   : np.percentile(arr, 90)/1e6,
        "Prob NPV < 0"   : np.mean(arr < 0)
    })

stats_base = summary_stats(npv_base)
stats_new  = summary_stats(npv_new)

print("\n=== Baseline (Diskontsatz 6 %) ===")
print(stats_base.to_string(float_format="%.2f"))

print("\n=== Neue Simulation (unsicherer Diskontsatz) ===")
print(stats_new.to_string(float_format="%.2f"))

#Visualisierung
plt.figure(figsize=(8, 5))
plt.hist(npv_base / 1e6, bins=50, label="Baseline")
median_new = np.median(npv_new) / 1e6
plt.axvline(median_new, color="k", linestyle="dashed",
            label=f"Median NPV (neu): {median_new:.1f} M€")
plt.xlabel("NPV (Million €)")
plt.ylabel("Häufigkeit")
plt.title("NPV-Verteilung – Baseline + Markierung neue Simulation")
plt.legend()
plt.tight_layout()
plt.show()
