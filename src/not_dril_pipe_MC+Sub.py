from __future__ import annotations
import numpy as np
import matplotlib.pyplot as plt


def drilling_cost(depth_m: float | np.ndarray) -> np.ndarray:

    return 2 * (0.131223 * depth_m ** 2 + 2_508.990455 * depth_m + 1_643_364.545458)

def pipeline_cost(length_m: float | np.ndarray) -> np.ndarray:

    return 700.0 * length_m

def mc_total_cost(
    n_samples: int = 100_000,
    depth_range: tuple[float, float] = (1_700, 2_200),
    length_range: tuple[float, float] = (1_000, 3_000),
    subsidy_factor: float = 0.4,
    seed: int = 42,
    plot: bool = True,
):

    rng = np.random.default_rng(seed)

    # Random samples
    depths = rng.uniform(*depth_range, n_samples)
    lengths = rng.uniform(*length_range, n_samples)

    # Cost components
    c_drill = drilling_cost(depths)
    c_pipe = pipeline_cost(lengths)
    subsidy = subsidy_factor * c_drill  # 40% of drilling cost
    c_total = c_drill + c_pipe
    c_net = c_total - subsidy

    # Helper to compute statistics
    def stats(arr):
        mean = arr.mean()
        std = arr.std(ddof=1)
        moe = 1.96 * std / np.sqrt(n_samples)  # 95% CI half‑width
        p10, p50, p90 = np.percentile(arr, [10, 50, 90])
        return dict(mean=mean, moe=moe, p10=p10, median=p50, p90=p90)

    s_drill, s_pipe, s_total, s_subsidy, s_net = map(
        stats, (c_drill, c_pipe, c_total, subsidy, c_net)
    )

    # Pretty print helper
    def pretty(d):
        return (
            f"Ø {d['mean']:,.0f} €  ±{d['moe']:,.0f} €  "
            f"(Median: {d['median']:,.0f} €, 10.–90%: "
            f"{d['p10']:,.0f}–{d['p90']:,.0f} €)"
        )

    print(
        f"{n_samples:,} Simulationen\n"
        f"Bohrkosten     : {pretty(s_drill)}\n"
        f"Pipelinekosten : {pretty(s_pipe)}\n"
        f"Gesamtkosten   : {pretty(s_total)}\n"
        f"Subventionen   : {pretty(s_subsidy)}  # Fix40%\n"
        f"Nettokosten    : {pretty(s_net)}"
    )

    # Plots
    if plot:
        # Histogram – percentage frequencies
        weights = np.full_like(c_net, 100 / len(c_net))
        plt.figure()
        plt.hist(c_net / 1e6, bins=50, weights=weights)
        plt.xlabel("Net costs (Mio. €)")
        plt.ylabel("Frequency (%)")
        plt.title("Net Costs – Monte Carlo (%)")
        plt.tight_layout()
        plt.show()

    return depths, lengths, subsidy, c_net


if __name__ == "__main__":
    mc_total_cost()
