"""Day 10 solutions."""

from operator import add

DATA_PATH = "./data/day10_trails.txt"
TRAIL_START = 0
TRAIL_END = 9
ADJACENCIES = [  # Only the four cardinal directions are considered adjacent
    (0, 1),
    (1, 0),
    (0, -1),
    (-1, 0)
]


def parse_input(path: str) -> list[list[int]]:
    """Read and parse the input data."""
    with open(path, "r", encoding="utf8") as f:
        data = f.read().splitlines()
    return [[int(x) for x in list(row)] for row in data]


# I don't like reading the data automatically outside of main, but it makes things smooth...
TRAIL_MAP = parse_input(DATA_PATH)
SIZE = len(TRAIL_MAP)


def get_adjacent(pos: tuple[int, int]) -> set[tuple[int, int]]:
    """Get a list of valid adjacent coordinates."""
    def _is_inside(pos: tuple[int, int]) -> bool:
        """Determines whether a coordinate is within the map."""
        return (0 <= pos[0] < SIZE) and (0 <= pos[1] < SIZE)

    def _is_step(pos: tuple[int, int]) -> bool:
        """Determines wheter a coordinate is exactly 1 value higher."""
        return TRAIL_MAP[pos[0]][pos[1]] - val == 1

    new_coords = [tuple(map(add, pos, step)) for step in ADJACENCIES]
    val = TRAIL_MAP[pos[0]][pos[1]]

    return [coord for coord in new_coords if _is_inside(coord) and _is_step(coord)]


def main():
    """Solve today's puzzles."""
    trailhead_score = 0
    trailhead_ratings = 0
    for i, row in enumerate(TRAIL_MAP):
        for j, val in enumerate(row):
            if val != TRAIL_START:
                continue

            # For each trail start, we traverse breadth first. Each iteration yields all coordinates
            # which are adjacent and exactly one value above all current coordinates.
            coords = [(i, j)]
            for _ in range(TRAIL_END):
                new_coords = []
                for coord in coords:
                    new_coords.extend(get_adjacent(coord))
                coords = new_coords

            trailhead_score += len(set(coords))  # Skip duplicates by casting to set (Part 1)
            trailhead_ratings += len(coords)  # Include duplicates i.e. all unique paths (Part 2)

    print(f"The sum of scores of all trailheads is {trailhead_score}")
    print(f"The sum of ratings of all trailheads is {trailhead_ratings}")


if __name__ == "__main__":
    main()
