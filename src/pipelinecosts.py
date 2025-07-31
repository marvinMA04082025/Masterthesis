from __future__ import annotations
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick


def pipelinecosts(L: float) -> float:
    return 700.0 * L


def tabelle_und_plot(start: int = 1_000, stop: int = 3_000, step: int = 10) -> None:
    laengen = list(range(start, stop + 1, step))
    kosten = [pipelinecosts(L) for L in laengen]

    # Plot erzeugen
    fig, ax = plt.subplots()
    ax.plot(laengen, kosten, marker="o")

    # X‑Achse bündig am linken Rand starten lassen
    ax.margins(x=0)

    # Y‑Achse direkt in Millionen Euro anzeigen
    ax.yaxis.set_major_formatter(
        mtick.FuncFormatter(lambda x, pos: f"{x / 1_000_000:.1f}")
    )
    ax.set_ylabel("Pipeline costs (Mio. €)")

    ax.set_xlabel("Length (m)")
    ax.set_title("Pipeline costs depending on pipeline length")
    ax.grid(True)

    # Funktionsgleichung als Textbox
    ax.text(
        0.05,
        0.95,
        "Pk(L) = 700 · L",
        transform=ax.transAxes,
        fontsize=10,
        verticalalignment="top",
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.7),
    )
    plt.show()


if __name__ == "__main__":
    tabelle_und_plot()
