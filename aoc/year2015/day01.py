# 2015-01

import logging

log = logging.getLogger("aoc_logger")


def part1(in_data, test=False):
    count = 0
    for c in in_data:
        if c == "(":
            count += 1
        elif c == ")":
            count -= 1
    return count


def part2(in_data, test=False):
    count = 0
    result = 0
    for i in range(len(in_data)):
        c = in_data[i]
        if c == "(":
            count += 1
        elif c == ")":
            count -= 1
        if count == -1:
            result = i + 1
            break
    return result
