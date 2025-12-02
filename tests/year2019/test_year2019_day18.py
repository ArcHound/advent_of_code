# test 2019-18
# vim: nomodeline

import pytest

from aoc.year2019.day18 import part1, part2

in_data0 = """#########
#b.A.@.a#
#########
"""
part0_ans = "8"

in_data1 = """#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################
"""
part1_ans = "136"

in_data2 = """########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################
"""

part2_ans = "86"

in_data3 = """########################
#@..............ac.GI.b#
###d#e#f################
###A#B#C################
###g#h#i################
########################
"""

part3_ans = "81"


# def test_part1():
#     assert str(part1(in_data1, True)) == part1_ans


# in_data2 = in_data1
# part2_ans = "part2 output 2019-18"

in_data4 = """#############
#DcBa.#.GhKl#
#.###...#I###
#e#d#.@.#j#k#
###C#...###J#
#fEbA.#.FgHi#
#############
"""

part4_ans = "32"


def test_part2():
    assert str(part2(in_data4, True)) == part4_ans
