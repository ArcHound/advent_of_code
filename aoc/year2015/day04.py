# 2015-04

import logging
import hashlib

log = logging.getLogger("aoc_logger")


def part1(in_data, test=False):
    i = 0
    if test:
        i = 609000
    done = False
    result = 0
    while not done:
        val = hashlib.md5((in_data.strip() + str(i)).encode()).hexdigest()
        if i == 609043:
            log.debug(val)
        if val.startswith("00000"):
            result = i
            done = True
        i += 1
    return result


def part2(in_data, test=False):
    if test:
        return "part2 output 2015-04"
    i = 0
    done = False
    result = 0
    while not done:
        val = hashlib.md5((in_data.strip() + str(i)).encode()).hexdigest()
        if val.startswith("000000"):
            result = i
            done = True
        i += 1
    return result
