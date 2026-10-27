# 2016-01

import logging

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = list()
    for line in in_data.splitlines():
        for inst in line.strip().split(", "):
            data.append((inst[0], int(inst[1:])))
    return data


dirs = ["N", "E", "S", "W"]


def turn(direction, d):
    if d == "R":
        direction = (direction + 1) % 4
    else:
        direction = (direction - 1 + 4) % 4
    return direction


def step(position, direction, v):
    a, b = position
    if dirs[direction] == "N":
        position = (a, b - v)
    elif dirs[direction] == "E":
        position = (a + v, b)
    elif dirs[direction] == "S":
        position = (a, b + v)
    elif dirs[direction] == "W":
        position = (a - v, b)
    else:
        raise ValueError("Invalid direction??")
    return position


def part1(in_data, test=False):
    data = parse_data(in_data)
    position = (0, 0)
    direction = 0
    for d, v in data:
        direction = turn(direction, d)
        position = step(position, direction, v)
    a, b = position
    return abs(a) + abs(b)


def part2(in_data, test=False):
    data = parse_data(in_data)
    position = (0, 0)
    direction = 0
    visited = set()
    done = False
    for d, v in data:
        direction = turn(direction, d)
        for s in range(v):
            position = step(position, direction, 1)
            log.debug(position)
            if position in visited:
                done = True
                break
            visited.add(position)
        if done:
            break
    a, b = position
    return abs(a) + abs(b)
