# test 2023-22

import pytest

from aoc.year2023.day22 import part1, part2

in_data1 = """1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9
"""
part1_ans = "5"


def test_part1():
    assert str(part1(in_data1)) == part1_ans


in_data2 = in_data1
part2_ans = "7"


def test_part2():
    assert str(part2(in_data2)) == part2_ans
