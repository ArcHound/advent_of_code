# 2019-19
import logging
from aoc_lib.intcode2019 import Intcode2019
from aoc_lib.map2d import Map2d

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = list()
    for line in in_data.splitlines():
        data.append(line)
    return [int(x) for x in data[0].split(",")]


def part1(in_data, test=False):
    program = parse_data(in_data)
    pulled = 0
    obstacle_list = list()
    bounds = ((0, 0), (50, 50))
    computer = Intcode2019()
    for i in range(bounds[0][0], bounds[1][0]):
        for j in range(bounds[0][1], bounds[1][1]):
            computer.run_program_sync(program, [i, j])
            o = computer.get_single_output()
            if o > 0:
                pulled += 1
                obstacle_list.append((i, j))
    map2d = Map2d.from_obstacle_list(obstacle_list, bounds=bounds)
    # log.error(map2d.debug_draw())
    return pulled


def part2(in_data, test=False):
    program = parse_data(in_data)
    pulled = 0
    obstacle_list = list()
    indent = 0
    computer = Intcode2019()
    point = (0, 0)
    i = indent
    for j in range(101, 400000):
        obstacle = False
        while not obstacle:
            computer.run_program_sync(program, [i, j])
            o = computer.get_single_output()
            if o > 0:
                obstacle = True
                break
            i += 1
        # check square
        computer.run_program_sync(program, [i, j - 99])
        o1 = computer.get_single_output()
        computer.run_program_sync(program, [i + 99, j - 99])
        o2 = computer.get_single_output()
        if o1 > 0 and o2 > 0:
            point = (i, j)
            break
        if j % 100 == 0:
            log.error(j)
    return point[0] * 10000 + (point[1] - 99)
