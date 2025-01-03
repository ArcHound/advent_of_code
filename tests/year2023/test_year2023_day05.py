# test 2023-5

import pytest

from aoc.year2023.day05 import part1, part2

in_data1 = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""
part1_ans = "35"


def test_part1():
    assert str(part1(in_data1)) == part1_ans


in_data2 = in_data1
part2_ans = "46"


def test_part2():
    assert str(part2(in_data2)) == part2_ans
