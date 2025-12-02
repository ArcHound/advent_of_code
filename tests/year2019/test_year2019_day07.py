# test 2019-7
# vim: nomodeline

import pytest

from aoc.year2019.day07 import part1, part2

in_data1 = """3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0
"""
part1_ans = "43210"


def test_part1():
    assert str(part1(in_data1, True)) == part1_ans


in_data2 = """3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5
"""
part2_ans = "139629729"


def test_part2():
    assert str(part2(in_data2, True)) == part2_ans
