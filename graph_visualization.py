import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch


edges = [
    ('A', 'B', 2, 0),
    ('B', 'C', 2, 1),
    ('A', 'D', 2, 2),
    ('D', 'C', 2, 3),
    ('D', 'B', 1, 4)
]

G = nx.DiGraph()
for u, v, cap, idx in edges:
    G.add_edge(u, v, capacity=cap, index=idx)


pos = {
    'A': (0, 0),
    'D': (1, -1),
    'B': (1, 1),
    'C': (2, 0)
}

plt.figure(figsize=(8, 6))

nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=1200)
nx.draw_networkx_labels(G, pos, font_size=16, font_weight='bold')

nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=False,
                       connectionstyle='arc3,rad=0.1', width=1.5)


for u, v in G.edges():
    x1, y1 = pos[u]
    x2, y2 = pos[v]
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    dx, dy = x2 - x1, y2 - y1
    length = np.hypot(dx, dy)
    if length == 0:
        continue
    dx, dy = dx / length, dy / length
    arrow_len = 0.25
    start = (mx - (arrow_len/2)*dx, my - (arrow_len/2)*dy)
    end   = (mx + (arrow_len/2)*dx, my + (arrow_len/2)*dy)
    arrow = FancyArrowPatch(start, end, arrowstyle='->', mutation_scale=20,
                            color='gray', linewidth=1.5, zorder=10)
    plt.gca().add_patch(arrow)


edge_labels = {}
label_positions = {}
for u, v, data in G.edges(data=True):
    cap = data['capacity']
    idx = data['index']
    edge_labels[(u, v)] = f"{cap} (e{idx})"

    x1, y1 = pos[u]
    x2, y2 = pos[v]
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    dx, dy = x2 - x1, y2 - y1
    length = np.hypot(dx, dy)
    if length > 0:
        dx, dy = dx / length, dy / length

        perp_x, perp_y = -dy, dx

        offset = 0.12
        label_x = mx + perp_x * offset
        label_y = my + perp_y * offset
        label_positions[(u, v)] = (label_x, label_y)
    else:
        label_positions[(u, v)] = (mx, my)

for (u, v), label in edge_labels.items():
    x, y = label_positions[(u, v)]
    plt.text(x, y, label, fontsize=12, ha='center', va='center',
             bbox=dict(facecolor='white', edgecolor='none', alpha=0.7, boxstyle='round,pad=0.2'))

plt.text(pos['A'][0]-0.2, pos['A'][1]-0.2, 'Source', fontsize=12, color='green')
plt.text(pos['C'][0]+0.1, pos['C'][1]-0.2, 'Sink', fontsize=12, color='red')

plt.axis('off')
plt.tight_layout()
plt.savefig("example_graph.png", dpi=150)
plt.show()