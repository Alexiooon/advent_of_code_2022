"""Day 14 challenges."""
import numpy as np

def read_input(path):
    """Read the input data."""
    with open(path, 'r', encoding='utf8') as f:
        return f.read().splitlines()


class Platform():
    """Large platforms with rouch and cubic rocks on it."""

    def __init__(self, dish: list[str]) -> None:
        self.dish = np.array([list(row) for row in dish])
        self.rows, self.cols = self.dish.shape

    def _swap_locations(self, row1, col1, row2, col2):
        """Swamp the elements of two positions."""
        self.dish[row1, col1], self.dish[row2, col2] = self.dish[row2, col2], self.dish[row1, col1]

    def tilt_north(self):
        """Send all the round rocks as far north as possible."""
        for _ in range(1, self.rows):
            for row in range(1, self.rows):
                for col in range(self.cols):
                    if self.dish[row, col] == "O" and self.dish[row-1, col] == ".":
                        self._swap_locations(row, col, row-1, col)

    def tilt_west(self):
        """Send all the round rocks as far west as possible."""
        self.dish = np.rot90(np.rot90(np.rot90(self.dish)))  # Rotate 90 degrees clockwise
        self.tilt_north()
        self.dish = np.rot90(self.dish)  # Return to normal

    def tilt_south(self):
        """Send all the round rocks as far south as possible."""
        self.dish = np.rot90(np.rot90(self.dish))  # Rotate 180 degrees
        self.tilt_north()
        self.dish = np.rot90(np.rot90(self.dish))  # Return to normal

    def tilt_east(self):
        """Send all the round rocks as far east as possible."""
        self.dish = np.rot90(self.dish)  # Rotate 90 degrees counter clockwise
        self.tilt_north()
        self.dish = np.rot90(np.rot90(np.rot90(self.dish)))  # Return to normal

    def spin(self):
        """Spin the platform right round (like a record)."""
        self.tilt_north()
        self.tilt_west()
        self.tilt_south()
        self.tilt_east()

    def calc_load(self) -> int:
        """Calculate the current load on the platform."""
        total_load = 0
        for row in range(self.rows):
            load = self.rows - row  # Load counted from bottom to top
            total_load += load * len(np.where(self.dish[row,:] == "O")[0])
        return total_load

    def update_rock_coordinates(self):
        """Get all the coordinates of rocks"""
        return np.where(self.dish == "O")


def coords_exist(coordinates, new_coords):
    """Determine whether the coordinates have already been explored."""
    for i, coords in enumerate(coordinates):
        if all(np.equal(coords[0], new_coords[0])) and all(np.equal(coords[1], new_coords[1])):
            return i
    return -1

def main():
    """Solve todays challenges."""
    full_data = read_input("./data/day_14_rocks.txt")
    platform = Platform(full_data)
    platform.tilt_north()
    load = platform.calc_load()
    print(f"The total load on the platform after tilting it north is {load}")

    # Part 2
    # Find a periodicity in the layout after a cycle. Once we've found that, we the remaining cycles
    # is within that.
    n_cycles = 1000000000  # Small sample
    rock_coordinates = []
    for i in range(n_cycles):
        platform.spin()
        new_coords = platform.update_rock_coordinates()
        match_idx = coords_exist(rock_coordinates, new_coords)
        if  match_idx != -1:
            diff = i - match_idx
            remaining_iters = n_cycles - i - 1
            load = platform.calc_load()
            break
        rock_coordinates.append(new_coords)
    print(f"Layout repeats every {diff} cycles, and we have {remaining_iters} cycles left to")

    cycle_offset = remaining_iters % diff
    for _ in range(cycle_offset):
        platform.spin()
    final_load = platform.calc_load()
    print(f"After {n_cycles} cycles, the total load on the northern beam is {final_load}")
    # Not completely happy with the solution as it is very slow (takes multiple minutes)
    # I have multiple ideas to improve it, mostly focusing on the "tilt" algorithm which is slowest.
    # However, probably wont implement them.

if __name__ == '__main__':
    main()
