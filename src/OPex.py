# ---------------------------------------------------------------------------
#  PARAMETER
# ---------------------------------------------------------------------------
F_LOWER, F_UPPER = 0.10, 0.20        # Pumpenanteil an der Eigenleistung 10–20 %
HEAT_PRICE = 170                     # [€/MWh_th]  Ø Fernwärme-Arbeitspreis
BINS = 60                            # Histogramm-Auflösung

# ---------------------------------------------------------------------------
#  PUMPENANTEIL SAMPLEN  &  OPEX (= variable Betriebskosten)
# ---------------------------------------------------------------------------
f_samples   = np.random.uniform(F_LOWER, F_UPPER, Q_GWh.size)   # Anteil je Stichprobe
E_pump_GWh  = Q_GWh * f_samples                                 # Pumpenenergie
opex_eur    = E_pump_GWh * 1_000 * HEAT_PRICE                   # €/a   (1 GWh = 1 000 MWh)

# ---------------------------------------------------------------------------
#  STATISTIK  (Mittelwert + P10 / P50 / P90)
# ---------------------------------------------------------------------------
mean, p10, p50, p90 = (
    np.mean(opex_eur),
    *np.percentile(opex_eur, [10, 50, 90])
)

print("=== Variable OPEX – Pumpenkosten ===================================")
print(f"⌀ Mittelwert : {mean:10,.0f} € /a")
print(f"P10          : {p10:10,.0f} € /a")
print(f"P50 (Median) : {p50:10,.0f} € /a")
print(f"P90          : {p90:10,.0f} € /a")

# ---------------------------------------------------------------------------
#  MONTE-CARLO-DIAGRAMM  (Kostenverteilung in %)
# ---------------------------------------------------------------------------
plt.figure(figsize=(7,4))
plt.hist(opex_eur,
         bins=BINS,
         weights=np.ones_like(opex_eur) * 100 / opex_eur.size,
         edgecolor="black")
plt.gca().yaxis.set_major_formatter(PercentFormatter())       # y-Achse in %
plt.xlabel("Jährliche OPEX (Pumpen) [€]")
plt.ylabel("Häufigkeit [%]")
plt.title(f"Monte-Carlo-Verteilung der Pumpen-OPEX "
          f"(f ∼ U({F_LOWER:.2f}–{F_UPPER:.2f}), n = {opex_eur.size:,})")
plt.grid(axis="y", ls=":")
plt.tight_layout()
plt.show()
