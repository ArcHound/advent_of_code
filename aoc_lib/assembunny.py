import logging
from copy import deepcopy

log = logging.getLogger("aoc_logger")


def parse_program(in_data):
    data = list()
    for line in in_data.splitlines():
        data.append(tuple(line.strip().split(" ")))
    return data


class AssemBunny:
    def __init__(self, a=0, b=0, c=0, d=0):
        self.registers = dict()
        self.registers["a"] = a
        self.registers["b"] = b
        self.registers["c"] = c
        self.registers["d"] = d

    def get_register(self, x):
        if x not in "abcd":
            raise ValueError(f"Invalid register {x}")
        return self.registers[x]

    def set_register(self, x, val):
        if x not in "abcd":
            raise ValueError(f"Invalid register {x}")
        if type(val) != int:
            raise TypeError(f"Value needs to be int, got {type(val)} instead")
        self.registers[x] = val

    def register_or_const(self, a):
        if a in "abcd":
            return self.get_register(a)
        else:
            return int(a)

    def run_program(self, program_data):
        program = deepcopy(program_data)
        ip = 0
        while ip < len(program):
            log.debug(ip)
            log.debug(program)
            log.debug(self.registers)
            inst = program[ip]
            if inst[0] == "inc":
                if inst[1] not in "abcd":
                    ip += 1
                    continue
                self.registers[inst[1]] += 1
                ip += 1
            elif inst[0] == "dec":
                if inst[1] not in "abcd":
                    ip += 1
                    continue
                self.registers[inst[1]] -= 1
                ip += 1
            elif inst[0] == "cpy":
                if inst[2] not in "abcd":
                    ip += 1
                    continue
                else:
                    self.registers[inst[2]] = self.register_or_const(inst[1])
                ip += 1
            elif inst[0] == "jnz":
                con = self.register_or_const(inst[1])
                jmp = self.register_or_const(inst[2])
                if con != 0:
                    ip += jmp
                else:
                    ip += 1
            elif inst[0] == "tgl":
                where = self.register_or_const(inst[1])
                if ip + where < 0 or ip + where >= len(program):
                    ip += 1
                    continue
                new_inst = deepcopy(program[ip + where])
                if new_inst[0] in ["inc", "dec", "tgl"]:
                    if new_inst[0] == "inc":
                        new_inst = ("dec", new_inst[1])
                    else:
                        new_inst = ("inc", new_inst[1])
                elif new_inst[0] in ["cpy", "jnz"]:
                    if new_inst[0] == "jnz":
                        new_inst = ("cpy", new_inst[1], new_inst[2])
                    else:
                        new_inst = ("jnz", new_inst[1], new_inst[2])
                program[ip + where] = new_inst
                ip += 1
