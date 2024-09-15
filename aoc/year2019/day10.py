# 2019-10
import logging
from aoc_lib.map2d import Map2d
import math

log = logging.getLogger("aoc_logger")


def ray_traces_from_point(map2d, start):
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
        line = map2d.trace(start, norm_vector)
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


def get_full_lines(map2d, start):
    vector_map = dict()
    for i in range(len(map2d.obstacle_str)):
        end = map2d.translate_index(i)
        if start[0] == end[0] and start[1] == end[1]:
            continue
        vector = (end[0] - start[0], end[1] - start[1])
        norm_vector = (
            vector[0] // math.gcd(vector[0], vector[1]),
            vector[1] // math.gcd(vector[0], vector[1]),
        )
        if norm_vector in vector_map:
            continue
        line = map2d.trace(start, norm_vector, until_obstacle=False)
        vector_map[norm_vector] = line
        # log.debug(line)
    return vector_map


def vector_clockwise_sort(vectors):
    q41 = [x for x in vectors if x[0] == 0 and x[1] > 0]
    q1 = sorted(
        [x for x in vectors if x[0] > 0 and x[1] > 0],
        key=lambda x: math.acos(float(x[1]) / math.sqrt(x[0] * x[0] + x[1] * x[1])),
        reverse=True,
    )
    q12 = [x for x in vectors if x[0] > 0 and x[1] == 0]
    q2 = sorted(
        [x for x in vectors if x[0] > 0 and x[1] < 0],
        key=lambda x: math.acos(float(x[0]) / math.sqrt(x[0] * x[0] + x[1] * x[1])),
        reverse=True,
    )
    q23 = [x for x in vectors if x[0] == 0 and x[1] < 0]
    q3 = sorted(
        [x for x in vectors if x[0] < 0 and x[1] < 0],
        key=lambda x: math.acos(
            float(-1 * x[1]) / math.sqrt(x[0] * x[0] + x[1] * x[1])
        ),
        reverse=True,
    )
    q34 = [x for x in vectors if x[0] < 0 and x[1] == 0]
    q4 = sorted(
        [x for x in vectors if x[0] < 0 and x[1] > 0],
        key=lambda x: math.acos(
            float(-1 * x[0]) / math.sqrt(x[0] * x[0] + x[1] * x[1])
        ),
        reverse=True,
    )
    return q23 + q2 + q12 + q1 + q41 + q4 + q34 + q3


def part1(in_data, test=False):
    map2d = Map2d.from_lines(in_data)
    maximum_visibility = 0
    for i in range(len(map2d.obstacle_str)):
        if map2d.obstacle_str[i] != "#":
            continue
        obst = ray_traces_from_point(map2d, map2d.translate_index(i))
        if obst > maximum_visibility:
            maximum_visibility = obst
    return maximum_visibility


def part2(in_data, test=False):
    map2d = Map2d.from_lines(in_data)
    maximum_visibility = 0
    station = (0, 0)
    for i in range(len(map2d.obstacle_str)):
        if map2d.obstacle_str[i] != "#":
            continue
        obst = ray_traces_from_point(map2d, map2d.translate_index(i))
        if obst > maximum_visibility:
            maximum_visibility = obst
            station = map2d.translate_index(i)
    log.debug(station)
    map2d.set_point(station, "X")
    log.debug("----")
    vector_map = get_full_lines(map2d, station)
    vectors = vector_clockwise_sort(list(vector_map.keys()))
    counter = 0
    v_counter = 0
    last_asteroid = (0, 0)
    no_more_asteroids = False
    while counter < 200 and not no_more_asteroids:
        obstacle = False
        timeout = 0
        start_v_counter = v_counter
        while not obstacle:
            v = vectors[v_counter]
            for x in vector_map[v]:
                if map2d.get_obstacle_from_point(x) == Map2d.obstacle_sym:
                    obstacle = True
                    last_asteroid = x
                    map2d.set_point(x, Map2d.empty_sym)
                    counter += 1
                    break
            v_counter += 1
            v_counter %= len(vectors)
            if start_v_counter == v_counter:
                no_more_asteroids = True
                log.error("No more asteroids")
                break
    return last_asteroid[0] * 100 + last_asteroid[1]
