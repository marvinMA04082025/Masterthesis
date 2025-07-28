import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import zipfile
from scipy.stats import norm


def drilling_cost(depth_m: np.ndarray) -> np.ndarray:

    return 2 * (0.131223 * depth_m ** 2 + 2_508.990455 * depth_m + 1_643_364.545458)

def mc_drilling_cost(
        n_samples: int = 100_000,
        depth_min: float = 3_900,
        depth_max: float = 4_000,
        seed: int = 42,
        plot: bool = True,
):
    rng = np.random.default_rng(seed)

    # a) sample depths ~ U(depth_min, depth_max)
    depths = rng.uniform(depth_min, depth_max, n_samples)

    # b) deterministic costs for each depth
    costs = drilling_cost(depths)

    # c) descriptive statistics
    mean = costs.mean()
    std = costs.std(ddof=1)
    ci95 = 1.96 * std / np.sqrt(n_samples)  # 95‑% CI half‑width (margin of error)
    p10, p50, p90 = np.percentile(costs, [10, 50, 90])

    print(f"{n_samples:,} runs")
    print(f"Mean cost      : {mean:,.0f} €  ± {ci95:,.0f} €  (95 % CI)")
    print(f"Median         : {p50:,.0f} €")
    print(f"10th percentile: {p10:,.0f} €")
    print(f"90th percentile: {p90:,.0f} €")

    # d) plots
    if plot:
        # 1. Histogramm der Monte-Carlo-Ergebnisse
        weights = np.ones_like(costs) * 100 / n_samples
        plt.figure()
        plt.hist(
            costs / 1e6,
            bins=50,
            weights=weights,
            edgecolor='black',
            alpha=0.9,
            label="Monte-Carlo histogram"
        )
        plt.xlabel("costs (Mio. €)")
        plt.ylabel("frequency (%)")
        plt.title("Drilling costs with Monte‑Carlo simulation")
        plt.tight_layout()
        plt.show()

        # 2. Normalverteilung als eigene Balken-Abbildung
        plt.figure()

        # Gleiche x-Achse wie Histogramm
        x_vals = np.linspace((mean - 4 * std), (mean + 4 * std), 1000)
        bin_edges = np.linspace((mean - 4 * std), (mean + 4 * std), 51)  # 50 Balken
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
        bin_width = bin_edges[1] - bin_edges[0]

        # Wahrscheinlichkeitsdichte * binbreite * 100 ergibt geschätzte %-Häufigkeit
        pdf_vals = norm.pdf(bin_centers, loc=mean, scale=std)
        frequencies = pdf_vals * bin_width * 100 * n_samples

        plt.bar(bin_centers / 1e6, frequencies / n_samples, width=bin_width / 1e6, color='blue', edgecolor='black',
                alpha=0.8)

        plt.xlabel("costs (Mio. €)")
        plt.ylabel("frequency (%)")
        plt.title("Normal distribution")
        plt.legend()
        plt.tight_layout()
        plt.show()

    return depths, costs


if __name__ == "__main__":
    mc_drilling_cost()