# 2024-06

import logging
from aoc_lib.map2d import Map2d
from aoc_lib.vector2d import *
from tqdm import tqdm

log = logging.getLogger("aoc_logger")

directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]


def guard_travel(
    guard_point, guard_dir, map2d, visited=dict(), start_index=0, new_obstacle=None
):
    cycle = False
    index = start_index
    working_map = Map2d.copy(map2d)
    if new_obstacle:
        working_map.set_point(new_obstacle, "#")
    while working_map.in_bounds_point(guard_point):
        visited[index] = (guard_point, guard_dir)
        index += 1
        next_point = v_add(guard_point, directions[guard_dir])
        if not working_map.in_bounds_point(next_point):
            break
        elif len([x for x in visited if visited[x] == visited[index - 1]]) > 1:
            x1, x2 = [x for x in visited if visited[x] == visited[index - 1]]
            # debug_map = Map2d.copy(working_map)
            # for i in range(x1, x2+1):
            #     debug_map.set_point(visited[i][0], 'O')
            # log.error(debug_map.debug_draw())
            # for i in range(x1, x2+1):
            #     log.error(visited[i])
            cycle = True
            break
        elif working_map.get_point(next_point) == ".":
            guard_point = next_point
        elif working_map.get_point(next_point) == "#":
            guard_dir = (guard_dir + 1) % 4
    return visited, cycle


def part1(in_data, test=False):
    map2d = Map2d.from_lines(in_data)
    guard_index = map2d.obstacle_str.find("^")
    map2d.set_index(guard_index, ".")
    guard_point = map2d.translate_index(guard_index)
    guard_dir = 0
    visited, cycle = guard_travel(guard_point, guard_dir, map2d)
    return len(set([visited[x][0] for x in visited]))


def part2(in_data, test=False):
    map2d = Map2d.from_lines(in_data)
    guard_index = map2d.obstacle_str.find("^")
    map2d.set_index(guard_index, ".")
    guard_point = map2d.translate_index(guard_index)
    guard_dir = 0
    visited, cycle = guard_travel(guard_point, guard_dir, map2d)
    obst_points = set()
    visited_points_list = [visited[x][0] for x in visited]
    # oh boy, I am here for it.
    # so basically, go through the path again, and try placing obstacles before your head
    # also, check if the path is reachable with the new obstacle, as we are placing it before the guard starts
    # it runs in 30 min, but it works.
    for i in tqdm(visited):
        visited_copy = dict()
        for j in range(i + 1):
            if j in visited:
                visited_copy[j] = visited[j]
        visited_point, visited_dir = visited[i]
        next_dir = (visited_dir + 1) % 4
        next_point = v_add(visited_point, directions[visited_dir])
        if next_point in obst_points:
            continue
        if not map2d.in_bounds_point(next_point) or map2d.get_point(next_point) == "#":
            continue
        if (
            next_point in visited_points_list
            and visited_points_list.index(next_point) < i - 1
        ):
            continue  # can't get to the solution
        v_copy_copy, cycle = guard_travel(
            visited_point, next_dir, map2d, visited_copy, i, next_point
        )
        if cycle:
            obst_points.add(next_point)
    total = 0
    if guard_point in obst_points:
        total = len(obst_points) - 1
    else:
        total = len(obst_points)
    log.debug(obst_points)
    return total
