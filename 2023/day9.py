"""Day 7 challenges."""


def read_input(path):
    """Read the input data."""
    with open(path, 'r', encoding='utf8') as f:
        return f.read().splitlines()


def get_numbers(number_str: str) -> list[int]:
    """Returns a list of numbers from a string of space-separated numbers."""
    return [int(x) for x in number_str.split(" ") if x]  # Filter out empty strings


def get_differences(sequence: list[int]) -> list[int]:
    """Get a list of differences between adjacent elements of a list."""
    return [sequence[i] - sequence[i-1] for i in range(1, len(sequence))]


def main():
    """Solve todays challenges."""
    full_data = read_input("./data/day_9_sequences.txt")
    parsed_data = [get_numbers(line) for line in full_data]

    extrapolated_value_sum_forward = 0
    extrapolated_value_sum_backward = 0
    for line in parsed_data:
        new_line = line.copy()
        last_elements = [new_line[-1]]  # List of all the first elements for each iteration
        first_elements = [new_line[0]]  # List of all the final elements for each iteration
        while any(new_line):  # While any element is non-zero
            new_line = get_differences(new_line)
            last_elements.append(new_line[-1])
            first_elements.append(new_line[0])
        extrapolated_value_sum_forward += sum(last_elements)
        extrapolated_value_sum_backward += sum(first_elements[i]*(-1)**(i)
                                               for i in range(len(first_elements)))
    print(f"The sum of all extrapolated values forward is {extrapolated_value_sum_forward}")
    print(f"The sum of all extrapolated values backward is {extrapolated_value_sum_backward}")


if __name__ == '__main__':
    main()
