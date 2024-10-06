# 2019-22
import logging
import math

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = list()
    for line in in_data.splitlines():
        if line.startswith("deal into new stack"):
            data.append((1, 0))
        elif line.startswith("deal with increment"):
            data.append((3, int(line.split(" ")[-1])))
        elif line.startswith("cut"):
            data.append((2, int(line.split(" ")[-1])))
    return data


def part1(in_data, test=False):
    if test:
        pos = 2
        table = 10
    else:
        pos = 2019
        table = 10007
    data = parse_data(in_data)
    for op, val in data:
        log.debug(pos)
        log.debug(f"{op}: {val}")
        if op == 1:
            pos = (table - pos - 1) % table
        elif op == 2:
            pos = (pos - val + table) % table
        elif op == 3:
            pos = (pos * val) % table
        log.debug("----")
    return pos


def part2(in_data, test=False):
    if test:
        pos = 2
        table = 10
    else:
        pos = 2020
        table = 119315717514047
    data = parse_data(in_data)
    data.reverse()
    start = pos
    repeats = 101741582076661
    for op, val in data:
        log.debug(pos)
        log.debug(f"{op}: {val}")
        if op == 1:
            pos = (table - pos - 1) % table
        elif op == 2:
            pos = (pos + val) % table
        elif op == 3:
            pos = (pos * pow(val, -1, table)) % table
        log.debug("----")
    f_pos = pos
    for op, val in data:
        log.debug(pos)
        log.debug(f"{op}: {val}")
        if op == 1:
            pos = (table - pos - 1) % table
        elif op == 2:
            pos = (pos + val + table) % table
        elif op == 3:
            pos = (pos * pow(val, -1, table)) % table
        log.debug("----")
    ff_pos = pos
    # it's all linear -> combination is linear too!
    # there's f=A*x+B % table
    # we've got two points, we can solve it
    A = (f_pos - ff_pos) * pow(start - f_pos + table, -1, table) % table
    B = (f_pos - A * start) % table
    # then we need to apply this linear function n-times
    return (
        pow(A, repeats, table) * start
        + (pow(A, repeats, table) - 1) * pow(A - 1, -1, table) * B
    ) % table
