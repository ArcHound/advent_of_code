# 2015-06

import logging

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = list()
    for line in in_data.splitlines():
        tokens = line.strip().split(" ")
        inst = ""
        if tokens[0] == "turn":
            inst = tokens[1]
            start = tuple([int(x) for x in tokens[2].split(",")])
            end = tuple([int(x) for x in tokens[4].split(",")])
        elif tokens[0] == "toggle":
            inst = tokens[0]
            start = tuple([int(x) for x in tokens[1].split(",")])
            end = tuple([int(x) for x in tokens[3].split(",")])
        data.append((inst, start, end))
    return data


def process(map_map, inst, start, end):
    for x in range(start[0], end[0] + 1):
        for y in range(start[1], end[1] + 1):
            if inst == "on":
                map_map[(x, y)] = "#"
            elif inst == "off":
                map_map[(x, y)] = "."
            elif inst == "toggle":
                if map_map[(x, y)] == ".":
                    map_map[(x, y)] = "#"
                else:
                    map_map[(x, y)] = "."


def part1(in_data, test=False):
    data = parse_data(in_data)
    map_map = dict()
    for i in range(1000 + 1):
        for j in range(1000 + 1):
            map_map[(i, j)] = "."
    for inst, start, end in data:
        process(map_map, inst, start, end)
    count = sum([1 for x in map_map if map_map[x] == "#"])
    return count


def process_2(map_map, inst, start, end):
    for x in range(start[0], end[0] + 1):
        for y in range(start[1], end[1] + 1):
            if inst == "on":
                map_map[(x, y)] += 1
            elif inst == "off":
                map_map[(x, y)] -= 1
                if map_map[(x, y)] < 0:
                    map_map[(x, y)] = 0
            elif inst == "toggle":
                map_map[(x, y)] += 2


def part2(in_data, test=False):
    if test:
        return "part2 output 2015-06"
    data = parse_data(in_data)
    map_map = dict()
    for i in range(1000 + 1):
        for j in range(1000 + 1):
            map_map[(i, j)] = 0
    for inst, start, end in data:
        process_2(map_map, inst, start, end)
    return sum([map_map[x] for x in map_map])
