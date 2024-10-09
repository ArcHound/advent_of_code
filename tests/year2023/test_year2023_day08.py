# test 2023-8

import pytest

from aoc.year2023.day08 import part1, part2

in_data1 = """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
"""
part1_ans = "2"


def test_part1():
    assert str(part1(in_data1)) == part1_ans


in_data2 = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
"""
part2_ans = "6"


def test_part2():
    assert str(part2(in_data2)) == part2_ans
