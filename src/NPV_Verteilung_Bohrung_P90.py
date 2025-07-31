import matplotlib.pyplot as plt
import numpy as np

# Neue CAPEX-Quantile (Euro)
CAPEX_P10 = 10_160_000.0   # 5,58 Mio €
CAPEX_P50 = 10_570_000.0   # 5,99 Mio €
CAPEX_P90 = 10_980_000.0   # 6,40 Mio €

# Unverändert – andere Randbedingungen
Q_P10, Q_P50, Q_P90 = 77.66, 88.76, 100.70
OPEX_P10, OPEX_P50, OPEX_P90 = 1_842_494.42, 2_493_592.47, 3_218_984.25
PRICE_PER_MWH, OPEX_GROWTH, DISCOUNT_RATE = 80.0, 0.02, 0.06
YEARS, N_SIM, RNG_SEED = 30, 10_000, 42

def lognormal_params(p10, p50, p90):
    z10, z90 = -1.2815515655446004, 1.2815515655446004
    mu = np.log(p50)
    sigma = (np.log(p90) - np.log(p10)) / (z90 - z10)
    return mu, sigma

# Parameter der Lognormal‑Verteilungen
MU_CAPEX, SIG_CAPEX = lognormal_params(CAPEX_P10, CAPEX_P50, CAPEX_P90)
MU_Q, SIG_Q = lognormal_params(Q_P10, Q_P50, Q_P90)
MU_OPEX1, SIG_OPEX1 = lognormal_params(OPEX_P10, OPEX_P50, OPEX_P90)

# Zufallsziehungen
rng = np.random.default_rng(RNG_SEED)
capex_draw = rng.lognormal(MU_CAPEX, SIG_CAPEX, N_SIM)
q_draw = rng.lognormal(MU_Q, SIG_Q, N_SIM)
opex1_draw = rng.lognormal(MU_OPEX1, SIG_OPEX1, N_SIM)

# Kapitalwert‑Simulation
t = np.arange(1, YEARS + 1)
discount = 1.0 / (1.0 + DISCOUNT_RATE) ** t
opex_fac = (1.0 + OPEX_GROWTH) ** (t - 1)

revenue_y1 = q_draw[:, None] * 1_000 * PRICE_PER_MWH
opex_year = opex1_draw[:, None] * opex_fac
net_cf = revenue_y1 - opex_year
disc_ops = (net_cf * discount).sum(axis=1)
npv = -capex_draw + disc_ops

# Empirische Quantile
p10_val, p50_val, p90_val = np.percentile(npv, [10, 50, 90]) / 1e6  # in Mio €

# Histogramm
weights = np.ones_like(npv) * 100.0 / len(npv)

plt.figure(figsize=(8, 5))
plt.hist(npv / 1e6, bins=50, edgecolor="white", weights=weights)
plt.axvline(0, linestyle="dashed", color="black")

# Quantil‑Linien
plt.axvline(p10_val, linestyle="dashed", color="darkblue", label=f"P10 ({p10_val:0.2f} M€)")
plt.axvline(p50_val, linestyle="dashed", color="darkblue", label=f"P50 ({p50_val:0.2f} M€)")
plt.axvline(p90_val, linestyle="dashed", color="darkblue", label=f"P90 ({p90_val:0.2f} M€)")

plt.xlabel("NPV (Million €)")
plt.ylabel("Frequency (%)")
plt.title("Distrbution of the Net Present Value (Monte‑Carlo)")
plt.legend()
plt.tight_layout()
plt.show()
