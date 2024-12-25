"""Day 14 solutions."""

from collections import Counter
from math import floor, prod
from operator import add

DATA_PATH = "./data/day14_robots.txt"
WIDTH = 101
HEIGHT = 103
MIDPOINT_WIDTH = floor(WIDTH / 2)
MIDPOINT_HEIGHT = floor(HEIGHT / 2)
TIME = 100
EASTER_EGG_LIMIT = 0.30


class Robot():
    """Teleporting, springing, and moving robot."""

    def __init__(self, position: tuple[int, int], velocity: tuple[int, int]):
        """Spawn a new robot with a set position and velocity."""
        self.position = position
        self.velocity = velocity

    def move(self):
        """Move the robot one step and update its coordinates."""
        self.position = tuple(map(add, self.position, self.velocity))
        x, y = self.position  # Easier to work with shorter names
        x -= floor(x / WIDTH) * WIDTH  # Map to within boundaries
        y -= floor(y / HEIGHT) * HEIGHT
        self.position = (x, y)

    def get_quadrant(self):
        """Get the quadrant the robot is placed in."""
        x, y = self.position  # Easier to work with shorter names
        x -= floor(x / WIDTH) * WIDTH  # Map to within boundaries
        y -= floor(y / HEIGHT) * HEIGHT

        if x > MIDPOINT_WIDTH and y < MIDPOINT_HEIGHT:
            return 1  # Top right
        if x < MIDPOINT_WIDTH and y < MIDPOINT_HEIGHT:
            return 2  # Top left
        if x < MIDPOINT_WIDTH and y > MIDPOINT_HEIGHT:
            return 3  # Bottom left
        if x > MIDPOINT_WIDTH and y > MIDPOINT_HEIGHT:
            return 4  # Bottom right

        return 0  # 0 is considered no quadrant


def _load(path: str) -> str:
    """Load input data."""
    with open(path, "r", encoding="utf8") as f:
        return f.read()


def format_input(path: str) -> list[dict]:
    """Format the input data to a more appropriate format."""
    data = _load(path).splitlines()
    initial_conditions = []
    for line in data:
        p, v = line.split(" ")
        p = tuple(int(x) for x in p[2:].split(","))
        v = tuple(int(x) for x in v[2:].split(","))
        initial_conditions.append([p, v])

    return initial_conditions


def print_map(robots: list[Robot]) -> None:
    """Pretty print the map of robots."""
    robot_map = [["."] * WIDTH for _ in range(HEIGHT)]
    for robot in robots:
        x, y = robot.position  # Easier to work with shorter names
        x -= floor(x / WIDTH) * WIDTH  # Map to within boundaries
        y -= floor(y / HEIGHT) * HEIGHT
        robot_map[y][x] = "X"

    for row in robot_map:
        print("".join(row))


def is_tree_candidate(robots: list[Robot]) -> bool:
    """Determine whether a robot composistion resembles a christmas tree."""
    x_positions = [robot.position[0] for robot in robots]
    y_positions = [robot.position[1] for robot in robots]
    if max(Counter(x_positions).values()) > WIDTH * EASTER_EGG_LIMIT:
        return True
    if max(Counter(y_positions).values()) > HEIGHT * EASTER_EGG_LIMIT:
        return True
    return False


def solve():
    """Solve todays puzzles."""
    data = format_input(DATA_PATH)
    robot_gang = [Robot(*start) for start in data]
    robot_count = [0] * 5  # Count per quadrant, 0th is no quadrant
    for robot in robot_gang:
        for _ in range(TIME):
            robot.move()
        quad = robot.get_quadrant()
        robot_count[quad] += 1

    safety_factor = prod(robot_count[1:])  # Skip the "no quadrant" robots
    print(robot_count)
    print(f"The safety factor is {safety_factor}")

    # Part 2: Hunt for the christmas tree
    # This method is rather crude; the 'is_valid_candidate' only checks if there are many robots
    # on the same row or column. I assumed its a rather fast check to do every iteration, and I
    # left it to manual inspection afterwards. It was enough for me to solve it, but to remove
    # some manual labour perhaps one could check for a large group of adjacent robots as well.
    i = TIME  # Let's assume the tree hasn't already occured and we continue from here.
    while True:

        if is_tree_candidate(robot_gang):
            print("\n")
            print_map(robot_gang)
            print(f"Formation occured after {i} seconds")
            is_tree = input("Enter to continue search, anything else to exit.")
            if is_tree:
                break

        # Move one step further
        for robot in robot_gang:
            robot.move()
        i += 1
    print(f"Christmas tree found after {i} seconds.")


if __name__ == "__main__":
    solve()
