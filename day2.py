"""Day 2 challenges."""
# pylint: disable=invalid-name
# Imports
import os

# Read the data
path = os.path.join('.', 'data', 'day2_strategy_guide.txt')
with open(path, 'r', encoding='utf8') as f:
    rounds = f.read().splitlines()

# %% Challenge 1
outcomes = {
    "A X": 3 + 1,
    "B X": 0 + 1,
    "C X": 6 + 1,
    "A Y": 6 + 2,
    "B Y": 3 + 2,
    "C Y": 0 + 2,
    "A Z": 0 + 3,
    "B Z": 6 + 3,
    "C Z": 3 + 3,
}
score = 0
for game_round in rounds:
    score += outcomes[game_round]
print(f"Total score following your strategy guide: {score}")

# %% Challenge 2
outcomes_refined = {
    "A X": 0 + 3,  # Loss + scissor
    "B X": 0 + 1,
    "C X": 0 + 2,
    "A Y": 3 + 1,  # Draw + rock
    "B Y": 3 + 2,
    "C Y": 3 + 3,
    "A Z": 6 + 2,
    "B Z": 6 + 3,
    "C Z": 6 + 1,
}
score = 0
for game_round in rounds:
    score += outcomes_refined[game_round]
print(f"Total score following the revised strategy guide: {score}")