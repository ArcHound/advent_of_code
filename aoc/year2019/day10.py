# 2019-10
import logging
from aoc_lib.map2d import Map2d
import math

log = logging.getLogger("aoc_logger")


def ray_trace_from_point(map2d, start):
    seen_vectors = set()
    seen_obstacles = 0
    obst_list = list()
    for i in range(len(map2d.obstacle_str)):
        end = map2d.translate_index(i)
        if start[0] == end[0] and start[1] == end[1]:
            continue
        vector = (end[0] - start[0], end[1] - start[1])
        norm_vector = (
            vector[0] // math.gcd(vector[0], vector[1]),
            vector[1] // math.gcd(vector[0], vector[1]),
        )
        if norm_vector in seen_vectors:
            continue
        seen_vectors.add(norm_vector)
        line = map2d.trace_until_obstacle(start, norm_vector)
        # log.debug(line)
        if map2d.get_obstacle_from_point(line[-1]) == Map2d.obstacle_sym:
            obst_list.append(line[-1])
            # log.debug("obstacle")
            seen_obstacles += 1
    # log.debug('-----------')
    # log.debug(obst_list)
    # log.debug(start)
    # log.debug('-----------')
    return seen_obstacles


def part1(in_data, test=False):
    map2d = Map2d.from_lines(in_data)
    maximum_visibility = 0
    for i in range(len(map2d.obstacle_str)):
        if map2d.obstacle_str[i] != "#":
            continue
        obst = ray_trace_from_point(map2d, map2d.translate_index(i))
        if obst > maximum_visibility:
            maximum_visibility = obst
    return maximum_visibility


def part2(in_data, test=False):
    map2d = Map2d.from_lines(in_data)
    return "part2 output 2019-10"
