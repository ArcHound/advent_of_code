# 2025-03

import logging
from tqdm import tqdm

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = list()
    for line in in_data.splitlines():
        data.append([int(x) for x in line])
    return data


def joltage(batteries):
    result = 0
    for i in range(len(batteries)):
        for j in range(i):
            if batteries[j] * 10 + batteries[i] > result:
                result = batteries[j] * 10 + batteries[i]
    return result


def part1(in_data, test=False):
    data = parse_data(in_data)
    return sum([joltage(line) for line in data])


def joltage_r(batteries, length):
    if length == 1:
        return max(batteries)
    else:
        max_val = max(batteries)
        any_indices = False
        while not any_indices:
            indices = [
                i
                for i in range(len(batteries))
                if batteries[i] == max_val and i + length - 1 < len(batteries)
            ]
            if len(indices) > 0:
                any_indices = True
            elif max_val == -1:
                raise ValueError("Somehow we F'd up")
            else:
                max_val = max_val - 1
        return max_val * pow(10, length - 1) + max(
            [joltage_r(batteries[i + 1 :], length - 1) for i in indices]
        )


def part2(in_data, test=False):
    data = parse_data(in_data)
    result = 0
    for line in tqdm(data):
        log.debug(line)
        r = joltage_r(line, 12)
        log.debug(r)
        log.debug("-------------------------------")
        result += r
    return result
