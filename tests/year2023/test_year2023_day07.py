# test 2023-7
# vim: nomodeline

import pytest

from aoc.year2023.day07 import part1, part2

in_data1 = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""
part1_ans = "6440"


def test_part1():
    assert str(part1(in_data1)) == part1_ans


in_data2 = in_data1
part2_ans = "5905"


def test_part2():
    assert str(part2(in_data2)) == part2_ans
