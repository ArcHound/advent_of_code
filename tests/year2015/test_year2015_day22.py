# test 2015-22
# vim: nomodeline

import pytest

from aoc.year2015.day22 import part1, part2

simple_test = """Hit Points: 13
Damage: 8
"""

simple_test_2 = """Hit Points: 14
Damage: 8
"""


def test_part1():
    cases = [
        {
            "label": "simple",
            "input": {
                "in_data": simple_test,
                "test": True,
            },
            "output": "226",
            "ex": None,
        },
        {
            "label": "simple 2",
            "input": {
                "in_data": simple_test_2,
                "test": True,
            },
            "output": "641",
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
