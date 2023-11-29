# test 2022-8

import pytest

from aoc.year2022.day8 import part1, part2

in_data = """30373
25512
65332
33549
35390
"""

part1_ans = "21"
part2_ans = "8"


def test_part1():
    assert str(part1(in_data)) == part1_ans


def test_part2():
    assert str(part2(in_data)) == part2_ans
