from enum import Enum


class Heading(Enum):
    N = (-1, 0)
    S = (+1, 0)
    E = (0, +1)
    W = (0, -1)


PIPES = {
    "|": {Heading.N: Heading.N, Heading.S: Heading.S},
    "-": {Heading.E: Heading.E, Heading.W: Heading.W},
    "L": {Heading.S: Heading.E, Heading.W: Heading.N},
    "J": {Heading.S: Heading.W, Heading.E: Heading.N},
    "7": {Heading.N: Heading.W, Heading.E: Heading.S},
    "F": {Heading.N: Heading.E, Heading.W: Heading.S},
}


def parse_maze(data):
    maze = []
    start = None
    for row, line in enumerate(data.splitlines()):
        maze.append(line)
        if "S" in line:
            start = row, line.index("S")
    return maze, start


def traverse(maze, start):
    path = set()

    r, c = start
    heading = Heading.E
    while True:
        path.add((r, c))
        dr, dc = heading.value
        r += dr
        c += dc
        if (pipe := maze[r][c]) == "S":
            break
        heading = PIPES[pipe][heading]

    return path


def count_inside(maze, path):
    # Walk each row in the maze from left to right, switching between
    # "outside" (initially) and "inside" the loop as we cross over its
    # constituent pipes. The following are the important cases:
    #
    #   |                     : switch
    #   -                     : ignore
    #   Zig-zag (e.g. L7, FJ) : switch
    #   Hairpin (e.g. LJ, F7) : ignore
    #
    # Note there may be one or more '-' pipes in between the start and
    # end of zig-zag or hairpin sections.

    count = 0

    for row, line in enumerate(maze):
        keep = False
        prev = None
        for col, char in enumerate(line):
            if (p := (row, col)) not in path:
                if keep:
                    count += 1
                continue

            match (char, prev):
                case ("L", _) | ("F", _):
                    # Start of a zig-zag or hairpin, store for later
                    prev = char
                case ("|", _) | ("J", "F") | ("7", "L"):
                    # Switch between inside and outside
                    keep = not keep

    return count


def run(data):
    maze, start = parse_maze(data)

    path = traverse(maze, start)
    inside = count_inside(maze, path)

    return len(path) // 2, inside
