import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as mpimg
import numpy as np
import os

# -------------------------------------------------
# 1) Daten & EMV‑Berechnung
# -------------------------------------------------
npv_success_values = [31.35, 48.75, 66.28]   # Mio €
npv_failure = -5.6                           # Mio €
mean_success = np.mean(npv_success_values)   # 48.79 Mio €
emv = 0.5 * mean_success + 0.5 * npv_failure # 21.60 Mio €

root_label = f"Drilling\nEMV = {emv:0.2f} Mio €"

# -------------------------------------------------
# 2) Bilder laden
# -------------------------------------------------
img_success_dist_path = r"C:\\Users\\Marvin\\Desktop\\Masterarbeit\\Bilder von Python\\NPV Verteilung Bohrkosten P10.png"
img_failure_path      = r"C:\\Users\\Marvin\\Desktop\\Masterarbeit\\Bilder von Python\\NPV Verteilung Abbruch_Borhkosten_without subsidies.png"

img_p10_path = r"C:\\Users\\Marvin\\Desktop\\Masterarbeit\\Bilder von Python\\Drilling_decision_P10_without subsidies.png"
img_p50_path = r"C:\\Users\\Marvin\\Desktop\\Masterarbeit\\Bilder von Python\\Drilling_decision_P50_without subsidies.png"
img_p90_path = r"C:\\Users\\Marvin\\Desktop\\Masterarbeit\\Bilder von Python\\Drilling_decision_P90_without subsidies.png"

def load_or_placeholder(path: str, size=(200, 200, 3)):

    if os.path.exists(path):
        return mpimg.imread(path)
    # Grauer Platzhalter (RGB‑Wert 0.8)
    return np.full(size, 0.8)

img_success_dist = load_or_placeholder(img_success_dist_path)
img_failure      = load_or_placeholder(img_failure_path)
img_p10          = load_or_placeholder(img_p10_path)
img_p50          = load_or_placeholder(img_p50_path)
img_p90          = load_or_placeholder(img_p90_path)

# -------------------------------------------------
# 3) Entscheidungsbaum nach rechts aufbauen
# -------------------------------------------------
fig, ax = plt.subplots(figsize=(14, 7))
ax.axis("off")

# Koordinaten
root       = (0.05, 0.50)
success_n  = (0.25, 0.70)
failure_n  = (0.25, 0.30)


failure_lf = (0.45, 0.1)

p10_lf = (0.8, 0.90)       #Standort der Bildder
p50_lf = (0.8, 0.5)
p90_lf = (0.8, 0.10)

bbox_kwargs = dict(boxstyle="round", ec="black", lw=1)

# Knotenbeschriftungen
ax.text(*root,      root_label,              ha="center", va="center", bbox=bbox_kwargs, fontsize=11, linespacing=1.3)
ax.text(*success_n, "Success\nP = 50 %",      ha="center", va="center", bbox=bbox_kwargs, fontsize=10)
ax.text(*failure_n, "Failure\nP = 50 %",  ha="center", va="center", bbox=bbox_kwargs, fontsize=10)

# Unterpfad‑Labels (P10/P50/P90) – mittig auf den Ästen
label_props = dict(ha="center", va="center", fontsize=9)
ax.text((success_n[0]+p10_lf[0])/2, (success_n[1]+p10_lf[1])/2 + 0.02, "P10", **label_props)
ax.text((success_n[0]+p50_lf[0])/2, (success_n[1]+p50_lf[1])/2,             "P50", **label_props)
ax.text((success_n[0]+p90_lf[0])/2, (success_n[1]+p90_lf[1])/2 - 0.02, "P90", **label_props)

# Äste zeichnen
# Wurzel → Erfolg / Fehlschlag
ax.plot([root[0], success_n[0]],  [root[1], success_n[1]],  lw=1.5)
ax.plot([root[0], failure_n[0]], [root[1], failure_n[1]], lw=1.5)

# Erfolg → P10 / P50 / P90
ax.plot([success_n[0], p10_lf[0]], [success_n[1], p10_lf[1]], lw=1.5)
ax.plot([success_n[0], p50_lf[0]], [success_n[1], p50_lf[1]], lw=1.5)
ax.plot([success_n[0], p90_lf[0]], [success_n[1], p90_lf[1]], lw=1.5)

# Fehlschlag → Leaf
ax.plot([failure_n[0], failure_lf[0]], [failure_n[1], failure_lf[1]], lw=1.5)

# Wahrscheinlichkeits‑Labels (Hauptebene)
ax.text((root[0]+success_n[0])/2, (root[1]+success_n[1])/2 + 0.05, "50 %", ha="center", va="center", fontsize=9)
ax.text((root[0]+failure_n[0])/2, (root[1]+failure_n[1])/2 - 0.05, "50 %", ha="center", va="center", fontsize=9)

# Helper‑Funktion zum Einfügen der Bilder

def add_img(ax, img, pos, zoom=0.3, align=(0.5, 0.5)):
    ab = AnnotationBbox(OffsetImage(img, zoom=zoom, resample=True),
                        pos, frameon=False, box_alignment=align)
    ax.add_artist(ab)


# Bilder platzieren
add_img(ax, img_failure,     failure_lf, zoom=0.32)
add_img(ax, img_p10,         p10_lf,     zoom=0.32)
add_img(ax, img_p50,         p50_lf,     zoom=0.32)
add_img(ax, img_p90,         p90_lf,     zoom=0.32)

plt.title("Decision tree – drilling costs without subsidies", fontsize=13, pad=15)
plt.tight_layout()
plt.show()
