# test 2023-15

import pytest

from aoc.year2023.day15 import part1, part2

in_data1 = """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
"""
part1_ans = "1320"


def test_part1():
    assert str(part1(in_data1)) == part1_ans


in_data2 = in_data1
part2_ans = "145"


def test_part2():
    assert str(part2(in_data2)) == part2_ans
