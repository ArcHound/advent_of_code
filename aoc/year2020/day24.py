# 2020-24

import logging
from aoc_lib.vector2d import *

log = logging.getLogger("aoc_logger")

direction_map = {
    "e": (2, 0),
    "se": (1, 1),
    "sw": (-1, 1),
    "w": (-2, 0),
    "nw": (-1, -1),
    "ne": (1, -1),
}

neighbors = [v for k, v in direction_map.items()]


def parse_data(in_data):
    data = list()
    for line in in_data.splitlines():
        buf = list()
        i = 0
        l = line.strip()
        while i < len(l):
            if l[i] == "e" or l[i] == "w":
                buf.append(l[i])
                i += 1
            else:
                buf.append(l[i] + l[i + 1])
                i += 2
        data.append(buf)
    return data


def traverse_path(path, tiles):
    pos = (0, 0)
    for p in path:
        pos = v_add(pos, direction_map[p])
    if pos not in tiles or tiles[pos] == False:
        tiles[pos] = True
    else:
        tiles[pos] = False


def part1(in_data, test=False):
    data = parse_data(in_data)
    log.debug(data)
    tiles = dict()
    for dirs in data:
        traverse_path(dirs, tiles)
    return sum([1 for pos in tiles if tiles[pos]])


def part2(in_data, test=False):
    data = parse_data(in_data)
    tiles = dict()
    for dirs in data:
        traverse_path(dirs, tiles)
    # True is black, False is white
    new_tiles = dict()
    for k, v in tiles.items():
        new_tiles[k] = v
        for n in neighbors:
            p = v_add(k, n)
            if p not in new_tiles:
                new_tiles[p] = False
    tiles = new_tiles
    for i in range(100):
        new_tiles = dict()
        for k, v in tiles.items():
            black_tiles = sum([1 for n in neighbors if tiles.get(v_add(k, n), False)])
            if (v and (black_tiles == 1 or black_tiles == 2)) or (
                not v and black_tiles == 2
            ):
                new_tiles[k] = True
                for n in neighbors:
                    np = v_add(k, n)
                    if np not in new_tiles:
                        new_tiles[np] = False
            else:
                new_tiles[k] = False
        tiles = new_tiles
    return sum([1 for pos in tiles if tiles[pos]])
