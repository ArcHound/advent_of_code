# 2016-08

import logging
from aoc_lib.map2d import Map2d

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = list()
    for line in in_data.splitlines():
        tokens = line.strip().split(" ")
        if tokens[0] == "rect":
            a, b = tokens[1].split("x")
            data.append(("rect", int(a), int(b)))
        elif tokens[0] == "rotate":
            vector = (0, 0)
            start = (0, 0)
            line_id = int(tokens[2].split("=")[1])
            if tokens[1] == "row":
                vector = (1, 0)
                start = (0, line_id)
            elif tokens[1] == "column":
                vector = (0, 1)
                start = (line_id, 0)
            amount = int(tokens[4])
            data.append(("rotate", vector, start, amount))
    return data


def process_on_map(map2d, inst):
    inst_type = inst[0]
    if inst_type == "rect":
        for i in range(inst[1]):
            for j in range(inst[2]):
                map2d.set_point((i, j), "#")
    elif inst_type == "rotate":
        start, vector, amount = inst[2], inst[1], inst[3]
        points = map2d.trace(start, vector, False)
        p_dict = {p: str(map2d.get_point(p)) for p in points}
        log.debug(p_dict)
        for p in p_dict:
            map2d.set_point(
                (
                    (p[0] + vector[0] * amount) % map2d.bounds[1][0],
                    (p[1] + vector[1] * amount) % map2d.bounds[1][1],
                ),
                p_dict[p],
            )


def part1(in_data, test=False):
    data = parse_data(in_data)
    dims = (50, 6) if not test else (7, 3)
    map2d = Map2d("." * dims[0] * dims[1], ((0, 0), dims))
    for inst in data:
        process_on_map(map2d, inst)
    return sum([1 for x in map2d.obstacle_str if x == "#"])


def part2(in_data, test=False):
    data = parse_data(in_data)
    dims = (50, 6) if not test else (7, 3)
    map2d = Map2d("." * dims[0] * dims[1], ((0, 0), dims))
    for inst in data:
        process_on_map(map2d, inst)
    log.critical(map2d.debug_draw())
    return "Sorry, no OCR"
