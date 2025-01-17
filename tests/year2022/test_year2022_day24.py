# test 2022-24

import pytest

from aoc.year2022.day24 import part1, part2

simple_test = """#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#
"""


def test_part1():
    cases = [
        {
            "label": "simple",
            "input": {
                "in_data": simple_test,
                "test": True,
            },
            "output": "18",
            "ex": None,
        },
    ]
    for case in cases:
        try:
            output = part1(**case["input"])
            assert str(output) == str(
                case["output"]
            ), "case '{}', output: exp {}, got {}".format(
                case["label"], case["output"], output
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(
                case["label"], case["ex"], type(e)
            )


def test_part2():
    cases = [
        {
            "label": "simple",
            "input": {
                "in_data": simple_test,
                "test": True,
            },
            "output": "54",
            "ex": None,
        },
    ]
    for case in cases:
        try:
            output = part2(**case["input"])
            assert str(output) == str(
                case["output"]
            ), "case '{}', output: exp {}, got {}".format(
                case["label"], case["output"], output
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(
                case["label"], case["ex"], type(e)
            )
