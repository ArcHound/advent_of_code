# 2024-25

import logging
from aoc_lib.map2d import Map2d
from collections import Counter

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    maps = list()
    buf = ""
    for line in in_data.splitlines():
        if line.strip() != "":
            buf += line + "\n"
        else:
            maps.append(Map2d.from_lines(buf))
            buf = ""
    maps.append(Map2d.from_lines(buf))
    return maps


def part1(in_data, test=False):
    maps = parse_data(in_data)
    num_maps = list()
    total = 0
    for i in maps:
        new_str = ""
        for j in range(len(i.obstacle_str)):
            if i.obstacle_str[j] == "#":
                new_str += "1"
            else:
                new_str += "0"
        num_maps.append(int(new_str, 2))
    for i in range(len(num_maps)):
        for j in range(i):
            if num_maps[i] & num_maps[j] == 0:
                total += 1
    return total


def part2(in_data, test=False):
    data = parse_data(in_data)
    return "part2 output 2024-25"
