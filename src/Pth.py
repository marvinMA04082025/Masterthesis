import numpy as np
import matplotlib.pyplot as plt
from massenstrom import m_dot

# --------------------------------------------------
# Konstanten (bei Bedarf anpassen)
m_dot = m_dot        # kg/s   – Massenstrom
c_p   = 3700.59         # J/(kg·K)  – Wasser
b     = -5           # K      – Achsenabschnitt aus deinen Gleichungen
gradients = np.linspace(0.028, 0.033, 6)   # g-Werte von 0.028 … 0.033
# --------------------------------------------------

def delta_T(x, g, b=b):
    """ΔT(x) = g·x + b  (x z. B. Tiefe in m)."""
    return g * x + b

def Pth(x, g, m_dot=m_dot, c_p=c_p, b=b):
    """P(x) = ṁ · c_p · ΔT(x)  liefert Leistung in Watt."""
    return m_dot * c_p * delta_T(x, g, b)

#Verlauf zwischen 1000 m und 2000 m
x = np.arange(1700, 2200, 1)          # x-Achse (m)

plt.figure()
for g in gradients:
    P = Pth(x, g) / 1_000     # kW
    plt.plot(x, P, marker="o",
             label=f"g = {g:.3f} °C/m")

plt.xlabel("depth x (m)")
plt.ylabel("thermal performance (kW)")
plt.title("P(x) = g·x + b")
plt.grid(True)
plt.legend(title="g-functions")
plt.tight_layout()
plt.show()

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