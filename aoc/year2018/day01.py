# 2018-01

import logging

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = list()
    for line in in_data.splitlines():
        data.append(int(line.strip()))
    return data


def part1(in_data, test=False):
    data = parse_data(in_data)
    return sum(data)


def part2(in_data, test=False):
    data = parse_data(in_data)
    return "part2 output 2018-01"
