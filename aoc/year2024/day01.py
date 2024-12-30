# 2024-01

import logging
from collections import Counter

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    left = list()
    right = list()
    for line in in_data.splitlines():
        nums = line.split(" ")
        left.append(int(nums[0]))
        right.append(int(nums[-1]))
    return left, right


def part1(in_data, test=False):
    left, right = parse_data(in_data)
    left.sort()
    right.sort()
    diff = 0
    for i in range(len(left)):
        diff += abs(left[i] - right[i])
    return diff


def part2(in_data, test=False):
    left, right = parse_data(in_data)
    c = Counter(right)
    diff = 0
    for a in left:
        diff += a * c[a]
    return diff
