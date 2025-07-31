import numpy as np
import matplotlib.pyplot as plt

CAPEX_P10 = 9_143_985
CAPEX_P50 = 9_845_536
CAPEX_P90 = 10_540_442

Q_P10, Q_P50, Q_P90 = 77.66, 88.76, 100.70  # GWh pro Jahr
OPEX_P10, OPEX_P50, OPEX_P90 = 1_900_863, 2_567_868, 3_302_972  # EUR

# Feste Parameter

PRICE_PER_MWH = 80       # EUR
OPEX_GROWTH = 0.02         # 2% p.a.
DISCOUNT_RATE = 0.06    # 6% p.a.
YEARS = 30
N_SIM = 10_000
RNG_SEED = 42

MAINT_PCT = 0.02          # 2%

# Hilfsfunktion: Lognormal‑Parameter aus P10/P50/P90
def lognormal_params(p10, p50, p90):
    z10, z90 = -1.2815515655446004, 1.2815515655446004  # z‑Werte StdNormal
    mu = np.log(p50)
    sigma = (np.log(p90) - np.log(p10)) / (z90 - z10)
    return mu, sigma

# Verteilungsparameter
MU_CAPEX, SIG_CAPEX = lognormal_params(CAPEX_P10, CAPEX_P50, CAPEX_P90)
MU_Q, SIG_Q = lognormal_params(Q_P10, Q_P50, Q_P90)
MU_OPEX1, SIG_OPEX1 = lognormal_params(OPEX_P10, OPEX_P50, OPEX_P90)

# Monte‑Carlo‑Zufallsziehungen
rng = np.random.default_rng(RNG_SEED)
capex_draw = rng.lognormal(MU_CAPEX, SIG_CAPEX, N_SIM)  # EUR
q_draw = rng.lognormal(MU_Q, SIG_Q, N_SIM)              # GWh
opex1_draw = rng.lognormal(MU_OPEX1, SIG_OPEX1, N_SIM)  # EUR

# Zeitachsen & Abzinsungsfaktoren
t = np.arange(1, YEARS + 1)
discount = 1.0 / (1.0 + DISCOUNT_RATE) ** t
opex_fac = (1.0 + OPEX_GROWTH) ** (t - 1)

# OPEX: Basis + Eskalation (inkl. 2% CAPEX‑Anteil)
opex_base = opex1_draw + MAINT_PCT * capex_draw          # (N_SIM,)
opex_year = opex_base[:, None] * opex_fac                # (N_SIM, YEARS)

# Erlöse & Netto‑Cashflows
revenue_y = q_draw[:, None] * 1_000 * PRICE_PER_MWH      # 1GWh = 1000MWh
net_cf = revenue_y - opex_year

disc_ops = (net_cf * discount).sum(axis=1)              # abgezinste operat. CF

# Kapitalwert (NPV)
npv = -capex_draw + disc_ops

# Perzentile
p10, p50, p90 = np.percentile(npv, [10, 50, 90]) / 1e6  # Mio. EUR


# Histogramm
weights = np.ones_like(npv) * 100.0 / len(npv)

plt.figure(figsize=(8, 5))
plt.hist(npv / 1e6, bins=50, color="skyblue", edgecolor="white", weights=weights)
plt.axvline(0, linestyle="dashed", color="black")
plt.axvline(p10, linestyle="dashed", color="darkblue", label=f"P10 ({p10:,.2f}M€)")
plt.axvline(p50, linestyle="dashed", color="darkblue", label=f"P50 ({p50:,.2f}M€)")
plt.axvline(p90, linestyle="dashed", color="darkblue", label=f"P90 ({p90:,.2f}M€)")
plt.xlabel("NPV (Million €)")
plt.ylabel("frequency (%)")
plt.title("NPV -Distribution")
plt.legend()
plt.tight_layout()
plt.show()
