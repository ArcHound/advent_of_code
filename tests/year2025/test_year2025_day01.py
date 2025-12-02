# test 2025-01

import pytest

from aoc.year2025.day01 import part1, part2

simple_test = """L68
L30
R48
L5
R60
L55
L1
L99
R14
L82
"""


def test_part1():
    cases = [
        {
            "label": "simple",
            "input": {
                "in_data": simple_test,
                "test": True,
            },
            "output": "3",
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


def test_part2():
    cases = [
        {
            "label": "simple",
            "input": {
                "in_data": simple_test,
                "test": True,
            },
            "output": "6",
            "ex": None,
        },
        {
            "label": "2L",
            "input": {
                "in_data": "L150",
                "test": True,
            },
            "output": "2",
            "ex": None,
        },
        {
            "label": "2R",
            "input": {
                "in_data": "R150",
                "test": True,
            },
            "output": "2",
            "ex": None,
        },
        {
            "label": "2R2L",
            "input": {
                "in_data": "R150\nL201",
                "test": True,
            },
            "output": "4",
            "ex": None,
        },
        {
            "label": "2L2R",
            "input": {
                "in_data": "L150\nR201",
                "test": True,
            },
            "output": "4",
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
