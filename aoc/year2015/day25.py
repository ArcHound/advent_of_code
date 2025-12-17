# 2015-25

import logging
import re

log = logging.getLogger("aoc_logger")

ex_pattern = "To continue, please consult the code grid in the manual.  Enter the code at row (?P<y>[0-9]*), column (?P<x>[0-9]*)."


def parse_data(in_data):
    match = re.search(ex_pattern, in_data)
    return int(match.group("x")), int(match.group("y"))


def part1(in_data, test=False):
    x, y = parse_data(in_data)
    start = 20151125
    mod = 33554393
    mult = 252533
    log.debug(f"{x}, {y}")
    diagonal_start = (x + y - 2) * (x + y - 1) // 2
    index_of_point = diagonal_start + x
    log.debug(index_of_point)
    return (start * pow(mult, index_of_point - 1, mod)) % mod
