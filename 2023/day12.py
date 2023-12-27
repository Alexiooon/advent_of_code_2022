"""Day 12 challenges."""
import itertools
import math


def read_input(path):
    """Read the input data."""
    with open(path, 'r', encoding='utf8') as f:
        return f.read().splitlines()


def parse_input(data: list[str]):
    """Parse the input data by separating it into separate lists of springs and groupings."""
    springs = []
    groups = []
    for row in data:
        spring, group = row.split(" ", maxsplit=1)
        springs.append(spring)
        groups.append([int(x) for x in group.split(",")])
    return springs, groups


def expand_row(row: str, group: list[int]):
    """Expand a row of springs fivefold, with a "?" between each iteration."""
    factor = 1
    big_row = "?".join([row]*factor)
    big_group = group*factor
    return big_row, big_group


def count_safe(spring_row: str) -> int:
    """Count the number of springs known to be safe in a row i.e. "."."""
    return spring_row.count(".")


def count_damaged(spring_row: str) -> int:
    """Count the number of springs known to be damaged in a row i.e. "#"."""
    return spring_row.count("#")


def count_unknowns(spring_row: str) -> int:
    """Count the number of unknown springs i.e. "?" in a row."""
    return spring_row.count("?")


def count_total_damaged(group: list[int]) -> int:
    """Count the total number of damaged springs in a row (unknown locations included)."""
    return sum(group)


def create_layout(row: str, indexes: list[int]):
    """Create a layout given a list of indexes to place damaged springs at."""
    return "".join("#" if i in indexes or spring == "#" else "." for i, spring in enumerate(row))


def is_valid_layout(row: str, groups: list[int]) -> bool:
    """Check whether the proposed layout is valid given a set of groups."""
    row_groups = row.split(".")
    row_groups = [x for x in row_groups if x]
    if not len(row_groups) == len(groups):
        return False
    return all(len(row_groups[i]) == groups[i] for i in range(len(groups)))


def _get_first_cluster(row: str, start_index: int):
    """Get the first cluster."""
    i = start_index
    cluster_found = False
    cluster_start = len(row)
    while i < len(row):
        if row[i] != "." and not cluster_found:
            cluster_start = i
            cluster_found = True
        if cluster_found and row[i] == ".":
            break
        i += 1
    return cluster_start, i


def solve_everything(row: str, group: list[int]):
    """Solve everything for a row."""
    # Identify first group of (possible) damaged 
    gr = _get_first_cluster(row, 0)

    print("\n")
    print(f"Analyzing row: {row}")
    print(f"With remaining groups: {group}")
    if len(row) == 0:
        return 1

    groups_included = []
    total_combinations_row = 0
    while gr[1]-gr[0] >= sum(groups_included) + len(groups_included) - 1:
        # Calc possibilities
        total_spaces = gr[1] - gr[0] - sum(groups_included)
        combos = math.comb(total_spaces+1, len(groups_included))

        print(f"Checking subgroups: {groups_included}")
        print(f"Total spaces in the row: {total_spaces}")
        input()
        combos *= solve_everything(row[gr[1]:], group[len(groups_included):])
        total_combinations_row += combos
        print(combos)

        # Add another one
        if len(groups_included) == len(group):
            pass
        groups_included.append(group[len(groups_included)])
    print(f"Total ways of arranging {row} in {group}: {total_combinations_row}")
    return total_combinations_row


def solve_nothing(row: str, group: list[int]):
    """Useless function (just like me fr fr)."""

    def _end_of_line(row: str, group: list[int]):
        """Calculates whether we have enough tiles to go"""
        if not row:
            return True  # Nothing
        return len(row) < sum(group) + len(group) - 1 

    gidx = 0
    tot_pos = 0
    rowidx, _ = _get_first_cluster(row, 0)  # TODO: Use second output as rowidx+gize, is equal
    while True:  # gidx < len(group):
        # Get some info
        gsize = group[gidx]
        if rowidx == len(row):
            break
        # Propose the layout and check if its valid
        pos = 0
        block = row[rowidx:rowidx+gsize]
        next_tile = None if len(row) <= rowidx+gsize else row[rowidx+gsize]
        try:
            if all(x != "." for x in block) and next_tile != "#":
                pos = 1
                pos *= solve_nothing(row[rowidx+gsize+1:], group[gidx+1:])
        except IndexError:
            pass

        # Step up
        rowidx += 1
        tot_pos += pos
        if _end_of_line(row[rowidx+gsize+1:], group[gidx+1:]):
            break


    return tot_pos


def main():
    """Solve todays challenges."""
    full_data = read_input("./2023/data/day_12_springs.txt")
    # full_data = read_input("./2023/data/day_12_practice.txt")
    all_springs, all_groups = parse_input(full_data)

    # Early estimation of max number of possibilities i.e. ways we can place remaining damaged
    # springs at unknown locations (the layout does not have to be valid)
    possibilities = 0
    for i, line in enumerate(all_springs):
        possibilities = math.comb(count_unknowns(line),
                                  count_total_damaged(all_groups[i])-count_damaged(line))
    print(f"The number of possibilities is: {possibilities}")  # Few enough to brute force

    # Evaluate all combinations
    total_valid_layouts = 0
    for i, row in enumerate(all_springs):
        unknown_indexes = [j for j in range(len(row)) if row[j] == "?"]
        indexes_to_select = count_total_damaged(all_groups[i])-count_damaged(row)
        for layout in itertools.combinations(unknown_indexes, indexes_to_select):
            proposed_layout = create_layout(row, layout)
            total_valid_layouts += is_valid_layout(proposed_layout, all_groups[i])
    print(f"The total number of valid layouts is {total_valid_layouts}")

    # Part 2: Brute forcing probably wont do this time
    # Calculate number of possibilities again
    possibilities = 0
    for i, row in enumerate(all_springs):
        big_row, big_group = expand_row(row, all_groups[i])
        # print(f"Row under analysis: {big_row}, {big_group}")
        # possibilities = math.comb(count_unknowns(big_row),
        #                           count_total_damaged(big_group)-count_damaged(big_row))
        pos = solve_nothing(big_row, big_group)
        possibilities += pos
        # print(pos)
    print(f"The number of possibilities in part 2 is: {possibilities}")  # Yep, that's too much
    return
    # Find all valid combinations
    total_valid_layouts = 0
    for i, row in enumerate(all_springs):
        big_row, big_group = expand_row(row, all_groups[i])

        # Brute force the first row
        unknown_indexes = [j for j in range(len(big_row)) if big_row[j] == "?"]
        indexes_to_select = count_total_damaged(big_group)-count_damaged(big_row)
        for layout in itertools.combinations(unknown_indexes, indexes_to_select):
            proposed_layout = create_layout(big_row, layout)
            total_valid_layouts += is_valid_layout(proposed_layout, big_group)
        
        # Try a smart solution
        # sol = solve_everything(big_row, big_group)
        

        break
    print(f"For the first row there are now {total_valid_layouts} valid layouts")
    print(f"With the fancy formula, there are {combos} valid layouts")

if __name__ == '__main__':
    main()
