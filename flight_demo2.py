import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math

# Create a simple hub-and-spoke network
G = nx.Graph()

# Add nodes (airports)
hub = "ATL"  # Atlanta hub
spokes = ["NYC", "LAX", "CHI"]  # Spoke airports

# Add hub node to graph
G.add_node(hub)

# Add spoke nodes and connect each to the hub
for spoke in spokes:
    G.add_node(spoke)
    G.add_edge(hub, spoke)  # Create edge from hub to spoke

# Position nodes for visualization
pos = {}
pos[hub] = [0, 0]  # Hub in center at origin

# Place spokes in a circle around the hub
for i, spoke in enumerate(spokes):
    angle = 2 * math.pi * i / len(spokes)  # Evenly space around circle
    pos[spoke] = [2 * math.cos(angle), 2 * math.sin(angle)]  # Radius of 2

# Simple Flight - just track position and progress
route = [hub, "NYC", hub]  # Flight route: ATL -> NYC -> ATL (round trip)
current_segment = 0  # Which segment of route we're currently on (0 = ATL to NYC, 1 = NYC to ATL)
progress = 0.0  # Progress along current segment (0.0 = start, 1.0 = end)
speed = 0.01  # How fast plane moves per frame (0.01 = 1% per frame)

# Set up the matplotlib figure
fig, ax = plt.subplots(figsize=(10, 8))

def animate(frame):
    """Animation function called every frame"""
    global current_segment, progress

    # Clear previous frame
    ax.clear()
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.axis('off')
    plt.title("Flight Animation - Single Plane", fontsize=16)

    # Draw the network graph
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color='gray', width=2)  # Draw edges (routes)

    # Draw spoke airports (blue circles)
    nx.draw_networkx_nodes(G, pos, nodelist=spokes, ax=ax,
                          node_color='lightblue', node_size=800)

    # Draw hub airport (larger red circle)
    nx.draw_networkx_nodes(G, pos, nodelist=[hub], ax=ax,
                          node_color='red', node_size=1200)

    # Draw airport labels
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=12, font_weight='bold')

    # Calculate and draw plane position
    if current_segment < len(route) - 1:
        # Get start and end airports for current segment
        start_node = route[current_segment]
        end_node = route[current_segment + 1]

        start_pos = pos[start_node]
        end_pos = pos[end_node]

        # Interpolate between start and end positions
        plane_x = start_pos[0] + (end_pos[0] - start_pos[0]) * progress
        plane_y = start_pos[1] + (end_pos[1] - start_pos[1]) * progress

        # Draw plane emoji at calculated position
        ax.text(plane_x, plane_y, '✈️', fontsize=25, ha='center', va='center', zorder=10)

        # Update progress along current segment
        progress += speed

        # Check if we've reached the end of current segment
        if progress >= 1.0:
            progress = 0.0  # Reset progress for next segment
            current_segment += 1  # Move to next segment

            # Check if we've completed the entire route
            if current_segment >= len(route) - 1:
                current_segment = 0  # Start route over from beginning

# Create animation (500 frames, 50ms between frames)
ani = animation.FuncAnimation(fig, animate, frames=500, interval=50, repeat=True)

plt.tight_layout()
plt.show()
