# 2025-05

import logging
from aoc_lib.interval import Interval

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    intervals = list()
    data = list()
    for line in in_data.splitlines():
        if "-" in line.strip():
            a = int(line.strip().split("-")[0])
            b = int(line.strip().split("-")[1]) + 1
            intervals.append(Interval(a, b))
        elif len(line.strip()) > 0:
            a = int(line.strip())
            data.append(a)
    return intervals, data


def part1(in_data, test=False):
    intervals, data = parse_data(in_data)
    count = 0
    for num in data:
        log.debug(num)
        got = False
        for i in intervals:
            log.debug(i)
            if i.contains_val(num):
                got = True
                break
        if got:
            count += 1
    return count


def part2(in_data, test=False):
    intervals, data = parse_data(in_data)
    joined = Interval.join_list(intervals)
    total = 0
    for i in joined:
        total += i.length()
    return total
