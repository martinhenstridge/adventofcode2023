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


def candidates(costs, position):
    for move in MOVES:
        candidate = (position[0] + move[0], position[1] + move[1])
        if candidate not in costs:
            continue
        yield candidate, move


def find_path(costs, start, goal):
    best = {p: 0xffffffff for p in costs}
    best[start] = 0
    for c, m in candidates(costs, start):
        print(c, m)

    pending = []
    heapq.heappush(pending, (0, start, []))

    while pending:
        _, pos, moves = heapq.heappop(pending)
        if pos == goal:
            print(pos)
            print(moves)
            break

        print("considering", pos, moves)

        cumcost = best[pos]
        for new_pos, new_move in candidates(costs, pos):
            new_moves = moves[:] + [new_move]
            if len(new_moves) > 3 and all(m == new_move for m in new_moves[-4:-1]):
                cost = cumcost + 0xffffffff
            else:
                cost = cumcost + costs[new_pos]
            heapq.heappush(pending, (cost, new_pos, new_moves))
        input()

    return best[goal]


def run(data):
    data = DATA
    size, costs = parse_costs(data)
    print(size, costs)
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
