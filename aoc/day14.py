def load(sequence, length):
    return sum(length - i for i, item in enumerate(sequence) if item == "O")


def roll(col):
    round_rocks = 0
    empty_space = 0

    for item in col:
        if item == ".":
            empty_space += 1
        elif item == "O":
            round_rocks += 1
        elif item == "#":
            for _ in range(round_rocks):
                yield "O"
            for _ in range(empty_space):
                yield "."
            round_rocks = 0
            empty_space = 0
            yield item
    for _ in range(round_rocks):
        yield "O"
    for _ in range(empty_space):
        yield "."


def run(data):
    #data = DATA
    rows = data.splitlines()
    total = 0
    for col in zip(*rows):
        rolled = roll(col)
        total += load(rolled, len(col))
    return total, 0


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
