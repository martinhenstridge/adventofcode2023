import itertools


def calculate_load(cols):
    return sum(
        len(col) - i for col in cols for i, item in enumerate(col) if item == "O"
    )


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


def tilted(cols):
    return tuple(tuple(roll(col)) for col in cols)


def rotated(cols):
    return tuple(reversed([tuple(row) for row in zip(*cols)]))


def spin(cols):
    return rotated(tilted(cols))


def cycled(cols, n):
    history = {}
    for i in itertools.count():
        if cols in history:
            break
        history[cols] = i
        for _ in range(4):
            cols = spin(cols)

    offset = history[cols]
    period = i - offset
    index = offset + ((n - offset) % period)

    for cols, i in history.items():
        if i == index:
            return cols


def run(data):
    cols = tuple(tuple(row) for row in zip(*data.splitlines()))

    one = tilted(cols)
    billion = cycled(cols, 1000000000)

    return calculate_load(one), calculate_load(billion)
