import random

# Grid size
SIZE = 10

# States
WATER = 0
LAND = 1

# Probability that land becomes water if it has water neighbors
EROSION_PROB = 0.3

# Initialize grid: left half water, right half land
grid = [[WATER if j < SIZE//2 else LAND for j in range(SIZE)] for i in range(SIZE)]

def print_grid(grid, step):
    """Print grid with water as ~ and land as #"""
    print(f"\nStep {step}:")
    for row in grid:
        print(''.join(['~' if cell == WATER else '#' for cell in row]))

def count_water_neighbors(grid, i, j):
    """Count water cells in the 4 adjacent neighbors"""
    count = 0
    for di, dj in [(-1,0), (1,0), (0,-1), (0,1)]:
        ni, nj = i + di, j + dj
        if 0 <= ni < SIZE and 0 <= nj < SIZE:
            if grid[ni][nj] == WATER:
                count += 1
    return count

def update_grid(grid):
    """Apply erosion rules"""
    new_grid = [row[:] for row in grid]  # Deep copy

    for i in range(SIZE):
        for j in range(SIZE):
            if grid[i][j] == LAND:
                water_neighbors = count_water_neighbors(grid, i, j)
                if water_neighbors > 0:
                    # Land erodes to water with probability
                    prob = EROSION_PROB * water_neighbors / 4
                    if random.random() < prob:
                        new_grid[i][j] = WATER

    return new_grid

# Simulate
print_grid(grid, 0)

for step in range(1, 15):
    grid = update_grid(grid)
    print_grid(grid, step)
