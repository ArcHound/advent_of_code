# test 2019-6
# vim: nomodeline

import pytest

from aoc.year2019.day06 import part1, part2

in_data1 = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
"""
part1_ans = "42"


def test_part1():
    assert str(part1(in_data1, True)) == part1_ans


in_data2 = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN
"""
part2_ans = "4"


def test_part2():
    assert str(part2(in_data2, True)) == part2_ans
