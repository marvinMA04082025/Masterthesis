import numpy as np
import matplotlib.pyplot as plt

# ---------------- Parameter ----------------
CAPEX_P10, CAPEX_P50, CAPEX_P90 = 14_432_000, 15_462_000, 16_529_000   # NEU
Q_P10, Q_P50, Q_P90             = 77.66, 88.76, 100.70
OPEX_P10, OPEX_P50, OPEX_P90    = 1_900_863.42, 2_567_868.47, 3_302_972.25
PRICE_PER_MWH, OPEX_GROWTH      = 80.0, 0.02
DISCOUNT_RATE, YEARS, N_SIM     = 0.06, 30, 10_000
RNG_SEED                        = 42

# -------------- Hilfsfunktion --------------
def lognormal_params(p10, p50, p90):
    z10, z90 = -1.2815515655446004,  1.2815515655446004
    mu    = np.log(p50)
    sigma = (np.log(p90) - np.log(p10)) / (z90 - z10)
    return mu, sigma

# ------------------ Ziehungen ----------------
MU_CAPEX,  SIG_CAPEX  = lognormal_params(CAPEX_P10, CAPEX_P50, CAPEX_P90)
MU_Q,      SIG_Q      = lognormal_params(Q_P10,     Q_P50,     Q_P90)
MU_OPEX1,  SIG_OPEX1  = lognormal_params(OPEX_P10,  OPEX_P50,  OPEX_P90)

rng          = np.random.default_rng(RNG_SEED)
capex_draw   = rng.lognormal(MU_CAPEX,  SIG_CAPEX,  N_SIM)
q_draw       = rng.lognormal(MU_Q,      SIG_Q,      N_SIM)
opex1_draw   = rng.lognormal(MU_OPEX1,  SIG_OPEX1,  N_SIM)

# ------------- Kapitalwert-Modell -------------
t         = np.arange(1, YEARS + 1)
discount  = 1.0 / (1.0 + DISCOUNT_RATE) ** t
opex_fac  = (1.0 + OPEX_GROWTH) ** (t - 1)

revenue_y1 = q_draw[:, None] * 1_000 * PRICE_PER_MWH   # Jahresumsatz Jahr 1
opex_year  = opex1_draw[:, None] * opex_fac            # OPEX-Pfad
net_cf     = revenue_y1 - opex_year                    # Netto-Cash-flow
disc_ops   = (net_cf * discount).sum(axis=1)           # Barwert Opex-/Ertragskette
npv        = -capex_draw + disc_ops                    # Kapitalwert

# ----------------- Visualisierung -----------------
weights = np.full_like(npv, 100.0 / len(npv))          # Prozent-Gewichtung
plt.figure(figsize=(8, 5))
plt.hist(npv / 1e6, bins=50, color="skyblue", edgecolor="white", weights=weights)          # NPV in Mio €
plt.axvline(0, linestyle="dashed")                     # NPV-Break-even-Linie

# Perzentile
p10, p50, p90 = np.percentile(npv, [10, 50, 90]) / 1e6
plt.axvline(p10, linestyle="dashed", label=f"P10 ({p10:.2f} M€)")
plt.axvline(p50, linestyle="dashed", label=f"P50 ({p50:.2f} M€)")
plt.axvline(p90, linestyle="dashed", label=f"P90 ({p90:.2f} M€)")

plt.xlabel("NPV (Million €)")
plt.ylabel("frequency (%)")
plt.title("NPV-Distribution without subsidies")
plt.legend()
plt.tight_layout()
plt.show()
