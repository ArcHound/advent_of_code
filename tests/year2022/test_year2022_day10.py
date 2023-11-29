# test 2022-10

import pytest

from aoc.year2022.day10 import part1, part2

in_data = """
"""

part1_ans = "part1 output 2022-10"
part2_ans = "part2 output 2022-10"


def test_part1():
    assert str(part1(in_data)) == part1_ans


def test_part2():
    assert str(part2(in_data)) == part2_ans
