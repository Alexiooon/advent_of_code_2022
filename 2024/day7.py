"""Day 7 solutions."""

import numpy as np

DATA_PATH = "./data/day7_equations.txt"

# Operands
ADDITION = "0"
MULTIPLICATION = "1"
CONCATENATION = "2"


def parse_input(path: str) -> list:
    """Read and parse the input data."""
    with open(path, 'r', encoding='utf8') as f:
        data = f.read().splitlines()

    equations = []
    for row in data:
        total, components = row.split(": ")
        components = [int(x) for x in components.split(" ")]  # Convert str --> list[int]
        equations.append([int(total), components])

    return equations


def get_sum(components: list[int], operands: list[int]) -> int:
    """Calculate calibration value based on lists of components and operands."""
    tot = components[0]
    for i, operand in enumerate(operands):
        if operand == ADDITION:
            tot += components[i + 1]
        elif operand == MULTIPLICATION:
            tot *= components[i + 1]
        elif operand == CONCATENATION:
            tot = int(str(tot) + str(components[i + 1]))

    return tot


def is_valid_equation(total: int, components: list[int], base: int) -> bool:
    """Determines whether an equation is valid and should be considered."""
    def _increment(num: str) -> str:
        """Increment a number in arbitary base and return as string."""
        return np.base_repr(int(num, base) + 1, base).zfill(len(components) - 1)

    op_str = "0".zfill(len(components) - 1)
    while len(op_str) < len(components):
        eq_sol = get_sum(components, op_str)
        if eq_sol == total:
            return True
        op_str = _increment(op_str)
    return False


def main():
    """Solve today's puzzles."""
    equations = parse_input(DATA_PATH)

    # Part 1
    # Strategy is to construct a binary number where the 0s and 1s represent addition/multiplication
    # and its position in the number is where the operand should be applied. Definitely not my first
    # idea, but it was necessary for part 2 and still not very efficient.
    calibration_results = 0
    valid_rows = []
    for i, row in enumerate(equations):
        if is_valid_equation(*row, base=2):
            calibration_results += row[0]
            valid_rows.append(i)
    print(f"The total calibration result from valid eqations is {calibration_results}")

    # Part 2
    # Now we just change from binary numbers to ternary, and let 2 be the concatenation operator
    for i, row in enumerate(equations):
        if i in valid_rows:
            continue  # Already counted from part 1
        if is_valid_equation(*row, base=3):
            calibration_results += row[0]
    print(f"When allowing concatenation, the total calibration result is {calibration_results}")


if __name__ == "__main__":
    main()
