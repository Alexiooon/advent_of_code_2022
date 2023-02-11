

# %% Day 1 part 1

# Read input
FILE = 'data/day1_depth.txt'
with open(FILE, 'r') as f:
    data = f.readlines()

# Convert to list
data = [int(val) for val in data]

# Iterate through list to get number of increases
count = 0
for i in range(len(data)-1):
    if data[i+1] > data[i]:
        count += 1
print('Number of increases: ', count)
# %% Day 1 part 2

# Iterate to get number of increases over 3 point averages
sum3_data = [sum(data[i:i+3]) for i in range(len(data)-2)]
count = 0
for i in range(len(sum3_data)-1):
    if sum3_data[i+1] > sum3_data[i]:
        count += 1
print('Number of increases across 3-point sums: ', count)
