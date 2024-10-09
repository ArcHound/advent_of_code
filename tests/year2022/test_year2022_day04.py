# test 2022-4

import pytest

from aoc.year2022.day04 import part1, part2

in_data = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
"""

part1_ans = "2"
part2_ans = "4"


def test_part1():
    assert str(part1(in_data)) == part1_ans


def test_part2():
    assert str(part2(in_data)) == part2_ans
