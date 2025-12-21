# 2020-06

import logging
from collections import Counter

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = list()
    buf = ""
    for line in in_data.splitlines():
        if line.strip() == "":
            data.append(buf.strip())
            buf = ""
        else:
            buf += " " + line.strip()
    data.append(buf.strip())
    return data


def part1(in_data, test=False):
    data = parse_data(in_data)
    return sum([sum([1 for y in Counter(x).keys() if y != " "]) for x in data])


def part2(in_data, test=False):
    data = parse_data(in_data)
    return sum(
        [
            sum(
                [
                    1
                    for y in Counter(x).keys()
                    if y != " " and Counter(x)[y] == len(x.split(" "))
                ]
            )
            for x in data
        ]
    )
