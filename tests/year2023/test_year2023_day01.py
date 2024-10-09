# test 2023-1

import pytest

from aoc.year2023.day01 import part1, part2

in_data = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
"""

part1_ans = "142"


def test_part1():
    assert str(part1(in_data)) == part1_ans


in_data2 = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
"""
part2_ans = "281"


def test_part2():
    assert str(part2(in_data2)) == part2_ans
