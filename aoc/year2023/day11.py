# 2023-11
import logging
from aoc_lib.vector2d import *

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    lines = in_data.splitlines()
    columns = len(lines[0]) * [0]
    rows = len(lines) * [0]
    j = 0
    galaxies = list()
    # simple: note the coordinates of each '#'
    for line in lines:
        i = 0
        for c in line:
            if c == "#":
                # also note that it's present in that column/row
                columns[i] += 1
                rows[j] += 1
                galaxies.append((i, j))
            i += 1
        j += 1
    # then you can see the zeroes - empties
    return (
        galaxies,
        [i for i in range(len(columns)) if columns[i] == 0],
        [j for j in range(len(rows)) if rows[j] == 0],
    )


def part1(in_data):
    galaxies, empty_cols, empty_rows = parse_data(in_data)
    log.debug(galaxies)
    log.debug(empty_cols)
    log.debug(empty_rows)
    new_galaxies = list()
    # not much to talk about here - for each empty row/column note the index then add them all at once so you don't mess with the ordering
    for g in galaxies:
        x_diff = 0
        for c in empty_cols:
            if g[0] > c:
                x_diff += 1
        y_diff = 0
        for c in empty_rows:
            if g[1] > c:
                y_diff += 1
        new_galaxies.append((g[0] + x_diff, g[1] + y_diff))
    galaxies = new_galaxies
    log.debug(galaxies)
    count = 0
    for i in range(len(galaxies)):
        for j in range(i):
            count += v_abs_val(v_diff(galaxies[i], galaxies[j]))
    return count


def part2(in_data):
    galaxies, empty_cols, empty_rows = parse_data(in_data)
    log.debug(galaxies)
    log.debug(empty_cols)
    log.debug(empty_rows)
    new_galaxies = list()
    for g in galaxies:
        x_diff = 0
        for c in empty_cols:
            if g[0] > c:
                x_diff += (
                    1000000 - 1
                )  # the same as above but 1->1000000 so we need to add 1000000-1
        y_diff = 0
        for c in empty_rows:
            if g[1] > c:
                y_diff += 1000000 - 1
        new_galaxies.append((g[0] + x_diff, g[1] + y_diff))
    galaxies = new_galaxies
    log.debug(galaxies)
    count = 0
    for i in range(len(galaxies)):
        for j in range(i):
            count += v_abs_val(v_diff(galaxies[i], galaxies[j]))
    return count
