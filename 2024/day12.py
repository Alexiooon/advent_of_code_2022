"""Day 12 solutions."""

from common import get_neighbours

DATA_PATH = "./data/day12_fields.txt"


def parse_input(path: str) -> list[list[int]]:
    """Read and parse the input data."""
    with open(path, "r", encoding="utf8") as f:
        data = f.read().splitlines()
    return [list(row) for row in data]


def is_new(coord: tuple[int, int]) -> bool:
    """Check whether a new coordinate is new."""
    row, col = coord
    return not IS_COUNTED[row][col]


def is_same_crop(coord: tuple[int, int], crop: str) -> bool:
    """Check whether a coordinate has the specified crop growing."""
    row, col = coord
    return GARDEN_MAP[row][col] == crop


def main():
    """Solve today's puzzles."""
    total_price = 0  # Part 1 solution
    for i, row in enumerate(GARDEN_MAP):
        for j, crop in enumerate(row):
            if IS_COUNTED[i][j]:
                continue

            coords = set()
            new_coords = {(i, j)}
            while len(new_coords):
                coords.update(new_coords)
                new_coords = set()
                for coord in coords:
                    neighbours = [x for x in get_neighbours(coord, SIZE) if is_same_crop(x, crop)]
                    new_coords.update(set(x for x in neighbours if x not in coords))
                    IS_COUNTED[coord[0]][coord[1]] = 1

            area = len(coords)
            circ = 4 * area - sum(len([x for x in get_neighbours(coord, SIZE) if is_same_crop(x, crop)])
                                  for coord in coords)  # The list comprehension from hell
            total_price += area * circ

    print(f"The total price for putting up fences around the plots is {total_price}")


if __name__ == "__main__":
    GARDEN_MAP = parse_input(DATA_PATH)
    SIZE = len(GARDEN_MAP)
    IS_COUNTED = [[0] * SIZE for _ in range(SIZE)]

    main()
