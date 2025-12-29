# 2020-25

import logging

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = list()
    for line in in_data.splitlines():
        data.append(int(line))
    return data[0], data[1]


def part1(in_data, test=False):
    p1, p2 = parse_data(in_data)
    mod = 20201227
    start = 7
    i = 0
    val = 1
    while True:
        i += 1
        val = (val * start) % mod
        if val == p1 or val == p2:
            break
    key = 1
    p = 1
    # it's diffie hellman-ish where they switch the keys
    if val == p1:
        p = p2
    else:
        p = p1
    prod = 1
    for j in range(i):
        prod = (prod * p) % mod
    return prod
