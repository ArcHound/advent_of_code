# 2015-24

import logging
from itertools import combinations

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = list()
    for line in in_data.splitlines():
        data.append(int(line.strip()))
    return data


def prod(combo):
    result = 1
    for c in combo:
        result *= c
    return result


def balance(items, count):
    group_size = sum(items) // count
    found_one = False
    cb = list()
    for i in range(2, (len(items) // count) + 1):
        for c in combinations(items, i):
            if sum(c) == group_size:
                found_one = True
                cb.append(c)
        if found_one:
            break
    return min([prod(x) for x in cb])


def part1(in_data, test=False):
    data = parse_data(in_data)
    return balance(data, 3)


def part2(in_data, test=False):
    data = parse_data(in_data)
    return balance(data, 4)
