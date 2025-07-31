import numpy as np
import matplotlib.pyplot as plt

def pipeline_cost(length_m):
    """length_m – Skalar oder ndarray in Metern"""
    return 700.0 * length_m


def mc_pipeline_cost(
    n_samples=100_000,
    L_min=1_000,          # 1 km
    L_max=3_000,          # 3 km
    seed=42,
    plot=True,
):
    rng = np.random.default_rng(seed)

    # a) Zufällige Längen ~ U(L_min, L_max)
    lengths = rng.uniform(L_min, L_max, n_samples)

    # b) Kosten berechnen
    costs = pipeline_cost(lengths)

    # c) Kennzahlen
    mean = costs.mean()
    std = costs.std(ddof=1)
    ci95 = 1.96 * std / np.sqrt(n_samples)
    p10, p50, p90 = np.percentile(costs, [10, 50, 90])

    print(f"{n_samples:,} Durchläufe")
    print(f"Ø Kosten      : {mean:,.0f} €  ± {ci95:,.0f} €  (95 %-KI)")
    print(f"Median        : {p50:,.0f} €")
    print(f"10. Perzentil : {p10:,.0f} €")
    print(f"90. Perzentil : {p90:,.0f} €")

    # d) Histogramm
    if plot:
        plt.figure()
        plt.hist(costs / 1e6, bins=40)
        plt.xlabel("Kosten (Mio. €)")
        plt.ylabel("Häufigkeit")
        plt.title("Verteilung der Pipelinekosten"
                  f"  –  Monte Carlo, {n_samples:,} Läufe")
        plt.tight_layout()
        plt.show()

    return lengths, costs

if __name__ == "__main__":
    mc_pipeline_cost()


# Selbst-Archivierung
if __name__ == "__main__":
    import zipfile
    from pathlib import Path

    ZIP_PATH = Path(r"C:\Users\Marvin\Desktop\Mein_erstes_Projekt_scripts.zip")
    ZIP_PATH.parent.mkdir(parents=True, exist_ok=True)

    this_file = Path(__file__).resolve()

    with zipfile.ZipFile(ZIP_PATH, mode="a", compression=zipfile.ZIP_DEFLATED) as zf:
        if this_file.name not in zf.namelist():  # wenn es schon einmal drin ist, nicht nochmal speichern
            zf.write(this_file, arcname=this_file.name)
            print(f"✔ {this_file.name} wurde zu {ZIP_PATH} hinzugefügt")
        else:
            print(f"ℹ {this_file.name} ist bereits im Archiv – kein erneutes Speichern")