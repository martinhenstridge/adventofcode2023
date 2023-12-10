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
    r, c = start
    heading = Heading.E

    path = set()
    while True:
        path.add((r, c))
        dr, dc = heading.value
        r += dr
        c += dc
        if (pipe := maze[r][c]) == "S":
            break
        heading = PIPES[pipe][heading]

    return path


def flood(maze, path):
    inside = set()

    for row, line in enumerate(maze):
        keep = False
        prev = None
        for col, char in enumerate(line):
            if (p := (row, col)) not in path:
                if keep:
                    inside.add(p)
                continue

            if char == "-":
                continue

            if char == "|":
                keep = not keep
                continue

            if (char == "J" and prev != "L") or (char == "7" and prev != "F"):
                keep = not keep
            prev = char

    return inside


def run(data):
    maze, start = parse_maze(data)

    path = traverse(maze, start)
    inside = flood(maze, path)

    return len(path) // 2, len(inside)
