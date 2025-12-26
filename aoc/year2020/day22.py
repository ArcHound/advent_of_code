# 2020-22

import logging
from collections import deque

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    p1 = list()
    p2 = list()
    state = ""
    for line in in_data.splitlines():
        if "Player" in line:
            state = line.split(" ")[1][0]
        elif state == "1" and line.strip() != "":
            p1.append(int(line))
        elif state == "2" and line.strip() != "":
            p2.append(int(line))
    return p1, p2


def part1(in_data, test=False):
    p1, p2 = parse_data(in_data)
    p1 = deque(p1)
    p2 = deque(p2)
    while len(p1) != 0 and len(p2) != 0:
        c1 = p1.popleft()
        c2 = p2.popleft()
        if c1 > c2:
            p1.append(c1)
            p1.append(c2)
        else:
            p2.append(c2)
            p2.append(c1)
    p = p1 if len(p1) > 0 else p2
    total = 0
    for i in range(len(p)):
        total += (len(p) - i) * p[i]
    return total


def recursive_combat(d1, d2):
    log.debug("recursed")
    p1 = deque(d1)
    p2 = deque(d2)
    cache = set()
    while len(p1) != 0 and len(p2) != 0:
        log.debug(p1)
        log.debug(p2)
        if (tuple(p1), tuple(p2)) in cache:
            log.debug("collision")
            return True, p1, p2
        cache.add((tuple(p1), tuple(p2)))
        c1 = p1.popleft()
        c2 = p2.popleft()
        if c1 <= len(p1) and c2 <= len(p2):
            wc, rp1, rp2 = recursive_combat(deque(list(p1)[:c1]), deque(list(p2)[:c2]))
            if wc:
                p1.append(c1)
                p1.append(c2)
            else:
                p2.append(c2)
                p2.append(c1)
        elif c1 > c2:
            p1.append(c1)
            p1.append(c2)
        else:
            p2.append(c2)
            p2.append(c1)
    log.debug(f"win p1 {len(p1) > 0}")
    return len(p1) > 0, p1, p2


def part2(in_data, test=False):
    d1, d2 = parse_data(in_data)
    wc, p1, p2 = recursive_combat(d1, d2)
    p = p1 if wc else p2
    total = 0
    for i in range(len(p)):
        total += (len(p) - i) * p[i]
    return total
