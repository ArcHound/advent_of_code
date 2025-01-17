# 2022-18

import logging
from aoc_lib.vector3d import *

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = list()
    for line in in_data.splitlines():
        x, y, z = line.strip().split(",")
        data.append(Point3d(int(x), int(y), int(z)))
    return data


def part1(in_data, test=False):
    data = parse_data(in_data)
    total = 0
    for p in data:
        for x in v_touches_squares(p):
            if x not in data:
                total += 1
    return total


def in_bounds(p, bounds):
    return (
        bounds[0][0] <= p[0]
        and p[0] < bounds[1][0]
        and bounds[0][1] <= p[1]
        and p[1] < bounds[1][1]
        and bounds[0][2] <= p[2]
        and p[2] < bounds[1][2]
    )


def part2(in_data, test=False):
    data = parse_data(in_data)
    bounds = (Point3d(-1, -1, -1), Point3d(25, 25, 25))
    queue = list()
    queue.append(Point3d(-1, -1, -1))
    visited = set()
    visited.add(Point3d(-1, -1, -1))
    total = 0
    while len(queue) > 0:
        p = queue.pop(0)
        for q in v_touches_squares(p):
            if in_bounds(q, bounds) and q not in visited and q not in data:
                queue.append(q)
                visited.add(q)
            elif q in data:
                total += 1
    return total
