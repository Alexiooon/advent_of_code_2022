"""Day 3 challenges."""

import math

# Read the data
def read_input(path):
    """Read the input data."""
    with open(path, 'r', encoding='utf8') as f:
        return f.read().splitlines()


def nearest_neighbours(arr: str, index: int, length: int) -> list:
    """Returns the values of all adjacent elements of a 2D array"""
    values = []
    indices = []
    row = int(index / length)
    col = index % length
    row_slice = range(max(0, col-1), min(col+2, length))
    if row != 0:  # If not on the top row
        for i in row_slice:
            values.append(arr[(row-1)*length + i])
            indices.append((row-1)*length + i)

    for i in row_slice:
        values.append(arr[row*length + i])
        indices.append(row*length + i)

    if row != length-1:  # If not on the bottom row
        for i in row_slice:
            values.append(arr[(row+1)*length + i])
            indices.append((row+1)*length + i)

    return values, indices

def full_number(arr: str, index: int, length):
    """Get the full number from a schematic. Assumes index is the first digit"""
    num = ""
    while True:
        num += arr[index]
        index += 1
        if index % length == 0 or not is_number(arr[index]):
            break
    return int(num)

def is_number(element: str) -> bool:
    """Check whether the element is a number."""
    return element.isnumeric()

def is_symbol(element: str) -> bool:
    """Check whether the element is a 'symbol' i.e not a number nor dot."""
    return not element.isnumeric() and element != "."

def is_gear(element: str) -> bool:
    """Check whether the element is an asterix a.k.a. gear."""
    return element == '*'

def main():
    """Solve todays challenges."""
    schematic = read_input('./data/day_3_schematic.txt')
    width = len(schematic[0])  # Length of one row

    schematic_str = "".join(schematic)

    number_found = False  # Whether we have already found the number we're on
    number_start = 0
    is_counted = False  # Whether the current number has been counted
    total = 0
    for i, icon in enumerate(schematic_str):

        if is_number(icon) and is_counted:
            continue

        if not is_number(icon):
            number_found = False  # We are no longer on the same number
            is_counted = False
            continue

        if not number_found:
            number_start = i
            number_found = True
            n_total += 1

        if any(is_symbol(x) for x in nearest_neighbours(schematic_str, i, width)[0]):
            total += full_number(schematic_str, number_start, width)
            is_counted = True
    print(f"The sum of all part numbers in the engine schematic is {total}")

    # Part 2
    total = 0
    gear_box = {}  # Key is the index/location of a "*", value is a list of adjacent numbers
    for i, icon in enumerate(schematic_str):

        if not is_number(icon):
            number_found = False  # We are no longer on the same number
            adjacent_gears = set()
            continue

        if i % width == 0:  # New row
            number_found = False
            adjacent_gears = set()

        if not number_found:  # A new number has been found, note down its position
            number_start = i
            number_found = True
            adjacent_gears = set()  # Track all gears adjacent to this number to avoid repitition

        values, indices = nearest_neighbours(schematic_str, i, width)
        for j, val in enumerate(values):  # Check all adjacent elements for "*"
            if is_gear(val):
                if indices[j] not in adjacent_gears:
                    adjacent_gears.add(indices[j])
                    if indices[j] not in gear_box:  # If gear is completely new, add it to the box
                        gear_box[indices[j]] = []

                    gear_box[indices[j]].append(full_number(schematic_str, number_start, width))

    # Take all gears with exactly two adjacent part numbers, multiply the two
    # numbers and sum the results
    total = sum(math.prod(val) for val in gear_box.values() if len(val) == 2)
    print(f"The sum of all gear ratios in the engine schematic is {total}")


if __name__ == '__main__':
    main()
