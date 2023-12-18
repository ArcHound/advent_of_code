# 2023-18
import logging
from aoc_lib.vector2d import *
from aoc_lib.map2d import Map2d

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    return [
        {
            "dir": line.split(" ")[0],
            "steps": int(line.split(" ")[1]),
            "color": "0x" + line.split(" ")[2][2:-1],
        }
        for line in in_data.splitlines()
    ]


dirmap = {"R": (1, 0), "D": (0, 1), "L": (-1, 0), "U": (0, -1)}


def part1(in_data):
    # technique parse
    data = parse_data(in_data)
    # draw the graph
    point = (0, 0)
    edge = [(0, 0)]
    for entry in data:
        for i in range(entry["steps"]):
            new_point = v_add(point, dirmap[entry["dir"]])
            edge.append(new_point)
            point = new_point
    bounds = (
        (min([p[0] for p in edge]) - 1, min([p[1] for p in edge]) - 1),
        (max([p[0] for p in edge]) + 2, max([p[1] for p in edge]) + 2),
    )
    map2d = Map2d.from_obstacle_list(edge, bounds)
    # flood
    map2d.flood(map2d.minimal)
    # check empty spaces - that's our capacity
    # it works, but it's pretty slow - keeping for posterity though.
    # obviously the part 2 algo would solve the part 1 as well
    return sum([1 for x in map2d.flooded if x == -1])


def parse_data2(in_data):
    return [
        {
            "dir": line.split(" ")[2][2:-1][-1],
            "steps": int("0x" + line.split(" ")[2][2:-2], 16),
        }
        for line in in_data.splitlines()
    ]


dirmap2 = {"0": (1, 0), "1": (0, 1), "2": (-1, 0), "3": (0, -1)}


def shoelace_formula(points):
    return (
        sum(
            [
                points[i][0] * points[i + 1][1] - points[i + 1][0] * points[i][1]
                for i in range(len(points) - 1)
            ]
        )
        // 2
    )


def part2(in_data):
    # ok, I can't draw that map in memory, it's too big.
    # It's a right angled polygon
    data = parse_data2(in_data)
    point = (0, 0)
    points = [(0, 0)]
    cycle_len = 0
    # walk the distances, note the edge points
    for entry in data:
        cycle_len += entry["steps"]
        diff = v_const_mult(dirmap2[entry["dir"]], entry["steps"])
        new_point = v_add(point, diff)
        points.append(new_point)
        if new_point == (0, 0):
            log.debug("Cycle complete")
            break
        point = new_point
    # a bump into the positive coordinates
    bounds = (
        (min([p[0] for p in points]) - 1, min([p[1] for p in points]) - 1),
        (max([p[0] for p in points]) + 2, max([p[1] for p in points]) + 2),
    )
    new_points = [v_add(p, v_diff((0, 0), bounds[0])) for p in points]
    # shoelace formula gets us the inner area, we need to include half of the border (and off by one error, apparently)
    return shoelace_formula(new_points) + cycle_len // 2 + 1
