from matplotlib.pyplot import title

import numpy as np
import matplotlib.pyplot as plt
"""
Plot von ΔT(z) = g·z + b
   – Tiefe z  : 1000–2000 m (Schritt 100 m)
   – Gradient : 0,028–0,033 °C/m (6 Stützpunkte)
   – b        : T_surface – T_measured
"""

import numpy as np
import matplotlib.pyplot as plt

#Eingabeparameter
T_surface   = 10.0      # °C  Oberflächentemperatur
T_measured  = 15.0      # °C  gemessene Temperatur
depth_min   = 1700      # m   Starttiefe
depth_max   = 2200      # m   Endtiefe
step        = 50        # m   Schrittweite
grad_min    = 0.028     # °C/m   untere Gradientgrenze
grad_max    = 0.033     # °C/m   obere Gradientgrenze
num_lines   = 6         # Anzahl der Linien zwischen min & max


# Tiefenvektor erzeugen
depths = np.arange(depth_min, depth_max + step, step)

# Gleichmäßig verteilte Gradienten
gradients = np.linspace(grad_min, grad_max, num_lines)

# Gemeinsamer Achsenabschnitt  b = T_surface – T_measured
b = T_surface - T_measured        # hier: 10 – 15 = –5 K

#Plot vorbereiten 
plt.figure()

for g in gradients:
    delta_T = g * depths + b                     # ΔT(z)
    func_str = f"ΔT(x) = {g:.3f}·x {b:+.0f}"
    plt.plot(depths, delta_T, marker="o", label=func_str)
    print(func_str)                              # Gleichung in Konsole

# Achsen & Titel
plt.xlabel("Depth z (m)")
plt.ylabel("ΔT (K)")
plt.title("ΔT(z) = gradient · x + (T_surface − T_injected)")
plt.grid(True)
plt.legend(title="Functions")
plt.tight_layout()
plt.show()