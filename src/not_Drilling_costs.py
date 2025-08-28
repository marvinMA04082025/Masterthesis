from __future__ import annotations
import pandas as pd
import matplotlib.pyplot as plt


def bohrkosten(x: float) -> float:

    return 0.131223 * x**2 + 2508.990455 * x + 1_643_364.545458


def main(start: int = 1700, stop: int = 2200, step: int = 100) -> None:

    # Daten erzeugen
    depths = list(range(start, stop + 1, step))
    costs = [bohrkosten(d) for d in depths]

    # Tabelle ausgeben
    df = pd.DataFrame({"Tiefe (m)": depths, "Bohrkosten (€)": costs})
    print("\nBohrkosten[Tiefe → Kosten]:\n")
    print(df.to_string(index=False))

    # Plot erzeugen
    fig, ax = plt.subplots()
    ax.plot(depths, costs)
    ax.set_xlabel("Tiefe (m)")
    ax.set_ylabel("Bohrkosten (M€)")
    ax.set_title(f"Bohrkosten für Tiefen {start}–{stop}m")
    ax.grid(True)

    # Funktionsgleichung im Plot anzeigen
    equation = r"$K(x)=0.131223\,x^{2}+2508.990455\,x+1\,643\,364.545458$"
    ax.text(
        0.05,
        0.95,
        equation,
        transform=ax.transAxes,
        fontsize=10,
        va="top",
        bbox=dict(boxstyle="round", facecolor="white", alpha=0.8),
    )

    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()