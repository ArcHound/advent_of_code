# 2019-9
import logging

from aoc_lib.intcode2019 import Intcode2019

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = list()
    for line in in_data.splitlines():
        data.append(line)
    log.debug(data[0].split(","))
    return [int(x) for x in data[0].split(",")]


def part1(in_data, test=False):
    data = parse_data(in_data)
    comp = Intcode2019()
    comp.run_program_sync(data, stdin=[1])
    out = comp.get_list_output()
    log.error(out)
    return out[0]


def part2(in_data, test=False):
    data = parse_data(in_data)
    comp = Intcode2019()
    comp.run_program_sync(data, stdin=[2])
    out = comp.get_list_output()
    log.error(out)
    return out[0]
