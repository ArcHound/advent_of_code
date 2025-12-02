# test 2023-16
# vim: nomodeline

import pytest

from aoc.year2023.day16 import part1, part2

in_data1 = r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
"""
part1_ans = "46"


def test_part1():
    assert str(part1(in_data1)) == part1_ans


in_data2 = in_data1
part2_ans = "51"


def test_part2():
    assert str(part2(in_data2)) == part2_ans
