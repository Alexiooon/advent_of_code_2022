"""Common functionality for multiple puzzles."""

from operator import add


def get_neighbours(coords: tuple[int, int], size: int) -> list[tuple[int, int]]:
    """Takes a set of (x,y) coordinates and returns a list of its neighbours."""
    def _is_inside(pos: tuple[int, int]) -> bool:
        """Determines whether a coordinate is within the map."""
        return (0 <= pos[0] < size) and (0 <= pos[1] < size)

    adjacencies = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    new_coords = [tuple(map(add, coords, step)) for step in adjacencies]

    return [coord for coord in new_coords if _is_inside(coord)]
