# 2020-15

import logging
from tqdm import tqdm

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    return [int(x) for x in in_data.strip().split(",")]


def part1(in_data, test=False):
    data = parse_data(in_data)
    log.debug(data)
    cache = dict()
    for i in range(len(data)):
        cache[data[i]] = [i]
    i = len(data)
    # let's not overcopmlicate this
    spoken_num = 0
    cache[0].append(i)
    i += 1
    while i < 2020:
        if spoken_num not in cache:
            cache[0].append(i)
            spoken_num = 0
            i += 1
        elif len(cache[spoken_num]) == 1:
            cache[0].append(i)
            spoken_num = 0
            i += 1
        else:
            a = cache[spoken_num][-2] + 1
            b = cache[spoken_num][-1] + 1
            spoken_num = b - a
            if b - a not in cache:
                cache[b - a] = list()
            cache[spoken_num].append(i)
            if len(cache[spoken_num]) > 2:
                cache[spoken_num] = cache[spoken_num][-2:]
            i += 1
    return spoken_num


def part2(in_data, test=False):
    data = parse_data(in_data)
    log.debug(data)
    cache = dict()
    for i in range(len(data)):
        cache[data[i]] = [i]
    i = len(data)
    # let's not overcopmlicate this
    spoken_num = 0
    cache[0].append(i)
    i += 1
    j = i
    for i in tqdm(range(j, 30000000)):
        if spoken_num not in cache:
            cache[0].append(i)
            spoken_num = 0
            i += 1
        elif len(cache[spoken_num]) == 1:
            cache[0].append(i)
            spoken_num = 0
            i += 1
        else:
            a = cache[spoken_num][-2] + 1
            b = cache[spoken_num][-1] + 1
            spoken_num = b - a
            if b - a not in cache:
                cache[b - a] = list()
            cache[spoken_num].append(i)
            if len(cache[spoken_num]) > 2:
                cache[spoken_num] = cache[spoken_num][-2:]
            i += 1
    return spoken_num
