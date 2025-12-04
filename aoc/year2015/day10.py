# 2015-10

import logging

log = logging.getLogger("aoc_logger")


def expand_digits(line):
    state = "start"
    count = 0
    result = ""
    for c in line:
        if state == "start":
            state = c
            count = 1
        elif state == c:
            count += 1
        else:
            result += str(count) + state
            state = c
            count = 1
    result += str(count) + state
    return result


def part1(in_data, test=False):
    count = 40
    if test:
        count = 5
    line = in_data.strip()
    for i in range(count):
        line = expand_digits(line)
        log.debug(line)
    return len(line)


def part2(in_data, test=False):
    count = 50
    if test:
        count = 5
    line = in_data.strip()
    for i in range(count):
        line = expand_digits(line)
        log.debug(line)
    return len(line)
