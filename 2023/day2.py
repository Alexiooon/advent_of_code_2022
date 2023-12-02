"""Day 2 Challenges."""
import os
import math

COLORS =['red', 'green', 'blue']
MAX_CUBES = {'red': 12, 'green': 13, 'blue': 14}

# Read the data
def read_input(path):
    """Read the input data."""
    with open(path, 'r', encoding='utf8') as f:
        data = f.read().splitlines()
    return data


def parse_game_data(game: str):
    """Parse game data into something workable."""
    # Get the game ID
    game_id, data = game.split(': ')
    game_id = int(game_id[5:])

    # Figure out the game data
    max_counted = {'red': 0, 'green': 0, 'blue': 0}
    rounds = data.split('; ')
    for game_round in rounds:
        cubes_sets = game_round.split(', ')
        for cube_set in cubes_sets:
            num, col = cube_set.split(' ')
            max_counted[col] = int(num) if int(num) > max_counted[col] else max_counted[col]

    return game_id, max_counted


def main():
    """Solve the challenges."""
    game_results = read_input(os.path.join('.', 'data', 'day_2_game_results.txt'))

    # Can solve both challenges in the same loop
    id_sum = 0
    power_sum = 0
    for res in game_results:
        _id, count = parse_game_data(res)
        power_sum += math.prod(count.values())
        if all(count[color] <= MAX_CUBES[color] for color in COLORS):
            id_sum += _id
    print(f'The sum of all possible games is: {id_sum}')
    print(f'The sum of all powers is: {power_sum}')


if __name__ == '__main__':
    main()
