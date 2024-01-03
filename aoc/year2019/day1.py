# 2019-1
import logging
import math

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = list()
    for line in in_data.splitlines():
        data.append(int(line))
    return data


def mass(a):
    return math.floor(a / 3) - 2


def part1(in_data):
    data = parse_data(in_data)
    return sum([mass(x) for x in data])


def recursive_mass(a):
    a_mass = mass(a)
    if a_mass <= 0:
        return 0
    else:
        return a_mass + recursive_mass(a_mass)


def part2(in_data):
    data = parse_data(in_data)
    return sum([recursive_mass(x) for x in data])
