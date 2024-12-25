# 2024-03

import logging
import re

log = logging.getLogger("aoc_logger")

mul_re = r"mul\((?P<a>[0-9][0-9]*),(?P<b>[0-9][0-9]*)\)"
do_re = r"(?P<y>do\(\))"
dont_re = r"(?P<y>don't\(\))"


def parse_data(in_data):
    data = list()
    for line in in_data.splitlines():
        data.append(line)
    return " ".join(data)


def part1(in_data, test=False):
    data = parse_data(in_data)
    return sum([int(x["a"]) * int(x["b"]) for x in re.finditer(mul_re, data)])


def part2(in_data, test=False):
    data = parse_data(in_data)
    all_dict = dict()
    for x in re.finditer(mul_re, data):
        log.debug(x.span()[0])
        all_dict[x.span()[0]] = int(x["a"]) * int(x["b"])
    for x in re.finditer(do_re, data):
        log.debug(x)
        all_dict[x.span()[0]] = True
    for x in re.finditer(dont_re, data):
        log.debug(x)
        all_dict[x.span()[0]] = False
    keys = sorted(list(all_dict.keys()))
    log.debug(all_dict)
    enabled = True
    total = 0
    for i in keys:
        if all_dict[i] == True:
            enabled = True
        elif all_dict[i] == False:
            enabled = False
        else:
            if enabled:
                total += all_dict[i]
    return total
