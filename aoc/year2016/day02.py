# 2016-02

import logging

log = logging.getLogger("aoc_logger")

dirs = ["U", "D", "L", "R"]


def parse_data(in_data):
    data = list()
    for line in in_data.splitlines():
        data.append([c for c in line.strip()])
    return data


def part1(in_data, test=False):
    data = parse_data(in_data)
    keypad_size = (3, 3)
    point = (1, 1)
    code = list()
    for chars in data:
        for c in chars:
            if c == "U":
                new_y = point[1] - 1
                if new_y < 0:
                    new_y = 0
                point = (point[0], new_y)
            elif c == "D":
                new_y = point[1] + 1
                if new_y > 3 - 1:
                    new_y = 3 - 1
                point = (point[0], new_y)
            elif c == "L":
                new_x = point[0] - 1
                if new_x < 0:
                    new_x = 0
                point = (new_x, point[1])
            elif c == "R":
                new_x = point[0] + 1
                if new_x > 3 - 1:
                    new_x = 3 - 1
                point = (new_x, point[1])
            else:
                raise ValueError("Invalid char, pls fix")
        code.append(point)
    log.debug(code)
    o = ""
    for point in code:
        n = point[1] * 3 + point[0] + 1
        o += str(n)
    return o


def part2(in_data, test=False):
    data = parse_data(in_data)
    keypad = {}
    keypad[(2, 0)] = "1"
    keypad[(1, 1)] = "2"
    keypad[(2, 1)] = "3"
    keypad[(3, 1)] = "4"
    keypad[(0, 2)] = "5"
    keypad[(1, 2)] = "6"
    keypad[(2, 2)] = "7"
    keypad[(3, 2)] = "8"
    keypad[(4, 2)] = "9"
    keypad[(1, 3)] = "A"
    keypad[(2, 3)] = "B"
    keypad[(3, 3)] = "C"
    keypad[(2, 4)] = "D"
    point = (0, 2)
    code = list()
    for chars in data:
        for c in chars:
            if c == "U":
                new_point = (point[0], point[1] - 1)
                if new_point in keypad:
                    point = new_point
            elif c == "D":
                new_point = (point[0], point[1] + 1)
                if new_point in keypad:
                    point = new_point
            elif c == "L":
                new_point = (point[0] - 1, point[1])
                if new_point in keypad:
                    point = new_point
            elif c == "R":
                new_point = (point[0] + 1, point[1])
                if new_point in keypad:
                    point = new_point
            else:
                raise ValueError("Invalid char, pls fix")
        code.append(point)
    log.debug(code)
    o = ""
    for c in code:
        o += keypad[c]
    return o
