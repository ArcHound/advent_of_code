# 2016-17

import logging
import hashlib
from aoc_lib.functional import bfs

log = logging.getLogger("aoc_logger")

dirs = "UDLR"
dir_vectors = {"U": (0, -1), "D": (0, 1), "L": (-1, 0), "R": (1, 0)}


def doors_from_path(salt, path):
    digest = hashlib.md5((salt + path).encode()).hexdigest()[:4]
    open_chars = "bcdef"
    return (
        digest[0] in open_chars,
        digest[1] in open_chars,
        digest[2] in open_chars,
        digest[3] in open_chars,
    )


def nearby_points(point, dims=((0, 0), (4, 4))):
    points = list()
    if point[1] == dims[0][1]:
        points.append(None)
    else:
        points.append((point[0], point[1] - 1))
    if point[1] == dims[1][1] - 1:
        points.append(None)
    else:
        points.append((point[0], point[1] + 1))
    if point[0] == dims[0][0]:
        points.append(None)
    else:
        points.append((point[0] - 1, point[1]))
    if point[0] == dims[1][0] - 1:
        points.append(None)
    else:
        points.append((point[0] + 1, point[1]))
    return points


target = (3, 3)


def is_done(position):
    point, path = position
    return point == target


def part1(in_data, test=False):
    salt = in_data.strip()

    def legal_moves(position):
        point, path = position
        moves = list()
        doors = doors_from_path(salt, path)
        points = nearby_points(point)
        for i in range(4):
            if doors[i] and points[i] is not None:
                moves.append(((points[i], path + dirs[i]), 1))
        return moves

    final_position = list()
    path_len = bfs(((0, 0), ""), is_done, legal_moves, False, final_position)
    log.debug(path_len)
    point, path = final_position[0]
    return path


def part2(in_data, test=False):
    salt = in_data.strip()
    forbidden_paths = list()

    def legal_moves(position):
        point, path = position
        moves = list()
        doors = doors_from_path(salt, path)
        points = nearby_points(point)
        for i in range(4):
            if (
                doors[i]
                and points[i] is not None
                and path + dirs[i] not in forbidden_paths
            ):
                moves.append(((points[i], path + dirs[i]), 1))
        return moves

    final_position = list()
    path_len = 0
    max_path_len = 0
    while path_len != -1:
        path_len = bfs(((0, 0), ""), is_done, legal_moves, False, final_position)
        if path_len == -1:
            break
        point, path = final_position[0]
        final_position = list()
        forbidden_paths.append(path)
        log.info(path_len)
        if path_len > max_path_len:
            max_path_len = path_len
    return max_path_len
