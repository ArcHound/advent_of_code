# test 2024-10
# vim: nomodeline

import pytest

from aoc.year2024.day10 import part1, part2

simple_test = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""


def test_part1():
    cases = [
        {
            "label": "simple",
            "input": {"in_data": simple_test},
            "output": "36",
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
            "input": {"in_data": simple_test},
            "output": "81",
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
