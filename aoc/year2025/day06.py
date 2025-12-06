# 2025-06

import logging

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = list()
    for line in in_data.splitlines():
        tokens = [x for x in line.strip().split(" ") if x != ""]
        if tokens[0][0] in "0123456789":
            tokens = [int(x) for x in tokens]
        data.append(tokens)
    return data


def norm_eval(expr):
    total = None
    if expr[-1] == "+":
        total = 0
        for x in expr[:-1]:
            total += x
    elif expr[-1] == "*":
        total = 1
        for x in expr[:-1]:
            total *= x
    return total


def part1(in_data, test=False):
    data = parse_data(in_data)
    total = 0
    for i in range(len(data[0])):
        total += norm_eval([x[i] for x in data])
    return total


def parse_data_2(in_data):
    data = list()
    lines = in_data.splitlines()
    line_num = len(lines)
    line_len = len(lines[0])
    line_bufs = ["" for i in range(line_num)]
    first = True
    for i in range(line_len):
        if not first and i + 1 < line_len and lines[-1][i + 1] in "+*":
            data.append(line_bufs)
            line_bufs = ["" for x in range(line_num)]
        else:
            for j in range(line_num):
                line_bufs[j] += lines[j][i]
        first = False
    data.append(line_bufs)
    return data


def centi_eval(expr):
    total = None
    log.debug(expr)
    op = expr[-1].strip()
    strs = [str(x) for x in expr[:-1]]
    nums = list()
    for i in range(len(strs[0])):
        num = ""
        for s in strs:
            if s[-1 - i] != " ":
                num += s[-1 - i]
        nums.append(int(num))
    log.debug(nums)
    if op == "+":
        total = 0
        for x in nums:
            total += x
    elif op == "*":
        total = 1
        for x in nums:
            total *= x
    return total


def part2(in_data, test=False):
    total = 0
    data = parse_data_2(in_data)
    log.debug(data)
    for ns in data:
        total += centi_eval(ns)
    return total
