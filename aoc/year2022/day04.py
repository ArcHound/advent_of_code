# 2022-4

from collections import Counter


def fully_contained(ranges):
    rmin = min([r[0] for r in ranges])
    rmax = max([r[1] for r in ranges])
    return (rmin, rmax) in ranges


def single_overlap(r_1, r_2):
    return (
        (r_2[0] <= r_1[0] and r_1[0] <= r_2[1])
        or (r_2[0] <= r_1[1] and r_1[1] <= r_2[1])
        or (r_1[0] <= r_2[0] and r_2[0] <= r_1[1])
        or (r_1[0] <= r_2[1] and r_2[1] <= r_1[1])
    )


def part1(in_data):
    ranges = [
        [(int(x.split("-")[0]), int(x.split("-")[1])) for x in l.split(",")]
        for l in in_data.splitlines()
    ]
    contains = Counter([fully_contained(r) for r in ranges])
    return contains[True]


def part2(in_data):
    ranges = [
        [(int(x.split("-")[0]), int(x.split("-")[1])) for x in l.split(",")]
        for l in in_data.splitlines()
    ]
    overlaping = Counter([single_overlap(r[0], r[1]) for r in ranges])
    return overlaping[True]
