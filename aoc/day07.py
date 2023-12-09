from collections import Counter

JOKER = "_"

CARD_STRENGTH = {
    JOKER: 1,
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

TYPE_STRENGTH = {
    (1, 1, 1, 1, 1): 1,
    (2, 1, 1, 1): 2,
    (2, 2, 1): 3,
    (3, 1, 1): 4,
    (3, 2): 5,
    (4, 1): 6,
    (5,): 7
}


def parse_hands(data):
    for line in data.splitlines():
        cards, bid = line.split()
        yield cards, int(bid)


def hand_type(cards):
    counts = Counter(cards)
    jokers = counts.pop(JOKER, 0)

    if jokers == 5:
        return (5,)

    signature = sorted(counts.values(), reverse=True)
    signature[0] += jokers
    return tuple(signature)


def hand_value(cards):
    value = TYPE_STRENGTH[hand_type(cards)] << 40
    for i, card in enumerate(cards):
        value |= CARD_STRENGTH[card] << 8 * (4 - i)
    return value


def calculate_winnings(hands):
    return sum(bid * (i + 1) for i, (_, bid) in enumerate(sorted(hands)))


def run(data):
    hands = {cards: bid for cards, bid in parse_hands(data)}

    orig = [(hand_value(cards), bid) for cards, bid in hands.items()]
    joke = [(hand_value(cards.replace("J", JOKER)), bid) for cards, bid in hands.items()]

    return calculate_winnings(orig), calculate_winnings(joke)
