"""Day 11 solutions."""

DATA_PATH = "./data/day11_stones.txt"


def parse_input(path: str) -> list[int]:
    """Read and parse the input data."""
    with open(path, 'r', encoding='utf8') as f:
        data = [int(x) for x in f.read().split(" ")]
    return data


def map_stone(stone: int):
    """Map a stone to a list of its new values after a blink."""
    if stone == 0:
        return [1]

    if len(str(stone)) % 2 == 0:
        strone = str(stone)
        return [int(strone[:int(len(strone) / 2)]), int(strone[int(len(strone) / 2):])]

    return [2024 * stone]


def stone_list_to_dict(stones: list[int], count: int = 1):
    """Convert a list of stones to a dictionary of stones."""
    new_dict = {}
    for val in stones:
        if val not in new_dict:
            new_dict[val] = 0
        new_dict[val] += count

    return new_dict


def count_stone(some_stones: dict, new_stones: dict):
    """Count stones and append to dictionary."""
    for key, val in new_stones.items():
        if val == 0:
            continue
        if key in some_stones:
            some_stones[key] += val
        else:
            some_stones[key] = val


def main():
    """Solve today's puzzles."""
    stones = parse_input(DATA_PATH)
    stone_dict = stone_list_to_dict(stones, 1)
    print(stone_dict)

    # Iterate
    blinks = 25
    for _ in range(blinks):
        new_stones = {}
        for key, val in stone_dict.items():
            if val == 0:
                continue
            ns = map_stone(key)
            count_stone(new_stones, stone_list_to_dict(ns, val))
        stone_dict = new_stones
    stone_count = sum(val for val in stone_dict.values())
    print(f"After {blinks} blinks there are {stone_count} stones in the arrangement")

    # Iterate more
    blinks = 50
    for _ in range(blinks):
        new_stones = {}
        for key, val in stone_dict.items():
            if val == 0:
                continue
            ns = map_stone(key)
            count_stone(new_stones, stone_list_to_dict(ns, val))

        stone_dict = new_stones
    stone_count = sum(val for val in stone_dict.values())
    print(f"After {blinks} more blinks there are {stone_count} stones in the arrangement")


if __name__ == "__main__":
    main()
