# 2015-03

import logging
from aoc_lib.vector2d import *

log = logging.getLogger("aoc_logger")

v_map = {
    "^": (0, -1),
    "v": (0, 1),
    "<": (-1, 0),
    ">": (1, 0),
}


def part1(in_data, test=False):
    cache = set()
    point = (0, 0)
    for c in in_data.strip():
        point = v_add(point, v_map[c])
        cache.add(point)
    return len(cache)


def part2(in_data, test=False):
    cache = set()
    point_s = (0, 0)
    point_r = (0, 0)
    state = "r"
    for c in in_data.strip():
        if state == "r":
            state = "s"
            point_s = v_add(point_s, v_map[c])
            cache.add(point_s)
        elif state == "s":
            state = "r"
            point_r = v_add(point_r, v_map[c])
            cache.add(point_r)
    return len(cache)
