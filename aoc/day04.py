def find_matching_numbers(data):
    cards = {}

    for line in data.splitlines():
        label, numbers = line.split(":")

        _, numstr = label.split()
        cardnum = int(numstr)

        parts = numbers.split("|")
        w = frozenset(parts[0].split())
        o = frozenset(parts[1].split())

        cards[cardnum] = len(w & o)

    return cards


def run(data):
    matches = find_matching_numbers(data)

    counts = {card: 1 for card in matches}
    for card, count in counts.items():
        for i in range(matches[card]):
            counts[card + i + 1] += count

    total_points = sum(2 ** (n - 1) for n in matches.values() if n)
    scratchcards = sum(counts.values())

    return total_points, scratchcards
