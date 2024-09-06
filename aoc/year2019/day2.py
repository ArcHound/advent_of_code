# 2019-2
import logging

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = list()
    for line in in_data.splitlines():
        data += [int(x) for x in line.split(",")]
    return data


def process_program(data_og):
    ip = 0
    done = False
    data = data_og.copy()
    while not done:
        code = data[ip]
        if code == 99:
            return data[0]
        elif code == 1:
            data[data[ip + 3]] = data[data[ip + 1]] + data[data[ip + 2]]
            ip += 4
        elif code == 2:
            data[data[ip + 3]] = data[data[ip + 1]] * data[data[ip + 2]]
            ip += 4
        else:
            return -1  # error


def part1(in_data, test=False):
    data = parse_data(in_data)
    if not test:
        data[1] = 12
        data[2] = 2
    return process_program(data)


def part2(in_data, test=False):
    data = parse_data(in_data)
    for i in range(100):
        for j in range(100):
            data[1] = i
            data[2] = j
            if process_program(data) == 19690720:
                return i * 100 + j
    return -1
