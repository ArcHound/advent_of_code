# 2016-25

import logging
from tqdm import tqdm
from aoc_lib.assembunny import parse_program, AssemBunny

log = logging.getLogger("aoc_logger")


def part1(in_data, test=False):
    program = parse_program(in_data)
    result = 0
    for i in tqdm(range(400000)):
        abc = AssemBunny()
        abc.set_register("a", i)
        abc.run_program(program, 10)
        if abc.read_stdout() == [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]:
            result = i
            break
    return result


def part2(in_data, test=False):
    program = parse_program(in_data)
    return "part2 output 2016-25"
