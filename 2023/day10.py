"""Day 10 challenges."""

import numpy as np
import sys
sys.setrecursionlimit(5000)

ROT_90 = np.array([[0, 1], [-1, 0]])


def read_input_data(path: str):
    """Get the input data."""
    with open(path, 'r', encoding='utf8') as f:
        return f.read().splitlines()


def _out_of_bounds(grid: list[str], position: tuple[int, int]) -> bool:
    """Determine whether a given position is out of range or not."""
    col_length = len(grid)
    row_length = len(grid[0])
    y, x = position
    return not ((0 <= y < row_length) and (0 <= x < col_length))


def find_starting_position(grid: list[str]) -> tuple[int, int]:
    """Find the starting position in a grid of pipes."""
    for i, row in enumerate(grid):
        for j in range(len(row)):
            if grid[i][j] == "S":
                return i, j
    raise ValueError("No starting position found in grid")


def get_connections_out(grid: list[str], position: tuple[int, int]):
    """Get the two adjacent positions in a pipe."""
    y0, x0 = position
    pipe = grid[y0][x0]
    if pipe == "|":
        y1, x1 = y0 + 1, x0
        y2, x2 = y0 - 1, x0
    elif pipe == "-":
        y1, x1 = y0, x0 + 1
        y2, x2 = y0, x0 - 1
    elif pipe == "J":
        y1, x1 = y0 - 1, x0
        y2, x2 = y0, x0 - 1
    elif pipe == "7":
        y1, x1 = y0 + 1, x0
        y2, x2 = y0, x0 - 1
    elif pipe == "L":
        y1, x1 = y0, x0 + 1
        y2, x2 = y0 - 1, x0
    elif pipe == "F":
        y1, x1 = y0, x0 + 1
        y2, x2 = y0 + 1, x0
    elif pipe == "S":  # Starting position
        v1, v2 = get_connections_in(grid, position)  # pylint: disable=unbalanced-tuple-unpacking
        y1, x1 = v1
        y2, x2 = v2
    else:
        raise ValueError(f"Invalid input value: {pipe}")

    return [(y1, x1), (y2, x2)]


def get_connections_in(grid: list[str], position: tuple[int, int]):
    """Get a list of coordinates connecting to the current position.

    This does NOT imply that the connection goes both ways.
    """
    y0, x0 = position
    connections = []
    for y in range(-1, 2):
        for x in range(-1, 2):
            new_position = (y0+y, x0+x)
            if new_position == position:
                continue
            if _out_of_bounds(grid, position):
                continue
            try:
                if position in get_connections_out(grid, new_position):
                    connections.append(new_position)  # The new position mapped to our current one
            except ValueError:  # "." or "S"
                pass
    return connections


def get_next_position(grid: list[str], position: tuple[int, int], last_position: tuple[int, int]):
    """Get the next position given the current and previous position."""
    pos_1, pos_2 = get_connections_out(grid, position)
    return pos_1 if pos_2 == last_position else pos_2


def sweep_grid(grid: list[str], grid_scan: list, pipe_coordinates: list, start: tuple[int, int]):
    """Recursively sweep and area for tiles which are not included in the main loop."""
    y0, x0 = start
    if _out_of_bounds(grid, start):
        return
    if start in pipe_coordinates:
        grid_scan[y0][x0] = 1
        return
    if grid_scan[y0][x0] == 2:
        return
    grid_scan[y0][x0] = 2  # Inside the loop

    # Scan adjacent tiles
    for y, x in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
        new_position = (y0+y, x0+x)
        if new_position == start:
            continue
        if _out_of_bounds(grid, new_position):
            continue
        if grid_scan[y0+y][x0+x] == 0:  # Not scanned
            sweep_grid(grid, grid_scan, pipe_coordinates, new_position)

def right_hand_tile(current_position: tuple, next_position: tuple) -> tuple:
    """Get the grid coordinates for the tile to the right i.e. 90 degree rotation."""
    y0, x0 = current_position
    y1, x1 = next_position
    vec_in = np.array([y1-y0, x1-x0])
    dy, dx = np.dot(ROT_90, vec_in)
    return y0+dy, x0+dx


def poly_area(xy):
    """ 
        Calculates polygon area.
        x = xy[:,0], y = xy[:,1]
    """
    l = len(xy)
    s = 0.0
    # Python arrys are zer0-based
    for i in range(l):
        j = (i+1)%l  # keep index in [0,l)
        s += (xy[j,0] - xy[i,0])*(xy[j,1] + xy[i,1])
    return -0.5*s


def main():
    """Do not execute main functionality."""
    grid = read_input_data("./data/day_10_pipes.txt")
    start = find_starting_position(grid)

    # Part 1
    pos_1, pos_2 = get_connections_in(grid, start)  # pylint: disable=unbalanced-tuple-unpacking
    i = 1  # Iteration variable, by finding the connections to "S" we've already moved 1 step
    last_pos_1 = start
    last_pos_2 = start
    while True:
        pos_1, last_pos_1 = get_next_position(grid, pos_1, last_pos_1), pos_1
        pos_2, last_pos_2 = get_next_position(grid, pos_2, last_pos_2), pos_2
        i += 1

        if pos_1 == pos_2:  # Paths connected
            break
    print(f"Paths connected after {i} iterations")

    # Part 2
    # Create a list of all pipe coordinates
    pos_1, _ = get_connections_in(grid, start)  # pylint: disable=unbalanced-tuple-unpacking
    pipe_coordinates = [pos_1]  # Coordinates of all pipes in the main loop
    last_pos_1 = start
    while True:
        pos_1, last_pos_1 = get_next_position(grid, pos_1, last_pos_1), pos_1
        pipe_coordinates.append(pos_1)
        if pos_1 == start:  # Full loop
            break

    # Find the most top-left pipe coordinate in the main loop (Row has priority over column)
    start = sorted(pipe_coordinates)[0]
    grid_scan = np.zeros(shape=(len(grid[0]), len(grid[0])), dtype=int)  # Array of zeroes
    pos_1 = (start[0], start[1]+1)
    last_pos_1 = start

    # Move a full loop through the pipe. For each step, get the tile to the right (relative to
    # travelling direction) and sweep for tiles not included in the main loop. All things to the
    # right of the loop in the moving direction is either another pipe or a tile enclosed by the
    # loop. (Since we always start of an "F" and move to the right)
    # rht = right_hand_tile(last_pos_1, pos_1)
    # sweep_grid(grid, grid_scan, pipe_coordinates, rht)

    # while True:
    #     pos_1, last_pos_1 = get_next_position(grid, pos_1, last_pos_1), pos_1
    #     rht = right_hand_tile(last_pos_1, pos_1)
    #     sweep_grid(grid, grid_scan, pipe_coordinates, rht)
    #     if pos_1 == start:  # Full loop
    #         break

    print(f"A total of {np.sum(np.floor(grid_scan/2))} tiles are enclosed by the main loop")
    print(f"A total of {len(pipe_coordinates)} tiles are in the main loop")
    print(f"Calculated value: {poly_area(np.array(pipe_coordinates))}")
    shape_1 = np.array([[0,0],[1,0],[1,1],[0,1]])
    print(poly_area(shape_1))

if __name__ == "__main__":
    main()

# Correct value is between 441 < x < 453
# \[ A=\sum_{i=1}^{N-1}I_{i+1,i}+I_{1,N} \] where e.g. \[ I_{2,1}=\intop_{x_{1}}^{x_{2}}ydx=\frac{1}{2}(y_{2}+y_{1})(x_{2}-x_{1}) \]
#