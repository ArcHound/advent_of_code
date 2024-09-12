# 2019-2
import logging

log = logging.getLogger("aoc_logger")

from aoc_lib.intcode2019 import Intcode2019


def parse_data(in_data):
    data = list()
    for line in in_data.splitlines():
        data += [int(x) for x in line.split(",")]
    return data


def part1(in_data, test=False):
    data = parse_data(in_data)
    computer = Intcode2019()
    if not test:
        data[1] = 12
        data[2] = 2
    computer.run_program(data)
    return computer.data[0]


def part2(in_data, test=False):
    data = parse_data(in_data)
    computer = Intcode2019()
    for i in range(100):
        for j in range(100):
            data[1] = i
            data[2] = j
            computer.run_program(data)
            if computer.data[0] == 19690720:
                return i * 100 + j
    return -1
