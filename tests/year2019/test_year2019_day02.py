# test 2019-2
# vim: nomodeline

import pytest

from aoc.year2019.day02 import part1, part2

in_data1 = """1,9,10,3,2,3,11,0,99,30,40,50
"""
part1_ans = "3500"


def test_part1():
    assert str(part1(in_data1, True)) == part1_ans


in_data2 = in_data1
part2_ans = "part2 output 2019-2"


# def test_part2():
#     assert str(part2(in_data2, True)) == part2_ans
