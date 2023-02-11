"""Day 9 challenges."""
# pylint: disable=invalid-name
# Imports
import os

# Read the input data
path = os.path.join('.', 'data', 'day9_rope_motion.txt')
with open(path, 'r', encoding='utf8') as f:
    instructions = f.read().splitlines()

# %% Challenge 1

def move_tail(loc_tail: tuple, loc_head: tuple):
    """Move the tail."""
    dist_x = int(loc_head[0] - loc_tail[0])
    dist_y = int(loc_head[1] - loc_tail[1])

    new_pos = list(loc_tail)
    # If head is close enough, we do not need to move
    if abs(dist_x) <= 1 and abs(dist_y) <= 1:
        return new_pos

    # Handle movement
    if abs(dist_x) == 2:
        new_pos[0] += int(dist_x / 2)
        if abs(dist_y) == 1:
            new_pos[1] += dist_y
    if abs(dist_y) == 2:
        new_pos[1] += int(dist_y / 2)
        if abs(dist_x) == 1:
            new_pos[0] += dist_x
    return new_pos

directions = {
    "U": [0, -1],
    "R": [1, 0],
    "D": [0, 1],
    "L": [-1, 0]
}

unique_positions = set(((0, 0),))
head_pos = [0, 0]
tail_pos = (0, 0)
for line in instructions:

    # Parse input line
    move, reps = line.split()
    move = directions[move]
    for _ in range(int(reps)):
        # Move head
        head_pos[0] += move[0]
        head_pos[1] += move[1]

        # Move tail
        tail_pos = tuple(move_tail(tail_pos, head_pos))

        # Update number of new positions
        unique_positions.update((tail_pos,))

print(f"Number of unique positions of the tail: {len(unique_positions)}")

# %% Challenge 2: We have to go deeper

knots = 10
unique_positions = set(((0, 0),))
positions = [(0,0) for _ in range(knots)]
for line in instructions:

    # Parse input line
    move, reps = line.split()
    move = directions[move]
    for _ in range(int(reps)):

        # Move head
        new_head_pos = list(positions[0])
        new_head_pos[0] += move[0]
        new_head_pos[1] += move[1]
        positions[0] = new_head_pos

        # Move tails
        for knot in range(1, knots):
            positions[knot] = tuple(move_tail(positions[knot], positions[knot-1]))

        # Update number of new positions for end of rope
        unique_positions.update((positions[-1],))

print(f"Number of unique positions for the end of the 10-knot rope: {len(unique_positions)}")
