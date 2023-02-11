"""Day 4 challenges."""
# pylint: disable=invalid-name
# Imports
import os

# Read the input data
path = os.path.join('.', 'data', 'day4_sections.txt')
with open(path, 'r', encoding='utf8') as f:
    pairs = f.read().splitlines()

# %% Challenge 1
# Parse the data
def min_max(section: str):
    """Get the min and max value from sections str"""
    return (int(x) for x in section.split("-"))

# Restructure data as a list of 4 element lists (min1, max1, min2, max2)
pairs_cleaned = []
for idx, pair in enumerate(pairs):
    data = pair.split(",")  # Split sections into separate string
    pairs_cleaned.append([int(x) for x in data[0].split("-") + data[1].split("-")])

overlapping_pairs = []
for pair in pairs_cleaned:
    if pair[0] <= pair[2] and pair[1] >= pair[3]:
        overlapping_pairs.append(pair)
    elif pair[0] >= pair[2] and pair[1] <= pair[3]:
        overlapping_pairs.append(pair)
print(f"The number of pairs which has a full overlap is {len(overlapping_pairs)}")

# %% Challenge 2
overlapping_pairs = []
for pair in pairs_cleaned:
    if pair[0] <= pair[2] <= pair[1]:
        overlapping_pairs.append(pair)
    elif pair[0] <= pair[3] <= pair[1]:
        overlapping_pairs.append(pair)
    elif pair[2] <= pair[0] <= pair[3]:
        overlapping_pairs.append(pair)
    elif pair[2] <= pair[1] <= pair[3]:
        overlapping_pairs.append(pair)
print(f"The number of pairs which has any overlap is {len(overlapping_pairs)}")
