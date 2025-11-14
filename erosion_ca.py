import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

# Grid size
SIZE = 10

# States (gradient from water to land)
WATER = 0
ERODING_3 = 1  # Heavily eroded
ERODING_2 = 2  # Moderately eroded
ERODING_1 = 3  # Slightly eroded
LAND = 4       # Solid land

# Probability that a cell erodes one level if it has water neighbors
EROSION_PROB = 0.4

# Initialize grid: left half water, right half land
grid = np.full((SIZE, SIZE), LAND, dtype=int)
grid[:, :SIZE//2] = WATER

# Create custom colormap: blue gradients for water/erosion, yellow for land
colors = ['#0047ab', '#3366cc', '#6699ff', '#99ccff', '#ffcc00']  # Dark blue -> light blue -> yellow
n_bins = 5
cmap = LinearSegmentedColormap.from_list('erosion', colors, N=n_bins)

def count_water_neighbors(grid, i, j):
    """Count cells with lower erosion state in the 4 adjacent neighbors"""
    count = 0
    current_state = grid[i, j]
    for di, dj in [(-1,0), (1,0), (0,-1), (0,1)]:
        ni, nj = i + di, j + dj
        if 0 <= ni < SIZE and 0 <= nj < SIZE:
            # Count neighbors with lower state (more eroded)
            if grid[ni, nj] < current_state:
                count += 1
    return count

def update_grid(grid):
    """Apply erosion rules - cells gradually erode through states"""
    new_grid = grid.copy()

    for i in range(SIZE):
        for j in range(SIZE):
            if grid[i, j] > WATER:  # If not already water
                eroded_neighbors = count_water_neighbors(grid, i, j)
                if eroded_neighbors > 0:
                    # Cell erodes one level with probability
                    prob = EROSION_PROB * eroded_neighbors / 4
                    if np.random.random() < prob:
                        new_grid[i, j] = grid[i, j] - 1  # Erode one level

    return new_grid

# Simulate
steps = 25
fig, axes = plt.subplots(2, 5, figsize=(12, 6))
axes = axes.flatten()

for step in range(steps):
    if step < 10:
        ax = axes[step]
        ax.imshow(grid, cmap=cmap, vmin=WATER, vmax=LAND, interpolation='nearest')
        ax.set_title(f'Step {step}')
        ax.axis('off')

    grid = update_grid(grid)

plt.tight_layout()
plt.savefig('erosion_simulation.png', dpi=150, bbox_inches='tight')
print("Simulation complete! Check 'erosion_simulation.png'")
plt.show()
