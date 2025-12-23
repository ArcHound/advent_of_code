# 2020-17

import logging
from aoc_lib.map2d import Map2d
from aoc_lib.vector3d import *

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    map2d = Map2d.from_lines(in_data)
    alive_points = list()
    for i in range(len(map2d.obstacle_str)):
        if map2d.get_index(i) == "#":
            alive_points.append(map2d.translate_index(i))
    return [(x[0], x[1], 0) for x in alive_points]


def part1(in_data, test=False):
    data = parse_data(in_data)
    log.debug(data)
    old_active = set(data)
    active = set(data)
    reachable = set(active)
    for p in active:
        for x in nearby_cubes(p):
            reachable.add(x)
    old_reachable = set(reachable)
    for i in range(6):
        old_reachable = set(reachable)
        reachable = set()
        old_active = set(active)
        active = set()
        for p in old_reachable:
            on = sum([1 for x in nearby_cubes(p) if x in old_active])
            reachable.add(p)
            if (p in old_active and (on == 2 or on == 3)) or (
                p not in old_active and on == 3
            ):
                active.add(p)
                for x in nearby_cubes(p):
                    reachable.add(x)
    return len(active)


def nearby_cubes4(a):
    cubes = list()
    for i in range(-1, 2, 1):
        for j in range(-1, 2, 1):
            for k in range(-1, 2, 1):
                for l in range(-1, 2, 1):
                    if (i, j, k, l) != (0, 0, 0, 0):
                        cubes.append((a[0] + i, a[1] + j, a[2] + k, a[3] + l))
    return cubes


def part2(in_data, test=False):
    data = parse_data(in_data)
    data = [(x[0], x[1], x[2], 0) for x in data]
    old_active = set(data)
    active = set(data)
    reachable = set(active)
    for p in active:
        for x in nearby_cubes4(p):
            reachable.add(x)
    old_reachable = set(reachable)
    for i in range(6):
        old_reachable = set(reachable)
        reachable = set()
        old_active = set(active)
        active = set()
        for p in old_reachable:
            on = sum([1 for x in nearby_cubes4(p) if x in old_active])
            reachable.add(p)
            if (p in old_active and (on == 2 or on == 3)) or (
                p not in old_active and on == 3
            ):
                active.add(p)
                for x in nearby_cubes4(p):
                    reachable.add(x)
    return len(active)
