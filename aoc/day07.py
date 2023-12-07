from enum import Enum
from collections import Counter

JOKER = "_"
STRENGTH = {
    "_": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "T": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14,
}


class Type(Enum):
    FIVE_OF_A_KIND = 7
    FOUR_OF_A_KIND = 6
    FULL_HOUSE = 5
    THREE_OF_A_KIND = 4
    TWO_PAIR = 3
    ONE_PAIR = 2
    HIGH_CARD = 1


class Hand:
    def __init__(self, cards):
        self.cards = cards
        self.kind = hand_type(cards)

    def __hash__(self):
        return hash(self.cards)

    def __lt__(self, other):
        if self.kind.value < other.kind.value:
            return True
        if self.kind.value > other.kind.value:
            return False
        for s, o in zip(self.cards, other.cards):
            if STRENGTH[s] < STRENGTH[o]:
                return True
            if STRENGTH[s] > STRENGTH[o]:
                return False

    def replace(self, a, b):
        cards = self.cards.replace(a, b)
        return Hand(cards)


def parse_hands(data):
    for line in data.splitlines():
        cards, bid = line.split()
        yield cards, int(bid)


def hand_type(cards):
    if JOKER in cards:
        cards = optimise(cards)

    counts = sorted(Counter(cards).values(), reverse=True)
    if counts[0] == 5:
        return Type.FIVE_OF_A_KIND
    if counts[0] == 4:
        return Type.FOUR_OF_A_KIND
    if counts[0] == 3 and counts[1] == 2:
        return Type.FULL_HOUSE
    if counts[0] == 3 and counts[1] == 1:
        return Type.THREE_OF_A_KIND
    if counts[0] == 2 and counts[1] == 2:
        return Type.TWO_PAIR
    if counts[0] == 2 and counts[1] == 1:
        return Type.ONE_PAIR
    if counts[0] == 1:
        return Type.HIGH_CARD


def optimise(cards):
    without_jokers = cards.replace(JOKER, "")
    if not without_jokers:
        return "AAAAA"

    def sort_fn(item):
        card, count = item
        return (count, STRENGTH[card])

    ordered = sorted(Counter(without_jokers).items(), key=sort_fn)
    replacement, _ = ordered[-1]
    return cards.replace(JOKER, replacement)


def calculate_winnings(hands):
    return sum(bid * (i + 1) for i, (hand, bid) in enumerate(sorted(hands.items())))


def run(data):
    hands = {Hand(cards): bid for cards, bid in parse_hands(data)}
    total1 = calculate_winnings(hands)

    hands = {hand.replace("J", JOKER): bid for hand, bid in hands.items()}
    total2 = calculate_winnings(hands)

    return total1, total2
