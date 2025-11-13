import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Create a hub-and-spoke network
G = nx.Graph()

# Add nodes (airports)
hub = "ATL"  # Atlanta hub
spokes = ["NYC", "LAX", "CHI", "MIA", "DEN"]

G.add_node(hub)
for spoke in spokes:
    G.add_node(spoke)
    G.add_edge(hub, spoke)

# Position nodes in a hub-and-spoke layout
pos = nx.spring_layout(G, k=2, iterations=50)
# Manually adjust to look more hub-and-spoke
pos[hub] = [0, 0]  # Hub in center
import math
for i, spoke in enumerate(spokes):
    angle = 2 * math.pi * i / len(spokes)
    pos[spoke] = [2 * math.cos(angle), 2 * math.sin(angle)]

# Flight class
class Flight:
    def __init__(self, flight_id, route):
        self.id = flight_id
        self.route = route  # List of nodes to visit
        self.current_idx = 0
        self.progress = 0.0  # 0 to 1 along current edge
        self.speed = 0.02  # Movement speed per frame
        self.at_airport = True
        self.wait_time = 0
        self.wait_duration = 30  # Frames to wait at airport

    def get_position(self):
        if self.current_idx >= len(self.route) - 1:
            # Completed route, return to start
            self.current_idx = 0
            self.progress = 0.0
            self.at_airport = True
            self.wait_time = 0

        current_node = self.route[self.current_idx]

        if self.at_airport:
            # Waiting at airport
            return pos[current_node]

        # Flying between airports
        next_node = self.route[self.current_idx + 1]
        current_pos = pos[current_node]
        next_pos = pos[next_node]

        # Interpolate position
        x = current_pos[0] + (next_pos[0] - current_pos[0]) * self.progress
        y = current_pos[1] + (next_pos[1] - current_pos[1]) * self.progress
        return [x, y]

    def update(self):
        if self.at_airport:
            # Wait at airport
            self.wait_time += 1
            if self.wait_time >= self.wait_duration:
                self.at_airport = False
                self.wait_time = 0
        else:
            # Move along edge
            self.progress += self.speed
            if self.progress >= 1.0:
                # Reached next airport
                self.progress = 0.0
                self.current_idx += 1
                self.at_airport = True

# Create flights with different routes
flights = [
    Flight("F1", [hub, "NYC", hub, "LAX", hub]),
    Flight("F2", [hub, "CHI", hub, "MIA", hub]),
    Flight("F3", [hub, "DEN", hub]),
]

# Set up the plot
fig, ax = plt.subplots(figsize=(10, 8))
ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.axis('off')
plt.title("Flight Network Simulation (Hub-and-Spoke)", fontsize=16)

def animate(frame):
    ax.clear()
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.axis('off')
    plt.title("Flight Network Simulation (Hub-and-Spoke)", fontsize=16)

    # Draw the network
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color='gray', width=2)
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color='lightblue',
                          node_size=800, node_shape='o')

    # Draw hub differently
    nx.draw_networkx_nodes(G, pos, nodelist=[hub], ax=ax,
                          node_color='red', node_size=1000, node_shape='o')

    # Draw labels
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=10, font_weight='bold')

    # Update and draw flights
    for flight in flights:
        flight.update()
        flight_pos = flight.get_position()

        # Draw plane as emoji
        ax.text(flight_pos[0], flight_pos[1], '✈️', fontsize=20,
               ha='center', va='center', zorder=10)

        # Draw flight ID near plane
        ax.text(flight_pos[0], flight_pos[1] - 0.2, flight.id,
               fontsize=8, ha='center', va='top')

# Create animation
ani = animation.FuncAnimation(fig, animate, frames=500, interval=50, repeat=True)

plt.tight_layout()
plt.show()
