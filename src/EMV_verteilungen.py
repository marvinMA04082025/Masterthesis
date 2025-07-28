import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
#P10
# Gegebene Quantile (in Millionen €)
P10 = 27.82
P50 = 45.34
P90 = 63.48

# Standardnormal-Quantile
z10 = norm.ppf(0.10)
z50 = norm.ppf(0.50)  # entspricht 0
z90 = norm.ppf(0.90)

# Mittelwert aus dem Median
mu = P50

# Standardabweichung aus P10 und P90 (Durchschnitt beider Schätzungen)
sigma1 = (P50 - P10) / abs(z10)
sigma2 = (P90 - P50) / z90
sigma = (sigma1 + sigma2) / 2

# Erwarteter monetärer Wert (EMV) ist bei einer Normalverteilung gleich mu
emv = mu

# Varianz
variance = sigma ** 2

# Ausgabe der Ergebnisse
print(f"Mittelwert P10(μ): {mu:.2f} Mio €")
print(f"Standardabweichung P10(σ): {sigma:.2f} Mio €")
print(f"Varianz P10(σ²): {variance:.2f} (Mio €)²")
print(f"EMV P10: {emv:.2f} Mio €")
print("----------------------------")
#P50
P10 = 27.10
P50 = 44.62
P90 = 62.75

# Standardnormal-Quantile
z10 = norm.ppf(0.10)
z50 = norm.ppf(0.50)  # entspricht 0
z90 = norm.ppf(0.90)

# Mittelwert aus dem Median
mu = P50

# Standardabweichung aus P10 und P90 (Durchschnitt beider Schätzungen)
sigma1 = (P50 - P10) / abs(z10)
sigma2 = (P90 - P50) / z90
sigma = (sigma1 + sigma2) / 2

# Erwarteter monetärer Wert (EMV) ist bei einer Normalverteilung gleich mu
emv = mu

# Varianz
variance = sigma ** 2

# Ausgabe der Ergebnisse
print(f"Mittelwert P50(μ): {mu:.2f} Mio €")
print(f"Standardabweichung P50(σ): {sigma:.2f} Mio €")
print(f"Varianz P50(σ²): {variance:.2f} (Mio €)²")
print(f"EMV P50: {emv:.2f} Mio €")
print("----------------------------")

#P90
P10 = 26.37
P50 = 43.89
P90 = 62.03

# Standardnormal-Quantile
z10 = norm.ppf(0.10)
z50 = norm.ppf(0.50)  # entspricht 0
z90 = norm.ppf(0.90)

# Mittelwert aus dem Median
mu = P50

# Standardabweichung aus P10 und P90 (Durchschnitt beider Schätzungen)
sigma1 = (P50 - P10) / abs(z10)
sigma2 = (P90 - P50) / z90
sigma = (sigma1 + sigma2) / 2

# Erwarteter monetärer Wert (EMV) ist bei einer Normalverteilung gleich mu
emv = mu

# Varianz
variance = sigma ** 2

# Ausgabe der Ergebnisse
print(f"Mittelwert P90(μ): {mu:.2f} Mio €")
print(f"Standardabweichung P90(σ): {sigma:.2f} Mio €")
print(f"Varianz P90(σ²): {variance:.2f} (Mio €)²")
print(f"EMV P90: {emv:.2f} Mio €")