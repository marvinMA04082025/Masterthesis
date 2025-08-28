import pandas as pd
import os
from itertools import product

# ---------------------------------
# Szenarien-Eingangsdaten (in €)
# ---------------------------------
bohrkosten_szenarien = {
    "P10": 12_874_705,
    "P50": 14_077_173,
    "P90": 15_289_907
}

pipelinekosten_szenarien = {
    "P10": 841_306,
    "P50": 1_403_443,
    "P90": 1_960_620
}

pumpkosten_szenarien = {
    "P10": 1_635_452,
    "P50": 2_249_649,
    "P90": 2_940_578
}

# Wärme in MWh/a (GWh_th/a × 1 000)
waerme_szenarien = {
    "P10": 77_660,     # 77.66 GWh_th/a
    "P50": 88_760,     # 88.76 GWh_th/a
    "P90": 100_700     # 100.70 GWh_th/a
}

# ---------------------------------
# Gemeinsame Parameter
# ---------------------------------
subventionen_rate = 0.40
lifetime_years   = 30
discount_rate    = 0.06
opex_escalation  = 0.02

# ---------------------------------
# Hilfsfunktionen
# ---------------------------------
def calc_crf(r, n):
    return (r * (1 + r) ** n) / ((1 + r) ** n - 1)

def pv_factor_escalating(g, r, n):
    if g == r:
        return n / (1 + r)
    return ((1 + g) ** n - (1 + r) ** n) / ((g - r) * (1 + r) ** n)

# ---------------------------------
# Szenarien berechnen
# ---------------------------------
results = []

for (bohr_szen,  bohrkosten), \
    (pipe_szen,  pipekosten), \
    (pump_szen,  pumpkosten_year1), \
    (heat_szen,  heat_per_year) in product(
        bohrkosten_szenarien.items(),
        pipelinekosten_szenarien.items(),
        pumpkosten_szenarien.items(),
        waerme_szenarien.items()
):
    # Netto-CAPEX nach Subvention
    subventionen   = subventionen_rate * bohrkosten
    capex_netto    = bohrkosten + pipekosten - subventionen

    # Annuitäten
    crf            = calc_crf(discount_rate, lifetime_years)
    capex_annuity  = capex_netto * crf

    opex_fix_year1 = 0.02 * capex_netto
    pv_factor      = pv_factor_escalating(opex_escalation, discount_rate, lifetime_years)
    pv_opex_total  = (opex_fix_year1 + pumpkosten_year1) * pv_factor
    opex_annuity   = pv_opex_total * crf

    # *** LCOH ***
    lcoh_lifetime = (capex_annuity + opex_annuity) / heat_per_year

    # *** NEU: LCOH im ersten Jahr ***
    opex_total_year1 = opex_fix_year1 + pumpkosten_year1
    lcoh_year1       = (capex_annuity + opex_total_year1) / heat_per_year

    # Ergebnis sammeln
    results.append({
        "Bohrkosten Szenario":     bohr_szen,
        "Pipeline Szenario":       pipe_szen,
        "Pumpkosten Szenario":     pump_szen,
        "Wärme Szenario":          heat_szen,
        "Wärmeproduktion (MWh/a)": heat_per_year,
        "Netto CAPEX (€)":         round(capex_netto, 2),
        "CAPEX-Annuität (€)":      round(capex_annuity, 2),
        "OPEX-Annuität (€)":       round(opex_annuity, 2),
        "LCOH (€/MWh)":            round(lcoh_lifetime, 2),
        "LCOH Jahr 1 (€/MWh)":     round(lcoh_year1, 2)           # << neu
    })

df = pd.DataFrame(results)

# ---------------------------------
# Ergebnis speichern
# ---------------------------------
output_folder = r"C:\Users\Marvin\Desktop\Masterarbeit"
os.makedirs(output_folder, exist_ok=True)

output_path = os.path.join(output_folder, "LCOH_Szenarien_neue Bohrkosten.xlsx")
df.to_excel(output_path, index=False)

print(f"Ergebnisse gespeichert unter:\n{output_path}")
