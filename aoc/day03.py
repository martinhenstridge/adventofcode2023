def parse_grid(grid):
    lines = grid.splitlines()
    numbers = {}
    symbols = {}

    for i, line in enumerate(lines):
        current = None
        for j, char in enumerate(line):
            if not char.isdigit():
                current = None
                if char != ".":
                    symbols[i, j] = char
            elif current is None:
                current = (i, j)
                numbers[current] = char
            else:
                numbers[current] += char

    return numbers, symbols


def adjacent_positions(start, length):
    i, j = start

    # left and right
    yield (i, j - 1)
    yield (i, j + length)

    # above and below
    for col in range(j - 1, j + length + 1):
        yield (i - 1, col)
        yield (i + 1, col)


def find_adjacent_symbol(symbols, start, length):
    for position in adjacent_positions(start, length):
        if position in symbols:
            return position
    return None


def run(data):
    numbers, symbols = parse_grid(data)
    gears = {position: [] for position, symbol in symbols.items() if symbol == "*"}

    sum_part_numbers = 0
    sum_gear_ratios = 0

    for start, numstr in numbers.items():
        position = find_adjacent_symbol(symbols, start, len(numstr))
        if position is None:
            continue

        num = int(numstr)
        sum_part_numbers += num

        if symbols[position] == "*":
            gears[position].append(num)

    for parts in gears.values():
        if len(parts) == 2:
            sum_gear_ratios += int(parts[0]) * int(parts[1])

    return sum_part_numbers, sum_gear_ratios
