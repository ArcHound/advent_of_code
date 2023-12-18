# test 2023-17

import pytest

from aoc.year2023.day17 import part1, part2

in_data1 = """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
"""
part1_ans = "102"


def test_part1():
    assert str(part1(in_data1)) == part1_ans


in_data2 = in_data1
part2_ans = "94"


def test_part2():
    assert str(part2(in_data2)) == part2_ans
