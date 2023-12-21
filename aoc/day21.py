def parse_garden(data):
    start = None
    garden = {}

    for r, line in enumerate(data.splitlines()):
        for c, char in enumerate(line):
            garden[r, c] = char
            if char == "S":
                start = (r, c)

    return start, garden


def neighbours(position):
    r, c = position
    yield r - 1, c
    yield r + 1, c
    yield r, c - 1
    yield r, c + 1


def step(garden, current):
    return {n for p in current for n in neighbours(p) if garden[n] != "#"}


def run(data):
    start, garden = parse_garden(data)

    plots = {start}
    for _ in range(64):
        plots = step(garden, plots)

    return len(plots), 0
