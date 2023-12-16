def parse_patterns(data):
    rows = []
    for line in data.splitlines():
        if line:
            rows.append(line)
        else:
            yield rows
            rows = []
    yield rows


def rotated(pattern):
    return ["".join(chars) for chars in zip(*pattern)]


def diffcount(pattern, a, b):
    return sum(1 if ca != cb else 0 for ca, cb in zip(pattern[a], pattern[b]))


def find_asymmetries(pattern, plane):
    above = reversed(range(plane))
    below = range(plane, len(pattern))
    return [(a, b) for a, b in zip(above, below) if pattern[a] != pattern[b]]


def find_plane_clean(pattern):
    for plane in range(1, len(pattern)):
        if not find_asymmetries(pattern, plane):
            return plane


def find_plane_smudge(pattern):
    for plane in range(1, len(pattern)):
        asymmetries = find_asymmetries(pattern, plane)
        if len(asymmetries) == 1 and diffcount(pattern, *asymmetries[0]) == 1:
            return plane


def find_summary(pattern, finder):
    plane = finder(pattern)
    if plane:
        return plane * 100

    plane = finder(rotated(pattern))
    if plane:
        return plane


def run(data):
    summary_clean = 0
    summary_smudge = 0

    for pattern in parse_patterns(data):
        summary_clean += find_summary(pattern, find_plane_clean)
        summary_smudge += find_summary(pattern, find_plane_smudge)

    return summary_clean, summary_smudge
