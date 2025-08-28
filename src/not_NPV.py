from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Tuple, Sequence

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

__all__ = [
    "capex",
    "kwf",
    "lcoh_point",
    "lcoh_grid",
    "plot_contour",
]


# Basiskonstanten – können in Funktionsaufrufen überschrieben werden
DEPTH_RANGE_DEFAULT: Tuple[int, int, int] = (1000, 2000, 20)  # min, max, step (m)
LENGTH_RANGE_DEFAULT: Tuple[int, int, int] = (1000, 3000, 20)  # min, max, step (m)
PUMP_SHARES_DEFAULT: np.ndarray = np.arange(0.10, 0.21, 0.01)  # 10 … 20 %

INTEREST_DEFAULT: float = 0.06       # 6 %
LIFETIME_DEFAULT: int = 30           # Jahre
Q_HEAT_DEFAULT: float = 8_168        # MWh_th/a (reichend für 1 MW_th Dauerbetrieb)
PRICE_EL_DEFAULT: float = 183.1      # €/MWh_el (BDEW-Strompreisanalyse 05/2025)

# Einfache Formeln
def capex(depth_m: float, length_m: float) -> float:

    return 0.131223 * depth_m ** 2 + 2_508.990455 * depth_m + 1_643_364.545458 + 700 * length_m


def kwf(rate: float, years: int) -> float:

    if rate == 0:
        return 1 / years
    r_pow = (1 + rate) ** years
    return rate * r_pow / (r_pow - 1)

# Kernfunktionen
def lcoh_point(
    depth_m: float,
    length_m: float,
    pump_share: float,
    *,
    q_heat: float = Q_HEAT_DEFAULT,
    price_el: float = PRICE_EL_DEFAULT,
    interest: float = INTEREST_DEFAULT,
    lifetime: int = LIFETIME_DEFAULT,
) -> float:

    C = capex(depth_m, length_m)
    pump_energy = pump_share * q_heat  # MWh_el/a
    pump_cost = pump_energy * price_el
    ann_C = kwf(interest, lifetime) * C
    return (ann_C + pump_cost) / q_heat


def lcoh_grid(
    depth_range: Tuple[int, int, int] = DEPTH_RANGE_DEFAULT,
    length_range: Tuple[int, int, int] = LENGTH_RANGE_DEFAULT,
    pump_shares: Sequence[float] = PUMP_SHARES_DEFAULT,
    *,
    q_heat: float = Q_HEAT_DEFAULT,
    price_el: float = PRICE_EL_DEFAULT,
    interest: float = INTEREST_DEFAULT,
    lifetime: int = LIFETIME_DEFAULT,
) -> pd.DataFrame:

    depths = np.arange(*depth_range)
    lengths = np.arange(*length_range)

    kwf_val = kwf(interest, lifetime)

    records = []
    for share in pump_shares:
        pump_energy = share * q_heat
        pump_cost = pump_energy * price_el

        for D in depths:
            for L in lengths:
                C = capex(D, L)
                ann_C = kwf_val * C
                lcoh_val = (ann_C + pump_cost) / q_heat

                records.append({
                    "Depth_m": D,
                    "Length_m": L,
                    "Pump_share_%": round(share * 100, 1),
                    "CAPEX_€": round(C),
                    "Pump_cost_€": round(pump_cost),
                    "Annualised_CAPEX_€": round(ann_C),
                    "LCOH_€/MWh": round(lcoh_val, 2),
                })

    return pd.DataFrame(records)



# plot


def plot_contour(
    df: pd.DataFrame,
    pump_share_percent: float,
    *,
    ax: plt.Axes | None = None,
    cmap_levels: int = 20,
    title_prefix: str | None = None,
):

    df_sel = df[df["Pump_share_%"] == pump_share_percent]
    if df_sel.empty:
        raise ValueError(f"Pump_share_% {pump_share_percent} ist im DataFrame nicht vorhanden.")

    pivot = df_sel.pivot(index="Depth_m", columns="Length_m", values="LCOH_€/MWh")
    depths = pivot.index.values
    lengths = pivot.columns.values
    lcoh_vals = pivot.values

    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 6))
    cs = ax.contourf(lengths, depths, lcoh_vals, levels=cmap_levels)
    cbar = plt.colorbar(cs, ax=ax, label="LCOH (€/MWh_th)")
    ax.set_xlabel("Pipeline Length L (m)")
    ax.set_ylabel("Drilling Depth D (m)")
    title = title_prefix + "\n" if title_prefix else ""
    title += f"LCOH Contour (s = {pump_share_percent:.0f} %, {LIFETIME_DEFAULT} a, {INTEREST_DEFAULT*100:.0f} % Zins)"
    ax.set_title(title)
    plt.tight_layout()
    return ax



# CLI – generiert CSV (und optional PNG‑plot)


def _cli():
    parser = argparse.ArgumentParser(description="Generate LCOH grid and export to CSV (and optionally PNG contour plot).")
    parser.add_argument("--csv", type=Path, default=Path("lcoh_grid.csv"), help="Pfad zur CSV‑Ausgabedatei")
    parser.add_argument("--png", type=Path, default=None, help="Wenn gesetzt, speichere einen Beispiel‑Plot (s=10 %).")
    parser.add_argument("--depth", nargs=3, type=int, metavar=("MIN", "MAX", "STEP"), default=DEPTH_RANGE_DEFAULT, help="Depth range: min max step")
    parser.add_argument("--length", nargs=3, type=int, metavar=("MIN", "MAX", "STEP"), default=LENGTH_RANGE_DEFAULT, help="Length range: min max step")
    parser.add_argument("--interest", type=float, default=INTEREST_DEFAULT, help="Diskontierungszins (dezimal)")
    parser.add_argument("--lifetime", type=int, default=LIFETIME_DEFAULT, help="Anlagenlebensdauer (Jahre)")
    parser.add_argument("--qheat", type=float, default=Q_HEAT_DEFAULT, help="Jährliche Wärmeproduktion (MWh_th/a)")
    parser.add_argument("--price_el", type=float, default=PRICE_EL_DEFAULT, help="Strompreis (€/MWh_el)")
    args = parser.parse_args()

    df = lcoh_grid(
        depth_range=tuple(args.depth),
        length_range=tuple(args.length),
        pump_shares=PUMP_SHARES_DEFAULT,
        q_heat=args.qheat,
        price_el=args.price_el,
        interest=args.interest,
        lifetime=args.lifetime,
    )

    args.csv.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.csv, index=False)
    print(f"CSV gespeichert unter: {args.csv.resolve()}")

    if args.png:
        fig, ax = plt.subplots(figsize=(8, 6))
        plot_contour(df, pump_share_percent=10.0, ax=ax, title_prefix="Auto‑Plot")
        args.png.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(args.png, dpi=300)
        print(f"Plot gespeichert unter: {args.png.resolve()}")


if __name__ == "__main__":
    _cli()