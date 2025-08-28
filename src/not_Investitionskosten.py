import numpy as np
import matplotlib.pyplot as plt

# Define the valid ranges
DEPTH_MIN, DEPTH_MAX = 1_700, 2_200    # meters
LENGTH_MIN, LENGTH_MAX = 1_000, 3_000  # meters


# --- Kostenfunktionen ---
def drilling_cost(depth_m: float) -> float:

    return 0.131223 * depth_m**2 + 2_508.990455 * depth_m + 1_643_364.545458

def pipeline_cost(length_m: float) -> float:
    
    return 700.0 * length_m

def investment_cost(depth_m: float, length_m: float) -> float:
   
    if not (DEPTH_MIN <= depth_m <= DEPTH_MAX):
        raise ValueError(f"depth_m ({depth_m}) muss zwischen {DEPTH_MIN} und {DEPTH_MAX} m liegen.")
    if not (LENGTH_MIN <= length_m <= LENGTH_MAX):
        raise ValueError(f"length_m ({length_m}) muss zwischen {LENGTH_MIN} und {LENGTH_MAX} m liegen.")
    return drilling_cost(depth_m) + pipeline_cost(length_m)

# --- Beispiel 1: Einzelberechnung ---

depth = 1_700   # m
length = 2_000  # m
print(f"Gesamt-CAPEX: {investment_cost(depth, length):,.0f} €")

# Generate grid
depths = np.linspace(DEPTH_MIN, DEPTH_MAX, 50)   # 50 points for smooth contours
lengths = np.linspace(LENGTH_MIN, LENGTH_MAX, 50)
D, L = np.meshgrid(depths, lengths)

# Cost function
C = 0.131223 * D**2 + 2_508.990455 * D + 1_643_364.545458 + 700 * L

# Plot
fig, ax = plt.subplots(figsize=(8, 6))
contour = ax.contourf(L, D, C, levels=20, cmap='YlOrRd')  # Beispiel mit 'plasma'
cbar = fig.colorbar(contour)
cbar.set_label('Investitionskosten (Mio. Euro)')

ax.set_xlabel('Leitungslänge L (m)')
ax.set_ylabel('Bohrtiefe d (m)')
ax.set_title('Investitionskosten in Abhängigkeit von Bohrtiefe und Leitungslänge')

plt.tight_layout()
plt.show()