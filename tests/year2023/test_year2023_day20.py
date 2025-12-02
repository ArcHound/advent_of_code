# test 2023-20
# vim: nomodeline

import pytest

from aoc.year2023.day20 import part1, part2

in_data1 = """broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output
"""
part1_ans = "11687500"


def test_part1():
    assert str(part1(in_data1)) == part1_ans


# don't think I'll be able to come up with a test case here
# in_data2 = in_data1
# part2_ans = "part2 output 2023-20"

# def test_part2():
#     assert str(part2(in_data2)) == part2_ans
