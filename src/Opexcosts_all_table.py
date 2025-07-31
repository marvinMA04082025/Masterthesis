from itertools import product
import pandas as pd
#  Eingabedaten
BOHRKOSTEN     = {"P10": 6_437_353, "P50": 7_038_546, "P90": 7_644_953}
PIPELINEKOSTEN = {"P10":   841_306, "P50": 1_403_443, "P90": 1_960_620}
THERM_POWER_KW = {"P10":     9_849.1, "P50":     11_126.2, "P90":     12_411.4}

SUBVENTION_RATE   = 0.40      # 40 % der Bohrkosten
FIX_OPEX_RATE     = 0.02      # 2 % des CAPEX
FULL_LOAD_HRS     = 8_000     # Volllaststunden pro Jahr
HEAT_PRICE_EUR_MWH = 170.0    # Wärmepreis

# Variable-OPEX-Quote: 10 % … 20 % in 1 %-Schritten
VAR_OPEX_SHARES = [x / 100 for x in range(10, 21)]   # [0.10, 0.11, …, 0.20]

#Berechnung
def build_rows():
    rows = []
    for b_pct, p_pct, t_pct, var_share in product(
            BOHRKOSTEN, PIPELINEKOSTEN, THERM_POWER_KW, VAR_OPEX_SHARES):

        b_cost = BOHRKOSTEN[b_pct]
        p_cost = PIPELINEKOSTEN[p_pct]
        sub    = b_cost * SUBVENTION_RATE
        capex  = b_cost + p_cost - sub
        fix_opex = capex * FIX_OPEX_RATE

        # jährliche Wärmeproduktion
        heat_mwh = THERM_POWER_KW[t_pct] * FULL_LOAD_HRS / 1_000

        var_opex  = heat_mwh * var_share * HEAT_PRICE_EUR_MWH

        rows.append({
            "Bohr-Pct": b_pct,
            "Pipe-Pct": p_pct,
            "Therm-Pct": t_pct,
            "VarOPEX-Share": f"{var_share:.0%}",
            "Bohrkosten €": round(b_cost),
            "Pipelinekosten €": round(p_cost),
            f"Subvention ({SUBVENTION_RATE:.0%}) €": round(sub),
            "CAPEX €": round(capex),
            f"Fixe OPEX ({FIX_OPEX_RATE:.0%}) €": round(fix_opex),
            "Wärme MWh/a": round(heat_mwh, 1),
            "Var. OPEX €": round(var_opex),
            "Gesamt-OPEX €": round(fix_opex + var_opex),
        })
    return rows

#Main
if __name__ == "__main__":
    df = pd.DataFrame(build_rows())
    # nach Wunsch sortieren oder filtern
    pd.set_option("display.max_rows", None)   # alles anzeigen
    print(df.to_string(index=False))

import os

if __name__ == "__main__":
    df = pd.DataFrame(build_rows())
    # nach Wunsch sortieren oder filtern
    pd.set_option("display.max_rows", None)  # alles anzeigen
    print(df.to_string(index=False))

    # ───────────── Excel-Export ─────────────
    # Ziel-Ordner und Dateiname
    output_dir = r"C:\Users\Marvin\Desktop\Masterarbeit"
    output_filename = "opex_auswertung.xlsx"

    # Ordner erstellen, falls er noch nicht existiert
    os.makedirs(output_dir, exist_ok=True)

    # Vollständigen Pfad erzeugen
    output_path = os.path.join(output_dir, output_filename)

    # DataFrame als Excel speichern
    df.to_excel(output_path, index=False)

    print(f"Datei erfolgreich gespeichert unter:\n{output_path}")
