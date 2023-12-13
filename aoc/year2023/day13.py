# 2023-13
import logging
from aoc_lib.map2d import Map2d

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    maps = list()
    buf = ""
    x_len = 0
    y_len = 0
    for line in in_data.splitlines():
        if line != "":
            buf += line.strip()
            y_len += 1
            x_len = len(line.strip())
        else:
            maps.append(Map2d(buf, ((0, 0), (x_len, y_len))))
            buf = ""
            y_len = 0
    maps.append(Map2d(buf, ((0, 0), (x_len, y_len))))
    return maps


def part1(in_data):
    maps = parse_data(in_data)
    log.debug(maps)
    total = 0
    for m in maps:
        (
            h_axis,
            v_axis,
        ) = (
            m.find_reflection_axes()
        )  # this method is pretty general, into the lib it goes
        if not h_axis:
            h_axis = 0
        if not v_axis:
            v_axis = 0
        total += 100 * h_axis + v_axis
    return total


def part2(in_data):
    maps = parse_data(in_data)
    log.debug(maps)
    total = 0
    # idea is to find axes (axii?) as before, but allow (and require!) a set number of mistakes in the reflection
    # this should be faster than flipping each position on the map and searching for axes and comparing differences with original
    total_mistakes = 1
    for m in maps:
        # so here is the method hidden in part1 - ripped from the lib
        # horizontal
        h_axis = None
        log.debug("horizontal")
        for j in range(1, m.y_len):  # for each horizontal axis
            mistakes = 0  # no mistakes yet
            log.debug(f"j: {j}")
            match = True
            for k in range(
                1, min([j, m.y_len - j]) + 1
            ):  # for each distance from the axis that falls into bounds
                log.debug(f"k: {k}")
                for i in range(0, m.x_len):  # for each vertical point
                    log.debug(f"i: {i}")
                    if m.get_obstacle_from_point(
                        (i, j + k - 1)
                    ) != m.get_obstacle_from_point(
                        (i, j - k)
                    ):  # check the match
                        log.debug("mistake!")
                        log.debug(f"{(i,j-k)}: {m.get_obstacle_from_point((i,j-k))}")
                        log.debug(
                            f"{(i,j+k-1)}: {m.get_obstacle_from_point((i,j+k-1))}"
                        )
                        mistakes += 1
                        if mistakes > total_mistakes:
                            log.debug(
                                "too many mistakes, i break"
                            )  # we can abandon it all if we found too many mistakes
                            match = False
                            break
                if not match:
                    log.debug("k break")
                    break
            if match:
                if mistakes == total_mistakes:  # enforce the mistake
                    log.debug("exactly one mistake, j break")
                    h_axis = j
                    break
        # vertical
        # same as above, just the x,y i,j are switched
        v_axis = None
        for i in range(1, m.x_len):
            mistakes = 0
            match = True
            for k in range(1, min([i, m.x_len - i]) + 1):
                for j in range(0, m.y_len):
                    if m.get_obstacle_from_point(
                        (i + k - 1, j)
                    ) != m.get_obstacle_from_point((i - k, j)):
                        mistakes += 1
                        if mistakes > total_mistakes:
                            match = False
                            break
                if not match:
                    break
            if match:
                if mistakes == total_mistakes:
                    v_axis = i
                    break
        if not h_axis:
            h_axis = 0
        if not v_axis:
            v_axis = 0
        total += 100 * h_axis + v_axis
        log.debug("----------------")
    return total
