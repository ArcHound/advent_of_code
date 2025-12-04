# 2025-04

import logging
from aoc_lib.map2d import Map2d

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    in_data = in_data.replace("@", "#")
    map2d = Map2d.from_lines(in_data, diagonal=True)
    return map2d


def part1(in_data, test=False):
    map2d = parse_data(in_data)
    log.debug(map2d.debug_draw())
    count = 0
    for i in range(len(map2d.obstacle_str)):
        if map2d.get_index(i) != "#":
            continue
        point_count = 0
        for j in map2d.nearby_indexes(i):
            if map2d.get_index(j) == "#":
                point_count += 1
        if point_count < 4:
            log.debug(map2d.translate_index(i))
            count += 1
    return count


def part2(in_data, test=False):
    map2d = parse_data(in_data)
    log.debug(map2d.debug_draw())
    count = 0
    starting_rolls = sum([1 for c in map2d.obstacle_str if c == "#"])
    movement = True
    while movement:
        movement = False
        for i in range(len(map2d.obstacle_str)):
            if map2d.get_index(i) != "#":
                continue
            point_count = 0
            for j in map2d.nearby_indexes(i):
                if map2d.get_index(j) == "#":
                    point_count += 1
            if point_count < 4:
                map2d.set_index(i, ".")
                movement = True
    return starting_rolls - sum([1 for c in map2d.obstacle_str if c == "#"])
