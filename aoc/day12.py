import enum


def parse_springs(data):
    for line in data.splitlines():
        conditions, groups = line.split()
        yield bytearray(ord(c) for c in conditions), tuple(int(g) for g in groups.split(","))


def find_groups(conditions):
    groups = []
    count = 0
    for c in conditions:
        if c == ord("#"):
            count += 1
        elif count:
            groups.append(count)
            count = 0
    if count:
        groups.append(count)
    return tuple(groups)


def acceptable(conditions, groups, unknowns):
    if unknowns:
        return True
    actual = find_groups(conditions)
    match = (actual == groups)
    #print(conditions, groups, actual, match)
    return match


def count_assuming(conditions, groups, unknowns, i, c):
    conditions[i] = c


def count_combinations(conditions, groups, unknowns):
    #print("!", conditions, groups, unknowns)
    if not acceptable(conditions, groups, unknowns):
        return 0
    elif not unknowns:
        return 1

    u, unknowns = unknowns[0], unknowns[1:]

    count = 0
    #print("0", conditions)
    conditions[u] = ord(".")
    #print("1", conditions)
    count += count_combinations(conditions, groups, unknowns)
    conditions[u] = ord("#")
    count += count_combinations(conditions, groups, unknowns)
    return count


def run(data):
    #data = DATA
    total = 0
    for conditions, groups in parse_springs(data):
        #print("==")
        #print(conditions, groups)
        #print("==")
        unknowns = [i for i, c in enumerate(conditions) if c == ord("?")]
        total += count_combinations(conditions, groups, unknowns)
        #input()
    return total, 0


DATA = """\
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""
