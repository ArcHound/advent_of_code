# 2016-23

import logging
from aoc_lib.assembunny import parse_program, AssemBunny

log = logging.getLogger("aoc_logger")


def part1(in_data, test=False):
    program = parse_program(in_data)
    abc = AssemBunny()
    abc.set_register("a", 7)
    abc.run_program(program)
    return abc.get_register("a")


def part2(in_data, test=False):
    program = parse_program(in_data)
    abc = AssemBunny()
    abc.set_register("a", 12)
    log.critical("Beware, this takes ~30min")
    abc.run_program(program)
    return abc.get_register("a")
