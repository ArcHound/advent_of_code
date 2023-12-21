# 2023-21
import logging
from aoc_lib.map2d import Map2d

log = logging.getLogger("aoc_logger")


def part1(in_data, test=False):
    STEPS = 6
    if not test:
        STEPS = 64  # for prod use-case
    map2d = Map2d.from_lines(in_data)
    log.debug(map2d)
    start = None
    for i in range(len(map2d.obstacle_str)):
        if map2d.obstacle_str[i] == "S":
            start = map2d.translate_index(i)
    log.debug(start)
    return map2d.iterative_flood_count(start, STEPS)


def part2(in_data):
    return "part2 output 2023-21"
