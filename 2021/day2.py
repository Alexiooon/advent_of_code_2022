# %% Day 2 part 1

# Read input
FILE = 'data/day2_depth.txt'
with open(FILE, 'r') as f:
    data = f.readlines()

# Convert to useful format
data = [x.split(' ') for x in data]
direction = [x[0] for x in data]
value = [int(x[1]) for x in data]

dist_forward = 0
dist_down = 0
for i in range(len(data)):
    if direction[i] == 'forward':
        dist_forward += value[i]
    elif direction[i] == 'down':
        dist_down += value[i]
    elif direction[i] == 'up':
        dist_down -= value[i]
    else:
        print('Warning: Direction could not be interpreted')
print(dist_forward*dist_down)

# %% Day 2 part 2

horizontal = 0
depth = 0
aim = 0
for i in range(len(data)):
    if direction[i] == 'forward':
        depth += value[i]*aim
        horizontal += value[i]
    elif direction[i] == 'down':
        aim += value[i]
    elif direction[i] == 'up':
        aim -= value[i]
    else:
        print('Warning: Direction could not be interpreted')
print(horizontal*depth)
