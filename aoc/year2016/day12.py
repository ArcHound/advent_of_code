# 2016-12

import logging
from aoc_lib.assembunny import parse_program, AssemBunny

log = logging.getLogger("aoc_logger")


def part1(in_data, test=False):
    data = parse_program(in_data)
    abc = AssemBunny()
    abc.run_program(data)
    return abc.get_register("a")


def part2(in_data, test=False):
    data = parse_program(in_data)
    abc = AssemBunny()
    abc.set_register("c", 1)
    abc.run_program(data)
    return abc.get_register("a")
