# 2015-12

import logging
import re
import json

log = logging.getLogger("aoc_logger")

num_pattern = "-?[0-9][0-9]*"


def part1(in_data, test=False):
    data = in_data.strip()
    total = 0
    for num in re.findall(num_pattern, data):
        total += int(num)
    return total


def recursive_count(obj):
    total = 0
    if isinstance(obj, list):
        for obj2 in obj:
            total += recursive_count(obj2)
    elif isinstance(obj, dict):
        if "red" in [v for k, v in obj.items()]:
            pass
        else:
            for k, v in obj.items():
                total += recursive_count(v)
    elif isinstance(obj, int):
        total += obj
    elif isinstance(obj, str):
        pass
    else:
        raise ValueError(f"Unknown instance '{obj}' of {type(obj)}")
    return total


def part2(in_data, test=False):
    obj = json.loads(in_data)
    return recursive_count(obj)
