# test 2023-11

import pytest

from aoc.year2023.day11 import part1, part2

in_data1 = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
"""
part1_ans = "374"


def test_part1():
    assert str(part1(in_data1)) == part1_ans


in_data2 = in_data1
part2_ans = "82000210"


def test_part2():
    assert str(part2(in_data2)) == part2_ans
