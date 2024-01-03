# test 2019-1

import pytest

from aoc.year2019.day1 import part1, part2

in_data1 = """12
14
1969
100756
"""
part1_ans = "34241"


def test_part1():
    assert str(part1(in_data1)) == part1_ans


in_data2 = in_data1
part2_ans = "51316"


def test_part2():
    assert str(part2(in_data2)) == part2_ans
