import pytest

from aoc.year2022.day01 import part1, part2

in_data = """1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
"""

part1_ans = "24000"
part2_ans = "45000"


def test_part1():
    assert str(part1(in_data)) == part1_ans


def test_part2():
    assert str(part2(in_data)) == part2_ans
