# test 2019-15

import pytest

from aoc.year2019.day15 import part1, part2

in_data1 = """
"""
part1_ans = "part1 output 2019-15"


def test_part1():
    assert str(part1(in_data1, True)) == part1_ans


in_data2 = in_data1
part2_ans = "part2 output 2019-15"


def test_part2():
    assert str(part2(in_data2, True)) == part2_ans
