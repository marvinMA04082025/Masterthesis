import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

# Pth-Funktion importieren
from Pth import Pth
from massenstrom import m_dot
from Pth import c_p
from Pth import b

# Parameter
VLS = 8000                                   # Volllaststunden [h/a]
x_range = np.arange(1700, 2201, 1)           # Tiefe 1700-2200 m
g_vals  = np.linspace(0.028, 0.033, 6)       # °C/m


def annual_heat_MWh(power_W):
    return power_W / 1_000_000 * VLS         # MW → MWh

k = m_dot * c_p * VLS / 1_000_000_000               # 1 GWh = 3,6·10^12 J

#Plot
plt.figure()
for g in g_vals:
    # Punktweise Leistung & Jahreswärme
    P_W   = Pth(x_range, g, m_dot=m_dot, c_p=c_p, b=b)
    Q_GWh = annual_heat_MWh(P_W) / 1000            # → GWh_th

    # Geradengleichungs-Parameter
    m = k * g
    n = k * b
    label = f"g={g:.3f} → Q = {m:.3f}·x {n:+.3f}"

    # Plot
    plt.plot(x_range, Q_GWh, label=label)

plt.xlabel("Tiefe x [m]")
plt.ylabel("Jährliche Wärmeproduktion Q [GWh_th/a]")
plt.title("Jährliche Wärmeproduktion entlang der Tiefe (VLS = 8000 h)")
plt.grid(True)
plt.legend(title="Temperaturgradient")
plt.tight_layout()
plt.show()

Q_all = []
for g in g_vals:
    P_W   = Pth(x_range, g, m_dot=m_dot, c_p=c_p, b=b)
    Q_GWh = annual_heat_MWh(P_W) / 1_000    # → GWh_th
    Q_all.append(Q_GWh)

Q_flat = np.concatenate(Q_all)

plt.figure(figsize=(6, 4))

# density=True skaliert die Fläche auf 1 →multiplizieren mit 100
plt.hist(Q_flat,
         bins=40,
         weights=np.ones_like(Q_flat) * 100 / Q_flat.size,
         edgecolor="black")

plt.gca().yaxis.set_major_formatter(PercentFormatter())  # Achse in %
plt.xlabel("Jährliche Wärmeproduktion Q [GWh$_{th}$/a]")
plt.ylabel("Häufigkeit [%]")
plt.title("Histogramm aller Q(x) – relative Häufigkeit")
plt.grid(axis="y", ls=":")
plt.tight_layout()
plt.show()


plt.figure(figsize=(6, 4))
colors = plt.cm.viridis(np.linspace(0, 1, len(g_vals)))

for g, Q, col in zip(g_vals, Q_all, colors):
    plt.hist(Q,
             bins=40,
             weights=np.ones_like(Q) * 100 / Q.size,
             alpha=0.5,
             edgecolor="black",
             color=col,
             label=f"g={g:.3f}")

plt.gca().yaxis.set_major_formatter(PercentFormatter())
plt.xlabel("Jährliche Wärmeproduktion Q [GWh$_{th}$/a]")
plt.ylabel("Häufigkeit [%]")
plt.title("Histogramme der Q(x) nach Temperaturgradient g (relativ)")
plt.legend(title="g [°C/m]")
plt.grid(axis="y", ls=":")
plt.tight_layout()
plt.show()