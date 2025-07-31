import matplotlib.pyplot as plt
import numpy as np

# Sicherstellen, dass npv existiert
try:
    _ = npv
except NameError:
    # Minimal neu berechnen (gleiches Setup wie zuvor)
    import numpy as np
    CAPEX_P10 = (9_133_496)
    CAPEX_P50 = (9_833_970)
    CAPEX_P90 = (10_522_100)
    Q_P10, Q_P50, Q_P90 = 77.66, 88.76, 100.70
    OPEX_P10, OPEX_P50, OPEX_P90 = 1_838_090, 2_491_655, 3_215_698
    PRICE_PER_MWH, OPEX_GROWTH, DISCOUNT_RATE = 80.0, 0.02, 0.06
    YEARS, N_SIM, RNG_SEED = 30, 10_000, 42

    def lognormal_params(p10, p50, p90):
        z10, z90 = -1.2815515655446004, 1.2815515655446004
        mu = np.log(p50)
        sigma = (np.log(p90) - np.log(p10)) / (z90 - z10)
        return mu, sigma

    MU_CAPEX, SIG_CAPEX = lognormal_params(CAPEX_P10, CAPEX_P50, CAPEX_P90)
    MU_Q, SIG_Q = lognormal_params(Q_P10, Q_P50, Q_P90)
    MU_OPEX1, SIG_OPEX1 = lognormal_params(OPEX_P10, OPEX_P50, OPEX_P90)

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
    npv = -capex_draw + disc_ops

# ----------------- Histogramm in Prozent -----------------
weights = np.ones_like(npv) * 100.0 / len(npv)  # Jede Beobachtung = 0.01 %

plt.figure(figsize=(8, 5))
plt.hist(npv / 1e6, bins=50, color="skyblue", edgecolor="white", weights=weights)
plt.axvline(0, linestyle="dashed", color="black")

# Linien (Dunkelblau)
plt.axvline(31.35, linestyle="dashed", color="darkblue", label="P10 (31,35 M€)")
plt.axvline(48.75, linestyle="dashed", color="darkblue", label="P50 (48,75 M€)")
plt.axvline(66.28, linestyle="dashed", color="darkblue", label="P90 (66,28 M€)")

plt.xlabel("NPV (Million €)")
plt.ylabel("Häufigkeit (%)")
plt.title("Verteilung des Kapitalwerts (Monte‑Carlo)")
plt.legend()
plt.tight_layout()
plt.show()
