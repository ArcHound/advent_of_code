# test 2023-24
# vim: nomodeline

import pytest

from aoc.year2023.day24 import part1, part2

in_data1 = """19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3
"""
part1_ans = "2"


def test_part1():
    assert str(part1(in_data1, test=True)) == part1_ans


in_data2 = in_data1
part2_ans = "47"


def test_part2():
    assert str(part2(in_data2)) == part2_ans
