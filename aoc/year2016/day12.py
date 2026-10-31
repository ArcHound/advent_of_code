# 2016-12

import logging

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = list()
    for line in in_data.splitlines():
        data.append(tuple(line.strip().split(" ")))
    return data


def run_program(registers, program):
    ip = 0
    while ip < len(program):
        inst = program[ip]
        if inst[0] == "inc":
            registers[inst[1]] += 1
            ip += 1
        elif inst[0] == "dec":
            registers[inst[1]] -= 1
            ip += 1
        elif inst[0] == "cpy":
            if inst[1] in "abcd":
                registers[inst[2]] = registers[inst[1]]
            else:
                registers[inst[2]] = int(inst[1])
            ip += 1
        elif inst[0] == "jnz":
            if inst[1] in "abcd":
                if registers[inst[1]] != 0:
                    ip += int(inst[2])
                else:
                    ip += 1
            elif int(inst[1]) != 0:
                ip += int(inst[2])
            else:
                ip += 1


def part1(in_data, test=False):
    data = parse_data(in_data)
    registers = {"a": 0, "b": 0, "c": 0, "d": 0}
    run_program(registers, data)
    return registers["a"]


def part2(in_data, test=False):
    data = parse_data(in_data)
    registers = {"a": 0, "b": 0, "c": 1, "d": 0}
    run_program(registers, data)
    return registers["a"]
