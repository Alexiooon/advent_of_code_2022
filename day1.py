"""Day 1 challenges."""
# pylint: disable=invalid-name
# Imports
import os

#%% Challenge 1
# Read the data
path = os.path.join('.', 'data', 'day1_calories.txt')
with open(path, 'r', encoding='utf8') as f:
    inv = f.read().splitlines()

# Group each elf's inventory
cal_totals = []
elf = 0
for snack in inv:
    if not snack:
        cal_totals.append(elf)
        elf = 0
        continue
    elf += int(snack)
cal_totals.append(elf)

# Get the max value
print(f'Highest amount of calories carried by any elf: {max(cal_totals)}')

# %% Challenge 2

# Sort the elves by their calorie inventory, sum the last three
cal_totals.sort()
print(f'Total amount of calories carried by the top 3 elves: {sum(cal_totals[-3:])}')
