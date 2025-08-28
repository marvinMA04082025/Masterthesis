import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as mpimg

# Bilddateien
# --- Bilddateien (lokale Windows-Pfadnamen) ---
img_success_path = r"C:\Users\Marvin\Desktop\Masterarbeit\Bilder von Python\NPV Verteilung Bohrkosten P10.png"
img_failure_path = r"C:\Users\Marvin\Desktop\Masterarbeit\Bilder von Python\NPV Verteilung Abbruch_Borhksoten.png"


img_failure = mpimg.imread(img_failure_path)
img_success = mpimg.imread(img_success_path)

# Canvas
fig, ax = plt.subplots(figsize=(12, 8))
ax.axis("off")

# Positionen (x, y)
root = (0.5, 0.9)
left_child = (0.25, 0.6)
right_child = (0.75, 0.6)
left_leaf = (0.25, 0.25)
right_leaf = (0.75, 0.25)

bbox_kwargs = dict(boxstyle="round", ec="black", lw=1)

# Knotenbeschriftung: getauschte Pfade
ax.text(*root, "Bohrung\n(Drilling)", ha="center", va="center", bbox=bbox_kwargs, fontsize=12)
ax.text(*left_child, "Erfolg\nP = 50 %", ha="center", va="center", bbox=bbox_kwargs, fontsize=11)
ax.text(*right_child, "Fehlschlag\nP = 50 %", ha="center", va="center", bbox=bbox_kwargs, fontsize=11)

# Äste
ax.plot([root[0], left_child[0]], [root[1], left_child[1]], linewidth=1.5)
ax.plot([root[0], right_child[0]], [root[1], right_child[1]], linewidth=1.5)
ax.plot([left_child[0], left_leaf[0]], [left_child[1], left_leaf[1]], linewidth=1.5)
ax.plot([right_child[0], right_leaf[0]], [right_child[1], right_leaf[1]], linewidth=1.5)

# Wahrscheinlichkeiten (50 % je Pfad)
ax.text((root[0]+left_child[0])/2 - 0.03, (root[1]+left_child[1])/2 + 0.02, "50 %", ha="center", va="center", fontsize=10)
ax.text((root[0]+right_child[0])/2 + 0.03, (root[1]+right_child[1])/2 + 0.02, "50 %", ha="center", va="center", fontsize=10)

# Helper zum Einbetten
def add_img(ax, img, position, zoom=0.35):
    im = OffsetImage(img, zoom=zoom)
    ab = AnnotationBbox(im, position, frameon=False)
    ax.add_artist(ab)

# Bilder an Endknoten (getauscht)
add_img(ax, img_success, left_leaf, zoom=0.35)   # Erfolg links
add_img(ax, img_failure, right_leaf, zoom=0.35)  # Fehlschlag rechts

plt.title("Entscheidungsbaum mit NPV-Verteilungen", fontsize=14, pad=20)
plt.tight_layout()
plt.show()
