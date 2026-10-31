# test 2016-15
# vim: nomodeline

import pytest

from aoc.year2016.day15 import part1, part2

simple_test = """Disc #1 has 5 positions; at time=0, it is at position 4.
Disc #2 has 2 positions; at time=0, it is at position 1.
"""


def test_part1():
    cases = [
        {
            "label": "simple",
            "input": {
                "in_data": simple_test,
                "test": True,
            },
            "output": "5",
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
