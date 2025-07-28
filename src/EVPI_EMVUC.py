import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Gegebene Werte (in Mio €)
V_success = 44.62
V_failure = -8.4

# Erfolgswahrscheinlichkeit p
p = np.linspace(0, 1, 100)

# EMV unter Unsicherheit (EMVUC)
EMVUC = p * V_success + (1 - p) * V_failure

# Erwartungswert bei perfekter Information (EV-perfect)
# Annahme: Alternative Entscheidung bei Scheitern liefert 0
EV_perfect = p * V_success

# EVPI
EVPI = EV_perfect - EMVUC

# Kritische Erfolgswahrscheinlichkeit
p_crit = -V_failure / (V_success - V_failure)

# Plot EMVUC vs. p
plt.figure()
plt.plot(p, EMVUC)
plt.axhline(0, linestyle='--')
plt.axvline(p_crit, linestyle='--')
plt.xlabel('Erfolgswahrscheinlichkeit p')
plt.ylabel('EMVUC [Mio €]')
plt.title('EMV unter Unsicherheit (EMVUC) als Funktion von p')
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()

# Plot EVPI vs. p
plt.figure()
plt.plot(p, EVPI)
plt.axvline(p_crit, linestyle='--')
plt.xlabel('Erfolgswahrscheinlichkeit p')
plt.ylabel('EVPI [Mio €]')
plt.title('EVPI als Funktion der Erfolgswahrscheinlichkeit p')
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()

# Tabelle mit ausgewählten Punkten
indices = [0, np.argmin(np.abs(p - p_crit)), 50, len(p) - 1]
df = pd.DataFrame({
    'p': p[indices],
    'EMVUC [Mio €]': EMVUC[indices],
    'EVPI [Mio €]': EVPI[indices]
})


# Python-Skript zur Berechnung von EMV, EMV unter Unsicherheit (EMVUC) und EVPI

# Gegebene Werte (in Mio €)
V_success = 44.62   # Ertrag bei Erfolg
V_failure = -8.4    # Verlust/Kosten bei Misserfolg
p = 0.5             # Aktuelle Erfolgswahrscheinlichkeit

# 1. EMV unter Unsicherheit
EMVUC = p * V_success + (1 - p) * V_failure

# 2. Erwartungswert bei perfekter Information
#    (bei Misserfolg keine Bohrung: Auszahlungswert = 0)
E_perfect = p * V_success + (1 - p) * 0

# 3. EVPI
EVPI = E_perfect - EMVUC

# Ausgabe
print(f"Aktueller p-Wert: {p:.2f}")
print(f"EMV unter Unsicherheit (EMVUC): {EMVUC:.2f} Mio €")
print(f"Erwartungswert mit perfekter Information: {E_perfect:.2f} Mio €")
print(f"EVPI (Wert perfekter Information): {EVPI:.2f} Mio €")
