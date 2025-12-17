# 2020-03

import logging
from aoc_lib.map2d import Map2d

log = logging.getLogger("aoc_logger")


def count_slope(start, change, map2d):
    point = start
    bounds = map2d.bounds
    count = 0
    while point[1] < bounds[1][1]:
        if map2d.get_point(point) == "#":
            count += 1
        point = ((point[0] + change[0]) % bounds[1][0], point[1] + change[1])
    return count


def part1(in_data, test=False):
    map2d = Map2d.from_lines(in_data)
    point = (0, 0)
    change = (3, 1)
    return count_slope(point, change, map2d)


def part2(in_data, test=False):
    map2d = Map2d.from_lines(in_data)
    prod = 1
    point = (0, 0)
    for change in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]:
        count = count_slope(point, change, map2d)
        prod *= count
    return prod
