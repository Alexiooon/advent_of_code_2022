"""Day 10 challenges."""

import numpy as np

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


def right_hand_corner(current_position: tuple, next_position: tuple, from_next: bool) -> tuple:
    """Get the coordinates the "corner" to the right in front of the current position."""
    y0, x0 = current_position
    y1, x1 = next_position
    vec_fwd = np.array([y1-y0, x1-x0])
    vec_rhs = np.dot(ROT_90, vec_fwd)
    y, x = (vec_fwd+vec_rhs) / 2
    if from_next:
        return next_position[0] + y, next_position[1] + x
    return current_position[0] + y, current_position[1] + x

def poly_area(coordinates: list[tuple[int, int]]):
    """Calculates the area of a polygon."""
    length = len(coordinates)
    s = 0.0
    for i in range(length):
        j = (i+1) % length  # Next index, looping around
        s += (coordinates[j,0] - coordinates[i,0])*(coordinates[j,1] + coordinates[i,1])
    return 0.5*s


def main():
    """Solve todays challenges."""
    grid = read_input_data("./data/day_10_pipes.txt")
    start = find_starting_position(grid)

    # Part 1
    pos_1, pos_2 = get_connections_in(grid, start)  # pylint: disable=unbalanced-tuple-unpacking
    i = 1  # Iteration variable, by finding the connections to "S" we've already moved 1 step
    last_pos_1 = start
    last_pos_2 = start
    pipe_coordinates = [pos_1, pos_2]  # Coordinates of all pipes in the main loop, used in part 2
    while True:
        pos_1, last_pos_1 = get_next_position(grid, pos_1, last_pos_1), pos_1
        pos_2, last_pos_2 = get_next_position(grid, pos_2, last_pos_2), pos_2
        pipe_coordinates.append(pos_1)
        pipe_coordinates.append(pos_2)

        i += 1
        if pos_1 == pos_2:  # Paths connected
            break
    print(f"Paths connected after {i} iterations")

    # Part 2
    # Find the most top-left pipe coordinate in the main loop (Row has priority over column)
    start = sorted(pipe_coordinates)[0]
    pos_1 = (start[0], start[1]+1)  # First tile is guaranteed "F", now we can choose the direction
    last_pos_1 = start

    # We calculate the area inside a closed loop with Greens theorem. The only issue is that even
    # the pipe tiles are included, and the enclosed area from a corner depends on whether its an
    # inner corner (1/4th of a tile) or outside corner (3/4th). So, we loop through the pipe and
    # get the coordinates to the inner side of the pipe for each tile.
    polygon_coordinates = []
    while True:
        polygon_coordinates.append(right_hand_corner(last_pos_1, pos_1, from_next=False))
        polygon_coordinates.append(right_hand_corner(last_pos_1, pos_1, from_next=True))
        pos_1, last_pos_1 = get_next_position(grid, pos_1, last_pos_1), pos_1
        if pos_1 == start:  # Full loop
            break

    area = int(poly_area(np.array(polygon_coordinates)))  # Minus sign due to the direction we chose
    print(f"The number of tiles enclosed by the loop is value: {area}")


if __name__ == "__main__":
    main()
