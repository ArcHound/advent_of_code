# 2023-14
from aoc_lib.map2d import Map2d
from aoc_lib.vector2d import v_add
from tqdm import tqdm
import logging

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    # might make this a constructor at this point
    buf = ""
    x_len = 0
    y_len = 0
    for line in in_data.splitlines():
        if line != "":
            buf += line.strip()
            y_len += 1
            x_len = len(line.strip())
    return Map2d(buf, ((0, 0), (x_len, y_len)))


def gravity(map2d, diff=(0, -1)):
    # naive approach - scan it, if something moved let us know
    new_map = Map2d(map2d.obstacle_str, (map2d.minimal, map2d.maximal))
    motion = False
    for i in range(
        len(map2d.obstacle_str)
    ):  # how did this work? we should look at the diff to know the direction of scanning, no?
        if map2d.obstacle_str[i] == "O":
            p = map2d.translate_index(i)
            # if we have an empty space in the place we're going to we can go there
            if (
                map2d.in_bounds_point(v_add(p, diff))
                and map2d.get_point(v_add(p, diff)) == "."
            ):
                new_map.set_point(v_add(p, diff), "O")
                new_map.set_point(p, ".")
                motion = True
    return new_map, motion


def eval_map(m):
    # function that evals the number associated with the configuration
    count = 0
    i = 0
    for line in m.debug_draw().splitlines()[1:]:
        for c in line:
            if c == "O":
                count += m.y_len - i
        i += 1
    return count


def part1(in_data):
    m = parse_data(in_data)
    log.debug(m.debug_draw())
    # naive approach, do one step then recalculate
    motion = True
    while motion:
        m, motion = gravity(m)
        log.debug(m.debug_draw())
    return eval_map(m)


def cycle(map2d):
    m = map2d
    # this is the order of the directions
    for diff in [(0, -1), (-1, 0), (0, 1), (1, 0)]:
        motion = True
        # surprisingly slow, but no intent to optimize
        while motion:
            m, motion = gravity(m, diff)
    return m


def brent(f, x0):
    # a confession - I don't recall this algorithm exactly, I know it's for cycle detection
    # https://en.wikipedia.org/wiki/Cycle_detection#Brent's_algorithm
    power = 1
    lam = 1
    tortoise = x0
    hare = f(x0)
    log.info("start")
    while tortoise != hare:
        if power == lam:
            tortoise = hare
            power *= 2
            log.info(power)
            lam = 0
        hare = f(hare)
        lam += 1
    log.info("first cycle done")
    tortoise = x0
    hare = x0
    log.info(f"brent lam {lam}")
    for i in range(lam):
        hare = f(hare)
    log.info("second cycle done")

    mu = 0
    while tortoise != hare:
        tortoise = f(tortoise)
        hare = f(hare)
        mu += 1
    log.info("third cycle done")

    return lam, mu


def part2(in_data):
    # intuition tells me that such a constrained environment must end in a stable state.
    # fortunately, my intuition was right
    # We need to find that cycle
    cycles = 1000000000
    m = parse_data(in_data)
    lam, mu = brent(cycle, m)  # using the brent algorithm for cycle detection
    log.info(f"period: {lam}")
    log.info(f"offset: {mu}")
    offset = (
        cycles - (cycles // lam) * lam + ((mu // lam) + 1) * lam
    )  # find the place that's in the cycle and after the offset
    log.info(f"New offset: {offset}")
    for i in range(offset):
        log.debug(f"{i}: {eval_map(m)}")  # just go there
        m = cycle(m)
    return eval_map(m)
