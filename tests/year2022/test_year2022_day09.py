# test 2022-9
# vim: nomodeline

import pytest

from aoc.year2022.day09 import part1, part2

in_data = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
"""

part1_ans = "13"
part2_ans = "1"


def test_part1():
    assert str(part1(in_data)) == part1_ans


def test_part2():
    assert str(part2(in_data)) == part2_ans
