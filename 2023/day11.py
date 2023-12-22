"""Day 11 challenges."""
import numpy as np

def read_input(path):
    """Read the input data."""
    with open(path, 'r', encoding='utf8') as f:
        return f.read().splitlines()


def expand_universe(universe: np.ndarray):
    """Return an expanded copy of the universe."""
    i = 0
    empty_rows = []
    while i < universe.shape[0]:
        row = universe[i,:]
        if "#" not in row:
            empty_rows.append(i)
        i += 1
    print(empty_rows)

    j = 0
    empty_cols = []
    while j < universe.shape[1]:
        col = universe[:,j]
        if "#" not in col:
            empty_cols.append(j)
        j += 1
    print(empty_cols)


def calc_distance(galaxy_1: tuple[int, int], galaxy_2: tuple[int, int]) -> int:
    """Calcualte the distance between two galaxies."""
    base_distance = abs(galaxy_1[0] - galaxy_2[0]) + abs(galaxy_1[1] - galaxy_2[1])
    # Calculate the extra distance due to expansion
    return base_distance


class Universe():
    """The observable universe (or well, what has been mapped in this observatory)."""

    def __init__(self, starmap: list[str]) -> None:
        self.starmap = np.array([list(row) for row in starmap])
        self.galaxies = []  # List of coordinates for all galaxies
        self.empty_rows = []
        self.empty_cols = []

    def expand(self) -> None:
        """Create and store lists of empty rows and columns."""
        i = 0
        while i < self.starmap.shape[0]:
            row = self.starmap[i,:]
            if "#" not in row:
                self.empty_rows.append(i)
            i += 1

        j = 0
        while j < self.starmap.shape[1]:
            col = self.starmap[:,j]
            if "#" not in col:
                self.empty_cols.append(j)
            j += 1

    def find_galaxies(self):
        """Find all galaxies in the observed universe."""
        galaxies = []
        return galaxies


    def calc_distance(self, galaxy_1: tuple[int, int], galaxy_2: tuple[int, int]) -> int:
        """Calcualte the distance between two galaxies."""
        distance = abs(galaxy_1[0] - galaxy_2[0]) + abs(galaxy_1[1] - galaxy_2[1])

        # Add expansion
        min_y = min(galaxy_1[0], galaxy_2[0])
        max_y = max(galaxy_1[0], galaxy_2[0])
        min_x = min(galaxy_1[1], galaxy_2[1])
        max_x = max(galaxy_1[1], galaxy_2[1])
        distance += len(y for y in self.empty_rows if min_y < y < max_y)
        distance += len(x for x in self.empty_cols if min_x < x < max_x)
        return distance


def main():
    """Solve todays challenges."""
    full_data = read_input("./data/day_11_universe.txt")
    universe = Universe(full_data)
    universe.expand()
    galaxies = universe.find_galaxies()
    for row in full_data:
        galaxies += row.count("#")
    print(galaxies)
    print(f"Distances to count: {int(galaxies*(galaxies-1)/2)}")

if __name__ == '__main__':
    main()
