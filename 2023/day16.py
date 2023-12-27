"""Day 16 challenges."""
import sys
import time

import numpy as np

sys.setrecursionlimit(5000)

def read_input(path):
    """Read the input data."""
    with open(path, 'r', encoding='utf8') as f:
        return f.read().splitlines()


class MirrorContraption():
    """A contraption of mirrors and splitters.
    
    Directions are defined as follows:
        0 - From left to right
        1 - From top to bottom
        2 - From right to left
        3 - From bottom to top
    """

    reflection_lookup = {
        "0.":  [0],
        "1.":  [1],
        "2.":  [2],
        "3.":  [3],
        "0/":  [3],
        "1/":  [2],
        "2/":  [1],
        "3/":  [0],
        "0\\": [1],
        "1\\": [0],
        "2\\": [3],
        "3\\": [2],
        "0-":  [0],
        "1-":  [0, 2],
        "2-":  [2],
        "3-":  [0, 2],
        "0|":  [1, 3],
        "1|":  [1],
        "2|":  [1, 3],
        "3|":  [3],
    }

    def __init__(self, grid: list[str]) -> None:
        self.grid = np.array([list(row) for row in grid])
        self.energized = np.zeros_like(self.grid)

    def calc_reflection(self, position, direction) -> list:
        """Return a list of directions a beam will travel out from a tile."""
        tile = self.grid[position]
        key = str(direction) + tile
        return self.reflection_lookup[key]

    def _out_of_bounds(self, position):
        """Return a bool stating whether the given position is within the grid"""
        return not (0 <= position[0] < self.grid.shape[0] and 0 <= position[1] < self.grid.shape[1])


    def send_beam(self, start, direction):
        """Send a beam in a specified direction."""
        if self._out_of_bounds(start):
            return
        row, col = start
        i = 0

        # Check if its already energized in this direction
        if str(direction) in self.energized[start]:
            return  # No need to follow this path again
        self.energized[start] += str(direction)

        while True:
            next_position = {
                0: (row, col+i), 1: (row+i, col), 2: (row, col-i), 3: (row-i, col)
            }[direction]
            # print()
            # print(next_position)
            if self._out_of_bounds(next_position):
                # print("OOB")
                beams = []
                break
            beams =  self.calc_reflection(next_position, direction)

            if str(direction) in self.energized[next_position]:
                break  # No need to follow this path again
            self.energized[next_position] += str(direction)

            if direction not in beams:
                break
            i+=1

        # Handle any and all subsequent beams
        for new_direction in beams:
            row, col = next_position
            # Get the first position after the reflection, start from there
            next_position = {
                0: (row, col+1), 1: (row+1, col), 2: (row, col-1), 3: (row-1, col)
            }[new_direction]
            self.send_beam(next_position, new_direction)

    def get_energy(self):
        """Get the energy of the current layout."""
        return len(np.where(self.energized != "")[0])

    def reset(self):
        """Reset all beams and set the energy to 0."""
        self.energized = np.zeros_like(self.grid)


def main():
    """Solve todays challenges."""
    full_data = read_input("./data/day_16_contraption.txt")

    t_start = time.time()
    contraption = MirrorContraption(full_data)

    energies = []
    rows = contraption.grid.shape[0]
    for i in range(rows):
        contraption.send_beam((i,0), 0)
        energies.append(contraption.get_energy())
        contraption.reset()

        contraption.send_beam((i, rows-1), 2)
        energies.append(contraption.get_energy())
        contraption.reset()

    cols = contraption.grid.shape[1]
    for j in range(cols):
        contraption.send_beam((0,j), 1)
        energies.append(contraption.get_energy())
        contraption.reset()

        contraption.send_beam((cols-1, j), 3)
        energies.append(contraption.get_energy())
        contraption.reset()
    
    print(f"The total amount of energized tiles if sending the beam right from top-right corner is {energies[0]}")
    print(f"The total amount of energized tiles if sending the beam right from top-right corner is {max(energies)}")

if __name__ == '__main__':
    main()
