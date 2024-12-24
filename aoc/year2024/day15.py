# 2024-15

import logging
from aoc_lib.map2d import Map2d
from aoc_lib.vector2d import *
import time

log = logging.getLogger("aoc_logger")

moves_map = {">": (1, 0), "<": (-1, 0), "^": (0, -1), "v": (0, 1)}


def parse_data(in_data):
    map_buffer = list()
    inst_buffer = list()
    for line in in_data.splitlines():
        if line.startswith("#"):
            map_buffer.append(line)
        elif len(line) > 0 and line[0] in "^Vv<>":
            inst_buffer.append(line)
    map2d = Map2d.from_lines("\n".join(map_buffer))
    objects = {
        i: map2d.translate_index(i)
        for i in range(len(map2d.obstacle_str))
        if map2d.get_index(i) == "O"
    }
    player = map2d.translate_index(map2d.obstacle_str.find("@"))
    for o in objects:
        map2d.set_point(objects[o], ".")
    map2d.set_point(player, ".")
    instructions = [x for line in inst_buffer for x in line.strip()]
    return map2d, instructions, objects, player


def try_move(position, vector, map2d, objects):
    new_pos = v_add(position, vector)
    obj = [x for x in objects if objects[x] == new_pos]
    obj_id = None
    if len(obj) > 0:
        obj_id = obj[0]
    if map2d.get_point(new_pos) == "#":
        return position
    elif obj_id is not None:
        test = try_move(new_pos, vector, map2d, objects)
        if v_diff(test, new_pos) == (0, 0):
            return position
        else:
            objects[obj_id] = test
            return new_pos
    else:
        return new_pos


def part1(in_data, test=False):
    map2d, instructions, objects, player = parse_data(in_data)
    for i in instructions:
        player = try_move(player, moves_map[i], map2d, objects)
    total = sum([objects[x][0] + objects[x][1] * 100 for x in objects])
    return total


def try_move2(thing, vector, map2d, objects, obj_id):
    new_thing = list()
    can_move = dict()
    next_positions = dict()
    for p in thing:
        new_thing.append(v_add(p, vector))
    next_positions[obj_id] = new_thing
    log.debug(f"Pushing {thing} to {new_thing}")
    # first, check for wall - recursion stopping point
    if any([map2d.get_point(x) == "#" for x in new_thing]):
        can_move[obj_id] = False
        return can_move, next_positions
    affected_objs = list()
    # get affected objects
    for p in new_thing:
        obj = [x for x in objects if p in objects[x]]
        if len(obj) > 0:
            for o in obj:
                if o != obj_id:
                    affected_objs.append(o)
    for o in affected_objs:
        # F it, recursion should be enough here - look to the affected objects if they can be moved
        t_can, t_next = try_move2(objects[o], vector, map2d, objects, o)
        for i in t_next:
            next_positions[i] = t_next[i]
        for i in t_can:
            can_move[i] = t_can[i]
        if all([t_can[i] for i in t_can]):
            can_move[o] = True
        else:
            can_move[o] = False
    # if we can move, DON'T MOVE! Just note it and pass it on.
    if all([can_move[x] for x in can_move]):
        can_move[obj_id] = True
    else:
        can_move[obj_id] = False
    return can_move, next_positions


def part2(in_data, test=False):
    """This was juicy. See the last edge case for the final issue, the animation is nice though"""
    map2d, instructions, objects, player = parse_data(in_data)
    log.error(len(instructions))
    log.error(len(objects))
    player = [(player[0] * 2, player[1])]
    for i in objects:
        objects[i] = [
            (objects[i][0] * 2, objects[i][1]),
            (objects[i][0] * 2 + 1, objects[i][1]),
        ]
    obstacle_list = list()
    for i in range(len(map2d.obstacle_str)):
        if map2d.get_index(i) == "#":
            point = map2d.translate_index(i)
            obstacle_list.append((point[0] * 2, point[1]))
            obstacle_list.append((point[0] * 2 + 1, point[1]))
    double_map = Map2d.from_obstacle_list(obstacle_list)
    double_map.set_point((0, double_map.bounds[1][1] // 2), "F")
    for i in instructions:
        can_move, next_positions = try_move2(
            player, moves_map[i], double_map, objects, -1
        )
        # I needed to separate the moving from the attempted move, so I needed to refactor the logic
        if all([can_move[i] for i in can_move]):
            for j in next_positions:
                if j == -1:
                    player = next_positions[j]
                else:
                    objects[j] = next_positions[j]
        # uncomment this to draw the animation
        # copy_map = Map2d(double_map.obstacle_str, double_map.bounds)
        # for o in objects:
        #     copy_map.set_point(objects[o][0], '[')
        #     copy_map.set_point(objects[o][1], ']')
        # copy_map.set_point(player[0],i)
        # log.error(copy_map)
    for o in objects:
        for p in objects[o]:
            double_map.set_point(p, "O")
    double_map.set_point(player[0], "@")
    total = sum([objects[x][0][0] + objects[x][0][1] * 100 for x in objects])
    return total
