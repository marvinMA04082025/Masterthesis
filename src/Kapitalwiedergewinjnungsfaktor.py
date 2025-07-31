def kapitalgewinnungsfaktor(i: float, n: int) -> float:
    return i * (1 + i)**n / ((1 + i)**n - 1)
crf = kapitalgewinnungsfaktor(0.06, 30)
print(f"CRF = {crf:.4f}  →  jährliche Annuität = K0 × {crf:.4f}")
