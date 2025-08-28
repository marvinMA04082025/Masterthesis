import argparse
from pathlib import Path
import numpy as np
import pandas as pd

#feste Parameter
SUBVENTION_RATE   = 0.40      # 40 % der Bohrkosten
FIX_OPEX_RATE     = 0.02      # 2 % des CAPEX
FULL_LOAD_HRS     = 8_000     # Volllaststunden pro Jahr
HEAT_PRICE_EUR_MWH = 170.0    # Wärmepreis
N_RUNS            = 100_000   # Anzahl Zufallsläufe
OUT_XLSX          = "monte_opex.xlsx"

#Eingabe holen
def get_inputs():
    ap = argparse.ArgumentParser(description="Monte-Carlo-OPEX-Rechner")
    ap.add_argument("--bohr",  type=float, help="Bohrkosten in €")
    ap.add_argument("--pipe",  type=float, help="Pipelinekosten in €")
    ap.add_argument("--power", type=float, help="Thermische Leistung in kW")
    args = ap.parse_args()

    bohr  = args.bohr  or float(input("Bohrkosten (€): ").replace(" ", ""))
    pipe  = args.pipe  or float(input("Pipelinekosten (€): ").replace(" ", ""))
    power = args.power or float(input("Thermische Leistung (kW): ").replace(" ", ""))

    return bohr, pipe, power

#Simulation
def simulate(bohr, pipe, power_kw):
    subvention   = bohr * SUBVENTION_RATE
    capex        = bohr + pipe - subvention
    fix_opex     = capex * FIX_OPEX_RATE
    heat_mwh     = power_kw * FULL_LOAD_HRS / 1_000  # kW → MWh/a

    # Ziehe 100 000 Zufalls-Quoten U[0.10, 0.20]
    var_share = np.random.uniform(0.10, 0.20, N_RUNS)
    var_opex  = heat_mwh * var_share * HEAT_PRICE_EUR_MWH
    total_opex = fix_opex + var_opex

    df = pd.DataFrame({
        "Var_OPEX_Share_%": np.round(var_share * 100, 2),
        "Var_OPEX_€":       np.round(var_opex,  2),
        "Total_OPEX_€":     np.round(total_opex, 2),
    })
    return df, fix_opex

#Hauptprogramm
if __name__ == "__main__":
    bohr, pipe, power = get_inputs()
    df, fix_opex = simulate(bohr, pipe, power)

    # Excel speichern
    out_file = Path(OUT_XLSX).resolve()
    df.to_excel(out_file, index=False)

    # Kennzahlen
    stats = df["Total_OPEX_€"].quantile([0.10, 0.50, 0.90]).to_dict()
    mean  = df["Total_OPEX_€"].mean()

    print("\n─ Ergebnisse ─")
    print(f"Fixe OPEX          : {fix_opex:,.0f} €")
    print(f"Gesamt-OPEX Ø      : {mean:,.0f} €")
    print(f"P10 (10-Perzentil) : {stats[0.10]:,.0f} €")
    print(f"P50 (Median)       : {stats[0.50]:,.0f} €")
    print(f"P90 (90-Perzentil) : {stats[0.90]:,.0f} €")
    print(f"\nAlle {N_RUNS:,} Läufe wurden in '{out_file.name}' gespeichert.")
