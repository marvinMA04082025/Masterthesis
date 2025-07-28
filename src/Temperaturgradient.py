def berechne_ergebnis(x: float, tiefe: float, gradient: float, y: float) -> float:

    return x + (tiefe * gradient) - y


if __name__ == "__main__":
    x = 10.0          # °C
    tiefe = 1000    # m
    gradient = 0.03   # °C/m  (= 30 °C pro km)
    y = 15           # °C

    ergebnis = berechne_ergebnis(x, tiefe, gradient, y)

    print(f"Ergebnis : {ergebnis:.3f} °C")
