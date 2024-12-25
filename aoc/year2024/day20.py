# 2024-20

import logging
from aoc_lib.map2d import Map2d
from aoc_lib.vector2d import *
from tqdm import tqdm

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    map2d = Map2d.from_lines(in_data)
    start, end = (None, None)
    for i in range(len(map2d.obstacle_str)):
        if map2d.get_index(i) == "S":
            start = map2d.translate_index(i)
        elif map2d.get_index(i) == "E":
            end = map2d.translate_index(i)
    return map2d, start, end


def part1(in_data, test=False):
    threshold = 0
    if test:
        threshold = 10
    else:
        threshold = 100
    map2d, start, end = parse_data(in_data)
    map2d.flood(start)
    basic_len = map2d.get_flooded_point(end)
    log.debug(basic_len)
    map2d.clear_flood()
    total = 0
    # efficient? Lol no, but I can leave it running while I prep my coffee
    for i in tqdm(range(len(map2d.obstacle_str))):
        if map2d.get_index(i) == "#":
            map2d.set_index(i, ".")
            map2d.flood(start)
            if map2d.get_flooded_point(end) + threshold <= basic_len:
                total += 1
            map2d.clear_flood()
            map2d.set_index(i, "#")
    return total


def part2(in_data, test=False):
    threshold = 0
    if test:
        threshold = 50
    else:
        threshold = 100
    map2d, start, end = parse_data(in_data)
    map2d.flood(start)
    log.debug(map2d)
    basic_len = map2d.get_flooded_point(end)
    # realize that there are no crossroads
    the_path = [(i, map2d.flooded.index(i)) for i in range(basic_len)]
    total = 0
    for val, p in tqdm(the_path):
        # find all points in range of cheat
        for i in range(-20, 21):
            for j in range(-20, 21):
                walk_len = abs(i) + abs(j)
                if walk_len <= 20 and (i, j) != (0, 0):
                    new_p = v_add(map2d.translate_index(p), (i, j))
                    if not map2d.in_bounds_point(new_p):
                        continue
                    new_val = map2d.get_flooded_point(new_p)
                    # if I can land on a tile that is closer than threshold after accounting for walk
                    if new_val != -1 and new_val - val - walk_len >= threshold:
                        total += 1
    return total
