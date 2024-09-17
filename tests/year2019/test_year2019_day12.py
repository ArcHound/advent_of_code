# test 2019-12

import pytest

from aoc.year2019.day12 import part1, part2

in_data1 = """<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>
"""
part1_ans = "1940"


def test_part1():
    assert str(part1(in_data1, True)) == part1_ans


in_data2 = in_data1
part2_ans = "4686774924"


def test_part2():
    assert str(part2(in_data2, True)) == part2_ans
