# test 2023-10

import pytest

from aoc.year2023.day10 import part1, part2

in_data1 = """..F7.
.FJ|.
SJ.L7
|F--J
LJ...
"""
part1_ans = "8"


def test_part1():
    assert str(part1(in_data1)) == part1_ans


in_data2 = """FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
"""
part2_ans = "10"

in_data2_2 = """.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
"""


def test_part2():
    assert str(part2(in_data2)) == part2_ans
    assert str(part2(in_data2_2)) == "8"
