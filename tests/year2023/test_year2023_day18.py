# test 2023-18

import pytest

from aoc.year2023.day18 import part1, part2

in_data1 = """R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
"""
part1_ans = "62"


def test_part1():
    assert str(part1(in_data1)) == part1_ans


in_data2 = in_data1
part2_ans = "952408144115"


def test_part2():
    assert str(part2(in_data2)) == part2_ans
