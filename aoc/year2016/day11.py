# 2016-11

import logging
import dataclasses
from collections import defaultdict, deque

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = list()
    floors = ["", "", "", ""]  # fixed floor number
    fc = 0
    element_map = dict()
    el_counter = 0
    for line in in_data.splitlines():
        contents = line.split("contains ")[1]
        if contents == "nothing relevant.":
            continue
        contents = contents[:-1].replace(",", "")  # remove interpunction
        tokens = [x for x in contents.split(" ") if x not in ["a", "and"]]
        for i in range(len(tokens) // 2):
            el = tokens[2 * i].split("-")[0]
            # less than 26 elements (part 1 ok, part 2 hopefully too)
            char = ""
            if el not in element_map:
                element_map[el] = chr(ord("a") + el_counter)
                el_counter += 1
            char = element_map[el]
            t = tokens[2 * i + 1]
            # generators upper case as they are big. Microchips lower case, obv
            if t == "generator":
                char = char.upper()
            floors[fc] += char
        fc += 1
    # useless I think, but we have it
    log.debug(element_map)
    return tuple(floors)


def is_done(floors):
    return all([len(floors[i]) == 0 for i in range(len(floors) - 1)])


def is_floor_legal(floor):
    if len(floor) == 0:
        # empty floor is legal
        return True
    types = defaultdict(int)
    for item in floor:
        if item.isupper():
            types[item.lower()] += 1
        elif item.islower():
            types[item.lower()] -= 1
    # all chips, all generators or all chips have corresponding generator
    return (
        all([item.islower() for item in floor])
        or all([item.isupper() for item in floor])
        or all([types[element] >= 0 for element in types])
    )


def legal_moves(floors, elevator):
    if is_done(floors):
        return list()
    if len(floors[elevator]) == 0:
        return list()
    legal_moves = list()
    elevator_moves = list()
    if elevator != 0:
        elevator_moves.append(elevator - 1)
    if elevator != len(floors) - 1:
        elevator_moves.append(elevator + 1)
    for item in floors[elevator]:
        for e_move in elevator_moves:
            new_floors = list(floors)
            new_floors[elevator] = new_floors[elevator].replace(item, "")
            new_floors[e_move] += item
            nft = tuple(new_floors)
            if all([is_floor_legal(f) for f in nft]):
                legal_moves.append((nft, e_move))
    for i in range(len(floors[elevator])):
        for j in range(i):
            for e_move in elevator_moves:
                new_floors = list(floors)
                new_floors[elevator] = new_floors[elevator].replace(
                    floors[elevator][i], ""
                )
                new_floors[elevator] = new_floors[elevator].replace(
                    floors[elevator][j], ""
                )
                new_floors[e_move] += floors[elevator][i]
                new_floors[e_move] += floors[elevator][j]
                nft = tuple(new_floors)
                if all([is_floor_legal(f) for f in nft]):
                    # log.debug(nft)
                    legal_moves.append((nft, e_move))
    # normalize
    normalized = list()
    for nft, move in legal_moves:
        new_floors = tuple(["".join(sorted([x for x in f])) for f in nft])
        normalized.append((new_floors, move))
    return normalized


def bfs(floors, elevator):
    for floor in floors:
        assert is_floor_legal(floor)
    queue = deque([(floors, elevator, 0)])
    seen = {(floors, elevator)}
    minimum = -1
    while len(queue) > 0:
        f, e, s = queue.popleft()
        if is_done(f):
            if minimum == -1 or s < minimum:
                minimum = s
                break
        moves = legal_moves(f, e)
        for nf, ne in moves:
            if (nf, ne) not in seen:
                seen.add((nf, ne))
                queue.append((nf, ne, s + 1))
    return minimum


def part1(in_data, test=False):
    floors = parse_data(in_data)
    log.debug(floors)
    log.debug(is_done(floors))
    elevator = 0  # starting floor
    return bfs(floors, elevator)


def part2(in_data, test=False):
    floors = list(parse_data(in_data))
    elevator = 0
    log.info("start")
    og = bfs(tuple(floors), elevator)
    log.info(og)
    # ok, so there are two ideas.
    # one was to transfer the next two boxes after doing the original shuffle to add the steps
    # that wasn't it
    # then there must exist some kind of configuration that enables us to transfer boxes upwards that is then cleaned up
    # therefore I can omit a full-set to see how much steps the ladder adds
    # then I count the ladder twice
    # these differ by 2 steps. I'd say that the original idea has plenty merit IRL
    c = ""
    for i in floors[0]:
        if i.upper() in floors[0] and i.lower() in floors[0]:
            c = i
            break
    nf = floors[0].replace(c.upper(), "")
    nf = nf.replace(c.lower(), "")
    floors[0] = nf
    add_on = bfs(tuple(floors), elevator)
    log.info("done")
    return og + (og - add_on) * 2
