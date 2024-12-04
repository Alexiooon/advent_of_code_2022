"""Day 1 solutions."""

DATA_PATH = "./data/day1_locations.txt"


def read_input(path):
    """Read the input data."""
    with open(path, 'r', encoding='utf8') as f:
        return f.read().splitlines()


def main():
    """Solve today's puzzles."""
    data = read_input(DATA_PATH)
    
    # Re-organize into something a bit nicer to work with
    col0 = []
    col1 = []
    for i, line in enumerate(data):
        x0, x1 = line.split("   ")
        col0.append(int(x0))
        col1.append(int(x1))
    
    # Solve it
    col0.sort()
    col1.sort()

    dist = sum(abs(col0[i] - col1[i]) for i in range(len(data)))
    print(f"The total distance between the lists is {dist}")

    # Part 2:
    # Don't think it matters that we sorted them, only need to count the elements
    sim_score = 0
    for x in col0:
        sim_score += x * col1.count(x)
    print(f"The total similarity score the lists is {sim_score}")


if __name__ == "__main__":
    main()
