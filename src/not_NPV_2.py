import numpy as np

def calc_npv(C_inv, Q_year, price_heat, O1, g, F_pump, r, N):

    years       = np.arange(1, N+1)
    discount    = 1.0 / (1 + r)**years
    O_series    = O1 * (1 + g)**(years - 1)             # O&M pro Jahr
    R_series    = Q_year * price_heat                   # Erlös konstant
    cashflows   = R_series - (O_series + F_pump)
    pv_cashflows= np.sum(cashflows * discount)
    npv         = -C_inv + pv_cashflows
    return npv

def main():
    print("=== NPV-Rechner Geothermie ===")
    C_inv      = float(input("Einmalige CAPEX (EUR): "))
    Q_year     = float(input("Jährliche Wärmemenge Q (MWh_th): "))
    price_heat = float(input("Verkaufspreis Wärme (EUR/MWh_th): "))
    O1         = float(input("Betriebskosten Jahr 1 (EUR): "))
    g          = float(input("Wachstumsrate O&M p.a. (z.B. 0.02): "))
    F_pump     = float(input("Jährliche Pumpstrom-Kosten (EUR): "))
    r          = float(input("Diskontsatz r (z.B. 0.06): "))
    N          = int(input("Projektlaufzeit N (Jahre): "))

    npv = calc_npv(C_inv, Q_year, price_heat, O1, g, F_pump, r, N)
    print(f"\nNPV: {npv:,.2f} EUR")

if __name__ == "__main__":
    main()
