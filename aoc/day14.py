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


def cycle(cols):
    for _ in range(4):
        cols = rotated(roll(col) for col in cols)
    return cols


def rotated(cols):
    return list(reversed(["".join(row) for row in zip(*cols)]))


def dump(cols):
    print("--")
    for row in zip(*cols):
        print("".join(row))


def find_nth_cycle(cols, n):
    history = {}
    for i in itertools.count():
        signature = "".join(cols)
        print(i, load(cols))
        if signature in history:
            break
        history[signature] = i
        cols = cycle(cols)

    offset = history[signature]
    period = i - offset
    index = offset + ((n - offset) % period)
    print("offset:", offset)
    print("period:", period)
    print("index:", index)
    return index



def run(data):
    #data = DATA
    cols = ["".join(row) for row in zip(*data.splitlines())]

    n = find_nth_cycle(cols, 1000000000)
    print(n)
    return 0, 0


DATA = """\
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""
