# 2023-17
import logging
from aoc_lib.vector2d import *
from collections import defaultdict
import math
from heapq import heappush, heappop, heapify

import sys

sys.setrecursionlimit(10000)

log = logging.getLogger("aoc_logger")

direction_map = {
    (0, 1): [(0, 1), (1, 0), (-1, 0)],
    (1, 0): [(1, 0), (0, 1), (0, -1)],
    (0, -1): [(0, -1), (1, 0), (-1, 0)],
    (-1, 0): [(-1, 0), (0, 1), (0, -1)],
}


def in_bounds(point, x_len, y_len):
    return point[0] >= 0 and point[0] < x_len and point[1] >= 0 and point[1] < y_len


def part1(in_data):
    city_map = in_data.splitlines()
    x_len = len(city_map[0])
    y_len = len(city_map)
    max_count = 3
    start = (0, 0)
    result = -1
    fin_point = (x_len - 1, y_len - 1)
    distances = defaultdict(lambda: math.inf)
    queue = [
        (0, start, (1, 0), 0),
        (0, start, (0, 1), 0),
    ]  # first digit is the heat loss, since in python comparison of tuples starts with first item it works with heap
    heapify(queue)
    visited = set()
    while len(queue) > 0:
        loss, point, direction, dir_count = heappop(queue)
        if point == (x_len - 1, y_len - 1):  # if we're there, return -> minimum
            return loss
        if (
            point,
            direction,
            dir_count,
        ) in visited:  # if we've been there, nothing to do
            continue
        visited.add((point, direction, dir_count))
        for new_d in direction_map[direction]:
            new_point = v_add(point, new_d)
            if in_bounds(new_point, x_len, y_len):
                val = int(city_map[new_point[1]][new_point[0]])
                if new_d == direction:  # if we are continuing in the same direction
                    if dir_count + 1 <= max_count:
                        heappush(queue, (loss + val, new_point, new_d, dir_count + 1))
                    else:
                        continue
                else:
                    heappush(queue, (loss + val, new_point, new_d, 1))


def part2(in_data):
    city_map = in_data.splitlines()
    x_len = len(city_map[0])
    y_len = len(city_map)
    max_count = 10
    start = (0, 0)
    result = -1
    fin_point = (x_len - 1, y_len - 1)
    distances = defaultdict(lambda: math.inf)
    queue = [
        (0, start, (1, 0), 0),
        (0, start, (0, 1), 0),
    ]  # first digit is the heat loss, since in python comparison of tuples starts with first item it works with heap
    heapify(queue)
    visited = set()
    while len(queue) > 0:
        loss, point, direction, dir_count = heappop(queue)
        if point == (x_len - 1, y_len - 1):
            return loss
        if (point, direction, dir_count) in visited:
            continue
        visited.add((point, direction, dir_count))
        for new_d in direction_map[direction]:
            new_point = v_add(point, new_d)
            if in_bounds(new_point, x_len, y_len):
                val = int(city_map[new_point[1]][new_point[0]])
                if new_d == direction:  # if we are continuing in the same direction
                    if dir_count + 1 <= max_count:
                        if new_point == (
                            x_len - 1,
                            y_len - 1,
                        ):  # for the last point we need to check momentum
                            if dir_count + 1 >= 4:
                                heappush(
                                    queue, (loss + val, new_point, new_d, dir_count + 1)
                                )
                        else:
                            heappush(
                                queue, (loss + val, new_point, new_d, dir_count + 1)
                            )
                    else:
                        continue
                elif dir_count >= 4:  # we can turn here
                    heappush(queue, (loss + val, new_point, new_d, 1))
