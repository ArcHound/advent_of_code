# 2016-20

import logging
from aoc_lib.interval import Interval

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = list()
    for line in in_data.splitlines():
        a, b = line.strip().split("-")
        data.append(Interval(int(a), int(b) + 1))
    return data


def part1(in_data, test=False):
    data = parse_data(in_data)
    new_list = Interval.join_list(data)
    return new_list[0].end


def part2(in_data, test=False):
    data = parse_data(in_data)
    new_list = Interval.join_list(data)
    end_end = 4294967295
    counter = 0
    log.error(new_list)
    for i in range(len(new_list) - 1):
        diff = new_list[i + 1].start - new_list[i].end
        counter += diff
    counter += end_end - new_list[-1].end
    return counter + 1  # I don't even know where I've lost this one.
    # Fuck off by one error, all my homies hate off by one errors.
