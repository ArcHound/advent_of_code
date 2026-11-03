# 2016-24

import logging
from aoc_lib.map2d import Map2d
from aoc_lib.functional import bfs

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    map2d = Map2d.from_lines(in_data)
    points = dict()
    for i in range(len(map2d.obstacle_str)):
        if map2d.get_index(i) in "0123456789":
            points[int(map2d.get_index(i))] = map2d.translate_index(i)
            map2d.set_index(i, ".")
    graph = dict()
    for i in points:
        p = points[i]
        map2d.flood(p)
        for j in points:
            if i == j:
                continue
            new_p = (min([i, j]), max([i, j]))
            if new_p not in graph:
                graph[new_p] = map2d.get_flooded_point(points[j])
        map2d.clear_flood()
    return map2d, points, graph


def part1(in_data, test=False):
    map2d, points, graph = parse_data(in_data)
    node_count = len(points.keys())

    def is_done(pos):
        return len(pos) == node_count

    def legal_moves(pos):
        moves = list()
        for c in points:
            if str(c) not in pos:
                new_p = (min([int(pos[-1]), c]), max([int(pos[-1]), c]))
                moves.append((pos + str(c), graph[new_p]))
        return moves

    start = "0"
    fp = list()
    final_len = bfs(start, is_done, legal_moves, True, fp, False)
    log.debug(fp)
    return final_len


def part2(in_data, test=False):
    map2d, points, graph = parse_data(in_data)
    node_count = len(points.keys())

    def is_done(pos):
        return len(pos) == node_count + 1

    def legal_moves(pos):
        moves = list()
        if len(pos) < node_count:
            for c in points:
                if str(c) not in pos:
                    new_p = (min([int(pos[-1]), c]), max([int(pos[-1]), c]))
                    moves.append((pos + str(c), graph[new_p]))
        elif len(pos) == node_count:
            c = pos[-1]
            new_p = (0, int(c))
            moves.append((pos + "0", graph[new_p]))
        else:
            pass
        return moves

    start = "0"
    fp = list()
    final_len = bfs(start, is_done, legal_moves, True, fp, False)
    return final_len
