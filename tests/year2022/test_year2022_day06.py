# test 2022-6

import pytest

from aoc.year2022.day06 import part1, part2

in_data = """mjqjpqmgbljsphdztnvjfqwrcgsmlb
"""

part1_ans = "7"
part2_ans = "19"


def test_part1():
    assert str(part1(in_data)) == part1_ans


def test_part2():
    assert str(part2(in_data)) == part2_ans
