# 2022-15

import logging
import re
from aoc_lib.vector2d import *
from aoc_lib.interval import Interval
import dataclasses
from tqdm import tqdm

log = logging.getLogger("aoc_logger")


@dataclasses.dataclass
class Circle:
    center: tuple[int, int]
    radius: int
    def_point: tuple[int, int]

    def line_circle_intersects_y(self, y):
        return self.center[1] - self.radius <= y and y <= self.center[1] + self.radius

    def line_within_circle_y(self, y):
        result = list()
        if self.line_circle_intersects_y(y):
            lost = abs(self.center[1] - y)
            result.append((self.center[0], y))
            for i in range(1, self.radius - lost + 1):
                result.append((self.center[0] + i, y))
                result.append((self.center[0] - i, y))
        return result

    def line_within_circle_y_interval(self, y):
        result = None
        if self.line_circle_intersects_y(y):
            lost = abs(self.center[1] - y)
            result = Interval(
                self.center[0] - (self.radius - lost),
                self.center[0] + (self.radius - lost) + 1,
            )
        return result

    def point_in_circle(self, p):
        return abs(self.center[0] - p[0]) + abs(self.center[1] - p[1]) <= self.radius


def parse_data(in_data):
    data = list()
    for line in in_data.splitlines():
        match = re.search(
            r"Sensor at x=(?P<sx>-?[0-9]+), y=(?P<sy>-?[0-9]+): closest beacon is at x=(?P<bx>-?[0-9]+), y=(?P<by>-?[0-9]+)",
            line,
        )
        sx = int(match["sx"])
        sy = int(match["sy"])
        bx = int(match["bx"])
        by = int(match["by"])
        data.append(
            Circle(
                center=(sx, sy), def_point=(bx, by), radius=abs(sx - bx) + abs(sy - by)
            )
        )
    return data


def part1(in_data, test=False):
    data = parse_data(in_data)
    if test:
        target_row = 10
    else:
        target_row = 2000000
    log.debug(data)
    matched = set()
    beacons = {c.def_point for c in data}
    for circle in data:
        intersection = circle.line_within_circle_y(target_row)
        for i in intersection:
            if i not in beacons:
                matched.add(i)
    log.debug(sorted(list(matched), key=lambda x: x[0]))
    return len(matched)


def part2(in_data, test=False):
    data = parse_data(in_data)
    if test:
        max_c = 20
    else:
        max_c = 4000000
    log.debug(data)
    matched = set()
    beacons = {c.def_point for c in data}
    result = 0
    target = Interval(0, max_c + 1)
    for y in tqdm(range(max_c + 1)):
        big_interval = list()
        for circle in data:
            intersection = circle.line_within_circle_y_interval(y)
            if intersection:
                big_interval.append(intersection)
        log.debug(big_interval)
        joined = Interval.join_list(big_interval)
        log.debug(joined)
        if all([not x.contains(target) for x in joined]):
            log.debug(y)
            x = [x.start - 1 for x in joined if 0 <= x.start and x.start <= max_c][0]
            result = 4000000 * x + y
            break
    return result
