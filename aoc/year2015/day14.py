# 2015-14

import logging
import re
from dataclasses import dataclass

log = logging.getLogger("aoc_logger")

ex_pattern = "(?P<name>[A-Z][a-z]*) can fly (?P<speed>[0-9]*) km/s for (?P<hold>[0-9]*) seconds, but then must rest for (?P<rest>[0-9]*) seconds."


@dataclass
class Reindeer:
    name: str
    speed: int
    hold: int
    rest: int


def parse_data(in_data):
    data = dict()
    for line in in_data.splitlines():
        match = re.search(ex_pattern, line.strip())
        name = match.group("name")
        speed = int(match.group("speed"))
        hold = int(match.group("hold"))
        rest = int(match.group("rest"))
        data[name] = Reindeer(name, speed, hold, rest)
    return data


def calc_distance(r, duration):
    cycles = duration // (r.hold + r.rest)
    remainder = duration % (r.hold + r.rest)
    if remainder > r.hold:
        remainder = r.hold
    return cycles * r.hold * r.speed + remainder * r.speed


def part1(in_data, test=False):
    duration = 2503
    if test:
        duration = 1000
    data = parse_data(in_data)
    max_distance = 0
    for reindeer in data:
        d = calc_distance(data[reindeer], duration)
        if d > max_distance:
            max_distance = d
    return max_distance


def part2(in_data, test=False):
    duration = 2503
    if test:
        duration = 1000
    data = parse_data(in_data)
    scoreboard = {x: 0 for x in data}
    for i in range(duration):
        leaders = list()
        dist = 0
        for reindeer in data:
            d = calc_distance(data[reindeer], i + 1)
            if d > dist:
                leaders = [reindeer]
                dist = d
            elif d == dist:
                leaders.append(reindeer)
        for leader in leaders:
            scoreboard[leader] += 1
    log.debug(scoreboard)
    return max([v for k, v in scoreboard.items()])
