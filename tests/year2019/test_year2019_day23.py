# test 2019-23

import pytest

from aoc.year2019.day23 import part1, part2

in_data1 = """3,90,1005,90,18,1101,0,1,91,4,91,104,1011,104,1,1105,1,22,1101,0,0,91,3,92,1007,92,0,94,1005,94,22,3,93,1002,93,2,93,1005,90,54,1007,93,65536,95,1005,95,51,1101,0,1,93,1105,1,72,1007,93,256,96,1005,96,68,1101,0,255,91,1105,1,72,1101,0,0,91,4,91,4,92,4,93,1105,1,22,99
"""
part1_ans = "512"


# def test_part1():
#     assert str(part1(in_data1, True)) == part1_ans


in_data2 = in_data1
part2_ans = "512"


# def test_part2():
#     assert str(part2(in_data2, True)) == part2_ans
