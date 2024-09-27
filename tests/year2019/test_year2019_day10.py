# test 2019-10

import pytest

from aoc.year2019.day10 import part1, part2

in_data1 = """
"""
part1_ans = "part1 output 2019-10"

cases = {
    1: (
        """.#..#
.....
#####
....#
...##""",
        8,
    ),
    2: (
        """#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.""",
        35,
    ),
    3: (
        """.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##""",
        210,
    ),
}


def test_part1():
    for case in cases:
        assert str(part1(cases[case][0], True)) == str(cases[case][1])


in_data2 = """.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##"""
part2_ans = "802"


def test_part2():
    assert str(part2(in_data2, True)) == part2_ans