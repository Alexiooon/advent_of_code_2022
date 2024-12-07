"""Day 5 solutions."""

DATA_PATH = "./data/day5_updates.txt"


def parse_input(path: str) -> tuple[list[int, int], list[int]]:
    """Read and parse the input data."""
    with open(path, 'r', encoding='utf8') as f:
        data = f.read().splitlines()

    split_index = data.index("")  # Cutoff index between rules and updates

    # I don't like double list comprehensions, but anyways
    rules = [[int(num) for num in rule.split("|")] for rule in data[:split_index]]
    updates = [[int(num) for num in update.split(",")] for update in data[split_index + 1:]]

    return rules, updates


def is_valid_update(update: list[int], rules: dict) -> bool:
    """Determines whether an update has all its pages ordered correctly."""
    # The way I've structured my data, its simplest to go backwards, and check
    # whether that number must come before any of the one which comes before it
    # in the update sheet.
    for idx, page in enumerate(reversed(update)):
        if any(i in rules[page] for i in update[:-(idx + 1)]):
            return False
    return True


def fix_update(update: list[int], rules: dict) -> list[int]:
    """Sort an update according to a set of rules."""
    # The strategy here is to iterate in the same fashion as in part 1. If a
    # number is OK in its position, then we pop it and append it to an new list.
    # Repeat until the original list is exhausted. The new list will always be
    # reversly ordered (i.e. a reverse()) would fix it. But we only care about
    # the middle number anyways so skip the reverse
    sorted_upd = []
    upd = update.copy()  # Even though its unnecessary, I don't want to destroy the input list
    while upd:
        for idx, page in enumerate(reversed(upd)):
            if all(i not in rules[page] for i in upd[:-(idx + 1)]):
                pop_idx = -(idx + 1)
                pop_val = upd.pop(pop_idx)
                sorted_upd.append(pop_val)
                break

    return sorted_upd


def main():
    """Solve today's puzzles."""
    rules, updates = parse_input(DATA_PATH)

    # My approach is to make a dictionary, where the keys are page numbers and its values are the
    # pages the must not come before it.
    rules_dict = {rule[0]: set() for rule in rules}
    for rule in rules:  # Add all the rules
        rules_dict[rule[0]].add(rule[1])

    # Now we just go through each update and try to determine if its valid
    middle_page_sum_p1 = 0  # Part 1 answer
    middle_page_sum_p2 = 0  # Part 2 answer
    for upd in updates:
        if is_valid_update(upd, rules_dict):
            middle_page_sum_p1 += upd[int(len(upd) / 2)]
        else:
            sorted_upd = fix_update(upd, rules_dict)
            middle_page_sum_p2 += sorted_upd[int(len(sorted_upd) / 2)]

    print(f"The sum of valid middle page numbers is {middle_page_sum_p1}")
    print(f"The sum of middle pages for corrected updates numbers is {middle_page_sum_p2}")


if __name__ == "__main__":
    main()
