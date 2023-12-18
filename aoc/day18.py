import re
import itertools


HEADINGS = {
    "0": (0, +1),
    "R": (0, +1),
    "1": (+1, 0),
    "D": (+1, 0),
    "2": (0, -1),
    "L": (0, -1),
    "3": (-1, 0),
    "U": (-1, 0),
}


def parse_instructions(data):
    for line in data.splitlines():
        match = re.fullmatch(r"(U|D|L|R) (\d+) \(\#([0-9a-f]+)\)", line)
        yield HEADINGS[match[1]], int(match[2]), match[3]


def parse_colour(colour):
    distance = int(colour[:-1], 16)
    heading = HEADINGS[colour[-1]]
    return heading, distance


def walk_perimeter(sections):
    length = 0
    corners = []

    p = (0, 0)
    for (dr, dc), distance in sections:
        length += distance
        r, c = p
        p = (r + dr * distance, c + dc * distance)
        corners.append(p)

    return length, corners


def batched(iterable, n):
    for i in range(0, len(iterable), n):
        yield tuple(iterable[i : i + n])


def find_internal_area(corners):
    prev_row = None
    columns = set()

    area = 0
    for row, points in itertools.groupby(sorted(corners), key=lambda p: p[0]):
        corner_cols = set(p[1] for p in points)

        for block in batched(sorted(columns), 2):
            area += (row - prev_row - 1) * (block[1] - block[0] - 1)

        include = True
        walls = set(batched(sorted(corner_cols), 2))
        for segment in itertools.pairwise(sorted(columns | corner_cols)):
            if segment in walls:
                if (segment[0] in columns) == (segment[1] in columns):
                    include = not include
            else:
                if include:
                    area += segment[1] - segment[0] - 1
                include = not include

        prev_row = row
        columns = columns ^ corner_cols
    return area


def find_area(sections):
    perimeter, corners = walk_perimeter(sections)
    internal = find_internal_area(corners)
    return internal + perimeter


def run(data):
    instructions = list(parse_instructions(data))

    small = [i[:2] for i in instructions]
    large = [parse_colour(i[2]) for i in instructions]

    return find_area(small), find_area(large)
