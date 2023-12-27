"""Day 15 challenges."""


def read_input(path):
    """Read the input data."""
    with open(path, 'r', encoding='utf8') as f:
        return f.read().splitlines()


def hash(string: str):
    """Hash a string."""
    hash_val = 0
    for char in string:
        hash_val += ord(char)
        hash_val *= 17
        hash_val %= 256
    return hash_val


class Lens():
    """A lens."""

    def __init__(self, label: str, focal_length: int):
        """Init."""
        self.label = label
        self.focal_length = focal_length

    def __str__(self) -> str:
        return self.label


class LensBoxes():
    """An arrangement of 256 lens boxes."""

    def __init__(self) -> None:
        """Init."""
        self.boxes = [[] for _ in range(256)]

    def _lens_index(self, box: int, label: str) -> int:
        """Search for a specific lens in a box, returning its index or -1 if not found."""
        for i, lens in enumerate(self.boxes[box]):
            if str(lens) == label:
                return i
        return -1

    def add_lens(self, box: int, label: str, focal_length: int) -> None:
        """Add a lens to a given box, or replace it if one with the same label already exists."""
        idx = self._lens_index(box, label)
        if idx != -1:
            self.boxes[box][idx].focal_length = focal_length
        else:
            self.boxes[box].append(Lens(label, focal_length))

    def remove_lens(self, box: int, label: str):
        """Remove a lens from a given box."""
        idx = self._lens_index(box, label)
        if idx != -1:
            self.boxes[box].pop(idx)

    def calc_focusing_power(self):
        """Calculate and return the focusing power of the current lens configuration."""
        tot_focusing_power = 0
        for i, box in enumerate(self.boxes):
            for j, lens in enumerate(box):
                tot_focusing_power += (i+1) * (j+1) * lens.focal_length
        return tot_focusing_power


def main():
    """Solve todays challenges."""
    full_data = read_input("./data/day_15_initialization_sequence.txt")[0]
    parsed_data = full_data.split(",")

    # Part 1
    tot_val = 0
    for string in parsed_data:
        tot_val += hash(string)
    print(f"The sum of the results is {tot_val}")

    # Part 2
    lens_boxes = LensBoxes()
    for string in parsed_data:
        if "=" in string:
            label = string[:string.index("=")]
            box = hash(label)
            focal_length = int(string[-1])
            lens_boxes.add_lens(box, label, focal_length)
        elif "-" in string:
            label = string[:string.index("-")]
            box = hash(label)
            lens_boxes.remove_lens(box, label)
    focusing_power = lens_boxes.calc_focusing_power()
    print(f"The total focusing power with this lens configuration is {focusing_power}")


if __name__ == '__main__':
    main()
