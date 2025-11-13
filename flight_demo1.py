import networkx as nx
import matplotlib.pyplot as plt

# Create a simple hub-and-spoke network
G = nx.Graph()

# Add nodes (airports)
hub = "ATL"  # Atlanta hub
spokes = ["NYC", "LAX", "CHI"]

# Add hub
G.add_node(hub)

# Add spokes and connect to hub
for spoke in spokes:
    G.add_node(spoke)
    G.add_edge(hub, spoke)

# Position nodes in a hub-and-spoke layout
pos = {}
pos[hub] = [0, 0]  # Hub in center

# Place spokes around the hub
import math
for i, spoke in enumerate(spokes):
    angle = 2 * math.pi * i / len(spokes)
    pos[spoke] = [2 * math.cos(angle), 2 * math.sin(angle)]

# Create the plot
fig, ax = plt.subplots(figsize=(10, 8))
ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.axis('off')
plt.title("Flight Network - Hub and Spoke", fontsize=16)

# Draw the network
nx.draw_networkx_edges(G, pos, ax=ax, edge_color='gray', width=2)

# Draw spoke nodes
nx.draw_networkx_nodes(G, pos, nodelist=spokes, ax=ax,
                      node_color='lightblue', node_size=800, node_shape='o')

# Draw hub node (larger, different color)
nx.draw_networkx_nodes(G, pos, nodelist=[hub], ax=ax,
                      node_color='red', node_size=1200, node_shape='o')

# Draw labels
nx.draw_networkx_labels(G, pos, ax=ax, font_size=12, font_weight='bold')

# Print graph info
print(f"Number of airports: {G.number_of_nodes()}")
print(f"Number of routes: {G.number_of_edges()}")
print(f"Hub: {hub}")
print(f"Spokes: {spokes}")

plt.tight_layout()
plt.show()
