"""Day 7 challenges."""

import math

def read_input(path):
    """Read the input data."""
    with open(path, 'r', encoding='utf8') as f:
        return f.read().splitlines()


def find_starting_positions(coordinates: list[str]):
    """Return a list of all locations which end with "A"."""
    return [coord for coord in coordinates if coord[-1] == "A"]


def main():
    """Solve todays challenges."""
    full_data = read_input("./data/day_8_coordinates.txt")
    lr_instr = full_data[0]

    # Create a dictionary with LHS as keys and RHS as values
    mapping = {}
    for line in full_data[2:]:
        mapping[line[0:3]] = {
            "L": line[7:10],
            "R": line[12:15]
        }

    # Part 1: Traverse the map
    i = 0  # Iteration variable
    loc = "AAA"  # Current location
    while True:
        direction = lr_instr[i % len(lr_instr)]
        loc = mapping[loc][direction]
        i += 1
        if loc == "ZZZ":
            break
    print(f"It took {i} steps to reach ZZZ")

    # Part 2: We start at multiple destinations, and hope its not too hard to brute force... (it is)
    # Also gather some data about when and where the different ghosts reaches end nodes
    locs = find_starting_positions(mapping.keys())
    i = 0  # Iteration variable
    max_iter = 1000000
    ghost_tracking = [{"iter": []} for _ in range(len(locs))]  # Record endpoints we reach and when
    while True:
        direction = lr_instr[i % len(lr_instr)]
        locs = [mapping[ghost_loc][direction] for ghost_loc in locs]
        i += 1
        end_nodes = [ghost_loc == "ZZZ" for ghost_loc in locs]
        if all(end_nodes):  # We found the solution
            break
        if i > max_iter:  # Took too long, probably won't be able to brute force
            break

        # Track endpoints we find
        for j, ghost_loc in enumerate(locs):
            if ghost_loc[-1] == "Z":
                ghost_tracking[j]["iter"].append(i)
                if ghost_loc not in ghost_tracking[j]:
                    ghost_tracking[j][ghost_loc] = 0
                ghost_tracking[j][ghost_loc] += 1
    if i <= max_iter:
        print(f"It took {i} steps to only be on nodes ending with Z")
        return
    print(f"Could not find the solution to part 2 in {max_iter} steps")

    # Check our ghost tracking for some info:
    #  1. Assert that each ghost only reaches a single endpoint
    #  2. Assert that it reaches that endpoint at a frequency that is dividable with the length of
    #     our set of instructions
    # These two combined means that every ghost is in a closed loop which we know the number of
    # steps in. So we just need to find the first common point between them
    # i.e. least common denominator.
    frequencies = []
    for ghost in ghost_tracking:
        assert len(ghost.keys()) == 2, "The number of unique end points reached was not 1"

        assert len(ghost["iter"]) > 1, "Not enough data to find end point frequency"
        for i, end_iter in enumerate(ghost["iter"]):
            assert end_iter % len(lr_instr) == 0, "Found end point with bad frequency"
        frequencies.append(ghost["iter"][1] - ghost["iter"][0])
    print(f"It took {math.lcm(*frequencies)} steps to only be on nodes ending with Z")

if __name__ == '__main__':
    main()
