# test 2022-5
# vim: nomodeline

import pytest

from aoc.year2022.day05 import part1, part2

in_data = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""

part1_ans = "CMZ"
part2_ans = "MCD"


def test_part1():
    assert str(part1(in_data)) == part1_ans


def test_part2():
    assert str(part2(in_data)) == part2_ans
