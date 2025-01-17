# 2022-14

import logging
from aoc_lib.map2d import Map2d
from aoc_lib.vector2d import *

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    obstacles = set()
    for line in in_data.splitlines():
        path = line.strip().split(" -> ")
        points = [(int(x.split(",")[0]), int(x.split(",")[1])) for x in path]
        for i in range(len(points) - 1):
            s = points[i]
            f = points[i + 1]
            for x in range(min((s[0], f[0])), max((s[0], f[0])) + 1):
                for y in range(min((s[1], f[1])), max((s[1], f[1])) + 1):
                    obstacles.add((x, y))
    proto = Map2d.from_obstacle_list(list(obstacles))
    s, f = proto.bounds
    x, y = s
    bounds = ((x - 1, 0), f)
    return Map2d.from_obstacle_list(list(obstacles), bounds=bounds), obstacles


def pour_sand(map2d, pouring_point):
    new_grain = True
    down = (0, 1)
    down_left = (-1, 1)
    down_right = (1, 1)
    while new_grain:
        movement = True
        new_grain = False
        particle = pouring_point
        while movement:
            if map2d.get_point(pouring_point) != ".":
                break
            lookahead = v_add(particle, down)
            if not map2d.in_bounds_point(lookahead):
                break
            if map2d.get_point(lookahead) == ".":
                particle = lookahead
            else:
                look2 = v_add(particle, down_left)
                look3 = v_add(particle, down_right)
                if map2d.get_point(look2) == ".":
                    particle = look2
                elif map2d.get_point(look3) == ".":
                    particle = look3
                else:
                    new_grain = True
                    movement = False
                    map2d.set_point(particle, "o")


def part1(in_data, test=False):
    map2d, _ = parse_data(in_data)
    pour_sand(map2d, (500, 0))
    log.debug(map2d)
    return sum([1 for x in map2d.obstacle_str if x == "o"])


def part2(in_data, test=False):
    map2d, obstacles = parse_data(in_data)
    s, f = map2d.bounds
    fx, fy = f
    for i in range(1000):
        obstacles.add((i, fy + 1))
    new_map = map2d.from_obstacle_list(list(obstacles), bounds=((0, 0), (1000, fy + 2)))
    pour_sand(new_map, (500, 0))
    return sum([1 for x in new_map.obstacle_str if x == "o"])
