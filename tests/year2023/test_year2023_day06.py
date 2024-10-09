# test 2023-6

import pytest

from aoc.year2023.day06 import part1, part2

in_data1 = """Time:      7  15   30
Distance:  9  40  200
"""
part1_ans = "288"


def test_part1():
    assert str(part1(in_data1)) == part1_ans


in_data2 = in_data1
part2_ans = "71503"


def test_part2():
    assert str(part2(in_data2)) == part2_ans
