# 2024-11

import logging
from tqdm import tqdm
from collections import defaultdict, deque
import networkx as nx

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = deque()
    for line in in_data.splitlines():
        data.extend([int(x) for x in line.strip().split(" ")])
    return data


def eval_stone(stone):
    s = str(stone)
    if stone == 0:
        return (1,)
    elif len(s) % 2 == 0:
        mid = len(s) // 2
        return (int(s[:mid]), int(s[mid:]))
    else:
        return (stone * 2024,)


def blink(stones, cache):
    new_stones = deque()
    for stone in stones:
        if stone not in cache:
            e = eval_stone(stone)
            cache[stone] = e
        new_stones.extend(cache[stone])
    return new_stones


def part1(in_data, test=False):
    data = parse_data(in_data)
    log.debug(data)
    cache = dict()
    for i in range(25):
        data = blink(data, cache)
    return len(data)


def part2(in_data, test=False):
    """Well, what did you expect would happen in part2?"""
    data = parse_data(in_data)
    cache = defaultdict(int)
    for x in data:
        cache[x] = 1
    for i in range(75):
        # The idea: we can count occurences of the stones in each step and build upon that.
        # There's some duplication, but it's fast
        new_cache = defaultdict(int)
        for stone, count in cache.items():
            s = str(stone)
            if stone == 0:
                new_cache[1] += count
            elif len(s) % 2 == 0:
                mid = len(s) // 2
                new_cache[int(s[:mid])] += count
                new_cache[int(s[mid:])] += count
            else:
                new_cache[stone * 2024] += count
        cache = new_cache
    total = sum(cache[x] for x in cache)
    return total
