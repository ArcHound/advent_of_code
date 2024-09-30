# 2019-13
import logging
from aoc_lib.intcode2019 import Intcode2019
from aoc_lib.map2d import Map2d

log = logging.getLogger("aoc_logger")


def part1(in_data, test=False):
    program = Intcode2019.parse_int_program(in_data)
    computer = Intcode2019()
    computer.run_program_sync(program)
    output = computer.get_list_output()
    x = 0
    y = 0
    t = 0
    game_map = dict()
    for i in range(len(output)):
        if i % 3 == 0:
            x = output[i]
        elif i % 3 == 1:
            y = output[i]
        else:
            game_map[(x, y)] = output[i]
    counter = 0
    for x in game_map:
        if game_map[x] == 2:
            counter += 1
    return counter


def check_map(program):
    computer = Intcode2019()
    computer.run_program_sync(program)
    output = computer.get_list_output()
    x = 0
    y = 0
    t = 0
    game_map = dict()
    for i in range(len(output)):
        if i % 3 == 0:
            x = output[i]
        elif i % 3 == 1:
            y = output[i]
        else:
            game_map[(x, y)] = output[i]
    xs = [x[0] for x in game_map.keys()]
    ys = [y[1] for y in game_map.keys()]
    bounds = ((min(xs), min(ys)), (max(xs) + 1, max(ys) + 1))
    obs_str = "." * ((max(xs) - min(xs) + 1) * (max(ys) - min(ys) + 1))
    map2d = Map2d(obs_str, bounds)
    draw_map = {0: ".", 1: "#", 2: "B", 3: "-", 4: "o"}
    for x in game_map:
        map2d.set_point(x, draw_map[game_map[x]])
    s = map2d.debug_draw()
    log.debug(s)


def part2(in_data, test=False):
    program = Intcode2019.parse_int_program(in_data)
    # hack the memory to make the bar looooong
    for i in range(1324, 1358):
        program[i] = 3
    check_map(program)
    # after the elaborate check is done, run the program for real
    program[0] = 2
    computer = Intcode2019()
    computer.run_program_sync(
        program, [0 for i in range(500000)]
    )  # 500k inputs should do the trick
    l = computer.get_list_output()
    # log.debug(l)
    return l[-1]  # it's the last number, as it should be
