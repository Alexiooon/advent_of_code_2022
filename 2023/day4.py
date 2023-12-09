"""Day 4 challenges."""

# Read the data
def read_input(path):
    """Read the input data."""
    with open(path, 'r', encoding='utf8') as f:
        return f.read().splitlines()

def filter_card_id(scratchcard: str) -> str:
    """Remove the first part of a scratchcard."""
    return scratchcard.split(": ")[1]

def get_numbers(number_str: str) -> list[int]:
    """Returns a list of numbers from a string of space-separated numbers."""
    return [int(x) for x in number_str.split(" ") if x]  # Filter out empty strings

def main():
    """Solve todays challenges."""
    cards = read_input("./data/day_4_scratchcards.txt")

    points = 0  # Total amount of points (Part 1 of challenge)
    copies = [1]*len(cards)  # Copies of each card, including the original
    for i, card in enumerate(cards):
        winning_numbers = 0  # The amount of winning numbers in the card
        winners_string = get_numbers(card[10:40])
        players_string = get_numbers(card[42:])

        # Find the number of winning numbers
        for num in players_string:
            if num in winners_string:
                winning_numbers += 1

        # Calculate winning points (Part 1)
        points += 2**(winning_numbers-1) if winning_numbers else 0

        # Create copies of cards
        for j in range(1, winning_numbers+1):
            copies[i+j] += copies[i]

    print(f"The total points across all scratchcards is {points}")
    print(f"The total amount of scratchcards is {sum(copies)}")

if __name__ == '__main__':
    main()
