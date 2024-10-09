# 2022-9
import logging
from copy import deepcopy

from aoc_lib import vector2d

log = logging.getLogger("aoc_logger")

table = {
    (0, 0): (0, 0),
    (0, 1): (0, 0),
    (1, 0): (0, 0),
    (1, 1): (0, 0),
    (2, 0): (1, 0),
    (0, 2): (0, 1),
    (2, 1): (1, 1),
    (1, 2): (1, 1),
    (2, 2): (1, 1),
}


def get_dirs(in_file):
    return [
        (l.strip().split()[0], int(l.strip().split()[1])) for l in in_file.splitlines()
    ]


def apply_tail(h_old, h_new, t):
    diff = vector2d.v_diff(h_new, t)
    change = vector2d.v_cp_sign(table[vector2d.v_abs(diff)], diff)
    return vector2d.v_add(t, change)


def render_rope(rope, dims=(-15, 20, -5, 12)):
    strs = list()
    for j in range(dims[2], dims[3]):
        line = ""
        for i in range(dims[0], dims[1]):
            c = "."
            if (i, j) == (0, 0):
                c = "s"
            if (i, j) in rope:
                c = str(rope.index((i, j)))
            line += c
        strs.append(line)
    strs.reverse()
    return "\n".join(strs)


def simulate_rope(in_file, knot_num):
    dirs = get_dirs(in_file)
    rope = [(0, 0) for r in range(knot_num + 1)]
    new_rope = [(0, 0) for r in range(knot_num + 1)]
    tail_visits = list()
    tail_visits.append((0, 0))
    dirmap = {"R": (1, 0), "L": (-1, 0), "U": (0, 1), "D": (0, -1)}
    for d in dirs:
        vector = dirmap[d[0]]
        for step in range(d[1]):
            new_rope[0] = vector2d.v_add(rope[0], vector)
            for i in range(len(rope) - 1):
                new_rope[i + 1] = apply_tail(rope[i], new_rope[i], rope[i + 1])
                if i == len(rope) - 2:
                    tail_visits.append(new_rope[i + 1])
            # log.debug(rope)
            # log.debug(new_rope)
            rope = deepcopy(new_rope)
            log.debug(render_rope(new_rope))
    log.debug(tail_visits)
    log.debug(set(tail_visits))
    return len(set(tail_visits))


def part1(in_data):
    return simulate_rope(in_data, 1)


def part2(in_data):
    return simulate_rope(in_data, 9)
