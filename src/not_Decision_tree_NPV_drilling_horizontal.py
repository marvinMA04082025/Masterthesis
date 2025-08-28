import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as mpimg
import numpy as np
import os

# -------------------------------------------------
# 1) Daten & EMV‑Berechnung
# -------------------------------------------------
npv_success_values = [31.35, 48.75, 66.28]   # Mio€
npv_failure = -5.6                           # Mio€
mean_success = np.mean(npv_success_values)   # 48.79Mio€
emv = 0.5 * mean_success + 0.5 * npv_failure # 21.60Mio€

root_label = f"Bohrung\n(Drilling)\nEMV = {emv:0.2f}Mio€"

# -------------------------------------------------
# 2) Bilder laden (falls nicht vorhanden: Platzhalter)
# -------------------------------------------------
img_success_path = r"C:\Users\Marvin\Desktop\Masterarbeit\Bilder von Python\NPV Verteilung Bohrkosten P10.png"
img_failure_path = r"C:\Users\Marvin\Desktop\Masterarbeit\Bilder von Python\NPV Verteilung Abbruch_Borhksoten.png"

def load_or_placeholder(path, size=(200, 200, 3)):
    if os.path.exists(path):
        return mpimg.imread(path)
    # grauer Platzhalter
    return np.full(size, 0.8)

img_success = load_or_placeholder(img_success_path)
img_failure = load_or_placeholder(img_failure_path)

# -------------------------------------------------
# 3) Entscheidungsbaum nach rechts aufbauen
# -------------------------------------------------
fig, ax = plt.subplots(figsize=(12, 6))
ax.axis("off")

# Koordinaten
root       = (0.1, 0.5)
success_n  = (0.4, 0.7)
failure_n  = (0.4, 0.3)
success_lf = (0.75, 0.7)
failure_lf = (0.75, 0.3)

bbox_kwargs = dict(boxstyle="round", ec="black", lw=1)

# Knotenbeschriftungen
ax.text(*root,        root_label,          ha="center", va="center",
        bbox=bbox_kwargs, fontsize=11, linespacing=1.3)
ax.text(*success_n,   "Erfolg\nP = 50%",   ha="center", va="center",
        bbox=bbox_kwargs, fontsize=10)
ax.text(*failure_n,   "Fehlschlag\nP = 50%", ha="center", va="center",
        bbox=bbox_kwargs, fontsize=10)

# Äste
ax.plot([root[0], success_n[0]],  [root[1], success_n[1]],  lw=1.5)
ax.plot([root[0], failure_n[0]], [root[1], failure_n[1]], lw=1.5)
ax.plot([success_n[0], success_lf[0]], [success_n[1], success_lf[1]], lw=1.5)
ax.plot([failure_n[0], failure_lf[0]], [failure_n[1], failure_lf[1]], lw=1.5)

# Wahrscheinlichkeitslabels
ax.text((root[0] + success_n[0]) / 2, (root[1] + success_n[1]) / 2 + 0.05,
        "50%", ha="center", va="center", fontsize=9)
ax.text((root[0] + failure_n[0]) / 2, (root[1] + failure_n[1]) / 2 - 0.05,
        "50%", ha="center", va="center", fontsize=9)

# Helfer für Bilder
def add_img(ax, img, position, zoom=0.35):
    ab = AnnotationBbox(OffsetImage(img, zoom=zoom), position, frameon=False)
    ax.add_artist(ab)

add_img(ax, img_success, success_lf)
add_img(ax, img_failure, failure_lf)

plt.title("Entscheidungsbaum (horizontal)", fontsize=13, pad=15)
plt.tight_layout()
plt.show()
