"""Day 3 solutions."""

DATA_PATH = "./data/day3_memory.txt"


def read_input(path):
    """Read the input data."""
    with open(path, 'r', encoding='utf8') as f:
        return f.read()


def find_many(string: str, sub: list[str]) -> int:
    """Search for multiple strings at once and return lowest index."""
    try:
        return min(string.find(s) for s in sub if string.find(s) >= 0)
    except ValueError:
        return -1


def main():
    """Solve today's puzzles."""
    memory = read_input(DATA_PATH)
    sum_num = 0
    conditional_sum_num = 0  # Part 2 answer

    # Search for first part
    substring = "mul("
    enable_string = "do()"
    disable_string = "don't()"
    is_enabled = True
    i = 0
    while i < len(memory):
        # Find the next function and parse
        search_idx = find_many(memory[i:], [substring, enable_string, disable_string])
        if search_idx == -1:
            break  # Reached the end

        i += search_idx
        if memory[i:i + 3] == "do(":
            is_enabled = True
            i += 1
            continue
        elif memory[i:i + 3] == "don":
            is_enabled = False
            i += 1
            continue

        close_bracket = i + memory[i:].find(")")
        mem_range = memory[i + 4:close_bracket]
        try:
            factors = mem_range.split(",")
            assert all(len(x) < 4 for x in factors)
            assert len(factors) == 2
            factors = [int(x) for x in factors]
            sum_num += int(factors[0]) * int(factors[1])
            if is_enabled:
                conditional_sum_num += int(factors[0]) * int(factors[1])
        except (ValueError, IndexError, AssertionError):
            pass
        i += 1

    print(f"Sum of products: {sum_num}")
    print(f"Sum of products with do/don't conditions: {conditional_sum_num}")


if __name__ == "__main__":
    main()
