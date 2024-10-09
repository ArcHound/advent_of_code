# test 2019-4

import pytest

from aoc.year2019.day04 import check

part1 = {
    111111: True,
    223450: False,
    123789: False,
}


def test_part1():
    for k in part1:
        assert check(k, False) == part1[k]


part2 = {
    112233: True,
    123444: False,
    111122: True,
}


def test_part2():
    for k in part2:
        assert check(k, True) == part2[k]
