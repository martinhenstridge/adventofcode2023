import collections
import heapq
import math
from enum import Enum


class Move(Enum):
    U = (-1, 0)
    D = (+1, 0)
    L = (0, -1)
    R = (0, +1)

    def __lt__(self, other):
        return self.value < other.value


def parse_costs(data):
    lines = data.splitlines()
    return len(lines), {
        (row, col): int(char)
        for row, line in enumerate(lines)
        for col, char in enumerate(line)
    }


def candidate_moves(heading):
    match heading:
        case Move.U | Move.D:
            yield from (Move.L, Move.R)
        case Move.L | Move.R:
            yield from (Move.U, Move.D)
        case _:
            yield from (Move.U, Move.D, Move.L, Move.R)


def candidates(costs, position, heading, min_steps, max_steps):
    for move in candidate_moves(heading):
        r, c = position
        dr, dc = move.value
        cost = 0
        for step in range(1, max_steps + 1):
            r += dr
            c += dc
            try:
                cost += costs[r, c]
            except KeyError:
                break
            if step >= min_steps:
                yield (r, c), move, cost


def find_lowest_cost_path(costs, start, goal, min_steps, max_steps):
    result = math.inf
    best = collections.defaultdict(lambda: math.inf)
    best[(start, None)] = 0

    pending = []
    heapq.heappush(pending, (0, start, None))

    while pending:
        cost, position, heading = heapq.heappop(pending)
        if position == goal:
            if cost < result:
                result = cost
            continue

        for next_position, next_heading, step_cost in candidates(
            costs, position, heading, min_steps, max_steps
        ):
            cost = best[position, heading] + step_cost
            if cost < best[next_position, next_heading]:
                best[next_position, next_heading] = cost
                heapq.heappush(pending, (cost, next_position, next_heading))

    return result


def run(data):
    size, costs = parse_costs(data)

    cost_normal = find_lowest_cost_path(
        costs, start=(0, 0), goal=(size - 1, size - 1), min_steps=0, max_steps=3
    )
    cost_ultra = find_lowest_cost_path(
        costs, start=(0, 0), goal=(size - 1, size - 1), min_steps=4, max_steps=10
    )

    return cost_normal, cost_ultra
