# 2020-02

import logging

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = list()
    for line in in_data.splitlines():
        tokens = line.strip().split(" ")
        password = tokens[-1]
        flag = tokens[1][0]
        interval = (int(tokens[0].split("-")[0]), int(tokens[0].split("-")[1]))
        data.append((interval, flag, password))
    return data


def part1(in_data, test=False):
    data = parse_data(in_data)
    good = 0
    log.debug(data)
    for interval, flag, password in data:
        c = sum([1 for x in password if x == flag])
        if c >= interval[0] and c <= interval[1]:
            good += 1
    return good


def part2(in_data, test=False):
    data = parse_data(in_data)
    good = 0
    log.debug(data)
    for interval, flag, password in data:
        if (
            password[interval[0] - 1] == flag and password[interval[1] - 1] != flag
        ) or (password[interval[0] - 1] != flag and password[interval[1] - 1] == flag):
            good += 1
    return good
