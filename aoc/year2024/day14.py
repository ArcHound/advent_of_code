# 2024-14

import logging
from collections import defaultdict

from aoc_lib.vector2d import *
from aoc_lib.map2d import Map2d
from tqdm import tqdm

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = list()
    for line in in_data.splitlines():
        p, v = line.split(" ")
        p_x, p_y = p[2:].split(",")
        v_x, v_y = v[2:].split(",")
        data.append(((int(p_x), int(p_y)), (int(v_x), int(v_y))))
    return data


def move(position, velocity, bounds):
    return (
        (position[0] + velocity[0]) % bounds[0][1],
        (position[1] + velocity[1]) % bounds[1][1],
    )


def quadrants(bounds):
    a = (bounds[0][1] - 1) // 2
    b = (bounds[1][1] - 1) // 2
    c = bounds[0][1]
    d = bounds[1][1]
    return [
        ((0, a), (0, b)),
        ((0, a), (b + 1, d)),
        ((a + 1, c), (0, b)),
        ((a + 1, c), (b + 1, d)),
    ]


def part1(in_data, test=False):
    bounds = None
    if test:
        bounds = ((0, 11), (0, 7))
    else:
        bounds = ((0, 101), (0, 103))
    qs = quadrants(bounds)
    data = parse_data(in_data)
    moved = list()
    for p, v in data:
        position = p
        for i in range(100):
            position = move(position, v, bounds)
        moved.append(position)
    quad_dict = defaultdict(int)
    for p in moved:
        for q in qs:
            if (
                q[0][0] <= p[0]
                and p[0] < q[0][1]
                and q[1][0] <= p[1]
                and p[1] < q[1][1]
            ):
                quad_dict[q] += 1
    total = 1
    for q in qs:
        total *= quad_dict[q]
    return total


def part2(in_data, test=False):
    bounds = None
    if test:
        bounds = ((0, 11), (0, 7))
    else:
        bounds = ((0, 101), (0, 103))
    map_bounds = (
        (bounds[0][0], bounds[1][0]),
        (bounds[0][1], bounds[1][1]),
    )  # historical reasons :facepalm:
    data = parse_data(in_data)
    for i in tqdm(range(0, 10000)):
        new_data = list()
        to_map = list()
        for p, v in data:
            position = move(p, v, bounds)
            new_data.append((position, v))
            to_map.append(position)
        map2d = Map2d.from_obstacle_list(to_map, map_bounds)
        if "##################" in map2d.obstacle_str:
            log.critical(map2d.debug_draw())
            return i + 1
        data = new_data
    return "Can't find it :("
