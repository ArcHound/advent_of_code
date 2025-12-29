# 2020-20

import logging
from aoc_lib.map2d import Map2d
from aoc_lib.vector2d import *
from aoc_lib.pixels import *
from collections import Counter

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = dict()
    state = None
    buf = ""
    num = 0
    for line in in_data.splitlines():
        if "Tile" in line:
            num = int(line.strip().split(" ")[1][:-1])
        elif line.strip() == "":
            m = Map2d.from_lines(buf)
            data[num] = m
            buf = ""
        else:
            buf += line.strip() + "\n"
    if num not in data:
        m = Map2d.from_lines(buf)
        data[num] = m
    return data


def part1(in_data, test=False):
    data = parse_data(in_data)
    border_data = {i: data[i].borders() for i in data}
    all_borders = list()
    for i in border_data:
        for j in border_data[i]:
            all_borders.append(j)
            all_borders.append(j[::-1])
    counter = Counter(all_borders)
    # now, the corners have two borders without a match
    prod = 1
    for i in border_data:
        single_lines = 0
        for j in border_data[i]:
            if counter[j] == 1:
                single_lines += 1
        if single_lines == 2:
            prod *= i
    return prod


def find_and_rotate(tile, edge, direction_i, maps, borders):
    other_tile = [
        x
        for x in borders
        if (edge in borders[x] or edge[::-1] in borders[x]) and x != tile
    ][0]
    m = maps[other_tile]
    m_b = m.borders()
    while edge != m_b[direction_i] and edge[::-1] != m_b[direction_i]:
        m = m.rotate_clockwise()
        m_b = m.borders()
    if edge[::-1] in m_b:
        if direction_i in [0, 1]:
            m = m.flip_vertically()
        else:
            m = m.flip_horizontally()
    return other_tile, m


def find_monsters(final_map, encoded_monster):
    for i in range(len(final_map.obstacle_str)):
        p = final_map.translate_index(i)
        if all(
            [final_map.in_bounds_point(v_add(p, x)) for x in encoded_monster]
        ) and all([final_map.get_point(v_add(p, x)) == "#" for x in encoded_monster]):
            for x in encoded_monster:
                final_map.set_point(v_add(p, x), "O")


def part2(in_data, test=False):
    data = parse_data(in_data)
    border_data = {i: data[i].borders() for i in data}
    all_borders = list()
    for i in border_data:
        for j in border_data[i]:
            all_borders.append(j)
            all_borders.append(j[::-1])
    counter = Counter(all_borders)
    log.debug(counter)
    # let's fix a corner and move from there
    fc = 0
    for i in border_data:
        single_lines = 0
        for j in border_data[i]:
            if counter[j] == 1:
                single_lines += 1
        if single_lines == 2:
            fc = i
            break
    log.debug(fc)
    fc_map = data[fc]
    t, b, l, r = fc_map.borders()
    while counter[t] != 1 or counter[l] != 1:
        fc_map = fc_map.rotate_clockwise()
        t, b, l, r = fc_map.borders()
    # fc is top left
    first_col = [fc_map]
    first_col_i = [fc]
    iter_map = fc_map
    prev_tile = fc
    while counter[b] != 1:
        index, iter_map = find_and_rotate(prev_tile, b, 0, data, border_data)
        first_col.append(iter_map)
        first_col_i.append(index)
        t, b, l, r = iter_map.borders()
        prev_tile = index
    log.debug(first_col_i)
    rows = list()
    row_is = list()
    log.debug(data[2473])
    log.debug(data[1543])
    for i in range(len(first_col)):
        index = first_col_i[i]
        iter_map = first_col[i]
        t, b, l, r = iter_map.borders()
        row = [iter_map]
        row_i = [index]
        while counter[r] != 1:
            log.debug(iter_map)
            log.debug(index)
            index, iter_map = find_and_rotate(index, r, 2, data, border_data)
            row.append(iter_map)
            row_i.append(index)
            t, b, l, r = iter_map.borders()
            log.debug("------")
        rows.append(row)
        row_is.append(row_i)
    log.debug(row_is)
    # join rows
    joined_rows = list()
    for i in range(len(rows)):
        row = rows[i]
        row_i = row_is[i]
        m = row[0].trim_edges()
        for j in range(1, len(row)):
            tm = row[j].trim_edges()
            m = Map2d.join_maps_left_right(m, tm)
        joined_rows.append(m)
    for jr in joined_rows:
        log.debug(jr)
    final_map = joined_rows[0]
    for j in range(1, len(joined_rows)):
        final_map = Map2d.join_maps_top_bottom(final_map, joined_rows[j])
    log.debug(final_map)
    # find the monsters
    monster_str = """..................#.
#....##....##....###
.#..#..#..#..#..#...
"""
    monster_map = Map2d.from_lines(monster_str)
    log.debug(monster_map)
    encoded_monster = [
        monster_map.translate_index(i)
        for i in range(len(monster_map.obstacle_str))
        if monster_map.get_index(i) == "#"
    ]
    log.debug(encoded_monster)
    # here I pray that the monsters don't overlap
    log.debug(final_map)
    find_monsters(final_map, encoded_monster)
    final_map = final_map.rotate_clockwise()
    for i in range(3):
        find_monsters(final_map, encoded_monster)
        final_map = final_map.rotate_clockwise()
    final_map = final_map.flip_vertically()
    for i in range(4):
        find_monsters(final_map, encoded_monster)
        final_map = final_map.rotate_clockwise()
    log.debug(final_map)
    # image
    pixel_dict = {
        final_map.translate_index(i): final_map.get_index(i)
        for i in range(len(final_map.obstacle_str))
    }
    pixel_map = {".": (0, 0, 127), "#": (50, 50, 50), "O": (255, 0, 255)}
    pd = map_pixel_dict(pixel_dict, pixel_map)
    draw_array(dict_to_array(pd))
    return sum(
        [1 for i in range(len(final_map.obstacle_str)) if final_map.get_index(i) == "#"]
    )
