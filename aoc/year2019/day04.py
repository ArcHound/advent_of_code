# 2019-4
import logging

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = list()
    for line in in_data.splitlines():
        data.append(line)
    return data


def check(n, part2=False):
    digits = [int(x) for x in str(n)]
    double = False
    digi_counts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(len(digits) - 1):
        if digits[i] > digits[i + 1]:
            return False
        elif digits[i] == digits[i + 1]:
            double = True
        digi_counts[digits[i]] += 1
    digi_counts[digits[len(digits) - 1]] += 1
    if not part2:
        return double
    else:
        return 2 in digi_counts


def part1(in_data, test=False):
    data = parse_data(in_data)
    s, e = data[0].split("-")
    s = int(s)
    e = int(e)
    counter = 0
    for i in range(s, e):
        if check(i):
            counter += 1
    return counter


def part2(in_data, test=False):
    data = parse_data(in_data)
    s, e = data[0].split("-")
    s = int(s)
    e = int(e)
    counter = 0
    for i in range(s, e):
        if check(i, True):
            counter += 1
    return counter
