# test 2019-16
# vim: nomodeline

import pytest

from aoc.year2019.day16 import part1, part2

in_data1 = """12345678
"""
part1_ans = "01029498"


def test_part1():
    assert str(part1(in_data1, True)) == part1_ans
