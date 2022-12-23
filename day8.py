"""Day 8 challenges."""
# pylint: disable=invalid-name
# Imports
import os
import numpy as np

# Read the input data
path = os.path.join('.', 'data', 'day8_tree_grid.txt')
with open(path, 'r', encoding='utf8') as f:
    data = f.read().splitlines()

# Convert to numpy array of ints
grid = []
for row in data:
    grid.append([int(x) for x in row])
grid = np.array(grid, int)

visible = np.zeros_like(grid, dtype=bool)
def is_visible(x, y):
    """Check whether a tree is visible from any sides."""
    return grid[x, y] > max(grid[x, :y]) or grid[x, y] > max(grid[:x, y]) \
        or grid[x, y] > max(grid[x, y+1:]) or grid[x, y] > max(grid[x+1:, y])

for i, row in enumerate(grid):
    if i in (0, len(grid)-1):
        visible[i, :] = True
        continue
    for j, col in enumerate(row):
        if j in (0, len(grid)-1):
            visible[i, j] = True
            continue
        visible[i,j] = is_visible(i, j)
print(f"Total number of trees: {99*99}")
print(f"The number of visible trees from the outside is: {np.sum(np.sum(visible))}")

# %% Challenge 2
scenic_score = np.zeros_like(grid)

def get_score(x, y):
    """Get the scenic score from a tree."""
    height = grid[x,y]

    # Look up
    view = list(grid[x, :y])
    view.reverse()
    for dist, tree in enumerate(view):
        if tree >= height:
            break
    score = dist + 1  # pylint: disable=undefined-loop-variable

    # Look right
    view = list(grid[x+1:, y])
    for dist, tree in enumerate(view):
        if tree >= height:
            break
    score *= (dist + 1)

    # Look down
    view = list(grid[x, y+1:])
    for dist, tree in enumerate(view):
        if tree >= height:
            break
    score *= (dist + 1)

    # Look left
    view = list(grid[:x, y])
    view.reverse()
    for dist, tree in enumerate(view):
        if tree >= height:
            break
    score *= (dist + 1)

    return score

for i, row in enumerate(grid):
    if i in (0, len(grid)-1):
        scenic_score[i, :] = 0
        continue
    for j, col in enumerate(row):
        if j in (0, len(grid)-1):
            scenic_score[i, j] = 0
            continue
        scenic_score[i,j] = get_score(i, j)

print(f"Largest scenic score for any tree: {np.max(scenic_score)}")
