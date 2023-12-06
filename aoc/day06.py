import math


def parse_separate(data):
    lines = data.splitlines()
    time_line = lines[0].split()
    dist_line = lines[1].split()
    for t, d in zip(time_line[1:], dist_line[1:]):
        yield int(t), int(d)


def parse_combined(data):
    lines = data.splitlines()
    time_line = lines[0].split()
    dist_line = lines[1].split()
    yield int("".join(time_line[1:])), int("".join(dist_line[1:]))


def min_max_button_times(t, d):
    # t - race time
    # d - distance travelled
    # b - time spend holding button
    #
    # d = b * (t - b)  =>  b^2 - t*b - d = 0
    #
    # Solve using quadratic formula to get values of b to exactly match
    # record. Shift the smaller value up slightly and the larger value
    # down slightly to get to the nearest integer button times which
    # result in exceeding the record.

    sqrt = math.sqrt(t * t - 4 * d)
    b1 = (t + sqrt) / 2
    b2 = (t - sqrt) / 2
    bmin, bmax = sorted([b1, b2])
    return math.floor(bmin + 1), math.ceil(bmax - 1)


def count_ways(data, parser):
    product = 1
    for t, d in parser(data):
        bmin, bmax = min_max_button_times(t, d)
        product *= 1 + bmax - bmin
    return product


def run(data):
    ways_separate = count_ways(data, parse_separate)
    ways_combined = count_ways(data, parse_combined)

    return ways_separate, ways_combined
