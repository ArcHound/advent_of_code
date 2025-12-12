# 2025-12

import logging
from dataclasses import dataclass

log = logging.getLogger("aoc_logger")


@dataclass
class Puzzle:
    length: int
    width: int
    tile_counts: list[int]


def parse_data(in_data):
    tiles = list()
    data = list()
    for line in in_data.splitlines():
        if "x" in line:
            sq, counts = line.strip().split(": ")
            data.append(
                Puzzle(
                    length=int(sq.split("x")[0]),
                    width=int(sq.split("x")[1]),
                    tile_counts=[int(x) for x in counts.split(" ")],
                )
            )
        else:
            # not implemented
            continue
    return data


def part1(in_data, test=False):
    data = parse_data(in_data)
    log.debug(data)
    # ugly trick incoming
    # basically, assume each part is a 3x3 brick
    # if that fits, the whole fits.
    # if that doesn't fit, let's just say it's impossible
    count = 0
    for puzzle in data:
        squares = (puzzle.length // 3) * (puzzle.width // 3)
        if squares >= sum(puzzle.tile_counts):
            count += 1
    return count
