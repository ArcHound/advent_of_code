# 2019-24
import logging
from aoc_lib.map2d import Map2d

log = logging.getLogger("aoc_logger")


def transform(data):
    new_obst_str = list()
    for i in range(len(data.obstacle_str)):
        bug_count = 0
        for j in data.nearby_indexes(i):
            if data.obstacle_str[j] == "#":
                bug_count += 1
        if data.obstacle_str[i] == ".":
            if bug_count == 1 or bug_count == 2:
                new_obst_str.append("#")
            else:
                new_obst_str.append(".")
        elif data.obstacle_str[i] == "#":
            if bug_count != 1:
                new_obst_str.append(".")
            else:
                new_obst_str.append("#")
    return Map2d("".join(new_obst_str), data.bounds, diagonal=False)


def part1(in_data, test=False):
    map2d = Map2d.from_lines(in_data, diagonal=False)
    layouts = list()
    log.debug(map2d.debug_draw())
    # countdown = 5
    while map2d.obstacle_str not in layouts:
        layouts.append(map2d.obstacle_str)
        map2d = transform(map2d)
        # log.debug(map2d.debug_draw())
        # countdown -=1
        # if countdown == 0:
        #     break
    log.debug(map2d.debug_draw())
    eval_obst_str = sum(
        [
            pow(2, i)
            for i in range(len(map2d.obstacle_str))
            if map2d.obstacle_str[i] == "#"
        ]
    )
    return eval_obst_str


def part2(in_data, test=False):
    map2d = Map2d.from_lines(in_data)
    return "part2 output 2019-24"
