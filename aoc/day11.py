import itertools


def find_galaxies(grid):
    return [
        (row, col)
        for row, line in enumerate(grid)
        for col, char in enumerate(line)
        if char == "#"
    ]


def find_cumulative_empty(charset):
    empty = []
    count = 0
    for chars in charset:
        empty.append(count)
        if not any(char == "#" for char in chars):
            count += 1
    return empty


def expand_by(galaxies, cum_empty_rows, cum_empty_cols, extra):
    return [
        (r + extra * cum_empty_rows[r], c + extra * cum_empty_cols[c])
        for r, c in galaxies
    ]


def sum_shortest_paths(galaxies):
    return sum(
        abs(r1 - r2) + abs(c1 - c2)
        for (r1, c1), (r2, c2) in itertools.combinations(galaxies, 2)
    )


def run(data):
    grid = data.splitlines()
    galaxies = find_galaxies(grid)

    cum_empty_rows = find_cumulative_empty(grid)
    cum_empty_cols = find_cumulative_empty(zip(*grid))

    expanded1 = expand_by(galaxies, cum_empty_rows, cum_empty_cols, extra=1)
    expanded2 = expand_by(galaxies, cum_empty_rows, cum_empty_cols, extra=999999)

    return sum_shortest_paths(expanded1), sum_shortest_paths(expanded2)
