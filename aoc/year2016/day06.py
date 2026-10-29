# 2016-06

import logging
from collections import defaultdict

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = list()
    for line in in_data.splitlines():
        data.append(line.strip())
    return data


def part1(in_data, test=False):
    data = parse_data(in_data)
    counts = dict()
    for i in range(len(data[0])):
        counts[i] = defaultdict(int)
    for s in data:
        for i in range(len(s)):
            counts[i][s[i]] += 1
    result = ""
    for i in range(len(data[0])):
        result += sorted(
            [(c, counts[i][c]) for c in counts[i]], reverse=True, key=lambda x: x[1]
        )[0][0]
    return result


def part2(in_data, test=False):
    data = parse_data(in_data)
    counts = dict()
    for i in range(len(data[0])):
        counts[i] = defaultdict(int)
    for s in data:
        for i in range(len(s)):
            counts[i][s[i]] += 1
    result = ""
    for i in range(len(data[0])):
        result += sorted([(c, counts[i][c]) for c in counts[i]], key=lambda x: x[1])[0][
            0
        ]
    return result
