# 2024-18

import logging
from aoc_lib.map2d import Map2d

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = list()
    for line in in_data.splitlines():
        x, y = line.strip().split(",")
        data.append((int(x), int(y)))
    return data


def part1(in_data, test=False):
    if test:
        input_len = 12
        bounds = ((0, 0), (7, 7))
        end = (6, 6)
    else:
        input_len = 1024
        bounds = ((0, 0), (71, 71))
        end = (70, 70)
    start = (0, 0)
    data = parse_data(in_data)[:input_len]
    map2d = Map2d.from_obstacle_list(data, bounds)
    map2d.flood(start)
    return map2d.get_flooded_point(end)


def part2(in_data, test=False):
    if test:
        input_len = 12
        bounds = ((0, 0), (7, 7))
        end = (6, 6)
    else:
        input_len = 1024
        bounds = ((0, 0), (71, 71))
        end = (70, 70)
    start = (0, 0)
    data = parse_data(in_data)
    map2d = Map2d.from_obstacle_list(data[:input_len], bounds)
    breaking_point = None
    for i in range(input_len, len(data)):
        map2d.set_point(data[i], "#")
        map2d.flood(start)
        if map2d.get_flooded_point(end) < 0:
            breaking_point = data[i]
            break
        map2d.clear_flood()
    return f"{breaking_point[0]},{breaking_point[1]}"
