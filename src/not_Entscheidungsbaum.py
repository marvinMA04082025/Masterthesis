import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

EDGE_COLOR = "#555555"
# Net Present Value (NPV) calculation function
# Includes 2% yearly growth for both O&M and pump costs
def calc_npv(C_inv, Q_year, price_heat, O1, g, F_pump, r, N):
    years       = np.arange(1, N+1)
    discount    = 1.0 / (1 + r) ** years
    O_series    = O1 * (1 + g) ** (years - 1)
    F_series    = F_pump * (1 + g) ** (years - 1)
    R_series    = Q_year * price_heat
    cashflows   = R_series - (O_series + F_series)
    return -C_inv + np.sum(cashflows * discount)

# --- Projektparameter ---
price_heat = 170      # EUR/MWh_th
g          = 0.02     # Wachstumsrate 2%
r          = 0.06     # Diskontsatz 6%
N          = 30       # Lebensdauer in Jahren

# --- Excel-Daten einlesen ---
df = pd.read_excel(r"C:\Users\Marvin\Desktop\Masterarbeit\Opex auswertung_P10 undso.xlsx")

# Kosten-Mappings
drilling_map = {"P10": 6_437_353, "P50": 7_038_546, "P90": 7_644_953}
pipeline_map = {"P10":   841_306, "P50": 1_403_443, "P90": 1_960_620}
pumping_map  = {"P10": 1_775_124, "P50": 2_380_268, "P90": 2_992_288}

# Entscheidungen und Wertebereiche
decisions = [
    ("drilling costs", ["P10", "P50", "P90"]),
    ("subsidies",      ["approved", "denied"]),
    ("pipeline costs", ["P10", "P50", "P90"]),
    ("pumping costs",  ["P10", "P50", "P90"]),
]

class Node:
    def __init__(self, name, node_type="decision", subsidy_flag=False):
        self.name = name
        self.node_type = node_type  # decision, intermediate, leaf
        self.subsidy_flag = subsidy_flag
        self.children: dict[str, "Node"] = {}

# Pfad-NPV-Funktion
def compute_npv(path: list[str]) -> float:
    dr, sb, pl, pu = path
    # Basis CAPEX
    C_inv = drilling_map[dr] + pipeline_map[pl]
    # Abzug 40% Subvention auf Bohrkosten
    if sb == "approved":
        C_inv -= 0.4 * drilling_map[dr]
    # OPEX-Parameter aus Excel
    row = df[(df["Bohrkosten €"] == drilling_map[dr]) &
             (df["Pipelinekosten €"] == pipeline_map[pl])].iloc[0]
    O1     = row["Gesamt-OPEX €"]
    F_pump = pumping_map[pu]
    Q_year = row["Wärme MWh/a"]
    return calc_npv(C_inv, Q_year, price_heat, O1, g, F_pump, r, N)

# Baumaufbau mit Subsidy-Flag-Propagation
def build_tree(level: int = 0, path: list[str] = None, subsidy_applied: bool = False) -> Node:
    if path is None:
        path = []
    if level == len(decisions):
        npv = compute_npv(path)
        return Node(f"NPV={npv:,.2f} EUR", "leaf", subsidy_flag=subsidy_applied)

    dec_name, values = decisions[level]
    node = Node(dec_name, "decision", subsidy_flag=subsidy_applied)
    for v in values:
        # Determine if subsidy applies on this branch
        new_subsidy = subsidy_applied or (dec_name == "subsidies" and v == "approved")
        inter = Node(f"result\n({dec_name}={v})", "intermediate", subsidy_flag=new_subsidy)
        node.children[v] = inter
        inter.children[""] = build_tree(level + 1, path + [v], new_subsidy)
    return node

# Layout
root = build_tree()
positions = {}
edges = []
def assign_pos(node: Node, depth: int, x_counter: list[int], spacing: int = 6) -> float:
    y = -depth if node.node_type != "intermediate" else -(depth + 0.5)
    if not node.children:
        x = x_counter[0] * spacing
        x_counter[0] += 1
        positions[node] = (x, y)
        return x
    child_infos = []
    for lbl, child in node.children.items():
        cx = assign_pos(child, depth + 1, x_counter, spacing)
        child_infos.append((cx, lbl, child))
    x = sum(cx for cx, _, _ in child_infos) / len(child_infos)
    positions[node] = (x, y)
    for cx, lbl, child in child_infos:
        edges.append(((positions[node][0], positions[node][1]), (cx, positions[child][1]), lbl))
    return x
assign_pos(root, 0, [0])

# Zeichnen
fig, ax = plt.subplots(figsize=(38, 20))
ax.set_axis_off()
for (x0, y0), (x1, y1), label in edges:
    ax.plot([x0, x1], [y0, y1], linewidth=0.9, color=EDGE_COLOR)
    if label:
        xm, ym = (x0 + x1) / 2, (y0 + y1) / 2
        ax.text(xm, ym, label, ha="center", va="center", fontsize=7)
for node, (x, y) in positions.items():
    # Coloring: highlight if subsidy_flag=True
    if node.subsidy_flag:
        facecolor = "#FFEBCC"  # light orange
    else:
        facecolor = "#EFEFEF" if node.node_type == "intermediate" else ("#CCEFFF" if node.node_type == "leaf" else "#FFFFFF")
    ax.text(x, y, node.name, ha="center", va="center",
            bbox=dict(boxstyle="round", pad=0.35, facecolor=facecolor, linewidth=0.8), fontsize=8)
plt.tight_layout()
plt.show()
