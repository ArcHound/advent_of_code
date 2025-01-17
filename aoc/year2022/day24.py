# 2022-24

import logging
from aoc_lib.map2d import Map2d
from aoc_lib.vector2d import *

log = logging.getLogger("aoc_logger")

dir_map = {">": (1, 0), "<": (-1, 0), "v": (0, 1), "^": (0, -1)}


def parse_data(in_data):
    map2d = Map2d.from_lines(in_data)
    start = None
    end = None
    blizzards = list()
    for i in range(len(map2d.obstacle_str)):
        if map2d.get_index(i) == ".":
            if start is None:
                start = map2d.translate_index(i)
            end = map2d.translate_index(i)
        if map2d.get_index(i) in dir_map:
            blizzards.append((map2d.translate_index(i), dir_map[map2d.get_index(i)]))
            map2d.set_index(i, ".")
    return map2d, start, end, blizzards


def calc_blizzard(start, b_dir, time, x_len, y_len):
    shifted = v_diff(start, (1, 1))
    moved = v_add(shifted, v_const_mult(b_dir, time))
    return ((moved[0] % x_len) + 1, (moved[1] % y_len) + 1)


def djikstra(start, end, start_time, blizzards, map2d, x_len, y_len):
    blizzard_cache = dict()
    queue = list()
    queue.append((start, start_time))
    min_time = -1
    seen_time = 0
    while len(queue) > 0:
        point, time = queue.pop(0)
        if time > seen_time:
            log.debug(time)
            seen_time = time
        if point == end and (time < min_time or min_time == -1):
            min_time = time
            continue
        if time > min_time and min_time != -1:
            continue
        if time + 1 not in blizzard_cache:
            blizzard_cache[time + 1] = [
                calc_blizzard(b[0], b[1], time + 1, x_len, y_len) for b in blizzards
            ]
        for p in map2d.nearby_points(point) + [point]:
            if map2d.get_point(p) == "#" or p in blizzard_cache[time + 1]:
                continue
            if (p, time + 1) not in queue:
                queue.append((p, time + 1))
        queue.sort(key=lambda x: x[1])
    return min_time


def part1(in_data, test=False):
    map2d, start, end, blizzards = parse_data(in_data)
    x_len = end[0]
    y_len = end[1] - 1
    min_time = djikstra(start, end, 0, blizzards, map2d, x_len, y_len)
    return min_time


def part2(in_data, test=False):
    map2d, start, end, blizzards = parse_data(in_data)
    x_len = end[0]
    y_len = end[1] - 1
    trip_1_min_time = djikstra(start, end, 0, blizzards, map2d, x_len, y_len)
    trip_2_min_time = djikstra(
        end, start, trip_1_min_time, blizzards, map2d, x_len, y_len
    )
    trip_3_min_time = djikstra(
        start, end, trip_2_min_time, blizzards, map2d, x_len, y_len
    )
    return trip_3_min_time
