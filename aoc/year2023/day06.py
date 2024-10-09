# 2023-6
import logging
from functools import lru_cache


log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    times = [
        int(x) for x in in_data.splitlines()[0].split(":")[1].split(" ") if x != ""
    ]
    distances = [
        int(x) for x in in_data.splitlines()[1].split(":")[1].split(" ") if x != ""
    ]
    return times, distances


def part1(in_data):
    times, distances = parse_data(in_data)
    log.debug(times)
    log.debug(distances)
    prod = 1
    for i in range(len(times)):
        count = 0
        for t in range(1, times[i]):
            if (times[i] - t) * (t) > distances[i]:
                count += 1
        prod *= count
    return prod


def parse_data2(in_data):
    times = int(
        "".join(
            [x for x in in_data.splitlines()[0].split(":")[1].split(" ") if x != ""]
        )
    )
    distances = int(
        "".join(
            [x for x in in_data.splitlines()[1].split(":")[1].split(" ") if x != ""]
        )
    )
    return times, distances


def part2(in_data):
    times, distances = parse_data2(in_data)
    log.debug(times)
    log.debug(distances)
    count = 0
    # f it, we bruteforce today
    for t in range(1, times):
        if (times - t) * (t) > distances:
            count += 1
    return count
