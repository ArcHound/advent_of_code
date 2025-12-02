# test 2023-25
# vim: nomodeline

import pytest

from aoc.year2023.day25 import part1, part2

in_data1 = """jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr
"""
part1_ans = "54"


def test_part1():
    assert str(part1(in_data1, True)) == part1_ans


in_data2 = in_data1
part2_ans = "Push that button already!"


def test_part2():
    assert str(part2(in_data2)) == part2_ans
