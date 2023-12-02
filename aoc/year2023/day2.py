# 2023-2
import logging
import dataclasses

log = logging.getLogger("aoc_logger")


@dataclasses.dataclass
class Game:
    g_id: int
    rounds: list[dict]

def parse(in_data):
    games = list()
    for line in in_data.splitlines():
        g = line.split(':')[0]
        r = line.split(':')[1]
        g_id = int(g.split(' ')[1])
        rounds = list()
        for _round in r.split(';'):
            colors = {"red":0, "green":0, "blue":0}
            for elem in _round.split(','):
                b = int(elem.split(' ')[1])
                c = elem.split(' ')[2]
                colors[c]+=b
            rounds.append(colors)
        games.append(Game(g_id=g_id, rounds=rounds))
    return games

def possible_game(game):
    cond = {"red":12, "green":13, "blue":14}
)
    return False not in [max([r[color] for r in game.rounds])<=cond[color] for color in cond]

def power_of_game(game):
    power = 1
    for n in [max([r[color] for r in game.rounds]) for color in ["red", "green", "blue"]]:
        power *= n
    return power


def part1(in_data):
    games = parse(in_data)
    return sum([game.g_id for game in games if possible_game(game)])

def part2(in_data):
    games = parse(in_data)
    return sum([power_of_game(game) for game in games])
