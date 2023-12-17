import itertools


def load(cols):
    return sum(len(col) - i for col in cols for i, item in enumerate(col) if item == "O")


def roll(col):
    empty_space = 0

    for item in col:
        if item == ".":
            empty_space += 1
        elif item == "O":
            yield item
        elif item == "#":
            for _ in range(empty_space):
                yield "."
            empty_space = 0
            yield item

    for _ in range(empty_space):
        yield "."


def rolled(cols):
    return tuple("".join(roll(col)) for col in cols)


def spin(cols):
    return rotated(rolled(cols))


def cycle(cols):
    for _ in range(4):
        cols = spin(cols)
    return cols


def rotated(cols):
    return tuple(reversed(["".join(row) for row in zip(*cols)]))


def find_nth_cycle(cols, n):
    history = {}
    for i in itertools.count():
        if cols in history:
            break
        history[cols] = i
        cols = cycle(cols)

    offset = history[cols]
    period = i - offset
    index = offset + ((n - offset) % period)

    for cols, i in history.items():
        if i == index:
            return cols


def run(data):
    cols = tuple("".join(row) for row in zip(*data.splitlines()))

    one = rolled(cols)
    billion = find_nth_cycle(cols, 1000000000)

    return load(one), load(billion)
