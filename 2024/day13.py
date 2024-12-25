"""Day 13 solutions."""

from operator import add

DATA_PATH = "./data/day13_arcade.txt"
COST = {
    "A": 3,
    "B": 1
}
DIM = 2  # We're working in 2 dimensions here
BUFFER = 10000000000000  # Part 2 stuff


def _load(path: str) -> str:
    """Load input data."""
    with open(path, "r", encoding="utf8") as f:
        return f.read()


def format_input(path: str) -> list[dict]:
    """Format the input data to a more appropriate format."""
    data = _load(path).splitlines()

    machines = []
    for i in range(0, len(data), 4):
        new_machine = {
            "A": tuple(int(j[2:]) for j in data[i].split("Button A: ")[1].split(", ")),
            "B": tuple(int(j[2:]) for j in data[i + 1].split("Button B: ")[1].split(", ")),
            "Prize": tuple(int(j[2:]) for j in data[i + 2].split("Prize: ")[1].split(", ")),
            "P2": tuple(int(j[2:]) + BUFFER for j in data[i + 2].split("Prize: ")[1].split(", "))
        }
        machines.append(new_machine)
    return machines


def is_equal(iterable: list) -> bool:
    """Return whether all elements in a list are equal."""
    return len(set(iterable)) <= 1


def main():
    """Solve todays puzzles."""
    total_cost = 0

    for machine in DATA:
        a_button = machine["A"]
        b_button = machine["B"]
        prize = machine["Prize"]
        current = [0, 0]
        a_presses = 0
        while all(current[i] < prize[i] for i in range(DIM)):
            remaining = [prize[0] - current[0], prize[1] - current[1]]
            if is_equal(remaining[i] / b_button[i] for i in range(DIM)):
                total_cost += COST["A"] * a_presses + COST["B"] * (remaining[0] / b_button[0])
                break
            current = list(map(add, current, a_button))
            a_presses += 1
    print(f"Total cost is: {int(total_cost)}")

    # Part 2, need to work smarter.
    # Finding the remainder (modulo) of a large number is fast, and the principle still remains that
    # we want to minimize the number of A presses while still reaching the price. So we check
    # Prize % B button, to find the remainders in both X and Y coordinates. Then, starting from 0,
    # we check each multiple of A-button presses that yields the same modulo. If we find a valid
    # candidate we can just exit and calculate the cost. If we find a repitition in the loop it
    # means we will never find a valid candidate.
    #
    # Proof is left as an exercise to the reader :^)
    total_cost = 0
    for machine_number, machine in enumerate(DATA):
        a_button = machine["A"]
        b_button = machine["B"]
        prize = machine["P2"]
        print()
        print(a_button)
        print(b_button)
        print(prize)

        # Find the frequency
        modulo_freq = 0
        modulooo = [prize[i] % b_button[i] for i in range(DIM)]
        for a_presses in range(300000):  # Arbitary big number
            if [(a_button[j] * a_presses) % b_button[j] for j in range(DIM)] == modulooo:
                remaining = [prize[i] - a_presses * a_button[i] for i in range(DIM)]

                if modulo_freq:
                    modulo_freq = a_presses - modulo_freq
                    break
                modulo_freq = a_presses

        # Find the AB-ratio
        diff_prize = prize[1] - prize[0]
        diff_button = [a_button[1] - a_button[0], b_button[1] - b_button[0]]

        print(diff_prize)
        print(diff_button)
        break

    print(f"Total cost is: {int(total_cost)}")


if __name__ == "__main__":
    DATA = format_input(DATA_PATH)
    main()
