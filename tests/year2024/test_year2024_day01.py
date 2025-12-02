# test 2024-01
# vim: nomodeline

import pytest

from aoc.year2024.day01 import part1, part2


def test_part1():
    cases = [
        {
            "label": "small",
            "input": {
                "in_data": """3   4
4   3
2   5
1   3
3   9
3   3
"""
            },
            "output": "11",
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
            "label": "small",
            "input": {
                "in_data": """3   4
4   3
2   5
1   3
3   9
3   3
"""
            },
            "output": "31",
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
