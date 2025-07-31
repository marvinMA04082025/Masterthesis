import numpy as np
import matplotlib.pyplot as plt
# -----------------------------------------------------------
# Grundeinstellungen
T_surface, T_measured = 10.0, 15.0          # °C
b        = T_surface - T_measured           # −5 K
m_dot    = 55.1786268                       # kg/s
c_p      = 3_700.59                         # J/(kg·K)
n_samples = 100_000
seed       = 42
# Uniform-Intervalle für z und g
depth_min, depth_max = 1700, 2200         # m
grad_min,  grad_max  = 0.028, 0.033         # °C/m
# -----------------------------------------------------------

rng = np.random.default_rng(seed)

# 1) Monte-Carlo für ΔT -------------------------------------
depths    = rng.uniform(depth_min, depth_max, n_samples)
gradients = rng.uniform(grad_min,  grad_max,  n_samples)
delta_T   = gradients * depths + b                        # K

# Statistik ΔT
dT_mean = delta_T.mean()
dT_std  = delta_T.std(ddof=1)
dT_ci   = 1.96 * dT_std / np.sqrt(n_samples)

print(f"ΔT  – Mittel = {dT_mean:.2f} K  ± {dT_ci:.2f} K (95 %-KI)")

# 2) Thermische Leistung – nur noch deterministische Umrechnung
P_th_kW = m_dot * c_p * delta_T / 1_000                   # kW

# Statistik P_th
P_mean = P_th_kW.mean()
P_std  = P_th_kW.std(ddof=1)
P_ci   = 1.96 * P_std / np.sqrt(n_samples)

print(f"P_th – Mittel = {P_mean:.1f} kW ± {P_ci:.1f} kW (95 %-KI)\n")

# -----------------------------------------------------------
# Plots
# -----------------------------------------------------------
## Hexbin ΔT vs. Tiefe
plt.figure(figsize=(8,5))
hb = plt.hexbin(depths, delta_T, gridsize=60, bins="log", cmap="viridis")
plt.colorbar(hb, label="log₁₀(N)")
plt.xlabel("Tiefe z (m)")
plt.ylabel("ΔT (K)")
plt.title("ΔT-Verteilung (Monte Carlo)")
plt.tight_layout()
plt.show()

## Hexbin P_th vs. Tiefe  – gleiche Tiefen, abgeleitete Leistung
plt.figure(figsize=(8,5))
hb2 = plt.hexbin(depths, P_th_kW, gridsize=60, bins="log", cmap="plasma")
plt.colorbar(hb2, label="log₁₀(N)")
plt.xlabel("Tiefe z (m)")
plt.ylabel("P_th (kW)")
plt.title("P_th-Verteilung (abgeleitet aus denselben ΔT-Samples)")
plt.tight_layout()
plt.show()

## Histogramme in %
fig, ax = plt.subplots(1, 2, figsize=(13,4))
weights = np.ones_like(delta_T) / n_samples * 100

ax[0].hist(delta_T, bins=60, weights=weights)
ax[0].axvline(dT_mean, ls="--")
ax[0].fill_betweenx([0, weights.max()],
                    dT_mean-dT_ci, dT_mean+dT_ci, alpha=0.2)
ax[0].set_xlabel("ΔT (K)")
ax[0].set_ylabel("Häufigkeit (%)")
ax[0].set_title("ΔT-Histogramm")

ax[1].hist(P_th_kW, bins=60, weights=weights, color="tab:orange")
ax[1].axvline(P_mean, ls="--", color="k")
ax[1].fill_betweenx([0, weights.max()],
                    P_mean-P_ci, P_mean+P_ci, alpha=0.2,
                    color="tab:orange")
ax[1].set_xlabel("P_th (kW)")
ax[1].set_ylabel("Häufigkeit (%)")
ax[1].set_title("P_th-Histogramm")

fig.suptitle("Ergebnisse einer einzigen MC-Kette")
fig.tight_layout()
plt.show()

# Selbst-Archivierung
if __name__ == "__main__":
    import zipfile
    from pathlib import Path

    ZIP_PATH = Path(r"C:\Users\Marvin\Desktop\Mein_erstes_Projekt_scripts.zip")
    ZIP_PATH.parent.mkdir(parents=True, exist_ok=True)

    this_file = Path(__file__).resolve()

    with zipfile.ZipFile(ZIP_PATH, mode="a", compression=zipfile.ZIP_DEFLATED) as zf:
        if this_file.name not in zf.namelist():  # wenn es schon einmal drin ist, nicht nochmal speichern
            zf.write(this_file, arcname=this_file.name)
            print(f"✔ {this_file.name} wurde zu {ZIP_PATH} hinzugefügt")
        else:
            print(f"ℹ {this_file.name} ist bereits im Archiv – kein erneutes Speichern")