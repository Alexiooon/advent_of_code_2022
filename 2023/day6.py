"""Day 6 challenges."""

import math

def read_input(path):
    """Read the input data."""
    with open(path, 'r', encoding='utf8') as f:
        return f.read().splitlines()


def get_numbers(number_str: str) -> list[int]:
    """Returns a list of numbers from a string of space-separated numbers."""
    return [int(x) for x in number_str.split(" ") if x]  # Filter out empty strings


def calc_roots(tau: int, s: int):
    """Calculate the two roots where the time button is held matches the record."""
    t1 = tau/2 + math.sqrt(tau**2/4 - s)
    t2 = tau/2 - math.sqrt(tau**2/4 - s)
    return t1, t2


def main():
    """Solve todays challenges."""
    full_data = read_input("./data/day_6_boat_races.txt")

    # Part 1
    times = get_numbers(full_data[0].split(":")[1])
    records = get_numbers(full_data[1].split(":")[1])
    n_races = len(times)
    product = 1
    for i in range(n_races):
        t1, t2 = calc_roots(times[i], records[i])
        product *= math.floor(t1) - math.floor(t2)

    # Part 2
    # Combine all races into one big number
    tot_time = int("".join(str(x) for x in times))
    tot_record = int("".join(str(x) for x in records))
    print(f"The product of all ways to win is {product}")

    # Calculate the roots
    t1, t2 = calc_roots(tot_time, tot_record)
    possibilities = math.floor(t1) - math.floor(t2)
    print(f"The amount of ways to win the single big race is {possibilities}")

if __name__ == '__main__':
    main()
