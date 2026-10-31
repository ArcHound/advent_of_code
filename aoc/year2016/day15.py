# 2016-15

import logging
import re
from aoc_lib.num_theory import iterative_crt

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = list()
    for line in in_data.splitlines():
        match = re.search(
            r"Disc #. has (?P<size>[0-9]*) positions; at time=0, it is at position (?P<pos>[0-9]*)",
            line.strip(),
        )
        data.append((int(match["pos"]), int(match["size"])))
    return data


def part1(in_data, test=False):
    data = parse_data(in_data)
    log.debug(data)
    counter = 1
    eqs = list()
    for a, b in data:
        eqs.append(((-a - counter + 2 * b) % b, b))
        counter += 1
    log.debug(eqs)
    t = iterative_crt(eqs)
    return t


def part2(in_data, test=False):
    data = parse_data(in_data)
    counter = 1
    eqs = list()
    for a, b in data:
        eqs.append(((-a - counter + 2 * b) % b, b))
        counter += 1
    eqs.append(((0 - counter + 2 * 11) % 11, 11))
    t = iterative_crt(eqs)
    return t
