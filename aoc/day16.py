from enum import Enum


class Heading(Enum):
    U = (-1, 0)
    D = (+1, 0)
    L = (0, -1)
    R = (0, +1)


TILES = {
    ".": {
        Heading.U: [Heading.U],
        Heading.D: [Heading.D],
        Heading.L: [Heading.L],
        Heading.R: [Heading.R],
    },
    "/": {
        Heading.U: [Heading.R],
        Heading.D: [Heading.L],
        Heading.L: [Heading.D],
        Heading.R: [Heading.U],
    },
    "\\": {
        Heading.U: [Heading.L],
        Heading.D: [Heading.R],
        Heading.L: [Heading.U],
        Heading.R: [Heading.D],
    },
    "|": {
        Heading.U: [Heading.U],
        Heading.D: [Heading.D],
        Heading.L: [Heading.U, Heading.D],
        Heading.R: [Heading.U, Heading.D],
    },
    "-": {
        Heading.U: [Heading.L, Heading.R],
        Heading.D: [Heading.L, Heading.R],
        Heading.L: [Heading.L],
        Heading.R: [Heading.R],
    },
}


def parse_grid(data):
    lines = data.splitlines()
    return len(lines), {
        (r, c): char for r, line in enumerate(lines) for c, char in enumerate(line)
    }


def traverse(grid, initial_heading, initial_position):
    history = {p: set() for p in grid}

    beams = [(initial_position, initial_heading)]

    while beams:
        position, heading = beams.pop()
        history[position].add(heading)

        tile = grid[position]

        for new_heading in TILES[tile][heading]:
            r, c = position
            r += new_heading.value[0]
            c += new_heading.value[1]
            new_position = (r, c)

            if new_position not in grid:
                continue

            if new_heading in history[new_position]:
                continue

            beams.append((new_position, new_heading))

    return sum(1 if h else 0 for h in history.values())


def run(data):
    size, grid = parse_grid(data)

    count = traverse(grid, Heading.R, (0, 0))

    umax = max(traverse(grid, Heading.U, (size - 1, c)) for c in range(size))
    dmax = max(traverse(grid, Heading.D, (0, c)) for c in range(size))
    lmax = max(traverse(grid, Heading.L, (r, size - 1)) for r in range(size))
    rmax = max(traverse(grid, Heading.R, (r, 0)) for r in range(size))

    return count, max([umax, dmax, lmax, rmax])
