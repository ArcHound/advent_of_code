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


def turbo_nearby_points(point):
    # I have two options - off by one error hell, or hardcoding 24 positions.
    # B is correct - it's still off by one error hell, but cleaner
    transform_dict = {
        # outer corners
        (0, 0): [(0, (0, 1)), (0, (1, 0)), (0 - 1, (2, 1)), (0 - 1, (1, 2))],
        (4, 0): [(0, (4, 1)), (0, (3, 0)), (0 - 1, (2, 1)), (0 - 1, (3, 2))],
        (0, 4): [(0, (1, 4)), (0, (0, 3)), (0 - 1, (1, 2)), (0 - 1, (2, 3))],
        (4, 4): [(0, (3, 4)), (0, (4, 3)), (0 - 1, (3, 2)), (0 - 1, (2, 3))],
        # left outer
        (0, 1): [(0, (1, 1)), (0, (0, 0)), (0, (0, 2)), (0 - 1, (1, 2))],
        (0, 2): [(0, (1, 2)), (0, (0, 1)), (0, (0, 3)), (0 - 1, (1, 2))],
        (0, 3): [(0, (1, 3)), (0, (0, 2)), (0, (0, 4)), (0 - 1, (1, 2))],
        # right outer
        (4, 1): [(0, (3, 1)), (0, (4, 0)), (0, (4, 2)), (0 - 1, (3, 2))],
        (4, 2): [(0, (3, 2)), (0, (4, 1)), (0, (4, 3)), (0 - 1, (3, 2))],
        (4, 3): [(0, (3, 3)), (0, (4, 2)), (0, (4, 4)), (0 - 1, (3, 2))],
        # top outer
        (1, 0): [(0, (1, 1)), (0, (0, 0)), (0, (2, 0)), (0 - 1, (2, 1))],
        (2, 0): [(0, (2, 1)), (0, (1, 0)), (0, (3, 0)), (0 - 1, (2, 1))],
        (3, 0): [(0, (3, 1)), (0, (2, 0)), (0, (4, 0)), (0 - 1, (2, 1))],
        # bottom outer
        (1, 4): [(0, (1, 3)), (0, (0, 4)), (0, (2, 4)), (0 - 1, (2, 3))],
        (2, 4): [(0, (2, 3)), (0, (1, 4)), (0, (3, 4)), (0 - 1, (2, 3))],
        (3, 4): [(0, (3, 3)), (0, (2, 4)), (0, (4, 4)), (0 - 1, (2, 3))],
        # inner corners
        (1, 1): [(0, (1, 0)), (0, (0, 1)), (0, (2, 1)), (0, (1, 2))],
        (3, 1): [(0, (3, 0)), (0, (3, 2)), (0, (4, 1)), (0, (2, 1))],
        (1, 3): [(0, (0, 3)), (0, (2, 3)), (0, (1, 4)), (0, (1, 2))],
        (3, 3): [(0, (3, 2)), (0, (4, 3)), (0, (3, 4)), (0, (2, 3))],
        # top inner
        (2, 1): [(0, (2, 0)), (0, (1, 1)), (0, (3, 1))]
        + [(0 + 1, (i, 0)) for i in range(5)],
        # bottom inner
        (2, 3): [(0, (2, 4)), (0, (1, 3)), (0, (3, 3))]
        + [(0 + 1, (i, 4)) for i in range(5)],
        # left inner
        (1, 2): [(0, (0, 2)), (0, (1, 1)), (0, (1, 3))]
        + [(0 + 1, (0, i)) for i in range(5)],
        # right inner
        (3, 2): [(0, (4, 2)), (0, (3, 1)), (0, (3, 3))]
        + [(0 + 1, (4, i)) for i in range(5)],
    }
    return transform_dict[point]


def transform2(stack):
    bounds = stack[0].bounds
    new_stack = list()
    for layer in range(len(stack)):
        new_obst_str = list()
        # if all(['.'== x for z in range(max(layer-1,0),min(layer+1,len(stack)-1)) for x in stack[z].obstacle_str]):
        #     new_stack.append(stack[layer]) # if nearby layers are empty, this one is empty too!
        #     continue
        for i in range(bounds[0][0], bounds[1][0]):
            for j in range(bounds[0][1], bounds[1][1]):
                if i == 2 and j == 2:
                    new_obst_str.append(".")  # doesn't matter, skip the center
                    continue
                bug_count = 0
                for s, p in turbo_nearby_points((i, j)):
                    if layer + s < 0 or layer + s >= len(stack):
                        # raise ValueError("STACK OVERFLOW!!") # shouldn't happen
                        continue
                    if stack[layer + s].get_obstacle_from_point(p) == "#":
                        bug_count += 1
                if stack[layer].get_obstacle_from_point((i, j)) == ".":
                    if bug_count == 1 or bug_count == 2:
                        new_obst_str.append("#")
                    else:
                        new_obst_str.append(".")
                elif stack[layer].get_obstacle_from_point((i, j)) == "#":
                    if bug_count != 1:
                        new_obst_str.append(".")
                    else:
                        new_obst_str.append("#")
        new_layer = Map2d("".join(new_obst_str), bounds, diagonal=False)
        new_stack.append(new_layer)
    return new_stack


def part2(in_data, test=False):
    rounds = 200
    if test:
        rounds = 10
    map2d = Map2d.from_lines(in_data)
    empty_map = "." * len(map2d.obstacle_str)
    the_stack = [Map2d(empty_map, map2d.bounds) for i in range(round(rounds * 2.5))]
    zero = round(rounds * 2.5 / 2)
    the_stack[zero] = map2d
    for i in range(rounds):
        the_stack = transform2(the_stack)
    bug_count = 0
    for l in the_stack:
        for i in range(len(map2d.obstacle_str)):
            if l.obstacle_str[i] == "#":
                bug_count += 1
    for i in range(-1 * rounds, rounds):
        log.debug(the_stack[i].debug_draw())
    return bug_count
