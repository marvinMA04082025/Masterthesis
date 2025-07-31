#!/usr/bin/env python3
"""
CAPEX, fixe OPEX und variable OPEX
─ mit festen absoluten Werten für Variable OPEX je Szenario.

→ Export als Excel-Datei in gewünschten Ordner.
"""

from itertools import product
import pandas as pd
import os

# ─────────────────────────── Eingabedaten ────────────────────────────
BOHRKOSTEN     = {"P10": 6_437_353, "P50": 7_038_546, "P90": 7_644_953}
PIPELINEKOSTEN = {"P10":   841_306, "P50": 1_403_443, "P90": 1_960_620}
THERM_POWER_KW = {"P10":     9_849.1, "P50":     11_126.2, "P90":     12_411.4}

SUBVENTION_RATE   = 0.40      # 40 % der Bohrkosten
FIX_OPEX_RATE     = 0.02      # 2 % des CAPEX
FULL_LOAD_HRS     = 8_000     # Volllaststunden pro Jahr

# Feste absolute Werte für variable OPEX je Szenario (€)
VAR_OPEX_ABS = {
    "P10": 1_775_124,
    "P50": 2_380_268,
    "P90": 2_992_288
}

# ────────────────────────── Berechnung ──────────────────────────────
def build_rows():
    rows = []
    for b_pct, p_pct, t_pct in product(
            BOHRKOSTEN, PIPELINEKOSTEN, THERM_POWER_KW):

        b_cost = BOHRKOSTEN[b_pct]
        p_cost = PIPELINEKOSTEN[p_pct]
        sub    = b_cost * SUBVENTION_RATE
        capex  = b_cost + p_cost - sub
        fix_opex = capex * FIX_OPEX_RATE

        # jährliche Wärmeproduktion
        heat_mwh = THERM_POWER_KW[t_pct] * FULL_LOAD_HRS / 1_000

        # fixe absolute Var. OPEX aus Dictionary
        var_opex = VAR_OPEX_ABS[t_pct]

        rows.append({
            "Bohr-Pct": b_pct,
            "Pipe-Pct": p_pct,
            "Therm-Pct": t_pct,
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

# ────────────────────────────── Main ────────────────────────────────
if __name__ == "__main__":
    df = pd.DataFrame(build_rows())

    # Anzeige in Konsole (optional)
    pd.set_option("display.max_rows", None)
    print(df.to_string(index=False))

    # Speicherort definieren
    output_dir = r"C:\Users\Marvin\Desktop\Masterarbeit"
    output_file = os.path.join(output_dir, "output.xlsx")

    # Falls Ordner nicht existiert, anlegen
    os.makedirs(output_dir, exist_ok=True)

    # Excel speichern
    df.to_excel(output_file, index=False)
    print(f"\nExcel-Datei erfolgreich gespeichert unter:\n{output_file}")
