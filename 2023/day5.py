"""Day 5 challenges."""

# Read the data
def read_input(path):
    """Read the input data."""
    with open(path, 'r', encoding='utf8') as f:
        return f.read().splitlines()


def get_numbers(number_str: str) -> list[int]:
    """Returns a list of numbers from a string of space-separated numbers."""
    return [int(x) for x in number_str.split(" ") if x]  # Filter out empty strings

def get_ranges(numbers: list[int]) -> list[tuple[int, int]]:
    """Get a list of ranges from a list of numbers."""    
    return [(numbers[i], numbers[i+1]) for i in range(0, len(numbers), 2)]


def parse_map(_map: list[str]):
    """Parse a map."""
    return [get_numbers(line) for line in _map]


def get_and_parse_maps(data: list[str]) -> list[list[int, int, int]]:
    """Find and parse all the maps."""
    map_starts = []
    for i, line in enumerate(data):
        if "map" in line:
            map_starts.append(i)

    # Separate the maps. skip the header
    maps = []
    for i, start in enumerate(map_starts):
        try:
            maps.append(parse_map(data[start+1:map_starts[i+1]-1]))
        except IndexError:
            maps.append(parse_map(data[start+1:]))
    return maps


def map_value(val: int, _map: list[list[int, int, int]]):
    """Map a value to a new one."""
    new_val = val
    for line in _map:
        dest, src, length = line
        if not src <= val < src+length:  # This line of the map does not include our value
            continue
        diff = val - src
        new_val = dest + diff
        break
    return new_val


def split_range(range_1: tuple[int, int], range_2: tuple[int, int]) -> list[tuple]:
    """Split a range depending if it overlaps with another."""
    split_indices = []  # Values at where to split
    val_1, length_1 = range_1
    val_2, length_2 = range_2
    if val_1 < val_2 < val_1 + length_1:
        split_indices.append(val_2)
    if val_1 < val_2 + length_2 - 1 < val_1 + length_1:
        split_indices.append(val_2 + length_2)

    # Split into new ranges
    new_ranges = []
    start = val_1
    for index in split_indices:
        new_ranges.append((start, index-start))
        start = index  # Start of new range
    new_ranges.append((start, val_1 + length_1 - start))

    return new_ranges

def map_range(start_ranges: list[tuple[int, int]], _map: list[list[int, int, int]]):
    """Map a range of values onto new ones."""
    # Split the start range into smaller ranges which overlap completely with a mapping
    ranges = start_ranges
    for line in _map:
        src_range = (line[1], line[2])
        new_ranges = []
        for val_range in ranges:
            new_ranges.extend(split_range(val_range, src_range))
        ranges = new_ranges

    # Map the initial value of each range
    mapped_ranges = []
    for val_range in ranges:
        mapped_ranges.append((map_value(val_range[0], _map), val_range[1]))
    return mapped_ranges

def main():
    """Solve todays challenges."""
    full_data = read_input("./data/day_5_seed_maps.txt")

    # Part 1
    # The main idea here is that we map the seeds one by one, all the way to location
    # Mapping is done by finding whether the initial value is within the source range, and if so,
    # Find the difference between source range start and the value. This diff plus the destination
    # range start is the new value.
    seeds = get_numbers(full_data[0][7:])
    maps = get_and_parse_maps(full_data)

    # Map the seeds to locations one at a time
    locations = []
    for seed in seeds:
        val = seed
        for _map in maps:
            val = map_value(val, _map)
        locations.append(val)

    loc = min(locations)
    print(f"The lowest location number using seed VALUES is {loc}")

    # Part 2
    # As the ranges are in the billions, it is no longer feasible to use the same approach as in
    # part 1. Instead, we treat everything as a range, defined as (start_value, range_length). We
    # then perform one mapping at a time, for all ranges we have. The only issue is whenever the
    # source range of any map does not completely cover an input range. To solve this, we split the
    # input range into multiple segments, each having a uniform transform with the given map. In the
    # end we have a lot more ranges than we started with, but its still significantly faster than
    # calculating every value.
    seed_ranges = get_ranges(seeds)
    ranges = seed_ranges
    for _map in maps:
        ranges = map_range(ranges, _map)

    loc = min(_range[0] for _range in ranges)
    print(f"The lowest location number using seed RANGES is {loc}")


if __name__ == '__main__':
    main()
