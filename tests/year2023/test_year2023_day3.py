# test 2023-3

import pytest

from aoc.year2023.day3 import part1, part2

in_data1 = """
"""
part1_ans = "part1 output 2023-3"

def test_part1():
    assert str(part1(in_data1)) == part1_ans

in_data2 = in_data1
part2_ans = "part2 output 2023-3"

def test_part2():
    assert str(part2(in_data2)) == part2_ans
        
        
