# 2020-23

import logging
from tqdm import tqdm
import dataclasses

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    return [int(x) for x in in_data.strip()]


def shuffle(dd, fix_point, l):
    fix_point = dd[fix_point]
    after_hold = dd[dd[dd[dd[fix_point]]]]
    hold = dd[fix_point]
    hold_vals = (hold, dd[hold], dd[dd[hold]])
    dd[fix_point] = after_hold
    fval = (fix_point - 1) % l
    while fval in hold_vals or fval == 0:
        fval = (fval - 1) % (l + 1)
    nfval = dd[fval]
    dd[fval] = hold
    dd[dd[dd[hold]]] = nfval
    return fix_point


def part1(in_data, test=False):
    data = parse_data(in_data)
    log.debug(data)
    l = len(data)
    dd = {data[i]: data[i + 1] for i in range(len(data) - 1)}
    dd[data[-1]] = data[0]
    l = len(data)
    fix_point = data[-1]
    log.debug(dd)
    for i in tqdm(range(100)):
        fix_point = shuffle(dd, fix_point, l)
    result = ""
    start = dd[1]
    for i in range(l - 1):
        result += str(start)
        start = dd[start]
    return result


def part2(in_data, test=False):
    data = parse_data(in_data)
    log.debug(data)
    data += [i for i in range(10, 1000001)]
    dd = {data[i]: data[i + 1] for i in range(len(data) - 1)}
    dd[data[-1]] = data[0]
    l = len(data)
    fix_point = data[-1]
    for i in tqdm(range(10000000)):
        fix_point = shuffle(dd, fix_point, l)
    result = dd[1] * dd[dd[1]]
    return result
