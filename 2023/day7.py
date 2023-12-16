"""Day 7 challenges."""

from collections import Counter

CARD_VALUES = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
}
CARD_VALUES_WITH_JOKER = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
    "J": 1,
}

def read_input(path):
    """Read the input data."""
    with open(path, 'r', encoding='utf8') as f:
        return f.read().splitlines()


def identify_hand(hand: str) -> int:
    """Identify the value of a hand."""
    count = Counter(hand)
    if max(count.values()) == 5:  # Five of a kind
        value = 7
    elif max(count.values()) == 4:  # Four of a kind
        value = 6
    elif 3 in count.values() and 2 in count.values():  # Full House
        value = 5
    elif max(count.values()) == 3:  # Three of a kind
        value = 4
    elif list(count.values()).count(2) == 2:  # Two pair
        value = 3
    elif max(count.values()) == 2:  # One pair
        value = 2
    else:  # High card
        value = 1
    return value


def identify_hand_with_jokers(hand: str) -> int:
    """Identify the value of a hand where 'J' is treated as a joker."""
    count = Counter(hand)

    # The strongest hand a Joker can make always involve them all changing to the same card,
    # so for simplicity we check every possibility and return the strongest result
    return max(identify_hand(hand.replace("J", card)) for card in count.keys())


def main():
    """Solve todays challenges."""
    full_data = read_input("./data/day_7_hands.txt")

    # Work with assigning a value to each hand and card. Put it in a list of tuples for sorting
    # (hand_value, card1, card2, card3, card4, card5, bid)
    parsed_data = [
        (
            identify_hand(line[:5]),
            CARD_VALUES[line[0]],
            CARD_VALUES[line[1]],
            CARD_VALUES[line[2]],
            CARD_VALUES[line[3]],
            CARD_VALUES[line[4]],
            int(line[6:])
        )
        for line in full_data
    ]
    sorted_data = sorted(parsed_data)

    # Find the sum of all ranks times bids
    tot = sum((rank+1)*val[-1] for rank, val in enumerate(sorted_data))
    print(f"The sum of ranks multiplied by their bids is {tot}")

    # Part 2
    # We just need to remake the identify_hand() function to be able to handle jokers
    parsed_data = [
        (
            identify_hand_with_jokers(line[:5]),
            CARD_VALUES_WITH_JOKER[line[0]],
            CARD_VALUES_WITH_JOKER[line[1]],
            CARD_VALUES_WITH_JOKER[line[2]],
            CARD_VALUES_WITH_JOKER[line[3]],
            CARD_VALUES_WITH_JOKER[line[4]],
            int(line[6:])
        )
        for line in full_data
    ]
    sorted_data = sorted(parsed_data)

    # Find the sum of all ranks times bids
    tot = sum((rank+1)*val[-1] for rank, val in enumerate(sorted_data))
    print(f"The sum of ranks multiplied by their bids is {tot} when J is Joker")


if __name__ == '__main__':
    main()
