# 2025-01

import logging

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    data = list()
    for line in in_data.splitlines():
        data.append((line[0], int(line[1:])))
    return data


def part1(in_data, test=False):
    data = parse_data(in_data)
    state = 50
    counter = 0
    for d, n in data:
        if d == "L":
            state = (100 + state - n) % 100
        elif d == "R":
            state = (state + n) % 100
        if state == 0:
            counter += 1
    return counter


def part2(in_data, test=False):
    data = parse_data(in_data)
    state = 50
    counter = 0
    log.debug(state)
    for d, n in data:
        log.debug(f"{d} {n}")
        if d == "L":
            state = state - n
            if state <= 0:
                log.debug("turned left")
                if (state + n != 0) or (n >= 100):
                    log.debug(state)
                    counter += (-1) * state // 100
                    if state + n > 0:
                        counter += 1
                    log.debug(f"L counter {counter}")
                state = ((n // 100) * 100 + state) % 100
        elif d == "R":
            state = state + n
            if state >= 100:
                log.debug("turned right")
                counter += (state) // 100
                state = state % 100
                log.debug(f"R counter {counter}")
        log.debug(state)
    return counter
