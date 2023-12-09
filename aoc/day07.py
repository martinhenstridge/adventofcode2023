from collections import Counter

JOKER = "_"

CARD_STRENGTH = {
    JOKER: 0,
    "2": 1,
    "3": 2,
    "4": 3,
    "5": 4,
    "6": 5,
    "7": 6,
    "8": 7,
    "9": 8,
    "T": 9,
    "J": 10,
    "Q": 11,
    "K": 12,
    "A": 13,
}

TYPE_STRENGTH = {
    (1, 1, 1, 1, 1): 0,
    (2, 1, 1, 1): 1,
    (2, 2, 1): 2,
    (3, 1, 1): 3,
    (3, 2): 4,
    (4, 1): 5,
    (5,): 6
}


class Hand:
    def __init__(self, cards):
        self.cards = cards
        self.type_strength = self.type_strength(cards)

    def replace(self, a, b):
        cards = self.cards.replace(a, b)
        return Hand(cards)

    def __lt__(self, other):
        if self.type_strength < other.type_strength:
            return True
        if self.type_strength > other.type_strength:
            return False
        for s, o in zip(self.cards, other.cards):
            if CARD_STRENGTH[s] < CARD_STRENGTH[o]:
                return True
            if CARD_STRENGTH[s] > CARD_STRENGTH[o]:
                return False

    @staticmethod
    def type_strength(cards):
        counts = Counter(cards)
        jokers = counts.pop(JOKER, 0)
        if jokers == 5:
            return TYPE_STRENGTH[(5,)]
        signature = sorted(counts.values(), reverse=True)
        signature[0] += jokers
        return TYPE_STRENGTH[tuple(signature)]


def parse_hands(data):
    for line in data.splitlines():
        cards, bid = line.split()
        yield cards, int(bid)


def calculate_winnings(hands):
    return sum(bid * (i + 1) for i, (hand, bid) in enumerate(sorted(hands)))


def run(data):
    orig = [(Hand(cards), bid) for cards, bid in parse_hands(data)]
    joke = [(hand.replace("J", JOKER), bid) for hand, bid in orig]

    return calculate_winnings(orig), calculate_winnings(joke)
