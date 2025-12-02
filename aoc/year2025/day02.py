# 2025-02

import logging

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = [(int(x.split("-")[0]), int(x.split("-")[1])) for x in in_data.split(",")]
    return data


def part1(in_data, test=False):
    data = parse_data(in_data)
    total = 0
    for a, b in data:
        for i in range(a, b + 1):
            s = str(i)
            if len(s) % 2 == 0:
                if s[: len(s) // 2] == s[len(s) // 2 :]:
                    total += int(s)
    return total


def part2(in_data, test=False):
    data = parse_data(in_data)
    total = 0
    for a, b in data:
        log.debug(f"{a} - {b}")
        for i in range(a, b + 1):
            s = str(i)
            valid = False
            for j in range(1, len(s) // 2 + 1):
                valid_inner = True
                pattern = s[:j]
                if len(s) % j != 0:
                    continue
                for k in range(1, len(s) // j):
                    if pattern != s[j * k : j * (k + 1)]:
                        valid_inner = False
                        break
                if valid_inner:
                    valid = True
                    break
            if valid:
                log.debug('found "invalid": %s', s)
                total += int(s)
    return total
