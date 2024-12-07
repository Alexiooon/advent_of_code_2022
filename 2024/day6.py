"""Day 6 solutions."""

import numpy as np

DATA_PATH = "./data/day6_patrol.txt"

# Map objects
BLOCK = "#"
OPEN = "."
GUARD = "^"

# Directions
DIR_UP = 0
DIR_RIGHT = 1
DIR_DOWN = 2
DIR_LEFT = 3


def parse_input(path: str) -> tuple[np.ndarray[str], tuple[int, int]]:
    """Read and parse the input data."""
    with open(path, 'r', encoding='utf8') as f:
        data = f.read().splitlines()

    # Find the guard
    for i, row in enumerate(data):
        col = row.find(GUARD)
        if col != -1:  # Found the fella
            row[col] == OPEN  # If he walks past his starting position later
            guard_pos = (i, col)

    # Numpy arrays are probably the easiest to work with here
    return np.array([list(row) for row in data], dtype=str), guard_pos


def _next_position(pos: tuple[int, int], direction: int) -> tuple[int, int]:
    """Return the next position in a given direction."""
    if direction == DIR_UP:
        return pos[0] - 1, pos[1]
    if direction == DIR_RIGHT:
        return pos[0], pos[1] + 1
    if direction == DIR_DOWN:
        return pos[0] + 1, pos[1]
    if direction == DIR_LEFT:
        return pos[0], pos[1] - 1
    raise ValueError("Direction must be an integer between 0 and 3")


def is_inside(gmap: np.ndarray, pos: tuple[int, int]) -> bool:
    """Determine whether a position is within the array."""
    if not (0 <= pos[0] < gmap.shape[0]):
        return False
    if not (0 <= pos[1] < gmap.shape[1]):
        return False
    return True


def walk(
        gmap: np.ndarray[str],
        start: tuple[int, int],
        direction: int,
        append_dir: bool = False
    ) -> tuple[tuple[int, int], set[tuple[int, int]]]:
    """Walk until you hit an obstacle."""
    pos = start
    traversed = set()
    while True:
        next_pos = _next_position(pos, direction)
        # Walked out of the map
        if not is_inside(gmap, next_pos):
            pos = next_pos  # We want to return the "outside position", but not traverse it
            break
        # Walked into a block
        if gmap[next_pos] == BLOCK:
            break

        # Track his path
        pos = next_pos
        if append_dir:
            traversed.add((*pos, direction))
        else:
            traversed.add(pos)

    return pos, traversed


def main():
    """Solve today's puzzles."""
    guard_map, start_pos = parse_input(DATA_PATH)

    current_direction = DIR_UP
    indices_traversed = {start_pos}  # All indices traversed. Just the starting point for now
    pos = start_pos
    while is_inside(guard_map, pos):
        pos, path = walk(guard_map, pos, current_direction)
        indices_traversed = indices_traversed.union(path)
        current_direction = (current_direction + 1) % 4

    print(f"The guard walked over {len(indices_traversed)} unique tiles.")

    # Part 2
    # So we use the unique tile set which was the previous parts answer, and try
    # to place a box at each location. To find our loop condition, we add the
    # direction to each coordinate it traverses; if it is in the same position
    # twice while walking in the same direction, it has hit a loop.
    indices_traversed.remove(start_pos)  # Not allowed to put a box here
    valid_box_locations = 0
    for box_pos in indices_traversed:

        guard_map[box_pos] = BLOCK
        current_direction = DIR_UP
        walked_indices = {(*start_pos, current_direction)}
        pos = start_pos
        while is_inside(guard_map, pos):
            pos, path = walk(guard_map, pos, current_direction, append_dir=True)
            if not walked_indices.isdisjoint(path):  # Guard is stuck in a loop
                valid_box_locations += 1
                break
            walked_indices = walked_indices.union(path)
            current_direction = (current_direction + 1) % 4

        guard_map[box_pos] = OPEN  # Be nice and remove the blockage when we're done

    print(f"There are {valid_box_locations} valid box locations.")


if __name__ == "__main__":
    main()
