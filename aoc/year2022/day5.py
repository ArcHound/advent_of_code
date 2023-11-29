# 2022-5
import logging
import dataclasses
from collections import defaultdict

log = logging.getLogger("aoc_logger")


@dataclasses.dataclass
class Move:
    count: int
    source: int
    target: int


def process_move(move):
    tokens = move.split()
    return Move(count=int(tokens[1]), source=int(tokens[3]), target=int(tokens[5]))


def process_stacks(stacks):
    result_stacks = defaultdict(list)
    for s in stacks:
        if s == "":
            continue
        for i in range(len(s)):
            if i % 4 == 0:
                if s[i] == "[":
                    result_stacks[(i // 4) + 1].append(s[i : i + 3])
                    log.debug(str((i // 4) + 1) + " " + s[i : i + 3])
    return result_stacks


def make_moves(stacks, moves):
    for move in moves:
        log.debug("-------")
        log.debug(move)
        log.debug(stacks[move.source])
        buf = stacks[move.source][: move.count]
        buf.reverse()
        stacks[move.target] = buf + stacks[move.target]
        stacks[move.source] = stacks[move.source][move.count :]
        log.debug(stacks[move.source])
        log.debug(stacks[move.target])
    return stacks


def make_moves2(stacks, moves):
    for move in moves:
        log.debug("-------")
        log.debug(move)
        log.debug(stacks[move.source])
        buf = stacks[move.source][: move.count]
        # buf.reverse()
        stacks[move.target] = buf + stacks[move.target]
        stacks[move.source] = stacks[move.source][move.count :]
        log.debug(stacks[move.source])
        log.debug(stacks[move.target])
    return stacks


def print_top_level(stacks):
    string = ""
    for i in range(len(stacks)):
        string += stacks[i + 1][0][1:-1]
        log.debug(string)
    return string


def part1(in_data):
    state = "stacks"
    moves = list()
    stack_list = list()
    for l in in_data.splitlines():
        if state == "stacks":
            if "move" in l:
                state = "moves"
                stacks = process_stacks(stack_list)
                moves.append(process_move(l))
            else:
                stack_list.append(l)
        elif state == "moves":
            moves.append(process_move(l))
    new_stacks = make_moves(stacks, moves)
    return print_top_level(new_stacks)


def part2(in_data):
    state = "stacks"
    moves = list()
    stack_list = list()
    for l in in_data.splitlines():
        if state == "stacks":
            if "move" in l:
                state = "moves"
                stacks = process_stacks(stack_list)
                moves.append(process_move(l))
            else:
                stack_list.append(l)
        elif state == "moves":
            moves.append(process_move(l))
    new_stacks = make_moves2(stacks, moves)
    return print_top_level(new_stacks)
