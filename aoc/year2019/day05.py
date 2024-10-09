# 2019-5
import logging

from aoc_lib.intcode2019 import Intcode2019

log = logging.getLogger("aoc_logger")


def part1(in_data, test=False):
    data = Intcode2019.parse_int_program(in_data)
    computer = Intcode2019()
    computer.run_program_sync(data, [1])
    return computer.get_list_output()[-1]


def part2(in_data, test=False):
    data = Intcode2019.parse_int_program(in_data)
    computer = Intcode2019()
    computer.run_program_sync(data, [5])
    return computer.get_list_output()[-1]
