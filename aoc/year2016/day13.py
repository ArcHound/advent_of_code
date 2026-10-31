# 2016-13

import logging
from aoc_lib.map2d import Map2d

log = logging.getLogger("aoc_logger")


def prepare_map(num, map_size=50):
    map2d = Map2d("." * map_size * map_size, ((0, 0), (map_size, map_size)))
    for i in range(map_size):
        for j in range(map_size):
            v = i * i + 3 * i + 2 * i * j + j + j * j + num
            if sum([1 for x in bin(v) if x == "1"]) % 2 != 0:
                map2d.set_point((i, j), "#")
    return map2d


def part1(in_data, test=False):
    start = (1, 1)
    target = (31, 39) if not test else (7, 4)
    num = int(in_data.strip())
    map2d = prepare_map(num)
    map2d.flood(start)
    return map2d.get_flooded_point(target)


def part2(in_data, test=False):
    start = (1, 1)
    num = int(in_data.strip())
    map2d = prepare_map(num)
    map2d.flood(start)
    log.debug(map2d.debug_draw())
    final_points = sum(
        [
            1
            for i in range(len(map2d.obstacle_str))
            if map2d.get_flooded_index(i) <= 50 and map2d.get_flooded_index(i) >= 0
        ]
    )
    return final_points
