# test 2024-11

import pytest

from aoc.year2024.day11 import part1, part2

simple_test = """125 17
"""


def test_part1():
    cases = [
        {
            "label": "simple",
            "input": {"in_data": simple_test},
            "output": "55312",
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


# def test_part2():
#     cases = [
#         {
#             "label": "small",
#             "input": {
#                 "in_data": simple_test
#             },
#             "output": "part2 output 2024-11",
#             "ex": None,
#         },
#     ]
#     for case in cases:
#         try:
#             output = part2(**case["input"])
#             assert str(output) == str(case["output"]), "case '{}', output: exp {}, got {}".format(
#                 case["label"], case["output"], output
#             )
#         except Exception as e:
#             assert type(e) == case["ex"], "case '{}', ex: exp {}, got {}".format(case["label"], case["ex"], type(e))
