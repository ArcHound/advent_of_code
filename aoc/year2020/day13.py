# 2020-13

import logging
from aoc_lib.num_theory import iterative_crt

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    one, two = in_data.splitlines()
    buses = [x for x in two.split(",")]
    return int(one), buses


def part1(in_data, test=False):
    start, buses = parse_data(in_data)
    buses = [int(x) for x in buses if x != "x"]
    time = start
    log.debug(time)
    log.debug(buses)
    done = False
    result_bus = 0
    result_time = 0
    while not done:
        time += 1
        for b in buses:
            if time % b == 0:
                result_bus = b
                result_time = time
                done = True
                break
    return (result_time - start) * result_bus


def part2(in_data, test=False):
    start, buses = parse_data(in_data)
    offsets = [i for i in range(len(buses)) if buses[i] != "x"]
    buses = [int(x) for x in buses if x != "x"]
    tuples = [(buses[i] - offsets[i], buses[i]) for i in range(len(offsets))]
    min_min = iterative_crt(tuples)
    return min_min
