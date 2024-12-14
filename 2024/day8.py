"""Day 8 solutions."""

import itertools

DATA_PATH = "./data/day8_antennas.txt"
MAP_SIZE = 50


def parse_input(path: str) -> str:
    """Read and parse the input data."""
    with open(path, "r", encoding="utf8") as f:
        data = f.read()
    return data.replace("\n", "")  # We don't want newlines


def idx_to_coord(idx: int) -> tuple[int, int]:
    """Convert an index to tuple of 2D coordinates."""
    return int(idx / MAP_SIZE), idx % MAP_SIZE


def is_inside(pos: tuple[int, int]) -> bool:
    """Determine whether a position is within the array."""
    if not (0 <= pos[0] < MAP_SIZE):
        return False
    if not (0 <= pos[1] < MAP_SIZE):
        return False
    return True


def _mirror(orig: tuple[int, int], pos: tuple[int, int]) -> tuple[int, int]:
    """Flip coordinates around an origin."""
    row = orig[0] + (orig[0] - pos[0])
    col = orig[1] + (orig[1] - pos[1])
    return row, col


def get_antinodes(*antenna_coordinates) -> set[tuple[int, int]]:
    """Get all valid antinodes for a frequency."""
    # Trust me it works
    return set(_mirror(*antenna_pair) for antenna_pair
               in itertools.permutations(antenna_coordinates, 2)
               if is_inside(_mirror(*antenna_pair)))


def get_antinodes_p2(*antenna_coordinates) -> set[tuple[int, int]]:
    """Get all valid antinodes for a frequency for Part 2."""
    new_antinodes = set()
    for antenna_pair in itertools.permutations(antenna_coordinates, 2):
        new_antinodes.update(antenna_pair)
        next_antinode, prev_antinode = antenna_pair
        while is_inside(next_antinode):
            new_antinode = _mirror(next_antinode, prev_antinode)
            if is_inside(new_antinode):
                new_antinodes.add(new_antinode)
            next_antinode, prev_antinode = new_antinode, next_antinode
    return new_antinodes


def main():
    """Solve today's puzzles."""
    antenna_str = parse_input(DATA_PATH)
    frequencies = set(antenna_str.replace(".", "").replace("\n", ""))

    antinodes_p1 = set()  # Part 1 answer
    antinodes_p2 = set()  # Part 2 answer
    for freq in frequencies:
        # Find all coordinates of the specific frequency
        idx = 0
        locations = []
        while idx < len(antenna_str):
            new_idx = antenna_str[idx:].find(freq)
            if new_idx == -1:
                break
            idx += new_idx
            locations.append(idx_to_coord(idx))
            idx += 1

        # Get the coordinates of each antinode
        antinodes_p1.update(get_antinodes(*locations))
        antinodes_p2.update(get_antinodes_p2(*locations))
    print(f"There are {len(antinodes_p1)} antinodes within the map boundaries.")
    print(f"There are {len(antinodes_p2)} antinodes with the new conditions.")


if __name__ == "__main__":
    main()
