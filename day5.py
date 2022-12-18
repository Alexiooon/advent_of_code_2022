"""Day 5 challenges."""
# pylint: disable=invalid-name
# Imports
import os
import numpy as np

# Read the input data
path = os.path.join('.', 'data', 'day5_crane_instructions.txt')
with open(path, 'r', encoding='utf8') as f:
    sheet = f.read().splitlines()

# %% Challenge 1:
# Parse the input data
# Each stack becomes a list of strings with their crates, top crate at end of list
crates_data = np.array([list(line) for line in sheet[0:8]])
crates_data = np.flip(crates_data[:,[1, 5, 9, 13, 17, 21, 25, 29, 33]].T, 1)
stacks = []
for stack in crates_data:
    stacks.append([crate for crate in stack if crate != ' '])
instructions = sheet[10:]

def move(instr: str):
    """Perform moves given a line of instructions."""
    n_moves = int(instr.split(" ")[1])
    start = int(instr.split(" ")[3]) - 1  # We start at index 0, instruction start at 1
    dest = int(instr.split(" ")[5]) - 1

    for _ in range(n_moves):
        stacks[dest].append(stacks[start].pop())

# Perform all moves
for line in instructions:
    move(line)

# Generate output string
top_crates = ""
for stack in stacks:
    top_crates += stack[-1]
print(f"String of all top crates is '{top_crates}'")

# %% Challenge 2
# New stack
stacks = []
for stack in crates_data:
    stacks.append([crate for crate in stack if crate != ' '])


def move_multiple(instr: str):
    """Perform moves given a line of instructions, preserving order."""
    n_moves = int(instr.split(" ")[1])
    start = int(instr.split(" ")[3]) - 1  # We start at index 0, instruction start at 1
    dest = int(instr.split(" ")[5]) - 1

    crane_hold = []
    for _ in range(n_moves):
        crane_hold.append(stacks[start].pop())
    crane_hold.reverse()
    stacks[dest].extend(crane_hold)

# Perform all moves
for line in instructions:
    move_multiple(line)

# Generate output string
top_crates = ""
for stack in stacks:
    top_crates += stack[-1]
print(f"String of all top crates while preserving move order is '{top_crates}'")