# test 2023-13

import pytest

from aoc.year2023.day13 import part1, part2

in_data1 = """#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
"""
part1_ans = "405"


def test_part1():
    assert str(part1(in_data1)) == part1_ans


in_data2 = in_data1
part2_ans = "400"


def test_part2():
    assert str(part2(in_data2)) == part2_ans
