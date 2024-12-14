# 2024-13

import logging
from aoc_lib.vector2d import *
from tqdm import tqdm

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = list()
    obj = list()
    for line in in_data.splitlines():
        if ":" in line:
            x, y = line.split(": ")[1].split(", ")
            obj.append((int(x[2:]), int(y[2:])))
            if len(obj) == 3:
                data.append({"A": obj[0], "B": obj[1], "P": obj[2]})
                obj = list()
    return data


def part1(in_data, test=False):
    data = parse_data(in_data)
    log.debug(data)
    total = 0
    for line in tqdm(data):
        cost = 500
        for i in range(100):
            for j in range(100):
                if (
                    v_add(v_const_mult(line["A"], i), v_const_mult(line["B"], j))
                    == line["P"]
                ):
                    c = i * 3 + j
                    if c < cost:
                        cost = c
        if cost != 500:
            total += cost
    return total


def find_cost(a, b, p):
    """
    p_x = a_x*u + b_x*v
    p_y = a_y*u + b_y*v
    3*u+v is minimal
    """
    u = 0
    v = 0
    if a[1] == 0:
        log.error("a_y == 0")
        return None  # shouldn't happen, checked input.
    q = (b[1] * a[0]) - (b[0] * a[1])
    w = (p[1] * a[0]) - (p[0] * a[1])
    if q == 0:
        if w == 0:
            log.error("many solutions")
            # please don't make me do it!
            # phew, you didn't make me do it.
            return None
        elif w != 0:
            # no solution
            return None
    else:
        # now we have one solution exactly
        # check for integer solutions only!
        if w % q == 0:
            v = w // q
            if (p[0] - b[0] * v) % a[0] == 0:
                u = (p[0] - b[0] * v) // a[0]
            else:
                return None
        else:
            return None
    return 3 * u + v


def part2(in_data, test=False):
    data = parse_data(in_data)
    for line in data:
        line["P"] = v_add(line["P"], (10000000000000, 10000000000000))
    total = 0
    for line in tqdm(data):
        cost = find_cost(line["A"], line["B"], line["P"])
        if cost is not None:
            total += cost
    return total
