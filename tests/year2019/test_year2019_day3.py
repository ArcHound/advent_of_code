# test 2019-3

import pytest

from aoc.year2019.day3 import part1, part2

in_data1 = """R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
U98,R91,D20,R16,D67,R40,U7,R15,U6,R7
"""
part1_1ans = "135"
part2_1ans = "410"

in_data2 = """R75,D30,R83,U83,L12,D49,R71,U7,L72
U62,R66,U55,R34,D71,R55,D58,R83
"""
part1_2ans = "159"
part2_2ans = "610"

in_data3 = """R8,U5,L5,D3
U7,R6,D4,L4
"""
part1_3ans = "6"
part2_3ans = "30"


def test_part1():
    assert str(part1(in_data1, True)) == part1_1ans
    assert str(part1(in_data2, True)) == part1_2ans
    assert str(part1(in_data3, True)) == part1_3ans


def test_part2():
    assert str(part2(in_data1, True)) == part2_1ans
    assert str(part2(in_data2, True)) == part2_2ans
    assert str(part2(in_data3, True)) == part2_3ans
