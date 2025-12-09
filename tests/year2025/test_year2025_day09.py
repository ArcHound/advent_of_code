# test 2025-09
# vim: nomodeline

import pytest

from aoc.year2025.day09 import part1, part2

simple_test = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
"""


def test_part1():
    cases = [
        {
            "label": "simple",
            "input": {
                "in_data": simple_test,
                "test": True,
            },
            "output": "50",
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
            "output": "24",
            "ex": None,
        },
        {
            "label": "v",
            "input": {
                "in_data": """0,0
                0,10
                10,10
                10,20
                20,20
                20,30
                30,30
                30,20
                40,20
                40,10
                50,10
                50,0
                30,0
                30,10
                20,10
                20,0""",
                "test": True,
            },
            "output": "341",
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
