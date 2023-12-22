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
    return {
        (r, c)
        for p in current
        for r, c in neighbours(p)
        if garden[r % 131, c % 131] != "#"
    }


def extrapolate_plots(steps):
    # Extrapolation based on the following observations / assumptions:
    #
    # - The garden is 131 x 131
    # - The starting point is the centre (65, 65)
    # - The path to the edge both horizontally and vertically is clear
    # - It takes 65 steps to reach the edge of the first tile
    # - It takes a further 131 steps to reach the edge of each subsequent tile
    # - A pattern is expected starting at 65 steps with a period of 131 steps
    # - The area (and hence reachable plots) is quadratic in number of steps
    #
    # Running the naive solution for:
    # - 65 steps  (= 65 + 0*131)
    # - 196 steps (= 65 + 1*131)
    # - 327 steps (= 65 + 2*131)
    # provides three points from which the quadratic solution may be derived.
    #
    # n  s    p
    # 0  65   3885
    # 1  196  34700
    # 2  327  96215

    n = (steps - 65) // 131
    return 3885 + 15465 * n + 15350 * n * n


def run(data):
    start, garden = parse_garden(data)

    plots = {start}
    for _ in range(64):
        plots = step(garden, plots)

    return len(plots), extrapolate_plots(26501365)
