# 2015-17

import logging
from itertools import combinations, chain
from tqdm import tqdm

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = dict()
    count = 0
    for line in in_data.splitlines():
        data[count] = int(line.strip())
        count += 1
    return data


def powerset(iterable, start=0):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(start, len(s) + 1))


def part1(in_data, test=False):
    total_capacity = 150
    if test:
        total_capacity = 25
    data = parse_data(in_data)
    count = 0
    for subset in tqdm(powerset([x for x in data])):
        if sum([data[x] for x in subset]) == total_capacity:
            count += 1
    return count


def part2(in_data, test=False):
    data = parse_data(in_data)
    total_capacity = 150
    if test:
        total_capacity = 25
    data = parse_data(in_data)
    count = 0
    first_hit = 0
    for subset in tqdm(powerset([x for x in data])):
        if first_hit != 0 and len(subset) > first_hit:
            continue
        if sum([data[x] for x in subset]) == total_capacity:
            if first_hit == 0:
                first_hit = len(subset)
            if len(subset) == first_hit:
                count += 1
    return count
