"""Day 9 challenges."""


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



def main():
    """Do not execute main functionality."""
    grid = read_input_data("./data/day_10_pipes.txt")
    start = find_starting_position(grid)
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


if __name__ == "__main__":
    main()
