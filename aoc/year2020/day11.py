# 2020-11

import logging
from aoc_lib.map2d import Map2d

log = logging.getLogger("aoc_logger")


def part1(in_data, test=False):
    map2d = Map2d.from_lines(in_data, diagonal=True)
    map_len = len(map2d.obstacle_str)
    buf = [map2d.get_index(i) for i in range(map_len)]
    log.debug(map2d.debug_draw())
    log.debug(buf)
    movement = True
    while movement:
        movement = False
        new_buf = list(buf)
        for i in range(map_len):
            if buf[i] == "L":
                if sum([1 for j in map2d.nearby_indexes(i) if buf[j] == "#"]) == 0:
                    new_buf[i] = "#"
                    movement = True
            elif buf[i] == "#":
                if sum([1 for j in map2d.nearby_indexes(i) if buf[j] == "#"]) >= 4:
                    new_buf[i] = "L"
                    movement = True
        buf = new_buf
    return sum([1 for j in range(map_len) if buf[j] == "#"])


def part2(in_data, test=False):
    map2d = Map2d.from_lines(in_data, diagonal=True)
    map_len = len(map2d.obstacle_str)
    neighbors = dict()
    directions = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]
    for i in range(map_len):
        if map2d.obstacle_str[i] == "L":
            point = map2d.translate_index(i)
            neighbors[i] = list()
            for d in directions:
                line = map2d.trace(point, d, False)
                for x in line[1:]:
                    if map2d.get_point(x) == "L":
                        neighbors[i].append(map2d.translate_point(x))
                        break
    movement = True
    buf = [map2d.get_index(i) for i in range(map_len)]
    log.debug(neighbors)
    while movement:
        movement = False
        new_buf = list(buf)
        for i in range(map_len):
            if buf[i] == "L":
                if sum([1 for j in neighbors[i] if buf[j] == "#"]) == 0:
                    new_buf[i] = "#"
                    movement = True
            elif buf[i] == "#":
                if sum([1 for j in neighbors[i] if buf[j] == "#"]) >= 5:
                    new_buf[i] = "L"
                    movement = True
        count = 0
        dbuf = ""
        for i in range(map_len):
            dbuf += new_buf[i]
            if i % 10 == 9:
                dbuf += "\n"
        log.debug(dbuf)
        buf = new_buf
    return sum([1 for j in range(map_len) if buf[j] == "#"])
