"""Day 10 challenges."""
# pylint: disable=invalid-name
# Imports
import os

# Read the input data
path = os.path.join('.', 'data', 'day10_program.txt')
with open(path, 'r', encoding='utf8') as f:
    commands = f.read().splitlines()

# %% Challenge 1

X = 1  # Register
cycle = 1
key_cycles = [20, 60, 100, 140, 180, 220]
signal_strengths = 0
for command in commands:
    if cycle in key_cycles:
        signal_strengths += X * cycle
    if command == "noop":
        cycle += 1
    elif "addx" in command:
        cmd, val = command.split()
        if cycle+1 in key_cycles:
            signal_strengths += (X * (cycle+1))
        cycle += 2
        X += int(val)
# Check final cycle
if cycle in key_cycles:
    signal_strengths += X

print(f"Sum of signal strength during the specific cycles: {signal_strengths}")

# %% Challenge 2

line = 0
cycle = 1
X = 1
wait = True
image = ""

while line < len(commands):
    # Draw the pixel
    if X-1 <= (cycle-1) % 40 <= X+1:
        image += "#"
    else:
        image += " "

    # Execute commands
    command = commands[line]
    if "noop" in command:
        line += 1
    elif "addx" in command:
        if not wait:
            X += int(command.split()[1])
            line += 1
        wait = not wait
    cycle += 1

print(image[0:40])
print(image[40:80])
print(image[80:120])
print(image[120:160])
print(image[160:200])
print(image[200:240])
