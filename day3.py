"""Day 3 challenges."""
# pylint: disable=invalid-name
# Imports
import os

# Read the data
path = os.path.join('.', 'data', 'day3_rucksacks.txt')
with open(path, 'r', encoding='utf8') as f:
    inventory = f.read().splitlines()

# %% Challenge 1
def mid_idx(iterable):
    """Return middle index of an iterable."""
    return int(len(iterable) / 2)

# Generate a dict with item priorities
pack_items = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
prio = {}
prio.update({item: ord(item) - 96 for item in pack_items[:mid_idx(pack_items)]})
prio.update({item: ord(item) - 38 for item in pack_items[mid_idx(pack_items):]})

sum_priorities = 0
for rucksack in inventory:
    for item in rucksack[mid_idx(rucksack):]:  # Iterate through first compartment
        if item in rucksack[:mid_idx(rucksack)]:
            sum_priorities += prio[item]
            break  # Only one error per rucksack
print(f"Sum of priorities of misplaced items: {sum_priorities}")

# %% Challenge 2
idx = 0
sum_priorities = 0
while idx < len(inventory):
    rucksack = inventory[idx]
    for item in rucksack:
        if item in inventory[idx+1] and item in inventory[idx+2]:
            sum_priorities += prio[item]
            break  # Only one error per rucksack
    idx += 3
print(f"Sum of priorities of group badges: {sum_priorities}")