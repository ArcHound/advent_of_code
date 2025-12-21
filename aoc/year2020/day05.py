# 2020-05

import logging

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = list()
    for line in in_data.splitlines():
        row = line.strip()[:7]
        row_int = 0
        for i in range(len(row)):
            row_int += pow(2, i) if row[len(row) - 1 - i] == "B" else 0
        col = line.strip()[-3:]
        col_int = 0
        for i in range(len(col)):
            col_int += pow(2, i) if col[len(col) - 1 - i] == "R" else 0
        data.append((row_int, col_int))
    return data


def part1(in_data, test=False):
    data = parse_data(in_data)
    return max([r * 8 + c for r, c in data])


def part2(in_data, test=False):
    data = parse_data(in_data)
    seat_nums = sorted([r * 8 + c for r, c in data])
    for i in range(len(seat_nums) - 1):
        if seat_nums[i + 1] != seat_nums[i] + 1:
            return seat_nums[i] + 1
    return -1
