# test 2018-01

import pytest

from aoc.year2018.day01 import part1, part2


def test_part1():
    cases = [
        {
            "label": "small",
            "input": {
                "in_data": """+1
+1
-2
"""
            },
            "output": "0",
            "ex": None,
        },
    ]
    for case in cases:
        try:
            output = part1(**case["input"])
            assert str(output) == str(case["output"]), (
                "case '{}', output: exp {}, got {}".format(
                    case["label"], str(case["output"]), str(output)
                )
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(
                case["label"], case["ex"], type(e)
            )


def test_part2():
    cases = [
        {
            "label": "small",
            "input": {
                "in_data": """+1
+1
-2
"""
            },
            "output": "part2 output 2018-01",
            "ex": None,
        },
    ]
    for case in cases:
        try:
            output = part2(**case["input"])
            assert str(output) == str(case["output"]), (
                "case '{}', output: exp {}, got {}".format(
                    case["label"], str(case["output"]), str(output)
                )
            )
        except Exception as e:
            assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(
                case["label"], case["ex"], type(e)
            )
