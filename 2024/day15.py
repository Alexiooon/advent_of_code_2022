"""Day 15 solutions."""

from operator import add

DATA_PATH = "./data/day15.txt"
WALL = "#"
BOX = "O"
WIDEBOX_LEFT = "["
WIDEBOX_RIGHT = "]"
ROBOT = "@"
SPACE = "."

MOVE_UP = "^"
MOVE_DOWN = "v"
MOVE_LEFT = "<"
MOVE_RIGHT = ">"

ADJACENCIES = {  # Only the four cardinal directions are considered adjacent
    MOVE_RIGHT: (0, 1),
    MOVE_DOWN: (1, 0),
    MOVE_LEFT: (0, -1),
    MOVE_UP: (-1, 0)
}


class RobotMalfunctionError(BaseException):
    """Custom error class for warehouse robot shenanigans."""


class Warehouse():
    """Warehouse full of food and a robot running amok."""

    def __init__(self, warehouse_map: list[str]):
        """Starting map."""
        self._map = [list(x) for x in warehouse_map]

        # Find the robot
        self._robot = None
        for i, row in enumerate(self._map):
            for j, val in enumerate(row):
                if val == ROBOT:
                    self._robot = (i, j)
                    break
            if self._robot:
                break

    def move(self, instruction: str):
        """Move the robot one step and update the map."""
        pos = self._robot
        row, col = tuple(map(add, pos, ADJACENCIES[instruction]))  # Candidate position

        next_space = self._check_for_blockage(pos, instruction)

        # Cannot move
        if not next_space:
            return

        # Pushing some boxes
        if next_space != (row, col):
            self._map[next_space[0]][next_space[1]] = BOX

        # Move the robot
        self._map[row][col] = ROBOT
        self._robot = (row, col)
        self._map[pos[0]][pos[1]] = SPACE

    def _check_for_blockage(self, pos: tuple[int, int], instruction: str) -> tuple[int, int] | None:
        """Return the next unoccupied tile in a line, or None if no such space exists."""
        row, col = tuple(map(add, pos, ADJACENCIES[instruction]))

        content = self._map[row][col]
        if content == WALL:
            return None
        if content == BOX:  # Recursion babyyyy
            return self._check_for_blockage((row, col), instruction)
        if content == SPACE:
            return row, col
        raise RobotMalfunctionError("Robot does not seem to play by the rules. Bad robot!")

    def get_robot(self) -> tuple[int, int]:
        """Get the robots current coordinates."""
        return self._robot

    def get_boxes(self) -> list[tuple[int, int]]:
        """Return a list of all boxes."""
        boxes = []
        for i, row in enumerate(self._map):
            for j, val in enumerate(row):
                if val == BOX:
                    boxes.append((i, j))
        return boxes

    def print_map(self, size: int = 3):
        """Print the map close to the robot."""
        y, x = self._robot
        try:
            for row in self._map[y - size : y + size + 1]:
                print("".join(row[x - size : x + size + 1]))
        except IndexError:
            print("Robot is too close to the edge and I can't bother handling this")


