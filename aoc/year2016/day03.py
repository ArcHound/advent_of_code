# 2016-03

import logging

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = list()
    for line in in_data.splitlines():
        data.append([int(x) for x in line.split(" ") if x != ""])
    return data


def part1(in_data, test=False):
    data = parse_data(in_data)
    counter = 0
    for triangle in data:
        s_t = sorted(triangle)
        if s_t[0] + s_t[1] > s_t[2]:
            counter += 1
    return counter


def part2(in_data, test=False):
    data = parse_data(in_data)
    pointer = 0
    counter = 0
    while pointer < len(data):
        t_1 = sorted(
            list((data[pointer][0], data[pointer + 1][0], data[pointer + 2][0]))
        )
        t_2 = sorted(
            list((data[pointer][1], data[pointer + 1][1], data[pointer + 2][1]))
        )
        t_3 = sorted(
            list((data[pointer][2], data[pointer + 1][2], data[pointer + 2][2]))
        )
        if t_1[0] + t_1[1] > t_1[2]:
            counter += 1
        if t_2[0] + t_2[1] > t_2[2]:
            counter += 1
        if t_3[0] + t_3[1] > t_3[2]:
            counter += 1
        pointer += 3
    return counter
