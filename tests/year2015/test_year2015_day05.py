# test 2015-05
# vim: nomodeline

import pytest

from aoc.year2015.day05 import part1, part2

simple_test = """ugknbfddgicrmopn
aaa
jchzalrnumimnmhp
haegwjzuvuyypxyu
dvszwmarrgswjxmb
"""


def test_part1():
    cases = [
        {
            "label": "simple",
            "input": {
                "in_data": simple_test,
                "test": True,
            },
            "output": "2",
            "ex": None,
        },
    ]
    for case in cases:
        try:
            output = part1(**case["input"])
            assert str(output) == str(case["output"]), (
                "case '{}', output: exp {}, got {}".format(
                    case["label"], case["output"], output
                )
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(
                case["label"], case["ex"], type(e)
            )


simple_test2 = """qjhvhtzxzqqjkmpb
xxyxx
uurcxstgmygtbstg
ieodomkazucvgmuy
"""


def test_part2():
    cases = [
        {
            "label": "simple",
            "input": {
                "in_data": simple_test2,
                "test": True,
            },
            "output": "2",
            "ex": None,
        },
    ]
    for case in cases:
        try:
            output = part2(**case["input"])
            assert str(output) == str(case["output"]), (
                "case '{}', output: exp {}, got {}".format(
                    case["label"], case["output"], output
                )
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(
                case["label"], case["ex"], type(e)
            )
