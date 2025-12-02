# test 2023-12
# vim: nomodeline

import pytest

from aoc.year2023.day12 import part1, part2

in_data1 = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""
part1_ans = "21"


def test_part1():
    assert str(part1(in_data1)) == part1_ans


in_data2 = in_data1
part2_ans = "525152"


def test_part2():
    assert str(part2(in_data2)) == part2_ans
