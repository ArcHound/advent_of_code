# 2016-22

import logging
from aoc_lib.map2d import Map2d

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    first_two = 2
    point_map = dict()
    for line in in_data.splitlines():
        # skip first two lines
        if first_two > 0:
            first_two -= 1
            continue
        tokens = [x for x in line.strip().split() if x != ""]
        p0, p1, p2 = tokens[0].split("-")
        point = int(p1[1:]), int(p2[1:])
        point_map[point] = (
            int(tokens[1][:-1]),
            int(tokens[2][:-1]),
            int(tokens[3][:-1]),
        )
    return point_map


def find_empty_node(point_map):
    for point in point_map:
        if point_map[point][1] == 0:
            return point


def part1(in_data, test=False):
    # I've eyeballed this part as it's quite simple
    # in my input, there's a single node with enough space (it's empty)
    # all the small nodes fit
    # all the big nodes don't
    # so... count all of the small nodes without the empty node
    point_map = parse_data(in_data)
    upper_bound = point_map[find_empty_node(point_map)][2]
    counter = 0
    for point in point_map:
        if point_map[point][1] <= upper_bound and point_map[point][1] > 0:
            counter += 1
    return counter


def part2(in_data, test=False):
    point_map = parse_data(in_data)
    empty_node = find_empty_node(point_map)
    upper_bound = point_map[empty_node][2]
    point_map2 = dict()
    needed_steps = 0
    # similar idea, we basically have a std AoE map
    # big nodes are obstacles, the rest are good to pass
    for point in point_map:
        if point_map[point][1] <= upper_bound:
            point_map2[point] = "."
        else:
            point_map2[point] = "#"
    map2d = Map2d.from_point_dict(point_map2)
    # mark the start and look at it
    map2d.set_point(empty_node, "S")
    log.debug(map2d.debug_draw())
    map2d.set_point(empty_node, ".")
    # we need to get the gap near the top right corner while avoiding the obstacle
    # so I think I want to target top row, second to last point here
    map2d.flood(empty_node)
    target = (
        map2d.bounds[1][0] - 1,
        0,
    )  # fuck off by one errors, all my homies hate off by one errors.
    log.debug(target)
    needed_steps += map2d.get_flooded_point(((target[0] - 1), 0))
    log.debug(map2d.debug_draw())
    log.debug(needed_steps)
    # now we have a gap next to the target data.
    # all we need are first two rows
    # ..._G -> ...G_ -> ...G. -> ...G. -> ...G. -> .._G.
    # .....    .....    ...._    ..._.    .._..    .....
    # this gives us 5 steps to move G by a point
    # on the last one, we don't need to shuffle, so 5*(x-1)+1
    # I hope there's no miracle cure, doesn't seem like it
    needed_steps += 5 * (target[0] - 1) + 1
    return needed_steps
