import itertools


def parse_histories(data):
    return [[int(v) for v in line.split()] for line in data.splitlines()]


def extrapolate(values):
    if all(v == 0 for v in values):
        return 0
    diffs = [b - a for a, b in itertools.pairwise(values)]
    return values[-1] + extrapolate(diffs)


def run(data):
    histories = parse_histories(data)
    return (
        sum(extrapolate(hist) for hist in histories),
        sum(extrapolate(list(reversed(hist))) for hist in histories),
    )
