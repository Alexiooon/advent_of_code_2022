"""Day 6 challenges."""
# pylint: disable=invalid-name
# Imports
import os

# Read the input data
path = os.path.join('.', 'data', 'day6_data_stream.txt')
with open(path, 'r', encoding='utf8') as f:
    data = f.read()

# %% Challenge 1
marker_length = 4
for i in range(marker_length, len(data)):
    buffer = set(data[i-marker_length:i])

    # Check whether buffer contains 4 unique digits
    if len(buffer) == marker_length:
        break
print(f"First marker comes after {i} characters")

# %% Challenge 2
marker_length = 14
for i in range(marker_length, len(data)):
    buffer = set(data[i-marker_length:i])

    # Check whether buffer contains 4 unique digits
    if len(buffer) == marker_length:
        break
print(f"First message comes after {i} characters")
