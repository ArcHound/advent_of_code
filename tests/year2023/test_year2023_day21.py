# test 2023-21

import pytest

from aoc.year2023.day21 import part1, part2

in_data1 = """...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
"""
part1_ans = "16"


def test_part1():
    assert str(part1(in_data1, True)) == part1_ans


in_data2 = in_data1
part2_ans = "part2 output 2023-21"


def test_part2():
    assert str(part2(in_data2)) == part2_ans
