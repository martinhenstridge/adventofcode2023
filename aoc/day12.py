import enum


def parse_line(line, unfold=False):
    cs, gs = line.split()
    if unfold:
        cs = "?".join([cs] * 5)
        gs = ",".join([gs] * 5)
    return list(cs), tuple(int(g) for g in gs.split(","))


def find_groups(conditions):
    count = 0
    for c in conditions:
        if c == "?":
            return
        if c == "#":
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

    conditions[u] = "."
    count += count_combinations(conditions, groups, unknowns)
    conditions[u] = "#"
    count += count_combinations(conditions, groups, unknowns)
    conditions[u] = "?"

    return count


def run(data):
    #data = DATA
    total = 0
    for line in data.splitlines():
        conditions, groups = parse_line(line)
        #print(conditions, groups)
        #input()
        #print("==")
        #print(conditions, groups)
        #print("==")
        unknowns = [i for i, c in enumerate(conditions) if c == "?"]
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
