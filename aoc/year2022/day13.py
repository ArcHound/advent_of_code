# 2022-13

import logging
import json
from functools import cmp_to_key

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = list()
    for line in in_data.splitlines():
        if line.strip() != "":
            data.append(json.loads(line))
    return data


def compare(left, right):
    result = 0
    # log.debug(f"{left} ? {right}")
    if type(left) == int and type(right) == int:
        if left < right:
            result = -1
        elif left > right:
            result = 1
        else:
            result = 0
    elif type(left) == list and type(right) == list:
        if (len(left) == 0 or len(right) == 0) and len(left) != len(right):
            if len(left) == 0:
                result = -1
            else:
                result = +1
        else:
            for i in range(max((len(left), len(right)))):
                if (i >= len(left) or i >= len(right)) and len(left) != len(right):
                    if i >= len(left):
                        result = -1
                    else:
                        result = +1
                    break
                temp = compare(left[i], right[i])
                if temp != 0:
                    result = temp
                    break
    else:
        if type(left) != list:
            return compare([left], right)
        else:
            return compare(left, [right])
    return result


def part1(in_data, test=False):
    data = parse_data(in_data)
    counter = 0
    total = 0
    while len(data) > 0:
        counter += 1
        left = data.pop(0)
        right = data.pop(0)
        if compare(left, right) < 0:
            log.debug(f"{left} < {right}")
            total += counter
        log.debug("--------------")
    return total


def part2(in_data, test=False):
    data = parse_data(in_data)
    data.append([[2]])
    data.append([[6]])
    n = sorted(data, key=cmp_to_key(compare))
    one = n.index([[2]]) + 1
    two = n.index([[6]]) + 1
    return one * two
