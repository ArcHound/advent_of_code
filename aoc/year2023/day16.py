# 2023-16
import logging
from aoc_lib.vector2d import *

log = logging.getLogger("aoc_logger")

# for novelty sake, I decided not to use my map2d lib
# here's a map of tiles -> entry directions -> exit directions
# code to spec, no creativity
direction_map = {
    "\\": {
        (0, -1): [(-1, 0)],
        (1, 0): [(0, 1)],
        (0, 1): [(1, 0)],
        (-1, 0): [(0, -1)],
    },
    "/": {
        (0, -1): [(1, 0)],
        (1, 0): [(0, -1)],
        (0, 1): [(-1, 0)],
        (-1, 0): [(0, 1)],
    },
    "|": {
        (0, -1): [(0, -1)],
        (1, 0): [(0, -1), (0, 1)],
        (0, 1): [(0, 1)],
        (-1, 0): [(0, -1), (0, 1)],
    },
    "-": {
        (0, -1): [(-1, 0), (1, 0)],
        (1, 0): [(1, 0)],
        (0, 1): [(-1, 0), (1, 0)],
        (-1, 0): [(-1, 0)],
    },
    ".": {
        (0, -1): [(0, -1)],
        (1, 0): [(1, 0)],
        (0, 1): [(0, 1)],
        (-1, 0): [(-1, 0)],
    },
}


def run_beam(lasermap, starting_point, starting_diff, x_len, y_len):
    to_process = [(starting_point, starting_diff)]  # we have a start
    visited_diffs = set()
    visited = set()
    while len(to_process) > 0:
        point, diff = to_process.pop(0)  # get point
        if (point, diff) in visited_diffs:
            continue  # cycle detected, break
        visited_diffs.add(
            (point, diff)
        )  # we still might pass through a point several times from other directions
        visited.add(point)
        c = lasermap[point[1]][point[0]]  # get the tile
        new_diffs = direction_map[c][diff]  # to get the directions
        for new_diff in new_diffs:
            next_point = v_add(point, new_diff)
            # if in bounds
            if (
                next_point[0] >= 0
                and next_point[0] < x_len
                and next_point[1] >= 0
                and next_point[1] < y_len
            ):
                to_process.append((next_point, new_diff))
        # draw the map for debug purposes
        # j = 0
        # for line in lasermap:
        #     i = 0
        #     buf = ''
        #     for c in line:
        #         if (i,j) in visited:
        #             buf += '#'
        #         else:
        #             buf += c
        #         i+=1
        #     log.debug(buf)
        #     j += 1
        # log.debug('-----------------')
    return len(visited)


def part1(in_data):
    lasermap = in_data.splitlines()
    x_len = len(lasermap[0])
    y_len = len(lasermap)
    return run_beam(lasermap, (0, 0), (1, 0), x_len, y_len)


def part2(in_data):
    lasermap = in_data.splitlines()
    x_len = len(lasermap[0])
    y_len = len(lasermap)
    # all of the starts
    starts = (
        [((i, 0), (0, 1)) for i in range(x_len)]
        + [((i, y_len - 1), (0, -1)) for i in range(x_len)]
        + [((0, j), (1, 0)) for j in range(y_len)]
        + [((x_len - 1, j), (-1, 0)) for j in range(y_len)]
    )
    # max of all of the beams
    return max([run_beam(lasermap, s, d, x_len, y_len) for s, d in starts])
