# test 2024-17

import pytest

from aoc.year2024.day17 import part1, part2

simple_test = """Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
"""


def test_part1():
    cases = [
        {
            "label": "simple",
            "input": {
                "in_data": simple_test,
                "test": True,
            },
            "output": "4,6,3,5,6,3,5,2,1,0",
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
