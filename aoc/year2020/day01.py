# 2020-01

import logging

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = list()
    for line in in_data.splitlines():
        data.append(int(line.strip()))
    return data


def part1(in_data, test=False):
    data = parse_data(in_data)
    for i in range(len(data)):
        for j in range(i):
            if data[i] + data[j] == 2020:
                return data[i] * data[j]
    return -1


def part2(in_data, test=False):
    data = parse_data(in_data)
    for i in range(len(data)):
        for j in range(i):
            for k in range(j):
                if data[i] + data[j] + data[k] == 2020:
                    return data[i] * data[j] * data[k]
    return -1
