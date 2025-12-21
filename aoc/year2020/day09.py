# 2020-09

import logging

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = list()
    for line in in_data.splitlines():
        data.append(int(line.strip()))
    return data


def part1(in_data, test=False):
    data = parse_data(in_data)
    for i in range(25, len(data)):
        s = data[i - 25 : i]
        valid = False
        for j in s:
            if j != data[i] - j and data[i] - j in s:
                valid = True
                break
        if not valid:
            result = data[i]
            break
    return result


def part2(in_data, test=False):
    data = parse_data(in_data)
    weakness = -1
    preamble_length = 25
    if test:
        preamble_length = 5
    for i in range(preamble_length, len(data)):
        s = data[i - preamble_length : i]
        valid = False
        for j in s:
            if j != data[i] - j and data[i] - j in s:
                valid = True
                break
        if not valid:
            weakness = i
            break
    previous_s = data[:weakness]
    result = 0
    log.debug(previous_s)
    for l in range(len(previous_s)):
        for j in range(len(previous_s) - l):
            if data[weakness] == sum(data[j : j + l]):
                log.debug
                result = min(data[j : j + l]) + max(data[j : j + l])
                break
        if result != 0:
            break
    return result
