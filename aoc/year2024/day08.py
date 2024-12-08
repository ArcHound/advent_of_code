# 2024-08

import logging
from collections import defaultdict
from aoc_lib.vector2d import *

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = defaultdict(list)
    y_count = 0
    x_count = 0
    for line in in_data.splitlines():
        x_count = len(line.strip())
        for i in range(x_count):
            if line[i] != ".":
                data[line[i]].append((i, y_count))
        y_count += 1
    return data, y_count, x_count


def in_bounds(a, x, y):
    return a[0] >= 0 and a[0] < x and a[1] >= 0 and a[1] < y


def get_new_points(a, b, k):
    new_points = list()
    diff = v_abs(v_diff(b, a))
    sign = v_one(v_diff(b, a))
    sign_inv = v_one(v_diff(a, b))  # I need the other sign
    a_side = v_add(a, v_const_mult(v_cp_sign(diff, sign_inv), k))
    b_side = v_add(b, v_const_mult(v_cp_sign(diff, sign), k))
    return a_side, b_side


def part1(in_data, test=False):
    data, y_len, x_len = parse_data(in_data)
    covered = set()
    for x in data:
        for i in range(len(data[x])):
            for j in range(i):
                if i == j:
                    continue
                a = data[x][i]
                b = data[x][j]
                a_side, b_side = get_new_points(a, b, 1)
                if in_bounds(a_side, x_len, y_len):
                    covered.add(a_side)
                if in_bounds(b_side, x_len, y_len):
                    covered.add(b_side)
    return len(covered)


def part2(in_data, test=False):
    data, y_len, x_len = parse_data(in_data)
    covered = set()
    for x in data:
        for i in range(len(data[x])):
            for j in range(i):
                if i == j:
                    continue
                added = 3  # w/e
                k = 0
                while added > 0:
                    added = 0
                    a = data[x][i]
                    b = data[x][j]
                    a_side, b_side = get_new_points(a, b, k)
                    if in_bounds(a_side, x_len, y_len):
                        covered.add(a_side)
                        added += 1
                    if in_bounds(b_side, x_len, y_len):
                        covered.add(b_side)
                        added += 1
                    k += 1
    return len(covered)
