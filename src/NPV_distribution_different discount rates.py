import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Gegebene P10/P50/P90-Werte
CAPEX_P10 = 9_143_985
CAPEX_P50 = 9_845_536
CAPEX_P90 = 10_540_442

Q_P10, Q_P50, Q_P90 = 77.66, 88.76, 100.70  # GWh pro Jahr
OPEX_P10, OPEX_P50, OPEX_P90 = 1_900_863, 2_567_868, 3_302_972  # EUR

# Feste Parameter
PRICE_PER_MWH = 80  # EUR
OPEX_GROWTH = 0.02  # 2% p.a.
YEARS = 30
N_SIM = 10_000
RNG_SEED = 42
MAINT_PCT = 0.02  # 2% Wartungskosten als Anteil an CAPEX


# Hilfsfunktion: Lognormal‑Parameter berechnen
def lognormal_params(p10, p50, p90):
    z10, z90 = -1.2815515655446004, 1.2815515655446004
    mu = np.log(p50)
    sigma = (np.log(p90) - np.log(p10)) / (z90 - z10)
    return mu, sigma


# Verteilungsparameter berechnen
MU_CAPEX, SIG_CAPEX = lognormal_params(CAPEX_P10, CAPEX_P50, CAPEX_P90)
MU_Q, SIG_Q = lognormal_params(Q_P10, Q_P50, Q_P90)
MU_OPEX1, SIG_OPEX1 = lognormal_params(OPEX_P10, OPEX_P50, OPEX_P90)

# Zufallsziehungen
rng = np.random.default_rng(RNG_SEED)
capex_draw = rng.lognormal(MU_CAPEX, SIG_CAPEX, N_SIM)
q_draw = rng.lognormal(MU_Q, SIG_Q, N_SIM)
opex1_draw = rng.lognormal(MU_OPEX1, SIG_OPEX1, N_SIM)

# Zeitachse
t = np.arange(1, YEARS + 1)
opex_fac = (1.0 + OPEX_GROWTH) ** (t - 1)

# OPEX mit Eskalation
opex_base = opex1_draw + MAINT_PCT * capex_draw
opex_year = opex_base[:, None] * opex_fac
revenue_y = q_draw[:, None] * 1_000 * PRICE_PER_MWH
net_cf = revenue_y - opex_year

# Discount-Rate Variation
discount_rates = np.linspace(0.05, 0.10, 6)  # 5%, 6%, ..., 10%

# Alternative Umsetzung: KDE manuell berechnen und korrekt in Prozent umrechnen (ohne seaborn.get_lines())

from scipy.stats import gaussian_kde

plt.figure(figsize=(10, 6))
colors = plt.cm.viridis(np.linspace(0, 1, len(discount_rates)))

x_vals = np.linspace(-20, 100, 1000)  # X-Achse in Millionen EUR

for idx, (rate, color) in enumerate(zip(discount_rates, colors)):
    discount = 1.0 / (1.0 + rate) ** t
    disc_ops = (net_cf * discount).sum(axis=1)
    npv = -capex_draw + disc_ops
    npv_mio = npv / 1e6

    kde = gaussian_kde(npv_mio)
    density = kde(x_vals) * 100  # Umrechnung in Prozent

    plt.plot(x_vals, density, label=f"{rate*100:.0f}%", color=color, linewidth=2)

    # P50-Linie
    p50 = np.percentile(npv_mio, 50)
    plt.axvline(p50, color=color, linestyle="dotted", linewidth=1)

plt.axvline(0, linestyle="dashed", color="black", label="Break-Even")
plt.xlabel("NPV (Million €)")
plt.ylabel("density (%)")
plt.title("NPV-Distribution with different discount rates")
plt.legend(title="discount rate")
plt.tight_layout()
plt.show()


