from itertools import product

# Eingabedaten
BOHRKOSTEN = {"P10": 6_437_353, "P50": 7_038_546, "P90": 7_644_953}
PIPELINEKOSTEN = {"P10":  841_306, "P50": 1_400_875, "P90": 1_960_620}

SUBVENTION_RATE = 0.40   # 40 % der Bohrkosten
OPEX_RATE       = 0.02   # 2 % der CAPEX

# Berechnung
def berechne_kombinationen(bohr, pipe, sub_rate, opex_rate):
    zeilen = []
    for b_pct, p_pct in product(bohr, pipe):
        b = bohr[b_pct]
        p = pipe[p_pct]
        sub = b * sub_rate
        capex = b + p - sub
        opex  = capex * opex_rate
        zeilen.append({
            "Bohr-Pct": b_pct,
            "Pipe-Pct": p_pct,
            "Bohrkosten €": round(b),
            "Pipelinekosten €": round(p),
            f"Subventionen ({sub_rate:.0%}) €": round(sub),
            "CAPEX €": round(capex),
            f"Fixe OPEX ({opex_rate:.0%}) €": round(opex),
        })
    return zeilen

def main():
    rows = berechne_kombinationen(BOHRKOSTEN, PIPELINEKOSTEN,
                                  SUBVENTION_RATE, OPEX_RATE)

    # 1) Versuche pandas
    try:
        import pandas as pd
        print(pd.DataFrame(rows).to_string(index=False))
        return
    except ImportError:
        pass

    # 2) Versuche tabulate
    try:
        from tabulate import tabulate   # pip install tabulate
        print(tabulate(rows, headers="keys", tablefmt="github"))
        return
    except ImportError:
        pass

    # 3) Plain print als letzte Rückfallebene
    for r in rows:
        print(r)

if __name__ == "__main__":
    main()