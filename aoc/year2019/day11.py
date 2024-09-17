# 2019-11
import logging
from threading import Event
from aoc_lib.intcode2019 import Intcode2019
from aoc_lib.pixels import default_draw

log = logging.getLogger("aoc_logger")


class HullPaintingRobot:
    # orientations = ['<', '^', '>', 'v']
    orientations = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    def __init__(self, program):
        self.position = (0, 0)
        self.orientation_pointer = 1
        self.program = program
        self.computer = Intcode2019()
        self.painted_tiles = set()
        self.paint_map = dict()

    def process_tuple(self, x, y):
        self.painted_tiles.add(self.position)
        self.paint_map[self.position] = x
        if y == 0:
            self.orientation_pointer = (self.orientation_pointer + 3) % 4
        elif y == 1:
            self.orientation_pointer = (self.orientation_pointer + 1) % 4

    def loop_inner(self):
        in_color = 0
        if self.position in self.paint_map:
            in_color = self.paint_map[self.position]
        self.computer.send_single_input(in_color)
        x = self.computer.get_single_output()
        y = self.computer.get_single_output()
        self.process_tuple(x, y)
        self.position = (
            self.position[0] + self.orientations[self.orientation_pointer][0],
            self.position[1] + self.orientations[self.orientation_pointer][1],
        )

    def gogogo(self):
        finished = Event()
        self.computer.run_program(self.program, finish_event=finished)
        counter = 0
        while not finished.is_set():
            counter += 1
            self.loop_inner()
        log.debug(f"counter {counter}")


def parse_data(in_data):
    data = list()
    for line in in_data.splitlines():
        data.append(line)
    return [int(x) for x in data[0].split(",")]


def part1(in_data, test=False):
    program = parse_data(in_data)
    hpr = HullPaintingRobot(program)
    hpr.gogogo()
    # log.debug(hpr.paint_map)
    return len(hpr.painted_tiles)


def part2(in_data, test=False):
    program = parse_data(in_data)
    hpr = HullPaintingRobot(program)
    hpr.paint_map[(0, 0)] = 1  # start on a white tile
    hpr.gogogo()
    default_draw(hpr.paint_map)
    return 0
