import heapq
from enum import Enum

MOVES = [
    (-1, 0),
    (+1, 0),
    (0, -1),
    (0, +1),
]

class Move(Enum):
    U = (-1, 0)
    D = (+1, 0)
    L = (0, -1)
    R = (0, +1)


def parse_costs(data):
    lines = data.splitlines()
    return len(lines), {
        (r, c): int(char) for r, line in enumerate(lines) for c, char in enumerate(line)
    }


def candidates(costs, pos, path):
    for move in Move:
        if len(path) > 2 and all(m == move for m in path[-3:]):
            continue
        new_pos = (pos[0] + move.value[0], pos[1] + move.value[1])
        if new_pos not in costs:
            continue
        yield new_pos, (*path, move)


def find_path(costs, start, goal):
    best = {p: 0xffffffff for p in costs}
    best[start] = 0

    pending = []
    heapq.heappush(pending, (0, start, tuple()))

    while pending:
        _, pos, path = heapq.heappop(pending)
        if pos == goal:
            continue

        #print("considering", _, pos, [p.name for p in path])

        for new_pos, new_path in candidates(costs, pos, path):
            cost = best[pos] + costs[new_pos]
            if cost < best[new_pos] or (cost == best[new_pos] and new_path:
                best[new_pos] = cost
                heapq.heappush(pending, (cost, new_pos, new_path))

    for k, v in best.items():
        print(k, v)

    return best[goal]


def run(data):
    data = DATA
    size, costs = parse_costs(data)
    cost = find_path(costs, (0, 0), (size - 1, size - 1))
    return 0, 0


DATA = """\
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""
