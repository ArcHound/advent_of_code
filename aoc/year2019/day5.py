# 2019-5
import logging

from aoc_lib.intcode_2019 import Intcode2019

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = list()
    for line in in_data.splitlines():
        data.append(line)
    return data


def part1(in_data, test=False):
    data = parse_data(in_data)
    return "part1 output 2019-5"


def part2(in_data, test=False):
    data = parse_data(in_data)
    return "part2 output 2019-5"
