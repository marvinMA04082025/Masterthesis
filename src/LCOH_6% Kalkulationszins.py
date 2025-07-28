import pandas as pd
import os

# Szenarien-Werte (in €)
bohrkosten_szenarien = {
    "P10": 9_143_985,
    "P50": 9_845_536,
    "P90": 10_540_442
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

# Gemeinsame Parameter
subventionen_rate = 0.40
heat_per_year = 50_000  # MWh/Jahr
lifetime_years = 30
discount_rate = 0.06
opex_escalation = 0.02

# Ergebnisliste
results = []


# Kapitalwiedergewinnungsfaktor (CRF) berechnen
def calc_crf(r, n):
    return (r * (1 + r) ** n) / ((1 + r) ** n - 1)


# Barwertfaktor für eine wachsende Rente
def pv_factor_escalating(g, r, n):
    if g == r:
        return n / (1 + r)
    else:
        return ((1 + g) ** n - (1 + r) ** n) / ((g - r) * (1 + r) ** n)


# Alle Szenario-Kombinationen durchrechnen
for bohr_scenario, bohrkosten in bohrkosten_szenarien.items():
    for pipeline_scenario, pipelinekosten in pipelinekosten_szenarien.items():
        for pump_scenario, pumpkosten_year1 in pumpkosten_szenarien.items():
            # Subventionen berechnen
            subventionen = subventionen_rate * bohrkosten
            capex_netto = (bohrkosten + pipelinekosten) - subventionen

            # CRF berechnen
            crf = calc_crf(discount_rate, lifetime_years)

            # CAPEX-Annuität
            capex_annuity = capex_netto * crf

            # OPEX fix (Jahr 1)
            opex_fix_year1 = 0.02 * capex_netto

            # Barwertfaktor für wachsende OPEX
            pv_factor = pv_factor_escalating(opex_escalation, discount_rate, lifetime_years)

            # Barwert der OPEX
            pv_opex_fix = opex_fix_year1 * pv_factor
            pv_opex_var = pumpkosten_year1 * pv_factor
            pv_opex_total = pv_opex_fix + pv_opex_var

            # Annuität der OPEX
            opex_annuity = pv_opex_total * crf

            # LCOH
            lcoh = (capex_annuity + opex_annuity) / heat_per_year

            # Ergebnisse speichern
            results.append({
                "Bohrkosten Szenario": bohr_scenario,
                "Pipelinekosten Szenario": pipeline_scenario,
                "Pumpkosten Szenario": pump_scenario,
                "Netto CAPEX (€)": round(capex_netto, 2),
                "CAPEX-Annuität (€)": round(capex_annuity, 2),
                "OPEX-Annuität (€)": round(opex_annuity, 2),
                "LCOH (€/MWh)": round(lcoh, 2)
            })

# Ergebnisse in ein DataFrame umwandeln
df = pd.DataFrame(results)

# Speicherort festlegen
output_folder = r"C:\Users\Marvin\Desktop\Masterarbeit"
os.makedirs(output_folder, exist_ok=True)  # Ordner anlegen, falls noch nicht vorhanden

output_filename = "LCOH_Szenarien.xlsx"
output_path = os.path.join(output_folder, output_filename)

# Excel-Datei speichern
df.to_excel(output_path, index=False)

print(f"Ergebnisse wurden erfolgreich gespeichert unter:\n{output_path}")
