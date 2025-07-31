rate     = 0.06    # Zinssatz pro Periode (6 %)
n        = 30      # Anzahl Perioden

pv = (1 + rate) ** -n / rate
print(pv)         # 863.837598531476