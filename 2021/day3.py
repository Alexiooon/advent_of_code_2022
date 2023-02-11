# %% Import modules
import numpy as np

# %% Day 3 part 1

# Read input
FILE = 'data/day3_input.txt'
with open(FILE, 'r') as f:
    data = f.readlines()

# Convert to useful format
data = [str(int(x)).zfill(len(x)-1) for x in data]  # Removes '\n'

gamma = ''
epsilon = ''
for i in range(len(data[0])):
    col = sum([int(x[i]) for x in data])
    if col > len(data)/2:
        gamma += '1'
        epsilon += '0'
    else:
        gamma += '0'
        epsilon += '1'
print('Power consumption: ', int(gamma, 2)*int(epsilon, 2))

# %% Day 3 part 2


def get_oxygen_rating(data):
    indexes = [i for i in range(len(data))]

    pos = 0
    while 1:
        # Get the most common value
        col = sum([int(x[pos]) for x in data[indexes]])

        # Update index list
        if col >= len(indexes)/2:
            indexes = [i for i in range(len(data))
                       if data[i][pos] == '1' and i in indexes]
        else:
            indexes = [i for i in range(len(data))
                       if data[i][pos] == '0' and i in indexes]

        # Check if we are finished
        if len(indexes) == 1:
            break
        else:
            pos += 1

    return data[indexes[0]]


def get_CO2_rating(data):
    indexes = [i for i in range(len(data))]

    pos = 0
    while 1:
        # Get the most common value
        col = sum([int(x[pos]) for x in data[indexes]])

        # Update index list
        if col >= len(indexes)/2:
            indexes = [i for i in range(len(data))
                       if data[i][pos] == '0' and i in indexes]
        else:
            indexes = [i for i in range(len(data))
                       if data[i][pos] == '1' and i in indexes]

        # Check if we are finished
        if len(indexes) == 1:
            break
        else:
            pos += 1

    return data[indexes[0]]


# Convert to numpy array
data = np.array(data)
oxygen_rating = get_oxygen_rating(data)
CO2_rating = get_CO2_rating(data)
print('Life support rating: ', int(oxygen_rating, 2)*int(CO2_rating, 2))
