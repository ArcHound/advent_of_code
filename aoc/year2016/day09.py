# 2016-09

import logging

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = list()
    for line in in_data.splitlines():
        data.append(line.strip())
    return data


def decompress_simple(line):
    state = "open"
    main_buf = ""
    mark_buf = ""
    exp_buf = ""
    pointer = 0
    marker = (0, 0)
    while pointer < len(line):
        c = line[pointer]
        if state == "open" and c != "(":
            main_buf += c
            pointer += 1
        elif state == "open" and c == "(":
            mark_buf = ""
            state = "marker"
            pointer += 1
        elif state == "marker" and c != ")":
            mark_buf += c
            pointer += 1
        elif state == "marker" and c == ")":
            marker = (int(mark_buf.split("x")[0]), int(mark_buf.split("x")[1]))
            pointer += 1
            exp_buf = ""
            for i in range(marker[0]):
                exp_buf += line[pointer + i]
            for i in range(marker[1]):
                main_buf += exp_buf
            pointer += marker[0]
            state = "open"
    return main_buf


def part1(in_data, test=False):
    data = parse_data(in_data)
    counter = 0
    for line in data:
        s = decompress_simple(line)
        log.debug(s)
        counter += len(s)
    return counter


def decompress_recurse(line):
    if "(" not in line:
        return len(line)
    line_total = 0
    pointer = 0
    main_buf = ""
    mark_buf = ""
    exp_buf = ""
    marker = (0, 0)
    state = "open"
    while pointer < len(line):
        c = line[pointer]
        if state == "open" and c != "(":
            main_buf += c
            pointer += 1
        elif state == "open" and c == "(":
            mark_buf = ""
            state = "marker"
            pointer += 1
        elif state == "marker" and c != ")":
            mark_buf += c
            pointer += 1
        elif state == "marker" and c == ")":
            marker = (int(mark_buf.split("x")[0]), int(mark_buf.split("x")[1]))
            pointer += 1
            exp_buf = ""
            for i in range(marker[0]):
                exp_buf += line[pointer + i]
            line_total += decompress_recurse(exp_buf) * marker[1]
            pointer += marker[0]
            state = "open"
    line_total += len(main_buf)
    return line_total


def part2(in_data, test=False):
    data = parse_data(in_data)
    counter = 0
    for line in data:
        s = decompress_recurse(line)
        log.debug(s)
        counter += s
    return counter
