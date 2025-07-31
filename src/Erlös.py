# Wärmepreis definieren
HEAT_PRICE = 180  # €/MWh_th

# Gegebene Werte (aus Monte-Carlo-Simulation)
mean_Q = 89.01    # GWh_th/a
Q_p10 = 77.76     # GWh_th/a
Q_p50 = 88.80     # GWh_th/a
Q_p90 = 100.75    # GWh_th/a

# Umrechnung GWh zu MWh (x 1000) und Berechnung Erlöse
mean_revenue = mean_Q * 1_000 * HEAT_PRICE
revenue_p10  = Q_p10  * 1_000 * HEAT_PRICE
revenue_p50  = Q_p50  * 1_000 * HEAT_PRICE
revenue_p90  = Q_p90  * 1_000 * HEAT_PRICE

# Ergebnisse ausgeben
print("=== Erlöse aus Wärmeproduktion ===")
print(f"⌀ Mittelwert : {mean_revenue:,.0f} €/a")
print(f"P10          : {revenue_p10:,.0f} €/a")
print(f"P50 (Median) : {revenue_p50:,.0f} €/a")
print(f"P90          : {revenue_p90:,.0f} €/a")
