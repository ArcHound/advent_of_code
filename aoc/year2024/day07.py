# 2024-07

import logging

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = dict()
    for line in in_data.splitlines():
        result, ops = line.split(": ")
        data[int(result)] = [int(x) for x in ops.split(" ")]
    return data


def try_ops(result, numbers):
    ops_num = len(numbers) - 1
    worked = False
    for i in range(pow(2, ops_num)):
        ops_list = list()
        for j in range(ops_num):
            if (i >> j) % 2 == 0:
                ops_list.append("+")
            else:
                ops_list.append("*")
        log.debug(ops_list)
        total = numbers[0]
        for i in range(1, len(numbers)):
            if ops_list[i - 1] == "+":
                total += numbers[i]
            else:
                total *= numbers[i]
        if total == result:
            worked = True
            log.debug(worked)
            break
    log.debug("---------------")
    return worked


def part1(in_data, test=False):
    data = parse_data(in_data)
    log.debug(data)
    total = 0
    for i in data:
        if try_ops(i, data[i]):
            total += i
    return total


def try_ops2(result, numbers):
    ops_num = len(numbers) - 1
    worked = False
    for i in range(pow(3, ops_num)):
        ops_list = list()
        for j in range(ops_num):
            if (i // pow(3, j)) % 3 == 0:
                ops_list.append("+")
            elif (i // pow(3, j)) % 3 == 1:
                ops_list.append("*")
            else:
                ops_list.append("|")
        log.debug(ops_list)
        total = numbers[0]
        for i in range(1, len(numbers)):
            if ops_list[i - 1] == "+":
                total += numbers[i]
            elif ops_list[i - 1] == "*":
                total *= numbers[i]
            else:
                total = total * pow(10, len(str(numbers[i]))) + numbers[i]
        if total == result:
            worked = True
            log.debug(worked)
            break
    log.debug("---------------")
    return worked


def part2(in_data, test=False):
    data = parse_data(in_data)
    total = 0
    for i in data:
        if try_ops2(i, data[i]):
            total += i
    return total
