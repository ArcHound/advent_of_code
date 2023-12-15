# 2023-15
import logging
from collections import defaultdict

log = logging.getLogger("aoc_logger")


def parse_data(in_data):
    vals = list()
    for line in in_data.splitlines():
        vals += line.strip().split(",")
    return vals


# code to spec, no creativity
def aoc_hash(s):
    checksum = 0
    for c in s:
        checksum += ord(c)
        checksum *= 17
        checksum %= 256
    return checksum


def part1(in_data):
    vals = parse_data(in_data)
    return sum([aoc_hash(v) for v in vals])


def part2(in_data):
    vals = parse_data(in_data)
    boxes = defaultdict(
        lambda: defaultdict(int)
    )  # no need to bother with inits this way
    # code to spec, no creativity
    for v in vals:
        if "=" in v:
            p = v.split("=")
            label = p[0]
            val = int(p[1])
            boxnum = aoc_hash(label)
            boxes[boxnum][label] = val
        elif "-" in v:
            label = v[:-1]
            boxnum = aoc_hash(label)
            if label in boxes[boxnum]:
                del boxes[boxnum][label]
        else:
            raise ValueError("WTF value")
        log.debug(boxes)
    count = 0
    # code to spec, no creativity
    for boxnum, items in boxes.items():
        i = 0
        for label, value in items.items():
            count += (boxnum + 1) * (i + 1) * value
            i += 1
    return count
