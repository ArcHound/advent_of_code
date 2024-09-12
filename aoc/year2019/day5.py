# 2019-5
import logging

from aoc_lib.intcode2019 import Intcode2019

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = list()
    for line in in_data.splitlines():
        data.append(line)
    return [int(x) for x in data[0].split(",")]


def part1(in_data, test=False):
    data = parse_data(in_data)
    computer = Intcode2019()
    computer.run_program(data, [1])
    return computer.stdout[-1]


def part2(in_data, test=False):
    data = parse_data(in_data)
    computer = Intcode2019()
    computer.run_program(data, [5])
    return computer.stdout[-1]
