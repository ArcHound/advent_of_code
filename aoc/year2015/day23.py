# 2015-23

import logging
from dataclasses import dataclass


@dataclass
class Instruction:
    name: str
    op1: str
    op2: str


class Computer:
    def __init__(self, program):
        self.ip = 0
        self.program = program
        self.bound = len(program)
        self.a = 0
        self.b = 0

    def process_instruction(self, instruction):
        if instruction.name == "hlf":
            if instruction.op1 == "a":
                self.a = self.a // 2
            else:
                self.b = self.b // 2
            self.ip += 1
        elif instruction.name == "tpl":
            if instruction.op1 == "a":
                self.a = self.a * 3
            else:
                self.b = self.b * 3
            self.ip += 1
        elif instruction.name == "inc":
            if instruction.op1 == "a":
                self.a = self.a + 1
            else:
                self.b = self.b + 1
            self.ip += 1
        elif instruction.name == "jmp":
            amount = int(instruction.op1)
            self.ip += amount
        elif instruction.name == "jie":
            if instruction.op1 == "a":
                if self.a % 2 == 0:
                    self.ip += int(instruction.op2)
                else:
                    self.ip += 1
            else:
                if self.b % 2 == 0:
                    self.ip += int(instruction.op2)
                else:
                    self.ip += 1
        elif instruction.name == "jio":
            if instruction.op1 == "a":
                if self.a == 1:
                    self.ip += int(instruction.op2)
                else:
                    self.ip += 1
            else:
                if self.b == 1:
                    self.ip += int(instruction.op2)
                else:
                    self.ip += 1

    def run(self, a=0, b=0):
        self.a = a
        self.b = b
        while self.ip < self.bound:
            self.process_instruction(self.program[self.ip])
        return self.b


log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = list()
    for line in in_data.splitlines():
        tokens = line.strip().split(" ")
        op1 = None
        op2 = None
        if "," in line:
            op1 = tokens[1][:-1]
            op2 = tokens[2]
        else:
            op1 = tokens[1]
        data.append(Instruction(tokens[0], op1, op2))
    return data


def part1(in_data, test=False):
    data = parse_data(in_data)
    c = Computer(data)
    return c.run()


def part2(in_data, test=False):
    data = parse_data(in_data)
    c = Computer(data)
    return c.run(a=1)
