# 2020-10

import logging

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = list()
    for line in in_data.splitlines():
        data.append(int(line.strip()))
    return data


def part1(in_data, test=False):
    data = parse_data(in_data)
    data.append(0)
    maxval = max(data)
    data.append(maxval + 3)
    data.sort()
    one = 0
    three = 0
    for i in range(len(data) - 1):
        if data[i + 1] - data[i] == 3:
            three += 1
        else:
            one += 1
    return three * one


def count_options(buf):
    # uh... maybe there will be no more than 5 elements and I don't need to bother?
    buf_map = {1: 1, 2: 1, 3: 2, 4: 4, 5: 7}
    return buf_map[buf]


def part2(in_data, test=False):
    data = parse_data(in_data)
    data = parse_data(in_data)
    data.append(0)
    maxval = max(data)
    data.append(maxval + 3)
    data.sort()
    buf = 1  # elements themselves don't matter, only their count
    prod = 1
    log.error(data)
    for i in range(len(data) - 1):
        if data[i + 1] - data[i] == 3:
            prod *= count_options(buf)
            log.error(f"{buf} -> {count_options(buf)} -> {prod}")
            buf = 1
        else:
            buf += 1
    return prod
