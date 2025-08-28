import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import PercentFormatter

# --- Eingabedaten & Parameter ---
CAPEX_P10 = 5_124_498.589876813
CAPEX_P50 = 5_621_832.615362095
CAPEX_P90 = 6_112_616.303802238
Q_P10, Q_P50, Q_P90 = 77.66, 88.76, 100.70
OPEX_P10, OPEX_P50, OPEX_P90 = 1_842_494.42, 2_493_592.47, 3_218_984.25
PRICE_PER_MWH, OPEX_GROWTH, DISCOUNT_RATE = 80.0, 0.02, 0.06
YEARS, N_SIM, RNG_SEED = 30, 10_000, 42
SUCCESS_PROB = 0.5  # 50 % Erfolgswahrscheinlichkeit

def lognormal_params(p10, p50, p90):
    z10, z90 = -1.2815515655446004, 1.2815515655446004
    mu = np.log(p50)
    sigma = (np.log(p90) - np.log(p10)) / (z90 - z10)
    return mu, sigma

# Lognormal-Parameter
MU_CAPEX, SIG_CAPEX = lognormal_params(CAPEX_P10, CAPEX_P50, CAPEX_P90)
MU_Q, SIG_Q = lognormal_params(Q_P10, Q_P50, Q_P90)
MU_OPEX1, SIG_OPEX1 = lognormal_params(OPEX_P10, OPEX_P50, OPEX_P90)

# Simulation
rng = np.random.default_rng(RNG_SEED)
capex_draw = rng.lognormal(MU_CAPEX, SIG_CAPEX, N_SIM)
q_draw = rng.lognormal(MU_Q, SIG_Q, N_SIM)
opex1_draw = rng.lognormal(MU_OPEX1, SIG_OPEX1, N_SIM)

t = np.arange(1, YEARS + 1)
discount = 1.0 / (1.0 + DISCOUNT_RATE) ** t
opex_fac = (1.0 + OPEX_GROWTH) ** (t - 1)
revenue_y1 = q_draw[:, None] * 1_000 * PRICE_PER_MWH
opex_year = opex1_draw[:, None] * opex_fac
net_cf = revenue_y1 - opex_year
disc_ops = (net_cf * discount).sum(axis=1)
npv_success = -capex_draw + disc_ops  # NPV wenn Bohrung gelingt

# Erfolgsindikator & risked NPV
success = rng.random(N_SIM) < SUCCESS_PROB
npv = np.where(success, npv_success, -capex_draw)

# --- Linienpositionen auf Basis der Erfolgsfälle (unverzerrt) ---
p10_s, p50_s, p90_s = np.percentile(npv_success, [10, 50, 90]) / 1e6

# --- Histogramm ---
weights = np.ones_like(npv) * 100.0 / len(npv)

fig, ax = plt.subplots(figsize=(8, 5))
ax.hist(npv / 1e6, bins=60, color="skyblue", edgecolor="white", weights=weights)
ax.axvline(0, linestyle="dashed", color="black")

# Fixierte Linien an Erfolgs-Quantilen
ax.axvline(p10_s, linestyle="dashed", color="darkblue", label=f"P10 Erfolg ({p10_s:,.1f} M€)")
ax.axvline(p50_s, linestyle="dashed", color="darkblue", label=f"P50 Erfolg ({p50_s:,.1f} M€)")
ax.axvline(p90_s, linestyle="dashed", color="darkblue", label=f"P90 Erfolg ({p90_s:,.1f} M€)")

ax.set_xlabel("NPV (Million €)")
ax.set_ylabel("Häufigkeit (%)")
ax.set_title("Kapitalwert-Verteilung (risked) + Fixierte Erfolgs-Quantile")
ax.yaxis.set_major_formatter(PercentFormatter(xmax=100, decimals=0))
ax.legend()
fig.tight_layout()
plt.show()
