# 2015-02

import logging

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = list()
    for line in in_data.splitlines():
        data.append(tuple(sorted([int(x) for x in line.split("x")])))
    return data


def part1(in_data, test=False):
    data = parse_data(in_data)
    total = 0
    for a, b, c in data:
        total += 3 * a * b + 2 * b * c + 2 * a * c
    return total


def part2(in_data, test=False):
    data = parse_data(in_data)
    total = 0
    for a, b, c in data:
        total += 2 * a + 2 * b + a * b * c
    return total
