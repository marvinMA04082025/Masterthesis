# Werte für die Wärmeproduktion (GWh_th/a)
P10 = 77.67
P50 = 88.79
P90 = 100.70

# Strompreis in €/MWh
strompreis = 180  # Beispielwert - hier kannst du deinen Preis eintragen

# Prozentsatz-Bereich (1% bis 20%)
percentages = list(range(1, 21))


# Funktion zur Berechnung der Pumpkosten in GWh_el/a
def calc_pump_energy(production, percent):
    return production * (percent / 100)


# Funktion zur Berechnung der Kosten in €
def calc_costs(gwh, price_per_mwh):
    mwh = gwh * 1000
    return mwh * price_per_mwh


# Tabellen-Ausgabe
print("Pumpkosten und Kosten (€) bei Strompreis von {} €/MWh:".format(strompreis))
print("{:<6} {:>12} {:>12} {:>12} {:>15} {:>15} {:>15}".format(
    "%",
    "P10 (GWh)",
    "P50 (GWh)",
    "P90 (GWh)",
    "P10 (€)",
    "P50 (€)",
    "P90 (€)"
))

for pct in percentages:
    pump_p10 = calc_pump_energy(P10, pct)
    pump_p50 = calc_pump_energy(P50, pct)
    pump_p90 = calc_pump_energy(P90, pct)

    cost_p10 = calc_costs(pump_p10, strompreis)
    cost_p50 = calc_costs(pump_p50, strompreis)
    cost_p90 = calc_costs(pump_p90, strompreis)

    print("{:<6} {:>12.4f} {:>12.4f} {:>12.4f} {:>15,.2f} {:>15,.2f} {:>15,.2f}".format(
        pct,
        pump_p10,
        pump_p50,
        pump_p90,
        cost_p10,
        cost_p50,
        cost_p90
    ))
