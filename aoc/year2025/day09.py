# 2025-09

import logging
from aoc_lib.vector2d import *
from aoc_lib.map2d import Map2d
from tqdm import tqdm

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = list()
    for line in in_data.splitlines():
        a, b = line.strip().split(",")
        data.append((int(a), int(b)))
    return data


def part1(in_data, test=False):
    data = parse_data(in_data)
    max_val = 0
    for i in range(len(data)):
        for j in range(i):
            ax, ay = data[i]
            bx, by = data[j]
            x, y = v_add(
                v_abs(v_diff((ax, ay), (bx, by))), (1, 1)
            )  # my first off by (1,1) error
            if x * y > max_val:
                max_val = x * y
    return max_val


def valid_rectangle(a, b, in_points):
    log.debug(f"{a},{b}")
    n_a = (min(a[0], b[0]), min(a[1], b[1]))
    n_b = (max(a[0], b[0]), max(a[1], b[1]))
    result = True
    for i in range(n_a[0], n_b[0] + 1):
        for j in [n_a[1], n_b[1]]:
            if not is_in_interval(i, in_points[j]):
                result = False
                break
        if not result:
            break
    for j in range(n_a[1], n_b[1] + 1):
        for i in [n_a[0], n_b[0]]:
            if not is_in_interval(i, in_points[j]):
                result = False
                break
        if not result:
            break
    log.debug(result)
    return result


def add_boundary(a, b, x_boundaries, y_boundaries):
    boundary = list()
    for i in range(min(a[0], b[0]), max(a[0], b[0]) + 1):
        for j in range(min(a[1], b[1]), max(a[1], b[1]) + 1):
            boundary.append((i, j))
    if boundary[0][0] == boundary[1][0]:
        x_boundaries.append(boundary)
    else:
        y_boundaries.append(boundary)


def convert_to_intervals(points):
    log.debug("Converting to intervals")
    pl = sorted(list(points))
    log.debug(pl)
    is_in = True
    intervals = list()
    start = pl[0]
    for i in range(1, len(pl)):
        if pl[i] == pl[i - 1] + 1:
            continue
        else:
            intervals.append((start, pl[i - 1]))
            start = pl[i]
    intervals.append((start, pl[-1]))
    log.debug(intervals)
    return intervals


def is_in_interval(x, pl):
    found = False
    for a, b in pl:
        if a > x:
            break
        if b < x:
            continue
        if a <= x and x <= b:
            found = True
            break
    return found


def part2(in_data, test=False):
    log.warning("WARNING! Takes more than an hour to run!")
    data = parse_data(in_data)
    x_boundaries = list()
    y_boundaries = list()
    for i in range(len(data) - 1):
        add_boundary(data[i], data[i + 1], x_boundaries, y_boundaries)
    add_boundary(data[-1], data[0], x_boundaries, y_boundaries)
    x_boundaries.sort(key=lambda x: x[0][0])
    x_bd = dict()
    for x in x_boundaries:
        if x[0][0] not in x_bd:
            x_bd[x[0][0]] = list()
        x_bd[x[0][0]].append(x)
    y_boundaries.sort(key=lambda x: x[0][1])
    y_bd = dict()
    for y in y_boundaries:
        if y[0][1] not in y_bd:
            y_bd[y[0][1]] = list()
        y_bd[y[0][1]].append(y)
    log.debug(f"x boundaries {x_boundaries}")
    log.debug(f"y boundaries {y_boundaries}")
    log.debug(f"x bd {x_bd}")
    log.debug(f"y bd {y_bd}")
    in_points = dict()
    for y in tqdm(range(y_boundaries[0][0][1], y_boundaries[-1][0][1] + 1)):
        is_in = False
        x = -1
        in_points[y] = set()
        if y - 1 not in in_points:
            in_points[y - 1] = list()  # already "converted"
        while x <= x_boundaries[-1][0][0]:
            check_y = [z for z in x_bd[x] if (x, y) in z] if x in x_bd else []
            if not is_in and (x not in x_bd or len(check_y) == 0):
                x += 1
            elif is_in and (x not in x_bd or len(check_y) == 0):
                in_points[y].add(x)
                x += 1
            elif not is_in and x in x_bd and len(check_y) > 0:
                if y in y_bd:
                    b = [z for z in y_bd[y] if (x, y) in z]
                    if len(b) > 0:
                        for p in b[0]:
                            in_points[y].add(p[0])
                        x = b[0][-1][0]
                        if is_in_interval(x + 1, in_points[y - 1]):
                            is_in = True
                        else:
                            is_in = False
                    else:
                        is_in = True
                        in_points[y].add(x)
                    x += 1
                else:
                    is_in = True
                    in_points[y].add(x)
                    x += 1
            elif is_in and x in x_bd and len(check_y) > 0:
                if y in y_bd:
                    b = [z for z in y_bd[y] if (x, y) in z]
                    if len(b) > 0:
                        for p in b[0]:
                            in_points[y].add(p[0])
                        x = b[0][-1][0]
                        if is_in_interval(x + 1, in_points[y - 1]):
                            is_in = True
                        else:
                            is_in = False
                    else:
                        is_in = False
                        in_points[y].add(x)
                    x += 1
                else:
                    is_in = False
                    in_points[y].add(x)
                    x += 1
        log.debug(in_points[y])
        in_points[y] = convert_to_intervals(in_points[y])
        log.debug(f"{y}--------------------------------")
    log.debug(f"in_points {in_points}")
    max_val = 0
    for i in tqdm(range(len(data))):
        for j in range(i):
            ax, ay = data[i]
            bx, by = data[j]
            x, y = v_add(v_abs(v_diff((ax, ay), (bx, by))), (1, 1))
            if x * y > max_val:
                if valid_rectangle((ax, ay), (bx, by), in_points):
                    log.debug(f"New max {x * y} for {data[i], data[j]}")
                    max_val = x * y
    return max_val