class WideWarehouse(Warehouse):
    """W I D E   W A R E H O U S E ."""

    def __init__(self, warehouse_map: list[list[str]]):
        """Starting map."""
        # Expand the map
        self._map = []
        for row in warehouse_map:
            wide_row = ""
            for val in row:
                if val == WALL:
                    wide_row += WALL + WALL
                elif val == BOX:
                    wide_row += WIDEBOX_LEFT + WIDEBOX_RIGHT
                elif val == SPACE:
                    wide_row += SPACE + SPACE
                elif val == ROBOT:
                    wide_row += ROBOT + SPACE
            self._map.append(list(wide_row))

        # Find the robot
        self._robot = None
        for i, row in enumerate(self._map):
            for j, val in enumerate(row):
                if val == ROBOT:
                    self._robot = (i, j)
                    break
            if self._robot:
                break

    def move(self, instruction: str):
        """Move the robot one step and update the map."""
        pos = self._robot
        row, col = tuple(map(add, pos, ADJACENCIES[instruction]))  # Candidate position for robot
        end_coords = self._check_for_blockage(pos, instruction)

        # Cannot move if there is any blockage
        if any(coord is None for coord in end_coords):
            return

        # Handle the complicated case of pushing boxes
        end_coords = list(set(end_coords))  # Handle any duplicate coordinates
        self._sort(end_coords, instruction)
        self._push(end_coords, instruction)
        self._robot = (row, col)

    @staticmethod
    def _sort(positions: list, instruction: str) -> None:
        """Sort a list of positions according to a movement instruction.

        Sorting appropriately ensures that boxes can be moved by swapping content between
        tiles iteratively.
        """
        if instruction == MOVE_UP:
            positions.sort()
        elif instruction == MOVE_DOWN:
            positions.sort()
            positions.reverse()
        elif instruction == MOVE_LEFT:
            positions.sort(key=lambda x: x[1])
        elif instruction == MOVE_RIGHT:
            positions.sort(key=lambda x: x[1])
            positions.reverse()

    def _push(self, sorted_positions: list, direction: str) -> None:
        """Push blocks in specified direction, assuming they're sorted correctly."""
        # Inverse direction
        if direction == MOVE_UP:
            inverse_direction = MOVE_DOWN
        if direction == MOVE_DOWN:
            inverse_direction = MOVE_UP
        if direction == MOVE_RIGHT:
            inverse_direction = MOVE_LEFT
        if direction == MOVE_LEFT:
            inverse_direction = MOVE_RIGHT

        # Move all boxes
        for tile in sorted_positions:
            tile_y, tile_x = tile
            orig_y, orig_x = tuple(map(add, tile, ADJACENCIES[inverse_direction]))
            self._map[tile_y][tile_x], self._map[orig_y][orig_x], = \
                self._map[orig_y][orig_x], self._map[tile_y][tile_x]

    def _check_for_blockage(self, pos: tuple[int, int], instruction: str) -> list:
        """Recursively check for coordinates, returning a list of all free spaces at the end."""
        row, col = tuple(map(add, pos, ADJACENCIES[instruction]))
        new_coords = [(row, col)]
        content = self._map[row][col]
        if content == WALL:
            return [None]

        if content == SPACE:
            return new_coords

        if content == WIDEBOX_LEFT:
            if instruction in {MOVE_DOWN, MOVE_UP}:  # Might push multiple boxes
                row_2, col_2 = tuple(map(add, (row, col), ADJACENCIES[MOVE_RIGHT]))
                new_coords.extend(self._check_for_blockage((row_2, col_2), instruction))
            new_coords.extend(self._check_for_blockage((row, col), instruction))

        if content == WIDEBOX_RIGHT:
            if instruction in {MOVE_DOWN, MOVE_UP}:  # Might push multiple boxes
                row_2, col_2 = tuple(map(add, (row, col), ADJACENCIES[MOVE_LEFT]))
                new_coords.extend(self._check_for_blockage((row_2, col_2), instruction))
            new_coords.extend(self._check_for_blockage((row, col), instruction))

        return new_coords

    def get_boxes(self) -> list[tuple[int, int]]:
        """Return a list of all wide boxes."""
        boxes = []
        for i, row in enumerate(self._map):
            for j, val in enumerate(row):
                if val == WIDEBOX_LEFT:
                    boxes.append((i, j))
        return boxes


def _load(path: str) -> str:
    """Load input data."""
    with open(path, "r", encoding="utf8") as f:
        return f.read()


def format_input(data: str):
    """Format the input data to a more appropriate format."""
    data = data.splitlines()

    i = 0
    while True:
        if not data[i]:  # Empty row i.e. split between map and instructions
            break
        i += 1
    warehouse_map = data[:i]
    instructions = "".join(data[i + 1:])

    return warehouse_map, instructions


def solve():
    """Solve todays puzzles."""
    warehouse_map, instructions = format_input(_load(DATA_PATH))
    warehouse = Warehouse(warehouse_map)

    # Move for all intended instructions
    for instr in instructions:
        warehouse.move(instr)

    # Calculate the solution
    gps_coordinate_sum = 0
    for box in warehouse.get_boxes():
        gps_coordinate_sum += 100 * box[0] + box[1]
    print(f"The sum of GPS coordinates for all boxes is {gps_coordinate_sum}")

    # Part 2: Same thing, wider warehouse
    wide_warehouse = WideWarehouse(warehouse_map)

    # Move for all intended instructions
    for instr in instructions:
        wide_warehouse.move(instr)

    # Calculate the solution again
    gps_coordinate_sum = 0
    for box in wide_warehouse.get_boxes():
        gps_coordinate_sum += 100 * box[0] + box[1]
    print(f"The sum of GPS coordinates in the second warehouse is {gps_coordinate_sum}")


if __name__ == "__main__":
    solve()
