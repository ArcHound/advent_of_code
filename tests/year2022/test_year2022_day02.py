# test 2022-2
# vim: nomodeline

import pytest

from aoc.year2022.day02 import part1, part2

in_data = """A Y
B X
C Z
"""

part1_ans = "15"
part2_ans = "12"


def test_part1():
    assert str(part1(in_data)) == part1_ans


def test_part2():
    assert str(part2(in_data)) == part2_ans
