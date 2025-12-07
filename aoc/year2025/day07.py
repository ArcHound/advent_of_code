# 2025-07

import logging
from aoc_lib.map2d import Map2d

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    map2d = Map2d.from_lines(in_data)
    start = None
    splitters = list()
    for i in range(len(map2d.obstacle_str)):
        if map2d.get_index(i) == "S":
            start = map2d.translate_index(i)
        elif map2d.get_index(i) == "^":
            splitters.append(map2d.translate_index(i))
    return map2d, start, splitters


def part1(in_data, test=False):
    map2d, start, splitters = parse_data(in_data)
    log.debug(map2d.debug_draw())
    log.debug(start)
    log.debug(splitters)
    beams = {start[0]}
    splits = 0
    for i in range(map2d.bounds[0][1], map2d.bounds[1][1]):
        log.debug(i)
        new_beams = set()
        for beam in beams:
            if (beam, i) in splitters:
                splits += 1
                new_beams.add(beam - 1)
                new_beams.add(beam + 1)
            else:
                new_beams.add(beam)
        beams = new_beams
    return splits


def part2(in_data, test=False):
    map2d, start, splitters = parse_data(in_data)
    cache = dict()
    for i in range(map2d.bounds[1][1] - 1, map2d.bounds[0][1], -1):
        for j in range(map2d.bounds[0][0], map2d.bounds[1][0]):
            if (j, i) in splitters:
                sp_left = 1
                left_done = False
                sp_right = 1
                right_done = False
                for k in range(i, map2d.bounds[1][1]):
                    if (j - 1, k) in splitters and not left_done:
                        sp_left = cache[(j - 1, k)]
                        left_done = True
                    if (j + 1, k) in splitters and not right_done:
                        sp_right = cache[(j + 1, k)]
                        right_done = True
                    if left_done and right_done:
                        break
                cache[(j, i)] = sp_left + sp_right
    first_splitter = sorted(splitters, key=lambda x: x[1])[0]
    log.debug(first_splitter)
    return cache[first_splitter]
