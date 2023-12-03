import collections
import re


def parse_game_id(string):
    match = re.match(r"Game (\d+):", string)
    return int(match[1])


def parse_pick(string):
    return {
        match[2]: int(match[1])
        for match in re.finditer(r"(\d+) (red|blue|green)", string)
    }


def parse_games(data):
    games = {}
    for line in data.splitlines():
        game_id = parse_game_id(line)
        picks = [parse_pick(pick) for pick in line.split(";")]
        games[game_id] = picks
    return games


def game_possible(criteria, picks):
    for pick in picks:
        for colour, count in pick.items():
            if count > criteria[colour]:
                return False
    return True


def minimum_set_power(picks):
    minimum = collections.defaultdict(int)
    for pick in picks:
        for colour, count in pick.items():
            if count > minimum[colour]:
                minimum[colour] = count
    return minimum["red"] * minimum["green"] * minimum["blue"]


def run(data):
    games = parse_games(data)

    possible_total = sum(
        game_id
        for game_id, picks in games.items()
        if game_possible({"red": 12, "green": 13, "blue": 14}, picks)
    )
    power_total = sum(minimum_set_power(picks) for picks in games.values())

    return possible_total, power_total
