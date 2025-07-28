import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Gegebene Werte (in Mio €)
V_success = 44.62
V_failure = -8.4

# EMV-Funktion
def emv(p):
    return p * V_success + (1 - p) * V_failure

# Kritische Erfolgswahrscheinlichkeit
p_crit = -V_failure / (V_success - V_failure)

# Werte für Plot
p = np.linspace(0, 1, 500)
emv_vals = emv(p)

# Plot erstellen
plt.figure()
plt.plot(p, emv_vals, label='EMV(p)')
plt.axhline(0, linestyle='--', label='EMV = 0')
plt.axvline(p_crit, linestyle='--', label=f'pₖ ≈ {p_crit:.4f}')
plt.xlabel('probability of success p')
plt.ylabel('EMV [Mio €]')
plt.title('EMV as a function of the probability of success p')
plt.legend()
plt.show()

# Tabelle mit ausgewählten Punkten
df = pd.DataFrame({
    'p': [0.0, p_crit, 0.5, 1.0],
    'EMV [Mio €]': [emv(0.0), emv(p_crit), emv(0.5), emv(1.0)]
})

import ace_tools as tools; tools.display_dataframe_to_user(name="EMV bei ausgewählten p-Werten", dataframe=df)
