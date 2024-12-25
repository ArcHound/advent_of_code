# 2024-17

import logging

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    program = list()
    registers = dict()
    for line in in_data.splitlines():
        if line.startswith("Register"):
            registers[line.split(" ")[1][0]] = int(line.split(" ")[-1])
        elif line.startswith("Program"):
            program = [int(x) for x in line.split(" ")[1].split(",")]
    registers["IP"] = 0
    registers["OUT"] = list()
    return registers, program


register_combo_map = {4: "A", 5: "B", 6: "C"}


def combo(registers, op):
    if 0 <= op and op <= 3:
        return op
    elif 4 <= op and op <= 6:
        return registers[register_combo_map[op]]
    else:
        raise ValueError("Invalid combo operand, shouldn't happen")


def adv(registers, op):
    registers["A"] = registers["A"] // pow(2, combo(registers, op))
    registers["IP"] += 2


def bxl(registers, op):
    registers["B"] = registers["B"] ^ op
    registers["IP"] += 2


def bst(registers, op):
    registers["B"] = combo(registers, op) % 8
    registers["IP"] += 2


def jnz(registers, op):
    if registers["A"] != 0:
        registers["IP"] = op
    else:
        registers["IP"] += 2


def bxc(registers, op):
    registers["B"] = registers["B"] ^ registers["C"]
    registers["IP"] += 2


def out(registers, op):
    registers["OUT"].append(combo(registers, op) % 8)
    registers["IP"] += 2


def bdv(registers, op):
    registers["B"] = registers["A"] // pow(2, combo(registers, op))
    registers["IP"] += 2


def cdv(registers, op):
    registers["C"] = registers["A"] // pow(2, combo(registers, op))
    registers["IP"] += 2


op_map = {0: adv, 1: bxl, 2: bst, 3: jnz, 4: bxc, 5: out, 6: bdv, 7: cdv}


def run_program(program, registers):
    while registers["IP"] < len(program):
        code = program[registers["IP"]]
        op = program[registers["IP"] + 1]
        f = op_map[code]
        deb_registers = {x: bin(registers[x]) for x in registers if x in "ABC"}
        f(registers, op)


def part1(in_data, test=False):
    registers, program = parse_data(in_data)
    log.debug(registers)
    log.debug(program)
    run_program(program, registers)
    return ",".join([str(x) for x in registers["OUT"]])


# 2,4,1,3,7,5,0,3,1,4,4,7,5,5,3,0
# 2,4, B = A%8 # take last three bits
# 1,3, B = B XOR 3 # flip last two
# 7,5, C = A >> B # C = shift A by B
# 0,3, A = A >> 3 # shift A by 3
# 1,4, B = B XOR 4 # flip the third bit
# 4,7, B = B XOR C # B XOR C
# 5,5, output B (last three bits)
# 3,0  goto start

# 0,3,5,4,3,0
# 0,3 A = A >> 3
# 5,4 output A (last three bits)
# 3,0 goto start


def options3(a):
    options = dict()
    for i in range(3):
        if a[i] is None:
            options[i] = [1, 0]
        else:
            options[i] = [a[i]]
    total_options = list()
    for i in options[0]:
        for j in options[1]:
            for k in options[2]:
                total_options.append([i, j, k])
    return total_options


def recursion(a, level, program, results):
    # a is in reverse bit order!
    if level == len(program):
        for i in range(len(a)):
            if a[i] is None:
                a[i] = 0
        results.append(a)
        return a
    if all([x in [1, 0] for x in a]):
        results.append(a)
        return a
    check_a = a[3 * level : 3 * level + 3]
    for option in options3(check_a):
        # this whole thing is tailored to my input
        new_a = a.copy()
        for i in range(3):
            new_a[3 * level + i] = option[i]
        num_a = (
            new_a[3 * level] + 2 * (new_a[3 * level + 1]) + 4 * (new_a[3 * level + 2])
        )
        shift = (
            1
            - new_a[3 * level]
            + 2 * (1 - new_a[3 * level + 1])
            + 4 * new_a[3 * level + 2]
        )
        target = program[level] ^ 7 ^ num_a
        # check for contradictions
        contradiction = False
        if 3 * level + shift + 2 > len(a):
            contradiction = True
        for i in range(3):
            index = 3 * level + shift + i
            if new_a[index] is None or new_a[index] == target % 2:
                new_a[index] = target % 2
            else:
                contradiction = True
            target = target // 2
        # no contradictions, we can fix couple more bits next time
        if not contradiction:
            recursion(new_a, level + 1, program, results)
        else:
            pass
            # log.error("Contradiction!")


def part2(in_data, test=False):
    registers, program = parse_data(in_data)
    registers_copy = {x: registers[x] for x in registers}
    program_flag = ",".join([str(x) for x in program])
    # yea, right
    # done = False
    # i = 0
    # while not done:
    #     if i%10000 == 0:
    #         log.error(i)
    #     registers = {x:registers_copy[x] for x in registers_copy}
    #     registers["A"] = i
    #     run_program(program, registers)
    #     if ','.join([str(x) for x in registers["OUT"]])==program_flag:
    #         done = True
    #         return i
    #     i+= 1
    # ok, new plan:
    a = [None, None, None] * 3 * len(program)
    results = list()
    recursion(a, 0, program, results)
    valid_results = list()
    for result in results:
        a = int("".join([str(x) for x in reversed(result)]), 2)
        registers = {x: registers_copy[x] for x in registers_copy}
        registers["A"] = a
        registers["OUT"] = list()
        run_program(program, registers)
        if registers["OUT"] == program:
            valid_results.append(a)
    log.error(len(valid_results))
    return min(valid_results)
