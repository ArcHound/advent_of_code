# test 2023-3

import pytest

from aoc.year2023.day03 import part1, part2

in_data1 = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""
part1_ans = "4361"


def test_part1():
    assert str(part1(in_data1)) == part1_ans


in_data2 = in_data1
part2_ans = "467835"


def test_part2():
    assert str(part2(in_data2)) == part2_ans
