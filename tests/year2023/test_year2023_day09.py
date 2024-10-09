# test 2023-9

import pytest

from aoc.year2023.day09 import part1, part2

in_data1 = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""
part1_ans = "114"


def test_part1():
    assert str(part1(in_data1)) == part1_ans


in_data2 = in_data1
part2_ans = "2"


def test_part2():
    assert str(part2(in_data2)) == part2_ans
