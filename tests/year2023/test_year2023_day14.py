# test 2023-14

import pytest

from aoc.year2023.day14 import part1, part2

in_data1 = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""
part1_ans = "136"


def test_part1():
    assert str(part1(in_data1)) == part1_ans


in_data2 = in_data1
part2_ans = "64"


def test_part2():
    assert str(part2(in_data2)) == part2_ans
