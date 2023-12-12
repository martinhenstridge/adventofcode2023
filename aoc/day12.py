import enum


def parse_springs(data):
    for line in data.splitlines():
        conditions, groups = line.split()
        yield bytearray(ord(c) for c in conditions), tuple(int(g) for g in groups.split(","))


def find_groups(conditions):
    count = 0
    for c in conditions:
        if c == ord("?"):
            return
        if c == ord("#"):
            count += 1
        elif count:
            yield count
            count = 0
    if count:
        yield count


def acceptable(conditions, groups, unknowns):
    found = tuple(find_groups(conditions))
    if len(found) > len(groups):
        return False

    for actual, expected in zip(found, groups):
        #print(expected, actual)
        if actual != expected:
            return False

    return len(found) == len(groups) or unknowns


def count_combinations(conditions, groups, unknowns):
    #print("!", conditions, groups, unknowns)
    if not acceptable(conditions, groups, unknowns):
        #print("no")
        return 0
    elif not unknowns:
        #print("match!", conditions)
        return 1

    u, unknowns = unknowns[0], unknowns[1:]
    count = 0

    #conditions[u] = ord(".")
    count += count_combinations(conditions.replace(b"?", b".", 1), groups, unknowns)
    #conditions[u] = ord("#")
    count += count_combinations(conditions.replace(b"?", b"#", 1), groups, unknowns)

    return count


def run(data):
    #data = DATA
    total = 0
    for conditions, groups in parse_springs(data):
        #print("==")
        #print(conditions, groups)
        #print("==")
        unknowns = [i for i, c in enumerate(conditions) if c == ord("?")]
        count = count_combinations(conditions, groups, unknowns)
        #print(">>>", count)
        total += count
    return total, 0


DATA = """\
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""
