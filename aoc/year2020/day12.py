# 2020-12

import logging

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = list()
    for line in in_data.splitlines():
        data.append((line[0], int(line[1:])))
    return data


clock = [(0, -1), (1, 0), (0, 1), (-1, 0)]


def move(position, orientation, letter, number):
    n_position = position
    n_orientation = orientation
    if letter == "N":
        n_position = (position[0], position[1] - number)
    elif letter == "E":
        n_position = (position[0] + number, position[1])
    elif letter == "S":
        n_position = (position[0], position[1] + number)
    elif letter == "W":
        n_position = (position[0] - number, position[1])
    elif letter == "L":
        n_orientation = (orientation - 1 * (number // 90) + 16) % 4
    elif letter == "R":
        n_orientation = (orientation + 1 * (number // 90) + 16) % 4
    elif letter == "F":
        n_position = (
            position[0] + number * clock[orientation][0],
            position[1] + number * clock[orientation][1],
        )
    return n_position, n_orientation


def part1(in_data, test=False):
    data = parse_data(in_data)
    position = (0, 0)
    orientation = 1
    for letter, number in data:
        position, orientation = move(position, orientation, letter, number)
        log.debug((position, orientation))
    return abs(position[0]) + abs(position[1])


def rotate_r(point, steps):
    if steps == 0:
        return point
    elif steps == 1:
        return (-1 * point[1], point[0])
    elif steps == 2:
        return (-1 * point[0], -1 * point[1])
    elif steps == 3:
        return (point[1], -1 * point[0])


def move_waypoint(position, waypoint, letter, number):
    n_position = position
    n_waypoint = waypoint
    if letter == "N":
        n_waypoint = (waypoint[0], waypoint[1] - number)
    elif letter == "E":
        n_waypoint = (waypoint[0] + number, waypoint[1])
    elif letter == "S":
        n_waypoint = (waypoint[0], waypoint[1] + number)
    elif letter == "W":
        n_waypoint = (waypoint[0] - number, waypoint[1])
    elif letter == "L":
        n_waypoint = rotate_r(waypoint, (16 - (number // 90)) % 4)
    elif letter == "R":
        n_waypoint = rotate_r(waypoint, (number // 90) % 4)
    elif letter == "F":
        n_position = (
            position[0] + number * waypoint[0],
            position[1] + number * waypoint[1],
        )
    return n_position, n_waypoint


def part2(in_data, test=False):
    data = parse_data(in_data)
    position = (0, 0)
    waypoint = (10, -1)
    for letter, number in data:
        position, waypoint = move_waypoint(position, waypoint, letter, number)
        log.debug((position, waypoint))
    return abs(position[0]) + abs(position[1])
