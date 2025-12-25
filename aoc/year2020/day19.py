# 2020-19

import logging
from dataclasses import dataclass
from collections import deque

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = list()
    rules = dict()
    for line in in_data.splitlines():
        if ":" in line:
            f, t = line.strip().split(": ")
            variants = [x.split(" ") for x in t.split(" | ")]
            rules[f] = variants
        elif line.strip() != "":
            data.append(line.strip())
    return data, rules


def recursive_eval(line, pointer, state, rules):
    if state.startswith('"'):
        if pointer >= len(line):
            return False, 1
        elif line[pointer] == state[1]:  # we know it's a single char
            return True, 1
        else:
            return False, 1
    matches = False
    match_len = 0
    for variant in rules[state]:
        current_len = 0
        matches_var = True
        for label in variant:
            m, ml = recursive_eval(line, pointer + current_len, label, rules)
            if not m:
                matches_var = False
                break
            current_len += ml
        if matches_var:
            return True, current_len
    return matches, match_len


def part1(in_data, test=False):
    data, rules = parse_data(in_data)
    total = 0
    for line in data:
        m, ml = recursive_eval(line, 0, "0", rules)
        if m and ml == len(line):
            total += 1
    return total


def part2(in_data, test=False):
    data, rules = parse_data(in_data)
    total = 0
    # f it, we ball
    tops = list()
    for i in range(1, 10):
        for j in range(1, 10):
            eights = ["42" for k in range(i)]
            elevens = ["42" for k in range(j)] + ["31" for k in range(j)]
            rules[f"0_{i}_{j}"] = [eights + elevens]
            tops.append(f"0_{i}_{j}")
    for line in data:
        for top in tops:
            m, ml = recursive_eval(line, 0, top, rules)
            if m and ml == len(line):
                total += 1
                break
    return total
