# 2020-08

import logging

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = list()
    for line in in_data.splitlines():
        inst, val = line.strip().split(" ")
        val = int(val)
        data.append((inst, val))
    return data


def halts_acc(program):
    ip = 0
    acc = 0
    visited = set()
    while ip not in visited:
        visited.add(ip)
        if program[ip][0] == "nop":
            ip += 1
        elif program[ip][0] == "acc":
            acc += program[ip][1]
            ip += 1
        elif program[ip][0] == "jmp":
            ip += program[ip][1]
        if ip >= len(program):
            return "halts!", acc
    return "inf_loop", acc


def part1(in_data, test=False):
    data = parse_data(in_data)
    m, val = halts_acc(data)
    return val


def part2(in_data, test=False):
    data = parse_data(in_data)
    for p in range(len(data)):
        i, c = data[p]
        copy_data = list(data)
        if i == "jmp":
            copy_data[p] = ("nop", c)
        elif i == "nop":
            copy_data[p] = ("jmp", c)
        m, val = halts_acc(copy_data)
        if m == "halts!":
            return val
