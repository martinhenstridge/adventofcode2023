from functools import cache


def parse_line(line):
    cs, gs = line.split()
    return cs, tuple(int(g) for g in gs.split(","))


@cache
def count_arrangements(conditions, groups):
    # Credit to https://github.com/Domyy95/Challenges/blob/master/2023-12-Advent-of-code/12.py

    if not groups:
        return 0 if "#" in conditions else 1
    if not conditions:
        return 0 if groups else 1

    count = 0

    if conditions[0] in ".?":
        count += count_arrangements(conditions[1:], groups)

    if conditions[0] in "#?":
        group, remaining_groups = groups[0], groups[1:]
        if (
            group <= len(conditions)
            and "." not in conditions[:group]
            and (group == len(conditions) or conditions[group] != "#")
        ):
            count += count_arrangements(conditions[group + 1 :], remaining_groups)

    return count


def run(data):
    total_folded = 0
    total_unfolded = 0

    for line in data.splitlines():
        conditions, groups = parse_line(line)
        total_folded += count_arrangements(conditions, groups)

        conditions = "?".join([conditions] * 5)
        groups = groups * 5
        total_unfolded += count_arrangements(conditions, groups)

    return total_folded, total_unfolded
