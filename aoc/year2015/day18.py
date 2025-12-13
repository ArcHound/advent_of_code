# 2015-18

import logging
from aoc_lib.map2d import Map2d

log = logging.getLogger("aoc_logger")


def iteration(map2d):
    new_map = Map2d(map2d.obstacle_str, map2d.bounds, diagonal=True)
    new_map.obstacle_str = "." * len(map2d.obstacle_str)
    for i in range(len(map2d.obstacle_str)):
        point_count = sum(
            [
                1
                for p in map2d.nearby_points(map2d.translate_index(i))
                if map2d.get_point(p) == "#"
            ]
        )
        if point_count == 3 or (point_count == 2 and map2d.get_index(i) == "#"):
            new_map.set_index(i, "#")
    return new_map


def part1(in_data, test=False):
    iterations = 100
    if test:
        iterations = 4
    map2d = Map2d.from_lines(in_data, diagonal=True)
    # log.debug(map2d.debug_draw())
    for i in range(iterations):
        map2d = iteration(map2d)
        # log.debug(map2d.debug_draw())
        # log.debug('------------')
    return sum([1 for x in map2d.obstacle_str if x == "#"])


def corners(map2d):
    s, e = map2d.bounds
    s_x, s_y = s
    e_x, e_y = e
    return [(s_x, s_y), (s_x, e_y - 1), (e_x - 1, s_y), (e_x - 1, e_y - 1)]


def iteration_2(map2d):
    new_map = Map2d(map2d.obstacle_str, map2d.bounds, diagonal=True)
    new_map.obstacle_str = "." * len(map2d.obstacle_str)
    for i in range(len(map2d.obstacle_str)):
        if map2d.translate_index(i) in corners(map2d):
            new_map.set_index(i, "#")
            continue
        point_count = sum(
            [
                1
                for p in map2d.nearby_points(map2d.translate_index(i))
                if map2d.get_point(p) == "#"
            ]
        )
        if point_count == 3 or (point_count == 2 and map2d.get_index(i) == "#"):
            new_map.set_index(i, "#")
    return new_map


def part2(in_data, test=False):
    map2d = Map2d.from_lines(in_data)
    iterations = 100
    if test:
        iterations = 5
    map2d = Map2d.from_lines(in_data, diagonal=True)
    for c in corners(map2d):
        map2d.set_point(c, "#")
    log.debug(map2d.debug_draw())
    for i in range(iterations):
        map2d = iteration_2(map2d)
        log.debug(map2d.debug_draw())
        log.debug("------------")
    return sum([1 for x in map2d.obstacle_str if x == "#"])
