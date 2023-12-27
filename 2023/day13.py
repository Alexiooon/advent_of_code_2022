"""Day 13 challenges."""
import numpy as np

def read_input(path):
    """Read the input data."""
    with open(path, 'r', encoding='utf8') as f:
        return f.read().splitlines()


def get_maps(data: list[str]) -> list[np.ndarray]:
    """Get a map of ashes, dusts and reflections."""
    reflections = []
    start = 0
    for i in range(len(data)):
        if not data[i]:  # Empty line
            reflections.append(np.array([list(row) for row in data[start:i]]))
            start = i+1
    reflections.append(np.array([list(row) for row in data[start:]]))
    return reflections


def rows_equal(_map: np.ndarray, row_1: int, row_2):
    """Determine whether two rows are equal."""
    return np.array_equal(_map[row_1,:], _map[row_2,:])


def rows_almost_equal(_map: np.ndarray, row_1: int, row_2):
    """Determine whether two rows are equal with a single change."""
    equal = sum(_map[row_1,i] == _map[row_2,i] for i in range(_map.shape[1]))
    return _map.shape[1] - equal == 1  # Exactly one element differs


def is_reflection(_map: np.ndarray, index: int):
    """Determine whether a line is perfectly reflected."""
    j = 0
    while 0 <= index-j and index + j + 1 < _map.shape[0]:
        if not rows_equal(_map, index-j, index+j+1):
            return False
        j += 1
    return True


def is_almost_reflection(_map: np.ndarray, index: int):
    """Determine whether a line is perfectly reflected if exactly one tile is changed."""
    smudge_detected = False
    j = 0
    while 0 <= index-j and index + j + 1 < _map.shape[0]:
        if not rows_equal(_map, index-j, index+j+1):
            if smudge_detected:  # Second time two rows are not equal
                return False
            smudge_detected = rows_almost_equal(_map, index-j, index+j+1)
            if not smudge_detected:  # Symmetry was not fixed with a single change
                return False
        j += 1
    return smudge_detected  # Only if we actually corrected something is it a reflection


def main():
    """Solve todays challenges."""
    full_data = read_input("./data/day_13_reflections.txt")
    reflections = get_maps(full_data)

    result = 0
    for _map in reflections:
        reflection_found = False

        for i in range(_map.shape[0]-1):
            if is_reflection(_map, i):
                result += 100*(i+1)
                reflection_found = True
                break

        for i in range(_map.shape[1]-1):
            if is_reflection(_map.T, i):
                result += i+1
                reflection_found = True
                break
        
        assert reflection_found
    print(f"The total number for all maps is {result}")

    # Part 2
    result = 0
    for _map in reflections:
        reflection_found = False

        for i in range(_map.shape[0]-1):
            if is_almost_reflection(_map, i):
                result += 100*(i+1)
                reflection_found = True
                break

        for i in range(_map.shape[1]-1):
            if is_almost_reflection(_map.T, i):
                result += i+1
                reflection_found = True
                break
        
        assert reflection_found
    print(f"The total number for all maps with corrections is {result}")


if __name__ == '__main__':
    main()
