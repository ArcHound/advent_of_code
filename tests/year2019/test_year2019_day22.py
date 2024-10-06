# test 2019-22

import pytest

from aoc.year2019.day22 import part1, part2

in_data1 = """deal into new stack
cut -2
deal with increment 7
cut 8
cut -4
deal with increment 7
cut 3
deal with increment 9
deal with increment 3
cut -1
"""
part1_ans = "1"

simple = """deal with increment 3
"""
simple_ans = "6"

simple_cut = """cut 3
"""
simple_cut_ans = "9"

negative_cut = """cut -4
"""
negative_cut_ans = "6"


def test_part1():
    assert str(part1(simple, True)) == simple_ans
    assert str(part1(simple_cut, True)) == simple_cut_ans
    assert str(part1(negative_cut, True)) == negative_cut_ans
    # assert str(part1(in_data1, True)) == part1_ans


in_data2 = in_data1
part2_ans = "part2 output 2019-22"

# def test_part2():
#     assert str(part2(in_data2, True)) == part2_ans
