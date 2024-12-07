"""Day 4 solutions."""
# ruff: noqa: E226 for this one I think the whitespace hurts more than it helps

DATA_PATH = "./data/day4_words.txt"
LENGTH = 140  # Line length
KEY_WORD = "XMAS"


def read_input(path):
    """Read the input data."""
    with open(path, 'r', encoding='utf8') as f:
        return "".join(f.read().splitlines())


def _crosses_boundary(indexes: list[int]) -> bool:
    """Checks whether a set of indexes crosses the boundary of an array."""
    if any(x < 0 for x in indexes):
        return True
    if any(x % LENGTH <= 1 for x in indexes) and any(x % LENGTH >= LENGTH - 2 for x in indexes):
        return True
    if any(x >= LENGTH**2 for x in indexes):
        return True

    return False


def check_word(data: str, indexes: list[int]) -> bool:
    """Check for key word."""
    if _crosses_boundary(indexes):
        return False

    data_slice = "".join([data[i] for i in indexes])
    if data_slice == KEY_WORD:
        return True

    return False


def is_x_mas(data: str, indexes: list[int]) -> bool:
    """Determines if a set of indexes create an X-'mas'."""
    if _crosses_boundary(indexes):
        return False
    diag_string = "".join([data[i] for i in indexes])  # String of all 4 letters
    return diag_string in {"MMSS", "SMMS", "SSMM", "MSSM"}


def main():
    """Solve today's puzzles."""
    data = read_input(DATA_PATH)

    i = 0
    xmas_counter = [0] * 8
    while i < len(data):
        search_index = data[i:].find("X")
        if search_index == -1:
            break  # Reached the end
        i += search_index

        xmas_counter[0] += check_word(data, [i, i+1, i+2, i+3])  # Horizontal forward
        xmas_counter[1] += check_word(data, [i, i-1, i-2, i-3])  # Horizontal backwards
        xmas_counter[2] += check_word(data, [i, i+LENGTH, i+2*LENGTH, i+3*LENGTH])  # Vertical down
        xmas_counter[3] += check_word(data, [i, i-LENGTH, i-2*LENGTH, i-3*LENGTH])  # Vertical up
        xmas_counter[4] += check_word(data, [i, i+(LENGTH+1), i+2*(LENGTH+1), i+3*(LENGTH+1)])
        xmas_counter[5] += check_word(data, [i, i+(LENGTH-1), i+2*(LENGTH-1), i+3*(LENGTH-1)])
        xmas_counter[6] += check_word(data, [i, i-(LENGTH+1), i-2*(LENGTH+1), i-3*(LENGTH+1)])
        xmas_counter[7] += check_word(data, [i, i-(LENGTH-1), i-2*(LENGTH-1), i-3*(LENGTH-1)])
        i += 1

    print(f"There are {sum(xmas_counter)} '{KEY_WORD}' in the puzzle")

    # Part 2
    # So we search for 'A' instead since that's the centerpiece
    i = 0
    x_mas_counter = 0
    while i < len(data):
        search_index = data[i:].find("A")
        if search_index == -1:
            break  # Reached the end
        i += search_index

        indexes = [i+LENGTH+1, i+LENGTH-1, i-LENGTH-1, i-LENGTH+1]
        x_mas_counter += is_x_mas(data, indexes)
        i += 1
    print(f"There are {x_mas_counter} 'cross-MAS' in the puzzle")


if __name__ == "__main__":
    main()
