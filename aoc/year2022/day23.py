# 2022-23

import logging
from aoc_lib.map2d import Map2d
from collections import defaultdict
from tqdm import tqdm

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    map2d = Map2d.from_lines(in_data)
    elves_dict = defaultdict(bool)
    for i in range(len(map2d.obstacle_str)):
        if map2d.get_index(i) == "#":
            elves_dict[map2d.translate_index(i)] = True
    return elves_dict


def move_alg(elves, phase):
    wannabe = defaultdict(list)
    log.debug(len(elves))
    movement = False
    for e in elves:
        nearby_empty = True
        for v in [(1, 0), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1), (0, 1), (0, -1)]:
            if (e[0] + v[0], e[1] + v[1]) in elves:
                nearby_empty = False
                break
        if nearby_empty:
            wannabe[e].append(e)
            continue
        for i in range(4):
            broken = False
            if (i + phase) % 4 == 0:
                # look_north()
                if (
                    (e[0], e[1] - 1) not in elves
                    and (e[0] - 1, e[1] - 1) not in elves
                    and (e[0] + 1, e[1] - 1) not in elves
                ):
                    wannabe[(e[0], e[1] - 1)].append(e)
                    broken = True
                    break
            elif (i + phase) % 4 == 1:
                # look_south()
                if (
                    (e[0], e[1] + 1) not in elves
                    and (e[0] - 1, e[1] + 1) not in elves
                    and (e[0] + 1, e[1] + 1) not in elves
                ):
                    wannabe[(e[0], e[1] + 1)].append(e)
                    broken = True
                    break
            elif (i + phase) % 4 == 2:
                # look_west()
                if (
                    (e[0] - 1, e[1]) not in elves
                    and (e[0] - 1, e[1] - 1) not in elves
                    and (e[0] - 1, e[1] + 1) not in elves
                ):
                    wannabe[(e[0] - 1, e[1])].append(e)
                    broken = True
                    break
            elif (i + phase) % 4 == 3:
                # look_east()
                if (
                    (e[0] + 1, e[1]) not in elves
                    and (e[0] + 1, e[1] - 1) not in elves
                    and (e[0] + 1, e[1] + 1) not in elves
                ):
                    wannabe[(e[0] + 1, e[1])].append(e)
                    broken = True
                    break
        if not broken:
            wannabe[e].append(e)
    new_elves = defaultdict(bool)
    log.debug(f"Wannabe {wannabe}")
    for k in wannabe:
        if len(wannabe[k]) > 1:
            for e in wannabe[k]:
                new_elves[e] = True
        else:
            new_elves[k] = True
            if k not in elves:
                movement = True
    return new_elves, movement


def part1(in_data, test=False):
    elves = parse_data(in_data)
    no_elves = len(elves)
    log.error(no_elves)
    movement = True
    phase = 0
    for i in tqdm(range(10)):
        new_elves, movement = move_alg(elves, phase)
        phase += 1
        elves = new_elves
        # log.debug(f"No of elves: {len(elves)}")
        # debug_map = Map2d.from_obstacle_list(elves)
        # log.debug(debug_map)
    min_x = min([e[0] for e in elves])
    min_y = min([e[1] for e in elves])
    max_x = max([e[0] for e in elves])
    max_y = max([e[1] for e in elves])
    log.debug(max_x - min_x + 1)
    log.debug(max_y - min_y + 1)
    return (max_x + 1 - min_x) * (max_y + 1 - min_y) - no_elves


def part2(in_data, test=False):
    elves = parse_data(in_data)
    dict_elves = defaultdict(bool)
    for e in elves:
        dict_elves[e] = True
    no_elves = len(elves)
    log.error(no_elves)
    movement = True
    phase = 0
    counter = 0
    for i in tqdm(range(100000)):
        new_elves, movement = move_alg(dict_elves, phase)
        phase += 1
        dict_elves = new_elves
        counter += 1
        if not movement:
            break
        # log.debug(f"No of elves: {len(elves)}")
        # debug_map = Map2d.from_obstacle_list(elves)
        # log.debug(debug_map)
    # min_x = min([e[0] for e in elves])
    # min_y = min([e[1] for e in elves])
    # max_x = max([e[0] for e in elves])
    # max_y = max([e[1] for e in elves])
    # log.debug(max_x-min_x+1)
    # log.debug(max_y-min_y+1)
    return counter
