"""Day 11 challenges."""
import numpy as np

def read_input(path):
    """Read the input data."""
    with open(path, 'r', encoding='utf8') as f:
        return f.read().splitlines()


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
        for i in range(self.starmap.shape[0]):
            for j in range(self.starmap.shape[1]):
                if self.starmap[i,j] == "#":
                    galaxies.append((i,j))
        return galaxies


    def calc_distance(self, galaxy_1: tuple[int, int], galaxy_2: tuple[int, int],
                      expansion_factor: int) -> int:
        """Calcualte the distance between two galaxies."""
        distance = abs(galaxy_1[0] - galaxy_2[0]) + abs(galaxy_1[1] - galaxy_2[1])

        # Add expansion
        min_y = min(galaxy_1[0], galaxy_2[0])
        max_y = max(galaxy_1[0], galaxy_2[0])
        min_x = min(galaxy_1[1], galaxy_2[1])
        max_x = max(galaxy_1[1], galaxy_2[1])
        distance += len([y for y in self.empty_rows if min_y < y < max_y])*(expansion_factor-1)
        distance += len([x for x in self.empty_cols if min_x < x < max_x])*(expansion_factor-1)
        return distance


def main():
    """Solve todays challenges."""
    full_data = read_input("./data/day_11_universe.txt")
    universe = Universe(full_data)
    universe.expand()
    galaxies = universe.find_galaxies()
    tot_dist = 0
    tot_big_dist = 0
    for i in range(len(galaxies)-1):
        for j in range(i+1, len(galaxies)):
            tot_dist += universe.calc_distance(galaxies[i], galaxies[j], expansion_factor=2)
            tot_big_dist += universe.calc_distance(galaxies[i], galaxies[j],
                                                   expansion_factor=1000000)
    print(f"Sum of distances between galaxies in expanded universe: {tot_dist}")
    print(f"Sum of distances between galaxies in very big expanded universe: {tot_big_dist}")

if __name__ == '__main__':
    main()
