# 2024-04

import logging

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = dict()
    x = 0
    y = 0
    max_x = 0
    max_y = 0
    for line in in_data.splitlines():
        x = 0
        for c in line:
            data[(x, y)] = c
            x += 1
        max_x = x  # same exclusive end
        y += 1
    max_y = y
    return data, max_x, max_y


def add_xmases(data, x, y, x_len, y_len):
    vectors = [(0, 1), (1, 0), (1, 1), (-1, 0), (0, -1), (-1, -1), (1, -1), (-1, 1)]
    xmas_map = {0: "X", 1: "M", 2: "A", 3: "S"}
    total = 0
    log.debug((x, y))
    for v_x, v_y in vectors:
        log.debug((v_x, v_y))
        for k in range(1, 4):
            t_x = x + k * v_x
            t_y = y + k * v_y
            log.debug((t_x, t_y))
            if (
                t_x < 0
                or t_x >= x_len
                or t_y < 0
                or t_y >= y_len
                or data[t_x, t_y] != xmas_map[k]
            ):
                break
            if k == 3:
                log.debug((x, y))
                log.debug((v_x, v_y))
                log.debug("------")
                total += 1
        log.debug("========")
    return total


def part1(in_data, test=False):
    data, x_len, y_len = parse_data(in_data)
    log.debug(data[(0, 0)])
    total = 0
    for i in range(x_len):
        for j in range(y_len):
            if data[(i, j)] == "X":
                total += add_xmases(data, i, j, x_len, y_len)
    return total


def add_x_mases(data, x, y, x_len, y_len):
    vectors = [(1, 1), (-1, -1), (1, -1), (-1, 1)]
    vector_pairs = [((1, 1), (-1, -1)), ((-1, 1), (1, -1))]
    ms = {"M", "S"}
    total = 0
    log.debug((x, y))
    xmas = True
    for v1, v2 in vector_pairs:
        t_x = x + v1[0]
        t_y = y + v1[1]
        log.debug((t_x, t_y))
        if t_x < 0 or t_x >= x_len or t_y < 0 or t_y >= y_len:
            xmas = False
            break
        c_1 = data[(t_x, t_y)]
        t_x = x + v2[0]
        t_y = y + v2[1]
        log.debug((t_x, t_y))
        if t_x < 0 or t_x >= x_len or t_y < 0 or t_y >= y_len:
            xmas = False
            break
        c_2 = data[(t_x, t_y)]
        if ms != {c_1, c_2}:
            xmas = False
            break
        else:
            log.debug("ok")
    log.debug(xmas)
    log.debug("========")
    return xmas


def part2(in_data, test=False):
    data, x_len, y_len = parse_data(in_data)
    log.debug(data[(0, 0)])
    total = 0
    for i in range(x_len):
        for j in range(y_len):
            if data[(i, j)] == "A":
                log.debug(total)
                if add_x_mases(data, i, j, x_len, y_len):
                    total += 1
    return total
