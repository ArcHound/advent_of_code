# 2024-02

import logging

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = list()
    for line in in_data.splitlines():
        data.append([int(x) for x in line.split(" ")])
    return data


def is_safe(reports):
    increasing = None
    if reports[0] < reports[1]:
        increasing = True
    elif reports[0] > reports[1]:
        increasing = False
    else:
        return False
    for i in range(0, len(reports) - 1):
        d = 0
        if increasing:
            d = reports[i + 1] - reports[i]
        else:
            d = reports[i] - reports[i + 1]
        if 1 <= d and d <= 3:
            continue
        else:
            return False
    return True


def problem_dampener(reports):
    if is_safe(reports):
        return True
    else:
        for i in range(len(reports)):
            if is_safe(reports[:i] + reports[i + 1 :]):
                return True
        return False


def part1(in_data, test=False):
    data = parse_data(in_data)
    count = 0
    for r in data:
        if is_safe(r):
            log.debug(f"{r} is safe")
            count += 1
        else:
            log.debug(f"{r} is not safe")
    return count


def part2(in_data, test=False):
    data = parse_data(in_data)
    count = 0
    for r in data:
        if problem_dampener(r):
            log.debug(f"{r} is safe")
            count += 1
        else:
            log.debug(f"{r} is not safe")
    return count
